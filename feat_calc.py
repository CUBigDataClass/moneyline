import pandas as pd
import numpy as np

def avg_ppg(df):
    return round(sum(df['PTS'].astype(int)) / len(df), 4)

def avg_fg_pct(df):
    return round(sum(df['FG_PCT'].astype(float)) / len(df), 4)

def avg_ft_pct(df):
    return round(sum(df['FT_PCT'].astype(float)) / len(df), 4)

def avg_rbpg(df):
    return round(sum(df['REB'].astype(int)) / len(df), 4)