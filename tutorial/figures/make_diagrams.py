"""
Generate the schematic diagrams embedded in the tutorial chapters.

make_figures.py draws *data* (curves computed from the physics); this script
draws *pictures*: circuits, level ladders, Bloch spheres, pulse sequences,
wiring and code layouts. Every diagram is original. Where a diagram contains
numbers (level energies, trajectories, populations) they are computed here
from the same illustrative parameters as the chapter text.

Run from any directory:

    python tutorial/figures/make_diagrams.py            # all diagrams
    python tutorial/figures/make_diagrams.py 05 10      # only these chapters

Requires numpy, matplotlib and schemdraw (circuit symbols).
"""

import logging
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.lines import Line2D

try:
    import schemdraw
    import schemdraw.elements as elm
except ImportError:  # pragma: no cover - friendly message for learners
    sys.exit("make_diagrams.py needs schemdraw: python -m pip install schemdraw")

HERE = Path(__file__).resolve().parent
# Fixed limits plus equal aspect make matplotlib log a harmless notice per panel.
logging.getLogger("matplotlib").setLevel(logging.ERROR)

# One palette for every diagram, matching matplotlib's default cycle used by
# make_figures.py so data plots and schematics read as one family.
BLUE, ORANGE, GREEN, RED, PURPLE = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"
INK, GREY, LIGHT = "#222222", "#7f7f7f", "#e8e8e8"
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "mathtext.fontset": "dejavusans",
    "savefig.facecolor": "white",
})

REGISTRY = []


def diagram(func):
    """Register a diagram-drawing function; its name starts with the chapter."""
    REGISTRY.append(func)
    return func


def save(fig, name):
    fig.savefig(HERE / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


def blank(ax, xlim=None, ylim=None):
    """Hide axes; keep the axes box fixed so panel titles line up."""
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")


def title(ax, letter, text, **kw):
    ax.set_title(f"({letter})  {text}", loc="left", **kw)


def schematic(ax, unit=2.0, fontsize=12):
    """A schemdraw Drawing that renders onto an existing matplotlib axis."""
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(unit=unit, fontsize=fontsize, lw=1.6)
    return d


def part(d, element, start, end, label=None, loc=None, ofst=None, color=None, **lkw):
    """Place a two-terminal schemdraw element between two explicit points."""
    e = element.endpoints(start, end)
    if label is not None:
        e = e.label(label, loc=loc, ofst=ofst, **lkw)
    if color is not None:
        e = e.color(color)
    d.add(e)
    return e


def wire(d, *pts, color=INK):
    for a, b in zip(pts, pts[1:]):
        d.add(elm.Line().endpoints(a, b).color(color))


def dot(d, p, color=INK):
    d.add(elm.Dot(radius=0.09).at(p).color(color))


def transmon_levels(ec, ej, ng=0.0, nlev=5, cutoff=40):
    """Exact charge-basis levels of 4EC(n-ng)^2 - EJ cos(phi), same units as EC."""
    n = np.arange(-cutoff, cutoff + 1)
    ham = (np.diag(4 * ec * (n - ng) ** 2)
           - 0.5 * ej * (np.eye(2 * cutoff + 1, k=1) + np.eye(2 * cutoff + 1, k=-1)))
    return np.linalg.eigvalsh(ham)[:nlev]


def ladder(ax, energies, potential, grid, label_dx=0.12, fs=11, **kw):
    """Draw levels between their classical turning points, labelled |n> on the left."""
    for n, en in enumerate(energies):
        inside = grid[potential(grid) <= en]
        ax.hlines(en, inside.min(), inside.max(), color=INK, lw=2, **kw)
        ax.text(inside.min() - label_dx, en, rf"$|{n}\rangle$", va="center",
                ha="right", fontsize=fs)


def varrow(ax, x, y0, y1, color=INK, text=None, fs=10, lw=1.5, dx=0.1, ha="left"):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw,
                                shrinkA=0, shrinkB=0))
    if text:
        ax.text(x + (dx if ha == "left" else -dx), (y0 + y1) / 2, text, color=color,
                fontsize=fs, va="center", ha=ha,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.0))


# ===========================================================================
# Chapter 01: harmonic versus anharmonic ladder
# ===========================================================================
@diagram
def ch01_energy_ladders():
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(11.5, 5.2))

    # (a) Harmonic oscillator in units of hbar*omega (x = Phi / Phi_zpf).
    x = np.linspace(-4.3, 4.3, 900)
    pot = lambda q: 0.25 * q ** 2
    axl.plot(x, pot(x), color=BLUE, lw=2.2)
    energies = [n + 0.5 for n in range(4)]
    ladder(axl, energies, pot, x)
    for n in range(3):
        varrow(axl, 0.9, energies[n] + 0.05, energies[n + 1] - 0.05, RED,
               r"$\hbar\omega$", fs=11)
    axl.text(0, 3.95, "a drive at $\\omega$ is resonant with every rung:\n"
             "population climbs the whole ladder", ha="center", fontsize=10, color=RED)
    axl.set(xlim=(-4.6, 4.6), ylim=(0, 4.6), xlabel=r"flux $\Phi$",
            ylabel=r"energy / $\hbar\omega$")
    axl.set_xticks([]), axl.set_yticks([])
    title(axl, "a", "LC oscillator: parabola, equal spacing ($\\alpha=0$)")

    # (b) Josephson cosine well, exact levels for EJ/EC = 20 (alpha exaggerated).
    ec, ej = 1.0, 20.0
    lev = transmon_levels(ec, ej, nlev=4)
    e01 = lev[1] - lev[0]
    phi = np.linspace(-np.pi, np.pi, 1200)
    cos_pot = lambda p: (-ej * np.cos(p) - lev[0]) / e01 + 0.5
    lev_n = (lev - lev[0]) / e01 + 0.5
    near = np.abs(phi) < 1.25
    axr.plot(phi, cos_pot(phi), color=BLUE, lw=2.2, label=r"$-E_J\cos\varphi$")
    axr.plot(phi[near], (-ej + 0.5 * ej * phi[near] ** 2 - lev[0]) / e01 + 0.5, "--",
             color=GREY, lw=1.3, label="parabola (harmonic part)")
    ladder(axr, lev_n, cos_pot, phi)
    labels = [r"$\hbar\omega_{01}$", r"$\hbar(\omega_{01}+\alpha)$",
              r"$\hbar(\omega_{01}+2\alpha)$"]
    for n, (lab, col) in enumerate(zip(labels, [GREEN, GREY, GREY])):
        varrow(axr, 0.25, lev_n[n] + 0.05, lev_n[n + 1] - 0.05, col, lab, fs=10.5)
    axr.text(0, 3.95, "each rung is $|\\alpha|$ narrower: a drive at $\\omega_{01}$\n"
             "misses $1\\to2$, leaving an addressable qubit", ha="center",
             fontsize=10, color=GREEN)
    axr.set(xlim=(-np.pi, np.pi), ylim=(0, 4.6), xlabel=r"phase $\varphi$",
            ylabel=r"energy / $\hbar\omega_{01}$")
    axr.set_xticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    axr.set_yticks([])
    axr.legend(loc="lower left", fontsize=9, frameon=False)
    title(axr, "b", "Josephson well: cosine, shrinking spacing ($\\alpha<0$)")
    fig.text(0.5, -0.01, "Panel (b) is an exact charge-basis diagonalization at $E_J/E_C=20$, "
             "chosen to make $\\alpha$ visible; transmons typically use $E_J/E_C\\approx50$-100.",
             ha="center", fontsize=9, color=GREY)
    fig.tight_layout()
    save(fig, "01-energy-ladders.png")


# ===========================================================================
# Chapter 02: LC circuit and its mechanical twin
# ===========================================================================
@diagram
def ch02_lc_circuit():
    fig, (axc, axm) = plt.subplots(1, 2, figsize=(11.5, 4.3),
                                   gridspec_kw={"width_ratios": [0.9, 1.4]})
    d = schematic(axc)
    part(d, elm.Capacitor(), (0, 0), (0, 2.6), "$C$", loc="bottom", ofst=0.3)
    part(d, elm.Inductor2(loops=4), (2.6, 2.6), (2.6, 0), "$L$", loc="top", ofst=0.3)
    wire(d, (0, 2.6), (2.6, 2.6))
    wire(d, (0, 0), (2.6, 0))
    dot(d, (1.3, 2.6))
    dot(d, (1.3, 0))
    d.add(elm.Ground().at((1.3, 0)))
    d.draw()
    axc.text(1.3, 2.85, r"node flux $\Phi(t)=\int V\,dt$", ha="center", color=BLUE, fontsize=11)
    axc.text(-0.3, 1.62, "$+Q$", ha="right", fontsize=11, color=RED)
    axc.text(-0.3, 0.92, "$-Q$", ha="right", fontsize=11, color=RED)
    axc.annotate("", xy=(3.4, 0.9), xytext=(3.4, 1.7),
                 arrowprops=dict(arrowstyle="->", color=INK, lw=1.3))
    axc.text(3.5, 1.3, "$I$", fontsize=11, va="center")
    axc.text(1.3, -1.25, r"$V=\dot\Phi,\quad Q=C\dot\Phi$", ha="center", fontsize=11)
    blank(axc, (-1.2, 4.0), (-1.6, 3.9))
    title(axc, "a", "LC circuit: one node, one degree of freedom")

    # (b) Mass on a spring, drawn by hand, plus the dictionary.
    axm.plot([0, 0], [-0.6, 0.9], color=INK, lw=3)
    for yy in np.linspace(-0.55, 0.85, 8):
        axm.plot([-0.18, 0], [yy - 0.12, yy], color=INK, lw=1)
    xs = np.linspace(0, 2.4, 400)
    axm.plot(xs, 0.16 * np.sin(2 * np.pi * 7 * (xs - 0.15) / 2.1) * (xs > 0.15) * (xs < 2.25),
             color=INK, lw=1.6)
    axm.add_patch(patches.FancyBboxPatch((2.4, -0.42), 1.0, 0.84,
                                         boxstyle="round,pad=0.02", fc=LIGHT, ec=INK, lw=1.6))
    axm.text(2.9, 0, "$m$", ha="center", va="center", fontsize=14)
    axm.text(1.2, 0.33, "$k$", ha="center", fontsize=13)
    axm.plot([0, 4.0], [-0.6, -0.6], color=INK, lw=1.2)
    axm.annotate("", xy=(3.6, -0.8), xytext=(2.9, -0.8),
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.6))
    axm.text(3.68, -0.8, "$x$", color=BLUE, va="center", fontsize=13)
    rows = [("position $x$", "flux $\\Phi$"), ("momentum $p$", "charge $Q$"),
            ("mass $m$", "capacitance $C$"), ("stiffness $k$", "inverse inductance $1/L$"),
            ("$\\omega=\\sqrt{k/m}$", "$\\omega=1/\\sqrt{LC}$"),
            ("$[\\hat x,\\hat p]=i\\hbar$", "$[\\hat\\Phi,\\hat Q]=i\\hbar$")]
    for i, (mech, circ) in enumerate(rows):
        yy = 0.95 - 0.33 * i
        axm.text(4.4, yy, mech, fontsize=10.5, va="center")
        axm.text(6.35, yy, "$\\leftrightarrow$", fontsize=11, va="center", ha="center")
        axm.text(6.65, yy, circ, fontsize=10.5, va="center", color=BLUE)
    blank(axm, (-0.4, 9.3), (-1.0, 1.25))
    title(axm, "b", "Mechanical twin: same Lagrangian, same quantization")
    fig.tight_layout()
    save(fig, "02-lc-circuit.png")


