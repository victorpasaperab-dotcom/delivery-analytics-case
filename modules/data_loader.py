# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 10:42:07 2026

@author: vic_p
"""

import pandas as pd
import numpy as np

def get_data(path):
    # Detecta \N como nulo
    df = pd.read_csv(path, na_values='\\N')
    df['order_final_state_timestamp_local'] = pd.to_datetime(
        df['order_final_state_timestamp_local'], errors='coerce'
    )
    numeric_cols = ['ATD', 'pickup_distance', 'dropoff_distance']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['total_distance'] = df['pickup_distance'] + df['dropoff_distance']
    bins = [0, 10, 20, 40, 60, np.inf]
    labels = ['0-10 min', '11-20 min', '21-40 min', '40-60 min', '60+ min']
    df['atd_segment'] = pd.cut(df['ATD'], bins=bins, labels=labels)
    df['order_final_state_timestamp_local'] = pd.to_datetime(df['order_final_state_timestamp_local'])
    df['day_of_week'] = df['order_final_state_timestamp_local'].dt.day_name()
    df['hour_of_day'] = df['order_final_state_timestamp_local'].dt.hour
    return df

# df1=get_data("C:/Users/vic_p/reto_analytics/data/BC_A&A_with_ATD.csv")
