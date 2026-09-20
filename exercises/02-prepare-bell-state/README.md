# Exercise 2: prepare a Bell state

**Difficulty:** Introductory  
**Prerequisites:** Tensor products, Hadamard, CNOT

Starting from $|00\rangle$, construct $|\Phi^+\rangle$ using only repository
gates and state helpers. Do not return the Bell-state constant directly.

Verify that:

- the state is normalized;
- amplitudes of `01` and `10` are zero;
- probabilities of `00` and `11` are each $1/2$;
- tracing out either qubit gives $I/2$.

The [reference solution](solution.py) keeps the preparation steps explicit.