# ===========================================================================
# Chapter 03: the junction, its symbol, and the tilted washboard
# ===========================================================================
@diagram
def ch03_josephson_junction():
    fig = plt.figure(figsize=(13.5, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 0.85, 1.3])
    ax_sis, ax_sym, ax_wash = (fig.add_subplot(gs[i]) for i in range(3))

    # (a) Superconductor-insulator-superconductor sandwich.
    for x0 in (0.0, 2.15):
        ax_sis.add_patch(patches.Rectangle((x0, 0), 2.0, 1.4, fc="#cfe2f3", ec=INK, lw=1.4))
    ax_sis.add_patch(patches.Rectangle((2.0, 0), 0.15, 1.4, fc="#999999", ec=INK, lw=1.0))
    ax_sis.text(1.0, 1.0, "Al", ha="center", fontsize=12)
    ax_sis.text(3.15, 1.0, "Al", ha="center", fontsize=12)
    ax_sis.text(1.0, 0.55, r"$\psi_L=\sqrt{n_s}\,e^{i\theta_L}$", ha="center", fontsize=11)
    ax_sis.text(3.15, 0.55, r"$\psi_R=\sqrt{n_s}\,e^{i\theta_R}$", ha="center", fontsize=11)
    ax_sis.annotate("AlO$_x$ tunnel barrier (~1 nm)", xy=(2.075, 1.4), xytext=(2.075, 1.95),
                    ha="center", fontsize=10,
                    arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    for dx in (-0.07, 0.07):
        ax_sis.add_patch(patches.Circle((1.55 + dx, 0.2), 0.055, color=RED))
    ax_sis.annotate("", xy=(2.8, 0.2), xytext=(1.72, 0.2),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))
    ax_sis.text(2.075, -0.3, "Cooper pairs tunnel coherently", ha="center",
                fontsize=10, color=RED)
    ax_sis.text(2.075, -0.75, r"$\varphi=\theta_L-\theta_R$ in a gauge with $A\approx0$",
                ha="center", fontsize=10)
    blank(ax_sis, (-0.2, 4.35), (-1.0, 2.3))
    title(ax_sis, "a", "Two condensates, one phase difference")

    # (b) Circuit symbol and its small-signal equivalent.
    d = schematic(ax_sym)
    part(d, elm.Josephson(), (0, 0), (0, 2.4), "$E_J,\\ I_c$", loc="top", ofst=0.25)
    wire(d, (2.7, 0), (2.7, 0.5), (2.2, 0.5))
    wire(d, (2.7, 0.5), (3.2, 0.5))
    wire(d, (2.7, 2.4), (2.7, 1.9), (2.2, 1.9))
    wire(d, (2.7, 1.9), (3.2, 1.9))
    part(d, elm.Capacitor(), (2.2, 0.5), (2.2, 1.9), "$C_J$", loc="top", ofst=0.2)
    part(d, elm.Inductor2(loops=3), (3.2, 0.5), (3.2, 1.9), "$L_J(\\varphi)$", loc="bottom", ofst=0.2)
    d.draw()
    ax_sym.text(1.05, 1.2, "$\\simeq$", fontsize=20, ha="center", va="center")
    ax_sym.text(0.0, -0.55, "junction symbol", ha="center", fontsize=10)
    ax_sym.text(2.7, -0.55, "small-signal model", ha="center", fontsize=10)
    ax_sym.text(1.35, -1.15, r"$L_J(\varphi)=\dfrac{\Phi_0}{2\pi I_c\cos\varphi}$",
                ha="center", fontsize=11)
    blank(ax_sym, (-1.3, 4.3), (-1.6, 2.8))
    title(ax_sym, "b", "Symbol and equivalent")

    # (c) Tilted washboard U = -EJ cos(phi) - (hbar I / 2e) phi.
    phi = np.linspace(-1.5 * np.pi, 4.6 * np.pi, 1200)
    for tilt, color, lab in [(0.0, BLUE, "$I=0$"), (0.6, ORANGE, "$I=0.6\\,I_c$")]:
        ax_wash.plot(phi, -np.cos(phi) - tilt * phi, color=color, lw=2, label=lab)
    ax_wash.plot([0], [-1], "o", color=INK, ms=9, zorder=5)
    ax_wash.annotate("qubit: lowest swings\nof the untilted well", xy=(-0.15, -1.15),
                     xytext=(-4.65, -4.3), fontsize=9.5,
                     arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    p0 = np.arcsin(0.6) + 2 * np.pi
    ax_wash.plot([p0], [-np.cos(p0) - 0.6 * p0], "o", color=ORANGE, ms=8, zorder=5)
    ax_wash.annotate("as $I\\to I_c$ the phase runs:\n"
                     "$V=(\\hbar/2e)\\langle\\dot\\varphi\\rangle\\neq0$",
                     xy=(3.45 * np.pi, -0.6 * 3.45 * np.pi + 0.1), xytext=(1.75 * np.pi, -2.75),
                     fontsize=9.5, color=ORANGE,
                     arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    ax_wash.set(xlabel=r"phase $\varphi$", ylabel=r"$U/E_J$", ylim=(-9.5, 2.4))
    ax_wash.set_xticks(np.arange(-1, 5) * np.pi,
                       [r"$-\pi$", "0", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"])
    ax_wash.legend(loc="lower left", fontsize=9.5, frameon=False)
    ax_wash.grid(alpha=0.25)
    title(ax_wash, "c", "The tilted washboard")
    fig.tight_layout()
    save(fig, "03-josephson-junction.png")


# ===========================================================================
# Chapter 04: from Cooper-pair box to tunable transmon; the exact ladder
# ===========================================================================
def flux_symbol(ax, x, y, label=r"$\Phi_{\rm ext}$"):
    ax.add_patch(patches.Circle((x, y), 0.2, fc="white", ec=PURPLE, lw=1.5, zorder=5))
    for s in (1, -1):
        ax.plot([x - 0.13, x + 0.13], [y - s * 0.13, y + s * 0.13], color=PURPLE, lw=1.5, zorder=6)
    ax.text(x, y - 0.5, label, color=PURPLE, ha="center", fontsize=11)


@diagram
def ch04_transmon_circuits():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))

    # (a) Cooper-pair box: a voltage-biased island.
    d = schematic(axes[0])
    part(d, elm.SourceV(), (0, 0), (0, 2.4), "$V_g$", loc="bottom", ofst=0.25)
    wire(d, (0, 2.4), (0.4, 2.4))
    part(d, elm.Capacitor(), (0.4, 2.4), (1.8, 2.4), "$C_g$", loc="top", ofst=0.15)
    wire(d, (1.8, 2.4), (3.2, 2.4))
    part(d, elm.Josephson(), (3.2, 2.4), (3.2, 0), "$E_J$", loc="bottom", ofst=0.25)
    wire(d, (3.2, 0), (0, 0))
    dot(d, (2.5, 2.4), BLUE)
    d.draw()
    axes[0].text(2.5, 2.75, "island", ha="center", color=BLUE, fontsize=11)
    axes[0].text(1.6, -0.75, r"$n_g=C_gV_g/2e$", ha="center", fontsize=11)
    blank(axes[0], (-1.2, 4.4), (-1.3, 3.4))
    title(axes[0], "a", "Cooper-pair box, $E_J/E_C\\sim1$")

    # (b) Transmon: the same circuit plus a large shunt capacitor.
    d = schematic(axes[1])
    part(d, elm.SourceV(), (0, 0), (0, 2.4), "$V_g$", loc="bottom", ofst=0.25)
    wire(d, (0, 2.4), (0.4, 2.4))
    part(d, elm.Capacitor(), (0.4, 2.4), (1.8, 2.4), "$C_g$", loc="top", ofst=0.15)
    wire(d, (1.8, 2.4), (4.4, 2.4))
    part(d, elm.Josephson(), (2.9, 2.4), (2.9, 0), "$E_J$", loc="bottom", ofst=0.25)
    part(d, elm.Capacitor(), (4.4, 2.4), (4.4, 0), "$C_B$", loc="bottom", ofst=0.25, color=BLUE)
    wire(d, (4.4, 0), (0, 0))
    for p in [(2.9, 2.4), (2.9, 0)]:
        dot(d, p)
    d.draw()
    axes[1].text(2.2, -0.75, r"$E_C=\dfrac{e^2}{2C_\Sigma}$,  $C_\Sigma=C_J+C_B+C_g$",
                 ha="center", fontsize=11)
    blank(axes[1], (-1.2, 5.6), (-1.3, 3.4))
    title(axes[1], "b", "Transmon: large $C_B$ gives $E_J/E_C\\gg1$")

    # (c) Flux-tunable transmon: a dc SQUID replaces the single junction.
    d = schematic(axes[2])
    wire(d, (0.0, 2.0), (1.4, 2.0))
    wire(d, (0.0, 0.6), (1.4, 0.6))
    part(d, elm.Josephson(), (0.0, 2.0), (0.0, 0.6), "$E_{J1}$", loc="top", ofst=0.2)
    part(d, elm.Josephson(), (1.4, 2.0), (1.4, 0.6), "$E_{J2}$", loc="bottom", ofst=0.2)
    wire(d, (0.7, 2.0), (0.7, 2.6), (3.2, 2.6))
    wire(d, (0.7, 0.6), (0.7, 0.0), (3.2, 0.0))
    part(d, elm.Capacitor(), (3.2, 2.6), (3.2, 0.0), "$C_B$", loc="bottom", ofst=0.25, color=BLUE)
    for p in [(0.7, 2.0), (0.7, 0.6)]:
        dot(d, p)
    d.draw()
    flux_symbol(axes[2], 0.7, 1.45)
    axes[2].text(1.6, -0.75, r"$E_{J,\rm eff}(\Phi_{\rm ext})$ tunes $f_{01}$",
                 ha="center", fontsize=11)
    blank(axes[2], (-1.3, 4.4), (-1.3, 3.4))
    title(axes[2], "c", "Tunable transmon: a dc-SQUID loop")
    fig.tight_layout()
    save(fig, "04-transmon-circuits.png")


@diagram
def ch04_transmon_levels():
    ec, ej = 0.25, 15.0                      # GHz, the chapter's worked example
    lev = transmon_levels(ec, ej, nlev=4)
    phi = np.linspace(-np.pi, np.pi, 1500)
    pot = lambda p: -ej * np.cos(p)
    fig, ax = plt.subplots(figsize=(9, 5.8))
    ax.plot(phi, pot(phi), color=BLUE, lw=2.2, label=r"$-E_J\cos\varphi$")
    near = np.abs(phi) < 1.75
    ax.plot(phi[near], -ej + 0.5 * ej * phi[near] ** 2, "--", color=GREY, lw=1.2,
            label=r"harmonic part $-E_J+\frac{1}{2}E_J\varphi^2$")
    ladder(ax, lev, pot, phi)
    trans = np.diff(lev)
    quartic = [np.sqrt(8 * ej * ec) - ec * (m + 1) for m in range(3)]
    for m in range(3):
        varrow(ax, 0.15, lev[m] + 0.12, lev[m + 1] - 0.12, GREEN if m == 0 else INK,
               rf"$f_{{{m}{m + 1}}}={trans[m]:.3f}$ GHz  (quartic: {quartic[m]:.3f})",
               fs=9.5, dx=0.08)
    alpha = (trans[1] - trans[0]) * 1e3
    ax.text(0.0, 6.6, rf"exact $\alpha/2\pi={alpha:.0f}$ MHz"
            "\n" r"(leading order $-E_C/h=-250$ MHz)", ha="center", fontsize=10.5, color=RED)
    ax.annotate(r"barrier top: $2E_J/h=30$ GHz above the minimum", xy=(np.pi - 0.05, 14.9),
                xytext=(1.05, 12.2), fontsize=9.5, ha="center",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
    ax.set(xlim=(-np.pi, np.pi), ylim=(-16, 16), xlabel=r"phase $\varphi$",
           ylabel=r"energy $/h$ (GHz)")
    ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
                  [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.grid(alpha=0.2)
    ax.set_title(r"Transmon ladder by exact diagonalization ($E_C/h=0.25$ GHz, $E_J/E_C=60$)")
    fig.tight_layout()
    save(fig, "04-transmon-levels.png")


# ===========================================================================
# Chapter 05: the circuit-QED circuit and the Jaynes-Cummings ladder
# ===========================================================================
@diagram
def ch05_cqed_circuit():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    d = schematic(ax)
    top, bot = 2.4, 0.0
    # Transmon: junction parallel to its capacitance.
    part(d, elm.Josephson(), (0, top), (0, bot), "$E_J$", loc="top", ofst=0.25)
    part(d, elm.Capacitor(), (1.2, top), (1.2, bot), "$C_\\Sigma$", loc="bottom", ofst=0.25)
    wire(d, (0, top), (1.2, top))
    # Coupling capacitor sets g.
    part(d, elm.Capacitor(), (1.2, top), (3.0, top), "$C_g$", loc="top", ofst=0.2, color=GREEN)
    # Readout resonator: an LC mode.
    wire(d, (3.0, top), (4.4, top))
    part(d, elm.Capacitor(), (3.2, top), (3.2, bot), "$C_r$", loc="top", ofst=0.25)
    part(d, elm.Inductor2(loops=3), (4.4, top), (4.4, bot), "$L_r$", loc="bottom", ofst=0.25)
    # Coupling to the feedline sets kappa.
    part(d, elm.Capacitor(), (4.4, top), (6.2, top), "$C_\\kappa$", loc="top", ofst=0.2, color=ORANGE)
    wire(d, (0, bot), (6.2, bot))
    for p in [(1.2, top), (1.2, bot), (3.2, top), (3.2, bot), (4.4, top), (4.4, bot)]:
        dot(d, p)
    d.add(elm.Ground().at((2.2, bot)))
    d.draw()
    # Feedline drawn as a thick transmission line with signal arrows.
    ax.plot([6.2, 6.2], [-0.2, 3.6], color=INK, lw=5, solid_capstyle="butt")
    ax.plot([6.2, 6.2], [-0.2, 3.6], color="white", lw=2, solid_capstyle="butt")
    ax.annotate("", xy=(6.75, 2.0), xytext=(6.75, 3.4),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
    ax.text(6.95, 3.0, "probe tone in\n(near $\\omega_r$)", fontsize=10, color=BLUE, va="center")
    ax.annotate("", xy=(6.75, -0.15), xytext=(6.75, 1.25),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
    ax.text(6.95, 0.55, "signal out\nto amplifiers", fontsize=10, color=BLUE, va="center")
    # Region labels.
    for x0, x1, text, sub in [(-0.6, 1.75, "transmon qubit", r"$\omega_q,\ \alpha$"),
                              (2.75, 4.95, "readout resonator", r"$\omega_r$"),
                              (5.85, 6.55, "feedline", r"50 $\Omega$")]:
        ax.add_patch(patches.FancyBboxPatch((x0, -1.2), x1 - x0, 0.75, boxstyle="round,pad=0.03",
                                            fc=LIGHT, ec="none"))
        ax.text((x0 + x1) / 2, -0.72, text, ha="center", fontsize=10.5)
        ax.text((x0 + x1) / 2, -1.05, sub, ha="center", fontsize=10.5)
    ax.text(2.1, 3.15, "coupling $g$", color=GREEN, ha="center", fontsize=11)
    ax.text(5.3, 3.15, "decay $\\kappa$", color=ORANGE, ha="center", fontsize=11)
    blank(ax, (-1.2, 8.6), (-1.4, 3.8))
    ax.set_title("Circuit QED: one capacitor sets $g$, another sets $\\kappa$")
    fig.tight_layout()
    save(fig, "05-cqed-circuit.png")


@diagram
def ch05_jc_ladder():
    g = 0.085                                  # exaggerated so splittings are visible
    fig, ax = plt.subplots(figsize=(9, 6.2))
    xb, xd = (0.0, 1.0), (2.2, 3.2)
    for n in range(4):
        e = float(n)
        if n == 0:
            ax.hlines(e, *xb, color=INK, lw=2)
            ax.hlines(e, *xd, color=INK, lw=2)
            ax.text(xb[0] - 0.1, e, r"$|g,0\rangle$", ha="right", va="center")
            ax.text(xd[1] + 0.1, e, r"$|g,0\rangle$", ha="left", va="center")
            ax.plot([xb[1], xd[0]], [e, e], ":", color=GREY, lw=1)
            continue
        ax.hlines(e, xb[0], 0.46, color=INK, lw=2)
        ax.hlines(e, 0.54, xb[1], color=INK, lw=2)
        ax.text(xb[0] - 0.1, e, rf"$|e,{n - 1}\rangle,\ |g,{n}\rangle$", ha="right", va="center")
        split = g * np.sqrt(n)
        for sgn, lab in [(1, "+"), (-1, "-")]:
            ax.hlines(e + sgn * split, *xd, color=BLUE, lw=2)
            ax.plot([xb[1], xd[0]], [e, e + sgn * split], ":", color=GREY, lw=1)
            ax.text(xd[1] + 0.1, e + sgn * split, rf"$|{n - 1},{lab}\rangle$", ha="left",
                    va="center", color=BLUE)
        ax.annotate("", xy=(3.85, e + split), xytext=(3.85, e - split),
                    arrowprops=dict(arrowstyle="<->", color=RED, lw=1.3, shrinkA=0, shrinkB=0))
        lab = {1: r"$2g$", 2: r"$2\sqrt{2}\,g$", 3: r"$2\sqrt{3}\,g$"}[n]
        ax.text(3.95, e, lab, color=RED, va="center", fontsize=11)
    # Vacuum-Rabi doublet: absorption from |g,0> to the two N=1 dressed states.
    for sgn, col in [(1, PURPLE), (-1, PURPLE)]:
        ax.annotate("", xy=(2.5 + 0.25 * (sgn > 0), 1 + sgn * g), xytext=(2.5 + 0.25 * (sgn > 0), 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2))
    ax.text(2.0, 0.5, r"$\omega_r\pm g$" "\nvacuum-Rabi\ndoublet", ha="right", va="center",
            color=PURPLE, fontsize=9.5)
    ax.text(0.5, 3.75, "bare states\n(uncoupled, $\\Delta=0$)", ha="center", fontsize=11)
    ax.text(2.7, 3.75, "dressed states\n(eigenstates of $H_{\\rm JC}$)", ha="center", fontsize=11)
    ax.set(xlim=(-1.9, 4.9), ylim=(-0.35, 4.15))
    ax.set_ylabel(r"energy / $\hbar\omega_r$  (excitation number $N$)")
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xticks([])
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_title("Jaynes-Cummings ladder on resonance: splittings grow as $\\sqrt{N}$ "
                 "($g$ exaggerated)", fontsize=11.5)
    fig.tight_layout()
    save(fig, "05-jc-ladder.png")


# ===========================================================================
# Chapter 06: heterodyne readout chain from AWG to a single IQ point
# ===========================================================================
def box(ax, x, y, w, h, text, fc="white", ec=INK, fs=9.5, color=INK, lw=1.3, ls="-"):
    ax.add_patch(patches.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.04",
                                        fc=fc, ec=ec, lw=lw, ls=ls, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color, zorder=4)


def mixer(ax, x, y, r=0.32):
    ax.add_patch(patches.Circle((x, y), r, fc="white", ec=INK, lw=1.3, zorder=3))
    k = r / np.sqrt(2)
    for s in (1, -1):
        ax.plot([x - k, x + k], [y - s * k, y + s * k], color=INK, lw=1.2, zorder=4)


def amp(ax, x, y, size=0.5, direction=1, fc="white", label=None, fs=9):
    """Amplifier triangle pointing right (direction=1) or left (-1)."""
    pts = [(x - direction * size / 2, y - size / 2), (x - direction * size / 2, y + size / 2),
           (x + direction * size / 2, y)]
    ax.add_patch(patches.Polygon(pts, closed=True, fc=fc, ec=INK, lw=1.3, zorder=3))
    if label:
        ax.text(x, y - size / 2 - 0.22, label, ha="center", va="top", fontsize=fs)


def arrow(ax, p0, p1, color=INK, lw=1.3, style="-|>"):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                                      shrinkA=0, shrinkB=0), zorder=2)


@diagram
def ch06_readout_chain():
    fig, ax = plt.subplots(figsize=(12.5, 5.2))
    yt, yb = 3.0, 0.0
    # Fridge outline.
    ax.add_patch(patches.FancyBboxPatch((5.9, -1.1), 4.0, 5.2, boxstyle="round,pad=0.05",
                                        fc="#eef4fb", ec=BLUE, lw=1.2, ls="--", zorder=1))
    ax.text(7.9, 3.75, "dilution refrigerator", ha="center", color=BLUE, fontsize=10)
    # Up-conversion (top row).
    box(ax, 0.6, yt, 1.1, 0.8, "AWG\n$I(t),Q(t)$\nat $f_{\\rm IF}$")
    arrow(ax, (1.15, yt), (2.88, yt))
    mixer(ax, 3.2, yt)
    ax.text(3.2, yt + 0.55, "IQ mixer", ha="center", fontsize=9.5)
    arrow(ax, (3.52, yt), (6.2, yt))
    ax.text(4.75, yt + 0.18, "pulse at $f_{\\rm LO}+f_{\\rm IF}\\approx f_r$", ha="center", fontsize=9.5)
    box(ax, 6.75, yt, 1.0, 0.6, "attenuators\n+ filters", fs=9)
    arrow(ax, (7.25, yt), (7.9, yt))
    # Chip.
    ax.add_patch(patches.FancyBboxPatch((7.9, 1.0), 1.7, 2.4, boxstyle="round,pad=0.04",
                                        fc="white", ec=INK, lw=1.4, zorder=3))
    ax.text(8.75, 2.85, "chip", ha="center", fontsize=10, zorder=4)
    ax.add_patch(patches.Rectangle((8.27, 1.75), 0.96, 0.5, fc="#d9ead3", ec=INK, lw=1, zorder=4))
    ax.text(8.75, 2.0, "resonator", ha="center", va="center", fontsize=8.5, zorder=5)
    ax.add_patch(patches.Circle((8.75, 1.32), 0.2, fc="#fde9d9", ec=INK, lw=1, zorder=4))
    ax.text(8.75, 1.32, "Q", ha="center", va="center", fontsize=8.5, zorder=5)
    ax.text(9.2, 1.32, "$\\chi$", fontsize=10, va="center", zorder=5)
    # Return path (bottom row, right to left).
    arrow(ax, (8.75, 1.0), (8.75, yb + 0.05), )
    ax.plot([8.75, 8.75], [1.0, yb], color=INK, lw=1.3)
    amp(ax, 8.1, yb, direction=-1, fc="#fff2cc", label="TWPA\n10 mK")
    amp(ax, 6.7, yb, direction=-1, fc="#fff2cc", label="HEMT\n4 K")
    arrow(ax, (8.75, yb), (8.35, yb))
    arrow(ax, (7.85, yb), (6.95, yb))
    arrow(ax, (6.45, yb), (5.2, yb))
    amp(ax, 4.95, yb, direction=-1, label="RT amp")
    arrow(ax, (4.7, yb), (3.52, yb))
    mixer(ax, 3.2, yb)
    ax.text(3.2, yb - 0.55, "IQ mixer", ha="center", va="top", fontsize=9.5)
    # Shared local oscillator.
    ax.add_patch(patches.Circle((3.2, 1.5), 0.32, fc="white", ec=INK, lw=1.3, zorder=3))
    sx = np.linspace(-0.2, 0.2, 50)
    ax.plot(3.2 + sx, 1.5 + 0.1 * np.sin(sx * np.pi / 0.1), color=INK, lw=1.1, zorder=4)
    ax.text(2.75, 1.5, "LO\n$f_{\\rm LO}$", ha="right", va="center", fontsize=9.5)
    arrow(ax, (3.2, 1.82), (3.2, yt - 0.32))
    arrow(ax, (3.2, 1.18), (3.2, yb + 0.32))
    # Digital back end.
    arrow(ax, (2.88, yb), (2.0, yb))
    box(ax, 1.55, yb, 0.8, 0.6, "ADC")
    arrow(ax, (1.15, yb), (0.55, yb))
    box(ax, 0.0, yb, 1.05, 1.0, "demodulate\n$\\times e^{-i\\omega_{\\rm IF}t}$\nintegrate\n$\\int w(t)\\,dt$", fs=8.5)
    arrow(ax, (0.0, -0.5), (0.0, -1.15))
    # Mini IQ plane.
    rng = np.random.default_rng(3)
    ins = ax.inset_axes([-0.62, -2.95, 1.25, 1.65], transform=ax.transData)
    for mu, col in [((-1, 0), BLUE), ((1, 0), RED)]:
        pts = rng.normal(mu, 0.38, size=(150, 2))
        ins.scatter(pts[:, 0], pts[:, 1], s=3, color=col, alpha=0.6)
    ins.axvline(0, color=INK, lw=1, ls="--")
    ins.set_xticks([]), ins.set_yticks([])
    ins.set_xlabel("$I$", fontsize=9, labelpad=1)
    ins.set_ylabel("$Q$", fontsize=9, labelpad=1)
    ins.text(-1, 1.25, "$|0\\rangle$", color=BLUE, ha="center", fontsize=9)
    ins.text(1, 1.25, "$|1\\rangle$", color=RED, ha="center", fontsize=9)
    ins.set(xlim=(-2.2, 2.2), ylim=(-1.6, 1.8))
    ax.text(0.85, -2.1, "one shot = one point;\nthreshold assigns 0 or 1", fontsize=9.5, va="center")
    blank(ax, (-1.0, 10.4), (-3.1, 4.6))
    ax.set_title("Heterodyne dispersive readout: the same LO up-converts the pulse "
                 "and down-converts the echo")
    fig.tight_layout()
    save(fig, "06-readout-chain.png")


# ===========================================================================
# Chapter 07: rotations on the Bloch sphere
# ===========================================================================
def bloch_axes(ax, labels=True, xlabel="$+x$"):
    u, v = np.mgrid[0:2 * np.pi:60j, 0:np.pi:30j]
    ax.plot_surface(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v),
                    color="#dfe9f5", alpha=0.18, linewidth=0, shade=False)
    t = np.linspace(0, 2 * np.pi, 200)
    for curve in [(np.cos(t), np.sin(t), 0 * t), (np.cos(t), 0 * t, np.sin(t)),
                  (0 * t, np.cos(t), np.sin(t))]:
        ax.plot(*curve, color=GREY, lw=0.6, alpha=0.6)
    for vec in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        ax.plot([-vec[0], vec[0]], [-vec[1], vec[1]], [-vec[2], vec[2]], color=GREY, lw=0.6)
    if labels:
        ax.text(0, 0, 1.22, r"$|0\rangle$", ha="center", fontsize=11)
        ax.text(0, 0, -1.32, r"$|1\rangle$", ha="center", fontsize=11)
        ax.text(1.38, 0, 0, xlabel, ha="center", fontsize=10)
        ax.text(0, 1.3, 0, "$+y$", ha="center", fontsize=10)
        ax.text(0, -1.38, 0, "$-y$", ha="center", fontsize=10)
    ax.set_box_aspect((1, 1, 1))
    ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))
    ax.view_init(elev=18, azim=28)
    ax.axis("off")


def rotate(r, n, theta):
    """Right-handed rotation of Bloch vector r about unit axis n (Rodrigues)."""
    n = np.asarray(n, float) / np.linalg.norm(n)
    r = np.asarray(r, float)
    return (r * np.cos(theta)[:, None] + np.cross(n, r) * np.sin(theta)[:, None]
            + np.outer(1 - np.cos(theta), n * np.dot(n, r)))


def arrow3d(ax, vec, color, lw=2.2, label=None, scale=1.0, ls="-"):
    v = np.asarray(vec) * scale
    ax.quiver(0, 0, 0, *v, color=color, lw=lw, arrow_length_ratio=0.12, linestyle=ls)
    if label:
        ax.text(*(v * 1.15), label, color=color, fontsize=10, ha="center")


@diagram
def ch07_bloch_rotation():
    fig = plt.figure(figsize=(11.5, 5.4))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    north = np.array([0, 0, 1.0])

    bloch_axes(ax1)
    arrow3d(ax1, (1, 0, 0), ORANGE, scale=1.25)
    ax1.text2D(-0.01, 0.37, "drive axis ($\\phi=0$)", color=ORANGE, fontsize=10,
               transform=ax1.transAxes)
    path = rotate(north, (1, 0, 0), np.linspace(0, np.pi / 2, 100))
    rest = rotate(north, (1, 0, 0), np.linspace(np.pi / 2, np.pi, 100))
    ax1.plot(*path.T, color=BLUE, lw=2.6)
    ax1.plot(*rest.T, color=BLUE, lw=1.4, ls="--")
    arrow3d(ax1, path[-1], BLUE)
    ax1.text(0, -1.25, 0.8, r"$X_{90}$: $\theta=\pi/2$", color=BLUE, fontsize=10, ha="right")
    ax1.text2D(0.12, 0.22, r"$X$: $\theta=\pi$", color=BLUE, fontsize=10, transform=ax1.transAxes)
    ax1.set_title("(a) Resonant drive: axis = phase, angle = pulse area", fontsize=11.5)

    bloch_axes(ax2)
    omega, delta = 1.0, 1.0
    axis = np.array([omega, 0, delta]) / np.hypot(omega, delta)
    arrow3d(ax2, axis, ORANGE, scale=1.25)
    ax2.text(1.05, 0.15, 1.3, r"$\mathbf{b}=(\Omega,0,\Delta)$", color=ORANGE, fontsize=10)
    orbit = rotate(north, axis, np.linspace(0, 2 * np.pi, 200))
    ax2.plot(*orbit.T, color=RED, lw=2.4)
    half = rotate(north, axis, np.array([np.pi]))[0]
    arrow3d(ax2, half, RED)
    ax2.text2D(0.5, 0.07, "lowest point: $P_1=\\Omega^2/\\Omega_R^2=1/2$", color=RED,
               fontsize=10, ha="center", transform=ax2.transAxes)
    ax2.set_title("(b) Detuned drive ($\\Delta=\\Omega$): tilted axis, never reaches $|1\\rangle$",
                  fontsize=11.5)
    fig.text(0.5, 0.02, "Convention of Chapter 07: $|0\\rangle$ at the north pole and "
             "$H_{\\rm rot}=\\frac{\\Delta}{2}\\sigma_z+\\frac{\\Omega}{2}(\\cos\\phi\\,\\sigma_x"
             "+\\sin\\phi\\,\\sigma_y)$, so the Bloch vector precesses about $\\vec{b}$ "
             "at the rate $\\Omega_R=|\\vec{b}|$.", ha="center", fontsize=9.5, color=GREY)
    fig.subplots_adjust(left=0.0, right=1.0, top=0.9, bottom=0.06, wspace=0.0)
    save(fig, "07-bloch-rotation.png")


# ===========================================================================
# Chapter 08: coupling circuits and the exchange level structure
# ===========================================================================
def transmon_cell(d, x, top=2.4, bot=0.0, label="1", gap=1.0):
    part(d, elm.Josephson(), (x, top), (x, bot), f"$E_{{J{label}}}$", loc="top", ofst=0.2)
    part(d, elm.Capacitor(), (x + gap, top), (x + gap, bot), f"$C_{label}$", loc="bottom", ofst=0.2)
    wire(d, (x, top), (x + gap, top))
    wire(d, (x, bot), (x + gap, bot))
    dot(d, (x + gap, top))


@diagram
def ch08_coupling_circuits():
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw={"width_ratios": [1, 1.45]})
    d = schematic(axa)
    transmon_cell(d, 0.0, label="1")
    part(d, elm.Capacitor(), (1.0, 2.4), (2.8, 2.4), "$C_g$", loc="top", ofst=0.2, color=GREEN)
    part(d, elm.Josephson(), (2.8, 2.4), (2.8, 0), "$E_{J2}$", loc="top", ofst=0.2)
    part(d, elm.Capacitor(), (3.8, 2.4), (3.8, 0), "$C_2$", loc="bottom", ofst=0.2)
    wire(d, (2.8, 2.4), (3.8, 2.4))
    wire(d, (0, 0), (3.8, 0))
    dot(d, (2.8, 2.4))
    d.add(elm.Ground().at((1.9, 0)))
    d.draw()
    axa.text(1.9, -1.2, r"$g\approx\frac{1}{2}\frac{C_g}{\sqrt{C_1C_2}}\sqrt{\omega_1\omega_2}$  (always on)",
             ha="center", fontsize=11)
    axa.text(0.5, 3.0, "Q1", ha="center", fontsize=11, fontweight="bold")
    axa.text(3.3, 3.0, "Q2", ha="center", fontsize=11, fontweight="bold")
    blank(axa, (-1.0, 4.8), (-1.6, 3.6))
    title(axa, "a", "Direct capacitive coupling: fixed $g$")

    d = schematic(axb)
    transmon_cell(d, 0.0, label="1")
    part(d, elm.Capacitor(), (1.0, 2.4), (2.4, 2.4), "$C_{1c}$", loc="top", ofst=0.2, color=GREEN)
    # Coupler: SQUID loop shunted by C_c.
    wire(d, (2.4, 2.4), (3.0, 2.4))
    wire(d, (2.6, 1.85), (3.6, 1.85))
    wire(d, (2.6, 0.55), (3.6, 0.55))
    part(d, elm.Josephson(), (2.6, 1.85), (2.6, 0.55))
    part(d, elm.Josephson(), (3.6, 1.85), (3.6, 0.55))
    wire(d, (3.1, 2.4), (3.1, 1.85))
    wire(d, (3.1, 0.55), (3.1, 0.0))
    wire(d, (3.0, 2.4), (4.5, 2.4))
    part(d, elm.Capacitor(), (4.5, 2.4), (4.5, 0), "$C_c$", loc="bottom", ofst=0.2)
    part(d, elm.Capacitor(), (4.5, 2.4), (6.3, 2.4), "$C_{2c}$", loc="top", ofst=0.2, color=GREEN)
    part(d, elm.Josephson(), (6.3, 2.4), (6.3, 0), "$E_{J2}$", loc="top", ofst=0.2)
    part(d, elm.Capacitor(), (7.3, 2.4), (7.3, 0), "$C_2$", loc="bottom", ofst=0.2)
    wire(d, (6.3, 2.4), (7.3, 2.4))
    wire(d, (0, 0), (7.3, 0))
    for p in [(3.1, 2.4), (3.1, 1.85), (3.1, 0.55), (4.5, 2.4), (6.3, 2.4)]:
        dot(d, p)
    # Direct path arching over the coupler.
    wire(d, (1.0, 2.4), (1.0, 3.5))
    part(d, elm.Capacitor(), (1.0, 3.5), (6.3, 3.5), "$C_{12}$ (direct)", loc="bottom", ofst=0.2,
         color=PURPLE)
    wire(d, (6.3, 3.5), (6.3, 2.4))
    d.draw()
    flux_symbol(axb, 3.1, 1.2, r"$\Phi_c$")
    axb.text(0.5, 2.85, "Q1", ha="center", fontsize=11, fontweight="bold")
    axb.text(6.8, 2.85, "Q2", ha="center", fontsize=11, fontweight="bold")
    axb.text(3.1, -0.4, "coupler", ha="center", fontsize=10, color=INK)
    axb.text(3.65, -1.0, r"$g_{\rm eff}=g_{12}+\frac{g_1g_2}{2}\left(\frac{1}{\Delta_1}+\frac{1}{\Delta_2}\right)$:"
             r" tune $\Phi_c$ to cancel the two paths", ha="center", fontsize=11)
    blank(axb, (-1.0, 8.3), (-1.5, 4.6))
    title(axb, "b", "Tunable coupler: interfering direct and indirect paths")
    fig.tight_layout()
    save(fig, "08-coupling-circuits.png")


