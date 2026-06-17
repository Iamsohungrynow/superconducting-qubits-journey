"""
Dispersive readout: the cavity field encodes the qubit state.

In circuit QED a qubit is coupled to a microwave cavity. When the qubit and
cavity are far detuned, the interaction reduces to a dispersive coupling:

    H_disp = -chi * sigmaz * a.dag() * a

The cavity frequency is pulled by -chi or +chi depending on whether the qubit
is in |0> (ground) or |1> (excited). If we drive the cavity on resonance, the
steady-state coherent field <a> lands at a DIFFERENT point in the IQ plane for
each qubit state. Measuring that field IS the qubit readout.

This script works entirely in the cavity rotating frame, drives the cavity,
solves the open-system dynamics with cavity decay, and plots the field
trajectory <a> in the complex (I, Q) plane for the qubit prepared in |0> and
|1>. The separation between the two steady-state points is the readout signal.

Convention used throughout:
    |0> = basis(2, 0) = GROUND state
    |1> = basis(2, 1) = EXCITED state
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import (basis, destroy, qeye, sigmaz, tensor, mesolve, ket2dm,
                   steadystate, expect)

# ---------------------------------------------------------------------------
# Parameters (illustrative but realistic; frequencies as 2*pi*MHz, time in us)
# ---------------------------------------------------------------------------
N = 20                       # cavity Fock-space truncation
chi = 2 * np.pi * 5.0        # dispersive shift, 5 MHz
drive = 2 * np.pi * 5.0      # cavity drive amplitude, 5 MHz
kappa = 2 * np.pi * 5.0      # cavity decay rate, 5 MHz

# Drive detuning. We work in the frame rotating at the DRIVE frequency, which
# we place exactly halfway between the two qubit-pulled cavity resonances (the
# symmetric readout point). In that frame each qubit state sees an effective
# cavity detuning of -chi or +chi, so the two steady-state fields land on
# opposite sides of the IQ plane and are maximally separated.
delta = 0.0                  # bare cavity detuning at the symmetric point

# Time grid for the trajectory plot. The coherent field amplitude relaxes as
# exp(-(kappa/2) t), so its envelope settles on a timescale 2/kappa (here
# 2/kappa ~ 0.064 us = 64 ns), NOT 1/kappa. We integrate well past that (several settling
# times) so the trajectory visibly spirals in and lands on the steady state.
# The reported landing points themselves come from the exact steady state
# (steadystate(), below), not from the last transient sample.
tlist = np.linspace(0, 0.4, 800)

# ---------------------------------------------------------------------------
# Operators on the joint qubit (x) cavity Hilbert space
# ---------------------------------------------------------------------------
a = tensor(qeye(2), destroy(N))   # cavity lowering operator
sz = tensor(sigmaz(), qeye(N))    # qubit sigmaz

# Hamiltonian in the frame rotating at the drive frequency:
#   H = delta * a.dag() a          (bare cavity detuning from the drive)
#       - chi * sigmaz * a.dag() a (qubit-state-dependent cavity pull)
#       + drive * (a + a.dag())    (coherent cavity drive)
# For each qubit state sigmaz = +/-1, so the cavity sees an effective detuning
# (delta -/+ chi); driving at the symmetric point (delta = 0) gives the two
# states opposite -chi / +chi detunings and maximal IQ separation.
H = delta * a.dag() * a - chi * sz * a.dag() * a + drive * (a + a.dag())

# Cavity decay is the only dissipation we model here.
c_ops = [np.sqrt(kappa) * a]

# ---------------------------------------------------------------------------
# Initial states: cavity in vacuum, qubit in |0> or in |1>
# ---------------------------------------------------------------------------
vac = basis(N, 0)
psi_ground = tensor(basis(2, 0), vac)    # qubit |0>
psi_excited = tensor(basis(2, 1), vac)   # qubit |1>

# Solve the master equation for both qubit states, tracking <a>.
res_g = mesolve(H, ket2dm(psi_ground), tlist, c_ops, e_ops=[a])
res_e = mesolve(H, ket2dm(psi_excited), tlist, c_ops, e_ops=[a])

a_g = np.asarray(res_g.expect[0])   # complex <a>(t) for qubit |0>
a_e = np.asarray(res_e.expect[0])   # complex <a>(t) for qubit |1>

# ---------------------------------------------------------------------------
# Quantitative results: steady-state field points and their separation.
#
# We get the landing points from the EXACT steady state, not from a_g[-1]/
# a_e[-1] (which would be biased by whatever transient survives at t_final).
# Because the Hamiltonian commutes with the qubit sigmaz and the qubit has no
# dissipation, each qubit state |0>/|1> just fixes the cavity detuning to
# -chi/+chi. So the steady-state field is that of a single driven, damped
# cavity mode with detuning +/- chi, which steadystate() solves directly.
# ---------------------------------------------------------------------------
ac = destroy(N)   # single-mode cavity operator (qubit factored out)


def cavity_steady_field(sz_value):
    """Exact steady-state <a> for the cavity when sigmaz = sz_value (+1 -> |0>,
    -1 -> |1>), i.e. effective cavity detuning delta - sz_value*chi."""
    H_cav = (delta - sz_value * chi) * ac.dag() * ac + drive * (ac + ac.dag())
    rho_ss = steadystate(H_cav, [np.sqrt(kappa) * ac])
    return expect(ac, rho_ss)


ss_g = cavity_steady_field(+1.0)   # qubit |0>  (sigmaz = +1)
ss_e = cavity_steady_field(-1.0)   # qubit |1>  (sigmaz = -1)
separation = np.abs(ss_e - ss_g)

print("Dispersive readout simulation")
print("-----------------------------")
print(f"chi/2pi   = {chi / (2 * np.pi):.1f} MHz")
print(f"kappa/2pi = {kappa / (2 * np.pi):.1f} MHz")
print(f"drive/2pi = {drive / (2 * np.pi):.1f} MHz")
print()
print(f"Steady-state field, qubit |0>: I = {ss_g.real:+.4f}, Q = {ss_g.imag:+.4f}")
print(f"Steady-state field, qubit |1>: I = {ss_e.real:+.4f}, Q = {ss_e.imag:+.4f}")
print(f"|<a>| for |0> = {np.abs(ss_g):.4f}")
print(f"|<a>| for |1> = {np.abs(ss_e):.4f}")
print()
print(f"IQ separation between the two qubit states = {separation:.4f}")
print("This separation is the readout signal: a larger value means the two")
print("qubit states are easier to distinguish in a single measurement.")

# ---------------------------------------------------------------------------
# Plot: cavity field trajectory in the IQ plane for both qubit states
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 6))

ax.plot(a_g.real, a_g.imag, color="tab:blue", lw=1.5, label="qubit |0> (ground)")
ax.plot(a_e.real, a_e.imag, color="tab:red", lw=1.5, label="qubit |1> (excited)")

# Mark the steady-state landing points.
ax.scatter([ss_g.real], [ss_g.imag], color="tab:blue", s=80, zorder=5)
ax.scatter([ss_e.real], [ss_e.imag], color="tab:red", s=80, zorder=5)

# Draw the separation between the two steady-state points.
ax.annotate(
    "",
    xy=(ss_e.real, ss_e.imag),
    xytext=(ss_g.real, ss_g.imag),
    arrowprops=dict(arrowstyle="<->", color="black", lw=1.2),
)
mid = 0.5 * (ss_g + ss_e)
ax.text(mid.real, mid.imag, f"  separation = {separation:.3f}", fontsize=10)

ax.scatter([0], [0], color="gray", marker="+", s=60)  # origin (vacuum)
ax.set_xlabel("I = Re<a>")
ax.set_ylabel("Q = Im<a>")
ax.set_title("Dispersive readout: cavity field separates by qubit state")
ax.axhline(0, color="lightgray", lw=0.6)
ax.axvline(0, color="lightgray", lw=0.6)
ax.set_aspect("equal", adjustable="datalim")
ax.legend(loc="best")
ax.grid(True, alpha=0.3)

# Save the figure next to this script.
figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "dispersive.png"), dpi=130, bbox_inches="tight")
plt.show()
