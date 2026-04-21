# Quantum-Ed — Quantum Computing, Information & Hardware

Quantum-Ed is an educational repository for learning **quantum computing** from first principles through a combination of:
- structured theory notes,
- runnable notebooks,
- small reusable Python modules,
- and tests that validate the underlying mathematics.

The goal of the repository is not just to collect notes, but to build a **rigorous and inspectable learning path** from basic linear algebra to circuits, measurement, entanglement, noise, and hardware-aware reasoning.

---

## Why this repository matters

Many quantum-computing repositories jump immediately into frameworks or high-level APIs.

Quantum-Ed is designed differently:
- it emphasizes the **mathematical foundations**,
- keeps core ideas **transparent and inspectable**,
- and uses code as a way to make theory testable.

This makes the repository useful both as a study resource and as a compact technical project showing:
- scientific computing structure,
- mathematical clarity,
- educational repository design,
- and disciplined use of notebooks, code, and tests together.

---

## Repository structure

- `docs/` — structured theory chapters in Markdown
- `notebooks/` — runnable Jupyter lessons and demonstrations
- `src/quantum_ed/` — small Python modules for core concepts
- `demos/` — lightweight scripts for quick experiments
- `tests/` — tests validating states, gates, measurement, and related behavior

---

## Current implemented focus

At the current stage, the repository is focused on a compact but solid foundation:

- linear algebra refresh for quantum computing
- qubits and state-vector representation
- measurement basics
- Bell states and introductory entanglement material
- introductory circuits and gates
- first notes toward noise, channels, and hardware constraints

The aim is to make these parts **clear, runnable, and extensible**, rather than to cover every topic superficially.

---

## Planned expansion

Planned future extensions include:
- additional notebooks on noise and fidelity
- more hardware-oriented sections
- optional comparisons with established ecosystems such as Qiskit or Cirq
- more exercises and validation tests
- broader coverage of quantum information and algorithmic examples

This section exists to clearly separate **what is already implemented** from **what is planned next**.

---

## Learning path

A good path through the repository is:

1. **Linear algebra refresh**  
   `docs/01-linear-algebra/README.md`

2. **Qubits and states**  
   `docs/02-qubits-and-states/README.md`

3. **Measurement**  
   `docs/03-measurement/README.md`

4. **Entanglement and Bell states**  
   `docs/04-entanglement/README.md`  
   `notebooks/02-bell-entanglement.ipynb`

5. **Circuits and gates**  
   `docs/05-circuits-and-gates/README.md`

6. **Noise and channels**  
   `docs/06-noise-and-channels/README.md`

7. **Hardware overview**  
   `docs/08-hardware/README.md`

---

## Quick reviewer guide

If you want to evaluate the repository quickly, the best path is:

1. Read this README for the project goal and scope.
2. Open `docs/` to inspect the structure of the theory material.
3. Open one notebook such as `notebooks/02-bell-entanglement.ipynb`.
4. Inspect `src/quantum_ed/` to see the supporting Python code.
5. Check `tests/` to confirm that the mathematical components are being validated.

---

## Philosophy

The repository follows a simple principle:

> understand the math first, then use tools with intention.

That is why the project starts from small, explicit implementations and educational notes before relying heavily on external quantum ecosystems.

The objective is not to compete with mature frameworks, but to make their underlying ideas easier to understand and reason about.

---

## Getting started

### Option A — Conda
```bash
conda env create -f environment.yml
conda activate quantum-ed
python -m pytest -q
jupyter lab
````

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

## Typical use cases

* studying the mathematical foundations of quantum computing
* using code to validate basic quantum operations
* building a structured educational portfolio around physics-informed computing
* creating a base for future extensions toward frameworks, noise models, and hardware-aware experiments

---

## Contributing

Improvements are welcome, especially:

* clearer explanations
* additional exercises
* more tests
* better notebook visualizations
* careful extensions of the current theoretical scope

---

## License

MIT (see `LICENSE`).
