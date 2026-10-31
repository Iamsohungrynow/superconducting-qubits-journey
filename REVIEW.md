# Repository review, 31 October 2026

This pass checked every chapter, lab README and the reading list again, with
three goals: correct anything still wrong, make the prose read cleanly, and
replace the remaining ASCII sketches with proper diagrams.

## Diagrams

A new script, [`tutorial/figures/make_diagrams.py`](tutorial/figures/make_diagrams.py),
draws 19 original schematic diagrams with Matplotlib and
[schemdraw](https://schemdraw.readthedocs.io): the harmonic versus anharmonic
ladder, the LC circuit and its mechanical twin, the Josephson junction and
washboard, Cooper-pair-box/transmon/SQUID circuits, the exact transmon ladder,
the circuit-QED circuit, the Jaynes-Cummings ladder, a heterodyne readout chain,
Bloch-sphere rotations and decoherence, coupler circuits, the iSWAP/CZ
resonances, Ramsey/echo/CPMG timelines, dilution-refrigerator wiring, RB
circuits, coherent versus stochastic error growth, the bit-flip-code circuit,
rotated surface codes at distance 3 and 5, and spacetime detection events.
Numbers that appear in diagrams (level energies, transition frequencies,
photon occupations, error growth) are computed, not drawn by hand. Every ASCII
diagram in the chapters has been replaced; Mermaid concept maps remain where
they summarize a chapter's logic. All images have descriptive alt text.

## Corrections and clarifications

| Finding | Correction |
|---|---|
| Ch07 said leakage of a 10 ns pulse "scales as $(\Omega/\alpha)^2\approx4\%$" | That is the transient $|2\rangle$ population; the simulated final leakage is $3\times10^{-4}$ (Gaussian) and $4\times10^{-6}$ (DRAG). Text and figure caption now distinguish them |
| Ch10 ASCII cascade started from "16 photons from 4 K" at 5 GHz, inconsistent with the 7 GHz figure and lab 12 | Replaced by a table that propagates 7 GHz noise from 300 K and reproduces lab 12 (20.2, 2.05, 0.021 and 0.24, 0.0024) |
| HEMT added noise quoted as 10-20 photons | 2-5 K noise temperature is about 5-20 photons at readout frequencies; table and Friis estimate updated |
| Ch09 cited a "~50x" CPMG improvement without context | Attributed precisely: more than 50-fold over $T_2^*$ with up to 200 CPMG pulses (Bylander et al.); preprint title difference noted |
| Ch08 limit written as $\alpha\to\infty$ | $|\alpha_{1,2}|\to\infty$, since transmon $\alpha<0$ |
| Ch02 pointed to Chapter 03 for pulse shaping | Chapter 03 builds the nonlinearity; Chapter 07 shapes the pulses |
| Ch03 worked example gave only the leading-order $\alpha$ | Exact value ($-287$ MHz, lab 09) quoted beside it; Ch04 ladder figure shows exact versus quartic transitions |
| Platform table listed the superconducting encoding as "Transmon (charge/flux)" | "Circuit eigenstates (transmon, fluxonium)" |
| Many sentences were comma splices left over from an earlier dash sweep | Rewritten with colons, semicolons, parentheses, or separate sentences throughout chapters, READMEs and the reading list |

Labs 09-12 READMEs now explain the physics and walk through the code at the same
depth as labs 01-08. The tutorial index lists key ideas and the matching lab for
every chapter, and the project README shows a figure gallery.

## Validation (this pass)

Run on Linux with Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1, Matplotlib 3.11.2,
QuTiP 5.3.1 and schemdraw 0.23:

```bash
python hands-on/run_labs.py --all --check
python tutorial/figures/make_figures.py
python tutorial/figures/make_diagrams.py
python tools/check_repo.py
```

All 12 labs pass their numerical checks, all 22 computed figures and 19
diagrams regenerate, and every local link and image resolves. Each new diagram
was inspected visually for overlapping labels and correct physics (for example,
the surface-code layouts were checked for commuting checks and correct
boundary types, and the Bloch-sphere trajectories follow
$\dot{\vec r}=\vec b\times\vec r$ in the Chapter 07 convention). The new
numerical statements were recomputed independently: the exact charge
dispersion at $E_J/E_C=60$ (1.88 kHz), the three-level DRAG simulation, and the
7 GHz attenuator cascade.

---

# Earlier review, 22 September 2026

The repository is now a twelve-chapter, twelve-lab transmon learning course
with a [guided learning path](tutorial/learning-path.md), explicit conventions,
worked checkpoints, and executable numerical checks. It is a companion to
[Krantz et al., arXiv:1904.06560v5](https://arxiv.org/abs/1904.06560v5), not an
exhaustive replacement for that review or an independent scientific peer review.

## Corrections made

| Finding | Correction |
|---|---|
| NumPy 1.24 was allowed although code calls `np.trapezoid` | Require NumPy 2+; document the actually tested environment |
| Chapter 05's atomic Pauli convention was easy to confuse with QuTiP's computational basis | Explicit $\sigma_z=-Z$ translation and a shared units/sign guide |
| Multilevel cavity midpoint was confused with the bare cavity frequency | Explain the common frequency shift separately from state-dependent $\chi$ |
| LC ground-state figure had the wrong width in zero-point-flux units | Correct the Gaussian amplitude so the density has unit rms width |
| Threshold figure extrapolated a scaling ansatz to probabilities greater than one | Stop curves at threshold and mark the invalid region |
| Critical photon number was described as a universal sharp QND boundary | Distinguish the two-level perturbative scale from multilevel transition onset |
| Receiver efficiency conventions could count amplifier noise twice | Distinguish transmission, vacuum-normalized efficiency, and SQL normalization |
| Nominal CZ phase and $P_{20}$ did not quantify the whole gate | Compute projected propagator, mean leakage, and average target overlap |
| Ramsey integration accumulated a small error over many fringes | Tighten solver tolerances and compare the full trace to the analytic solution |
| Several claims were too broad | Qualify Markovian coherence bounds, RB twirling, charge protection, DRAG fidelity, and repeated CZ cycles |
| Exercise confused noisy final readout with noisy syndrome extraction | State the independent reported-bit error model explicitly |
| QEC example blurred measured data, round time, and decoder latency | Attribute the measured milestone and distinguish throughput from latency |
| Early circuit physics and the microwave chain had no dedicated labs | Add transmon spectrum, JC, noise-filter/echo, and thermal/amplifier labs |

Run instructions now use the repository root consistently. Every chapter links
to a learning objective, runnable example, and checkpoint with an answer.
New figures are numerical models with parameter experiments and limitations
described beside them.

## Validation

Tested on Windows with Python 3.12.10, NumPy 2.4.4, SciPy 1.17.1,
Matplotlib 3.11.0, and QuTiP 5.3.0:

```bash
python hands-on/run_labs.py --all --check
python tutorial/figures/make_figures.py
python tools/check_repo.py
git diff --check
```

- All 12 default labs pass numerical checks, including analytic Rabi and
  Lindblad traces, driven-cavity fields, CZ evolution versus a matrix
  exponential, exact depolarizing RB survival, and repetition-code statistics.
- The added transmon lab checks charge-cutoff convergence; the echo lab checks
  quadrature convergence and DC rejection. These are checks of stated models,
  not validation against measured devices.
- All 22 chapter figures regenerate. New lab figures and modified textbook
  figures are visually inspected for readable axes and labels.
- Local file/image links and Python syntax are checked with the standalone
  repository checker. The runner also works when invoked from outside the repo.
- The 37 distinct arXiv paper identifiers cited in the course were opened and
  matched to their intended papers; preprint and published titles can differ.
  This is a reference-identity check, not a full rederivation of each cited paper.

Useful numerical checkpoints: lab 09 gives $f_{01}=4.735480$ GHz,
$\alpha/2\pi=-287.306$ MHz, and charge dispersion 9.908 kHz at
$E_C/h=250$ MHz and $E_J/E_C=50$. Lab 06's unoptimized nominal dwell gives
mean computational leakage 0.001264 and average CZ overlap 0.997870 after local
phase correction. Neither should be presented as an exact ideal gate or spectrum
approximation.

## Scope and remaining advanced work

The [paper map](tutorial/paper-map.md) explicitly lists the boundaries:
fluxonium/flux-qubit numerics, full circuit quantization, pulse-optimized
two-qubit gates, stochastic readout, nonlinear amplifier models, and repeated
noisy surface-code decoding are not implemented. The repository provides enough
executable work for the introductory transmon track; those topics require
additional models before claiming full numerical coverage of the paper.

No real hardware execution, clean-environment installation on other operating
systems, or exhaustive verification of every literature claim was performed.
The default numerical checks are regression guards, not a proof that every
possible learner modification is physically meaningful.
