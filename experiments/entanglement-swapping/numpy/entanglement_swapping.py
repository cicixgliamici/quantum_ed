"""Inspect ideal swapping through the installed NumPy teaching toolkit."""

import numpy as np

# Expose the same protocol state to validation without copying the core mathematics.
from quantum_ed.networks import (
    OUTCOMES, conditional_endpoint_state, endpoint_density, swapped_state,
)


def final_probabilities() -> np.ndarray:
    """Return corrected Alice-Charlie probabilities in endpoint wire order."""
    return np.diag(endpoint_density(corrected=True)).real


def main() -> None:
    """Print every outcome's probability and endpoint state after feed-forward."""
    for outcome in OUTCOMES:
        probability, state = conditional_endpoint_state(outcome)
        print(f"Bob={outcome}, probability={probability:.3f}, corrected state={state.ravel()}")
    print("Endpoint density without the outcome record:")
    print(endpoint_density())
    print("Corrected endpoint probabilities:", final_probabilities())


if __name__ == "__main__":
    main()
