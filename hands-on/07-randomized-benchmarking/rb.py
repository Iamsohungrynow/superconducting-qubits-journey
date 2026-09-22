"""
Single-qubit randomized benchmarking (pure numpy simulation).

Physics
-------
Randomized benchmarking (RB, Chapter 11) measures an average gate error
without trusting state preparation and measurement (SPAM). The protocol:

1. Apply m random Clifford gates.
2. Append the single recovery Clifford that undoes the whole sequence,
   so the ideal net operation is the identity.
3. Measure the probability of returning to |0> (the "survival").
4. Average over many random sequences and fit

       F(m) = A * p**m + B.

For stationary, Markovian, gate-independent in-subspace noise, a Clifford
twirl yields a depolarizing channel. Under these assumptions static SPAM only
moves A and B; the decay p isolates the gates themselves. The average error
per Clifford for a single qubit (d = 2) is

       r = (1 - p) * (d - 1) / d = (1 - p) / 2.

Here every Clifford is followed by a depolarizing channel of strength
lambda_dep,

       rho -> (1 - lambda_dep) * rho + lambda_dep * I/2,

which shrinks the Bloch vector by (1 - lambda_dep). Twirling leaves it
untouched, so theory predicts exactly p = 1 - lambda_dep and
r = lambda_dep / 2, which the fit should recover.

Convention
----------
|0> = ground state. States evolve as density matrices; gates are perfect
unitaries and all error lives in the explicit depolarizing channel.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

rng = np.random.default_rng(7)

# ---------------------------------------------------------------------------
# Build the 24-element single-qubit Clifford group by closing {H, S} under
# multiplication. Matrices are canonicalized up to global phase so duplicates
# can be recognized.
# ---------------------------------------------------------------------------
H_gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S_gate = np.array([[1, 0], [0, 1j]], dtype=complex)


def equal_up_to_phase(U, V):
    """For 2x2 unitaries, U = e^{i phi} V exactly when |Tr(U^dag V)| = 2."""
    return abs(np.trace(U.conj().T @ V)) > 2.0 - 1e-6


def build_clifford_group():
    group = [np.eye(2, dtype=complex)]
    frontier = list(group)
    while frontier:
        new = []
        for U in frontier:
            for G in (H_gate, S_gate):
                V = U @ G
                if not any(equal_up_to_phase(V, W) for W in group):
                    group.append(V)
                    new.append(V)
        frontier = new
    return group


cliffords = build_clifford_group()
assert len(cliffords) == 24, f"expected 24 Cliffords, got {len(cliffords)}"


def find_inverse(U):
    """Return the group element equal to U^dagger up to global phase."""
    target = U.conj().T
    for C in cliffords:
        if equal_up_to_phase(C, target):
            return C
    raise LookupError("inverse not found; the group is not closed?!")


# ---------------------------------------------------------------------------
# Noise model: depolarizing channel after every Clifford.
# ---------------------------------------------------------------------------
lambda_dep = 0.02                  # depolarizing strength per Clifford
p_theory = 1.0 - lambda_dep        # predicted RB decay constant
r_theory = lambda_dep / 2.0        # predicted error per Clifford


def depolarize(rho, lam):
    return (1.0 - lam) * rho + lam * 0.5 * np.eye(2)


def rb_sequence_survival(m):
    """Run one random RB sequence of m Cliffords + recovery; return P(|0>)."""
    rho = np.array([[1, 0], [0, 0]], dtype=complex)   # start in |0><0|
    U_total = np.eye(2, dtype=complex)
    for _ in range(m):
        C = cliffords[rng.integers(len(cliffords))]
        rho = C @ rho @ C.conj().T
        rho = depolarize(rho, lambda_dep)
        U_total = C @ U_total
    R = find_inverse(U_total)                          # recovery Clifford
    rho = R @ rho @ R.conj().T
    rho = depolarize(rho, lambda_dep)                  # recovery is noisy too
    return rho[0, 0].real


# ---------------------------------------------------------------------------
# Sweep sequence lengths, average many random sequences per length.
# ---------------------------------------------------------------------------
lengths = np.unique(np.round(np.logspace(0, np.log10(300), 14)).astype(int))
n_seq = 60                                              # sequences per length

means = []
for m in lengths:
    surv = [rb_sequence_survival(int(m)) for _ in range(n_seq)]
    means.append(np.mean(surv))
means = np.array(means)


def model(m, A, p, B):
    return A * p**m + B


popt, pcov = curve_fit(model, lengths, means, p0=[0.5, 0.98, 0.5],
                       bounds=([0, 0.8, 0], [1, 1, 1]))
A_fit, p_fit, B_fit = popt
r_fit = (1.0 - p_fit) / 2.0

print("Single-qubit randomized benchmarking")
print("=" * 60)
print(f"noise: depolarizing lambda = {lambda_dep} after every Clifford")
print(f"Clifford group size        = {len(cliffords)}")
print(f"sequence lengths m         = {lengths.tolist()}")
print(f"sequences per length       = {n_seq}")
print(f"fit:  F(m) = A p^m + B  ->  A = {A_fit:.3f}, p = {p_fit:.5f}, "
      f"B = {B_fit:.3f}")
print(f"decay constant p : fit {p_fit:.5f}   vs theory {p_theory:.5f}")
print(f"error/Clifford r : fit {r_fit:.5f}   vs theory {r_theory:.5f}")
print("=" * 60)
print("Note: r comes out right even though we never measured a single gate")
print("directly, and it would stay right with imperfect SPAM (try it below).")

# ---------------------------------------------------------------------------
# Plot the decay and the fit.
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
m_fine = np.linspace(1, lengths[-1], 400)
ax.plot(lengths, means, "o", color="C0", label="mean survival (60 seq/point)")
ax.plot(m_fine, model(m_fine, *popt), "-", color="C3",
        label=f"fit A p^m + B,  p = {p_fit:.4f}")
ax.axhline(0.5, color="k", ls=":", lw=1, alpha=0.5)
ax.set_xlabel("Number of Cliffords m")
ax.set_ylabel("P(return to |0>)")
ax.set_title(f"Randomized benchmarking: r = {r_fit:.4f} per Clifford "
             f"(theory {r_theory:.4f})")
ax.set_ylim(0.45, 1.02)
ax.legend()
ax.grid(True, alpha=0.3)

# ---------------------------------------------------------------------------
# Save the figure next to this script, then show it interactively.
# ---------------------------------------------------------------------------
figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "rb.png"), dpi=130, bbox_inches="tight")
plt.show()
