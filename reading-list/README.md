# Superconducting Qubits: An Annotated Reading List

A curated entry point into the literature on superconducting qubits, aimed at
someone who has a physics or engineering background and wants to come up to
speed on how these devices are designed, controlled, read out, and scaled.

The prose below is original and teaches only standard, publicly known physics.
Any numbers mentioned are generic and explicitly labelled *illustrative*; this
list contains no device-specific parameters, unpublished results, or
proprietary data. Every reference is a public source (arXiv, textbook, or a
well-known review). Each arXiv identifier below has been checked against the
arXiv listing; the few papers with no preprint are cited by their published
venue instead.

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

These two reviews are the recommended on-ramp. Read them first; almost every
later entry will make more sense afterwards.

- **A Quantum Engineer's Guide to Superconducting Qubits**, Krantz, Kjaergaard,
  Yan, Orlando, Gustavsson, Oliver (2019), A pedagogical, engineering-minded
  walkthrough covering qubit Hamiltonians, the transmon, control and readout
  hardware, noise and decoherence, and gate implementations. It is the single
  best place to start because it connects the physics to the actual microwave
  and cryogenic engineering. https://arxiv.org/abs/1904.06560

- **Superconducting Qubits: Current State of Play**, Kjaergaard, Schwartz,
  Braumüller, Krantz, Wang, Gustavsson, Oliver (2020), A higher-level survey of
  where the field stood circa 2020: qubit modalities, gate and readout schemes,
  coherence, and progress toward error correction. Pairs naturally with the
  Quantum Engineer's Guide as the "what" to its "how". https://arxiv.org/abs/1905.13641

- **Building Logical Qubits in a Superconducting Quantum Computing System**, Gambetta, Chow, Steffen (2017), A concise perspective on the architectural
  path from physical to logical qubits, useful for framing why the rest of the
  list matters. https://arxiv.org/abs/1510.04375

---

## Foundational theory

The conceptual core: how a circuit becomes a qubit, and how it couples to light.

- **Quantum Coherence with a Single Cooper Pair**, Bouchiat, Vion, Joyez,
  Esteve, Devoret (1998), An early demonstration of charge quantization and
  coherence in a Cooper-pair box, one of the first superconducting qubit
  precursors. Establishes the charge-qubit starting point that the transmon
  later tamed. (no arXiv preprint; published in Physica Scripta T76, 1998)

- **Manipulating the Quantum State of an Electrical Circuit**, Vion, Aassime,
  Cottet, Joyez, Pothier, Urbina, Esteve, Devoret (2002), The "quantronium"
  experiment, which introduced operating a charge qubit at a noise-insensitive
  sweet spot, a design idea that recurs throughout the field. https://arxiv.org/abs/cond-mat/0205343

- **Charge-Insensitive Qubit Design Derived from the Cooper Pair Box**, Koch,
  Yu, Gambetta, Houck, Schuster, Majer, Blais, Devoret, Girvin, Schoelkopf
  (2007), *The* transmon paper. It shows that shunting the Cooper-pair box with
  a large capacitor exponentially suppresses charge noise while retaining enough
  anharmonicity to act as a qubit. This design underlies the overwhelming
  majority of today's devices. https://arxiv.org/abs/cond-mat/0703002

- **Cavity Quantum Electrodynamics for Superconducting Electrical Circuits**, Blais, Huang, Wallraff, Girvin, Schoelkopf (2004), The founding theory paper
  of circuit QED: it maps a superconducting qubit coupled to a microwave
  resonator onto the Jaynes-Cummings model, enabling dispersive readout and
  cavity-mediated coupling. https://arxiv.org/abs/cond-mat/0402216

- **Strong Coupling of a Single Photon to a Superconducting Qubit Using Circuit
  Quantum Electrodynamics**, Wallraff, Schuster, Blais, Frunzio, Huang, Majer,
  Kumar, Girvin, Schoelkopf (2004), The experiment that realized the
  circuit-QED proposal, demonstrating strong coupling between a qubit and a
  single microwave photon. https://arxiv.org/abs/cond-mat/0407325

- **Circuit Quantum Electrodynamics**, Blais, Grimsmo, Girvin, Wallraff (2021), A comprehensive, modern review of cQED theory and practice: quantization of
  circuits, light-matter coupling regimes, readout, and multi-qubit
  architectures. The natural deep dive after the 2004 founding papers. https://arxiv.org/abs/2005.12667

- **Superconducting Qubits: A Short Review**, Devoret, Wallraff, Martinis
  (2004), A compact early review from key figures in the field; helpful
  historical context on the competing qubit modalities (charge, flux, phase)
  before the transmon's dominance. https://arxiv.org/abs/cond-mat/0411174

---

## Readout & amplification

Measuring a qubit without destroying neighboring information requires both a
clever measurement scheme (dispersive readout) and near-quantum-limited
amplifiers.

- **Approaching Unit Visibility for Control of a Superconducting Qubit with
  Dispersive Readout**, Wallraff, Schuster, Blais, Frunzio, Majer, Devoret,
  Girvin, Schoelkopf (2005), An early, high-fidelity demonstration of
  dispersive readout, where the qubit state pulls the resonator frequency and is
  inferred from the transmitted microwave signal. https://arxiv.org/abs/cond-mat/0502645

- **A Near-Quantum-Limited Josephson Traveling-Wave Parametric Amplifier**, Macklin, O'Brien, Hover, Schwartz, Bolkhovsky, Zhang, Oliver, Siddiqi (2015), Introduces the broadband Josephson traveling-wave parametric amplifier
  (TWPA), which made fast, high-fidelity, multiplexed readout practical by
  amplifying near the quantum limit over a wide bandwidth. (no arXiv preprint; published in Science 350, 2015)

