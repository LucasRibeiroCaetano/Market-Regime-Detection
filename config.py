"""Configuration file for Market Regime Detection.

Contains all configurable parameters for regime detection, plotting, and defaults.
"""
from __future__ import annotations

import datetime

# Default data parameters
DEFAULT_TICKER = "^GSPC"  # S&P 500 index
DEFAULT_START_DATE = "1946-05-21"  # S&P 500 inception date
DEFAULT_END_DATE = datetime.date.today().isoformat()

# Regime detection parameters
SMA_WINDOW = 50  # Number of weeks for Simple Moving Average
BEAR_MARKET_THRESHOLD = 10  # Consecutive weeks below SMA to declare bear market
BEAR_EXIT_CONFIRMATION = 4  # Consecutive weeks above SMA required to exit bear market

# Plotting parameters
OUTPUT_DIR = "plots"
PLOT_DPI = 300
PLOT_WIDTH = 12
PLOT_HEIGHT = 6

# Regime colors (hex codes)
REGIME_COLORS = {
    0: "#097969",  # Bull Market - Green
    1: "#ffca3a",  # Correction - Yellow
    2: "#D22B2B",  # Bear Market - Red
}

# Regime labels
REGIME_LABELS = {
    0: "Bull Market",
    1: "Correction",
    2: "Bear Market",
}
