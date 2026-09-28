# Qubits & Quantum States

The fundamental unit of classical information is the **bit**, which takes one of two discrete values: $0$ or $1$.
The fundamental unit of quantum information is the **quantum bit**, or **qubit**, which exists in a two-dimensional complex Hilbert space $\mathbb{C}^2$.

Unlike classical bits, qubits can exist in a continuum of superposition states, exhibit quantum interference, and acquire observable geometric phase shifts.

---

## 1. The State Vector Representation

A pure state of a single qubit is described by a unit vector $|\psi\rangle \in \mathbb{C}^2$:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}
$$

where $\alpha, \beta \in \mathbb{C}$ are the complex **probability amplitudes**.

The computational basis vectors represent the classical bit values:

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix},
\qquad
|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

### Normalization and the Born Rule
The vector must have unit Euclidean norm:

$$
\langle \psi | \psi \rangle = |\alpha|^2 + |\beta|^2 = 1
$$

According to the **Born rule**:
- Measuring $|\psi\rangle$ in the computational basis yields outcome $0$ with probability $P(0) = |\alpha|^2$.
- Measuring $|\psi\rangle$ in the computational basis yields outcome $1$ with probability $P(1) = |\beta|^2$.

### Superposition vs Classical Probabilistic Mixtures
It is vital to distinguish a **quantum superposition** from a classical probabilistic mixture (such as a coin flip before looking):
- In a classical probabilistic mixture, the bit is *definitely* $0$ or *definitely* $1$, but our knowledge is incomplete. Probabilities are non-negative real numbers $p_0, p_1 \ge 0$ that simply add up.
- In a quantum superposition, the state has no definite value of $0$ or $1$ prior to measurement. The system is described by **complex amplitudes**, which can interfere **constructively** (reinforcing each other) or **destructively** (canceling each other out).

#### Demonstration of Destructive Interference
Consider the equal superposition state $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$. Applying the Hadamard gate $H$:

$$
H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}},
\qquad
H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

Applying $H$ to $|+\rangle$:

$$
H|+\rangle = \frac{1}{\sqrt{2}}\left( \frac{|0\rangle + |1\rangle}{\sqrt{2}} + \frac{|0\rangle - |1\rangle}{\sqrt{2}} \right) = \frac{|0\rangle + |1\rangle + |0\rangle - |1\rangle}{2} = \frac{2|0\rangle + 0|1\rangle}{2} = |0\rangle
$$

Notice that the amplitudes for $|1\rangle$ have opposite signs ($+1/2$ and $-1/2$) and **completely cancel out**. This destructive interference is impossible in classical probability theory.

---

## 2. Global Phase vs. Relative Phase

A qubit has two distinct notions of phase: **global phase** and **relative phase**. Understanding the physical difference between them is essential.

### Global Phase (Unobservable)
If two state vectors $|\psi\rangle$ and $|\psi'\rangle$ differ only by an overall complex exponential factor:

$$
|\psi'\rangle = e^{i\phi}|\psi\rangle, \qquad \phi \in \mathbb{R}
$$

then $e^{i\phi}$ is called a **global phase**.

**Theorem:** Global phase has no physically observable consequences.
*Proof:* For any measurement operator or physical observable $M$:

$$
\langle \psi' | M | \psi' \rangle = \left(e^{i\phi}\langle \psi|\right) M \left(e^{i\phi}|\psi\rangle\right) = e^{-i\phi} e^{i\phi} \langle \psi | M | \psi \rangle = \langle \psi | M | \psi \rangle
$$

Similarly, the measurement probability of any outcome $|k\rangle$ is:

$$
P(k) = |\langle k | \psi' \rangle|^2 = |e^{i\phi}\langle k | \psi \rangle|^2 = |e^{i\phi}|^2 |\langle k | \psi \rangle|^2 = |\langle k | \psi \rangle|^2
$$

Because state vectors differing by a global phase describe the exact same physical reality, quantum states are formally equivalence classes (rays) in projective Hilbert space:

$$
|\psi\rangle \sim e^{i\phi}|\psi\rangle
$$

### Relative Phase (Physically Measurable)
Now consider the phase factor between the basis components:

$$
|\psi\rangle = \frac{|0\rangle + e^{i\varphi}|1\rangle}{\sqrt{2}}
$$

Here, $\varphi$ is the **relative phase** between $|0\rangle$ and $|1\rangle$.

**Relative phase produces dramatic, observable interference effects!**

For example, compare:
- $\varphi = 0$:

$$
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

- $\varphi = \pi$ ($e^{i\pi} = -1$):

$$
|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

Both $|+\rangle$ and $|-\rangle$ have identical 50/50 measurement probabilities in the computational basis ($P(0) = 1/2, P(1) = 1/2$).
However, they are completely orthogonal states:

$$
\langle + | - \rangle = \left(\frac{\langle 0| + \langle 1|}{\sqrt{2}}\right)\left(\frac{|0\rangle - |1\rangle}{\sqrt{2}}\right) = \frac{\langle 0|0\rangle - \langle 0|1\rangle + \langle 1|0\rangle - \langle 1|1\rangle}{2} = \frac{1 - 0 + 0 - 1}{2} = 0
$$