---

## Gates

How single- and two-qubit operations are actually implemented on transmons.

- **Simple All-Microwave Entangling Gate for Fixed-Frequency Superconducting
  Qubits**, Chow, Córcoles, Gambetta, Rigetti, Johnson, Smolin, Rozen, Keefe,
  Rothwell, Ketchen, Steffen (2011), Introduces the cross-resonance gate, an
  all-microwave two-qubit entangling gate widely used on fixed-frequency
  architectures. https://arxiv.org/abs/1106.0553

- **Tunable Coupling Scheme for Implementing High-Fidelity Two-Qubit Gates**, Yan, Krantz, Sung, Kjaergaard, Campbell, Orlando, Gustavsson, Oliver (2018), Describes a tunable coupler that can turn qubit-qubit interactions on and off,
  suppressing residual coupling and enabling fast, high-fidelity two-qubit
  gates. https://arxiv.org/abs/1803.09813

---

## Coherence & materials

Coherence times are ultimately limited by materials defects and loss channels;
this thread covers how those are characterized and improved.

- **Decoherence in Josephson Qubits from Dielectric Loss**, Martinis, Cooper,
  McDermott, Steffen, Ansmann, Osborn, Cicak, Oh, Pappas, Simmonds, Yu (2005), Identifies two-level-system defects in dielectrics as a dominant loss channel,
  framing much of the subsequent materials effort. https://arxiv.org/abs/cond-mat/0507622

- **New Material Platform for Superconducting Transmon Qubits with Coherence
  Times Exceeding 0.3 Milliseconds**, Place, Rodgers, Mundada, Smitham,
  Fitzpatrick, Leng, Premkumar, Bryon, Vrajitoarea, Sussman, Cheng, Madhavan,
  Babla, Le, Gang, Jäck, Gyenis, Yao, Cava, de Leon, Houck (2021), Demonstrates
  tantalum-based transmons reaching markedly longer coherence than the
  then-standard niobium/aluminum devices, kicking off the "tantalum transmon"
  materials direction. https://arxiv.org/abs/2003.00024

- **Transmon Qubit with Relaxation Time Exceeding 0.5 Milliseconds**, Wang, Li,
  Xu, Li, Wang, et al. (2021), A complementary tantalum-transmon result,
  reinforcing that careful materials and surface treatment substantially extend
  energy-relaxation times. https://arxiv.org/abs/2105.09890

---

## Error correction & roadmaps

Physical qubits are noisy; useful computation needs quantum error correction.
This section moves from the dominant code (surface code) to recent below-
threshold logical-qubit milestones.

- **Surface Codes: Towards Practical Large-Scale Quantum Computation**, Fowler, Mariantoni, Martinis, Cleland (2012), The standard reference on the
  surface code: a 2D lattice of physical qubits with a comparatively forgiving
  error threshold and purely local stabilizer measurements, which is why it
  became the default target architecture. https://arxiv.org/abs/1208.0928

- **State Preservation by Repetitive Error Detection in a Superconducting
  Quantum Circuit**, Kelly, Barends, Fowler, Megrant, Jeffrey, White, Sank,
  Mutus, Campbell, Chen, et al. (2015), An early experimental demonstration of
  repeated stabilizer-style error detection on a superconducting chip, an
  important proof of principle on the road to the surface code. https://arxiv.org/abs/1411.7403

- **Exponential Suppression of Bit or Phase Errors with Cyclic Error
  Correction**, Google Quantum AI (2021), Shows that error rates can be
  suppressed exponentially as a repetition code is made larger, a key scaling
  signature on the path to fault tolerance. https://arxiv.org/abs/2102.06132

- **Suppressing Quantum Errors by Scaling a Surface Code Logical Qubit**, Google Quantum AI (2023), A milestone showing that increasing surface-code
  distance can reduce the logical error rate, i.e. operating near the
  break-even point where larger codes help rather than hurt. https://arxiv.org/abs/2207.06431

- **Quantum Error Correction Below the Surface Code Threshold**, Google Quantum
  AI (2024), Reports a surface-code logical qubit operating *below* threshold,
  with the logical error rate decreasing as code distance grows, a headline
  fault-tolerance result for the platform. https://arxiv.org/abs/2408.13687

---

## Suggested reading order

1. **Orient yourself** with the two reviews: Krantz et al. (2019) for the
   engineering "how", then Kjaergaard et al. (2020) for the field-level "what".
2. **Build the core theory**: Koch et al. (2007) for the transmon, then Blais
   et al. (2004) for circuit QED, followed by the Blais et al. (2021) cQED
   review for depth. Dip into the Cooper-pair-box / quantronium papers
   (Bouchiat 1998, Vion 2002) for historical grounding.
3. **Learn the subsystems**: dispersive readout and the TWPA amplifier, then
   the gate papers (cross-resonance and tunable couplers).
4. **Understand the limits**: dielectric-loss decoherence and the tantalum-
   transmon materials advances.
5. **Look ahead**: the surface-code reference, then the sequence of
   error-correction experiments culminating in the below-threshold logical-qubit
   results.

> Note on identifiers: the arXiv identifiers given inline have been verified
> against the arXiv listing (title, authors, and year). Two entries, the
> Bouchiat et al. (1998) Cooper-pair-box paper and the Macklin et al. (2015)
> TWPA paper, have no arXiv preprint, and are cited by their published venue
> instead.
