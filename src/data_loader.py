"""Data loader and regime classification using 50-week SMA rule.

Downloads weekly SPX data, computes 50-week SMA, and classifies regimes:
- Bull Market (0): Price above 50W SMA (or exited bear with 4+ consecutive weeks above)
- Correction (1): Price below 50W SMA for <10 consecutive weeks
- Bear Market (2): Price below 50W SMA for >=10 consecutive weeks (exit requires 4 consecutive weeks above)
"""
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
import yfinance as yf

import config


def load_and_classify(ticker: str = "^GSPC", start: str = "2000-01-01", end: str = None) -> Tuple[pd.Series, np.ndarray]:
    """Download weekly SPX data and classify regimes based on 50W SMA.
    
    Always downloads data from the historical start (1946) to ensure consistent SMA and regime
    calculations, then filters to the requested date range for display.

    Parameters
    ----------
    ticker : str
        Asset ticker (default: ^GSPC for SPX)
    start : str
        Start date for displaying results (YYYY-MM-DD) - data will be calculated from 1946
    end : str
        End date (YYYY-MM-DD), defaults to today

    Returns
    -------
    price_series : pd.Series
        Weekly adjusted close price series (index = DatetimeIndex)
    regimes : np.ndarray
        1D array of regime labels:
        0 = Bull Market (green)
        1 = Correction (yellow)
        2 = Bear Market (red)
    """
    # Store the requested start date for filtering later
    requested_start = pd.Timestamp(start) if start else None
    
    # Always download from historical start to ensure consistent SMA and regime calculations
    # This ensures the 50W SMA and regime states are computed with full historical context
    data = yf.download(ticker, start=config.DEFAULT_START_DATE, end=end, interval="1wk", progress=False)
    
    # Get adjusted close
    if "Adj Close" in data.columns:
        price = data["Adj Close"].dropna()
    else:
        price = data["Close"].dropna()
    
    # Compute SMA using configured window
    sma = price.rolling(window=config.SMA_WINDOW).mean()
    
    # Drop initial NaN period from SMA calculation first
    valid_mask = sma.notna()
    price_clean = price[valid_mask].copy()
    sma_clean = sma[valid_mask].copy()
    
    # Determine if price is above/below SMA
    above_sma = (price_clean >= sma_clean).values
    below_sma = ~above_sma
    
    # Count consecutive weeks below SMA
    consecutive_weeks_below = np.zeros(len(price_clean), dtype=int)
    counter = 0
    
    for i in range(len(below_sma)):
        if below_sma[i]:
            counter += 1
            consecutive_weeks_below[i] = counter
        else:
            counter = 0
            consecutive_weeks_below[i] = 0
    
    # Count consecutive weeks above SMA (needed for bear market exit)
    consecutive_weeks_above = np.zeros(len(price_clean), dtype=int)
    counter = 0
    
    for i in range(len(above_sma)):
        if above_sma[i]:
            counter += 1
            consecutive_weeks_above[i] = counter
        else:
            counter = 0
            consecutive_weeks_above[i] = 0
    
    # Classify regimes (bull/correction/bear) with bear market exit rule
    regimes = np.zeros(len(price_clean), dtype=int)
    in_bear_market = False
    
    for i in range(len(regimes)):
        weeks_below = consecutive_weeks_below[i]
        weeks_above = consecutive_weeks_above[i]
        
        # Check if we enter bear market
        if weeks_below >= config.BEAR_MARKET_THRESHOLD:
            in_bear_market = True
        
        # Check if we exit bear market
        if in_bear_market and weeks_above >= config.BEAR_EXIT_CONFIRMATION:
            in_bear_market = False
        
        # Assign regime based on state
        if in_bear_market:
            regimes[i] = 2  # Bear Market
        elif weeks_below > 0:
            regimes[i] = 1  # Correction (below SMA but not bear)
        else:
            regimes[i] = 0  # Bull Market (above SMA)
    
    # Filter to requested date range if specified
    if requested_start is not None:
        mask = price_clean.index >= requested_start
        price_clean = price_clean[mask]
        regimes = regimes[mask if isinstance(mask, np.ndarray) else mask.values]
    
    return price_clean, regimes
