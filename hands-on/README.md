# Hands-On Track

These labs let you simulate and run the physics from the tutorial chapters on your own laptop. Each lab is a small, self-contained NumPy/SciPy or QuTiP simulation that turns a chapter's equations into something you can plot, tweak, and explore. No hardware, no accounts, and no lab setup are needed. Everything runs locally in pure simulation, so you can start experimenting right away.

## Setup (from the repository root)

Use Python 3.12. Create an isolated environment once:

```bash
python -m venv .venv
```

Activate on Windows PowerShell with `.venv\Scripts\Activate.ps1`, or on
macOS/Linux with `source .venv/bin/activate`. If PowerShell blocks activation,
use `.venv\Scripts\python.exe` in place of `python`; no policy change is needed.

```bash
python -m pip install -r hands-on/requirements.txt
python hands-on/run_labs.py --list
python hands-on/run_labs.py 09 10 --check
python hands-on/run_labs.py --all --check
```

`--check` uses a noninteractive plotting backend, runs each lab in a separate
process, checks numerical physics identities, saves figures, and writes an
ignored `hands-on/run-report.json` with results and installed versions. It
returns a nonzero exit status if any lab fails. Omit `--check` to open plots;
close each plot to proceed to the next lab. Running a script directly works too.
The runner can be invoked by absolute path from another working directory.

Verified environment: Python 3.12.10, NumPy 2.4.4, SciPy 1.17.1,
Matplotlib 3.11.0, QuTiP 5.3.0. NumPy 2+ is required for `np.trapezoid`.
The requirements specify supported API bounds, not a claim that every version
combination has been tested. The automated checks target the default teaching
parameters; restore defaults after experiments.

Follow the [learning path](../tutorial/learning-path.md) for a chapter-by-chapter
sequence, predictions, exercises, and answers. Read the [notation guide](../tutorial/00-notation.md)
before translating equations into code.

## Simulation labs

| Lab | Topic | Theory chapter |
| --- | --- | --- |
| [01-bloch-sphere/](01-bloch-sphere/) | Qubit states and the Bloch sphere | [tutorial/07-single-qubit-gates.md](../tutorial/07-single-qubit-gates.md) |
| [02-rabi/](02-rabi/) | Rabi oscillations | [tutorial/07-single-qubit-gates.md](../tutorial/07-single-qubit-gates.md) |
| [03-t1-t2/](03-t1-t2/) | T1 relaxation and T2 dephasing | [tutorial/09-coherence-noise.md](../tutorial/09-coherence-noise.md) |
| [04-dispersive-readout/](04-dispersive-readout/) | Dispersive readout (qubit-state-dependent cavity) | [tutorial/06-readout.md](../tutorial/06-readout.md) |
| [05-drag-leakage/](05-drag-leakage/) | Leakage to the third level and DRAG pulses | [tutorial/07-single-qubit-gates.md](../tutorial/07-single-qubit-gates.md) |
| [06-cz-gate/](06-cz-gate/) | A CZ gate from the \|11> <-> \|20> avoided crossing | [tutorial/08-two-qubit-gates.md](../tutorial/08-two-qubit-gates.md) |
| [07-randomized-benchmarking/](07-randomized-benchmarking/) | Randomized benchmarking (error per Clifford) | [tutorial/11-benchmarking.md](../tutorial/11-benchmarking.md) |
| [08-repetition-code/](08-repetition-code/) | Bit-flip repetition code and break-even | [tutorial/12-error-correction.md](../tutorial/12-error-correction.md) |
| [09-transmon-spectrum/](09-transmon-spectrum/) | Exact spectrum, charge dispersion, cutoff convergence | Chapters 03–04 |
| [10-jaynes-cummings/](10-jaynes-cummings/) | Avoided crossing, vacuum-Rabi exchange, perturbative limits | Chapter 05 |
| [11-noise-echo/](11-noise-echo/) | Ramsey/echo filters integrated against a noise PSD | Chapter 09 |
| [12-microwave-chain/](12-microwave-chain/) | Thermal attenuators and amplifier noise budget | Chapter 10 |

## Regenerate textbook figures

```bash
python tutorial/figures/make_figures.py
```

This regenerates the chapter figures headlessly. Lab figures are regenerated
when their script runs. Figures are teaching models, not measured device data.

## Roadmap

- [x] QuTiP simulation labs: available now
- [ ] Run on real IBM hardware (Qiskit + IBM Quantum): planned
- [ ] Characterize real devices (Qibocal / Qibolab): planned

## See also

- [Repository overview](../README.md)
- [Tutorial chapters](../tutorial/README.md)
