# Exercise 3: validate a noise channel

**Difficulty:** Intermediate  
**Prerequisites:** Density matrices, quantum channels, matrix eigenvalues

Apply amplitude damping to the excited state $|1\rangle$ and verify that the
result remains a density matrix for every damping probability in $[0,1]$.

Your validation should check:

- Hermiticity;
- trace one;
- nonnegative eigenvalues within numerical tolerance;
- the expected populations $\rho_{00}=\gamma$ and $\rho_{11}=1-\gamma$.

See the [reference solution](solution.py) after writing your own checks.