@diagram
def ch08_exchange_levels():
    fig, (axl, axp) = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={"width_ratios": [1.15, 1]})
    # (a) Which states meet: the iSWAP and CZ resonance conditions side by side.
    def bar(x, y, lab, col=INK, w=0.55):
        axl.hlines(y, x - w / 2, x + w / 2, color=col, lw=2.4)
        axl.text(x, y + 0.13, lab, ha="center", fontsize=10.5, color=col)

    w2, alpha = 1.0, -0.22                     # schematic units, |alpha| exaggerated
    # iSWAP point: omega1 = omega2.
    for x, n, lab in [(0.5, 0, r"$|00\rangle$"), (0.15, 1, r"$|01\rangle$"), (0.85, 1, r"$|10\rangle$")]:
        bar(x, n * w2, lab, BLUE if n == 1 else INK, w=0.5)
    for x, y, lab in [(0.5, 2 * w2, r"$|11\rangle$"), (0.15, 2 * w2 + alpha, r"$|02\rangle$"),
                      (0.85, 2 * w2 + alpha, r"$|20\rangle$")]:
        bar(x, y, lab, GREY, w=0.5)
    axl.annotate("", xy=(0.62, 1.0), xytext=(0.38, 1.0),
                 arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    axl.text(0.5, 1.1, "$g$", color=RED, ha="center", fontsize=11)
    axl.text(0.5, 2.55, "iSWAP point\n$\\omega_1=\\omega_2$", ha="center", fontsize=10.5)
    # CZ point: omega1 = omega2 + alpha2, so |11> meets |02>.
    w1 = w2 + alpha
    x0 = 2.0
    bar(x0 + 0.5, 0, r"$|00\rangle$", INK, w=0.5)
    bar(x0 + 0.15, w2, r"$|01\rangle$", GREY, w=0.5)
    bar(x0 + 0.85, w1, r"$|10\rangle$", GREY, w=0.5)
    bar(x0 + 0.15, 2 * w2 + alpha, r"$|02\rangle$", BLUE, w=0.5)
    bar(x0 + 0.85, w1 + w2, r"$|11\rangle$", BLUE, w=0.5)
    bar(x0 + 0.5, 2 * w1 + alpha, r"$|20\rangle$", GREY, w=0.5)
    axl.annotate("", xy=(x0 + 0.62, w1 + w2), xytext=(x0 + 0.38, w1 + w2),
                 arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
    axl.text(x0 + 0.5, w1 + w2 + 0.1, r"$\sqrt{2}\,g$", color=RED, ha="center", fontsize=11)
    axl.text(x0 + 0.5, 2.55, "CZ point\n$\\omega_1=\\omega_2+\\alpha_2$", ha="center", fontsize=10.5)
    axl.axvline(1.5, color=LIGHT, lw=1.5)
    axl.set(xlim=(-0.25, 3.25), ylim=(-0.25, 3.0))
    axl.set_xticks([])
    axl.set_yticks([0, 1, 2], ["0", "1", "2"])
    axl.set_ylabel("excitation number (energy, schematic)")
    for side in ("top", "right"):
        axl.spines[side].set_visible(False)
    title(axl, "a", "Two resonances, two gates (blue: the states that meet)")

    # (b) Exchange populations at the iSWAP point.
    gt = np.linspace(0, np.pi, 400)
    axp.plot(gt, np.cos(gt) ** 2, color=BLUE, lw=2.2, label=r"$P_{01}=\cos^2 gt$")
    axp.plot(gt, np.sin(gt) ** 2, color=ORANGE, lw=2.2, label=r"$P_{10}=\sin^2 gt$")
    for x, lab in [(np.pi / 4, r"$\sqrt{\rm iSWAP}$" "\n(maximally\nentangling)"),
                   (np.pi / 2, "iSWAP\n(full swap,\nphase $-i$)")]:
        axp.axvline(x, color=GREY, ls="--", lw=1)
        axp.text(x + 0.04, 0.62, lab, fontsize=9.5, va="center")
    axp.set(xlabel=r"dwell angle $gt$", ylabel="population", ylim=(-0.03, 1.3), xlim=(0, np.pi))
    axp.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi],
                   ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    axp.legend(loc="upper center", fontsize=9.5, ncol=2, frameon=False)
    axp.grid(alpha=0.25)
    title(axp, "b", "Start in $|01\\rangle$ at the iSWAP point")
    fig.tight_layout()
    save(fig, "08-exchange-levels.png")


# ===========================================================================
# Chapter 09: pulse sequences as filters; T1 versus dephasing on the sphere
# ===========================================================================
@diagram
def ch09_pulse_sequences():
    fig, axes = plt.subplots(3, 1, figsize=(11, 7.4), sharex=True)
    t_total = 1.0
    w2, w1 = 0.022, 0.044                      # pi/2 and pi pulse widths (schematic)
    rows = [
        ("Ramsey", [(0, "half"), (t_total, "half")], "low-pass: passes DC,\nso slow drift dephases"),
        ("Hahn echo", [(0, "half"), (0.5, "pi"), (t_total, "half")],
         "notch at DC: static\noffsets refocus"),
        ("CPMG, $N=4$", [(0, "half")] + [((2 * k + 1) / 8, "pi") for k in range(4)] + [(t_total, "half")],
         "passband near\n$N/(2t)$"),
    ]
    for ax, (name, pulses, note) in zip(axes, rows):
        ax.axhline(0.6, color=GREY, lw=0.8)
        flips = []
        for t0, kind in pulses:
            w = w2 if kind == "half" else w1
            col = BLUE if kind == "half" else ORANGE
            ax.add_patch(patches.Rectangle((t0 - w / 2, 0.6), w, 0.75, fc=col, ec=INK, lw=0.8))
            lab = r"$\frac{\pi}{2}$" if kind == "half" else (r"$\pi$" if name == "Hahn echo" else r"$\pi_y$")
            ax.text(t0, 1.45, lab, ha="center", va="bottom", fontsize=11)
            if kind == "pi":
                flips.append(t0)
        ax.add_patch(patches.FancyBboxPatch((t_total + 0.05, 0.62), 0.09, 0.6,
                                            boxstyle="round,pad=0.01", fc=LIGHT, ec=INK, lw=0.8))
        ax.text(t_total + 0.095, 0.92, "M", ha="center", va="center", fontsize=10)
        # Switching function g(t): flips sign at every pi pulse.
        edges = [0.0] + flips + [t_total]
        sign = 1
        for a, b in zip(edges, edges[1:]):
            ax.plot([a, b], [-0.45 + 0.35 * sign] * 2, color=GREEN, lw=2)
            sign = -sign
        for f in flips:
            ax.plot([f, f], [-0.8, -0.1], color=GREEN, lw=1.2, ls=":")
        ax.axhline(-0.45, color=GREY, lw=0.6, ls="--")
        ax.text(-0.04, -0.1, "+1", ha="right", va="center", fontsize=8.5, color=GREEN)
        ax.text(-0.04, -0.8, "-1", ha="right", va="center", fontsize=8.5, color=GREEN)
        ax.text(-0.17, 0.95, name, ha="right", va="center", fontsize=11.5, fontweight="bold")
        ax.text(-0.17, -0.45, "switching\nfunction $g(t)$", ha="right", va="center",
                fontsize=9, color=GREEN)
        ax.text(1.2, 0.3, note, ha="left", va="center", fontsize=10)
        ax.set(ylim=(-1.0, 2.0), xlim=(-0.5, 1.55))
        ax.axis("off")
    # Free-evolution annotations.
    def span(ax, a, b, text, y=0.42):
        ax.annotate("", xy=(b, y), xytext=(a, y),
                    arrowprops=dict(arrowstyle="<->", color=INK, lw=0.9, shrinkA=0, shrinkB=0))
        ax.text((a + b) / 2, y - 0.17, text, ha="center", va="top", fontsize=9.5)
    span(axes[0], 0.02, 0.98, r"free evolution $t$")
    span(axes[1], 0.02, 0.48, r"$t/2$")
    span(axes[1], 0.52, 0.98, r"$t/2$")
    span(axes[2], 0.02, 0.105, r"$\delta$")
    span(axes[2], 0.145, 0.355, r"$2\delta$")
    span(axes[2], 0.895, 0.98, r"$\delta$")
    axes[2].set_ylim(-1.45, 2.0)
    axes[2].text(0.5, -1.35, r"time $\rightarrow$   (CPMG: $t=2N\delta$)", ha="center", fontsize=10)
    fig.suptitle("Dynamical decoupling: each $\\pi$ pulse flips the sign with which "
                 "frequency noise accumulates phase", fontsize=12, y=0.99)
    fig.tight_layout()
    save(fig, "09-pulse-sequences.png")


@diagram
def ch09_bloch_decoherence():
    fig = plt.figure(figsize=(11.5, 5.2))
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    bloch_axes(ax1)
    t = np.linspace(0, 4, 200)                 # in units of T1
    path = np.stack([np.exp(-t / 2), 0 * t, 1 - np.exp(-t)], axis=1)
    ax1.plot(*path.T, color=RED, lw=2.4)
    for tk, alpha in [(0, 1.0), (0.5, 0.8), (1.0, 0.6), (2.0, 0.45)]:
        v = np.array([np.exp(-tk / 2), 0, 1 - np.exp(-tk)])
        arrow3d(ax1, v, RED, lw=1.8)
    ax1.text2D(0.5, 0.06, "energy relaxation: the vector shrinks and climbs to $|0\\rangle$\n"
               "populations relax at $1/T_1$, coherence at $1/(2T_1)$", ha="center",
               transform=ax1.transAxes, fontsize=10)
    ax1.set_title("(a) $T_1$: energy leaves the qubit", fontsize=11.5)

    bloch_axes(ax2)
    rng = np.random.default_rng(7)
    angles = rng.normal(0, 0.9, 14)
    for a in angles:
        arrow3d(ax2, (np.cos(a), np.sin(a), 0), BLUE, lw=1.0)
    mean = np.array([np.mean(np.cos(angles)), np.mean(np.sin(angles)), 0])
    arrow3d(ax2, mean, INK, lw=3.0)
    ax2.text2D(0.5, 0.06, "pure dephasing: each run precesses at a slightly different rate;\n"
               "the average (black) shrinks while populations stay put", ha="center",
               transform=ax2.transAxes, fontsize=10)
    ax2.set_title("(b) $T_\\phi$: phase is scrambled, no energy exchanged", fontsize=11.5)
    fig.subplots_adjust(left=0.0, right=1.0, top=0.92, bottom=0.02, wspace=0.0)
    save(fig, "09-bloch-decoherence.png")


# ===========================================================================
# Chapter 10: wiring a dilution refrigerator
# ===========================================================================
def attenuator(ax, x, y, text="20 dB", w=0.62, h=0.34):
    box(ax, x, y, w, h, text, fc="#fde9d9", fs=8.5)


def circulator(ax, x, y, r=0.17):
    ax.add_patch(patches.Circle((x, y), r, fc="white", ec=INK, lw=1.2, zorder=3))
    ax.add_patch(patches.FancyArrowPatch((x + 0.09, y - 0.06), (x - 0.09, y - 0.06),
                                         connectionstyle="arc3,rad=-1.3", arrowstyle="-|>",
                                         mutation_scale=7, color=INK, lw=0.9, zorder=4))


@diagram
def ch10_fridge_wiring():
    fig, ax = plt.subplots(figsize=(12, 9.6))
    stages = [("Room temperature", "300 K", "", 9.6),
              ("50 K plate", "~50 K", "tens of W", 8.4),
              ("4 K plate", "~4 K", "~1 W", 7.2),
              ("Still", "~0.8 K", "~10 mW", 6.0),
              ("Cold plate", "~0.1 K", "~100 uW", 4.8),
              ("Mixing chamber", "~10 mK", "~10-20 uW at 20 mK", 3.6)]
    for name, temp, power, y in stages[1:]:
        ax.add_patch(patches.Rectangle((0.3, y - 0.07), 9.3, 0.14, fc="#c9c9c9", ec="none", zorder=1))
    for name, temp, power, y in stages:
        ax.text(0.15, y + 0.12, name, ha="right", va="bottom", fontsize=10.5, fontweight="bold")
        ax.text(0.15, y - 0.05, temp + ("   " + power if power else ""), ha="right", va="top",
                fontsize=9, color=GREY)
    ax.text(0.15, 10.05, "stage, temperature, cooling power (illustrative)", ha="right",
            fontsize=8.5, color=GREY, style="italic")
    # Sample enclosure hanging below the mixing-chamber plate.
    ax.add_patch(patches.FancyBboxPatch((1.0, 0.0), 5.3, 1.25, boxstyle="round,pad=0.05",
                                        fc="#f4f8fc", ec=BLUE, lw=1.2, ls="--", zorder=1))
    ax.text(3.65, 0.08, "magnetic + IR-tight shield", ha="center", fontsize=8.5, color=BLUE)
    ax.add_patch(patches.FancyBboxPatch((1.7, 0.35), 3.8, 0.62, boxstyle="round,pad=0.04",
                                        fc="white", ec=INK, lw=1.4, zorder=3))
    ax.text(3.6, 0.66, "quantum chip: qubits + readout resonators", ha="center", va="center",
            fontsize=9, zorder=4)

    def anchors(x, ys):
        for y in ys:
            ax.plot([x - 0.12, x + 0.12], [y, y], color=INK, lw=4, zorder=3)

    # Input (drive/readout) line.
    xi = 2.2
    ax.plot([xi, xi], [9.9, 0.97], color=INK, lw=1.4, zorder=2)
    ax.text(xi, 10.05, "drive + readout\ninput", ha="center", va="bottom", fontsize=9.5)
    for y in (7.2, 4.8, 3.6):
        attenuator(ax, xi, y)
    box(ax, xi, 2.9, 0.62, 0.3, "LPF + IR", fc="#e2f0d9", fs=8)
    anchors(xi, (8.4, 6.0))
    for y, val in [(9.0, "892"), (6.6, "20"), (4.2, "0.24"), (3.25, "0.0024")]:
        ax.text(xi - 0.42, y, rf"$\bar n\approx{val}$", ha="right", va="center", fontsize=8.5, color=RED)
    ax.annotate("", xy=(xi, 1.0), xytext=(xi, 1.6), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))

    # Flux line.
    xf = 3.6
    ax.plot([xf, xf], [9.9, 0.97], color=INK, lw=1.4, zorder=2)
    ax.text(xf, 10.05, "flux bias\n(DC + pulses)", ha="center", va="bottom", fontsize=9.5)
    attenuator(ax, xf, 7.2, "ATT")
    box(ax, xf, 2.9, 0.62, 0.3, "low-pass", fc="#e2f0d9", fs=8)
    box(ax, xf, 2.4, 0.62, 0.3, "IR", fc="#e2f0d9", fs=8)
    anchors(xf, (8.4, 6.0, 4.8, 3.6))

    # Output line: the signal travels upward.
    xo = 5.0
    ax.plot([xo, xo], [0.97, 9.9], color=INK, lw=1.4, zorder=2)
    ax.text(xo, 10.05, "readout output\n(to digitizer)", ha="center", va="bottom", fontsize=9.5)
    for y in (1.55, 1.95):
        circulator(ax, xo, y)
    ax.add_patch(patches.Polygon([(xo - 0.22, 2.25), (xo + 0.22, 2.25), (xo, 2.62)],
                                 fc="#fff2cc", ec=INK, lw=1.2, zorder=3))
    circulator(ax, xo, 2.95)
    ax.add_patch(patches.Polygon([(xo - 0.25, 7.0), (xo + 0.25, 7.0), (xo, 7.42)],
                                 fc="#fff2cc", ec=INK, lw=1.2, zorder=3))
    ax.add_patch(patches.Polygon([(xo - 0.25, 9.3), (xo + 0.25, 9.3), (xo, 9.72)],
                                 fc="white", ec=INK, lw=1.2, zorder=3))
    anchors(xo, (8.4, 6.0, 4.8, 3.6))
    ax.annotate("", xy=(xo, 6.65), xytext=(xo, 6.2), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    labels = [(1.75, "circulators / isolators: route the signal, dump amplifier back-action into cold loads"),
              (2.43, "TWPA or JPA: near-quantum-limited first amplifier (pump line not shown)"),
              (2.95, "isolator"),
              (5.4, "superconducting NbTi coax: lossless signal, poor heat conductor"),
              (7.21, "HEMT amplifier: ~40 dB gain, few-kelvin noise temperature"),
              (7.8, "stainless / CuNi coax between warm stages"),
              (9.51, "room-temperature amplifier, then IQ down-conversion")]
    for y, text in labels:
        ax.text(xo + 0.42, y, text, va="center", fontsize=9)

    # Symbol key.
    lx = 7.15
    ax.plot([lx - 0.12, lx + 0.12], [0.95, 0.95], color=INK, lw=4)
    ax.text(lx + 0.4, 0.95, "thermal anchor (heat sink)", va="center", fontsize=8.5)
    attenuator(ax, lx, 0.5, "20 dB", w=0.55, h=0.28)
    ax.text(lx + 0.4, 0.5, "thermalized attenuator", va="center", fontsize=8.5)
    box(ax, lx, 0.05, 0.55, 0.28, "LPF", fc="#e2f0d9", fs=8)
    ax.text(lx + 0.4, 0.05, "filter", va="center", fontsize=8.5)
    ax.text(xi, -0.4, r"red: $\bar n$ at 7 GHz after each stage of attenuation (20/20/20 dB, as in lab 12)",
            fontsize=8.5, color=RED, ha="left")
    ax.set(xlim=(-2.6, 10.6), ylim=(-0.6, 10.8))
    ax.axis("off")
    ax.set_title("Wiring a dilution refrigerator for one qubit (schematic, illustrative values)",
                 fontsize=12.5)
    fig.tight_layout()
    save(fig, "10-fridge-wiring.png")


# ===========================================================================
# Chapter 11: randomized-benchmarking circuits; coherent versus incoherent
# ===========================================================================
def gate(ax, x, y, text, w=0.62, h=0.5, fc="white", fs=10.5):
    ax.add_patch(patches.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02",
                                        fc=fc, ec=INK, lw=1.2, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4)


def meter(ax, x, y, w=0.55, h=0.45):
    ax.add_patch(patches.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02",
                                        fc=LIGHT, ec=INK, lw=1.2, zorder=3))
    ax.add_patch(patches.Arc((x, y - 0.1), 0.36, 0.36, theta1=0, theta2=180, color=INK, lw=1.1, zorder=4))
    ax.plot([x, x + 0.13], [y - 0.1, y + 0.1], color=INK, lw=1.1, zorder=4)


