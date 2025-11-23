from __future__ import annotations

import argparse
import os
from typing import Optional

import config
from src.data_loader import load_and_classify
from src.plotting import save_regime_plots


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Market Regime Detection using 50-Week SMA Rule")
    parser.add_argument("--start", default=config.DEFAULT_START_DATE, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default=config.DEFAULT_END_DATE, help="End date (YYYY-MM-DD)")
    parser.add_argument("--ticker", default=config.DEFAULT_TICKER, help="Asset ticker (default: ^GSPC for SPX)")
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Load weekly SPX data and classify regimes using 50W SMA rule
    price_series, regimes = load_and_classify(
        ticker=args.ticker, start=args.start, end=args.end
    )

    # Plot and save (regimes are already labeled: 0=Bull, 1=Correction, 2=Bear)
    save_regime_plots(price_series, regimes, out_dir=config.OUTPUT_DIR)


if __name__ == "__main__":
    main()
