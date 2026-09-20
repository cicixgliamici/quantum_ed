# Exercise 1: normalize a state

**Difficulty:** Introductory  
**Prerequisites:** Complex vectors, norms, valid quantum states

Implement a function that accepts a nonzero complex vector and returns a column
vector with Euclidean norm one. It must reject the zero vector.

Verify these properties:

- the output shape is `(n, 1)`;
- the output norm is one;
- relative amplitudes are unchanged;
- the zero vector raises `ValueError`.

Compare your implementation with [`solution.py`](solution.py) after attempting
the exercise independently.
