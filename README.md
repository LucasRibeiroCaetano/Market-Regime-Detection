# Macro Regime Detection (Hidden Markov Model)

## Showcase

Placeholders for generated images:

![Regime Plot](plots/regime_plot.png)
![Regime Distribution](plots/regime_distribution.png)

## Description

This project detects macro market regimes using a Multivariate Gaussian Hidden Markov Model (HMM). The model uses asset log-returns (default: `SPY`) and VIX log-levels (standardized) to infer discrete regimes. The HMM uses full covariance to capture correlations between returns and volatility across regimes.

## Usage

Install requirements:

```
pip install -r requirements.txt
```

Run the CLI (defaults shown):

```
python main.py --start 2000-01-01 --end 2025-11-20 --states 2 --ticker SPY --vix ^VIX
```

For help:

```
python main.py --help
```

## Files

- `main.py`: CLI entry point.
- `src/data_loader.py`: Data download and preprocessing.
- `src/model.py`: HMM wrapper using `hmmlearn`'s `GaussianHMM`.
- `src/plotting.py`: Matplotlib + matplotx plotting utilities.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

Full license: https://creativecommons.org/licenses/by-nc/4.0/

## Author

Lucas Caetano
