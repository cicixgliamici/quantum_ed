# Grover search

Grover's algorithm searches an unstructured space of size $N$ with
$O(\sqrt{N})$ oracle calls instead of the classical $O(N)$ worst case.

For two qubits, begin in the uniform state $|s\rangle$. The oracle marks `11`
by changing only its phase. The diffusion operator

$$
D = 2|s\rangle\langle s| - I
$$

reflects amplitudes about their mean. With $N=4$ and one marked state, one
iteration rotates the state exactly onto $|11\rangle$.

See the [five-ecosystem experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/grover-search).