Measuring $|+\rangle$ in the Hadamard basis yields outcome $+$ with $100\%$ certainty, while measuring $|-\rangle$ yields outcome $-$ with $100\%$ certainty.
Relative phase is physically real and measurable.

---

## 3. The Bloch Sphere Geometry

Since global phase is physically irrelevant and the state is normalized, any pure single-qubit state can be represented uniquely on the surface of a three-dimensional unit sphere: the **Bloch Sphere**.

### Derivation of the Bloch Parameterization
Start from a general normalized state:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle, \quad |\alpha|^2 + |\beta|^2 = 1
$$

1. Writing $\alpha$ and $\beta$ in polar form: $\alpha = r_\alpha e^{i\phi_\alpha}$ and $\beta = r_\beta e^{i\phi_\beta}$.
2. Factor out the global phase $e^{i\phi_\alpha}$:

$$
|\psi\rangle = e^{i\phi_\alpha} \left( r_\alpha |0\rangle + r_\beta e^{i(\phi_\beta - \phi_\alpha)} |1\rangle \right)
$$

3. Neglecting the unphysical global phase and setting $\varphi \equiv \phi_\beta - \phi_\alpha$:

$$
|\psi\rangle \sim r_\alpha |0\rangle + r_\beta e^{i\varphi} |1\rangle
$$

4. The normalization constraint $r_\alpha^2 + r_\beta^2 = 1$ with $r_\alpha, r_\beta \ge 0$ parameterizes a circle. We can set $r_\alpha = \cos(\theta/2)$ and $r_\beta = \sin(\theta/2)$ for $\theta \in [0, \pi]$:

$$
|\psi\rangle = \cos\left(\frac{\theta}{2}\right) |0\rangle + e^{i\varphi}\sin\left(\frac{\theta}{2}\right) |1\rangle
$$

where:
- $\theta \in [0, \pi]$ is the **polar angle** (colatitude).
- $\varphi \in [0, 2\pi)$ is the **azimuthal angle** (longitude).

*(Why $\theta/2$ instead of $\theta$? Because two orthogonal states in Hilbert space, like $|0\rangle$ and $|1\rangle$, must be mapped to antipodal points—separated by $180^\circ$—on the sphere).*

### The Bloch Vector $\vec{r}$
The corresponding Cartesian coordinates $(x, y, z)$ on the unit sphere are:

$$
\vec{r} = \begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} \sin\theta \cos\varphi \\ \sin\theta \sin\varphi \\ \cos\theta \end{pmatrix}
$$

Notice that for any pure state, $\|\vec{r}\| = \sqrt{x^2 + y^2 + z^2} = 1$.

### Connection to Pauli Observables
The components of the Bloch vector are precisely the expectation values of the three Pauli matrices:

$$
x = \langle \psi | X | \psi \rangle,
\qquad
y = \langle \psi | Y | \psi \rangle,
\qquad
z = \langle \psi | Z | \psi \rangle
$$

### Cardinal Landmark States on the Bloch Sphere

| State Name | Mathematical Expression | $(\theta, \varphi)$ | Bloch Vector $(x, y, z)$ | Location |
|:---|:---:|:---:|:---:|:---|
| Ground state $|0\rangle$ | $|0\rangle$ | $(0, \text{any})$ | $(0, 0, 1)$ | North Pole ($+z$) |
| Excited state $|1\rangle$ | $|1\rangle$ | $(\pi, \text{any})$ | $(0, 0, -1)$ | South Pole ($-z$) |
| Plus state $|+\rangle$ | $\frac{|0\rangle + |1\rangle}{\sqrt{2}}$ | $(\pi/2, 0)$ | $(1, 0, 0)$ | Positive $x$-axis |
| Minus state $|-\rangle$ | $\frac{|0\rangle - |1\rangle}{\sqrt{2}}$ | $(\pi/2, \pi)$ | $(-1, 0, 0)$ | Negative $x$-axis |
| Plus-$i$ state $|+i\rangle$ | $\frac{|0\rangle + i|1\rangle}{\sqrt{2}}$ | $(\pi/2, \pi/2)$ | $(0, 1, 0)$ | Positive $y$-axis |
| Minus-$i$ state $|-i\rangle$ | $\frac{|0\rangle - i|1\rangle}{\sqrt{2}}$ | $(\pi/2, 3\pi/2)$ | $(0, -1, 0)$ | Negative $y$-axis |

---

## 4. Multi-Qubit State Spaces

When combining $n$ qubits, the Hilbert space grows exponentially:

$$
\mathcal{H} = (\mathbb{C}^2)^{\otimes n} \cong \mathbb{C}^{2^n}
$$

A general pure $n$-qubit state is written as:

$$
|\Psi\rangle = \sum_{x=0}^{2^n-1} c_x |x\rangle, \qquad \sum_{x=0}^{2^n-1} |c_x|^2 = 1
$$

