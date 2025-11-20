"""HMM wrapper using hmmlearn GaussianHMM with full covariance."""
from __future__ import annotations

from typing import Optional

import numpy as np
from hmmlearn.hmm import GaussianHMM


class HMMRegimeModel:
    """Simple wrapper around hmmlearn's GaussianHMM.

    Parameters
    ----------
    n_states : int
        Number of hidden states.
    random_state : Optional[int]
        Random seed for reproducibility.
    """

    def __init__(self, n_states: int = 2, random_state: Optional[int] = None):
        self.n_states = n_states
        self.random_state = random_state
        self.model = GaussianHMM(n_components=self.n_states, covariance_type="full", n_iter=1000, random_state=self.random_state)

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit the HMM and return the most likely state sequence.

        Parameters
        ----------
        X : np.ndarray
            2D feature array for HMM (n_samples, n_features).

        Returns
        -------
        np.ndarray
            1D array of regime labels (integers from 0..n_states-1)
        """
        # Fit the model
        self.model.fit(X)

        # Decode the most likely state sequence
        states = self.model.predict(X)
        return states
