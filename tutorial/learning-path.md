# Read → predict → run → explain

Use this as your laboratory notebook. Read a chapter, calculate its checkpoint
on paper, run the linked lab, then change one parameter and explain the result.
Each session can take 45–90 minutes; the full course needs several sessions.

Start with [notation and units](00-notation.md), the [paper map](paper-map.md),
and the [Python setup](../hands-on/README.md). Commands below run from the
repository root. Lab numbers preserve the original repository order; the
recommended learning order is deliberately different.

| Chapter | By the end you should be able to… | Run and investigate |
|---|---|---|
| [01](01-introduction.md) | Explain why nonlinearity and refrigeration solve different problems | `python hands-on/12-microwave-chain/chain.py`; compare 10 and 100 mK |
| [02](02-quantum-lc-oscillator.md) | Quantize an LC mode and calculate its zero-point scales | `python tutorial/figures/make_figures.py`; inspect the two chapter-02 figures |
| [03](03-josephson-junction.md) | Build the charge-basis matrix from the cosine | `python hands-on/09-transmon-spectrum/transmon.py`; compare charge cutoffs |
| [04](04-transmon.md) | Distinguish exact spectrum, quartic approximation, and asymptotic dispersion | Lab 09 again; sweep EJ at fixed EC |
| [05](05-circuit-qed.md) | Connect a spectral splitting to an excitation-swap time | `python hands-on/10-jaynes-cummings/jaynes_cummings.py` |
| [06](06-readout.md) | Explain pointer separation, ring-up, and receiver noise | `python hands-on/04-dispersive-readout/dispersive.py`; vary drive and cutoff |
| [07](07-single-qubit-gates.md) | Turn a pulse into a rotation and distinguish leakage from gate error | Run `bloch.py`, `rabi.py`, and `drag.py` via `python hands-on/run_labs.py 01 02 05` |
| [08](08-two-qubit-gates.md) | Separate local phases, conditional phase, leakage, and unwanted exchange | `python hands-on/06-cz-gate/cz_gate.py`; inspect full CZ overlap |
| [09](09-coherence-noise.md) | Recognize exponential versus nonexponential decay and explain echo | `python hands-on/run_labs.py 03 11` |
| [10](10-measurement-chain.md) | Calculate a staged photon and amplifier-noise budget | `python hands-on/12-microwave-chain/chain.py` |
| [11](11-benchmarking.md) | Extract error per Clifford and state the RB assumptions | `python hands-on/07-randomized-benchmarking/rb.py` |
| [12](12-error-correction.md) | Explain which errors repetition corrects and what it cannot protect | `python hands-on/08-repetition-code/repetition.py` |

## Checkpoints: try before revealing the answers

1. **Initialization:** Is a 5 GHz mode at 100 mK effectively empty? Distinguish
   oscillator photon occupation from the excited-state population of a thermal qubit.
2. **LC:** For $L=10$ nH and $C=100$ fF, calculate $f$, impedance, and
   $\Phi_{\rm zpf}Q_{\rm zpf}$.
3. **Josephson:** Why is the charge-matrix off-diagonal $-E_J/2$, and how many
   rows does cutoff 20 give?
4. **Transmon:** At $E_C/h=250$ MHz and $E_J/E_C=50$, which predicted quantity
   has the larger relative quartic-approximation error: frequency or anharmonicity?
5. **JC:** If $g/2\pi=100$ MHz, what are the avoided-crossing gap and swap time?
6. **Readout:** For $\kappa/2\pi=5$ MHz, calculate the photon and field decay times.
   Does twice the field separation necessarily imply twice the assignment fidelity?
7. **Control:** At $\Omega/2\pi=20$ MHz, how long is a resonant pi pulse? Does
   final $P_2=10^{-9}$ prove that the pulse is a high-fidelity X gate?
8. **CZ:** Why can virtual Z rotations correct local phases but not $|01\rangle
   \leftrightarrow|10\rangle$ exchange or population in $|02\rangle$?
9. **Noise:** Find $T_2$ for $T_1=30$ us and $T_\phi=40$ us. Can ideal echo
   undo Markovian energy relaxation?
10. **Chain:** At fixed total attenuation, why does moving an attenuator to a
    warmer stage change the photon budget?
11. **RB:** A single-qubit fit gives $p=0.98$. What is error per Clifford?
    Why is the default lab's sequence scatter essentially zero?
12. **QEC:** Evaluate the three-bit failure probability at $p=0.01$.
    What does observing zero failures in two million shots establish?

<details>
<summary>Answers and interpretation</summary>

1. $\bar n\approx0.100$ is not negligible. A thermal two-level qubit instead has
   $p_e=1/(e^{hf/k_BT}+1)\approx0.083$; in equilibrium $p_e=\bar n/(2\bar n+1)$.
2. $f\approx5.03$ GHz, $Z\approx316$ ohms, and the product is $\hbar/2$.
3. $\cos\varphi=(e^{i\varphi}+e^{-i\varphi})/2$ shifts charge by one;
   integers -20 through 20 give 41 rows.
4. Exact numerics give 4.73548 GHz and -287.31 MHz. Leading estimates are
   4.75 GHz and -250 MHz: about 0.31% versus 13.0% relative error.
5. 200 MHz and 2.5 ns. The gap is $2g$; the full swap takes $\pi/(2g)$.
6. $1/\kappa\approx31.8$ ns and $2/\kappa\approx63.7$ ns. Fidelity depends
   nonlinearly on overlap, noise, priors, decay, and the discriminator.
7. 25 ns. No: residual population error and phase error can remain even when
   leakage is tiny. Test all input states or the full channel.
8. A local Z correction is diagonal within the computational basis; it cannot
   reverse population transfer between basis states or recover lost population.
9. 24 us. Echo rejects slow phase noise; it does not reverse irreversible relaxation.
10. Each attenuator replaces absorbed photons with its own thermal emission.
11. $r=(1-p)/2=0.01$. Identical depolarizing channels commute with unitary gates;
    each sequence has survival $1/2+p^{m+1}/2$. The lab uses probabilities,
    not finite-shot samples.
12. $3p^2-2p^3=2.98\times10^{-4}$. Zero failures only bounds the rate:
    approximately $3/N=1.5\times10^{-6}$ at 95% confidence.

</details>

## Capstone: design, then challenge your model

Choose target $f_{01}=5$ GHz and $\alpha/2\pi=-250$ MHz. Infer initial $E_C,E_J$
from the leading formulas and use lab 09 to quantify their error. Choose a
7 GHz cavity with $g/2\pi=100$ MHz; calculate signed $\chi$, the two-level
$n_{\rm crit}$ scale, and unfiltered Purcell lifetime for $\kappa/2\pi=2$ MHz.
Use labs 04 and 12 to explain why pointer separation alone cannot predict
single-shot fidelity. Finish with a one-page table of assumptions, numerical
checks, and the additional models you would need before designing hardware.

[Chapter index](README.md) · [Run all numerical checks](../hands-on/README.md)
