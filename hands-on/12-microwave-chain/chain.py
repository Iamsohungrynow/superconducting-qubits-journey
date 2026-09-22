"""Thermal attenuator cascade and input-referred amplifier noise, SI units."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, k


def occupation(f, temperature):
    return 1/np.expm1(h*f/(k*temperature))


def cascade(f, attenuation_db, temperatures):
    result = [occupation(f, 300.)]
    for db, temperature in zip(attenuation_db, temperatures, strict=True):
        transmission = 10**(-db/10)
        result.append(transmission*result[-1] + (1-transmission)*occupation(f, temperature))
    return np.array(result)


def main():
    f = 7e9
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
    outputs = []
    for middle in (10, 20):
        ns = cascade(f, [20, middle, 20], [4, .1, .01])
        outputs.append(ns[-1])
        print(f"20-{middle}-20 dB: occupations {ns}; chip n={ns[-1]:.6f}")
        axes[0].semilogy(range(4), ns, "o-", label=f"20-{middle}-20 dB")
    assert .019 < outputs[0] < .021 and .0023 < outputs[1] < .0025
    # A passive attenuator at the same temperature as its input preserves equilibrium.
    thermal = occupation(f, 4)
    np.testing.assert_allclose(thermal/100+.99*thermal, thermal)
    temperatures = np.array([.3, 5/100, 75/(100*1e4)])
    added = temperatures.sum()/(h*f/k)
    eta_vac = .5/(.5+added)
    print(f"Amplifier-added system noise={temperatures.sum():.6f} K = {added:.4f} photons")
    print(f"Vacuum-normalized efficiency={eta_vac:.4f}; phase-preserving SQL-normalized={2*eta_vac:.4f}")
    axes[0].set(xticks=range(4), xticklabels=["300 K input", "4 K", "100 mK", "10 mK"],
                ylabel="Thermal photons at 7 GHz", title="Every attenuator emits noise")
    axes[0].legend()
    axes[1].bar(["TWPA", "HEMT / G1", "Room / G1G2"], temperatures)
    axes[1].set(yscale="log", ylabel="Input-referred added noise (K)", title="Why the first amplifier matters")
    out = Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "chain.png", dpi=140)
    plt.show()
    return {"chip_occupation_60db": float(outputs[1]), "added_noise_kelvin": float(temperatures.sum())}


if __name__ == "__main__":
    metrics = main()
