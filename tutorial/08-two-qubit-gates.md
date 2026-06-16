# 08 · Two-Qubit Gates

Single-qubit gates are "easy": drive one qubit with a shaped microwave pulse and you can rotate it anywhere on the Bloch sphere. But a quantum computer needs qubits to *talk* to each other. To create entanglement you need a gate whose action on one qubit depends on the state of another, and that requires a physical interaction between them. Engineering that interaction, turning it on cleanly, and turning it *off* again, is where most of the hard work in superconducting hardware lives. This chapter is about how we get two transmons to interact on purpose.

A theme that runs through everything below: **the same coupling $g$ that lets you build a gate also produces an always-on error.** The avoided crossing that powers the CZ gate is the *same* matrix element that dephases your idle qubits via residual $ZZ$. Different two-qubit gates are mostly different answers to one question, *which* resonance do I bring into play, and *when*?

## Coupling: where $g$ comes from

The simplest way to couple two transmons is to wire them together with a capacitor $C_g$. The shared capacitance produces an electrostatic energy proportional to the *product* of the two charges, $H_c \propto C_g\,V_1 V_2 \propto \hat n_1 \hat n_2$, a charge-charge interaction. Let us turn that into the familiar exchange term, one step at a time.

1. **Start from the charge coupling.** Each transmon is an anharmonic LC mode. Its charge operator in raising/lowering form is $\hat n_i \propto i(a_i^\dagger - a_i)$, with a zero-point amplitude $\propto \sqrt{\omega_i}$. So $\hat n_1 \hat n_2 \propto -(a_1^\dagger - a_1)(a_2^\dagger - a_2)$.
2. **Expand the product.** This gives four terms: $a_1^\dagger a_2$ and $a_1 a_2^\dagger$ (excitation-conserving), plus $a_1^\dagger a_2^\dagger$ and $a_1 a_2$ (excitation non-conserving).
3. **Rotating-wave approximation.** For near-resonant qubits the non-conserving terms oscillate at $\omega_1+\omega_2$ and average to zero, leaving the number-conserving $a_1^\dagger a_2 + a_1 a_2^\dagger$.
4. **Project onto two levels.** Replace $a_i \to \sigma_-^{(i)}$, $a_i^\dagger \to \sigma_+^{(i)}$:

$$H_\text{int} = g\left(\sigma_+^{(1)}\sigma_-^{(2)} + \sigma_-^{(1)}\sigma_+^{(2)}\right), \qquad g \approx \tfrac{1}{2}\,\frac{C_g}{\sqrt{C_1 C_2}}\sqrt{\omega_1 \omega_2}.$$

This is the **exchange** (or "flip-flop") interaction: qubit 1 hands an excitation to qubit 2 and vice versa. The boxed formula matters because it says $g$ is **not a free parameter**, it is set by geometry ($C_g$ relative to the qubit capacitances) and by the frequencies. This is the same Jaynes-Cummings physics as the qubit-resonator $g$ from earlier chapters; here the "cavity" is just a second qubit.

> **Intuition.** Two pendulums on a shared springy beam swap their swinging, that is exchange coupling. The stiffer the shared spring ($C_g$), the faster they trade energy.

The catch: direct capacitive coupling is *always on*. You engineer gates around an interaction you cannot switch off, typically by parking qubits at different frequencies (detuning them) so exchange is suppressed, then acting only when you want a gate.

## Two regimes: resonant vs. dispersive

Let $\Delta = \omega_1 - \omega_2$ be the qubit-qubit detuning. The exchange term behaves completely differently depending on $\Delta$ versus $g$:

- **Resonant ($|\Delta| \lesssim g$):** energy is exchanged on resonance, excitations swap. This is the iSWAP regime (and, at the $|11\rangle$-$|02\rangle$ resonance, the CZ regime).
- **Dispersive ($|\Delta| \gg g$):** direct energy exchange is suppressed; coupling acts only at second order through *virtual* excitations. What survives is a static **residual $ZZ$ shift**, a conditional phase that accrues even while you do nothing.

## Residual $ZZ$, the gate resource *and* the dominant idle error

The residual $ZZ$ is the conditional frequency shift on $|11\rangle$: how much qubit 1's frequency moves depending on whether qubit 2 is excited.

$$\zeta_{ZZ} = (E_{11}-E_{10}) - (E_{01}-E_{00}) \approx \frac{2g^2(\alpha_1+\alpha_2)}{(\Delta-\alpha_2)(\Delta+\alpha_1)}.$$

Derivation in words:

