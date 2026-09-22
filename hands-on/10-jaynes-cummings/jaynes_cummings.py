"""Exact single-excitation JC block versus dispersive perturbation theory.

Basis: |e,0>, |g,1>. H/hbar and g are in rad/us; time is in us.
The common cavity frequency is removed by a rotating frame.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm


def main():
    g = 2*np.pi*100
    detunings = 2*np.pi*np.linspace(-2000, 2000, 801)
    energies = np.array([np.linalg.eigvalsh([[d, g], [g, 0]]) for d in detunings])
    np.testing.assert_allclose(energies[400, 1]-energies[400, 0], 2*g)
    # Pick the eigenvalue connected to the bare cavity at large |Delta|.
    cavity_shift = np.where(detunings < 0, energies[:, 1], energies[:, 0])
    far = np.abs(detunings) >= 10*g
    approx = -g*g/detunings[far]
    relative_error = np.max(np.abs((cavity_shift[far]-approx)/approx))
    assert relative_error < .011
    times = np.linspace(0, .025, 501)
    hamiltonian = np.array([[0, g], [g, 0]])
    population = np.array([abs((expm(-1j*hamiltonian*t) @ [1, 0])[0])**2 for t in times])
    np.testing.assert_allclose(population, np.cos(g*times)**2, atol=1e-12)
    print(f"Resonant splitting / 2pi={2*g/(2*np.pi):.1f} MHz")
    print(f"Full excitation swap at {np.pi/(2*g)*1e3:.2f} ns")
    print(f"Max dispersive relative error for |Delta| >= 10g: {relative_error:.3%}")
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")
    axes[0].plot(detunings/(2*np.pi), energies/(2*np.pi))
    axes[0].set(xlabel="Delta / 2pi (MHz)", ylabel="Energy / h (MHz, cavity frame)", title="Avoided crossing")
    for sign in (-1, 1):
        mask = sign*detunings > 0
        axes[1].plot(detunings[mask]/(2*np.pi), cavity_shift[mask]/(2*np.pi),
                     color="C0", label="exact cavity-like branch" if sign == -1 else None)
    # Split the two wings so no line bridges the invalid region.
    for sign in (-1, 1):
        mask = (sign*detunings >= 5*g)
        axes[1].plot(detunings[mask]/(2*np.pi), -g*g/detunings[mask]/(2*np.pi),
                     "k--", label="-g^2/Delta" if sign == -1 else None)
    axes[1].set(xlabel="Delta / 2pi (MHz)", ylabel="Cavity shift / 2pi (MHz)", title="Approximation fails near resonance")
    axes[1].legend(fontsize=8)
    axes[2].plot(times*1e3, population, label="matrix exponential")
    axes[2].plot(times[::20]*1e3, np.cos(g*times[::20])**2, ".", label="cos²(gt)")
    axes[2].set(xlabel="Time (ns)", ylabel="P(e,0)", title="Vacuum-Rabi exchange")
    axes[2].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=.25)
    for ax in axes[:2]:
        ax.set_xticks([-2000, -1000, 0, 1000, 2000])
    out = Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "jaynes_cummings.png", dpi=140)
    plt.show()
    return {"dispersive_relative_error": float(relative_error)}


if __name__ == "__main__":
    metrics = main()
