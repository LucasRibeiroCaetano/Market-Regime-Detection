"""Data loader and preprocessing utilities.

Downloads price and VIX from yfinance, computes log returns for the asset and a
standardized VIX log-level. Returns aligned, standardized features for the HMM
and the original price series (adjusted close) for plotting.
"""
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
import yfinance as yf


def load_and_preprocess(ticker: str = "SPY", vix_ticker: str = "^VIX", start: str = "2000-01-01", end: str = None) -> Tuple[np.ndarray, pd.Series]:
    """Download data and return standardized features and price series.

    Returns
    -------
    features : np.ndarray
        2D array with columns [asset_log_return, vix_standardized_log]
    price_series : pd.Series
        Adjusted close price series aligned with the features (index = DatetimeIndex)
    """
    # Download adjusted close price for asset and vix close
    data = yf.download([ticker, vix_ticker], start=start, end=end, progress=False)

    # Adjusted close may be under column 'Adj Close' for assets, VIX has 'Close'
    if ("Adj Close" in data.columns.get_level_values(0)):
        price = data[('Adj Close', ticker)].dropna()
    else:
        price = data[('Close', ticker)].dropna()

    # VIX series — prefer 'Close' column
    try:
        vix = data[('Close', vix_ticker)].dropna()
    except Exception:
        # fallback if single-column returned
        vix = data[vix_ticker].dropna()

    # Compute log returns for the asset
    asset_log = np.log(price).diff()

    # Compute log of VIX level and then standardize (z-score)
    vix_log = np.log(vix).replace([np.inf, -np.inf], np.nan)

    # Align series
    df = pd.concat([asset_log, vix_log], axis=1)
    df.columns = ["asset_log_return", "vix_log"]

    # Drop NaNs created by diff/log
    df = df.dropna()

    # Standardize features (mean 0, std 1)
    features = (df - df.mean()) / df.std()

    # Return numpy array for HMM and the aligned price series (slice to same index)
    aligned_price = price.reindex(df.index)

    return features.values, aligned_price