@diagram
def ch11_rb_sequence():
    fig, ax = plt.subplots(figsize=(11.5, 3.8))
    for y, gates, label in [
            (1.6, [r"$C_1$", r"$C_2$", r"$C_3$", "...", r"$C_m$", r"$C_{\rm rec}$"], "standard RB"),
            (0.0, [r"$C_1$", "$G$", r"$C_2$", "$G$", "...", r"$C_m$", "$G$", r"$C_{\rm rec}$"],
             "interleaved RB")]:
        n = len(gates)
        xs = np.linspace(1.0, 8.6, n)
        ax.plot([0.35, 9.35], [y, y], color=INK, lw=1.2, zorder=1)
        ax.text(0.3, y, r"$|0\rangle$", ha="right", va="center", fontsize=12)
        ax.text(-0.35, y + 0.55, label, ha="left", fontsize=11, fontweight="bold")
        for x, g in zip(xs, gates):
            if g == "...":
                ax.text(x, y, r"$\cdots$", ha="center", va="center", fontsize=14,
                        bbox=dict(fc="white", ec="none"))
            else:
                fc = "#fde9d9" if g == "$G$" else ("#e2f0d9" if "rec" in g else "white")
                gate(ax, x, y, g, fc=fc)
        meter(ax, 9.6, y)
        ax.text(10.0, y, "survival\nprobability", va="center", fontsize=9.5)
    ax.text(4.8, -0.8, r"$C_i$: random Cliffords;  $C_{\rm rec}=(\cdots C_2C_1)^{-1}$ undoes the whole "
            r"sequence;  $G$: the Clifford gate under test.  Repeat for many random sequences "
            r"at each length $m$ and fit $A\,p^m+B$.", ha="center", fontsize=9.5, wrap=True)
    ax.set(xlim=(-0.6, 11.0), ylim=(-1.1, 2.6))
    ax.axis("off")
    ax.set_title("Randomized benchmarking circuits", fontsize=12)
    fig.tight_layout()
    save(fig, "11-rb-sequence.png")


