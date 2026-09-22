"""
Generate every figure embedded in the tutorial chapters.

Each figure is computed from the actual physics with the same illustrative
parameters used in the chapters' worked examples, no hand-drawn curves.
Run from this directory:

    python make_figures.py

Requires numpy, scipy, matplotlib.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(42)

h = 6.62607015e-34
hbar = h / (2 * np.pi)
kB = 1.380649e-23


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, name), dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def nbar(f_hz, T):
    return 1.0 / np.expm1(h * f_hz / (kB * T))


def transmon_levels(EC, EJ, ng=0.0, nlev=5, N=40):
    """Exact charge-basis diagonalization; energies in the same units as EC/EJ."""
    n = np.arange(-N, N + 1)
    H = np.diag(4 * EC * (n - ng) ** 2) - 0.5 * EJ * (
        np.eye(2 * N + 1, k=1) + np.eye(2 * N + 1, k=-1))
    return np.linalg.eigvalsh(H)[:nlev]


# ===========================================================================
# 01-tradeoff: exponential charge dispersion vs power-law anharmonicity
# ===========================================================================
r = np.linspace(1, 150, 500)
fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(r, np.exp(-np.sqrt(8 * r)), "C0", lw=2,
            label=r"exponential factor only: $e^{-\sqrt{8E_J/E_C}}$")
ax.semilogy(r, (8 * r) ** -0.5, "C1", lw=2,
            label=r"asymptotic $|\alpha_r| \approx (8E_J/E_C)^{-1/2}$")
ax.axvspan(50, 100, color="0.85", label="common design window")
ax.plot([39], [np.exp(-np.sqrt(8 * 39))], "ko", ms=7)
ax.annotate("worked example\n$E_J/E_C=39$", xy=(39, np.exp(-np.sqrt(8 * 39))),
            xytext=(55, 3e-7), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel("$E_J/E_C$")
ax.set_ylabel("dimensionless magnitude (log scale)")
ax.set_title("Exponential beats power law: the transmon trade-off")
ax.set_ylim(1e-16, 2)
ax.legend(loc="lower left")
ax.grid(True, alpha=0.3, which="both")
save(fig, "01-tradeoff.png")

# ===========================================================================
# 02-harmonic-well: parabola, even ladder, ground-state density
# ===========================================================================
x = np.linspace(-4, 4, 500)          # x = Phi / Phi_zpf
U = 0.25 * x**2                      # U/(hbar w) = (Phi/Phi_zpf)^2 / 4
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, U, "C0", lw=2)
for n in range(4):
    E = n + 0.5
    xt = 2 * np.sqrt(E)              # classical turning point
    ax.hlines(E, -xt, xt, color="C1", lw=1.8)
    ax.text(xt + 0.1, E, f"$E_{n} = {2*n+1}/2\\,\\hbar\\omega_q$",
            va="center", fontsize=9)
psi0 = np.exp(-x**2 / 4) / (2 * np.pi)**0.25  # density has rms x=1
ax.fill_between(x, 0.5, 0.5 + 0.8 * psi0**2, color="C2", alpha=0.4)
ax.annotate("$|\\psi_0(\\Phi)|^2$, rms width $\\Phi_{\\rm zpf}$",
            xy=(1.0, 0.75), xytext=(1.8, 1.1), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.annotate("$E_0$ sits above\nthe well bottom", xy=(-2.0, 0.5),
            xytext=(-3.9, 1.5), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"flux $\Phi/\Phi_{\rm zpf}$")
ax.set_ylabel(r"energy $/\ \hbar\omega_q$")
ax.set_title("The quantum LC well: evenly spaced levels, busy vacuum")
ax.set_ylim(0, 4.5)
ax.grid(True, alpha=0.3)
save(fig, "02-harmonic-well.png")

# ===========================================================================
# 02-thermal-occupation: nbar(5 GHz, T)
# ===========================================================================
T = np.logspace(np.log10(0.008), 0, 400)
fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(T * 1e3, nbar(5e9, T), "C0", lw=2)
annos = [(0.015, "15 mK fridge", (25, 1e-8), "left"),
         (0.240, r"crossover $\hbar\omega_q/k_B$ = 240 mK", (55, 3e-3), "left"),
         (0.300, "300 mK", (420, 0.03), "left")]
for Tm, lbl, txtpos, ha in annos:
    ax.plot([Tm * 1e3], [nbar(5e9, Tm)], "C3o", ms=6)
    ax.annotate(f"{lbl}\n$\\bar n \\approx$ {nbar(5e9, Tm):.2g}",
                xy=(Tm * 1e3, nbar(5e9, Tm)), xytext=txtpos,
                fontsize=9, ha=ha, arrowprops=dict(arrowstyle="->", alpha=0.6))
ax.set_xlabel("temperature (mK)")
ax.set_ylabel(r"thermal occupation $\bar n$ (5 GHz mode)")
ax.set_title("Why millikelvin: seven orders of magnitude between 300 mK and 15 mK")
ax.set_ylim(1e-14, 30)
ax.grid(True, alpha=0.3, which="both")
save(fig, "02-thermal-occupation.png")

# ===========================================================================
# 03-cosine-well: cosine vs parabola with exact levels (EJ/EC = 50)
# ===========================================================================
EC, EJ = 0.25, 12.5                         # GHz
E = transmon_levels(EC, EJ, nlev=4)
phi = np.linspace(-np.pi, np.pi, 600)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(phi, -EJ * np.cos(phi), "C0", lw=2, label=r"$-E_J\cos\varphi$")
ax.plot(phi, -EJ + 0.5 * EJ * phi**2, "C1--", lw=1.5,
        label=r"parabola $-E_J + \frac{1}{2} E_J\varphi^2$")
for m in range(4):
    xt = np.arccos(np.clip(-E[m] / EJ, -1, 1))
    ax.hlines(E[m], -xt, xt, color="C2", lw=1.8)
    ax.text(xt + 0.06, E[m], f"$E_{m}$", va="center", fontsize=9)
ax.annotate("", xy=(0.0, E[1]), xytext=(0.0, E[0]),
            arrowprops=dict(arrowstyle="<->", color="0.2", lw=1.2))
ax.text(0.08, (E[0] + E[1]) / 2,
        rf"$\hbar\omega_{{01}} = {E[1]-E[0]:.2f}$ GHz", fontsize=9)
ax.annotate("", xy=(0.0, E[2]), xytext=(0.0, E[1]),
            arrowprops=dict(arrowstyle="<->", color="0.2", lw=1.2))
ax.text(0.08, (E[1] + E[2]) / 2,
        rf"$\hbar\omega_{{12}} = {E[2]-E[1]:.2f}$ GHz (smaller)", fontsize=9)
ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
ax.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
ax.set_xlabel(r"phase $\varphi$")
ax.set_ylabel("energy / h (GHz)")
ax.set_title(r"Cosine well vs parabola ($E_J/E_C=50$): the gaps shrink upward")
ax.set_ylim(-EJ * 1.05, 5)
ax.legend(loc="upper center", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "03-cosine-well.png")

# ===========================================================================
# 03-charge-dispersion: exact bands, EJ/EC = 1 vs 50
# ===========================================================================
ngs = np.linspace(0, 1, 201)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True)
for ax, ratio in zip(axes, [1, 50]):
    EJr = ratio * EC
    bands = np.array([transmon_levels(EC, EJr, ng=ng, nlev=3) for ng in ngs])
    bands -= transmon_levels(EC, EJr, ng=0, nlev=3)[0]
    for m in range(3):
        ax.plot(ngs, bands[:, m], lw=1.8, label=f"$m={m}$")
    ax.set_xlabel("offset charge $n_g$")
    ax.set_title(f"$E_J/E_C = {ratio}$" +
                 ("  (charge qubit: wildly charge-sensitive)" if ratio == 1
                  else "  (transmon: flat bands)"))
    ax.grid(True, alpha=0.3)
axes[0].set_ylabel(r"$[E_m(n_g) - E_0(0)]/h$ (GHz)")
axes[1].legend(loc="center right", fontsize=9)
save(fig, "03-charge-dispersion.png")

# ===========================================================================
# 04-squid-tuning: f01 vs flux for d = 0 and d = 0.3
# ===========================================================================
EJS, ECs = 15.0, 0.25                       # GHz
phi_x = np.linspace(-1, 1, 801)             # Phi / Phi0
fig, ax = plt.subplots(figsize=(8, 5))
for d, color, lbl in [(0.0, "C0", "symmetric $d=0$"), (0.3, "C1", "asymmetric $d=0.3$")]:
    EJeff = EJS * np.sqrt(np.cos(np.pi * phi_x) ** 2 + d**2 * np.sin(np.pi * phi_x) ** 2)
    f01 = np.sqrt(8 * EJeff * ECs) - ECs
    valid = EJeff / ECs > 10                # transmon formula credibility
    ax.plot(np.where(valid, phi_x, np.nan), np.where(valid, f01, np.nan),
            color, lw=2, label=lbl)
    ax.plot(np.where(~valid, phi_x, np.nan), np.where(~valid, f01, np.nan),
            color, lw=1, ls=":", alpha=0.7)
for p0 in (-1, 0, 1):
    ax.plot([p0], [np.sqrt(8 * EJS * ECs) - ECs], "ko", ms=7, zorder=5)
d = 0.3
f_half = np.sqrt(8 * EJS * d * ECs) - ECs
for p0 in (-0.5, 0.5):
    ax.plot([p0], [f_half], "o", ms=7, mfc="white", mec="C1", zorder=5)
ax.annotate("sweet spots ($d\\omega/d\\Phi = 0$)", xy=(0, np.sqrt(8 * EJS * ECs) - ECs),
            xytext=(0.06, 5.9), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.annotate("second sweet spot of the\nasymmetric SQUID", xy=(0.5, f_half),
            xytext=(0.12, 1.6), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.annotate("steep flank:\nflux noise bites", xy=(-0.31, 4.3), xytext=(-0.95, 2.2),
            fontsize=9, arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"external flux $\Phi/\Phi_0$")
ax.set_ylabel("$f_{01}$ (GHz)")
ax.set_title("Flux-tuning a SQUID transmon ($E_{J\\Sigma}/h=15$ GHz, $E_C/h=0.25$ GHz)")
ax.set_ylim(0, 6.4)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "04-squid-tuning.png")

# ===========================================================================
# 05-avoided-crossing: dressed single-excitation frequencies vs qubit freq
# ===========================================================================
wr, g5 = 7.0, 0.1                            # GHz
wq = np.linspace(5, 9, 600)
D = wq - wr
Ep = (wq + wr) / 2 + 0.5 * np.sqrt(D**2 + 4 * g5**2)
Em = (wq + wr) / 2 - 0.5 * np.sqrt(D**2 + 4 * g5**2)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(wq, wq, "k--", lw=1, alpha=0.5, label=r"bare $\omega_q$")
ax.axhline(wr, color="k", ls=":", lw=1, alpha=0.5)
ax.text(5.1, wr + 0.05, r"bare $\omega_r$", fontsize=9)
ax.plot(wq, Ep, "C0", lw=2)
ax.plot(wq, Em, "C0", lw=2, label="dressed branches")
ax.annotate("", xy=(7.0, wr + g5), xytext=(7.0, wr - g5),
            arrowprops=dict(arrowstyle="<->", color="C3"))
ax.text(7.05, wr + 0.12, "min gap $2g$", color="C3", fontsize=9)
ax.annotate(r"cavity-like branch pulled to $\omega_r + g^2/|\Delta|$"
            "\n" r"($= \omega_r - \chi$ with $\chi<0$ here)",
            xy=(5.3, wr + g5**2 / 2), xytext=(5.15, 7.6), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"qubit frequency $\omega_q/2\pi$ (GHz)")
ax.set_ylabel("transition frequency (GHz)")
ax.set_title(r"Vacuum-Rabi avoided crossing ($\omega_r/2\pi=7$ GHz, $g/2\pi=100$ MHz)")
ax.set_ylim(5, 9)
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "05-avoided-crossing.png")

# ===========================================================================
# 05-chi-vs-detuning: two-level vs transmon chi
# ===========================================================================
g_MHz, alpha_MHz = 100.0, -300.0
Dm = np.linspace(-3000, 1000, 4000)
chi2 = g_MHz**2 / Dm
chit = g_MHz**2 / Dm * alpha_MHz / (Dm + alpha_MHz)
chi2[np.abs(Dm) < 30] = np.nan
chit[(np.abs(Dm) < 30) | (np.abs(Dm + alpha_MHz) < 30)] = np.nan
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(Dm / 1000, chi2, "C1--", lw=1.5, label=r"two-level $g^2/\Delta$")
ax.plot(Dm / 1000, chit, "C0", lw=2,
        label=r"transmon $\frac{g^2}{\Delta}\frac{\alpha}{\Delta+\alpha}$")
ax.axvline(0, color="k", ls=":", lw=1, alpha=0.6)
ax.axvline(-alpha_MHz / 1000, color="C3", ls=":", lw=1.2)
ax.text(0.32, 6.5, r"$\Delta=-\alpha$: resonator hits" "\n" r"$|e\rangle\to|f\rangle$ (diverges)",
        color="C3", fontsize=8)
ax.axvspan(0, -alpha_MHz / 1000, color="C3", alpha=0.08)
ax.text(0.02, -8.5, "straddling\nregime", color="C3", fontsize=8)
ax.plot([-2.0], [-0.65], "ko", ms=7)
ax.annotate("worked example:\n$-0.65$ MHz (vs $-5$ naive)", xy=(-2.0, -0.65),
            xytext=(-2.9, -5.5), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"detuning $\Delta/2\pi$ (GHz)")
ax.set_ylabel(r"dispersive shift $\chi/2\pi$ (MHz)")
ax.set_title(r"The third level changes $\chi$ ($g/2\pi=100$ MHz, $\alpha/2\pi=-300$ MHz)")
ax.set_yscale("symlog", linthresh=1)
ax.set_ylim(-200, 200)
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "05-chi-vs-detuning.png")

# ===========================================================================
# 06-resonator-pull: state-dependent Lorentzian response and phase
# ===========================================================================
kappa, chi6 = 2.0, -0.65                    # MHz
dw = np.linspace(-5, 5, 800)
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
for state, center, color in [("|0>", -chi6, "C0"), ("|1>", +chi6, "C3")]:
    mag = 1 / np.sqrt(1 + (2 * (dw - center) / kappa) ** 2)
    ph = -np.degrees(np.arctan(2 * (dw - center) / kappa))
    axes[0].plot(dw, mag, color, lw=2, label=f"qubit in {state}")
    axes[1].plot(dw, ph, color, lw=2)
axes[0].annotate("", xy=(-chi6, 1.03), xytext=(chi6, 1.03),
                 arrowprops=dict(arrowstyle="<->", color="0.3"))
axes[0].text(0, 1.06, r"$2|\chi|/2\pi = 1.3$ MHz", ha="center", fontsize=9)
axes[0].annotate(r"width $\kappa/2\pi = 2$ MHz", xy=(-chi6 + 1.0, 0.71),
                 xytext=(2.3, 0.8), fontsize=9,
                 arrowprops=dict(arrowstyle="->", alpha=0.7))
for ax in axes:
    ax.axvline(0, color="k", ls="--", lw=1, alpha=0.6)
    ax.grid(True, alpha=0.3)
axes[1].annotate("drive at $\\omega_r$:\nmaximal phase contrast", xy=(0, 20),
                 xytext=(1.2, 45), fontsize=9,
                 arrowprops=dict(arrowstyle="->", alpha=0.7))
axes[0].set_ylabel("response magnitude (norm.)")
axes[0].set_ylim(0, 1.15)
axes[0].legend(loc="upper left", fontsize=9)
axes[1].set_ylabel("transmitted phase (deg)")
axes[1].set_xlabel(r"probe detuning $(\omega-\omega_r)/2\pi$ (MHz)")
axes[0].set_title("One resonator, two positions: the qubit state pulls the cavity")
save(fig, "06-resonator-pull.png")

# ===========================================================================
# 06-iq-blobs: single-shot clouds at SNR = 4.33
# ===========================================================================
SNR = 4.33
sep_over_sigma = 2 * np.sqrt(2) * SNR / 2   # so that error = 0.5*erfc(SNR/2)
sigma = 1.0
mu = sep_over_sigma * sigma / 2
n_shots = 2000
I0 = rng.normal(-mu, sigma, n_shots); Q0 = rng.normal(0, sigma, n_shots)
I1 = rng.normal(+mu, sigma, n_shots); Q1 = rng.normal(0, sigma, n_shots)
fig, (ax, axh) = plt.subplots(2, 1, figsize=(8, 7), sharex=True,
                              gridspec_kw={"height_ratios": [3, 1]})
ax.plot(I0, Q0, ".", color="C0", ms=2.5, alpha=0.4, label=r"prepared $|0\rangle$")
ax.plot(I1, Q1, ".", color="C3", ms=2.5, alpha=0.4, label=r"prepared $|1\rangle$")
ax.axvline(0, color="k", ls="--", lw=1.2)
ax.text(0.02, 0.02, "dashed: decision threshold", transform=ax.transAxes,
        fontsize=9)
ax.set_ylabel("integrated Q (arb.)")
ax.set_title(f"Single-shot readout: SNR = {SNR}, overlap error "
             f"$\\approx {0.5*erfc(SNR/2)*100:.2f}$%")
ax.legend(loc="upper left", fontsize=9, markerscale=4)
ax.grid(True, alpha=0.3)
bins = np.linspace(-4 * sigma - mu, 4 * sigma + mu, 80)
axh.hist(I0, bins=bins, color="C0", alpha=0.6)
axh.hist(I1, bins=bins, color="C3", alpha=0.6)
axh.axvline(0, color="k", ls="--", lw=1.2)
axh.set_xlabel("integrated I (arb.)")
axh.set_ylabel("counts")
axh.grid(True, alpha=0.3)
save(fig, "06-iq-blobs.png")

# ===========================================================================
# 07-chevron: P1(t, Delta) colormap + cuts
# ===========================================================================
Om = 2 * np.pi * 25.0                       # rad/us
t7 = np.linspace(0, 0.12, 400)              # us
Dm7 = 2 * np.pi * np.linspace(-75, 75, 301) # rad/us
TT, DD = np.meshgrid(t7, Dm7)
OR = np.sqrt(Om**2 + DD**2)
P1 = (Om**2 / OR**2) * np.sin(OR * TT / 2) ** 2
fig, (axc, axl) = plt.subplots(1, 2, figsize=(12, 4.5),
                               gridspec_kw={"width_ratios": [1.3, 1]})
im = axc.pcolormesh(t7 * 1e3, Dm7 / (2 * np.pi), P1, cmap="viridis",
                    shading="auto", rasterized=True)
fig.colorbar(im, ax=axc, label="$P_1$")
axc.axhline(0, color="w", ls="--", lw=1, alpha=0.8)
axc.axhline(25, color="w", ls=":", lw=1, alpha=0.8)
axc.set_xlabel("pulse duration t (ns)")
axc.set_ylabel(r"detuning $\Delta/2\pi$ (MHz)")
axc.set_title(r"Rabi chevron ($\Omega/2\pi=25$ MHz)")
for Dcut, style, lbl in [(0.0, "-", r"$\Delta=0$: full contrast, $t_\pi=20$ ns"),
                         (2 * np.pi * 25.0, "--",
                          r"$\Delta=\Omega$: $\sqrt{2}$ faster, peak $=1/2$")]:
    ORc = np.sqrt(Om**2 + Dcut**2)
    axl.plot(t7 * 1e3, (Om**2 / ORc**2) * np.sin(ORc * t7 / 2) ** 2, style, lw=2,
             label=lbl)
axl.axvline(20, color="k", ls=":", lw=1, alpha=0.6)
axl.set_xlabel("pulse duration t (ns)")
axl.set_ylabel("$P_1$")
axl.set_ylim(0, 1.05)
axl.legend(fontsize=8, loc="upper right")
axl.grid(True, alpha=0.3)
axl.set_title("horizontal cuts")
save(fig, "07-chevron.png")

# ===========================================================================
# 07-drag: envelopes + 3-level leakage simulation (tg = 10 ns)
# ===========================================================================
alpha7 = 2 * np.pi * (-250.0)               # rad/us
tg7 = 0.010                                 # us
sg7 = tg7 / 4
tc = tg7 / 2
off = np.exp(-tc**2 / (2 * sg7**2))
tt = np.linspace(0, tg7, 2001)
area = np.trapezoid(np.exp(-(tt - tc) ** 2 / (2 * sg7**2)) - off, tt)
A7 = np.pi / area

def envx(t):
    return A7 * (np.exp(-(t - tc) ** 2 / (2 * sg7**2)) - off)

def denvx(t):
    return A7 * (-(t - tc) / sg7**2) * np.exp(-(t - tc) ** 2 / (2 * sg7**2))

def run3(beta):
    a3 = np.diag(np.sqrt([1.0, 2.0]), k=1)
    Hx3 = 0.5 * (a3 + a3.T)
    Hy3 = 0.5j * (a3.T - a3)
    H0 = np.diag([0.0, 0.0, alpha7])

    def rhs(t, y):
        psi = y[:3] + 1j * y[3:]
        Ht = H0 + envx(t) * Hx3 + (-beta * denvx(t) / alpha7) * Hy3
        d = -1j * Ht @ psi
        return np.concatenate([d.real, d.imag])

    ts = np.linspace(0, tg7, 300)
    sol = solve_ivp(rhs, (0, tg7), np.array([1, 0, 0, 0, 0, 0], float),
                    t_eval=ts, rtol=1e-10, atol=1e-12)
    psi = sol.y[:3] + 1j * sol.y[3:]
    return ts, np.abs(psi[2]) ** 2

fig, (axe, axp) = plt.subplots(1, 2, figsize=(12, 4.5))
axe.plot(tt * 1e3, envx(tt) / (2 * np.pi), "C0", lw=2,
         label=r"$\Omega_x$ (Gaussian, area $\pi$)")
axe.plot(tt * 1e3, -denvx(tt) / alpha7 / (2 * np.pi), "C3", lw=2,
         label=r"$\Omega_y = -\dot\Omega_x/\alpha$ (DRAG)")
axe.set_xlabel("time (ns)")
axe.set_ylabel("drive amplitude / $2\\pi$ (MHz)")
axe.set_title(r"DRAG envelopes ($t_g=10$ ns, $\alpha/2\pi=-250$ MHz)")
axe.legend(fontsize=9)
axe.grid(True, alpha=0.3)
for beta, color, lbl in [(0.0, "C3", "Gaussian only"), (1.0, "C0", "Gaussian + DRAG")]:
    ts, P2 = run3(beta)
    axp.semilogy(ts * 1e3, np.maximum(P2, 1e-12), color, lw=2, label=lbl)
axp.set_xlabel("time (ns)")
axp.set_ylabel("leakage population $P_2$")
axp.set_title("Leakage during the pulse (3-level simulation)")
axp.legend(fontsize=9)
axp.grid(True, alpha=0.3, which="both")
save(fig, "07-drag.png")

# ===========================================================================
# 08-cz-crossing: {|11>, |02>} avoided crossing vs dwell detuning
# ===========================================================================
g8 = 12.0                                   # MHz
coup = np.sqrt(2) * g8
dlt = np.linspace(-150, 150, 600)
Eup = dlt / 2 + np.sqrt((dlt / 2) ** 2 + coup**2)
Edn = dlt / 2 - np.sqrt((dlt / 2) ** 2 + coup**2)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(dlt, dlt, "k--", lw=1, alpha=0.5)
ax.axhline(0, color="k", ls=":", lw=1, alpha=0.5)
ax.text(-145, 8, r"bare $|02\rangle$", fontsize=9)
ax.text(-145, -125, r"bare $|11\rangle$", fontsize=9)
ax.plot(dlt, Eup, "C0", lw=2)
ax.plot(dlt, Edn, "C0", lw=2, label="hybridized branches")
ax.annotate("", xy=(0, coup), xytext=(0, -coup),
            arrowprops=dict(arrowstyle="<->", color="C3"))
ax.text(4, 20, r"$2\sqrt{2}\,g/2\pi \approx 34$ MHz", color="C3", fontsize=9)
k50 = int(np.argmin(np.abs(dlt - 50)))
ax.plot([50], [Eup[k50]], "ko", ms=7)
ax.annotate("worked-example dwell\n($\\delta/2\\pi = 50$ MHz)", xy=(50, Eup[k50]),
            xytext=(58, 130), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.plot(dlt, np.full_like(dlt, -170), "0.6", lw=1.2)
ax.plot(dlt, np.full_like(dlt, -190), "0.6", lw=1.2)
ax.text(-145, -163, r"$|01\rangle,|10\rangle$ references: flat, unaffected (not to scale)",
        fontsize=8, color="0.4")
ax.set_xlabel(r"detuning of $|11\rangle$ from $|02\rangle$, $\delta/2\pi$ (MHz)")
ax.set_ylabel(r"energy / h (MHz, relative to bare $|02\rangle$)")
ax.set_title(r"The CZ avoided crossing ($g/2\pi = 12$ MHz)")
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "08-cz-crossing.png")

# ===========================================================================
# 08-zz-vs-detuning: residual ZZ, poles at the crossings
# ===========================================================================
a8 = -300.0
Dzz = np.linspace(-600, 600, 4000)
zz = 2 * g8**2 * (a8 + a8) / ((Dzz - a8) * (Dzz + a8))
zz[np.abs(Dzz - a8) < 12] = np.nan
zz[np.abs(Dzz + a8) < 12] = np.nan
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(Dzz, zz, "C0", lw=2)
ax.set_yscale("symlog", linthresh=0.1)
for pole, lbl in [(a8, r"$\Delta=\alpha_2$: $|11\rangle$-$|02\rangle$ crossing"
                       "\n(the CZ operating point)"),
                  (-a8, r"$\Delta=-\alpha_1$: $|11\rangle$-$|20\rangle$ crossing")]:
    ax.axvline(pole, color="C3", ls="--", lw=1.2, alpha=0.8)
ax.text(0.06, 0.80, r"$\Delta=\alpha_2$:" "\n" r"$|11\rangle$-$|02\rangle$ crossing"
        "\n(CZ operating point)", fontsize=8, color="C3", transform=ax.transAxes)
ax.text(0.78, 0.80, r"$\Delta=-\alpha_1$:" "\n" r"$|11\rangle$-$|20\rangle$" "\ncrossing",
        fontsize=8, color="C3", transform=ax.transAxes)
ax.annotate("idle here: small always-on\nZZ error", xy=(0, zz[2000]),
            xytext=(-200, -30), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"qubit-qubit detuning $\Delta/2\pi$ (MHz)")
ax.set_ylabel(r"$\zeta_{ZZ}/2\pi$ (MHz, symlog)")
ax.set_title(r"Residual ZZ: idle error and CZ resource are one curve "
             r"($g/2\pi=12$ MHz, $\alpha/2\pi=-300$ MHz)")
ax.grid(True, alpha=0.3)
save(fig, "08-zz-vs-detuning.png")

# ===========================================================================
# 09-decays: T1 exponential, Ramsey Gaussian fringe, echo envelope
# ===========================================================================
t9 = np.linspace(0, 150, 3000)              # us
T1_, T2s, T2e = 100.0, 11.25, 45.0
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t9, np.exp(-t9 / T1_), "C2", lw=2, label=r"$T_1$: $e^{-t/100\,\mu s}$ (exponential)")
ram = np.exp(-(t9 / T2s) ** 2) * np.cos(2 * np.pi * 0.2 * t9)
ax.plot(t9, ram, "C0", lw=1, label=r"Ramsey: $T_2^*\approx11\,\mu$s (Gaussian envelope)")
ax.plot(t9, np.exp(-(t9 / T2s) ** 2), "C0", ls="--", lw=1, alpha=0.6)
ax.plot(t9, np.exp(-(t9 / T2e) ** 2), "C3", lw=2,
        label=r"echo envelope: $T_2^E\approx45\,\mu$s")
ax.set_xlabel(r"delay $t$ ($\mu$s)")
ax.set_ylabel(r"signal ($P_1$ or $\langle\sigma_x\rangle$)")
ax.set_title("The three clocks (worked-example numbers): note the shapes, not just the rates")
ax.set_ylim(-1.05, 1.05)
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "09-decays.png")

# ===========================================================================
# 09-filter-functions: 1/f noise vs Ramsey / echo filters
# ===========================================================================
ft = np.logspace(-2, 1, 800)                # dimensionless f*t
WR = np.sinc(ft) ** 2                       # numpy sinc(x) = sin(pi x)/(pi x)
WE = np.sin(np.pi * ft / 2) ** 4 / (np.pi * ft / 2) ** 2
S = 0.03 / ft
fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(ft, S, "0.4", lw=2, label=r"noise $S(f)\propto 1/f$")
ax.loglog(ft, WR, "C1", lw=2, label=r"Ramsey filter $W_R$")
ax.loglog(ft, WE, "C0", lw=2, label=r"echo filter $W_E$ (zero at $f=0$)")
ax.fill_between(ft, 1e-6, np.minimum(S, WR), color="C1", alpha=0.25,
                label=r"overlap $S\cdot W_R$ = dephasing")
ax.annotate("echo notch:\nslow noise refocused", xy=(0.012, WE[8]),
            xytext=(0.03, 3e-5), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"dimensionless frequency $f\,t$")
ax.set_ylabel("normalized magnitude")
ax.set_title("Where the rain falls vs where the bucket sits")
ax.set_ylim(1e-6, 20)
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.3, which="both")
save(fig, "09-filter-functions.png")

# ===========================================================================
# 10-thermal-photons: nbar(5 GHz) vs T with fridge stages
# ===========================================================================
T10 = np.logspace(np.log10(0.008), np.log10(300), 500)
fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(T10, nbar(5e9, T10), "C0", lw=2, label=r"$\bar n$(5 GHz, $T$)")
ax.loglog(T10, kB * T10 / (h * 5e9), "k--", lw=1, alpha=0.6,
          label=r"Rayleigh-Jeans $k_BT/\hbar\omega$")
stages = [(300, "300 K"), (50, "50 K"), (4, "4 K"), (0.8, "still"),
          (0.1, "cold plate"), (0.010, "MXC 10 mK")]
for Ts, lbl in stages:
    ax.plot([Ts], [nbar(5e9, Ts)], "C3o", ms=6)
    ax.annotate(lbl, xy=(Ts, nbar(5e9, Ts)), xytext=(Ts * 1.4, nbar(5e9, Ts) * 3),
                fontsize=8)
ax.axvline(0.24, color="0.5", ls=":", lw=1)
ax.text(0.26, 1e-8, "crossover\n240 mK", fontsize=8, color="0.4")
ax.set_xlabel("temperature (K)")
ax.set_ylabel(r"mean photon number $\bar n$")
ax.set_title("The one curve the whole chain serves")
ax.set_ylim(1e-12, 1e4)
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3, which="both")
save(fig, "10-thermal-photons.png")

# ===========================================================================
# 10-attenuation-cascade: staircase through the input chain (7 GHz)
# ===========================================================================
f7 = 7e9
def cascade(atts_db, temps):
    n = nbar(f7, 300.0)
    out = [n]
    for db, T_ in zip(atts_db, temps):
        A = 10 ** (db / 10)
        n = n / A + (1 - 1 / A) * nbar(f7, T_)
        out.append(n)
    return out

temps10 = [4.0, 0.1, 0.010]
labels10 = ["input\n(300 K)", "after ATT\n@ 4 K", "after ATT\n@ 100 mK",
            "after ATT\n@ 10 mK"]
fig, ax = plt.subplots(figsize=(8, 5))
xpos = np.arange(4)
for atts, color, lbl in [([20, 10, 20], "C0", "20 / 10 / 20 dB"),
                         ([20, 20, 20], "C1", "20 / 20 / 20 dB")]:
    vals = cascade(atts, temps10)
    ax.semilogy(xpos, vals, "o-", color=color, lw=2, ms=6,
                label=f"{lbl}: floor $\\bar n$ = {vals[-1]:.2g}", drawstyle="steps-post")
for T_, lbl in [(4.0, r"$\bar n$(4 K)"), (0.1, r"$\bar n$(100 mK)")]:
    ax.axhline(nbar(f7, T_), color="0.6", ls=":", lw=1)
    ax.text(2.75, nbar(f7, T_) * 1.4, lbl, fontsize=8, color="0.4")
ax.set_xticks(xpos)
ax.set_xticklabels(labels10, fontsize=9)
ax.set_ylabel(r"$\bar n$ referred forward (7 GHz)")
ax.set_title("Each attenuator resets the line toward its own temperature")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which="both")
save(fig, "10-attenuation-cascade.png")

# ===========================================================================
# 11-rb-decay: same p different SPAM, plus interleaved
# ===========================================================================
m11 = np.linspace(0, 2000, 500)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(m11, 0.49 * 0.999**m11 + 0.50, "C0", lw=2,
        label=r"reference: $A=0.49$, $B=0.50$, $p=0.9990$")
ax.plot(m11, 0.35 * 0.999**m11 + 0.55, "C0--", lw=2,
        label=r"worse SPAM: $A=0.35$, $B=0.55$, same $p=0.9990$")
ax.plot(m11, 0.49 * 0.9982**m11 + 0.50, "C3:", lw=2.5,
        label=r"interleaved: $p=0.9982$ (faster decay = gate error)")
ax.set_xlabel("sequence length m (number of Cliffords)")
ax.set_ylabel("ground-state survival F(m)")
ax.set_title("SPAM moves A and B; only gate error changes the decay rate p")
ax.set_ylim(0.45, 1.02)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "11-rb-decay.png")

# ===========================================================================
# 11-ramsey-fringe: detuning + T2* in one trace
# ===========================================================================
tau = np.linspace(0, 30, 2000)              # us
T2s11, df11 = 10.0, 0.25                    # us, MHz
P = 0.5 * (1 + np.exp(-tau / T2s11) * np.cos(2 * np.pi * df11 * tau))
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(tau, P, "C0", lw=1.2)
ax.plot(tau, 0.5 * (1 + np.exp(-tau / T2s11)), "C3--", lw=1.5,
        label=r"envelope $\to T_2^*$")
ax.plot(tau, 0.5 * (1 - np.exp(-tau / T2s11)), "C3--", lw=1.5)
ax.annotate(r"fringe period $1/\Delta f = 4\,\mu$s $\to$ detuning",
            xy=(4, 0.97), xytext=(7, 1.03), fontsize=9,
            arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.set_xlabel(r"Ramsey delay $\tau$ ($\mu$s)")
ax.set_ylabel(r"$P(|0\rangle)$")
ax.set_title(r"Ramsey fringe: $\Delta f = 250$ kHz, $T_2^* = 10\,\mu$s")
ax.set_ylim(-0.05, 1.12)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "11-ramsey-fringe.png")

# ===========================================================================
# 12-repetition-breakeven: 3p^2 - 2p^3 vs p
# ===========================================================================
p12 = np.linspace(0, 1, 500)
PL = 3 * p12**2 - 2 * p12**3
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(p12, p12, "0.5", ls="--", lw=1.5, label="unencoded error $p$")
ax.plot(p12, PL, "C0", lw=2, label=r"3-qubit code: $3p^2 - 2p^3$")
ax.plot([0.5], [0.5], "ko", ms=7)
ax.annotate("break-even $p = 1/2$", xy=(0.5, 0.5), xytext=(0.25, 0.6),
            fontsize=9, arrowprops=dict(arrowstyle="->", alpha=0.7))
ax.fill_between(p12, PL, p12, where=PL < p12, color="C2", alpha=0.15)
ax.text(0.16, 0.28, "encoding wins", color="C2", fontsize=10)
ax.fill_between(p12, p12, PL, where=PL > p12, color="C3", alpha=0.15)
ax.text(0.62, 0.85, "encoding hurts", color="C3", fontsize=10)
axin = ax.inset_axes([0.55, 0.08, 0.4, 0.4])
pp = np.logspace(-3, -0.5, 100)
axin.loglog(pp, pp, "0.5", ls="--", lw=1)
axin.loglog(pp, 3 * pp**2 - 2 * pp**3, "C0", lw=1.5)
axin.set_title("log-log: slope 2", fontsize=8)
axin.tick_params(labelsize=7)
axin.grid(True, alpha=0.3, which="both")
ax.set_xlabel("physical bit-flip probability $p$")
ax.set_ylabel("failure probability after correction")
ax.set_title("When does the repetition code help?")
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, alpha=0.3)
save(fig, "12-repetition-breakeven.png")

# ===========================================================================
# 12-threshold: p_L vs p for d = 3..9, threshold at 1%
# ===========================================================================
pth = 0.01
pphys = np.logspace(-4, np.log10(pth), 400)
fig, ax = plt.subplots(figsize=(8, 5))
for d, color in [(3, "C0"), (5, "C2"), (7, "C1"), (9, "C3")]:
    ax.loglog(pphys, (pphys / pth) ** ((d + 1) // 2), color, lw=2, label=f"$d={d}$")
ax.axvline(pth, color="k", ls="--", lw=1.2)
ax.text(0.0105, 3e-8, r"threshold $p_{\rm th}=1\%$", rotation=90, fontsize=9)
ax.axvline(0.001, color="0.5", ls=":", lw=1.2)
ax.text(0.00105, 3e-8, "worked example $p=0.1\\%$", rotation=90, fontsize=8,
        color="0.4")
ax.text(2.2e-4, 2e-4, "below threshold:\nbigger code wins", fontsize=9)
ax.text(0.012, 3e-2, "scaling model\nnot valid\nabove threshold", fontsize=9)
ax.axvspan(pth, .03, color="0.9")
ax.set_xlabel("physical error rate $p$")
ax.set_ylabel("logical error rate $p_L$")
ax.set_title(r"The threshold picture: $p_L = (p/p_{\rm th})^{(d+1)/2}$")
ax.set_ylim(1e-10, 1.2)
ax.set_xlim(1e-4, .03)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3, which="both")
save(fig, "12-threshold.png")

print("all figures generated")
