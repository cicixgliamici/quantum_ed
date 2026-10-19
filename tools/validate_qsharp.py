"""Compile and execute Q# experiments, including phase-sensitive checks."""

from validate_experiments import validate_ecosystem


if __name__ == "__main__":
    raise SystemExit(validate_ecosystem("qsharp"))