@diagram
def ch11_coherent_incoherent():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), gridspec_kw={"width_ratios": [1, 1, 1.35]})
    t = np.linspace(0, 2 * np.pi, 300)
    for ax, kind in zip(axes[:2], ("incoherent", "coherent")):
        ax.plot(np.cos(t), np.sin(t), color=GREY, lw=1.2, ls="--")
        ax.arrow(0, 0, 0, 0.93, color=GREY, width=0.012, head_width=0.07, length_includes_head=True)
        if kind == "incoherent":
            ax.plot(0.7 * np.cos(t), 0.7 * np.sin(t), color=BLUE, lw=2.2)
            ax.arrow(0, 0, 0, 0.65, color=BLUE, width=0.02, head_width=0.09, length_includes_head=True)
            for a in np.linspace(0, 2 * np.pi, 8, endpoint=False):
                ax.annotate("", xy=(0.74 * np.cos(a), 0.74 * np.sin(a)), xytext=(0.97 * np.cos(a), 0.97 * np.sin(a)),
                            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9))
            title(ax, "a", "Stochastic: the sphere shrinks")
            ax.text(0, -1.35, "information lost, errors add\nlike probabilities", ha="center", fontsize=9.5)
        else:
            ang = 0.45
            ax.plot(np.cos(t), np.sin(t), color=RED, lw=2.2)
            ax.arrow(0, 0, -0.97 * np.sin(ang), 0.97 * np.cos(ang), color=RED, width=0.02, head_width=0.09,
                     length_includes_head=True)
            ax.add_patch(patches.Arc((0, 0), 0.8, 0.8, theta1=90, theta2=90 + np.degrees(ang), color=RED, lw=1.3))
            ax.text(-0.6, 0.28, r"$N\epsilon$", color=RED, fontsize=11)
            title(ax, "b", "Coherent: the sphere rotates")
            ax.text(0, -1.35, "no information lost, but errors add\nlike amplitudes", ha="center", fontsize=9.5)
        ax.set(xlim=(-1.3, 1.3), ylim=(-1.75, 1.3))
        ax.set_aspect("equal")
        ax.axis("off")
    r_gate = 1e-4
    eps = 2 * np.arcsin(np.sqrt(1.5 * r_gate))
    n = np.arange(1, 101)
    incoherent = (1 - (1 - 2 * r_gate) ** n) / 2
    coherent = (2 / 3) * np.sin(n * eps / 2) ** 2
    ax = axes[2]
    ax.loglog(n, incoherent, color=BLUE, lw=2.2, label=r"depolarizing: $\approx N r$")
    ax.loglog(n, coherent, color=RED, lw=2.2, label=r"over-rotation: $\approx N^2 r$")
    ax.set(xlabel="number of gates $N$", ylabel="average infidelity after $N$ gates",
           ylim=(5e-5, 1))
    ax.legend(fontsize=9.5, loc="upper left")
    ax.grid(alpha=0.25, which="both")
    title(ax, "c", "Same error per gate ($r=10^{-4}$), different growth")
    fig.tight_layout()
    save(fig, "11-coherent-vs-incoherent.png")


