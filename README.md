# Quantum-Ed — Quantum Computing, Information & Hardware (Educational Repo)

A hands-on, educational repository to learn **Quantum Computing** from first principles:

- 📚 **Theory in Markdown** (`docs/`)
- 🧪 **Interactive notebooks** (`notebooks/`)
- 🧰 **Reusable Python code** (`src/quantum_ed/`)
- ✅ **Tests** (`tests/`) to keep the math honest

This repo is designed to scale from *“I know linear algebra”* to *“I can reason about circuits, noise, and hardware constraints.”*

---

## Quick start

### Option A — Conda (recommended)
```bash
conda env create -f environment.yml
conda activate quantum-ed
python -m pytest -q
jupyter lab
```

### Option B — pip
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
jupyter lab
```

---

## Repository map

- `docs/` — structured chapters (Markdown)
- `notebooks/` — runnable lessons (Jupyter)
- `src/quantum_ed/` — minimal “from scratch” quantum toolkit (NumPy-based)
- `demos/` — small scripts you can run from CLI
- `tests/` — unit tests validating gates/measurement/noise

---

## Learning path

1. **Linear algebra refresh** → `docs/01-linear-algebra/README.md`
2. **Qubits & states** → `docs/02-qubits-and-states/README.md`
3. **Measurement** → `docs/03-measurement/README.md`
4. **Entanglement** → `docs/04-entanglement/README.md`
5. **Circuits & gates** → `docs/05-circuits-and-gates/README.md`
6. **Noise & channels** → `docs/06-noise-and-channels/README.md`
7. **Hardware overview** → `docs/08-hardware/README.md`

---

## Philosophy (why a small custom library?)

Many QC tutorials jump straight into frameworks. Here we do both:

- **From scratch**: state vectors, gates, measurement, noise (NumPy)
- **Optional ecosystem**: later we can add Qiskit/Cirq notebooks as optional modules

This makes the underlying math explicit and testable.

---

## Contributing

PRs are welcome: fixes, better explanations, more exercises, plots, and additional hardware chapters.

---

## License

MIT (see `LICENSE`).
