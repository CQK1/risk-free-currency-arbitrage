# -*- coding: utf-8 -*-
import streamlit as st
import os
from core.data_engine import load_market_data, generate_realistic_fx_matrix, save_market_data
from core.arbitrage_algo import bellman_ford_arbitrage
from ui.visualizer import plot_interactive_network

st.set_page_config(page_title="Quant Arbitrage Detector", layout="wide")

st.title("Global Forex Market Arbitrage Simulator")
st.markdown("Quantitative tool to detect risk-free paths using **Bellman-Ford Algorithm**.")

# ==========================================
# Sidebar: Control Panel
# ==========================================
st.sidebar.header("Market Controls")

# New: Dynamic Noise Control
noise_level = st.sidebar.slider(
    "Market Volatility (Noise %)", 
    min_value=0.1, 
    max_value=2.0, 
    value=0.8, 
    step=0.1,
    help="Higher noise increases the chance of price discrepancies between currency pairs."
)

# Existing: Fee Control
fee_rate = st.sidebar.slider("Transaction Fee (%)", 0.0, 0.5, 0.1, 0.05)

# Button to trigger new data generation
if st.sidebar.button("Regenerate Market Data"):
    with st.spinner("Simulating new market conditions..."):
        # Convert percent to decimal for logic
        new_df = generate_realistic_fx_matrix(noise_level=noise_level/100.0)
        save_market_data(new_df)
        st.sidebar.success("New market data generated!")

# ==========================================
# Data Loading
# ==========================================
data_path = os.path.join("data", "fx_market_large.csv")
df_rates = load_market_data(data_path)

if df_rates is None:
    st.warning("No data found. Please click 'Regenerate Market Data' in the sidebar.")
    st.stop()

currencies = df_rates.columns.tolist()
rates = df_rates.values.tolist()

# Display Matrix
st.subheader(f"Current Exchange Rates ({len(currencies)} Currencies)")
st.dataframe(df_rates.style.format("{:.4f}"), height=300)

st.divider()

# ==========================================
# Arbitrage Execution
# ==========================================
if st.button("Start Arbitrage Scan", type="primary"):
    path = bellman_ford_arbitrage(rates, currencies, fee_rate)

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.subheader("Interactive Graph")
        plot_interactive_network(currencies, path)

    with col2:
        st.subheader("Execution Report")
        if path:
            st.success("Arbitrage loop detected!")
            # Logic for showing the path and profit...
            st.markdown(f"**Path:** {' ➔ '.join(path)}")
            # (Profit calculation logic remains the same as previous versions)
        else:
            st.info("Market is efficient. No arbitrage found under current fee/noise settings.")