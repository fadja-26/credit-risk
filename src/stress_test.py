"""
This module contains reusable functions for credit risk stress testing.
These functions are designed to be imported into notebooks or production scripts.
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX

def fetch_fred(series_id: str) -> pd.DataFrame:
    """
    Download a time series from FRED (Federal Reserve Economic Data).
    """
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    df = pd.read_csv(url, encoding='utf-8-sig')
    df.columns = df.columns.str.strip().str.upper()

    date_col = df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
    df.columns = [series_id]

    return df

def calculate_expected_loss(pd_forecast: float, lgd: float = 0.45, ead: float = 100.0) -> float:
    """
    Calculate Expected Loss (EL) using the standard credit risk formula:
    EL = PD * LGD * EAD

    Args:
        pd_forecast: Probability of Default (as a percentage, e.g., 3.5 for 3.5%)
        lgd: Loss Given Default (default 0.45)
        ead: Exposure at Default (default 100.0)

    Returns:
        The absolute expected loss.
    """
    return (pd_forecast / 100.0) * lgd * ead

def fit_sarima(data: pd.Series, order: tuple, seasonal_order: tuple):
    """
    Fit a SARIMA model and return the results object.
    """
    model = SARIMAX(data,
                    order=order,
                    seasonal_order=seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False)
    return model.fit(disp=False)
