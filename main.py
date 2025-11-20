"""Entry point for regime detection CLI.

Usage: `python main.py` with optional arguments.
"""
from __future__ import annotations

import argparse
import datetime
import os
from typing import Optional

from src.data_loader import load_and_preprocess
from src.model import HMMRegimeModel
from src.plotting import save_regime_plots


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Macro Regime Detection using Gaussian HMM")
    today = datetime.date.today().isoformat()
    parser.add_argument("--start", default="2000-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default=today, help="End date (YYYY-MM-DD)")
    parser.add_argument("--states", type=int, default=2, help="Number of HMM hidden states")
    parser.add_argument("--ticker", default="SPY", help="Asset ticker for price series")
    parser.add_argument("--vix", default="^VIX", help="Volatility index ticker (VIX)")
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()

    out_dir = "plots"
    os.makedirs(out_dir, exist_ok=True)

    # Load features and original price series
    features, price_series = load_and_preprocess(
        ticker=args.ticker, vix_ticker=args.vix, start=args.start, end=args.end
    )

    # Fit HMM and predict regimes
    model = HMMRegimeModel(n_states=args.states, random_state=42)
    regimes = model.fit_predict(features)

    # Plot and save
    save_regime_plots(price_series, regimes, out_dir=out_dir)


if __name__ == "__main__":
    main()
