# -*- coding: utf-8 -*-
"""
Data Engine Module
Handles loading, saving, and dynamic generation of FX market data.
"""

import pandas as pd
import numpy as np
import os

def generate_realistic_fx_matrix(noise_level=0.005, mispricing_chance=0.3):
    """
    Generates a 50x50 FX matrix in memory based on real-world currency codes.
    """
    currencies = [
        'USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD',
        'SEK', 'KRW', 'SGD', 'NOK', 'MXN', 'INR', 'RUB', 'ZAR', 'TRY', 'BRL',
        'TWD', 'DKK', 'PLN', 'THB', 'IDR', 'HUF', 'CZK', 'ILS', 'CLP', 'PHP',
        'AED', 'COP', 'SAR', 'MYR', 'RON', 'VND', 'PEN', 'EGP', 'KWD', 'BHD',
        'OMR', 'JOD', 'QAR', 'KZT', 'UAH', 'PKR', 'ARS', 'NGN', 'GHS', 'KES'
    ]
    
    n = len(currencies)
    # Baseline values relative to 1 USD for realism
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

    matrix = np.zeros((n, n))
    for i, curr_from in enumerate(currencies):
        for j, curr_to in enumerate(currencies):
            if i == j:
                matrix[i][j] = 1.0
            else:
                fair_rate = base_values[curr_to] / base_values[curr_from]
                # High-frequency market noise simulation
                if np.random.random() < mispricing_chance:
                    noise = np.random.uniform(1 - noise_level, 1 + noise_level)
                    matrix[i][j] = fair_rate * noise
                else:
                    # Near-perfect equilibrium
                    matrix[i][j] = fair_rate * np.random.uniform(0.9999, 1.0001)

    return pd.DataFrame(matrix, index=currencies, columns=currencies)

def load_market_data(filepath):
    """
    Standard loader for CSV data.
    """
    if not os.path.exists(filepath):
        return None
    return pd.read_csv(filepath, index_col=0)

def save_market_data(df, folder="data", filename="fx_market_large.csv"):
    """
    Persists the generated matrix to the data directory.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath)
    return filepath