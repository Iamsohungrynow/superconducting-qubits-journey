"""
Rabi oscillations of a driven qubit (pure QuTiP simulation).

Physics
-------
A two-level system (qubit) driven on resonance, viewed in the rotating frame,
obeys the time-independent Hamiltonian

    H = (Omega / 2) * sigmax

where Omega is the Rabi frequency set by the drive amplitude. Starting from the
ground state |0>, the excited-state population oscillates as

    P1(t) = sin^2(Omega * t / 2)

so the population completes a full cycle in the Rabi period T = 2*pi / Omega, and
reaches its first maximum (a pi-pulse, full population inversion) at t = pi / Omega.

Convention
----------
|0> = basis(2, 0) is the GROUND state.
|1> = basis(2, 1) is the EXCITED state.
num(2) = |1><1| measures the excited-state population directly.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, num, sigmax, sesolve

# ---------------------------------------------------------------------------
# Parameters (illustrative, clearly labelled).
# Frequencies are angular: Omega = 2*pi * f, with f in MHz and time in us.
# A 5 MHz drive (f = 5) gives a Rabi period of 200 ns = 0.2 us.
# We use slower, easier-to-read drives so the oscillations span ~microseconds.
# ---------------------------------------------------------------------------
omegas = [2 * np.pi * 5.0,    # 5 MHz Rabi drive  (Omega in rad/us)
          2 * np.pi * 10.0,   # 10 MHz Rabi drive
          2 * np.pi * 20.0]   # 20 MHz Rabi drive
labels = ["5 MHz", "10 MHz", "20 MHz"]

# Time grid in microseconds. 0.5 us is long enough to show several cycles
# of the fastest drive and at least one cycle of the slowest.
tlist = np.linspace(0.0, 0.5, 1000)

# Initial state: ground state |0>.
psi0 = basis(2, 0)

# Operator whose expectation value is the excited-state population P1.
P1_op = num(2)

# ---------------------------------------------------------------------------
# Simulate and plot one Rabi trace per drive amplitude.
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

print("Rabi oscillation simulation")
print("=" * 60)

for Omega, label, color in zip(omegas, labels, ["C0", "C1", "C2"]):
    # Rotating-frame, on-resonance Hamiltonian.
    H = 0.5 * Omega * sigmax()

    # Schroedinger-equation solve (closed system, no decay).
    result = sesolve(H, psi0, tlist, e_ops=[P1_op])
    P1 = result.expect[0]

    # Analytic Rabi quantities.
    rabi_period = 2 * np.pi / Omega   # full oscillation period (us)
    pi_pulse = np.pi / Omega          # first full inversion (us)
    rabi_freq_MHz = Omega / (2 * np.pi)  # linear Rabi frequency (MHz, since 1/us = MHz)

    # Extract the Rabi frequency numerically from the simulated trace by
    # locating the first time P1 crosses 0.5 on the way up; P1 = sin^2(Omega t / 2)
    # equals 0.5 at Omega t / 2 = pi/4, i.e. t = pi / (2 Omega) = quarter period.
    above = np.where(P1 >= 0.5)[0]
    if above.size > 0:
        t_half = tlist[above[0]]
        extracted_freq_MHz = 1.0 / (4.0 * t_half) if t_half > 0 else float("nan")
    else:
        extracted_freq_MHz = float("nan")

    print(f"Drive {label:>7}:  Omega = {Omega:7.3f} rad/us")
    print(f"    analytic  Rabi frequency = {rabi_freq_MHz:7.3f} MHz")
    print(f"    extracted Rabi frequency = {extracted_freq_MHz:7.3f} MHz")
    print(f"    Rabi period T = {rabi_period*1e3:7.3f} ns,"
          f"  pi-pulse time = {pi_pulse*1e3:7.3f} ns")

    ax.plot(tlist * 1e3, P1, color=color,
            label=f"{label}  (T = {rabi_period*1e3:.0f} ns)")

    # Annotate the pi-pulse time for the slowest (clearest) drive only.
    if Omega == omegas[0]:
        ax.axvline(pi_pulse * 1e3, color=color, ls="--", lw=1, alpha=0.6)
        ax.annotate("pi-pulse\n(full inversion)",
                    xy=(pi_pulse * 1e3, 1.0),
                    xytext=(pi_pulse * 1e3 + 30, 0.78),
                    arrowprops=dict(arrowstyle="->", color=color),
                    color=color, fontsize=9)
        ax.annotate("Rabi period T",
                    xy=(rabi_period * 1e3, 0.02),
                    xytext=(rabi_period * 1e3 + 5, 0.18),
                    color=color, fontsize=9)

print("=" * 60)
print("Note: the Rabi frequency scales LINEARLY with the drive amplitude Omega.")

ax.set_xlabel("Time (ns)")
ax.set_ylabel("Excited-state population  P1 = <num(2)>")
ax.set_title("Rabi oscillations: on-resonance driven qubit (rotating frame)")
ax.set_ylim(-0.05, 1.1)
ax.legend(loc="upper right")
ax.grid(True, alpha=0.3)

# ---------------------------------------------------------------------------
# Save the figure next to this script, then show it interactively.
# ---------------------------------------------------------------------------
figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "rabi.png"), dpi=130, bbox_inches="tight")
plt.show()
