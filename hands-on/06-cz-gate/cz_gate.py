"""
A CZ gate from the |11> <-> |20> avoided crossing (pure QuTiP simulation).

Physics
-------
Two coupled transmons (Chapter 08). Keeping three levels per transmon, with
an exchange coupling g, the Hamiltonian in the frame rotating at qubit 2's
frequency is

    H = Delta*n1 + (alpha1/2)*n1*(n1-1) + (alpha2/2)*n2*(n2-1)
        + g*(a*bdag + adag*b)

where Delta = omega1 - omega2 is the qubit-qubit detuning and alpha_i < 0 are
the anharmonicities. The coupling conserves the total excitation number, so
the two-excitation states {|20>, |11>, |02>} form a closed block.

The flux-tuned CZ gate: bring |11> and |20> into resonance. Their energies
are E11 = Delta and E20 = 2*Delta + alpha1, so they cross when

    Delta = -alpha1.

At that point the exchange coupling connects them with matrix element
sqrt(2)*g (the sqrt(2) is the |1> -> |2> harmonic-oscillator enhancement), and
they hybridize with an avoided-crossing gap 2*sqrt(2)*g. If you sit exactly
on resonance for one full population cycle,

    t_CZ = 2*pi / (2*sqrt(2)*g) = pi / (sqrt(2)*g),

the population goes |11> -> |20> -> back to |11>, but the round trip imprints
a MINUS SIGN, an extra phase of pi, on |11> only. That is exactly a
controlled-Z gate (up to single-qubit phases, which virtual-Z rotations
absorb, Chapter 07).

The conditional phase is read out frame-independently as

    phi_c = phi_11 - phi_10 - phi_01 + phi_00,   phi_ij = arg <ij|psi_ij(t)>.

Convention
----------
|ij> = qubit1 in |i>, qubit2 in |j>. Angular frequencies in rad/us
(2*pi x MHz), times in us.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, destroy, qeye, tensor, sesolve

# ---------------------------------------------------------------------------
# Parameters (illustrative, clearly labelled).
# ---------------------------------------------------------------------------
alpha1 = 2 * np.pi * (-250.0)   # anharmonicity of qubit 1: -250 MHz (rad/us)
alpha2 = 2 * np.pi * (-250.0)   # anharmonicity of qubit 2
g = 2 * np.pi * 15.0            # exchange coupling: 15 MHz (rad/us)
Delta_res = -alpha1             # detuning that puts |11> on resonance with |20>

# Two three-level transmons.
a = tensor(destroy(3), qeye(3))
b = tensor(qeye(3), destroy(3))
n1 = a.dag() * a
n2 = b.dag() * b


def ket(i, j):
    return tensor(basis(3, i), basis(3, j))


def hamiltonian(Delta):
    return (Delta * n1
            + 0.5 * alpha1 * n1 * (n1 - 1)
            + 0.5 * alpha2 * n2 * (n2 - 1)
            + g * (a * b.dag() + a.dag() * b))


# ---------------------------------------------------------------------------
# 1) The avoided crossing: eigenenergies of the two-excitation block vs Delta.
# ---------------------------------------------------------------------------
Deltas = 2 * np.pi * np.linspace(150.0, 350.0, 401)
two_exc = [ket(2, 0), ket(1, 1), ket(0, 2)]
branches = np.empty((len(Deltas), 3))
for k, D in enumerate(Deltas):
    H = hamiltonian(D)
    # Project onto the closed {|20>, |11>, |02>} block and diagonalize it.
    block = np.array([[(s1.dag() * H * s2) for s2 in two_exc] for s1 in two_exc],
                     dtype=complex)
    branches[k] = np.sort(np.linalg.eigvalsh(block))

# Numerical minimum gap between the two upper branches, vs theory 2*sqrt(2)*g.
gap = branches[:, 2] - branches[:, 1]
k_min = int(np.argmin(gap))
gap_theory = 2 * np.sqrt(2) * g

print("CZ gate from the |11> <-> |20> avoided crossing")
print("=" * 64)
print(f"coupling g/2pi            = {g/2/np.pi:6.1f} MHz")
print(f"resonance at Delta/2pi    = {Delta_res/2/np.pi:6.1f} MHz (= -alpha1)")
print(f"avoided-crossing gap: numerical {gap[k_min]/2/np.pi:6.2f} MHz at "
      f"Delta/2pi = {Deltas[k_min]/2/np.pi:.1f} MHz")
print(f"                      theory    {gap_theory/2/np.pi:6.2f} MHz "
      f"(2*sqrt(2)*g)")

# ---------------------------------------------------------------------------
# 2) Sit on resonance: population swaps |11> -> |20> -> |11> in t_CZ, and the
#    conditional phase accumulates to pi.
# ---------------------------------------------------------------------------
t_cz = np.pi / (np.sqrt(2) * g)
tlist = np.linspace(0.0, 1.6 * t_cz, 801)
H_res = hamiltonian(Delta_res)

comp = {(i, j): ket(i, j) for i in (0, 1) for j in (0, 1)}
states = {ij: sesolve(H_res, psi, tlist).states for ij, psi in comp.items()}

P11 = np.array([abs(ket(1, 1).overlap(s)) ** 2 for s in states[(1, 1)]])
P20 = np.array([abs(ket(2, 0).overlap(s)) ** 2 for s in states[(1, 1)]])

phases = {ij: np.unwrap(np.array([np.angle(comp[ij].overlap(s))
                                  for s in states[ij]]))
          for ij in comp}
phi_c = phases[(1, 1)] - phases[(1, 0)] - phases[(0, 1)] + phases[(0, 0)]

k_cz = int(np.argmin(np.abs(tlist - t_cz)))
print(f"gate time t_CZ            = {t_cz*1e3:6.2f} ns  (pi / (sqrt(2)*g))")
print(f"at t_CZ:  P11 back to     = {P11[k_cz]:.4f}")
print(f"          residual P20    = {P20[k_cz]:.2e}")
print(f"          conditional phase = {abs(phi_c[k_cz]):.4f} rad "
      f"(target pi = {np.pi:.4f})")
print("=" * 64)
print("Note: single-qubit phases do not matter, they are absorbed by")
print("virtual-Z rotations; only the conditional phase pi defines the CZ.")

# ---------------------------------------------------------------------------
# Plot: avoided crossing / population swap / conditional phase.
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

ax = axes[0]
for i in range(3):
    ax.plot(Deltas / (2 * np.pi), branches[:, i] / (2 * np.pi), "C0")
# Bare (g = 0) energies for reference.
ax.plot(Deltas / (2 * np.pi), Deltas / (2 * np.pi), "k--", lw=1, alpha=0.5,
        label="bare |11>")
ax.plot(Deltas / (2 * np.pi), (2 * Deltas + alpha1) / (2 * np.pi), "k:", lw=1,
        alpha=0.5, label="bare |20>")
ax.axvline(Delta_res / (2 * np.pi), color="C3", ls="--", lw=1, alpha=0.6)
ax.set_xlabel("Qubit-qubit detuning Delta/2pi (MHz)")
ax.set_ylabel("Two-excitation energies / 2pi (MHz)")
ax.set_title("Avoided crossing of |11> and |20>\n(gap = 2*sqrt(2)*g)")
ax.set_ylim(100, 500)
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, alpha=0.3)

ax = axes[1]
ax.plot(tlist * 1e3, P11, "C0", label="P(|11>)")
ax.plot(tlist * 1e3, P20, "C3", label="P(|20>)")
ax.axvline(t_cz * 1e3, color="k", ls="--", lw=1, alpha=0.6)
ax.annotate("t_CZ", xy=(t_cz * 1e3, 1.0), xytext=(t_cz * 1e3 + 1.5, 1.06),
            fontsize=9)
ax.set_ylim(-0.05, 1.14)
ax.set_xlabel("Time on resonance (ns)")
ax.set_ylabel("Population")
ax.set_title("One full |11> <-> |20> cycle")
ax.legend(loc="center right")
ax.grid(True, alpha=0.3)

ax = axes[2]
ax.plot(tlist * 1e3, np.abs(phi_c) / np.pi, "C2")
ax.axvline(t_cz * 1e3, color="k", ls="--", lw=1, alpha=0.6)
ax.axhline(1.0, color="C3", ls="--", lw=1, alpha=0.6)
ax.set_xlabel("Time on resonance (ns)")
ax.set_ylabel("|Conditional phase| / pi")
ax.set_title("Conditional phase reaches pi at t_CZ")
ax.grid(True, alpha=0.3)

fig.suptitle("CZ gate: park |11> on resonance with |20> for one swap cycle")
fig.tight_layout()

# ---------------------------------------------------------------------------
# Save the figure next to this script, then show it interactively.
# ---------------------------------------------------------------------------
figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "cz_gate.png"), dpi=130, bbox_inches="tight")
plt.show()