# ===========================================================================
# Chapter 12: repetition-code circuit, surface-code layout, detection events
# ===========================================================================
def cnot(ax, x, yc, yt, color=INK):
    ax.plot([x, x], [yc, yt], color=color, lw=1.3, zorder=2)
    ax.add_patch(patches.Circle((x, yc), 0.07, color=color, zorder=3))
    ax.add_patch(patches.Circle((x, yt), 0.16, fc="white", ec=color, lw=1.3, zorder=3))
    ax.plot([x - 0.16, x + 0.16], [yt, yt], color=color, lw=1.3, zorder=4)
    ax.plot([x, x], [yt - 0.16, yt + 0.16], color=color, lw=1.3, zorder=4)


@diagram
def ch12_repetition_circuit():
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ys = {"q1": 4, "q2": 3, "q3": 2, "a1": 1, "a2": 0}
    starts = {"q1": r"$\alpha|0\rangle+\beta|1\rangle$", "q2": r"$|0\rangle$", "q3": r"$|0\rangle$",
              "a1": r"$|0\rangle$", "a2": r"$|0\rangle$"}
    for k, y in ys.items():
        end = 8.4 if k.startswith("a") else 10.5
        ax.plot([0.2, end], [y, y], color=INK, lw=1.2, zorder=1)
        ax.text(0.1, y, starts[k], ha="right", va="center", fontsize=11)
        ax.text(-2.35, y, {"q1": "data 1", "q2": "data 2", "q3": "data 3",
                           "a1": "ancilla 1", "a2": "ancilla 2"}[k], ha="left", va="center",
                fontsize=9.5, color=GREY)
    # Encoder.
    ax.add_patch(patches.Rectangle((0.5, 1.6), 1.9, 2.8, fc="#eef4fb", ec="none", zorder=0))
    ax.text(1.45, 4.6, "encode", ha="center", fontsize=10, color=BLUE)
    cnot(ax, 1.0, 4, 3)
    cnot(ax, 1.9, 4, 2)
    # Noise.
    ax.add_patch(patches.FancyBboxPatch((2.8, 1.65), 1.0, 2.7, boxstyle="round,pad=0.03",
                                        fc="#fde9d9", ec=RED, lw=1.2, ls="--", zorder=3))
    ax.text(3.3, 3.0, "noise:\nmaybe\n$X_1$, $X_2$\nor $X_3$", ha="center", va="center", fontsize=9.5,
            color=RED, zorder=4)
    # Syndrome extraction.
    ax.add_patch(patches.Rectangle((4.2, -0.4), 3.6, 4.8, fc="#f3f3f3", ec="none", zorder=0))
    ax.text(6.0, 4.6, r"measure $Z_1Z_2$ and $Z_2Z_3$", ha="center", fontsize=10)
    cnot(ax, 4.6, 4, 1)
    cnot(ax, 5.4, 3, 1)
    cnot(ax, 6.4, 3, 0)
    cnot(ax, 7.2, 2, 0)
    for y in (1, 0):
        meter(ax, 8.65, y)
        ax.plot([8.95, 9.6], [y + 0.04, y + 0.04], color=INK, lw=0.9)
        ax.plot([8.95, 9.6], [y - 0.04, y - 0.04], color=INK, lw=0.9)
    gate(ax, 10.05, 0.5, "decoder\n(lookup)", w=0.9, h=1.3, fc=LIGHT, fs=9.5)
    # Correction on the data, classically controlled.
    gate(ax, 10.05, 3.0, "$X_i$?", w=0.7, h=2.4, fc="#e2f0d9")
    for dx in (-0.04, 0.04):
        ax.plot([10.05 + dx, 10.05 + dx], [1.15, 1.8], color=INK, lw=0.9)
    ax.text(10.75, 3.0, "correct", ha="left", va="center", fontsize=9.5, color=GREEN)
    ax.text(5.2, -1.0, "The ancillas learn only parities (do neighbours agree?), never "
            r"$\alpha$ or $\beta$, so the encoded superposition survives the measurement.",
            ha="center", fontsize=9.5)
    ax.set(xlim=(-2.4, 11.6), ylim=(-1.3, 5.0))
    ax.axis("off")
    ax.set_title("Three-qubit bit-flip code: encode, suffer noise, extract the syndrome, correct",
                 fontsize=12)
    fig.tight_layout()
    save(fig, "12-repetition-circuit.png")