where $|x\rangle = |x_0 x_1 \dots x_{n-1}\rangle$ is an $n$-bit computational basis state.

For $n=2$ qubits, there are $2^2 = 4$ basis states:

$$
|00\rangle = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}, \quad
|01\rangle = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}, \quad
|10\rangle = \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix}, \quad
|11\rangle = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}
$$

And the general state is:

$$
|\Psi\rangle = c_{00}|00\rangle + c_{01}|01\rangle + c_{10}|10\rangle + c_{11}|11\rangle, \quad |c_{00}|^2 + |c_{01}|^2 + |c_{10}|^2 + |c_{11}|^2 = 1
$$

This exponential capacity ($2^{50} \approx 10^{15}$ amplitudes, $2^{300} > \text{atoms in the observable universe}$) explains why classical computers cannot simulate large quantum systems by storing state vectors directly.

---

## 5. Python Implementation with `quantum_ed.states`

In `src/quantum_ed/states.py`, state vectors and Bloch transformations are directly accessible:

```python
import numpy as np
from quantum_ed.states import ket0, ket1, normalize, bloch_vector, state_from_bloch

# 1. Prepare basis states
q0 = ket0()
q1 = ket1()

# 2. Normalize an arbitrary unnormalized amplitude vector
raw_vector = np.array([[3.0], [4.0j]], dtype=complex)
normalized_psi = normalize(raw_vector)
print("Normalized amplitudes:\n", normalized_psi)  # [[0.6+0j], [0+0.8j]]

# 3. Calculate Bloch sphere vector for |+>
psi_plus = (q0 + q1) / np.sqrt(2)
rx, ry, rz = bloch_vector(psi_plus)
print(f"Bloch coords for |+>: x={rx:.2f}, y={ry:.2f}, z={rz:.2f}")
# Output: x=1.00, y=0.00, z=0.00

# 4. Construct a quantum state from spherical angles (theta=pi/2, phi=pi/2 -> |+i>)
theta = np.pi / 2
phi = np.pi / 2
psi_i = state_from_bloch(theta, phi)
print("\nState from Bloch (theta=pi/2, phi=pi/2):\n", psi_i)
```

---

## 6. Exercises and Worked Solutions

### Exercise 1: State Representation on the Bloch Sphere
**Problem:** Find the Bloch angles $(\theta, \varphi)$ and Cartesian coordinates $(x, y, z)$ for the state:

$$
|\psi\rangle = \frac{\sqrt{3}}{2}|0\rangle + \frac{1}{2}e^{i\pi/3}|1\rangle
$$

**Solution:**
Match with $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\varphi}\sin(\theta/2)|1\rangle$:
- $\cos(\theta/2) = \frac{\sqrt{3}}{2} \implies \frac{\theta}{2} = \frac{\pi}{6} \implies \theta = \frac{\pi}{3} = 60^\circ$.
- $\sin(\theta/2) = \sin(\pi/6) = \frac{1}{2}$ (consistent).
- $\varphi = \frac{\pi}{3} = 60^\circ$.

Now calculate Cartesian coordinates:
- $x = \sin\theta\cos\varphi = \sin(60^\circ)\cos(60^\circ) = \left(\frac{\sqrt{3}}{2}\right)\left(\frac{1}{2}\right) = \frac{\sqrt{3}}{4} \approx 0.433$
- $y = \sin\theta\sin\varphi = \sin(60^\circ)\sin(60^\circ) = \left(\frac{\sqrt{3}}{2}\right)\left(\frac{\sqrt{3}}{2}\right) = \frac{3}{4} = 0.75$
- $z = \cos\theta = \cos(60^\circ) = \frac{1}{2} = 0.5$

Verification: $x^2 + y^2 + z^2 = \frac{3}{16} + \frac{9}{16} + \frac{4}{16} = \frac{16}{16} = 1$.

### Exercise 2: Global Phase Verification
**Problem:** Given state $|\psi_1\rangle = \frac{1}{\sqrt{2}}|0\rangle - \frac{1}{\sqrt{2}}|1\rangle$ and $|\psi_2\rangle = -\frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$, show that they differ only by a global phase and find their Bloch vectors.
**Solution:**
Notice that:

$$
|\psi_2\rangle = (-1) |\psi_1\rangle = e^{i\pi} |\psi_1\rangle
$$

The states differ by the global phase factor $e^{i\pi} = -1$.
Their Bloch vectors are both:

$$
(x, y, z) = (-1, 0, 0)
$$

Both vectors point to the exact same point (the $-x$ pole) on the Bloch sphere, representing the physical state $|-\rangle$.

---

## 7. Next Steps

Now proceed to measurement and wavefunction collapse:
- [Chapter 3: Measurement](../03-measurement/README.md)
- Accompanying notebook: [`notebooks/01-qubit-bloch.ipynb`](https://github.com/cicixgliamici/quantum_ed/blob/main/notebooks/01-qubit-bloch.ipynb)
