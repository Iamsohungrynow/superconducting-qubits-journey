"""
Leakage to |2> and the DRAG correction (pure QuTiP simulation).

Physics
-------
A transmon is not a true two-level system: state |2> sits only one
anharmonicity alpha below where a harmonic level would be (Chapter 03/07).
A short pi-pulse has spectral width ~ 1/t_gate; once that becomes comparable
to |alpha|, the drive also excites the |1> -> |2> transition and population
LEAKS out of the qubit subspace.

In the frame rotating at the drive frequency (on resonance with |0> -> |1>),
the three-level Hamiltonian is

    H(t) = alpha |2><2|  +  (Ox(t)/2) (a + adag)  +  (Oy(t)/2) i(adag - a)

where a is the 3-level lowering operator (so the |1> -> |2> matrix element is
sqrt(2) times the |0> -> |1> one), Ox is the in-phase (I) drive envelope and
Oy the quadrature (Q) envelope.

DRAG (Derivative Removal by Adiabatic Gate, Motzoi et al. 2009) fixes leakage
to first order by adding a quadrature drive proportional to the DERIVATIVE of
the main envelope:

    Oy(t) = -beta * dOx/dt / alpha ,   beta = 1  (first-order DRAG)

This lab drives a Gaussian pi-pulse with and without DRAG, compares the final
leakage P2, sweeps the gate time, and scans beta to find the leakage-optimal
value.

Convention
----------
|0>, |1> are the qubit states; |2> is the leakage level.
alpha < 0 for a transmon (the level spacing shrinks going up).
Frequencies are angular: alpha = 2*pi*(-200) rad/us means -200 MHz.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, destroy, sesolve

# ---------------------------------------------------------------------------
# Parameters (illustrative, clearly labelled).
# Times in us, angular frequencies in rad/us (2*pi * MHz).
# ---------------------------------------------------------------------------
alpha = 2 * np.pi * (-200.0)   # transmon anharmonicity: -200 MHz (rad/us)
t_gate = 0.020                 # gate duration: 20 ns
sigma = t_gate / 4.0           # Gaussian width, a common choice

# Three-level operators.
a = destroy(3)
H0 = alpha * basis(3, 2) * basis(3, 2).dag()   # alpha |2><2|
Hx = 0.5 * (a + a.dag())                       # in-phase (I) drive operator
Hy = 0.5 * 1j * (a.dag() - a)                  # quadrature (Q) drive operator

psi0 = basis(3, 0)                             # start in the ground state
P_ops = [basis(3, n) * basis(3, n).dag() for n in range(3)]  # P0, P1, P2


def gaussian_envelope(t_gate, sigma):
    """Return Ox(t) and dOx/dt for an offset-subtracted Gaussian pi-pulse.

    The envelope is shifted so it starts and ends at exactly zero, and the
    amplitude A is normalized so the pulse area is pi (a pi-pulse):
        integral of Ox(t) dt from 0 to t_gate = pi.
    """
    tc = t_gate / 2.0
    offset = np.exp(-tc**2 / (2 * sigma**2))
    tgrid = np.linspace(0.0, t_gate, 2001)
    area_unit = np.trapezoid(np.exp(-(tgrid - tc) ** 2 / (2 * sigma**2)) - offset,
                             tgrid)
    A = np.pi / area_unit

    def Ox(t):
        return A * (np.exp(-(t - tc) ** 2 / (2 * sigma**2)) - offset)

    def dOx(t):
        return A * (-(t - tc) / sigma**2) * np.exp(-(t - tc) ** 2 / (2 * sigma**2))

    return Ox, dOx, A


def run_pulse(t_gate, sigma, beta, n_t=400):
    """Simulate one pi-pulse; return (tlist, P0(t), P1(t), P2(t))."""
    Ox, dOx, _ = gaussian_envelope(t_gate, sigma)

    def Oy(t):
        return -beta * dOx(t) / alpha          # first-order DRAG quadrature

    H = [H0, [Hx, Ox], [Hy, Oy]]
    tlist = np.linspace(0.0, t_gate, n_t)
    result = sesolve(H, psi0, tlist, e_ops=P_ops)
    return tlist, result.expect[0], result.expect[1], result.expect[2]


# ---------------------------------------------------------------------------
# 1) One 20 ns pi-pulse, with and without DRAG.
# ---------------------------------------------------------------------------
print("DRAG and leakage simulation (3-level transmon)")
print("=" * 60)
Ox, dOx, A = gaussian_envelope(t_gate, sigma)
print(f"anharmonicity alpha/2pi = {alpha/2/np.pi:7.1f} MHz")
print(f"gate time               = {t_gate*1e3:7.1f} ns, sigma = {sigma*1e3:.1f} ns")
print(f"peak Rabi rate  A/2pi   = {Ox(t_gate/2)/2/np.pi:7.1f} MHz")

results = {}
for beta, name in [(0.0, "no DRAG"), (1.0, "DRAG")]:
    tlist, P0, P1, P2 = run_pulse(t_gate, sigma, beta)
    results[name] = (tlist, P0, P1, P2)
    print(f"{name:>8}:  final P1 = {P1[-1]:.6f}   final leakage P2 = {P2[-1]:.2e}")

supp = results["no DRAG"][3][-1] / results["DRAG"][3][-1]
print(f"DRAG suppresses the final leakage by a factor of {supp:,.0f}")

# ---------------------------------------------------------------------------
# 2) Final leakage vs gate time: shorter gate -> broader spectrum -> more
#    leakage; DRAG buys roughly two orders of magnitude.
# ---------------------------------------------------------------------------
gate_times = np.linspace(0.008, 0.050, 22)    # 8 ns to 50 ns
leak = {0.0: [], 1.0: []}
for tg in gate_times:
    for beta in (0.0, 1.0):
        _, _, _, P2 = run_pulse(tg, tg / 4.0, beta, n_t=200)
        leak[beta].append(P2[-1])

# ---------------------------------------------------------------------------
# 3) Scan the DRAG coefficient beta: leakage is minimized near beta = 1.
# ---------------------------------------------------------------------------
betas = np.linspace(-0.5, 2.5, 61)
leak_beta = []
for b in betas:
    _, _, _, P2 = run_pulse(t_gate, sigma, b, n_t=200)
    leak_beta.append(P2[-1])
beta_opt = betas[int(np.argmin(leak_beta))]
print(f"beta scan: leakage-optimal beta = {beta_opt:.2f} (first-order theory: 1)")
print("=" * 60)
print("Note: leakage grows rapidly as gates shorten; DRAG postpones the problem.")

# ---------------------------------------------------------------------------
# Plot: populations during the pulse / leakage vs gate time / beta scan.
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

ax = axes[0]
for name, color in [("no DRAG", "C3"), ("DRAG", "C0")]:
    tlist, P0, P1, P2 = results[name]
    ax.semilogy(tlist * 1e3, np.maximum(P2, 1e-12), color=color, label=f"P2, {name}")
ax.set_xlabel("Time (ns)")
ax.set_ylabel("Leakage population P2")
ax.set_title(f"Leakage during a {t_gate*1e3:.0f} ns pi-pulse")
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1]
ax.semilogy(gate_times * 1e3, leak[0.0], "o-", color="C3", label="Gaussian only")
ax.semilogy(gate_times * 1e3, leak[1.0], "s-", color="C0", label="Gaussian + DRAG")
ax.set_xlabel("Gate time (ns)")
ax.set_ylabel("Final leakage P2")
ax.set_title("Leakage vs gate time")
ax.legend()
ax.grid(True, alpha=0.3, which="both")

ax = axes[2]
ax.semilogy(betas, leak_beta, "-", color="C2")
ax.axvline(1.0, color="k", ls="--", lw=1, alpha=0.6)
ax.set_xlabel("DRAG coefficient beta")
ax.set_ylabel("Final leakage P2")
ax.set_title("Leakage vs DRAG coefficient (min near beta = 1)")
ax.grid(True, alpha=0.3, which="both")

fig.suptitle("DRAG: cancelling leakage to |2> with a derivative quadrature pulse")
fig.tight_layout()

# ---------------------------------------------------------------------------
# Save the figure next to this script, then show it interactively.
# ---------------------------------------------------------------------------
figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "drag.png"), dpi=130, bbox_inches="tight")
plt.show()
