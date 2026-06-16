"""
Qubit states and the Bloch sphere with QuTiP (pure simulation).

This lab introduces the single qubit as a state in a 2D Hilbert space,
shows the Pauli operators and their expectation values, visualises a few
canonical states on the Bloch sphere, and then drives the qubit with an
X (sigmax) Hamiltonian to watch it precess across the sphere.

Convention used throughout:
    |0> = basis(2, 0) = GROUND state
    |1> = basis(2, 1) = EXCITED state
For relaxation we use destroy(2) as the lowering operator, which correctly
sends |1> -> |0>. (QuTiP's sigmam()/sigmap() naming is inverted relative to
this ground/excited convention, so we avoid them for collapse operators.)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, sigmax, sigmay, sigmaz, sesolve, expect, Bloch


# ----------------------------------------------------------------------
# 1. Build basic qubit states
# ----------------------------------------------------------------------
# Computational basis states.
ket0 = basis(2, 0)          # |0>, ground
ket1 = basis(2, 1)          # |1>, excited

# Equal superpositions. Normalisation by 1/sqrt(2) keeps <psi|psi> = 1.
plus = (ket0 + ket1).unit()             # (|0> + |1>)/sqrt(2), points along +x
plus_i = (ket0 + 1j * ket1).unit()      # (|0> + i|1>)/sqrt(2), points along +y

# Name the states so we can loop over them cleanly.
states = {
    "|0>          (ground)":     ket0,
    "|1>          (excited)":    ket1,
    "(|0>+|1>)/r2 (plus, +x)":   plus,
    "(|0>+i|1>)/r2 (plus_i,+y)": plus_i,
}


# ----------------------------------------------------------------------
# 2. Pauli operators and expectation values
# ----------------------------------------------------------------------
# The three Pauli operators are the measurement axes of the Bloch sphere.
sx, sy, sz = sigmax(), sigmay(), sigmaz()

print("=" * 60)
print("Expectation values <sx>, <sy>, <sz> for each named state")
print("(these are exactly the Bloch vector components x, y, z)")
print("=" * 60)
for name, psi in states.items():
    ex = expect(sx, psi)
    ey = expect(sy, psi)
    ez = expect(sz, psi)
    print(f"{name:26s}  <sx>={ex:+.3f}  <sy>={ey:+.3f}  <sz>={ez:+.3f}")
print()


# ----------------------------------------------------------------------
# 3. Plot the named states on a Bloch sphere
# ----------------------------------------------------------------------
# A pure state |psi> maps to the Bloch vector (<sx>, <sy>, <sz>).
b_states = Bloch()
b_states.point_marker = ["o"]
for psi in states.values():
    b_states.add_states(psi)


# ----------------------------------------------------------------------
# 4. Drive the qubit with an X Hamiltonian and follow the trajectory
# ----------------------------------------------------------------------
# Illustrative parameters. The Rabi/drive strength is written as 2*pi*(frequency in MHz) so
# that, with time measured in microseconds, the phase is dimensionless.
Omega = 2 * np.pi * 5.0          # X-drive (Rabi) strength, rad/us  (5 MHz-ish scale)
H = 0.5 * Omega * sx             # H = (Omega/2) sigmax drives Rabi oscillations

# Start in the ground state and evolve coherently (Schrodinger equation).
psi0 = ket0
tlist = np.linspace(0.0, 0.5, 200)   # microseconds

# sesolve integrates the closed-system dynamics and returns <sx>,<sy>,<sz>.
result = sesolve(H, psi0, tlist, e_ops=[sx, sy, sz])
xs, ys, zs = result.expect[0], result.expect[1], result.expect[2]

# Report a couple of quantitative checkpoints along the Rabi oscillation.
# A full population flip |0> -> |1> happens after time pi/Omega.
t_pi = np.pi / Omega
print("=" * 60)
print("X-drive Rabi oscillation from |0>")
print("=" * 60)
print(f"Drive strength Omega/2pi = {Omega / (2 * np.pi):.3f} MHz")
print(f"Predicted pi-pulse time  = {t_pi:.4f} us")
print(f"<sz> at t=0              = {zs[0]:+.3f}  (expect +1, ground)")
print(f"min <sz> over the sweep  = {zs.min():+.3f}  (approaches -1 at the flip)")
print()


# ----------------------------------------------------------------------
# 5. Plot the driven trajectory on a second Bloch sphere
# ----------------------------------------------------------------------
# The X drive rotates the state in the y-z plane; <sx> stays ~0 throughout.
b_traj = Bloch()
b_traj.point_marker = ["o"]
b_traj.add_points([xs, ys, zs], meth="l")   # connect the trajectory as a line


# ----------------------------------------------------------------------
# 6. Render both spheres side by side and save next to this script
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(11, 5))

ax1 = fig.add_subplot(1, 2, 1, projection="3d")
b_states.fig = fig
b_states.axes = ax1
b_states.render()
ax1.set_title("Named states")

ax2 = fig.add_subplot(1, 2, 2, projection="3d")
b_traj.fig = fig
b_traj.axes = ax2
b_traj.render()
ax2.set_title("X-drive trajectory from |0>")

figdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(figdir, exist_ok=True)
plt.savefig(os.path.join(figdir, "bloch.png"), dpi=130, bbox_inches="tight")
plt.show()
