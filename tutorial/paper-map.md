# How this course connects to Krantz et al.

Primary reading: [A Quantum Engineer's Guide to Superconducting Qubits, arXiv:1904.06560v5](https://arxiv.org/abs/1904.06560v5).
The journal publication is from 2019; v5 is the 2021 arXiv revision. Section
labels below follow the PDF. The experimental HTML rendering omits some later
sections, so use the PDF contents when following this map.

| Paper section | Course chapters | Numerical work |
|---|---|---|
| II.A: oscillator to transmon | 02–04 | 09: charge-basis spectrum |
| II.B: Hamiltonian engineering | 04 | 09; SQUID figure generator |
| II.C: interactions | 05, 08 | 10: JC spectrum; 06: coupled transmons |
| III: noise and mitigation | 09–10 | 03: Markovian decay; 11: echo; 12: thermal chain |
| IV.D: single-qubit control | 07 | 01, 02, 05: Bloch, Rabi, DRAG |
| IV.E–H: two-qubit control | 08 | 06: resonant CZ mechanism |
| V.A–D: readout and Purcell filtering | 05–06 | 04: pointer fields; 10: dispersive limit |
| V.E: amplification | 06, 10 | 12: amplifier noise budget |

This is an original **transmon-focused companion**, not a complete reproduction
of the review. Chapter 11 develops benchmarking and Chapter 12 extends into QEC;
their specific references supply material beyond the review's main treatment.

## What still deserves a separate advanced course?

- Flux-qubit and fluxonium spectra (II.B.2), including inductive shunts and
  transition matrix elements. The transmon Hamiltonian alone cannot describe them.
- Full capacitance-matrix quantization and longitudinal coupling (II.C).
- Microscopic quasiparticle/TLS models and reconstruction of an unknown noise PSD.
- Pulse-optimized adiabatic CZ, cross-resonance, parametric gates, and tunable
  couplers. The existing CZ simulation uses a sudden constant-frequency dwell.
- Stochastic single-shot readout, IQ mixer imperfections, a circuit model of a
  Purcell filter, and nonlinear parametric-amplifier dynamics.
- Noisy repeated syndrome extraction and a surface-code decoder. Majority voting
  in lab 08 is a classical statistical model of one error channel.

These boundaries matter: a teaching simulation can establish a mechanism without
being a device-design or experimental-calibration package.

[Learning path and exercises](learning-path.md) · [Notation](00-notation.md)
