# Reproducible notebooks

The notebooks are ordered as a short interactive learning path. They import the
installed `quantum_ed` package rather than copying its implementation logic.

| Notebook | Expected observation |
| --- | --- |
| `00-setup.ipynb` | The package imports and the Hadamard gate is unitary |
| `01-qubit-bloch.ipynb` | State amplitudes map consistently to Bloch vectors |
| `02-bell-entanglement.ipynb` | Bell correlations produce maximally mixed marginals |
| `03-noise-fidelity.ipynb` | Noise reduces fidelity and coherence predictably |
| `04-chsh.ipynb` | Bell-state correlations violate the classical CHSH bound |
| `05-quantum-teleportation.ipynb` | Alice's Bell-basis measurement and Bob's feedforward correction recover arbitrary states with unit fidelity |
| `06-grover-search.ipynb` | Amplitude amplification rotates the state in 2D to reach 100% target probability |

Versioned notebooks have empty outputs to keep reviews small and deterministic.
CI executes copies of every notebook and fails on the first cell error.

```bash
python -m pip install -e ".[notebooks]"
python -m jupyter nbconvert --to notebook --execute notebooks/*.ipynb \
  --output-dir executed-notebooks --ExecutePreprocessor.timeout=120
```