def surface_code(ax, d, labels=True, show_logicals=True):
    xcol, zcol = "#f6b26b", "#9fc5e8"
    pos = lambda i, j: (j, -i)                 # row i, column j
    def face(i, j, kind):
        pts = [pos(i, j), pos(i, j + 1), pos(i + 1, j + 1), pos(i + 1, j)]
        ax.add_patch(patches.Polygon(pts, closed=True, fc=xcol if kind == "X" else zcol,
                                     ec="white", lw=1.5, zorder=1))
        cx, cy = j + 0.5, -i - 0.5
        ax.add_patch(patches.Rectangle((cx - 0.08, cy - 0.08), 0.16, 0.16, color=INK, zorder=4))
    def half(p, q, kind, outward):
        (x1, y1), (x2, y2) = p, q
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        ang = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        w = patches.Wedge((cx, cy), 0.5, ang + (0 if outward > 0 else 180),
                          ang + (180 if outward > 0 else 360),
                          fc=xcol if kind == "X" else zcol, ec="white", lw=1.5, zorder=1)
        ax.add_patch(w)
        nx, ny = -(y2 - y1), (x2 - x1)
        norm = np.hypot(nx, ny)
        mx, my = cx + outward * 0.27 * nx / norm, cy + outward * 0.27 * ny / norm
        ax.add_patch(patches.Rectangle((mx - 0.08, my - 0.08), 0.16, 0.16, color=INK, zorder=4))
    for i in range(d - 1):
        for j in range(d - 1):
            face(i, j, "X" if (i + j) % 2 == 0 else "Z")
    for j in range(d - 1):
        if j % 2 == 1:                         # top: X check above each Z face
            half(pos(0, j), pos(0, j + 1), "X", +1)
        if (d - 2 + j) % 2 == 1:               # bottom: X check below each Z face
            half(pos(d - 1, j), pos(d - 1, j + 1), "X", -1)
    for i in range(d - 1):
        if i % 2 == 0:                         # left: Z check beside each X face
            half(pos(i, 0), pos(i + 1, 0), "Z", -1)
        if (i + d - 2) % 2 == 0:               # right: Z check beside each X face
            half(pos(i, d - 1), pos(i + 1, d - 1), "Z", +1)
    if show_logicals:
        ax.plot([-0.3, d - 0.7], [0.0, 0.0], color=BLUE, lw=7, alpha=0.35, zorder=2,
                solid_capstyle="round")
        ax.plot([d - 1, d - 1], [0.3, -(d - 1) - 0.3], color=RED, lw=7, alpha=0.35, zorder=2,
                solid_capstyle="round")
    for i in range(d):
        for j in range(d):
            ax.add_patch(patches.Circle(pos(i, j), 0.14, fc="white", ec=INK, lw=1.4, zorder=5))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set(xlim=(-0.9, d - 0.1 + 0.8), ylim=(-(d - 1) - 0.9, 0.9))


