# -*- coding: utf-8 -*-
"""
Currency Market Data Generator
Author: [Your Name/Student ID]
University of Lethbridge - Quantitative Finance Project

Description:
This script generates a synthetic but realistic exchange rate matrix for 50 
global currencies. It saves the output to 'data/fx_market_large.csv'.
"""

import pandas as pd
import numpy as np
import os

def generate_realistic_fx_data(noise_level=0.003, mispricing_chance=0.2):
    """
    Creates a 50x50 matrix of exchange rates.
    
    Parameters:
    - noise_level: How much the rates deviate from perfect equilibrium.
    - mispricing_chance: Probability (0 to 1) that a specific pair has a 
      significant price deviation (simulating market inefficiency).
    """
    
    # 1. Define 50 real-world currency codes
    # Majors, Minors, and Emerging Markets
    currencies = [
        'USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD',
        'SEK', 'KRW', 'SGD', 'NOK', 'MXN', 'INR', 'RUB', 'ZAR', 'TRY', 'BRL',
        'TWD', 'DKK', 'PLN', 'THB', 'IDR', 'HUF', 'CZK', 'ILS', 'CLP', 'PHP',
        'AED', 'COP', 'SAR', 'MYR', 'RON', 'VND', 'PEN', 'EGP', 'KWD', 'BHD',
        'OMR', 'JOD', 'QAR', 'KZT', 'UAH', 'PKR', 'ARS', 'NGN', 'GHS', 'KES'
    ]
    
    n = len(currencies)
    
    # 2. Assign a 'Base Value' for each currency relative to 1 USD
    # These are rough approximations of real-world values to keep it realistic
    base_values = {
        'USD': 1.0, 'EUR': 0.92, 'JPY': 150.5, 'GBP': 0.79, 'AUD': 1.52, 
        'CAD': 1.35, 'CHF': 0.88, 'CNY': 7.19, 'HKD': 7.82, 'NZD': 1.63,
        'SEK': 10.35, 'KRW': 1330.0, 'SGD': 1.34, 'NOK': 10.55, 'MXN': 17.05,
        'INR': 82.9, 'RUB': 92.5, 'ZAR': 19.1, 'TRY': 31.2, 'BRL': 4.97,
        'TWD': 31.5, 'DKK': 6.85, 'PLN': 3.98, 'THB': 35.8, 'IDR': 15600.0,
        'HUF': 362.0, 'CZK': 23.4, 'ILS': 3.65, 'CLP': 965.0, 'PHP': 56.1,
        'AED': 3.67, 'COP': 3950.0, 'SAR': 3.75, 'MYR': 4.75, 'RON': 4.58,
        'VND': 24600.0, 'PEN': 3.79, 'EGP': 30.9, 'KWD': 0.31, 'BHD': 0.38,
        'OMR': 0.38, 'JOD': 0.71, 'QAR': 3.64, 'KZT': 450.0, 'UAH': 38.5,
        'PKR': 278.0, 'ARS': 840.0, 'NGN': 1500.0, 'GHS': 12.5, 'KES': 145.0
    }

    # Initialize matrix
    matrix = np.zeros((n, n))

    # 3. Fill the matrix
    # We calculate the "Fair Rate" first, then add a tiny bit of noise
    for i, curr_from in enumerate(currencies):
        for j, curr_to in enumerate(currencies):
            if i == j:
                matrix[i][j] = 1.0
            else:
                # Fair Rate = (To_Value / From_Value)
                fair_rate = base_values[curr_to] / base_values[curr_from]
                
                # Apply noise only to some pairs to simulate actual market friction
                # Most pairs will be very efficient (near 1.0 multiplier)
                if np.random.random() < mispricing_chance:
                    # Random noise between (1 - noise) and (1 + noise)
                    noise = np.random.uniform(1 - noise_level, 1 + noise_level)
                    matrix[i][j] = fair_rate * noise
                else:
                    # Nearly perfect efficiency
                    tiny_noise = np.random.uniform(0.9999, 1.0001)
                    matrix[i][j] = fair_rate * tiny_noise

    # 4. Save the data
    df = pd.DataFrame(matrix, index=currencies, columns=currencies)
    
    # Ensure the 'data' directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        
    output_path = os.path.join("data", "fx_market_large.csv")
    df.to_csv(output_path)
    
    print(f"Done! Generated data for {n} currencies.")
    print(f"Saved to: {output_path}")
    print("If you don't see arbitrage in the dashboard, try increasing 'noise_level'.")

if __name__ == "__main__":
    # You can tweak noise_level to 0.01 if you want to GUARANTEE an arbitrage exists
    # Keeping it at 0.005 makes it a 'maybe' depending on your luck!
    generate_realistic_fx_data(noise_level=0.008, mispricing_chance=0.3)
