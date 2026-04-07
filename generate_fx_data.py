# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility in demonstrations
np.random.seed(42)
random.seed(42)

def generate_large_scale_fx_data(num_currencies=50, noise_level=0.005, filename="fx_market_large.csv"):
    """
    Generates large-scale simulated foreign exchange (FX) cross-rate data.
    
    Logic:
    1. Generate reasonable baseline exchange rates relative to a base currency (USD).
    2. Calculate perfect equilibrium exchange rates between all currency pairs using the base rates.
    3. Introduce random market noise (simulating price latency or liquidity deviations across exchanges).
    """
    # 1. Define codes for 50 currencies
    base_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'HKD', 'NZD']
    # Fill up to the target number; remaining currencies use C11, C12... to simulate emerging markets
    currencies = base_currencies + [f"C{i}" for i in range(11, num_currencies + 1)]

    # 2. Generate baseline rates relative to USD (values ranging from 0.1 to 150.0)
    # The rate for USD to itself is strictly 1.0
    base_rates_to_usd = {curr: np.random.uniform(0.1, 150.0) for curr in currencies}
    base_rates_to_usd['USD'] = 1.0

    # 3. Construct a 50x50 exchange rate matrix
    matrix = np.zeros((num_currencies, num_currencies))

    for i, curr_from in enumerate(currencies):
        for j, curr_to in enumerate(currencies):
            if i == j:
                matrix[i][j] = 1.0
            else:
                # Theoretical perfect equilibrium rate
                perfect_rate = base_rates_to_usd[curr_to] / base_rates_to_usd[curr_from]

                # Introduce market noise: e.g., +/- 0.5% fluctuation
                # This noise is the root cause of "arbitrage opportunities"
                noise = np.random.uniform(1 - noise_level, 1 + noise_level)
                matrix[i][j] = perfect_rate * noise

    # 4. Export to CSV
    df = pd.DataFrame(matrix, index=currencies, columns=currencies)
    df.to_csv(filename)
    print(f"Successfully generated {num_currencies}x{num_currencies} exchange rate data, saved as {filename}")
    print("This matrix contains sufficient market noise to test the Bellman-Ford algorithm's search capabilities.")

if __name__ == "__main__":
    # Generate a CSV with 50 currencies and a 0.5% (0.005) noise level
    generate_large_scale_fx_data(num_currencies=50, noise_level=0.005, filename="fx_market_large.csv")