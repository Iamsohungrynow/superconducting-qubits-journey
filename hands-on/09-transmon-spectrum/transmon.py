"""Charge-basis transmon spectrum. Energies divided by h are in GHz.

Run from the repository root: python hands-on/09-transmon-spectrum/transmon.py
The finite charge cutoff is checked against a larger basis before plotting.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from scipy.constants import h, e


def levels(ec, ej, ng=0.0, cutoff=20):
    """Lowest four eigenvalues of H/h in GHz; n counts Cooper pairs."""
    n = np.arange(-cutoff, cutoff + 1)
    return eigh_tridiagonal(4 * ec * (n - ng)**2,
                            np.full(2 * cutoff, -ej / 2),
                            select="i", select_range=(0, 3))[0]


def main():
    ec, ej = 0.25, 12.5
    ng = np.linspace(-0.5, 0.5, 201)
    spectra = np.array([levels(ec, ej, x) for x in ng])
    reference = np.array([levels(ec, ej, x, cutoff=30) for x in ng])
    convergence = np.max(np.abs(spectra - reference))
    np.testing.assert_allclose(spectra, reference, atol=1e-9, rtol=0)
    f01 = spectra[:, 1] - spectra[:, 0]
    alpha = spectra[:, 2] - 2 * spectra[:, 1] + spectra[:, 0]
    approx = np.sqrt(8 * ej * ec) - ec
    print(f"EC/h={ec} GHz, EJ/EC={ej/ec:g}")
    print(f"C={e**2/(2*h*ec*1e9)*1e15:.2f} fF")
    print(f"f01(ng=0)={f01[100]:.6f} GHz; quartic estimate={approx:.6f} GHz")
    print(f"alpha/2pi={alpha[100]*1e3:.3f} MHz; leading estimate={-ec*1e3:.1f} MHz")
    print(f"Transition charge dispersion={np.ptp(f01)*1e6:.3f} kHz")
    print(f"Cutoff 20 -> 30: max energy change={convergence*1e9:.3g} Hz")
    assert 9 < np.ptp(f01)*1e6 < 11
    ratios = np.linspace(5, 100, 120)
    exact = np.array([np.diff(levels(ec, ec*r))[:2] for r in ratios])
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")
    axes[0].plot(ng, (f01 - f01[100])*1e6)
    axes[0].set(xlabel="Offset charge ng (Cooper pairs)", ylabel="f01 - f01(0) (kHz)",
                title="Small does not mean zero")
    axes[1].plot(ratios, exact[:, 0], label="charge-basis diagonalization")
    axes[1].plot(ratios, np.sqrt(8*ratios)*ec-ec, "--", label="quartic approximation")
    axes[1].set(xlabel="EJ / EC", ylabel="f01 (GHz)", title="Test the approximation")
    axes[1].legend(fontsize=8)
    axes[2].plot(ratios, (exact[:, 1]-exact[:, 0])*1e3)
    axes[2].axhline(-ec*1e3, ls="--", color="C1", label="-EC/h")
    axes[2].set(xlabel="EJ / EC", ylabel="alpha / 2pi (MHz)", title="Anharmonicity at fixed EC")
    axes[2].legend()
    for ax in axes:
        ax.grid(alpha=.25)
    out = Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "transmon.png", dpi=140)
    plt.show()
    return {"dispersion_khz": float(np.ptp(f01)*1e6), "convergence_ghz": float(convergence)}


if __name__ == "__main__":
    metrics = main()
