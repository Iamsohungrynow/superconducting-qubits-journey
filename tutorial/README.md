# 📑 Tutorial Index: Superconducting Qubits from Scratch

Welcome! This is a self-contained, beginner-friendly tour of superconducting qubits, written for anyone with undergraduate physics and a little linear algebra. It starts from "what is a qubit?", builds the device up one circuit element at a time (LC oscillator, Josephson junction, transmon), and carries you through control, readout, the cryogenic chain, benchmarking, and a first look at quantum error correction. Every chapter teaches standard, publicly known physics in plain language, works at least one example with numbers, and ends with common pitfalls, key takeaways, and pointers to the canonical literature. All numbers are illustrative, order-of-magnitude values meant to build intuition.

Start with the [guided learning path and exercises](learning-path.md), [notation guide](00-notation.md), and [paper-to-course map](paper-map.md).

## Chapters

| # | Chapter | Key ideas | Lab |
|---|---------|-----------|-----|
| 01 | [**Introduction: Why Superconducting Qubits**](01-introduction.md) | DiVincenzo criteria, why nonlinearity is mandatory, the transmon trade-off, a preview of readout and wiring | [12](../hands-on/12-microwave-chain/) |
| 02 | [**The Quantum LC Oscillator**](02-quantum-lc-oscillator.md) | node flux, canonical quantization, zero-point fluctuations, thermal occupation | figures |
| 03 | [**The Josephson Junction & Anharmonicity**](03-josephson-junction.md) | Josephson relations, cosine potential, charge-basis Hamiltonian, charge dispersion | [09](../hands-on/09-transmon-spectrum/) |
| 04 | [**The Transmon Qubit**](04-transmon.md) | Duffing spectrum, exponential versus power law, SQUID tuning, sweet spots | [09](../hands-on/09-transmon-spectrum/) |
| 05 | [**Circuit QED: Qubits + Resonators**](05-circuit-qed.md) | Jaynes-Cummings ladder, vacuum-Rabi exchange, Schrieffer-Wolff, multilevel $\chi$, Purcell decay | [10](../hands-on/10-jaynes-cummings/) |
| 06 | [**Dispersive Readout**](06-readout.md) | pointer states, SNR and assignment fidelity, measurement-induced dephasing, quantum-limited amplification | [04](../hands-on/04-dispersive-readout/) |
| 07 | [**Single-Qubit Gates & Control**](07-single-qubit-gates.md) | rotating frame, Bloch rotations, generalized Rabi, leakage and DRAG, virtual Z, reset | [01](../hands-on/01-bloch-sphere/), [02](../hands-on/02-rabi/), [05](../hands-on/05-drag-leakage/) |
| 08 | [**Two-Qubit Gates**](08-two-qubit-gates.md) | exchange coupling, residual $ZZ$, CZ, tunable couplers, cross-resonance, iSWAP and fSim | [06](../hands-on/06-cz-gate/) |
| 09 | [**Coherence, Noise & Decoherence**](09-coherence-noise.md) | Bloch-Redfield rates, noise spectra and filter functions, echo and CPMG, materials | [03](../hands-on/03-t1-t2/), [11](../hands-on/11-noise-echo/) |
| 10 | [**The Cryogenic & Microwave Chain**](10-measurement-chain.md) | thermal photons, attenuator cascades, heat loads, the Haus-Caves limit, Friis | [12](../hands-on/12-microwave-chain/) |
| 11 | [**Calibration & Benchmarking**](11-benchmarking.md) | calibration loop, RB and interleaved RB, XEB, assignment matrix, coherent versus stochastic errors | [07](../hands-on/07-randomized-benchmarking/) |
| 12 | [**A First Look at Quantum Error Correction**](12-error-correction.md) | stabilizers, repetition and Shor codes, the surface code, spacetime decoding, threshold | [08](../hands-on/08-repetition-code/) |

## How to use this tutorial

Read the chapters in order; each one builds directly on the previous. Before running a lab, predict its result on paper, then use the [learning path](learning-path.md) checkpoints to test yourself. Following the "Go deeper" references at the end of each chapter (plus the [reading list](../reading-list/README.md)) is the fastest way to reach depth.

## About the figures

Every figure is original. The computed plots come from [`figures/make_figures.py`](figures/make_figures.py), using the same illustrative parameters as the worked examples; the schematic diagrams (circuits, level ladders, Bloch spheres, pulse sequences, wiring, code layouts) come from [`figures/make_diagrams.py`](figures/make_diagrams.py). Where a diagram shows numbers, such as level energies or photon occupations, they are computed rather than drawn by hand. Each image carries descriptive alt text for screen readers.

---

← [Project README](../README.md) · 📚 [Annotated reading list](../reading-list/README.md)
