# Superconducting Qubits: An Annotated Reading List

A curated entry point into the literature on superconducting qubits, aimed at
someone who has a physics or engineering background and wants to come up to
speed on how these devices are designed, controlled, read out, and scaled.

The prose below is original and teaches only standard, publicly known physics.
Any numbers mentioned are generic and explicitly labelled *illustrative*; this
list contains no device-specific parameters, unpublished results, or
proprietary data. Every reference is a public source (arXiv, textbook, or a
well-known review). Identifiers, titles and venues were checked against arXiv
and publisher records; where the arXiv title differs from the published one,
both are given. The few papers with no preprint are cited by their published
venue and DOI.

**How to use this list.** Each section matches part of the
[tutorial](../tutorial/README.md). Read the ⭐ entries first; the rest are for
when a chapter leaves you wanting the original argument or the experimental
details.

| Section | Tutorial chapters |
|---|---|
| [Start here (reviews)](#start-here-reviews) | all |
| [Circuit quantization and the transmon](#circuit-quantization-and-the-transmon) | 02 to 04 |
| [Circuit QED](#circuit-qed) | 05 |
| [Readout and amplification](#readout-and-amplification) | 06, 10 |
| [Gates](#gates) | 07 to 08 |
| [Benchmarking](#benchmarking) | 11 |
| [Coherence, noise and materials](#coherence-noise-and-materials) | 09 to 10 |
| [Error correction](#error-correction) | 12 |

---

## Why superconducting qubits?

A superconducting qubit is, at its core, a nonlinear electrical resonator built
from capacitors, inductors, and one or more Josephson junctions, cooled to tens
of millikelvin. The Josephson junction supplies the *nonlinearity* that turns an
otherwise harmonic LC circuit into an anharmonic oscillator, so that the lowest
two energy levels can be addressed as a qubit without accidentally driving
transitions to higher states. The same lithographic and microwave-engineering
toolbox that built classical electronics can therefore be repurposed to build
quantum bits, which is a large part of why the platform has scaled so quickly.
The references below trace that story from the first reviews through the
foundational theory, the supporting subsystems (readout, gates, materials), and
on to error correction.

---

## Start here (reviews)

The first two reviews below are the recommended on-ramp. Read them first; almost
every later entry will make more sense afterwards.

- ⭐ **A Quantum Engineer's Guide to Superconducting Qubits.** Krantz, Kjaergaard,
  Yan, Orlando, Gustavsson, Oliver (2019). *Appl. Phys. Rev.* 6, 021318.
  [arXiv:1904.06560](https://arxiv.org/abs/1904.06560)
  A pedagogical, engineering-minded walkthrough covering qubit Hamiltonians, the
  transmon, control and readout hardware, noise and decoherence, and gate
  implementations. It is the single best place to start because it connects the
  physics to the actual microwave and cryogenic engineering. The
  [paper map](../tutorial/paper-map.md) shows which chapter covers which section.

- ⭐ **Superconducting Qubits: Current State of Play.** Kjaergaard, Schwartz,
  Braumüller, Krantz, Wang, Gustavsson, Oliver (2020). *Annu. Rev. Condens.
  Matter Phys.* 11, 369. [arXiv:1905.13641](https://arxiv.org/abs/1905.13641)
  A higher-level survey of where the field stood circa 2020: qubit modalities,
  gate and readout schemes, coherence, and progress toward error correction.
  Pairs naturally with the Quantum Engineer's Guide as the "what" to its "how".

- **Circuit Quantum Electrodynamics.** Blais, Grimsmo, Girvin, Wallraff (2021).
  *Rev. Mod. Phys.* 93, 025005. [arXiv:2005.12667](https://arxiv.org/abs/2005.12667)
  A comprehensive, modern review of cQED theory and practice: quantization of
  circuits, light-matter coupling regimes, readout, and multi-qubit
  architectures. The natural deep dive after the first two reviews.

- **Building Logical Qubits in a Superconducting Quantum Computing System.**
  Gambetta, Chow, Steffen (2017). *npj Quantum Inf.* 3, 2.
  [arXiv:1510.04375](https://arxiv.org/abs/1510.04375)
  A concise perspective on the architectural path from physical to logical
  qubits, useful for framing why the rest of the list matters.

- **Superconducting Qubits: A Short Review.** Devoret, Wallraff, Martinis (2004).
  [arXiv:cond-mat/0411174](https://arxiv.org/abs/cond-mat/0411174)
  A compact early review from key figures in the field; helpful historical
  context on the competing qubit modalities (charge, flux, phase) before the
  transmon's dominance.

---

## Circuit quantization and the transmon

The conceptual core: how a circuit becomes a quantum system, and why the
transmon won.

- ⭐ **Introduction to Quantum Electromagnetic Circuits.** Vool, Devoret (2017).
  *Int. J. Circ. Theor. Appl.* 45, 897. [arXiv:1610.03438](https://arxiv.org/abs/1610.03438)
  The rigorous node-flux procedure behind Chapter 02: Lagrangian, conjugate
  charge, Hamiltonian, quantization, and how it generalizes to networks.

- **The Superconducting Circuit Companion: An Introduction with Worked
  Examples.** Rasmussen, Christensen, et al. (2021).
  *PRX Quantum* 2, 040204 (published as "Superconducting Circuit Companion: an
  Introduction with Worked Examples"). [arXiv:2103.01225](https://arxiv.org/abs/2103.01225)
  A tutorial that quantizes many standard circuits step by step, including
  couplers and drives; a good bridge from this course to research papers.

- **Quantum Coherence with a Single Cooper Pair.** Bouchiat, Vion, Joyez,
  Esteve, Devoret (1998). *Physica Scripta* T76, 165 (no arXiv preprint).
  An early demonstration of charge quantization and coherence in a Cooper-pair
  box, one of the first superconducting qubit precursors. Establishes the
  charge-qubit starting point that the transmon later tamed.

- **Manipulating the Quantum State of an Electrical Circuit.** Vion, Aassime,
  Cottet, Joyez, Pothier, Urbina, Esteve, Devoret (2002). *Science* 296, 886.
  [arXiv:cond-mat/0205343](https://arxiv.org/abs/cond-mat/0205343)
  The "quantronium" experiment, which introduced operating a charge qubit at a
  noise-insensitive sweet spot, a design idea that recurs throughout the field.

- ⭐ **Charge-Insensitive Qubit Design Derived from the Cooper Pair Box.** Koch,
  Yu, Gambetta, Houck, Schuster, Majer, Blais, Devoret, Girvin, Schoelkopf
  (2007). *Phys. Rev. A* 76, 042319. [arXiv:cond-mat/0703002](https://arxiv.org/abs/cond-mat/0703002)
  *The* transmon paper. It shows that shunting the Cooper-pair box with a large
  capacitor exponentially suppresses its sensitivity to charge noise while
  retaining enough anharmonicity to act as a qubit, and derives most formulas of
  Chapters 03 to 05. This design underlies the overwhelming majority of today's
  devices.

---

## Circuit QED

How a qubit couples to a resonator, and why one coupling serves readout and
entanglement alike.

- ⭐ **Cavity Quantum Electrodynamics for Superconducting Electrical Circuits: An
  Architecture for Quantum Computation.** Blais, Huang, Wallraff, Girvin,
  Schoelkopf (2004). *Phys. Rev. A* 69, 062320.
  [arXiv:cond-mat/0402216](https://arxiv.org/abs/cond-mat/0402216)
  The founding theory paper of circuit QED: it maps a superconducting qubit
  coupled to a microwave resonator onto the Jaynes-Cummings model, enabling
  dispersive readout and cavity-mediated coupling.

- **Strong Coupling of a Single Photon to a Superconducting Qubit Using Circuit
  Quantum Electrodynamics.** Wallraff, Schuster, Blais, Frunzio, Huang, Majer,
  Kumar, Girvin, Schoelkopf (2004). *Nature* 431, 162.
  [arXiv:cond-mat/0407325](https://arxiv.org/abs/cond-mat/0407325)
  The experiment that realized the circuit-QED proposal, observing the
  vacuum-Rabi splitting of Chapter 05 between a qubit and a single microwave
  photon.

- **Resolving Photon Number States in a Superconducting Circuit.** Schuster,
  Houck, Schreier, et al. (2007). *Nature* 445, 515.
  [arXiv:cond-mat/0608693](https://arxiv.org/abs/cond-mat/0608693)
  Enters the strong-dispersive regime, where each photon in the cavity shifts the
  qubit by a resolvable $2\chi$: the "qubit picture" of the cross-Kerr term in
  Chapter 06, seen directly in spectroscopy.

- **Coupling Superconducting Qubits via a Cavity Bus.** Majer, Chow, Gambetta,
  et al. (2007). *Nature* 449, 443.
  [arXiv:0709.2135](https://arxiv.org/abs/0709.2135)
  Demonstrates the virtual-photon "quantum bus" of Chapter 05: two qubits
  exchange excitations through a resonator that stays in its ground state.

---

## Readout and amplification

Measuring a qubit without destroying neighboring information requires both a
clever measurement scheme (dispersive readout) and near-quantum-limited
amplifiers.

- **Approaching Unit Visibility for Control of a Superconducting Qubit with
  Dispersive Readout.** Wallraff, Schuster, Blais, Frunzio, Majer, Devoret,
  Girvin, Schoelkopf (2005). *Phys. Rev. Lett.* 95, 060501.
  [arXiv:cond-mat/0502645](https://arxiv.org/abs/cond-mat/0502645)
  An early time-domain, ensemble-averaged demonstration of dispersive readout,
  where the qubit state pulls the resonator frequency and is inferred from the
  transmitted microwave signal.

- ⭐ **Qubit-Photon Interactions in a Cavity: Measurement-Induced Dephasing and
  Number Splitting.** Gambetta, Blais, Schuster, et al. (2006). *Phys. Rev. A* 74, 042318.
  [arXiv:cond-mat/0602322](https://arxiv.org/abs/cond-mat/0602322)
  The standard quantitative treatment of measurement back-action used in
  Chapter 06, valid beyond the small-$\chi$ limit.

- **Fast Reset and Suppressing Spontaneous Emission of a Superconducting Qubit.**
  Reed et al. (2010). *Appl. Phys.
  Lett.* 96, 203110. [arXiv:1003.0142](https://arxiv.org/abs/1003.0142)
  Introduces the Purcell filter: a frequency-selective element that protects the
  qubit's $T_1$ without slowing readout.

- **Fast Accurate State Measurement with Superconducting Qubits.** Jeffrey, Sank,
  et al. (2014). *Phys. Rev. Lett.* 112, 190504 (arXiv title: "Fast Scalable
  State Measurement with Superconducting Qubits").
  [arXiv:1401.0257](https://arxiv.org/abs/1401.0257)
  A bandpass Purcell filter on a multiplexed feedline, with fast, high-fidelity
  readout; a template for modern readout design.

- **Quantum Theory of a Bandpass Purcell Filter for Qubit Readout.** Sete,
  Martinis, Korotkov (2015). *Phys. Rev. A* 92, 012325.
  [arXiv:1504.06030](https://arxiv.org/abs/1504.06030)
  The theory behind the filter above, including how much it suppresses Purcell
  decay at the qubit frequency.

- **Rapid High-Fidelity Single-Shot Dispersive Readout of Superconducting
  Qubits.** Walter, Kurpiers, Gasparinetti, et al. (2017). *Phys. Rev. Applied*
  7, 054020 (arXiv title: "Realizing Rapid, High-Fidelity, Single-Shot Dispersive
  Readout of Superconducting Qubits"). [arXiv:1701.06933](https://arxiv.org/abs/1701.06933)
  Shows how choosing $\kappa$, $\chi$ and photon number together, as in the
  trade-off table of Chapter 06, gives readout in under 100 ns.

- **Rapid High-Fidelity Multiplexed Readout of Superconducting Qubits.** Heinsoo,
  Andersen, Remm, et al. (2018). *Phys. Rev. Applied* 10, 034040.
  [arXiv:1801.07904](https://arxiv.org/abs/1801.07904)
  Frequency-multiplexed readout of several qubits on one line, with individual
  Purcell filters and a careful account of crosstalk.

- **A Near-Quantum-Limited Josephson Traveling-Wave Parametric Amplifier.**
  Macklin, O'Brien, Hover, Schwartz, Bolkhovsky, Zhang, Oliver, Siddiqi (2015).
  *Science* 350, 307 (no arXiv preprint). [DOI:10.1126/science.aaa8525](https://doi.org/10.1126/science.aaa8525)
  Demonstrates a practical broadband Josephson traveling-wave parametric
  amplifier (TWPA), which made fast, high-fidelity, multiplexed readout practical
  by amplifying near the quantum limit over a wide bandwidth.

- ⭐ **Introduction to Quantum Noise, Measurement, and Amplification.** Clerk,
  Devoret, Girvin, Marquardt, Schoelkopf (2010). *Rev. Mod. Phys.* 82, 1155.
  [arXiv:0810.4729](https://arxiv.org/abs/0810.4729)
  The definitive source for the standard quantum limit, noise temperature, and
  the measurement-rate versus dephasing-rate bound of Chapters 06 and 10.

- **Quantum Limits on Noise in Linear Amplifiers.** Caves (1982). *Phys. Rev. D*
  26, 1817 (no arXiv preprint). [DOI:10.1103/PhysRevD.26.1817](https://doi.org/10.1103/PhysRevD.26.1817)
  The original half-photon added-noise theorem for phase-insensitive amplifiers.

---

## Gates

How single- and two-qubit operations are actually implemented on transmons.

- ⭐ **Simple Pulses for Elimination of Leakage in Weakly Nonlinear Qubits.**
  Motzoi, Gambetta, Rebentrost, Wilhelm (2009). *Phys. Rev. Lett.* 103, 110501.
  [arXiv:0901.0534](https://arxiv.org/abs/0901.0534)
  The original DRAG paper: the derivative quadrature and detuning correction of
  Chapter 07.

- **Efficient Z Gates for Quantum Computing.** McKay, Wood, Sheldon, Chow,
  Gambetta (2017). *Phys. Rev. A* 96, 022330.
  [arXiv:1612.00858](https://arxiv.org/abs/1612.00858)
  Virtual-Z gates: zero-duration, error-free $z$ rotations by frame bookkeeping.

- **Demonstration of Two-Qubit Algorithms with a Superconducting Quantum
  Processor.** DiCarlo, Chow, Gambetta, et al. (2009). *Nature* 460, 240.
  [arXiv:0903.2030](https://arxiv.org/abs/0903.2030)
  The first CZ gate through the $|11\rangle$-$|02\rangle$ avoided crossing of
  Chapter 08, used to run small algorithms.

- **Simple All-Microwave Entangling Gate for Fixed-Frequency Superconducting
  Qubits.** Chow, Córcoles, Gambetta, Rigetti, Johnson, Smolin, Rozen, Keefe,
  Rothwell, Ketchen, Steffen (2011). *Phys. Rev. Lett.* 107, 080502.
  [arXiv:1106.0553](https://arxiv.org/abs/1106.0553)
  Demonstrates the cross-resonance gate (proposed theoretically by Paraoanu in
  2006 and by Rigetti and Devoret in 2010), an all-microwave two-qubit
  entangling gate widely used on fixed-frequency architectures.

- **Procedure for Systematically Tuning Up Cross-Talk in the Cross-Resonance
  Gate.** Sheldon, Magesan, Chow, Gambetta (2016). *Phys. Rev. A* 93, 060302.
  [arXiv:1603.04821](https://arxiv.org/abs/1603.04821)
  The echoed cross-resonance gate and Hamiltonian tomography used to cancel the
  spurious $IX$, $ZI$ and $ZZ$ terms of Chapter 08.

- **Effective Hamiltonian Models of the Cross-Resonance Gate.** Magesan, Gambetta
  (2020). *Phys. Rev. A* 101, 052308. [arXiv:1804.04073](https://arxiv.org/abs/1804.04073)
  Derives the $ZX/IX/ZZ$ decomposition and its dependence on detuning and
  anharmonicity, including the frequency-collision structure.

- **Superconducting Quantum Circuits at the Surface Code Threshold for Fault
  Tolerance.** Barends, Kelly, Megrant, et al. (2014). *Nature* 508, 500 (arXiv
  title: "Logic gates at the surface code threshold: Superconducting qubits
  poised for fault-tolerant quantum computing").
  [arXiv:1402.4848](https://arxiv.org/abs/1402.4848)
  Single- and two-qubit gates benchmarked with RB and interleaved RB at fidelities
  near the surface-code threshold; a landmark for Chapters 08 and 11.

- **Tunable Coupling Scheme for Implementing High-Fidelity Two-Qubit Gates.**
  Yan, Krantz, Sung, Kjaergaard, Campbell, Orlando, Gustavsson, Oliver (2018).
  *Phys. Rev. Applied* 10, 054062. [arXiv:1803.09813](https://arxiv.org/abs/1803.09813)
  Describes a tunable coupler that can turn qubit-qubit interactions on and off
  by interfering direct and indirect paths, suppressing residual coupling and
  enabling fast, high-fidelity two-qubit gates.

- **Fast, High-Fidelity Conditional-Phase Gate Exploiting Leakage Interference in
  Weakly Anharmonic Superconducting Qubits.** Rol, Battistel, Malinowski, et al.
  (2019). *Phys. Rev. Lett.* 123, 120502 (arXiv title: "A fast, low-leakage,
  high-fidelity two-qubit gate for a programmable superconducting quantum
  computer"). [arXiv:1903.02492](https://arxiv.org/abs/1903.02492)
  The bipolar "net-zero" flux pulse for CZ mentioned in Chapter 08.

- **Demonstrating a Continuous Set of Two-Qubit Gates for Near-Term Quantum
  Algorithms.** Foxen, Neill, Dunsworth, et al. (2020). *Phys. Rev. Lett.* 125,
  120504. [arXiv:2001.08343](https://arxiv.org/abs/2001.08343)
  The fSim gate family that interpolates between iSWAP-like and CZ-like gates.

- **Realization of High-Fidelity CZ and ZZ-Free iSWAP Gates with a Tunable
  Coupler.** Sung, Ding, Braumüller, et al. (2021). *Phys. Rev. X* 11, 021058.
  [arXiv:2011.01261](https://arxiv.org/abs/2011.01261)
  Shows how a tunable coupler nulls residual $ZZ$ and supports both CZ and iSWAP
  at high fidelity.

---

## Benchmarking

How to assign an honest number to a gate (Chapter 11).

- ⭐ **Scalable and Robust Randomized Benchmarking of Quantum Processes.** Magesan,
  Gambetta, Emerson (2011). *Phys. Rev. Lett.* 106, 180504.
  [arXiv:1009.3639](https://arxiv.org/abs/1009.3639)
  The standard RB protocol and the twirling argument behind the single decay
  parameter $p$.

- **Efficient Measurement of Quantum Gate Error by Interleaved Randomized
  Benchmarking.** Magesan, Gambetta, Johnson, et al. (2012). *Phys. Rev. Lett.*
  109, 080505. [arXiv:1203.4550](https://arxiv.org/abs/1203.4550)
  Interleaved RB and its systematic error bound.

- **Quantification and Characterization of Leakage Errors.** Wood, Gambetta
  (2018). *Phys. Rev. A* 97, 032306. [arXiv:1704.03081](https://arxiv.org/abs/1704.03081)
  Leakage and seepage rates and how to extract them with an RB-style
  experiment, the model quoted in Chapter 11.

- **Estimating the Coherence of Noise.** Wallman, Granade, Harper, Flammia
  (2015). *New J. Phys.* 17, 113020. [arXiv:1503.07865](https://arxiv.org/abs/1503.07865)
  Unitarity (purity) benchmarking, which separates coherent from stochastic
  errors.

- **Characterizing Quantum Supremacy in Near-Term Devices.** Boixo, Isakov,
  Smelyanskiy, et al. (2018). *Nat. Phys.* 14, 595.
  [arXiv:1608.00263](https://arxiv.org/abs/1608.00263)
  Cross-entropy benchmarking with random circuits.

- **Quantum Supremacy Using a Programmable Superconducting Processor.** Arute et
  al. (2019). *Nature* 574, 505. [DOI:10.1038/s41586-019-1666-5](https://doi.org/10.1038/s41586-019-1666-5);
  supplementary information at [arXiv:1910.11333](https://arxiv.org/abs/1910.11333)
  XEB at scale on a 53-qubit processor, including the per-gate error budget that
  predicts circuit fidelity.

---

## Coherence, noise and materials

Coherence times are ultimately limited by materials defects and loss channels;
this thread covers how those are characterized and improved.

- **Decoherence in a Superconducting Quantum Bit Circuit.** Ithier, Collin,
  Joyez, et al. (2005). *Phys. Rev. B* 72, 134519.
  [arXiv:cond-mat/0508588](https://arxiv.org/abs/cond-mat/0508588)
  Free-induction versus echo decay under $1/f$ noise, sweet spots, and why
  Ramsey envelopes become Gaussian: the backbone of Chapter 09.

- **Noise Spectroscopy through Dynamical Decoupling with a Superconducting Flux
  Qubit.** Bylander, Gustavsson, Yan, et al. (2011). *Nat. Phys.* 7, 565 (arXiv
  title: "Dynamical decoupling and noise spectroscopy with a superconducting flux
  qubit"). [arXiv:1101.4707](https://arxiv.org/abs/1101.4707)
  Uses CPMG sequences with up to 200 pulses as a tunable filter to measure the
  noise spectrum, and extends the decay time more than 50-fold over $T_2^*$.

- **Decoherence in Josephson Qubits from Dielectric Loss.** Martinis, Cooper,
  McDermott, Steffen, Ansmann, Osborn, Cicak, Oh, Pappas, Simmonds, Yu (2005).
  *Phys. Rev. Lett.* 95, 210503. [arXiv:cond-mat/0507622](https://arxiv.org/abs/cond-mat/0507622)
  Identifies two-level-system defects in dielectrics as a dominant loss channel,
  framing much of the subsequent materials effort.

- **Towards Understanding Two-Level-Systems in Amorphous Solids: Insights from
  Quantum Circuits.** Müller, Cole, Lisenfeld (2019). *Rep. Prog. Phys.* 82,
  124501. [arXiv:1705.01108](https://arxiv.org/abs/1705.01108)
  A thorough review of what TLS defects are, how they couple to qubits, and how
  they are measured.

- **Observation of High Coherence in Josephson Junction Qubits Measured in a
  Three-Dimensional Circuit QED Architecture.** Paik, Schuster, Bishop, et al.
  (2011). *Phys. Rev. Lett.* 107, 240501. [arXiv:1105.4652](https://arxiv.org/abs/1105.4652)
  The 3D transmon: moving the electric field away from lossy surfaces raised
  coherence by an order of magnitude, the participation-ratio idea of Chapter 09.

- **Coherent Josephson Qubit Suitable for Scalable Quantum Integrated Circuits.**
  Barends, Kelly, Megrant, et al. (2013). *Phys. Rev. Lett.* 111, 080502.
  [arXiv:1304.2322](https://arxiv.org/abs/1304.2322)
  The planar "Xmon" transmon, combining good coherence with the connectivity
  needed for multi-qubit chips.

- **New Material Platform for Superconducting Transmon Qubits with Coherence
  Times Exceeding 0.3 Milliseconds.** Place, Rodgers, Mundada, Smitham,
  Fitzpatrick, Leng, Premkumar, Bryon, Vrajitoarea, Sussman, Cheng, Madhavan,
  Babla, Le, Gang, Jäck, Gyenis, Yao, Cava, de Leon, Houck (2021). *Nat. Commun.*
  12, 1779. [arXiv:2003.00024](https://arxiv.org/abs/2003.00024)
  Demonstrates tantalum-based transmons reaching markedly longer coherence than
  the then-standard niobium/aluminum devices, kicking off the "tantalum
  transmon" materials direction.

- **Transmon Qubit with Relaxation Time Exceeding 0.5 Milliseconds.** Wang, Li,
  Xu, Li, Wang, et al. (2021). Published in *npj Quantum Inf.* 8, 3 (2022) as
  "Towards practical quantum computers: transmon qubit with a lifetime
  approaching 0.5 milliseconds". [arXiv:2105.09890](https://arxiv.org/abs/2105.09890)
  A complementary tantalum-transmon result, reinforcing that careful materials
  and surface treatment substantially extend energy-relaxation times.

- **Millisecond Lifetimes and Coherence Times in 2D Transmon Qubits.** Bland,
  Bahrami, et al. (2025). *Nature* 647, 343 (arXiv title: "2D transmons with
  lifetimes and coherence times exceeding 1 millisecond").
  [arXiv:2503.14798](https://arxiv.org/abs/2503.14798)
  Tantalum on high-resistivity silicon pushes planar transmons past the
  millisecond mark; a best-device result, not a typical value.

- **Hot Nonequilibrium Quasiparticles in Transmon Qubits.** Serniak, Hays, de
  Lange, et al. (2018). *Phys. Rev. Lett.* 121, 157701.
  [arXiv:1803.00476](https://arxiv.org/abs/1803.00476)
  Measures quasiparticle tunnelling and the effective qubit temperature, two of
  the loss channels in the Chapter 09 cheat sheet.

- **Resolving Catastrophic Error Bursts from Cosmic Rays in Large Arrays of
  Superconducting Qubits.** McEwen, Faoro, Arya, et al. (2022). *Nat. Phys.* 18,
  107. [arXiv:2104.05219](https://arxiv.org/abs/2104.05219)
  High-energy impacts create correlated bursts of quasiparticle errors across a
  chip, a reminder that the independent-error model of Chapter 12 can fail.

- **Engineering Cryogenic Setups for 100-Qubit Scale Superconducting Circuit
  Systems.** Krinner, Storz, Kurpiers, et al. (2019). *EPJ Quantum Technol.* 6, 2.
  [arXiv:1806.07862](https://arxiv.org/abs/1806.07862)
  The practical guide to fridge wiring behind Chapter 10: heat loads,
  attenuation, filtering, and coax materials.

---

## Error correction

Physical qubits are noisy; useful computation needs quantum error correction.
This section moves from the theory of the surface code to the recent
below-threshold logical-qubit milestones.

- **Topological Quantum Memory.** Dennis, Kitaev, Landahl, Preskill (2002).
  *J. Math. Phys.* 43, 4452. [arXiv:quant-ph/0110143](https://arxiv.org/abs/quant-ph/0110143)
  The surface code as a quantum memory, its threshold, and the spacetime
  matching picture of decoding used in Chapter 12.

- **Universal Quantum Computation with Ideal Clifford Gates and Noisy Ancillas.**
  Bravyi, Kitaev (2005). *Phys. Rev. A* 71, 022316.
  [arXiv:quant-ph/0403025](https://arxiv.org/abs/quant-ph/0403025)
  Magic-state distillation, the standard route to the non-Clifford $T$ gate.

- ⭐ **Surface Codes: Towards Practical Large-Scale Quantum Computation.** Fowler,
  Mariantoni, Martinis, Cleland (2012). *Phys. Rev. A* 86, 032324.
  [arXiv:1208.0928](https://arxiv.org/abs/1208.0928)
  The standard reference on the surface code: a 2D lattice of physical qubits
  with a comparatively forgiving error threshold and purely local stabilizer
  measurements, which is why it became the default target architecture.

- **Surface Code Quantum Computing by Lattice Surgery.** Horsman, Fowler, Devitt,
  Van Meter (2012). *New J. Phys.* 14, 123011. [arXiv:1111.4022](https://arxiv.org/abs/1111.4022)
  Logical two-qubit operations by merging and splitting code patches.

- **Quantum Error Correction for Quantum Memories.** Terhal (2015). *Rev. Mod.
  Phys.* 87, 307. [arXiv:1302.3428](https://arxiv.org/abs/1302.3428)
  A rigorous, readable review of stabilizer codes, decoding and thresholds.

- **State Preservation by Repetitive Error Detection in a Superconducting
  Quantum Circuit.** Kelly, Barends, Fowler, Megrant, Jeffrey, White, Sank,
  Mutus, Campbell, Chen, et al. (2015). *Nature* 519, 66.
  [arXiv:1411.7403](https://arxiv.org/abs/1411.7403)
  An early experimental demonstration of repeated stabilizer-style error
  detection on a superconducting chip, an important proof of principle on the
  road to the surface code.

- **Removing Leakage-Induced Correlated Errors in Superconducting Quantum Error
  Correction.** McEwen, Kafri, Chen, et al. (2021). *Nat. Commun.* 12, 1761.
  [arXiv:2102.06131](https://arxiv.org/abs/2102.06131)
  Why leakage breaks the Pauli-digitization argument of Chapter 12, and an
  unconditional multi-level reset that removes it.

- **Exponential Suppression of Bit or Phase Errors with Cyclic Error
  Correction.** Google Quantum AI (Chen et al.) (2021). *Nature* 595, 383 (arXiv
  title: "Exponential suppression of bit or phase flip errors with repetitive
  error correction"). [arXiv:2102.06132](https://arxiv.org/abs/2102.06132)
  Shows that error rates can be suppressed exponentially as a repetition code is
  made larger, a key scaling signature on the path to fault tolerance.

- **Realizing Repeated Quantum Error Correction in a Distance-Three Surface
  Code.** Krinner, Lacroix, Remm, et al. (2022). *Nature* 605, 669.
  [arXiv:2112.03708](https://arxiv.org/abs/2112.03708)
  A complete distance-3 surface code with repeated syndrome extraction and
  real-time-capable control.

- **Suppressing Quantum Errors by Scaling a Surface Code Logical Qubit.** Google
  Quantum AI (2023). *Nature* 614, 676. [arXiv:2207.06431](https://arxiv.org/abs/2207.06431)
  A milestone showing that increasing surface-code distance can reduce the
  logical error rate, i.e. operating near the threshold, the crossover below
  which larger codes help rather than hurt.

- ⭐ **Quantum Error Correction Below the Surface Code Threshold.** Google Quantum
  AI and collaborators (Acharya et al.) (2025). *Nature* 638, 920.
  [arXiv:2408.13687](https://arxiv.org/abs/2408.13687)
  Reports a surface-code logical qubit operating *below* threshold, with the
  logical error rate decreasing as code distance grows, a headline
  fault-tolerance result for the platform.

---

## Suggested reading order

1. **Orient yourself** with the two reviews: Krantz et al. (2019) for the
   engineering "how", then Kjaergaard et al. (2020) for the field-level "what".
2. **Build the core theory**: Vool and Devoret (2017) for circuit quantization,
   Koch et al. (2007) for the transmon, then Blais et al. (2004) for circuit QED,
   followed by the Blais et al. (2021) review for depth. Dip into the
   Cooper-pair-box / quantronium papers (Bouchiat 1998, Vion 2002) for historical
   grounding.
3. **Learn the subsystems**: Gambetta et al. (2006) and the Purcell-filter papers
   for readout, Clerk et al. (2010) for amplification, then the gate papers (DRAG,
   virtual Z, CZ, cross-resonance, tunable couplers) and the benchmarking papers.
4. **Understand the limits**: Ithier et al. (2005) and Bylander et al. (2011) for
   noise, then dielectric loss, quasiparticles, and the tantalum-transmon materials
   advances.
5. **Look ahead**: Dennis et al. (2002) and Fowler et al. (2012) for the surface
   code, then the sequence of error-correction experiments culminating in the
   below-threshold logical-qubit results.

> Note on identifiers: where a paper's published title differs from its arXiv
> preprint, the published title is used and the arXiv title is given in
> parentheses. Four entries (Bouchiat et al. 1998, Macklin et al. 2015, Caves 1982,
> and the main text of Arute et al. 2019) are cited by their published venue
> instead of a preprint.
