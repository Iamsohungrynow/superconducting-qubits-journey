"""
T1 relaxation and T2 dephasing of a single qubit (pure QuTiP simulation).

We use the Lindblad master equation (mesolve) to model:
  1. T1 inversion recovery: an excited qubit relaxes to the ground state.
  2. Pure dephasing + Ramsey: a superposition loses phase coherence and the
     Ramsey signal <sx> oscillates (because of a detuning) under a decaying
     envelope set by T2*.

We then numerically verify the standard coherence relation:
      1/T2 = 1/(2*T1) + 1/Tphi

CONVENTION
  |0> = basis(2,0) = GROUND state
  |1> = basis(2,1) = EXCITED state
  The qubit lowering operator is destroy(2): it sends |1> -> |0>, which is the
  physical relaxation process. NOTE: do NOT use sigmam() here. In QuTiP the
  Pauli naming is such that sigmam() would act the wrong way on this basis and
  the excited-state population would NOT decay.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, destroy, sigmax, sigmaz, mesolve

# ---------------------------------------------------------------------------
# Parameters (illustrative but realistic; times in microseconds, freqs in MHz)
# ---------------------------------------------------------------------------
T1 = 30.0          # energy relaxation time [us]
Tphi = 40.0        # pure dephasing time   [us]
detuning = 2 * np.pi * 0.5   # Ramsey detuning, 0.5 MHz = 0.5 cycles/us [rad/us]

# Predicted total transverse decay time from the coherence relation.
T2_pred = 1.0 / (1.0 / (2.0 * T1) + 1.0 / Tphi)

# Operators
a = destroy(2)     # lowering operator |1> -> |0>  (correct relaxation operator)
sx = sigmax()
sz = sigmaz()

# ---------------------------------------------------------------------------
# Part 1: T1 inversion recovery
# Start fully excited |1>. Only collapse operator is relaxation.
# Excited-state population P1(t) should follow exp(-t / T1).
# ---------------------------------------------------------------------------
psi1 = basis(2, 1)                       # excited state
c_ops_T1 = [np.sqrt(1.0 / T1) * a]       # relaxation channel
n_op = a.dag() * a                       # number operator -> P1 = <n>

t1_times = np.linspace(0, 4 * T1, 400)
res_T1 = mesolve(0 * sz, psi1, t1_times, c_ops_T1, e_ops=[n_op])
P1 = np.real(res_T1.expect[0])

# Fit T1 from the slope of log(P1): log P1 = -t / T1.
mask = P1 > 1e-3
T1_fit = -1.0 / np.polyfit(t1_times[mask], np.log(P1[mask]), 1)[0]

# ---------------------------------------------------------------------------
# Part 2: Ramsey with pure dephasing
# Start in (|0> + |1>)/sqrt(2). Apply a small detuning so <sx> oscillates,
# and include BOTH relaxation and pure dephasing collapse operators.
# The fringe envelope decays with T2 = 1/(1/(2 T1) + 1/Tphi).
# ---------------------------------------------------------------------------
psi_plus = (basis(2, 0) + basis(2, 1)).unit()
H = 0.5 * detuning * sz                   # detuning Hamiltonian in rotating frame
c_ops_T2 = [
    np.sqrt(1.0 / T1) * a,                # relaxation contributes 1/(2 T1)
    np.sqrt(1.0 / (2.0 * Tphi)) * sz,     # pure dephasing contributes 1/Tphi
]

t2_times = np.linspace(0, 4 * T2_pred, 800)
res_T2 = mesolve(H, psi_plus, t2_times, c_ops_T2, e_ops=[sx])
Sx = np.real(res_T2.expect[0])

# Extract the envelope by fitting log(|peaks|). Use the analytic-signal-free
# approach: fit a decaying line to the running maxima of |Sx|. Simpler and
# robust: fit |Sx| upper envelope via the points where |Sx| is near a peak.
abs_Sx = np.abs(Sx)
# Take local maxima of |Sx| as envelope samples.
peak_idx = [i for i in range(1, len(abs_Sx) - 1)
            if abs_Sx[i] >= abs_Sx[i - 1] and abs_Sx[i] >= abs_Sx[i + 1]
            and abs_Sx[i] > 1e-3]
peak_t = t2_times[peak_idx]
peak_v = abs_Sx[peak_idx]
slope = np.polyfit(peak_t, np.log(peak_v), 1)[0]
T2star_fit = -1.0 / slope

# ---------------------------------------------------------------------------
# Consistency check: measured T2 vs predicted 1/(1/(2 T1) + 1/Tphi)
# ---------------------------------------------------------------------------
inv_T2_from_parts = 1.0 / (2.0 * T1) + 1.0 / Tphi
inv_T2_measured = 1.0 / T2star_fit

print("=== T1 relaxation ===")
print(f"  input  T1            = {T1:.2f} us")
print(f"  fitted T1            = {T1_fit:.2f} us")
print()
print("=== T2 Ramsey (dephasing) ===")
print(f"  predicted T2         = {T2_pred:.2f} us")
print(f"  fitted    T2*        = {T2star_fit:.2f} us")
print()
print("=== Consistency: 1/T2 = 1/(2 T1) + 1/Tphi ===")
print(f"  1/(2 T1) + 1/Tphi    = {inv_T2_from_parts:.5f} 1/us")
print(f"  1/T2 (measured)      = {inv_T2_measured:.5f} 1/us")
print(f"  relative error       = {abs(inv_T2_measured - inv_T2_from_parts) / inv_T2_from_parts * 100:.2f} %")

# ---------------------------------------------------------------------------
# Figure: two panels (T1 decay; Ramsey fringes with envelope)
# ---------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

ax1.plot(t1_times, P1, lw=2, label="P1(t) = <n>")
ax1.plot(t1_times, np.exp(-t1_times / T1), "k--", lw=1.5, label="exp(-t/T1)")
ax1.set_xlabel("time [us]")
ax1.set_ylabel("excited population P1")
ax1.set_title(f"T1 inversion recovery  (fit T1 = {T1_fit:.1f} us)")
ax1.legend()
ax1.grid(alpha=0.3)

ax2.plot(t2_times, Sx, lw=1, label="<sx>(t)")
ax2.plot(t2_times, np.exp(-t2_times / T2star_fit), "r--", lw=1.5, label="+envelope")
ax2.plot(t2_times, -np.exp(-t2_times / T2star_fit), "r--", lw=1.5)
ax2.set_xlabel("time [us]")
ax2.set_ylabel("<sx>")
ax2.set_title(f"Ramsey fringes  (fit T2* = {T2star_fit:.1f} us)")
ax2.legend()
ax2.grid(alpha=0.3)

fig.tight_layout()

figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "t1_t2.png"), dpi=130, bbox_inches="tight")
plt.show()
