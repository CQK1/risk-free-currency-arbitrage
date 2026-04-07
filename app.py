# -*- coding: utf-8 -*-
import os
import streamlit as st
import pandas as pd
from core.data_engine import load_market_data
from core.arbitrage_algo import bellman_ford_arbitrage
from ui.visualizer import plot_interactive_network

# Page configuration
st.set_page_config(page_title="Quant Arbitrage Analysis Model", layout="wide")

st.title("Global Forex Market Risk-Free Arbitrage Monitoring System")
st.markdown("Real-time arbitrage path discovery tool based on Graph Theory (**Bellman-Ford Algorithm**) and **Logarithmic Transformation**.")

# 1. Load Data
data_file = os.path.join("data", "fx_market_large.csv")
df_rates = load_market_data(data_file)

if df_rates is None:
    st.error(f"Cannot find data file `{data_file}`! Please run the data generation script first.")
    st.stop()

currencies = df_rates.columns.tolist()
rates = df_rates.values.tolist()
num_currencies = len(currencies)

# Sidebar UI
st.sidebar.info(f"Dataset loaded: {num_currencies} currencies included")
st.sidebar.header("Parameter Settings")
initial_capital = st.sidebar.number_input("Initial Capital (Simulated Units)", min_value=1000, value=10000, step=1000)
fee_rate = st.sidebar.slider("Transaction Fee per Trade (%)", min_value=0.0, max_value=0.5, value=0.1, step=0.05)

# Main UI - Data Preview
st.subheader("Current Market Exchange Rate Matrix")
st.dataframe(df_rates.iloc[:8, :8].style.format("{:.4f}"))
st.caption("Note: For display purposes, only the first 8 currencies are shown here. The algorithm processes the full network.")

st.divider()

# 2. Execution Module
if st.button("Scan for Arbitrage Opportunities", type="primary"):
    with st.spinner('Scanning graph network using Bellman-Ford...'):
        
        # Call the separated algorithm logic
        path = bellman_ford_arbitrage(rates, currencies, fee_rate)

        col1, col2 = st.columns([1.2, 0.8])

        with col1:
            st.subheader("Interactive Network Visualization")
            st.caption("You can drag the nodes! Red indicates the detected arbitrage path.")
            # Call the separated visualizer logic
            plot_interactive_network(currencies, path)

        with col2:
            st.subheader("Analysis Report")
            if path:
                st.success("Risk-free arbitrage opportunity successfully captured!")
                path_str = " ➔ ".join(path)
                st.markdown(f"**Arbitrage Path:** `{path_str}`")

                current_money = initial_capital
                st.write(f"**Initial Principal:** {initial_capital:,.2f} {path[0]}")

                for i in range(len(path) - 1):
                    curr_from = path[i]
                    curr_to = path[i+1]
                    rate = rates[currencies.index(curr_from)][currencies.index(curr_to)]

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