@diagram
def ch12_surface_code():
    fig, (ax3, ax5) = plt.subplots(1, 2, figsize=(12, 5.6), gridspec_kw={"width_ratios": [1.1, 1]})
    surface_code(ax3, 3)
    ax3.text(1.0, 0.75, r"logical $Z_L$: $Z$ on a full row", color=BLUE, ha="center", fontsize=10.5)
    ax3.text(2.75, -1.0, "logical $X_L$:\n$X$ on a full\ncolumn", color=RED, ha="left",
             va="center", fontsize=10.5)
    ax3.set_xlim(-1.0, 4.4)
    title(ax3, "a", "Distance 3: 9 data + 8 measure qubits")
    surface_code(ax5, 5, show_logicals=False)
    title(ax5, "b", "Distance 5: 25 data + 24 measure qubits")
    handles = [Line2D([], [], marker="o", ls="", mfc="white", mec=INK, ms=10, label="data qubit"),
               Line2D([], [], marker="s", ls="", color=INK, ms=6, label="measure (ancilla) qubit"),
               patches.Patch(fc="#f6b26b", label="$X$-type check ($X^{\\otimes 4}$ or $X^{\\otimes 2}$)"),
               patches.Patch(fc="#9fc5e8", label="$Z$-type check ($Z^{\\otimes 4}$ or $Z^{\\otimes 2}$)")]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=10)
    fig.suptitle("Rotated surface code: checkerboard of commuting four-body checks, "
                 "two-body checks on the boundary", fontsize=12)
    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    save(fig, "12-surface-code.png")


@diagram
def ch12_detection_events():
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(12.5, 4.9))
    nchk, nrnd = 6, 5
    for ax in (axa, axb):
        for r in range(nrnd):
            for c in range(nchk):
                ax.add_patch(patches.Circle((c, r), 0.09, fc="white", ec=GREY, lw=1, zorder=2))
            for b in (-1, nchk):
                ax.add_patch(patches.Rectangle((b - 0.09, r - 0.09), 0.18, 0.18, fc=LIGHT, ec=GREY,
                                               lw=1, zorder=2))
            ax.plot([-1, nchk], [r, r], color=LIGHT, lw=1, zorder=1)
        for c in range(nchk):
            ax.plot([c, c], [0, nrnd - 1], color=LIGHT, lw=1, zorder=1)
        ax.set(xlim=(-1.8, nchk + 0.8), ylim=(-0.5, nrnd - 0.4))
        ax.set_xticks(range(nchk), [f"$S_{c + 1}$" for c in range(nchk)])
        ax.set_yticks(range(nrnd), [str(r + 1) for r in range(nrnd)])
        ax.set_ylabel("syndrome round (time)")
        for side in ("top", "right", "left", "bottom"):
            ax.spines[side].set_visible(False)
        ax.tick_params(length=0)

    def defect(ax, c, r):
        ax.plot([c], [r], marker="*", ms=17, color=RED, mec=INK, mew=0.6, zorder=5)

    # (a) A data error and a measurement error, each giving a pair of detection events.
    defect(axa, 1, 2), defect(axa, 2, 2)
    axa.plot([1, 2], [2, 2], color=RED, lw=3, zorder=3)
    axa.text(1.5, 2.25, "data-qubit flip\n(space-like pair)", ha="center", va="bottom", fontsize=9.5)
    defect(axa, 4, 1), defect(axa, 4, 2)
    axa.plot([4, 4], [1, 2], color=PURPLE, lw=3, zorder=3)
    axa.text(4.25, 1.5, "faulty measurement\n(time-like pair)", ha="left", va="center", fontsize=9.5)
    axa.set_xlabel("checks (space)\ndetection event = a check whose outcome changed since the previous round",
                   fontsize=9.5)
    title(axa, "a", "Local faults leave pairs of detection events")
    # (b) A chain that ends on both boundaries: nothing fires.
    axb.plot([-1, nchk], [2, 2], color=RED, lw=3, zorder=3)
    for c in range(nchk + 1):
        axb.plot([c - 0.5], [2], marker="x", ms=9, mew=2, color=RED, zorder=4)
    axb.text(2.5, 2.3, "flip on every data qubit in one row", ha="center", va="bottom", fontsize=9.5)
    axb.set_xlabel("checks (space)\nboth ends absorbed by boundaries: no check fires, yet the logical bit flipped",
                   fontsize=9.5)
    title(axb, "b", "A spanning chain is invisible: logical error")
    fig.suptitle("Decoding in spacetime (repetition-code view; squares are virtual boundary nodes, "
                 "x marks are data-qubit flips)", fontsize=11.5)
    fig.tight_layout()
    save(fig, "12-detection-events.png")


def main(selected):
    for func in REGISTRY:
        if not selected or func.__name__[2:4] in selected:
            func()
    print("all diagrams generated")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
