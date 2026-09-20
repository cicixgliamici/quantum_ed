# Bit-ordering conventions

Bit ordering is a presentation convention, not a physical difference between
circuits. Always distinguish three ideas:

1. **Qubit index** identifies a wire in the circuit.
2. **Classical-bit index** identifies the destination of a measurement.
3. **Display order** determines how a tool prints a register as a string.

## Repository convention

Theory and OpenQASM comments describe values in increasing qubit-index order
unless a section says otherwise. Implementations map each measured qubit to the
classical bit with the same index.

Qiskit commonly displays the highest classical-bit index on the left. Q# result
arrays retain array-index order. OpenQASM register measurement maps qubit `j`
to classical bit `j`, although a consuming tool may format strings differently.

## Comparison rule

Compare indexed measurement mappings first and rendered strings second. Every
experiment README states the expected logical result to make this explicit.
