# -*- coding: utf-8 -*-
import streamlit as st
import os
import pandas as pd
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt

# Page configuration for wide display and title
st.set_page_config(page_title="Quant Arbitrage Analysis Model", layout="wide")

st.title("Global Forex Market Risk-Free Arbitrage Monitoring System")
st.markdown("Real-time arbitrage path discovery tool based on Graph Theory (**Bellman-Ford Algorithm**) and **Logarithmic Transformation**.")

# ==========================================
# 1. Data Engine Module
# ==========================================
# Function to load data from an external source
@st.cache_data
def load_market_data(filepath):
    # Read the generated CSV file using pandas
    df = pd.read_csv(filepath, index_col=0)
    return df

# Specify the data file name
data_file = "fx_market_large.csv"

# Check if the file exists, provide an error message if not
if not os.path.exists(data_file):
    st.error(f"Cannot find data file `{data_file}`! Please run the data generation script first.")
    st.stop()

# Load the data
df_rates = load_market_data(data_file)

# Automatically extract currency names and exchange rates from the CSV
currencies = df_rates.columns.tolist() # Get names of all currencies (e.g., 50 types)
rates = df_rates.values.tolist()       # Get the 50x50 exchange rate matrix
num_currencies = len(currencies)

# Display dataset scale in the sidebar for a professional look
st.sidebar.info(f"Dataset loaded: {num_currencies} currencies included")

# Since a 50-currency table is too large for the UI, we preview only the first 8
st.subheader(f"Market Rate Matrix Preview (Total: {num_currencies} currencies)")
st.dataframe(df_rates.iloc[:8, :8].style.format("{:.4f}"))
st.caption("Note: For display purposes, only the first 8 currencies are shown here. The algorithm processes the full network.")

df_rates = pd.DataFrame(rates, columns=currencies, index=currencies)

# Sidebar control panel
st.sidebar.header("Parameter Settings")
initial_capital = st.sidebar.number_input("Initial Capital (Simulated Units)", min_value=1000, value=10000, step=1000)
# Real financial markets involve fees; adding this detail enhances the model's realism.
fee_rate = st.sidebar.slider("Transaction Fee per Trade (%)", min_value=0.0, max_value=0.5, value=0.1, step=0.05)

# Display the current exchange rate matrix
st.subheader("Current Market Exchange Rate Matrix")
st.dataframe(df_rates.style.format("{:.4f}"))

# ==========================================
# 2. Math & Algorithm Module
# ==========================================
def bellman_ford_arbitrage(rate_matrix, currencies, fee):
    """
    Detects negative cycles (arbitrage opportunities) using the Bellman-Ford algorithm.
    """
    n = len(currencies)
    # Core mathematical conversion: Transform multiplication (rates) into addition.
    # Incorporate fee calculations: 
    # Actual Rate = Nominal Rate * (1 - fee_rate)
    # Graph Edge Weight w = -ln(Actual Rate)
    graph = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                actual_rate = rate_matrix[i][j] * (1 - fee / 100.0)
                # Prevent log errors
                if actual_rate > 0:
                    graph[i][j] = -math.log(actual_rate)
                else:
                    graph[i][j] = float('inf')
            else:
                graph[i][j] = 0

    # Initialize distance array and predecessor array
    dist = [float('inf')] * n
    dist[0] = 0  # Start from the first currency
    pred = [-1] * n

    # Bellman-Ford core step: Relax edges V-1 times
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if u != v and dist[u] + graph[u][v] < dist[v]:
                    dist[v] = dist[u] + graph[u][v]
                    pred[v] = u

    # V-th iteration to detect negative cycles
    arbitrage_path = None
    for u in range(n):
        for v in range(n):
            if u != v and dist[u] + graph[u][v] < dist[v] - 1e-8: # Adjusted for floating point precision
                # Negative cycle found, begin backtracking
                cycle = []
                curr = v
                # Step back N times to ensure we are inside the cycle
                for _ in range(n):
                    curr = pred[curr]

                # Record the cycle path
                cycle_start = curr
                cycle.append(cycle_start)
                curr = pred[curr]
                while curr != cycle_start:
                    cycle.append(curr)
                    curr = pred[curr]
                cycle.append(cycle_start)

                # Reverse path to chronological order and map to currency names
                cycle.reverse()
                arbitrage_path = [currencies[i] for i in cycle]
                return arbitrage_path

    return None

# ==========================================
# 3. Execution & Visualization Module
# ==========================================
if st.button("Scan for Arbitrage Opportunities", type="primary"):
    with st.spinner('Scanning graph network using Bellman-Ford...'):
        # Execute algorithm
        path = bellman_ford_arbitrage(rates, currencies, fee_rate)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Network Visualization")
            # Visualize the graph using NetworkX
            G = nx.DiGraph()
            for c in currencies:
                G.add_node(c)

            # Plotting configuration
            fig, ax = plt.subplots(figsize=(6, 6))
            pos = nx.spring_layout(G, seed=42) # Fixed node positions

            if path:
                # If an arbitrage path exists, highlight it in red
                path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                G.add_edges_from(path_edges)
                nx.draw(G, pos, with_labels=True, node_color='lightgreen',
                        node_size=3000, edge_color='red', width=3,
                        arrowsize=25, font_size=12, font_weight='bold', ax=ax)
                plt.title("Arbitrage Cycle Detected!", color='red')
            else:
                # Otherwise, draw simple connections for all currencies
                for i in range(num_currencies):
                    for j in range(num_currencies):
                        if i != j:
                            G.add_edge(currencies[i], currencies[j])
                nx.draw(G, pos, with_labels=True, node_color='lightblue',
                        node_size=3000, edge_color='gray', width=1,
                        arrowsize=15, alpha=0.5, font_size=12, ax=ax)
                plt.title("Market in Equilibrium")

            st.pyplot(fig)

        with col2:
            st.subheader("Analysis Report")
            if path:
                st.success("Risk-free arbitrage opportunity successfully captured!")
                path_str = " ➔ ".join(path)
                st.markdown(f"**Arbitrage Path:** `{path_str}`")

                # Calculate actual profit
                current_money = initial_capital
                st.write(f"**Initial Principal:** {initial_capital:,.2f} {path[0]}")

                for i in range(len(path) - 1):
                    curr_from = path[i]
                    curr_to = path[i+1]
                    idx_from = currencies.index(curr_from)
                    idx_to = currencies.index(curr_to)
                    rate = rates[idx_from][idx_to]

                    # Conversion after deducting transaction fee
                    after_fee_rate = rate * (1 - fee_rate / 100.0)
                    current_money = current_money * after_fee_rate
                    st.write(f"- Convert {curr_from} to {curr_to} (Rate {rate:.4f}, less fees): **{current_money:,.2f} {curr_to}**")

                profit = current_money - initial_capital
                profit_margin = (profit / initial_capital) * 100
                st.markdown(f"### Final Amount: {current_money:,.2f} {path[-1]}")
                st.markdown(f"### Net Profit: {profit:,.2f} {path[-1]} (+{profit_margin:.2f}%)")

            else:
                st.info("No arbitrage opportunities found under current rates and fee settings.")
                st.write("You can try **lowering the transaction fee** in the sidebar to see if opportunities appear.")