# Project design and contribution

Quantum-Ed connects mathematical derivations to code that can be inspected
and checked. Its contribution is an educational implementation and a controlled
reproduction of established results. It does not introduce a new quantum
algorithm or claim a hardware speedup.

## Keep the mathematics visible

The installable NumPy core exposes states, gates, measurement, density
matrices, and channels directly. Short functions make array shapes and
physical assumptions inspectable. SDK tutorials live in `examples/` so the
library API stays separate from framework-specific learning material.

This choice favors clarity for small simulations. State vectors and density
matrices still grow exponentially; the package is not intended to compete
with production-scale simulators.

## Compare the same scientific claim

Experiments are organized by concept before ecosystem. A manifest declares
the theory, expected result, and implementation entrypoints. Repository and
website catalogs are generated from those contracts so the two reading paths
show the same coverage.

Shared checks compare against analytical references, rather than accepting
framework agreement alone. The checks inspect QFT phases and teleportation
states because matching computational-basis probabilities can miss errors.
See the [validation protocol](reference/experiment-validation.md).

## Make conventions explicit

Tensor order and displayed bit strings can differ between frameworks.
Conversions belong at ecosystem boundaries, with asymmetric inputs that
make a reversal observable. Similarly, a familiar noise-channel name is not
enough to identify its parameterization. The Bell-noise study defines the
physical channel before converting parameters for independent models.

The [bit-ordering reference](reference/bit-ordering.md),
[input contracts](reference/input-contracts.md), and
[study derivation](07-noise-and-channels/bell-noise-study.md) document these choices.

## Separate experiments from investigations

An experiment compares a common expected result across programming ecosystems.
A study can examine capabilities that static circuit languages do not share,
such as mixed-state noise simulation. Keeping those roles separate avoids
presenting unlike computations as equivalent implementations.

The Bell study follows one question through analytical predictions,
independent NumPy and PennyLane models, physical-state checks, CSV data, and
figures. Its conclusions apply to the stated initial state and local channels.

## Publish evidence alongside explanations

The website executes notebook copies and renders code, outputs, and figures.
Source notebooks remain output-free for readable reviews. A failing cell
stops the build. Version locks, wheel-install checks, and environment reports
support independent reproduction without requiring identical plot image bytes.

The [reviewer guide](reviewer-guide.md) provides a short evidence route.
The [reproduction guide](reference/reproducibility.md) explains the environment;
[scientific scope](reference/scientific-scope.md) distinguishes exact identities,
model assumptions, numerical evidence, and external empirical claims.
