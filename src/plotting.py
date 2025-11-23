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

import config


plt.style.use(matplotx.styles.github["dark"])  # use the requested style


def save_regime_plots(price: pd.Series, regimes: Sequence[int], out_dir: str = "plots", state_names: dict[int, str] | None = None) -> None:
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

    # Main plot: price with regime-colored line segments
    fig, ax = plt.subplots(figsize=(config.PLOT_WIDTH, config.PLOT_HEIGHT))

    # Use configured regime colors and labels
    regime_colors = config.REGIME_COLORS
    regime_labels = config.REGIME_LABELS
    
    # Override with custom names if provided
    if state_names is not None:
        regime_labels.update(state_names)
    
    # Plot line segments by regime, including connecting points at transitions
    # Group consecutive indices with the same regime to create continuous line segments
    unique_states = np.unique(regimes)
    plotted_labels = set()
    
    i = 0
    while i < len(regimes):
        current_regime = regimes[i]
        color = regime_colors.get(int(current_regime), "#888888")
        label = regime_labels.get(int(current_regime), f"Regime {current_regime}")
        
        # Find the end of this regime segment
        j = i
        while j < len(regimes) and regimes[j] == current_regime:
            j += 1
        
        # Plot this segment (include one extra point at the end for smooth transition)
        end_idx = min(j + 1, len(dates))
        segment_dates = dates[i:end_idx]
        segment_prices = price_vals[i:end_idx]
        
        # Only add label once per regime type
        if label not in plotted_labels:
            ax.plot(segment_dates, segment_prices, color=color, linewidth=2.0, label=label)
            plotted_labels.add(label)
        else:
            ax.plot(segment_dates, segment_prices, color=color, linewidth=2.0)
        
        i = j

    ax.set_title("Asset Price with Detected Regimes")
    ax.set_ylabel("Price (Log Scale)")
    ax.set_yscale("log")
    ax.legend(loc="upper left")
    regime_plot_path = os.path.join(out_dir, "regime_plot.png")
    fig.savefig(regime_plot_path, dpi=config.PLOT_DPI, bbox_inches="tight")
    plt.close(fig)

    # Secondary plot: regime distribution (pie chart without labels on slices)
    counts = Counter(regimes.tolist())
    sorted_states = sorted(counts.keys())
    total = sum(counts.values())
    labels = [f"{regime_labels.get(int(s), f'Regime {s}')}: {100*counts[s]/total:.1f}%" for s in sorted_states]
    sizes = [counts[s] for s in sorted_states]
    colors = [regime_colors.get(int(s), "#888888") for s in sorted_states]

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    wedges, _ = ax2.pie(sizes, labels=None, startangle=90, colors=colors)
    # Use legend instead of direct labels on slices
    ax2.legend(wedges, labels, title="Regimes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax2.set_title("Regime Distribution")
    dist_plot_path = os.path.join(out_dir, "regime_distribution.png")
    fig2.savefig(dist_plot_path, dpi=config.PLOT_DPI, bbox_inches="tight")
    plt.close(fig2)
