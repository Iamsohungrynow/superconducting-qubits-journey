"""
The bit-flip repetition code: majority voting beats physical errors
(pure numpy Monte Carlo).

Physics
-------
The simplest quantum error-correcting code (Chapter 12): store one logical
bit in d physical qubits, |0_L> = |00...0>, |1_L> = |11...1>. If each
physical qubit independently suffers a bit flip with probability p, decoding
by majority vote fails only when more than half the qubits flip:

    P_L(d, p) = sum over k > d/2 of  C(d, k) * p**k * (1-p)**(d-k)

For d = 3 that is the classic  P_L = 3p^2 - 2p^3.

Two lessons drop out immediately:

* Below the break-even point p = 1/2, more qubits help EXPONENTIALLY:
  P_L ~ (const * p)^((d+1)/2). Each +2 of distance buys another power of p.
* Above p = 1/2 redundancy makes things WORSE: the majority is more likely
  to be wrong than any single qubit. Error correction only pays off if the
  hardware is already good enough, the origin of the idea of a threshold.

This is a one-round toy model with perfect syndrome measurement, and it only
fights X (bit-flip) errors; a phase flip on ANY single qubit flips the
logical phase, which is why real codes (like the surface code) must protect
both quadratures at once. Chapter 12 takes it from here.

Convention
----------
A logical error means the majority vote is wrong after one round of
independent physical flips.
"""

import numpy as np
import matplotlib.pyplot as plt
from math import comb
import os

rng = np.random.default_rng(12)

# ---------------------------------------------------------------------------
# Parameters.
# ---------------------------------------------------------------------------
distances = [1, 3, 5, 7]        # number of physical qubits per logical bit
n_shots = 200_000               # Monte Carlo shots per (d, p) point
p_grid_mc = np.logspace(-2.5, np.log10(0.8), 25)   # physical error rates
p_grid_th = np.logspace(-2.5, np.log10(0.8), 400)  # dense grid for theory


def logical_error_analytic(d, p):
    """Majority vote fails when more than d/2 of d qubits flip."""
    return sum(comb(d, k) * p**k * (1 - p) ** (d - k)
               for k in range(d // 2 + 1, d + 1))


def logical_error_montecarlo(d, p, shots):
    """Simulate one round: flip each of d bits with prob p, majority-vote."""
    flips = rng.random((shots, d)) < p
    return np.mean(flips.sum(axis=1) > d // 2)


# ---------------------------------------------------------------------------
# Run and compare.
# ---------------------------------------------------------------------------
print("Bit-flip repetition code: logical vs physical error rate")
print("=" * 66)
print(f"{n_shots:,} Monte Carlo shots per point\n")
print("Logical error rate at p = 1% (analytic | Monte Carlo):")
for d in distances:
    th = logical_error_analytic(d, 0.01)
    mc = logical_error_montecarlo(d, 0.01, 2_000_000)   # extra shots: rare events
    mc_str = f"{mc:10.3e}" if mc > 0 else " no events in 2e6 shots"
    print(f"  d = {d}:  {th:10.3e}  | {mc_str}")
print("(d = 7 failures at p = 1% are so rare that even 2 million shots")
print(" usually see none, that is the exponential suppression at work.)")

print("\nEach +2 of code distance buys roughly another factor of ~30 here")
print("(one more power of p times a combinatorial factor).")
print("Break-even: all curves cross P_L = p at p = 0.5; above it, more")
print("qubits make the logical bit WORSE.")
print("=" * 66)
print("Caveats built into this toy model: one error round, perfect syndrome")
print("measurement, and bit flips only, real codes must also handle phase")
print("flips and noisy measurements (Chapter 12).")

mc_curves = {d: np.array([logical_error_montecarlo(d, p, n_shots)
                          for p in p_grid_mc]) for d in distances}

# ---------------------------------------------------------------------------
# Plot.
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
colors = {1: "0.5", 3: "C0", 5: "C2", 7: "C3"}
for d in distances:
    ax.loglog(p_grid_th, [logical_error_analytic(d, p) for p in p_grid_th],
              "-", color=colors[d], lw=1.5,
              label=f"d = {d}" + ("  (no code)" if d == 1 else ""))
    mask = mc_curves[d] > 0
    ax.loglog(p_grid_mc[mask], mc_curves[d][mask], "o", color=colors[d],
              ms=4, alpha=0.7)
ax.axvline(0.5, color="k", ls="--", lw=1, alpha=0.6)
ax.annotate("break-even\np = 0.5", xy=(0.5, 3e-3), xytext=(0.13, 3e-3),
            fontsize=9, arrowprops=dict(arrowstyle="->", alpha=0.6))
ax.set_xlabel("Physical error probability p")
ax.set_ylabel("Logical error probability P_L")
ax.set_title("Repetition code: below break-even, distance helps exponentially\n"
             "(lines: analytic; dots: Monte Carlo)")
ax.legend(loc="lower right")
ax.grid(True, alpha=0.3, which="both")

# ---------------------------------------------------------------------------
# Save the figure next to this script, then show it interactively.
# ---------------------------------------------------------------------------
figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "repetition.png"), dpi=130, bbox_inches="tight")
plt.show()
