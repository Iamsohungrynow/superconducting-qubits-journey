"""Ramsey and echo filter integrals for classical Gaussian frequency noise.

Use a one-sided PSD S_f(f) of frequency fluctuations in (Hz)^2/Hz,
f in Hz and t in seconds. chi(t) = (2pi)^2/2 integral S_f |G|^2 df.
Ideal instantaneous echo pulses; independent Markovian T1 relaxation.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def filters(f, t):
    x = f[:, None]*t[None, :]
    ramsey = t[None, :]**2*np.sinc(x)**2
    echo = t[None, :]**2*np.sin(np.pi*x/2)**2*np.sinc(x/2)**2
    return ramsey, echo


def main():
    frequencies = np.geomspace(1, 1e8, 12000)
    times = np.linspace(0, 100e-6, 401)
    psd = (1e4)**2 / frequencies  # 10 kHz/sqrt(Hz) at 1 Hz, explicit cutoffs
    ramsey, echo = filters(frequencies, times)
    exponents = [2*np.pi**2*np.trapezoid(psd[:, None]*gf, frequencies, axis=0)
                 for gf in (ramsey, echo)]
    # Repeat quadrature on a denser grid: a numerical convergence check.
    dense_f = np.geomspace(1, 1e8, 24000)
    dense_filters = filters(dense_f, times[::20])
    for exponent, gf in zip(exponents, dense_filters):
        dense = 2*np.pi**2*np.trapezoid((1e8/dense_f)[:, None]*gf, dense_f, axis=0)
        np.testing.assert_allclose(exponent[::20], dense, rtol=2e-3, atol=1e-7)
    t1 = 100e-6
    coherence = [np.exp(-times/(2*t1)-x) for x in exponents]
    assert coherence[1][100] > coherence[0][100]
    r0, e0 = filters(np.array([0.]), np.array([10e-6]))
    np.testing.assert_allclose(r0, (10e-6)**2, atol=1e-20)
    assert e0[0, 0] == 0
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
    for label, curve in zip(("Ramsey", "Hahn echo"), coherence):
        axes[0].plot(times*1e6, curve, label=label)
        idx = np.flatnonzero(curve <= np.exp(-1))
        print(f"{label}: 1/e time " + (f"{times[idx[0]]*1e6:.2f} us (grid estimate)" if idx.size else ">100 us"))
    axes[0].plot(times*1e6, np.exp(-times/(2*t1)), "--", label="T1-only envelope")
    axes[0].set(xlabel="Time (us)", ylabel="Coherence magnitude", title="Same noise, different pulse sequence")
    axes[0].legend()
    gf = filters(frequencies, np.array([20e-6]))
    for label, values in zip(("Ramsey", "Echo"), gf):
        axes[1].loglog(frequencies, np.maximum(values[:, 0]/(20e-6)**2, 1e-12), label=label)
    axes[1].set(xlabel="Noise frequency (Hz)", ylabel="|G|² / t²", ylim=(1e-8, 2), title="Filters at 20 us")
    axes[1].legend()
    out = Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "echo.png", dpi=140)
    plt.show()
    return {"ramsey_at_25us": float(coherence[0][100]), "echo_at_25us": float(coherence[1][100])}


if __name__ == "__main__":
    metrics = main()
