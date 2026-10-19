"""Import and execute OpenQASM experiments against shared references."""

from validate_experiments import validate_ecosystem


if __name__ == "__main__":
    raise SystemExit(validate_ecosystem("openqasm"))
