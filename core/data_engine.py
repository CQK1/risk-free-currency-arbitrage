# -*- coding: utf-8 -*-
import pandas as pd
import os

def load_market_data(filepath):
    """
    Loads market data from a CSV file.
    """
    if not os.path.exists(filepath):
        return None
    
    df = pd.read_csv(filepath, index_col=0)
    return df