1. **Define the conditional part.** $\zeta$ is the energy of $|11\rangle$ *beyond* the sum of the single-excitation energies, the part not explained by single-qubit physics.
2. **Second-order repulsion.** $|11\rangle$ is pushed by the exchange interaction toward $|02\rangle$ and $|20\rangle$, with matrix element $\sqrt 2\,g$ each (the $\sqrt 2$ is the bosonic $\langle 2|a^\dagger|1\rangle$ enhancement). The singly-excited states $|01\rangle,|10\rangle$ have no such partner.
3. **Energy denominators.** Including anharmonicity, $|02\rangle$ sits at detuning $\Delta-\alpha_2$ and $|20\rangle$ at $\Delta+\alpha_1$ relative to $|11\rangle$ (each doubly-excited state carries its own qubit's anharmonicity). The repulsion is $(\sqrt 2 g)^2/$(denominator).
4. **Combine.** Adding the $|02\rangle$ and $|20\rangle$ contributions gives the compact form with $(\alpha_1+\alpha_2)$ on top.
5. **The crucial limit.** As $\alpha \to \infty$ (ideal two-level systems), $\zeta \to 0$. **$ZZ$ is a transmon effect**, it exists precisely *because* transmons are weakly anharmonic. Anharmonicity is essential, not incidental.

This single quantity is both the **resource for the CZ gate** and the **dominant always-on error** (idle crosstalk, correlated dephasing). The chapter's central reframing: idle $ZZ$ and the CZ conditional phase are the *same matrix element*, one accruing when you don't want it, the other deliberately integrated to $\pi$.

## The CZ gate via the $|11\rangle$-$|02\rangle$ avoided crossing

Tune the qubits so $|11\rangle$ and $|02\rangle$ become nearly degenerate. The $\{|11\rangle,|02\rangle\}$ block, coupled by $\sqrt 2\,g$, diagonalizes into an **avoided crossing** with minimum gap

$$\Delta_\text{gap} = 2\sqrt 2\, g \quad\text{at resonance.}$$

(Note the $2\sqrt 2$, not $2g$: the $\sqrt 2$ is the $1\to 2$ bosonic matrix element, easy to drop.)

```
 E                          |11⟩ (diabatic, rising)
 │        ╲                 ╱
 │         ╲      ___      ╱   ← upper branch (solid)
 │          ╲    /   \    ╱
 │           ╲  / gap  \  /        gap = 2√2 g
 │            ╲/ 2√2 g  \/
 │            /\        /\
 │           /  \  ___ /  ╲   ← lower branch (solid)
 │          ╱    ‾‾‾‾    ╲
 │     |02⟩ (diabatic, falling)
 │
 │ ───────────────────────────  |10⟩  (flat reference, unaffected)
 │ ───────────────────────────  |01⟩  (flat reference, unaffected)
 │ ───────────────────────────  |00⟩  (flat reference, unaffected)
 └─────────────────────────────────────► control flux / detuning
   trajectory: park → approach crossing → return
   shaded area swept by |11⟩ branch  =  ∫ζ dt  =  π
```

Now bring the qubits adiabatically toward the crossing and back. Along the path $|11\rangle$ is pushed *down* by the conditional shift $\zeta_{ZZ}(t)$ while $|00\rangle,|01\rangle,|10\rangle$ are not. The accumulated **conditional phase** is the time integral of that shift, and the gate condition is

$$\phi_{ZZ} = \int \zeta_{ZZ}(t)\,dt \;\stackrel{!}{=}\; \pi.$$

It is essential to define the gate phase as the *conditional* phase, not a vague "extra phase." Only the part of $|11\rangle$'s phase **not** explained by single-qubit phases counts:

$$\phi_{11} = \phi_\text{actual} - \phi_{01} - \phi_{10} + \phi_{00} = \pi \;\Rightarrow\; |11\rangle \to -|11\rangle,$$

with the other three computational states untouched. That conditional sign flip *is* a controlled-Z, $\text{CZ}=\mathrm{diag}(1,1,1,-1)$.

**The central tradeoff.** Going fast risks Landau-Zener leakage into $|02\rangle$. The sweep must stay slow relative to the gap, roughly $|d\varepsilon/dt| \ll \Delta_\text{gap}^2/\hbar$. Faster gates need larger $g$, but larger $g$ also raises leakage risk. The fix is not raw speed but a **shaped trajectory** (the "fast-adiabatic"/Martinis-style pulse, DRAG-like derivative shaping). Two ways to run CZ in practice: (a) adiabatic flux tuning into the crossing, and (b) diabatic/resonant and modern tunable-coupler "net-zero" approaches.

### Worked example, adiabatic CZ (all numbers illustrative)

Two flux-tunable transmons, $g/2\pi = 12$ MHz, $\alpha/2\pi = -300$ MHz each, $T_1=T_2=80\,\mu$s.

| Step | Quantity | Estimate |
|---|---|---|
| 1, avoided-crossing gap | $\Delta_\text{gap}/2\pi = 2\sqrt 2\,g/2\pi$ | $2(1.414)(12) \approx 34$ MHz |
| 2, conditional shift at dwell | $\zeta/2\pi \approx (\sqrt 2 g)^2/\delta$, $\delta/2\pi=50$ MHz | $(16.97)^2/50 \approx 5.8$ MHz |
| 3, gate time for $\pi$ phase | $t_\text{gate}\approx 1/(2\,\zeta_\text{Hz})$ | $1/(2\cdot 5.8\times10^6) \approx 86$ ns |
| 4, leakage (Landau-Zener) | $P_\text{LZ}\sim e^{-2\pi \Delta_\text{gap}^2/(4|d\varepsilon/dt|)}$ | $<10^{-3}$ *only if shaped* |
| 5, decoherence floor | $\varepsilon_\text{dec}\sim t_\text{gate}(1/T_1+1/T_2)\cdot O(1)$ | $86\text{e-}9\cdot 25000\cdot 0.5 \approx 1.1\times10^{-3}$ |

**Takeaway:** the *same* $g$ sets the gap (1), the conditional shift that powers the gate (2), the gate time (3), and the leakage risk (4); and coherence (5) puts a hard $\sim10^{-3}$ floor under all of it. That is why two-qubit gates dominate the error budget and sit near the surface-code threshold.

## Tunable couplers, making $g$ switchable

Insert a third element (a tunable transmon/SQUID) between the qubits. Now there are **two coupling paths**, direct, and indirect via a virtual coupler excitation, that *interfere*:

$$g_\text{eff} = g_\text{direct} + \frac{g_1 g_2}{2}\!\left(\frac{1}{\Delta_1} + \frac{1}{\Delta_2}\right).$$

The indirect term's *sign* is set by the coupler frequency (via $\Delta_1,\Delta_2$, the qubit-coupler detunings), so flux-tuning the coupler can make the two paths cancel.

```mermaid
graph LR
  Q1 -- "g_direct" --> Q2
  Q1 -- "g1" --> C[Coupler]
  C -- "g2" --> Q2
  subgraph ops [operating points]
    OFF["flux A: g_eff = g_direct + g_indirect = 0"]
    ON["flux B: g_eff large (gate on)"]
  end
  note["indirect path g1·g2·(1/Δ1+1/Δ2)/2<br/>tunable sign via coupler freq<br/>→ cancels direct path at OFF"]
```

Crucially, $g_\text{eff}=0$ and $\zeta_{ZZ}=0$ occur at generally *different but engineerable* flux points. The real design problem is making **both** small at the operating point, a high on/off ratio with low idle crosstalk. (A common misconception: the coupler does *not* null $g_\text{eff}$ everywhere, and the $ZZ$ null is nearby but not identical.)

## Cross-resonance: all-microwave entanglement

Tunable approaches need flux lines. The **cross-resonance (CR)** gate avoids them: keep two *fixed-frequency* qubits statically coupled (strength $J$), and drive the **control** qubit at the **target's** frequency. The static coupling transmits a weak resonant tone to the target whose sign depends on the control's state, a $ZX$ interaction:

$$H_\text{CR} \approx \underbrace{\frac{J\,\Omega}{\Delta}\!\left(\frac{\alpha}{\alpha+\Delta}\right)}_{\mu_{ZX}}\frac{ZX}{2} \;+\; \nu\, IX \;+\;\text{(IY, ZI, ZZ terms)}.$$

Derivation sketch: drive the control off-resonantly; it barely moves, but the dispersive coupling makes the target see a control-state-dependent X drive. Schrieffer-Wolff expansion in $J/\Delta$ and $\Omega/\Delta$ gives the leading $ZX$ rate $\propto J\Omega/\Delta$, and the control's third level adds the $\alpha/(\alpha+\Delta)$ factor (which can dominate and even flip the sign of $ZX$).

The raw gate is **not** a clean $ZX$, calibration must remove spurious terms:

| Term | Origin | Useful? | How handled |
|---|---|---|---|
| $ZX$ | conditioned drive via coupling $J$ | **yes** (entangling) | keep, calibrate to $\pi/2$ |
| $IX$ | classical crosstalk / direct bleed | no | cancel with target tone or echo |
| $ZI/IZ$ | Stark shifts | no | frame change / calibration |
| $ZZ$ | higher levels | no | echo / tunable detuning |

**Echoed-CR**: insert a control $\pi$-pulse and flip the drive phase halfway. $ZX$ (odd in control $Z$) survives while $IX,ZI$ (even) cancel, leaving a clean $ZX(\pi/2)\equiv$ CNOT up to single-qubit rotations. Because the rate is $\propto J\Omega/\Delta$ with all factors small, CR is intrinsically **slower** (hundreds of ns). And the $\alpha/(\alpha+\Delta)$ structure means certain frequency combinations kill or blow up the rate, the **frequency-collision** problem that makes fixed-frequency CR processors demand careful frequency targeting.

## The iSWAP family

Instead of routing through $|02\rangle$, bring $|01\rangle$ and $|10\rangle$ onto resonance ($\Delta=0$). Now the exchange acts within the degenerate single-excitation subspace, where $H_\text{int}=g\,\sigma_x$ (with $|01\rangle,|10\rangle$ as the basis), a Rabi-like rotation:

$$U_\text{exch}(t)=\exp\!\big[+i g t\,(\sigma_+^{(1)}\sigma_-^{(2)}+\text{h.c.})\big],\quad |01\rangle \to \cos(gt)\,|01\rangle + i\sin(gt)\,|10\rangle.$$

The only knob is dwell time $\theta = gt$:

```
 pop │  |01⟩ = cos²gt        |10⟩ = sin²gt
 1.0 │●╲              ╱‾‾╲              ╱
     │  ╲           ╱      ╲          ╱
 0.5 │   ╲╳        ╱        ╲╳       ╱
     │   ╱  ╲    ╱   |   ╲   ╱  ╲   ╱
 0.0 │  ╱     ‾‾‾    |    ‾‾‾     ‾‾
     └──────────────┼───────────────► t
              gt=π/4 │   gt=π/2
            √iSWAP    iSWAP
        (max entangling)  (full swap, +i phase)
```

- $gt=\pi/2$: full swap, $\;\text{iSWAP}: |01\rangle\to i|10\rangle,\;|10\rangle\to i|01\rangle$.
- $gt=\pi/4$: $\sqrt{\text{iSWAP}}$, maximally entangling, a common native gate on tunable-coupler chips.

This is the **same** $g$ as the CZ avoided crossing. iSWAP and CZ are two corners of one physics, iSWAP uses the $|01\rangle$-$|10\rangle$ resonance, CZ uses $|11\rangle$-$|02\rangle$, and the **fSim** (fermionic-simulation) family continuously interpolates swap angle $\theta$ and conditional phase $\phi$ on tunable-coupler hardware.

## Why entangling gates are the hard part

Frame the two-qubit error as a sum of channels, $\varepsilon_\text{2Q}\approx \varepsilon_\text{coh}+\varepsilon_\text{leak}+\varepsilon_\text{dec}$, with the decoherence floor scaling as

$$\varepsilon_\text{dec}\sim \frac{t_\text{gate}}{3}\!\left(\frac{1}{T_1}+\frac{1}{T_\phi}\right)\times O(1).$$

| Error channel | Scaling | Illustrative size | Mitigation |
|---|---|---|---|
| Decoherence | $t_\text{gate}(1/T_1+1/T_2)$ | $\sim 1\text{–}3\times10^{-3}$ | shorter gates, better $T_1/T_2$ |
| Leakage to $|02\rangle$ | adiabaticity | $\sim 10^{-4}\text{–}10^{-3}$ | fast-adiabatic / DRAG pulses |
| Residual $ZZ$ | $\zeta\cdot t_\text{gate}$ | variable | tunable coupler / echo |
| Coherent miscalibration |, | $\sim 10^{-4}$ | interleaved RB tune-up |

*(All numbers illustrative and hardware-dependent.)* Because $t_\text{gate}$ (tens of ns) is a non-negligible fraction of $T_1,T_2$ (tens-to-hundreds of $\mu$s), the decoherence floor alone is already $\sim10^{-3}$, which is why two-qubit errors dominate the budget and set the QEC threshold.

**How is the error actually measured?** The quoted $\sim$0.1-1% comes from **interleaved randomized benchmarking (RB)**: run random sequences of Clifford gates with and without the target two-qubit gate interleaved, fit the decay of survival probability versus sequence length, and divide out, isolating the gate's average error from state-prep and measurement errors.

## Mechanism comparison

| Gate | Native interaction | Tunable elements | What you sweep/drive | Speed (illustrative) | Main error channel | Platform |
|---|---|---|---|---|---|---|
| CZ (avoided crossing) | $ZZ$ / $|11\rangle$-$|02\rangle$ | flux on qubit/coupler | frequency into crossing | fast (tens of ns) | leakage to $|02\rangle$ | flux-tunable transmons |
| iSWAP / $\sqrt{\text{iSWAP}}$ | exchange | resonant tuning / coupler | $|01\rangle$-$|10\rangle$ resonant | fast | residual $ZZ$ | tunable-coupler chips |
| Cross-resonance | $ZX$ | none (fixed freq) | $\mu$wave on control@target | slower (hundreds of ns) | spurious $IX/ZZ$, collisions | fixed-frequency transmons |

## Common pitfalls

- **"$ZZ$ crosstalk and the CZ interaction are different things."** They are the *same* $|11\rangle$-$|02\rangle$ matrix element. CZ integrates the conditional shift to $\pi$ on purpose; idle $ZZ$ is the same shift accruing when you don't want it.
- **"Two-level qubits would also have $ZZ$ / a CZ gate."** No, both vanish as $\alpha\to\infty$. They are consequences of the transmon's weak anharmonicity.
- **"The avoided-crossing gap is $2g$."** It is $2\sqrt 2\,g$; the $\sqrt 2$ is the $\langle 2|a^\dagger|1\rangle$ bosonic factor.
- **"Cross-resonance gives a clean $ZX$."** Raw CR also produces $IX$, $ZI/IZ$, and $ZZ$; a usable CNOT needs an echo and calibration.
- **"Faster is always better."** Speed fights adiabaticity, go too fast and you leak into $|02\rangle$. The optimum is a *shaped* trajectory.
- **"A tunable coupler turns $g$ fully off everywhere."** It nulls transverse $g_\text{eff}$ at one flux; the residual-$ZZ$ null is nearby but not identical.

## Key takeaways

- Entanglement requires a real physical interaction; **capacitive coupling** gives an always-on exchange $g(\sigma_+\sigma_-+\sigma_-\sigma_+)$, with $g$ fixed by geometry and frequencies, not a free knob.
- **Residual $ZZ$** is second order in $g$, requires anharmonicity, and is *both* the CZ resource and the dominant idle error.
- The **CZ gate** integrates the conditional phase $\phi_{11}=\phi_\text{actual}-\phi_{01}-\phi_{10}+\phi_{00}=\pi$ at the $|11\rangle$-$|02\rangle$ crossing (gap $2\sqrt 2\,g$); speed fights leakage, so trajectories are shaped.
- **Tunable couplers** cancel direct + indirect paths to null $g_\text{eff}$ (and, separately, $ZZ$).
- **Cross-resonance** entangles fixed-frequency qubits via a $ZX$ term ($\propto J\Omega/\Delta$) but needs echoing and frequency-collision avoidance; **iSWAP/$\sqrt{\text{iSWAP}}$** and CZ are two corners of one exchange physics, unified by the fSim family.
- Two-qubit gates dominate the error budget; their rates are measured by **interleaved RB**.

## Go deeper

- DiCarlo et al., "Demonstration of two-qubit algorithms with a superconducting quantum processor," *Nature* (2009), the adiabatic CZ via $|11\rangle$-$|02\rangle$ ([arXiv:0903.2030](https://arxiv.org/abs/0903.2030)).
- Yan et al., "A Tunable Coupling Scheme for Implementing High-Fidelity Two-Qubit Gates," *Phys. Rev. Applied* (2018) ([arXiv:1803.09813](https://arxiv.org/abs/1803.09813)), direct+indirect path cancellation, simultaneous $g_\text{eff}$/$ZZ$ nulling.
- Magesan & Gambetta, "Effective Hamiltonian models of the cross-resonance gate," *Phys. Rev. A* (2020) ([arXiv:1804.04073](https://arxiv.org/abs/1804.04073)), the $ZX/IX/ZZ$ decomposition and $J\Omega/\Delta\cdot\alpha/(\alpha+\Delta)$ scaling.
- Krantz et al., "A Quantum Engineer's Guide to Superconducting Qubits," *Appl. Phys. Rev.* (2019) ([arXiv:1904.06560](https://arxiv.org/abs/1904.06560)), the lumped-element $g$, the CZ crossing, CR, iSWAP, and the error budget.
- Blais, Grimsmo, Girvin, Wallraff, "Circuit Quantum Electrodynamics," *Rev. Mod. Phys.* (2021) ([arXiv:2005.12667](https://arxiv.org/abs/2005.12667)), rigorous coupling-Hamiltonian, dispersive-shift, and $ZZ$ derivations.

---

Back to [project README](../README.md) · [Tutorial index](./README.md)
