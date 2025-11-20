"""Plotting utilities using matplotlib and matplotx.

Creates a regime-colored price plot and a regime distribution pie chart.
"""
from __future__ import annotations

import os
from collections import Counter
from typing import Sequence

import matplotlib.pyplot as plt
import matplotx
import numpy as np
import pandas as pd


plt.style.use(matplotx.styles.github["dark"])  # use the requested style


def save_regime_plots(price: pd.Series, regimes: Sequence[int], out_dir: str = "plots") -> None:
    """Create and save regime plots.

    Parameters
    ----------
    price : pd.Series
        Adjusted close price series indexed by date.
    regimes : Sequence[int]
        Regime labels aligned to `price`.
    out_dir : str
        Directory where plots will be saved.
    """
    os.makedirs(out_dir, exist_ok=True)

    # Ensure arrays
    dates = price.index
    price_vals = price.values
    regimes = np.asarray(regimes)

    # Main plot: price with regime-colored scatter
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, price_vals, color="#c9d1d9", linewidth=1.0, alpha=0.8)

    # Choose colors for regimes
    cmap = plt.get_cmap("tab10")
    unique_states = np.unique(regimes)

    for i, state in enumerate(unique_states):
        mask = regimes == state
        ax.scatter(dates[mask], price_vals[mask], s=10, color=cmap(i), label=f"Regime {state}")

    ax.set_title("Asset Price with Detected Regimes")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    regime_plot_path = os.path.join(out_dir, "regime_plot.png")
    fig.savefig(regime_plot_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Secondary plot: regime distribution (pie chart without labels on slices)
    counts = Counter(regimes.tolist())
    labels = [f"Regime {s}: {counts[s]}" for s in sorted(counts.keys())]
    sizes = [counts[s] for s in sorted(counts.keys())]

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    wedges, _ = ax2.pie(sizes, labels=None, startangle=90, colors=[cmap(i) for i in range(len(sizes))])
    # Use legend instead of direct labels on slices
    ax2.legend(wedges, labels, title="Regimes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax2.set_title("Regime Distribution")
    dist_plot_path = os.path.join(out_dir, "regime_distribution.png")
    fig2.savefig(dist_plot_path, dpi=300, bbox_inches="tight")
    plt.close(fig2)
