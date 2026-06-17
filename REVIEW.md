# Review of Tutorials 01-12

Scope: this audit covers `tutorial/01-introduction.md` through `tutorial/12-error-correction.md`, plus the paired hands-on examples in `hands-on/01-bloch-sphere/`, `hands-on/02-rabi/`, `hands-on/03-t1-t2/`, and `hands-on/04-dispersive-readout/`. The tutorials are Markdown theory chapters; executable examples are standalone Python scripts using NumPy, Matplotlib, SciPy, and QuTiP.

Primary references used for cross-checks:

- Koch et al., "Charge-insensitive qubit design derived from the Cooper pair box," Phys. Rev. A 76, 042319 (2007), https://arxiv.org/abs/cond-mat/0703002.
- Blais, Grimsmo, Girvin, Wallraff, "Circuit Quantum Electrodynamics," Rev. Mod. Phys. 93, 025005 (2021), https://arxiv.org/abs/2005.12667.
- Krantz et al., "A Quantum Engineer's Guide to Superconducting Qubits," Appl. Phys. Rev. 6, 021318 (2019), https://arxiv.org/abs/1904.06560.
- Vool and Devoret, "Introduction to Quantum Electromagnetic Circuits," Int. J. Circ. Theor. Appl. 45, 897 (2017), https://arxiv.org/abs/1610.03438.
- Gambetta et al., "Qubit-photon interactions in a cavity: Measurement induced dephasing and number splitting," Phys. Rev. A 74, 042318 (2006), https://arxiv.org/abs/cond-mat/0602322.
- McKay et al., "Efficient Z-Gates for Quantum Computing," Phys. Rev. A 96, 022330 (2017), https://arxiv.org/abs/1612.00858.
- Motzoi et al., "Simple Pulses for Elimination of Leakage in Weakly Nonlinear Qubits," Phys. Rev. Lett. 103, 110501 (2009), https://arxiv.org/abs/0901.0534.
- Bylander et al., "Dynamical decoupling and noise spectroscopy with a superconducting flux qubit," Nat. Phys. 7, 565 (2011), https://arxiv.org/abs/1101.4707.
- Krinner et al., "Engineering cryogenic setups for 100-qubit scale superconducting circuit systems," EPJ Quantum Technol. 6, 2 (2019), https://arxiv.org/abs/1806.07862.
- Magesan, Gambetta, and Emerson, "Robust randomized benchmarking of quantum processes," Phys. Rev. Lett. 106, 180504 (2011), https://arxiv.org/abs/1009.3639.
- Magesan et al., "Efficient measurement of quantum gate error by interleaved randomized benchmarking," Phys. Rev. Lett. 109, 080505 (2012), https://arxiv.org/abs/1203.4550.
- Wood and Gambetta, "Quantification and Characterization of Leakage Errors," Phys. Rev. A 97, 032306 (2018), https://arxiv.org/abs/1704.03081.
- Fowler et al., "Surface codes: Towards practical large-scale quantum computation," Phys. Rev. A 86, 032324 (2012), https://arxiv.org/abs/1208.0928.
- Dennis et al., "Topological quantum memory," J. Math. Phys. 43, 4452 (2002), https://arxiv.org/abs/quant-ph/0110143.
- Gottesman, "Stabilizer Codes and Quantum Error Correction," PhD thesis (1997), https://arxiv.org/abs/quant-ph/9705052.
- Acharya et al., "Quantum error correction below the surface code threshold," Nature 638, 920 (2025), https://arxiv.org/abs/2408.13687.

## Blockers

1. **Blocker - Tutorial 06 sign convention corrupts the JC/SW derivation and lab Hamiltonian.**
   `tutorial/06-readout.md:12,17,28,31,38,44,62-63,191,236`; `hands-on/04-dispersive-readout/README.md:35-37`; `hands-on/04-dispersive-readout/dispersive.py:7-10,63-66,98-102`.

   The chapter declares `sigma_z = |0><0| - |1><1|` with `|0>` ground, but then uses the standard `+ omega_q sigma_z/2` Hamiltonian and `+ chi sigma_z a^\dagger a` dispersive term. Those signs belong to the opposite convention, `sigma_z = |e><e| - |g><g|`. With the declared convention, the physical qubit Hamiltonian is `- omega_q Z/2` and the cross-Kerr term is `- chi Z a^\dagger a`.

   This is not cosmetic. With `Z|0> = +|0>`, the existing `+omega_q Z/2` places `|0>` above `|1>`. The Schrieffer-Wolff generator written in the chapter therefore has the wrong sign for canceling the coupling under the stated convention. The lab inherits the same sign in its Hamiltonian, so it teaches the wrong mapping between qubit state and cavity pull, even though the IQ separation magnitude happens to be unchanged.

No additional Blocker-severity issues were found in Tutorials 07-12. The 07-12 audit did find multiple Major issues, especially sign conventions in single-qubit control, ZZ/CZ/iSWAP sign conventions, noise-axis terminology, filter-function/PSD conventions, cryogenic attenuation accounting, RB leakage assumptions, and surface-code distance/qubit-count language.

## Tutorial 01 - Introduction

### 1. Major - Angular-frequency and energy conventions are mixed

File/lines: `tutorial/01-introduction.md:44,46,57,92,104,122-125,194`.

What is wrong: `alpha` is defined as a frequency difference, `omega_12 - omega_01`, but later written as an energy, `alpha approx -E_C`. The diagram also adds `2 alpha` directly to `hbar omega_01`.

Why it is wrong: If `alpha` is angular frequency, perturbation theory gives

```text
omega_01 ~= (sqrt(8 E_J E_C) - E_C) / hbar
alpha = omega_12 - omega_01 ~= -E_C / hbar
```

If ordinary GHz frequencies are being quoted, then `f_01 ~= (sqrt(8 E_J E_C) - E_C)/h` and `alpha/2pi ~= -E_C/h`.

Proposed fix:

```diff
--- a/tutorial/01-introduction.md
+++ b/tutorial/01-introduction.md
@@
-        [energy gap] hbar omega_01 + 2 alpha
+        [energy gap] hbar (omega_01 + 2 alpha)
@@
-        [energy gap] hbar omega_01 + alpha   (smaller, alpha<0)
+        [energy gap] hbar (omega_01 + alpha)   (smaller, alpha<0)
@@
-  R -->|">> 1"| TR["Transmon:<br/>weak anharmonicity<br/>alpha ~ -E_C"]
+  R -->|">> 1"| TR["Transmon:<br/>weak anharmonicity<br/>alpha/2pi ~ -E_C/h"]
@@
-$$\boxed{\;\hbar\omega_q \approx \sqrt{8E_JE_C} - E_C, \qquad \alpha \approx -E_C.\;}$$
+$$\boxed{\;\omega_{01} \approx \frac{\sqrt{8E_JE_C}-E_C}{\hbar}, \qquad \alpha \equiv \omega_{12}-\omega_{01} \approx -\frac{E_C}{\hbar}.\;}$$
@@
-> 1. **$E_C$ from $\alpha$.** Since $\alpha \approx -E_C/h$, we need $E_C/h = 300$ MHz.
+> 1. **$E_C$ from $\alpha$.** Since $\alpha/2\pi \approx -E_C/h$, we need $E_C/h = 300$ MHz.
@@
-- The transmon won because charge dispersion dies *exponentially* in $\sqrt{8E_J/E_C}$ while anharmonicity only weakens as a power law: $\hbar\omega_q\approx\sqrt{8E_JE_C}-E_C$, $\alpha\approx-E_C$.
+- The transmon won because charge dispersion dies *exponentially* in $\sqrt{8E_J/E_C}$ while anharmonicity only weakens as a power law: $\omega_{01}\approx(\sqrt{8E_JE_C}-E_C)/\hbar$, $\alpha\approx-E_C/\hbar$.
```

### 2. Major - Charge-dispersion check drops the Koch prefactor

File/lines: `tutorial/01-introduction.md:128,131`.

What is wrong: The worked example estimates charge dispersion as only `e^{-17.7} ~= 2e-8` of `E_C`. That ignores the algebraic prefactor in the Koch asymptotic expression already printed in the chapter.

Why it is wrong: For `E_J/E_C = 39`, Koch's asymptotic formula gives approximately `epsilon_0/E_C ~= 5e-6` and `epsilon_1/E_C ~= -3.5e-4`. With `E_C/h = 300 MHz`, the `0->1` transition wobble is therefore order `1e5 Hz`, not `2e-8 E_C`. It is still small relative to 5 GHz, but the stated calculation is wrong by orders of magnitude.

Proposed fix:

```diff
--- a/tutorial/01-introduction.md
+++ b/tutorial/01-introduction.md
@@
-> 6. **Charge-noise check.** $\epsilon \sim e^{-\sqrt{8\cdot39}} = e^{-17.7}\approx 2\times10^{-8}$ of $E_C$, utterly negligible.
+> 6. **Charge-noise check.** The exponential alone is $e^{-\sqrt{8\cdot39}}\approx2\times10^{-8}$, but Koch's prefactor matters. The same asymptotic formula gives $\epsilon_0/E_C\sim5\times10^{-6}$ and $\epsilon_1/E_C\sim-3.5\times10^{-4}$, so the $0\to1$ charge dispersion is of order $10^5$ Hz for $E_C/h=300$ MHz: small next to a 5 GHz qubit, but not the bare exponential by itself.
@@
-> **Takeaway:** two target numbers (frequency, anharmonicity) fix two circuit elements ($C\approx65$ fF, $I_c\approx23$ nA), and the design lands self-consistently deep in the charge-insensitive regime.
+> **Takeaway:** two target numbers (frequency, anharmonicity) fix two circuit elements ($C\approx65$ fF, $I_c\approx23$ nA), and the design lands in the transmon regime with strongly reduced, though not literally exponent-only, charge dispersion.
```

### 3. Major - QND readout is given the wrong reason

File/lines: `tutorial/01-introduction.md:139`.

What is wrong: "You measure the cavity, never the qubit, which is exactly why the measurement is QND" is too strong and gives the wrong criterion.

Why it is wrong: Indirect measurements can be non-QND. Dispersive readout is approximately QND because the effective interaction is proportional to `a^\dagger a sigma_z`, which commutes with the measured qubit observable. Finite `g/Delta`, Purcell decay, high photon number, and measurement-induced transitions spoil ideal QND behavior.

Proposed fix:

```diff
--- a/tutorial/01-introduction.md
+++ b/tutorial/01-introduction.md
@@
-You send a probe tone through a cavity of linewidth $\kappa$ and read which way it shifted, you measure the *cavity*, never the qubit, which is exactly why the measurement is **QND** (quantum non-demolition) and can be repeated.
+You send a probe tone through a cavity of linewidth $\kappa$ and read which way it shifted. In the dispersive approximation the leading interaction is a cross-Kerr term proportional to $a^\dagger a\,\sigma_z$, which commutes with $\sigma_z$; that is why the measurement is approximately **QND** (quantum non-demolition) and can be repeated, so long as Purcell decay, leakage, and measurement-induced transitions remain small.
```

### 4. Minor - Dispersive pull needs convention caveats

File/lines: `tutorial/01-introduction.md:135,137,139,187,195`.

What is wrong: The transmon `chi` formula is standard, but the text does not state that `g`, `Delta`, `alpha`, `chi`, and `kappa` are angular frequencies. Also, writing the resonator frequencies as exactly `omega_r +/- chi` silently absorbs a common Lamb shift into `omega_r`.

Why it is wrong: Second-order perturbation gives a conditioned cavity-frequency separation of `2 chi` under a chosen sign convention; the state labels swap if `chi` is negative. For multilevel transmons, common state-independent shifts are usually hidden inside the dressed definition of `omega_r`.

Proposed fix:

```diff
--- a/tutorial/01-introduction.md
+++ b/tutorial/01-introduction.md
@@
-You measure a transmon without touching it directly. Couple it to a microwave resonator (coupling strength $g$). In the **dispersive limit**, qubit and resonator far detuned, $|g/\Delta|\ll1$ with $\Delta = \omega_q-\omega_r$, a Schrieffer-Wolff transformation of the Jaynes-Cummings Hamiltonian removes the direct photon exchange and leaves a state-dependent cavity pull. For a *two-level* system this would be $\chi_0 = g^2/\Delta$, but a transmon has a $|2\rangle$ state nearby, and including it gives the correct multilevel shift:
+You measure a transmon without touching it directly. Couple it to a microwave resonator (coupling strength $g$). In the **dispersive limit**, qubit and resonator far detuned, $|g/\Delta|\ll1$ with $\Delta = \omega_q-\omega_r$, a Schrieffer-Wolff transformation of the Jaynes-Cummings Hamiltonian removes the direct photon exchange and leaves a state-dependent cavity pull. Here $g,\Delta,\alpha,\chi,\kappa$ are angular-frequency quantities. For a *two-level* system this would be $\chi_0 = g^2/\Delta$, but a transmon has a $|2\rangle$ state nearby, and including it gives the correct multilevel shift:
@@
-The resonator frequency moves to $\omega_r \pm \chi$ depending on whether the qubit is in $|0\rangle$ or $|1\rangle$.
+The two dressed resonator frequencies are separated by $2|\chi|$; after absorbing the common Lamb shift into $\omega_r$, this is often written as $\omega_r\pm\chi$.
```

## Tutorial 02 - The Quantum LC Oscillator

### 1. Major - Anharmonicity is defined in energy units but later used as frequency

File/lines: `tutorial/02-quantum-lc-oscillator.md:157-175`.

What is wrong: The chapter defines `alpha` as `(E_2 - E_1) - (E_1 - E_0)`, an energy, but later uses `alpha/2pi` in MHz and diagram labels such as `omega_01 + alpha`.

Why it is wrong: Since `E_n = hbar omega_q (n + 1/2)`, transition angular frequencies are `omega_{n,n+1} = (E_{n+1} - E_n)/hbar`. Standard superconducting-qubit anharmonicity in MHz is `alpha/2pi`, where `alpha = omega_12 - omega_01`.

Proposed fix:

```diff
--- a/tutorial/02-quantum-lc-oscillator.md
+++ b/tutorial/02-quantum-lc-oscillator.md
@@
-A qubit needs **two** addressable levels, a clean $\{|0\rangle,|1\rangle\}$ subspace we can drive with a pulse at $\omega_q$. But in the LC oscillator every gap is identical, $E_{n+1}-E_n = \hbar\omega_q$, independent of $n$. The **anharmonicity**
+A qubit needs **two** addressable levels, a clean $\{|0\rangle,|1\rangle\}$ subspace we can drive with a pulse at $\omega_q$. But in the LC oscillator every transition frequency is identical, $\omega_{n,n+1}=(E_{n+1}-E_n)/\hbar=\omega_q$, independent of $n$. The **anharmonicity**
 
-$$\alpha \equiv (E_2 - E_1) - (E_1 - E_0) = 0$$
+$$\alpha \equiv \omega_{12}-\omega_{01}
+= \frac{(E_2 - E_1) - (E_1 - E_0)}{\hbar} = 0$$
@@
-     gap hbar omega  (leak!)          omega_01 + 2 alpha  (off-resonant)
+     omega_q (leak!)                  omega_01 + 2 alpha  (off-resonant)
@@
-     gap hbar omega  (leak!)          omega_01 + alpha   (smaller gap)
+     omega_q (leak!)                  omega_01 + alpha   (smaller gap)
@@
-To make a qubit we must *bend the ladder* so $0\to1$ and $1\to2$ sit at different frequencies. For scale, a real transmon deliberately introduces **(illustrative)** $\alpha/2\pi \approx -200$ to $-300~\text{MHz}$, a few percent of $\omega_q$, so the $1\to2$ transition is detuned enough to avoid leakage (Chapter 03).
+To make a qubit we must *bend the ladder* so $0\to1$ and $1\to2$ sit at different frequencies. For scale, a real transmon deliberately introduces **(illustrative)** $\alpha/2\pi \approx -200$ to $-300~\text{MHz}$, a few percent of $f_q=\omega_q/2\pi$, so the $1\to2$ transition is detuned enough to avoid leakage (Chapter 03).
```

### 2. Major - Low-impedance "charge-like" wording is likely inverted

File/lines: `tutorial/02-quantum-lc-oscillator.md:125`.

What is wrong: The text says low-impedance resonators sit on the "charge-like side." This is ambiguous and likely inverted under the usual localization language.

Why it is wrong: With `varphi = 2pi Phi/Phi_0` and `n = Q/(2e)`, one finds `varphi_zpf^2 = pi Z/R_Q` and `n_zpf^2 = R_Q/(4 pi Z)`. Low `Z` gives small phase/flux spread and large charge-number spread, so it is clearer and physically safer to call these modes phase/flux-localized and charge-delocalized.

Proposed fix:

```diff
--- a/tutorial/02-quantum-lc-oscillator.md
+++ b/tutorial/02-quantum-lc-oscillator.md
@@
-Their product *saturates* the Heisenberg bound, the LC vacuum is a minimum-uncertainty state. Notice the role of impedance: a **large $Z$** gives big flux fluctuations and small charge fluctuations (flux-like circuits), and a **small $Z$** does the opposite (charge-like circuits). The benchmark is the resistance quantum $R_Q = h/4e^2 \approx 6.45~\text{k}\Omega$. Typical lab resonators have $Z\sim 50\text{ to }100~\Omega \ll R_Q$, so their *flux* fluctuations are tiny in units of $\Phi_0/2\pi$ (here $\Phi_{\rm zpf}\sim 0.1\text{ to }0.2\,\Phi_0/2\pi$) while their charge fluctuations are comparatively large, such low-impedance circuits sit far on the charge-like side, which is exactly why building a strongly anharmonic qubit takes deliberate engineering.
+Their product *saturates* the Heisenberg bound, the LC vacuum is a minimum-uncertainty state. Notice the role of impedance: a **large $Z$** gives big phase/flux fluctuations and small Cooper-pair-number fluctuations, while a **small $Z$** does the opposite. The benchmark is the resistance quantum $R_Q = h/4e^2 \approx 6.45~\text{k}\Omega$. Typical lab resonators have $Z\sim 50\text{ to }100~\Omega \ll R_Q$, so their *flux* fluctuations are tiny in units of $\Phi_0/2\pi$ (here $\Phi_{\rm zpf}\sim 0.1\text{ to }0.2\,\Phi_0/2\pi$) while their charge-number fluctuations are comparatively large; these low-impedance modes are phase/flux-localized and charge-delocalized.
```

### 3. Minor - Zero-point energy and zero-point variance are conflated

File/lines: `tutorial/02-quantum-lc-oscillator.md:119-127`.

What is wrong: The text says the additive `1/2 hbar omega_q` "is not a bookkeeping offset." For an isolated oscillator, the constant energy offset can be shifted away dynamically; the measurable content here is the ground-state variance.

Why it is wrong: Adding a constant to the Hamiltonian does not change isolated dynamics. The physical fluctuations are encoded in `Phi_zpf` and `Q_zpf`, e.g. `<0|Phi^2|0> = Phi_zpf^2`.

Proposed fix:

```diff
--- a/tutorial/02-quantum-lc-oscillator.md
+++ b/tutorial/02-quantum-lc-oscillator.md
@@
-That $\tfrac12\hbar\omega_q$ is not a bookkeeping offset, it encodes real, measurable fluctuations. On the vacuum $|0\rangle$, only the $\hat a\hat a^\dagger$ term survives, so
+The additive $\tfrac12\hbar\omega_q$ can often be shifted away for an isolated oscillator, but the ground state is not classical: it has real, measurable fluctuations. On the vacuum $|0\rangle$, only the $\hat a\hat a^\dagger$ term survives, so
@@
-> **Pitfall.** "Zero-point energy means nothing happens in the ground state." Wrong: $\Phi_{\rm zpf}$ and $Q_{\rm zpf}$ are genuine fluctuations, and they drive real physics (dispersive shifts, vacuum-induced relaxation, Casimir-like effects). The $\tfrac12$ is physically loaded, not ignorable.
+> **Pitfall.** "Zero-point energy means nothing happens in the ground state." Wrong: $\Phi_{\rm zpf}$ and $Q_{\rm zpf}$ are genuine fluctuations, and they drive real physics (dispersive shifts, vacuum-induced relaxation, Casimir-like effects). The variances are physically loaded even when the constant energy offset is dynamically removable.
```

### 4. Nit - Node-flux and impedance wording overclaim

File/lines: `tutorial/02-quantum-lc-oscillator.md:28,83`.

What is wrong: Node flux is a generalized circuit coordinate defined as a voltage integral, not literally "Faraday's law for the node." A single lumped LC oscillator has an oscillator impedance, not a wave impedance.

Why it is wrong: Vool and Devoret define generalized fluxes as time integrals of voltages and distinguish lumped oscillators from distributed transmission-line modes.

Proposed fix:

```diff
--- a/tutorial/02-quantum-lc-oscillator.md
+++ b/tutorial/02-quantum-lc-oscillator.md
@@
-the time integral of the voltage at the node, so that $V = \dot\Phi$ (this is just Faraday's law for the node). Two short steps build the Lagrangian:
+the time integral of the voltage at the node, so that $V = \dot\Phi$ (the node-flux coordinate; for an inductor branch it coincides with the usual magnetic flux variable). Two short steps build the Lagrangian:
@@
-Because $H$ is quadratic, we diagonalize it with ladder operators. The trick is to rescale $\Phi$ and $Q$ so that both terms in $H$ carry equal weight; the natural scale is the **characteristic (wave) impedance**
+Because $H$ is quadratic, we diagonalize it with ladder operators. The trick is to rescale $\Phi$ and $Q$ so that both terms in $H$ carry equal weight; the natural scale is the **oscillator impedance**
```

## Tutorial 03 - Josephson Junction and Anharmonicity

### 1. Major - Gauge-invariant phase and branch flux are underdefined

File/lines: `tutorial/03-josephson-junction.md:5,25,56,115`.

What is wrong: The chapter calls `varphi = theta_L - theta_R` gauge-invariant, but that expression is only valid in a gauge/path where the vector-potential contribution is negligible. Later it uses `Phi` in the inductive-energy matching without defining `Phi = (Phi_0/2pi) varphi`.

Why it is wrong: The gauge-invariant junction phase is `theta_L - theta_R - (2pi/Phi_0) integral A.dl`, up to orientation convention. The branch flux relation gives `V = dot Phi` and

```text
(1/2) E_J varphi^2 = Phi^2/(2 L_J0)
L_J0 = (Phi_0/2pi)^2/E_J = Phi_0/(2pi I_c).
```

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-Only the **gauge-invariant phase difference** $\varphi = \theta_L - \theta_R$ across the barrier matters, and through it Cooper pairs *tunnel* coherently across the gap.
+Only the **gauge-invariant phase difference**
+$$ \varphi = \theta_L-\theta_R-\frac{2\pi}{\Phi_0}\int_R^L \mathbf A\cdot d\mathbf l $$
+across the barrier matters. In a gauge with negligible vector potential across the barrier this reduces to $\theta_L-\theta_R$, and through it Cooper pairs *tunnel* coherently across the gap.
@@
-Let $\varphi$ be the gauge-invariant phase difference across the junction.
+Let $\varphi$ be the gauge-invariant phase difference across the junction, and define the branch flux $\Phi=(\Phi_0/2\pi)\varphi$ so that $V=\dot\Phi$.
@@
-The $\varphi^2$ term reproduces a harmonic oscillator (matching $\tfrac12 L_{J0}^{-1}\Phi^2$ identifies the linear inductance).
+Using $\Phi=(\Phi_0/2\pi)\varphi$, the $\varphi^2$ term reproduces a harmonic oscillator: $\tfrac12E_J\varphi^2=\Phi^2/(2L_{J0})$, so $L_{J0}=(\Phi_0/2\pi)^2/E_J=\Phi_0/(2\pi I_c)$.
```

### 2. Major - `E_C` uses total island capacitance, not generally junction capacitance

File/lines: `tutorial/03-josephson-junction.md:87,89,91,166`.

What is wrong: The chapter says the charging energy comes from the "junction capacitance." For a CPB/transmon, `E_C = e^2/(2 C_Sigma)`, where `C_Sigma` includes junction, gate, shunt, and network capacitances.

Why it is wrong: The transmon's central move is increasing shunt capacitance to reduce `E_C`. Calling `C` the junction capacitance misidentifies the physical element being designed.

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-Pair the cosine potential with the electrostatic (charging) energy of the junction capacitance. The charge on the island is $Q = 2e(\hat n - n_g)$, so its electrostatic energy $Q^2/2C$ gives the full Hamiltonian:
+Pair the cosine potential with the electrostatic charging energy of the island's effective capacitance $C_\Sigma$ (junction plus gate/shunt/network capacitances). The island charge is $Q = 2e(\hat n - n_g)$, so $Q^2/(2C_\Sigma)$ gives the full Hamiltonian:
@@
-$$ H = 4E_C\,(\hat n - n_g)^2 - E_J\cos\hat\varphi, \qquad E_C = \frac{e^2}{2C}, \qquad [\hat\varphi,\hat n] = i. $$
+$$ H = 4E_C\,(\hat n - n_g)^2 - E_J\cos\hat\varphi, \qquad E_C = \frac{e^2}{2C_\Sigma}, \qquad [\hat\varphi,\hat n] = i. $$
@@
-one full Cooper pair costs $4E_C$
+one full Cooper pair costs $4E_C$ at $n_g=0$
@@
-- Capacitance: $C = e^2/(2E_C) = e^2/(2h\cdot 250\,\text{MHz}) \approx 78\ \text{fF}$
+- Total island capacitance: $C_\Sigma = e^2/(2E_C) = e^2/(2h\cdot 250\,\text{MHz}) \approx 78\ \text{fF}$
```

### 3. Major - Anharmonicity mixes energy, angular frequency, and Hz

File/lines: `tutorial/03-josephson-junction.md:15,130,132,172,176,184,193`.

What is wrong: The chapter defines `alpha = omega_12 - omega_01`, an angular frequency, but then says "absolute anharmonicity is approx -E_C (a few hundred MHz)" and later describes `alpha approx -E_C` "in Hz."

Why it is wrong: Subtracting the perturbative levels gives an energy anharmonicity `alpha_E = E_21 - E_10 ~= -E_C`. The angular-frequency anharmonicity is `alpha_omega = alpha_E/hbar`; the cyclic-frequency value quoted in MHz is `alpha_E/h`.

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-E --> F["Unequal level spacing<br/>alpha approx -E_C"]
+E --> F["Unequal level spacing<br/>E12-E01 approx -E_C"]
@@
-$$ \hbar\omega_q = E_1 - E_0 \simeq \sqrt{8E_J E_C} - E_C, \qquad \alpha \equiv \omega_{12}-\omega_{01} \simeq -\frac{E_C}{\hbar}, \qquad \alpha_r \equiv \frac{\alpha}{\omega_{01}} \simeq -\Big(\frac{8E_J}{E_C}\Big)^{-1/2}. $$
+$$ \hbar\omega_q = E_1 - E_0 \simeq \sqrt{8E_J E_C} - E_C, \qquad \alpha_E \equiv (E_2-E_1)-(E_1-E_0) \simeq -E_C, $$
+$$ \alpha_\omega \equiv \omega_{12}-\omega_{01} = \frac{\alpha_E}{\hbar} \simeq -\frac{E_C}{\hbar}, \qquad \alpha_r \equiv \frac{\alpha_\omega}{\omega_{01}} \simeq -\Big(\frac{8E_J}{E_C}\Big)^{-1/2}. $$
@@
-So the **absolute anharmonicity** is $\approx -E_C$ (a few hundred MHz)
+So the **energy anharmonicity** is $\alpha_E\approx -E_C$; quoted as a cyclic frequency, $\alpha_E/h$ is typically a few hundred MHz
@@
-- **Two anharmonicities.** $\alpha$ (absolute, $\approx -E_C$, in Hz)
+- **Two anharmonicities.** $\alpha_E$ is an energy ($\approx -E_C$), while $\alpha_\omega=\alpha_E/\hbar$ is angular frequency and $\alpha_E/h$ is the value quoted in Hz
```

### 4. Major - LC/Josephson dissipation contrast is misleading

File/lines: `tutorial/03-josephson-junction.md:120,189`.

What is wrong: The table says a linear LC oscillator has "resistive losses," while the Josephson element is "non-dissipative." The tutorial's own setup is a superconducting LC oscillator, whose ideal `L` and `C` are also non-dissipative.

Why it is wrong: The bare LC oscillator fails as a qubit because it is harmonic, not because it is necessarily lossy. The Josephson junction supplies nonlinearity while remaining ideally non-dissipative.

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-| Dissipation | resistive losses | non-dissipative (ideal) |
+| Dissipation | non-dissipative if built from ideal superconducting $L,C$ | non-dissipative in the ideal junction model |
@@
-- The Josephson junction is the unique **nonlinear, non-dissipative** circuit element; without it you only get an unusable harmonic oscillator.
+- The Josephson junction supplies the standard **nonlinear, ideally non-dissipative** circuit element; a bare superconducting LC oscillator can be low-loss, but it remains harmonic and therefore unusable as an addressable qubit.
```

### 5. Minor - Josephson inductance singularity/sign change is imprecise

File/lines: `tutorial/03-josephson-junction.md:42,44`.

What is wrong: The text says `L_J` "diverges and turns negative at varphi = pi/2." It diverges at `pi/2 + k pi` and becomes negative only where `cos varphi < 0`.

Why it is wrong: `L_J = Phi_0/(2 pi I_c cos varphi)`. At the singular point it is undefined; beyond it, negative incremental inductance describes negative curvature, not a stable standalone inductor.

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-here $L_J$ stiffens and softens with $\varphi$, *diverges* and turns *negative* at $\varphi = \pi/2$.
+here $L_J$ stiffens and softens with $\varphi$, *diverges* at $\varphi=\pi/2+k\pi$, and has negative incremental sign where $\cos\varphi<0$.
@@
-Near $\varphi=\pi/2$ it blows up, don't read it as a real component at all phases.
+Near $\varphi=\pi/2+k\pi$ it blows up; where $\cos\varphi<0$ it describes negative curvature of the cosine potential, not a stable standalone inductor.
```

### 6. Minor - Charge-dispersion sign/width and worked numbers need tightening

File/lines: `tutorial/03-josephson-junction.md:138,174,178`.

What is wrong: The text calls `epsilon_m` a peak-to-peak width but includes the signed `(-1)^m` formula. The worked example rounds the `m=1` dispersion too loosely.

Why it is wrong: For `E_J/E_C = 50` and `E_C/h = 250 MHz`, the formula gives `epsilon_0/h ~= 147 Hz`, `|epsilon_1|/h ~= 11.8 kHz`, and transition dispersion `|epsilon_1 - epsilon_0|/h ~= 11.9 kHz`.

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-The peak-to-peak band width as $n_g$ sweeps $0\to1$ is the **charge dispersion** $\epsilon_m$
+Define the signed **charge dispersion** $\epsilon_m \equiv E_m(n_g=1/2)-E_m(n_g=0)$; the peak-to-peak width is $|\epsilon_m|$
@@
-evaluating the formula at $m=1$ gives $\epsilon_1/h \approx 10\ \text{kHz}$, about $70\times$ larger than $\epsilon_0$.
+evaluating the formula at $m=1$ gives $|\epsilon_1|/h \approx 11.8\ \text{kHz}$, about $80\times$ larger than $\epsilon_0$.
@@
-the $0\to1$ frequency wiggles peak-to-peak by $\approx |\epsilon_0|+|\epsilon_1|\approx 10\ \text{kHz}$
+the $0\to1$ frequency wiggles peak-to-peak by $|\epsilon_1-\epsilon_0|/h \approx |\epsilon_0|/h+|\epsilon_1|/h \approx 11.9\ \text{kHz}$
@@
-$0\to1$ charge dispersion $\approx 10\ \text{kHz}$
+$0\to1$ charge dispersion $\approx 12\ \text{kHz}$
```

### 7. Minor - Claim of generated figures is false

File/lines: `tutorial/03-josephson-junction.md:97`.

What is wrong: The text says the tridiagonal matrix is "exactly how the figures below are produced," but the following visuals are schematic ASCII diagrams, not generated numerical plots.

Why it is wrong: This makes the sketches appear numerically sourced and can send readers looking for missing code.

Proposed fix:

```diff
--- a/tutorial/03-josephson-junction.md
+++ b/tutorial/03-josephson-junction.md
@@
-You could type that matrix into NumPy, truncate at $|n|\le 10$, and `eigh` it to get the spectrum, that is exactly how the figures below are produced.
+You could type that matrix into NumPy, truncate at $|n|\le 10$, and use `eigh` to get the spectrum; that is the standard numerical route for plots of the CPB/transmon spectrum. The sketches below are schematic, not generated data.
```

## Tutorial 04 - The Transmon Qubit

### 1. Major - SQUID sweet spot at half flux is misstated

File/lines: `tutorial/04-transmon.md:141-152,169,185`.

What is wrong: The chapter says the symmetric SQUID has zero slope at both `Phi = 0` and `Phi = Phi_0/2`. At half flux, `|cos(pi Phi/Phi_0)|` has a cusp and `E_J,eff -> 0`, so the transmon approximation also fails.

Why it is wrong: For a symmetric SQUID, `E_J,eff = E_J,Sigma |cos x|`, `x = pi Phi/Phi_0`. At `x = pi/2`, the derivative is undefined, not zero. For asymmetric SQUIDs, the smooth expression `E_J,Sigma sqrt(cos^2 x + d^2 sin^2 x)` has a nonzero minimum and can have a smooth extremum at half flux.

Proposed fix:

```diff
--- a/tutorial/04-transmon.md
+++ b/tutorial/04-transmon.md
@@
-$$E_{J,\mathrm{eff}}(\Phi) = E_{J,\Sigma}\,\big|\cos(\pi\Phi/\Phi_0)\big|\,\sqrt{1 + d^2\tan^2(\pi\Phi/\Phi_0)},
+$$E_{J,\mathrm{eff}}(\Phi) = E_{J,\Sigma}\sqrt{\cos^2(\pi\Phi/\Phi_0)+d^2\sin^2(\pi\Phi/\Phi_0)},
 \qquad d=\frac{E_{J2}-E_{J1}}{E_{J1}+E_{J2}},$$
@@
-For the symmetric case $|\cos(\pi\Phi/\Phi_0)|$ has zero slope at $\Phi=0$ and $\Phi=\Phi_0/2$:
+For the symmetric case, the smooth flux sweet spots are at integer flux, $\Phi=k\Phi_0$. At $\Phi=\Phi_0/2$, $|\cos(\pi\Phi/\Phi_0)|$ has a cusp and $E_{J,\mathrm{eff}}=0$, so the transmon approximation no longer applies:
 
-$$\left.\frac{\partial\omega_q}{\partial\Phi}\right|_{\Phi=0}=0.$$
+$$\left.\frac{\partial\omega_q}{\partial\Phi}\right|_{\Phi=k\Phi_0}=0.$$
+
+For $d\neq0$, the nonsingular asymmetric expression also has a smooth extremum at $\Phi=(k+\tfrac12)\Phi_0$.
```

### 2. Major - Energy, angular-frequency, and Hz notation are mixed

File/lines: `tutorial/04-transmon.md:16,80,125,127,144,177,182`.

What is wrong: Line 80 defines `alpha = E_12 - E_01` in energy units, then divides by `omega_01`, a frequency. The worked example also uses `omega_q/2pi` where it is really computing `E_01/h`.

Why it is wrong: The dimensionless relative anharmonicity is either `alpha_E/E_01` or `(omega_12 - omega_01)/omega_01`. The leading energy relation is `hbar omega_01 ~= sqrt(8 E_J E_C) - E_C`.

Proposed fix:

```diff
--- a/tutorial/04-transmon.md
+++ b/tutorial/04-transmon.md
@@
-  A --> I["w_q = sqrt(8 E_J E_C)<br/>- E_C : a few GHz"]
+  A --> I["f_01 = (sqrt(8 E_J E_C)<br/>- E_C)/h : a few GHz"]
@@
-- **Relative anharmonicity.** $\displaystyle \alpha_r \equiv \frac{\alpha}{\omega_{01}} \simeq \frac{-E_C}{\sqrt{8E_JE_C}} = -\sqrt{\frac{E_C}{8E_J}} = -\left(\frac{8E_J}{E_C}\right)^{-1/2}.$
+- **Relative anharmonicity.** $\displaystyle \alpha_r \equiv \frac{\alpha_E}{E_{01}}=\frac{\omega_{12}-\omega_{01}}{\omega_{01}} \simeq \frac{-E_C}{\sqrt{8E_JE_C}} = -\sqrt{\frac{E_C}{8E_J}} = -\left(\frac{8E_J}{E_C}\right)^{-1/2}.$
@@
-Then $\omega_q/2\pi = 5.48 - 0.25 = \mathbf{5.23\ GHz}$
+Then $f_{01}=\omega_{01}/2\pi=E_{01}/h=5.48 - 0.25 = \mathbf{5.23\ GHz}$
@@
-Cross-check: $\alpha/\omega_q = -250/5230 = -4.8\%$
+Cross-check: $(\alpha_E/h)/f_{01} = -250/5230 = -4.8\%$
@@
-into $\omega_q(\Phi)=\sqrt{8E_{J,\mathrm{eff}}(\Phi)E_C}-E_C$
+into $\hbar\omega_{01}(\Phi)\simeq\sqrt{8E_{J,\mathrm{eff}}(\Phi)E_C}-E_C$
```

### 3. Minor - `E_C` should name total capacitance

File/lines: `tutorial/04-transmon.md:27-32`.

What is wrong: The derivation uses `C`, but for a transmon this should be `C_Sigma`, the total capacitance seen by the mode.

Why it is wrong: Koch defines `E_C = e^2/(2 C_Sigma)`, including junction, shunt, and gate capacitances.

Proposed fix:

```diff
--- a/tutorial/04-transmon.md
+++ b/tutorial/04-transmon.md
@@
-The electrostatic energy of an island holding charge $Q$ with gate-induced offset $Q_g$ is $(Q-Q_g)^2/2C$.
+The electrostatic energy of the island mode is $(Q-Q_g)^2/2C_\Sigma$, where $C_\Sigma$ is the total capacitance seen by that mode.
@@
-$$\frac{(2e)^2}{2C}(\hat n - n_g)^2 = \frac{2e^2}{C}(\hat n - n_g)^2 = 4E_C\,(\hat n - n_g)^2,
-\qquad E_C \equiv \frac{e^2}{2C}.$$
+$$\frac{(2e)^2}{2C_\Sigma}(\hat n - n_g)^2 = \frac{2e^2}{C_\Sigma}(\hat n - n_g)^2 = 4E_C\,(\hat n - n_g)^2,
+\qquad E_C \equiv \frac{e^2}{2C_\Sigma}.$$
```

### 4. Minor - "Absolute anharmonicity is fixed" needs parameter context

File/lines: `tutorial/04-transmon.md:104-105,119,133,184`.

What is wrong: The text says absolute anharmonicity is "roughly constant" or "fixed." That is only true at fixed `E_C`.

Why it is wrong: Since `alpha_E ~= -E_C`, raising `E_J/E_C` by adding shunt capacitance lowers `E_C` and therefore lowers `|alpha|`.

Proposed fix:

```diff
--- a/tutorial/04-transmon.md
+++ b/tutorial/04-transmon.md
@@
-- **Absolute** $\alpha\approx -E_C$ is *roughly constant*, it sets a fixed, ns-scale gate-speed limit.
+- **Absolute** $\alpha\approx -E_C$ is set mainly by $E_C$: at fixed $E_C$ it is nearly independent of $E_J$, but designs that lower $E_C$ also lower $|\alpha|$.
@@
-Double the ratio to 120: $\alpha_r$ only improves to $\sim-3.2\%$
+Double the ratio to 120: $\alpha_r$ only shrinks to $\sim-3.2\%$
@@
-- **Absolute** $\alpha\approx-E_C$ (fixed, sets the ns gate-speed limit) differs from **relative** $\alpha_r$ (slowly shrinks).
+- **Absolute** $\alpha\approx-E_C$ (set by the charging energy) differs from **relative** $\alpha_r$ (slowly shrinks with $E_J/E_C$).
```

### 5. Minor - Charge-dispersion example uses ground-level dispersion, not transition dispersion

File/lines: `tutorial/04-transmon.md:131`.

What is wrong: The example says `epsilon_0` is sub-kHz and treats that as the charge-noise check. The measured qubit transition dispersion is dominated by the first excited level.

Why it is wrong: For `E_J/E_C = 60` and `E_C/h = 250 MHz`, Koch's asymptotic expression gives `epsilon_0/h ~= 25 Hz` and `epsilon_1/h ~= -2.19 kHz`, so the transition swing is `|epsilon_1 - epsilon_0|/h ~= 2.2 kHz`.

Proposed fix:

```diff
--- a/tutorial/04-transmon.md
+++ b/tutorial/04-transmon.md
@@
-Even with the algebraic prefactor (tens-to-hundreds for the lowest level), $\epsilon_0$ lands in the sub-kHz range, negligible next to a 5 GHz qubit.
+For the ground level, $\epsilon_0/h\approx25$ Hz. The qubit transition dispersion is dominated by the first excited level; here $|\epsilon_1-\epsilon_0|/h\approx2.2$ kHz, still negligible next to a 5 GHz qubit.
```

## Tutorial 05 - Circuit QED

### 1. Major - `2 chi ~= kappa` is overstated and should use `|chi|`

File/lines: `tutorial/05-circuit-qed.md:145,151,188,214,225`.

What is wrong: The chapter states `2 chi ~= kappa` as a universal optimum and uses signed `2 chi` where the physical peak separation is `2|chi|`.

Why it is wrong: From `H_disp = hbar(omega_r + chi sigma_z)n + ...`, the conditional resonances are separated by `2|chi|`. Actual readout optimization depends on drive frequency, photon budget, integration time, filtering, and measurement-induced transitions. `2|chi| ~ kappa` is a useful engineering scale, not a theorem. Also, resonant strong coupling `g >> kappa,gamma` is distinct from this readout-design comparison.

Proposed fix:

```diff
--- a/tutorial/05-circuit-qed.md
+++ b/tutorial/05-circuit-qed.md
@@
-    R -.->|"QND<br/>target 2chi approx kappa"| AMP
+    R -.->|"QND<br/>use 2|chi| vs kappa"| AMP
@@
-**Readout linewidth and the $2\chi\approx\kappa$ optimum.** The cavity linewidth $\kappa$ sets both how fast information leaves the cavity and its bandwidth. The two qubit-dependent peaks are separated by $2\chi$ and each is $\sim\kappa$ wide. Maximal distinguishability lives near $2\chi\approx\kappa$, a **matching** condition, *not* "make $\chi$ huge." Too large $2\chi/\kappa$ wastes contrast and worsens measurement-induced mixing; too small and the peaks overlap inside one linewidth. The enabling separation of timescales is **strong coupling**, $g\gg\kappa,\gamma$.
+**Readout linewidth and the $2|\chi|/\kappa$ scale.** The cavity linewidth $\kappa$ sets both how fast information leaves the cavity and its bandwidth. The two qubit-dependent resonances are separated by $2|\chi|$ and each has linewidth $\sim\kappa$. A common fast-readout design point is $2|\chi|\sim\kappa$: if $2|\chi|\ll\kappa$, the responses overlap strongly; if $2|\chi|\gg\kappa$, the phase contrast saturates and the optimum depends on drive frequency, allowed photon number, integration time, filtering, and measurement-induced transitions. This is a readout-engineering tradeoff, distinct from resonant strong coupling $g\gg\kappa,\gamma$.
@@
-Here $2\chi<\kappa$: the peaks sit inside one linewidth
+Here $2|\chi|<\kappa$: the peaks sit inside one linewidth
@@
-- **"Bigger $\chi$ is always better."** The target is $2\chi\approx\kappa$, a matching condition, not "maximize."
+- **"Bigger $\chi$ is always better."** Compare $2|\chi|$ with $\kappa$: $2|\chi|\sim\kappa$ is a common design point, but the optimum is measurement-chain and drive dependent.
@@
-- One $g$ does double duty: readout (target $2\chi\approx\kappa$) and a virtual-photon **bus** $J\approx\tfrac{g_1g_2}{2}(1/\Delta_1+1/\Delta_2)$. Tame $\Gamma_\text{Purcell}=\kappa(g/\Delta)^2$ with a Purcell filter.
+- One $g$ does double duty: readout (set by $2|\chi|$ relative to $\kappa$) and a virtual-photon **bus** $J\approx\tfrac{g_1g_2}{2}(1/\Delta_1+1/\Delta_2)$. Tame $\Gamma_\text{Purcell}=\kappa(g/\Delta)^2$ with a Purcell filter.
```

### 2. Minor - QND claim is too absolute

File/lines: `tutorial/05-circuit-qed.md:104`.

What is wrong: The chapter says "the readout is QND, repeatable and projective" without caveats.

Why it is wrong: The effective dispersive Hamiltonian commutes with `sigma_z`, so the ideal model is QND. Real devices have finite `T_1`, Purcell decay, critical-photon-number limits, and measurement-induced transitions.

Proposed fix:

```diff
--- a/tutorial/05-circuit-qed.md
+++ b/tutorial/05-circuit-qed.md
@@
-Crucially $H_\text{disp}$ commutes with $\hat\sigma_z$: measuring the cavity does **not** flip the qubit. The readout is **quantum non-demolition (QND)**, repeatable and projective. SNR grows with photon number and integration time.
+Crucially, within this effective dispersive model, $H_\text{disp}$ commutes with $\hat\sigma_z$: the cavity measurement does not itself drive qubit flips. This is the basis of **quantum non-demolition (QND)** readout, repeatable and projective in the ideal limit. In real devices, finite $T_1$, Purcell decay, critical-photon-number physics, and measurement-induced transitions limit the QND fidelity.
```

### 3. Minor - "No dispersive shift" for a harmonic oscillator is imprecise

File/lines: `tutorial/05-circuit-qed.md:136,211`.

What is wrong: The chapter says a linear oscillator gives "no dispersive shift." Two linearly coupled oscillators can have state-independent normal-mode shifts.

Why it is wrong: What vanishes as `alpha -> 0` is the state-dependent cross-Kerr pull `chi` needed for qubit readout, not every possible frequency renormalization.

Proposed fix:

```diff
--- a/tutorial/05-circuit-qed.md
+++ b/tutorial/05-circuit-qed.md
@@
-- $\alpha\to0$ (a perfectly **harmonic** multilevel mode): the factor $\to0$, so $\chi\to0$. The two contributions **cancel exactly**, a linear oscillator coupled to a cavity gives *no* dispersive shift and **cannot be read out dispersively**. Anharmonicity is what makes readout possible. *This is the single most important correction to the naive formula.*
+- $\alpha\to0$ (a perfectly **harmonic** multilevel mode): the factor $\to0$, so the state-dependent pull $\chi\to0$. The two contributions **cancel exactly**: two linearly coupled oscillators can have state-independent normal-mode shifts, but they have no cross-Kerr / qubit-state-dependent dispersive shift to read out. Anharmonicity is what makes readout possible. *This is the single most important correction to the naive formula.*
@@
-- **"A linear resonator could be read out dispersively too."** No, for a harmonic mode the $|g\rangle\!-\!|e\rangle$ and $|e\rangle\!-\!|f\rangle$ contributions cancel and $\chi=0$. Anharmonicity is essential.
+- **"A linear resonator could be read out dispersively too."** Not as a qubit-state-dependent dispersive readout: for a harmonic mode the adjacent-transition contributions cancel and $\chi=0$, although state-independent normal-mode shifts remain. Anharmonicity is essential.
```

### 4. Nit - `sqrt(n)` wording conflicts with the chapter's indexing

File/lines: `tutorial/05-circuit-qed.md:44`.

What is wrong: The paragraph derives splitting `2g sqrt(n+1)` but then calls it a `sqrt(n)` nonlinearity.

Why it is wrong: Both conventions are common, but the paragraph should not switch indexing midstream. If the block spans `|e,n>` and `|g,n+1>`, the splitting is `2g sqrt(n+1)`. If indexed by total excitation number `N`, it is `2g sqrt(N)`.

Proposed fix:

```diff
--- a/tutorial/05-circuit-qed.md
+++ b/tutorial/05-circuit-qed.md
@@
-The $n=0$ rung splits by $2g$, the **vacuum-Rabi splitting**. Higher rungs split by $2g\sqrt2,\,2g\sqrt3,\dots$: the ladder is **anharmonic in photon number**. That $\sqrt{n}$ nonlinearity is exactly what distinguishes a true two-level emitter from a linear oscillator (which would give an evenly-spaced ladder).
+The $n=0$ rung splits by $2g$, the **vacuum-Rabi splitting**. Higher rungs split by $2g\sqrt2,\,2g\sqrt3,\dots$: the ladder is **anharmonic in photon number**. That $\sqrt{n+1}$ rung dependence, or $\sqrt{N}$ when indexed by total excitation number $N$, is exactly what distinguishes a true two-level emitter from a linear oscillator.
```

## Tutorial 06 - Dispersive Readout

Worked example run:

```powershell
python -c "import runpy, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; plt.savefig=lambda *a, **k: None; plt.show=lambda *a, **k: None; runpy.run_path(r'hands-on\04-dispersive-readout\dispersive.py', run_name='__main__')"
```

Observed output after installing `hands-on/requirements.txt`: the script runs, prints `chi/2pi = 5.0 MHz`, `kappa/2pi = 5.0 MHz`, `drive/2pi = 5.0 MHz`, steady-state fields `(-0.8000, -0.4000)` and `(+0.8000, -0.4000)`, magnitudes `0.8944`, and IQ separation `1.6000`. Matplotlib emitted a font-cache permission warning from the sandboxed home directory; this is environmental, not a code failure.

### 1. Blocker - `sigma_z` convention makes the JC/SW derivation and lab sign wrong

File/lines: `tutorial/06-readout.md:12,17,28,31,38,44,62-63,191,236`; `hands-on/04-dispersive-readout/README.md:35-37`; `hands-on/04-dispersive-readout/dispersive.py:7-10,63-66,98-102`.

What is wrong: The chapter declares `Z = |0><0| - |1><1|` with `|0>` ground, but uses the opposite-convention Hamiltonian and cross-Kerr signs. The lab uses QuTiP `sigmaz()` with the same `|0> -> +1` convention, so its Hamiltonian carries the same sign mismatch.

Why it is wrong: With `Z|0> = +|0>` and `Z|1> = -|1>`, the physical qubit Hamiltonian is `- omega_q Z/2`. In Blais's convention, `sigma_z = |e><e| - |g><g|`, so `+ chi sigma_z n` maps to `- chi Z n` in the chapter's readout convention. The existing derivation also chooses the wrong sign for the SW generator under the stated transformation.

Proposed fix:

```diff
--- a/tutorial/06-readout.md
+++ b/tutorial/06-readout.md
@@
-H/\hbar = \omega_r\, a^\dagger a + \tfrac{1}{2}\omega_q\,\sigma_z + g\left(a^\dagger \sigma_- + a\,\sigma_+\right).
+H/\hbar = \omega_r\, a^\dagger a - \tfrac{1}{2}\omega_q\,Z + g\left(a^\dagger \sigma_- + a\,\sigma_+\right).
@@
-S = \frac{g}{\Delta}\left(a^\dagger \sigma_- - a\,\sigma_+\right).
+S = -\frac{g}{\Delta}\left(a^\dagger \sigma_- - a\,\sigma_+\right).
@@
-\frac{g^2}{\Delta}\left(a^\dagger a + \tfrac{1}{2}\right)\sigma_z .
+-\frac{g^2}{\Delta}\left(a^\dagger a + \tfrac{1}{2}\right)Z .
@@
-\left(\omega_r + \chi\,\sigma_z\right) a^\dagger a + \tfrac{1}{2}\!\left(\omega_q + \chi\right)\sigma_z
+\left(\omega_r - \chi\,Z\right) a^\dagger a - \tfrac{1}{2}\!\left(\omega_q + \chi\right)Z
@@
-the resonator frequency is $\omega_r + \chi$ if the qubit is in $|0\rangle$
-and $\omega_r - \chi$ if in $|1\rangle$.
+the resonator frequency is $\omega_r - \chi$ if the qubit is in $|0\rangle$
+and $\omega_r + \chi$ if in $|1\rangle$.
--- a/hands-on/04-dispersive-readout/dispersive.py
+++ b/hands-on/04-dispersive-readout/dispersive.py
@@
-    H_disp = chi * sigmaz * a.dag() * a
+    H_disp = -chi * sigmaz * a.dag() * a
@@
-H = delta * a.dag() * a + chi * sz * a.dag() * a + drive * (a + a.dag())
+H = delta * a.dag() * a - chi * sz * a.dag() * a + drive * (a + a.dag())
@@
-    H_cav = (delta + sz_value * chi) * ac.dag() * ac + drive * (ac + ac.dag())
+    H_cav = (delta - sz_value * chi) * ac.dag() * ac + drive * (ac + ac.dag())
```

### 2. Major - Lab units are off by 1000

File/lines: `hands-on/04-dispersive-readout/dispersive.py:31,34-36,46-51,112-114`; `hands-on/04-dispersive-readout/README.md:60-68`.

What is wrong: With time in microseconds, `1/us = 1 MHz`. Therefore `2*pi*0.005` is `2*pi*0.005 MHz`, i.e. 5 kHz, not 5 MHz. The printed `*1e3` hides the error, and the claimed `2/kappa ~= 64 microseconds` confirms the simulation is using kHz-scale rates.

Why it is wrong: A 5 kHz readout linewidth is not physically representative of the MHz-scale readout rates discussed in circuit-QED readout design. The dimensionless steady-state IQ separation happens to match because `chi`, `kappa`, and `drive` were all scaled together, but the time axis and reported physical rates are wrong.

Proposed fix:

```diff
--- a/hands-on/04-dispersive-readout/dispersive.py
+++ b/hands-on/04-dispersive-readout/dispersive.py
@@
-chi = 2 * np.pi * 0.005      # dispersive shift, 5 MHz
-drive = 2 * np.pi * 0.005    # cavity drive amplitude, 5 MHz
-kappa = 2 * np.pi * 0.005    # cavity decay rate, 5 MHz
+chi = 2 * np.pi * 5.0        # dispersive shift, 5 MHz
+drive = 2 * np.pi * 5.0      # cavity drive amplitude, 5 MHz
+kappa = 2 * np.pi * 5.0      # cavity decay rate, 5 MHz
@@
-# 2/kappa ~ 64 us
+# 2/kappa ~ 0.064 us = 64 ns
@@
-tlist = np.linspace(0, 400.0, 800)
+tlist = np.linspace(0, 0.4, 800)
@@
-print(f"chi/2pi   = {chi / (2 * np.pi) * 1e3:.1f} MHz")
+print(f"chi/2pi   = {chi / (2 * np.pi):.1f} MHz")
--- a/hands-on/04-dispersive-readout/README.md
+++ b/hands-on/04-dispersive-readout/README.md
@@
-timescale `2/kappa` (about `64` microseconds here, not
+timescale `2/kappa` (about `64` ns here, not
```

### 3. Major - Kappa tradeoff row says the opposite of Purcell physics

File/lines: `tutorial/06-readout.md:201-205`.

What is wrong: The table says increasing `kappa` helps by giving "less Purcell-T1 cost." The same chapter correctly states `Gamma_Purcell = kappa (g/Delta)^2`.

Why it is wrong: Larger unfiltered `kappa` increases Purcell decay. The mitigation is a Purcell filter that gives high escape at `omega_r` while suppressing the density of states at `omega_q`.

Proposed fix:

```diff
--- a/tutorial/06-readout.md
+++ b/tutorial/06-readout.md
@@
-| $\kappa$ | faster info out; less Purcell-$T_1$ cost (fast escape) | less phase contrast; worse Purcell at $\omega_q$ (without filter) |
+| $\kappa$ | faster photon escape; shorter cavity ring-down | less phase contrast if too broad; larger unfiltered Purcell decay unless a Purcell filter suppresses the density of states at $\omega_q$ |
```

### 4. Minor - Transmon correction prose is sign-unsafe

File/lines: `tutorial/06-readout.md:72,75,217,230`.

What is wrong: The formula `chi = g^2 alpha/[Delta(Delta+alpha)]` is correct, but the prose "because alpha < 0, the factor is less than one" is only clean for the common `Delta < 0` case used later.

Why it is wrong: For `Delta > 0`, `alpha/(Delta+alpha)` can be negative if `Delta+alpha > 0`; near `Delta+alpha = 0`, the perturbation theory fails.

Proposed fix:

```diff
--- a/tutorial/06-readout.md
+++ b/tutorial/06-readout.md
@@
-Because $\alpha<0$, the factor $\alpha/(\Delta+\alpha)$ is less than one: **the third level partially cancels the dispersive shift.**
+For the common transmon-readout case used below, $\Delta<0$ and $\alpha<0$, so $0<\alpha/(\Delta+\alpha)<1$ and $|\chi|<|g^2/\Delta|$: **the third level partially cancels the two-level dispersive shift.** For other detuning signs, keep the full signed formula and avoid the straddling region $\Delta+\alpha\approx0$.
```

## Tutorial 07 - Single-Qubit Gates

Paired code: `hands-on/01-bloch-sphere/bloch.py` and `hands-on/02-rabi/rabi.py`.

### 1. Major - Lab-frame Hamiltonian uses the opposite `sigma_z` convention from the labs

File/lines: `tutorial/07-single-qubit-gates.md:22-45`.

What is wrong: the chapter writes `H_lab = + omega_q sigma_z/2` while the labs define `|0>` as the ground state and QuTiP `sigmaz()` gives `<sigma_z>=+1` for `|0>`. That Hamiltonian makes `|0>` the higher-energy state.

Why it is wrong: with the lab convention, the physical two-level Hamiltonian is `-omega_q Z/2` up to an irrelevant constant. McKay et al. use the same ground-state convention in their virtual-Z discussion. The code is internally consistent; the text is the part that should move.

Proposed fix:

```diff
--- a/tutorial/07-single-qubit-gates.md
+++ b/tutorial/07-single-qubit-gates.md
@@
-Modelling the qubit as a two-level system with gap $\omega_q$ (set $\hbar=1$), and letting the drive couple to the qubit dipole (represented by $\hat\sigma_x$), the lab-frame Hamiltonian is
+Using the same convention as the labs, $|0\rangle$ is the ground state and $\hat\sigma_z|0\rangle=+|0\rangle$. Dropping an irrelevant constant, the lab-frame Hamiltonian is
@@
-$$ H_\text{lab}(t) = \frac{\omega_q}{2}\,\hat\sigma_z + \Omega(t)\cos(\omega_d t + \phi)\,\hat\sigma_x . $$
+$$ H_\text{lab}(t) = -\frac{\omega_q}{2}\,\hat\sigma_z + \Omega(t)\cos(\omega_d t - \phi)\,\hat\sigma_x . $$
@@
-$$ U(t) = \exp\!\Big(\,i\,\frac{\omega_d t}{2}\,\hat\sigma_z\Big), \qquad H_\text{rot} = U H_\text{lab} U^\dagger + i\,\dot U\,U^\dagger . $$
+$$ U(t) = \exp\!\Big(-i\,\frac{\omega_d t}{2}\,\hat\sigma_z\Big), \qquad H_\text{rot} = U H_\text{lab} U^\dagger + i\,\dot U\,U^\dagger . $$
@@
-Together they give $\tfrac{\Delta}{2}\hat\sigma_z$ with **detuning** $\Delta = \omega_q - \omega_d$.
+Together they give $\tfrac{\Delta}{2}\hat\sigma_z$ with **detuning** $\Delta = \omega_d - \omega_q$.
```

### 2. Major - `X90` Bloch-sphere direction is reversed

File/lines: `tutorial/07-single-qubit-gates.md:69`.

What is wrong: the text says `X90` takes `|0>` to `+y`.

Why it is wrong: for `R_x(theta)=exp[-i theta sigma_x/2]`, `R_x(pi/2)|0>=(|0>-i|1>)/sqrt(2)`, whose Bloch vector is `-y`. `+y` would be `X-90` or the opposite Hamiltonian sign.

Proposed fix:

```diff
--- a/tutorial/07-single-qubit-gates.md
+++ b/tutorial/07-single-qubit-gates.md
@@
-         |        X90: 90 degree rotation about x
-         |   ___       takes |0> -> equator (+y)
+         |        X90: 90 degree rotation about +x
+         |   ___       takes |0> -> equator (-y)
```

### 3. Major - Virtual-Z phase update has inconsistent sign

File/lines: `tutorial/07-single-qubit-gates.md:140-144`.

What is wrong: one sentence says subsequent pulse phases shift by `+lambda`, while the next says commuting the gate leftward subtracts `lambda`.

Why it is wrong: under the chapter convention `R_phi(theta)=exp[-i theta(cos phi sigma_x + sin phi sigma_y)/2]`, compiling a logical `Z(lambda)` into later pulses uses `phi -> phi - lambda`. If the author wants the opposite sign, the drive phase convention must be changed consistently.

Proposed fix:

```diff
--- a/tutorial/07-single-qubit-gates.md
+++ b/tutorial/07-single-qubit-gates.md
@@
-Since every drive axis is defined relative to $\phi$, applying $Z(\lambda)$ equals shifting the phase reference of all *subsequent* pulses by $\lambda$:
+Since every drive axis is defined relative to $\phi$, applying $Z(\lambda)$ can be compiled into the phase reference of all *subsequent* pulses. With the convention above,
@@
-$$ Z(\lambda):\ \phi \to \phi+\lambda \ \text{ for every later pulse.} $$
+$$ Z(\lambda):\ \phi \to \phi-\lambda \ \text{ for every later pulse.} $$
@@
-Commuting a $Z(\lambda)$ leftward through later gates is exactly subtracting $\lambda$ from each later pulse phase
+Commuting a $Z(\lambda)$ through later gates is exactly this subtraction of $\lambda$ from each later pulse phase
```

### 4. Major - Worked-example units and gate duration mix angular and cyclic frequency

File/lines: `tutorial/07-single-qubit-gates.md:180-183`.

What is wrong: `Delta/2pi=25 MHz (=Omega)` equates a cyclic-frequency value with an angular frequency, and a Y90 half-pulse is called 20 ns even though the same example makes a pi pulse 20 ns.

Why it is wrong: if `Omega/2pi = 25 MHz`, the pi-pulse time is `pi/Omega = 20 ns` and a pi/2 pulse is `10 ns`. The text's 20 ns Y90 is a factor-of-two error.

Proposed fix:

```diff
--- a/tutorial/07-single-qubit-gates.md
+++ b/tutorial/07-single-qubit-gates.md
@@
-Mistune by $\Delta/2\pi=25$ MHz ($=\Omega$).
+Mistune by $|\Delta|/2\pi=25$ MHz, i.e. $|\Delta|=\Omega$.
@@
-4. **Hadamard.** Virtual $Z(\pi)$ (zero ns) then Y90, one 20 ns half-pulse total.
+4. **Hadamard.** Virtual $Z(\pi)$ (zero ns) then Y90, one 10 ns half-pulse total.
@@
-plus a small frame correction $\sim\Omega^2/(2\alpha)= (50)^2/(2\cdot250) = 5$ MHz
+plus a small frame correction with scale $|\Omega^2/(2\alpha)|/2\pi = (50)^2/(2\cdot250) = 5$ MHz
```

### 5. Major - DRAG detuning correction is sign- and convention-unsafe

File/lines: `tutorial/07-single-qubit-gates.md:123-125`.

What is wrong: the chapter gives a bare `delta_d = Omega_x^2/(2 alpha)` without stating the detuning convention or the leakage matrix-element convention.

Why it is wrong: in Motzoi et al., the quadrature correction and detuning correction are convention dependent; one common form is `Omega_y ~= -dot(Omega_x)/alpha`, with a dynamic detuning proportional to `(lambda^2-4)Omega_x^2/(4 alpha)` in their notation. Since transmon `alpha<0`, sign mistakes here compile directly into phase and leakage errors.

Proposed fix:

```diff
--- a/tutorial/07-single-qubit-gates.md
+++ b/tutorial/07-single-qubit-gates.md
@@
-$$ \Omega_y(t) = -\frac{\dot\Omega_x(t)}{\alpha}, \qquad \delta_d = \frac{\Omega_x^2}{2\alpha}\ \ (\text{detuning correction}). $$
+$$ \Omega_y(t) \simeq -\frac{\dot\Omega_x(t)}{\alpha}, \qquad
+\delta_1(t) \simeq \frac{(\lambda^2-4)\Omega_x^2(t)}{4\alpha}\ \ (\text{Motzoi convention: } \delta_1=\omega_{01}-\omega_d). $$
@@
-A residual diagonal AC-Stark shift $\sim\Omega_x^2/(2\alpha)$ remains and is cancelled by a small dynamic detuning
+A residual diagonal AC-Stark shift of order $\Omega_x^2/\alpha$ remains and is cancelled by a small dynamic detuning; the sign must follow the chosen detuning convention
```

### 6. Minor - Bloch lab relaxation exercise names the wrong steady state under drive

File/lines: `hands-on/01-bloch-sphere/README.md:78-80`.

What is wrong: the exercise says adding relaxation makes the driven trajectory spiral inward toward `|0>`.

Why it is wrong: with the continuous resonant X drive left on, `mesolve` approaches the driven steady state, not the ground state. A direct check with the lab's `Omega/2pi=5 MHz` and suggested `gamma=2/us` gives final `<sigma_z> ~= 0.0026`, near the Bloch-sphere center. The collapse operator itself is correct.

Proposed fix:

```diff
--- a/hands-on/01-bloch-sphere/README.md
+++ b/hands-on/01-bloch-sphere/README.md
@@
-2. Swap `sesolve` for `mesolve` with a collapse operator
-   `c_ops=[np.sqrt(2.0) * destroy(2)]` to add relaxation, and watch the
-   trajectory spiral inward toward `|0>` instead of staying on the surface.
+2. Import `mesolve` and `destroy`, then swap `sesolve` for `mesolve` with
+   `c_ops=[np.sqrt(2.0) * destroy(2)]` to add relaxation. Under the continuous
+   X drive the trajectory spirals inward toward the driven steady state; if you
+   turn the drive off afterward, relaxation carries it to `|0>`.
```

## Tutorial 08 - Two-Qubit Gates

No paired executable code was found for this tutorial.

### 1. Major - Static ZZ derivation drops the `|20>` denominator sign

File/lines: `tutorial/08-two-qubit-gates.md:41`.

What is wrong: the perturbative ZZ derivation treats the `|02>` and `|20>` contributions as if they had the same denominator sign.

Why it is wrong: with `Delta = omega_1 - omega_2`, `E_11-E_02 = Delta - alpha_2`, but `E_11-E_20 = -(Delta + alpha_1)`. The second-order `|11>` shift is therefore

```text
delta E_11 = 2 g^2/(Delta - alpha_2) - 2 g^2/(Delta + alpha_1),
```

while the `|10>` and `|01>` shifts cancel out of `zeta`. The text's sign error changes the predicted sign and possible cancellation of residual ZZ.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-2. The state $|11\rangle$ couples to both $|02\rangle$ and $|20\rangle$ with matrix element $\sqrt2 g$.
-3. The second-order shifts of $|10\rangle$, $|01\rangle$, and $|11\rangle$ do not cancel, leaving
+2. The state $|11\rangle$ couples to $|02\rangle$ and $|20\rangle$ with matrix element $\sqrt2 g$.
+3. With $\Delta=\omega_1-\omega_2$, the denominators are $E_{11}-E_{02}=\Delta-\alpha_2$ and $E_{11}-E_{20}=-(\Delta+\alpha_1)$. Thus
+   $$\delta E_{11}= \frac{2g^2}{\Delta-\alpha_2}-\frac{2g^2}{\Delta+\alpha_1}.$$
+   The single-excitation shifts cancel from $\zeta$, leaving the signed conditional shift.
```

### 2. Major - Idle ZZ and CZ phase are presented as literally the same quantity

File/lines: `tutorial/08-two-qubit-gates.md:45,200,210`.

What is wrong: the text says idle ZZ and CZ use the same matrix element/same quantity.

Why it is wrong: idle ZZ is a perturbative conditional frequency shift from virtual couplings to `|02>` and `|20>`. A CZ gate can accumulate conditional phase by pulsing near a selected avoided crossing. They share the exchange Hamiltonian but are not literally the same observable.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-The same matrix element that gives idle ZZ is what makes CZ possible.
+The same exchange Hamiltonian that gives idle ZZ also creates the avoided crossings used for CZ, but the idle shift and the pulsed gate phase are not the same measured quantity.
@@
-- **"ZZ is separate from CZ."** It is the same avoided-crossing physics: idle ZZ is the small always-on conditional phase rate; CZ is the deliberate large conditional phase.
+- **"ZZ is separate from CZ."** They share avoided-crossing physics: idle ZZ is the small perturbative always-on conditional phase rate, while CZ deliberately changes the spectrum to accumulate a calibrated conditional phase.
@@
-- Two-qubit gates are conditional phases from the same physics as residual ZZ; the difference is whether you suppress it or exploit it.
+- Two-qubit gates often exploit the same couplings that also create residual ZZ; the difference is whether the conditional phase is deliberately calibrated or accidentally left on.
```

### 3. Major - CZ conditional-phase sign and units are ambiguous

File/lines: `tutorial/08-two-qubit-gates.md:72,75-77`.

What is wrong: the chapter does not specify whether `zeta` is an angular frequency or cyclic frequency, and it drops the Schrodinger phase sign.

Why it is wrong: if `zeta` is an angular-frequency energy shift, the conditional phase is `phi_cond = - integral zeta(t) dt mod 2pi`. A pulse near the avoided crossing can raise or lower the relevant branch depending on detuning, so the sign is not universally "pushed down."

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-The `|11>` branch is pushed down, so it accumulates extra phase.
+The `|11>` branch is shifted by a signed conditional angular frequency $\zeta(t)$.
@@
-$$ \phi_\text{CZ} = \int \zeta(t)\,dt = \pi . $$
+$$ \phi_\text{cond} = -\int \zeta(t)\,dt \pmod{2\pi}, \qquad \phi_\text{cond}=\pi \ \text{for CZ}. $$
@@
-If $\zeta/2\pi = 5$ MHz, a CZ takes $t=\pi/\zeta=100$ ns.
+If $|\zeta|/2\pi = 5$ MHz, a conditional phase of $\pi$ takes $t=\pi/|\zeta|=100$ ns.
```

### 4. Major - Landau-Zener formula mixes energy and angular-frequency conventions

File/lines: `tutorial/08-two-qubit-gates.md:85,96`.

What is wrong: the formula uses a gap and sweep rate without defining whether they are energies or angular frequencies.

Why it is wrong: for `H/hbar = (epsilon/2)sigma_z + V sigma_x`, with `epsilon` and `V` in rad/s, the avoided-crossing gap is `Delta_gap=2V` and `P_LZ ~= exp[-pi Delta_gap^2/(2 |dot epsilon|)]`. Adding extra `hbar` factors in the angular-frequency convention gives the wrong exponent dimensions.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-$$ P_\text{LZ} \approx \exp\!\left[-\frac{\pi \Delta_\text{gap}^2}{2\hbar v}\right]. $$
+For $H/\hbar=(\epsilon/2)\sigma_z+V\sigma_x$, with $\epsilon$ and $V$ in angular-frequency units,
+$$ P_\text{LZ} \approx \exp\!\left[-\frac{\pi \Delta_\text{gap}^2}{2|\dot\epsilon|}\right], \qquad \Delta_\text{gap}=2|V|. $$
```

### 5. Major - iSWAP sign contradicts the stated Hamiltonian

File/lines: `tutorial/08-two-qubit-gates.md:149,166`.

What is wrong: the Hamiltonian is written with `+g(a1^\dagger a2 + a1 a2^\dagger)`, but the time evolution uses the opposite sign.

Why it is wrong: under `U=exp(-iHt)`, `|01> -> cos(gt)|01> - i sin(gt)|10>`. At `gt=pi/2`, this is `-i|10>`, not `+i|10>`. The existing text matches `iSWAP^\dagger` or the opposite coupling sign.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-|01\rangle \to \cos(gt)|01\rangle + i\sin(gt)|10\rangle .
+|01\rangle \to \cos(gt)|01\rangle - i\sin(gt)|10\rangle
+\quad \text{for the positive-}g\text{ Hamiltonian above}.
@@
-At $t=\pi/(2g)$ this is iSWAP.
+At $t=\pi/(2g)$ this is iSWAP up to the sign convention for $g$ and single-qubit phases; with the Hamiltonian sign above it is the `-i` version.
```

### 6. Major - Cross-resonance formula and echo-cancellation logic are over-specific

File/lines: `tutorial/08-two-qubit-gates.md:130,132-143`.

What is wrong: the CR rate formula is presented without saying that the anharmonicity is the driven control qubit's anharmonicity and that the sign is convention dependent. The echo paragraph also states the wrong parity logic for which terms cancel.

Why it is wrong: weak-drive CR expressions depend on the Hamiltonian convention, drive quadrature convention, and multilevel model. The apparent pole near `Delta=-alpha_c` is a breakdown/frequency-collision region, not a recipe for infinite rate.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-$$ \Omega_{ZX} \sim \Omega_d\,\frac{J\alpha}{\Delta(\Delta+\alpha)} . $$
+$$ \Omega_{ZX} \sim \Omega_d\,\frac{J\alpha_c}{\Delta(\Delta+\alpha_c)} $$
+up to sign and frame conventions, where $\alpha_c$ is the driven control qubit's anharmonicity. The formula is perturbative and fails near the collision $\Delta+\alpha_c\approx0$.
@@
-The echo cancels the single-qubit terms and keeps the ZX term.
+The echo cancels selected single-qubit and drive-odd terms by combining control pi pulses with drive phase reversal; the desired ZX term is retained after choosing the calibrated frame.
```

### 7. Minor - Tunable-coupler detuning convention is unstated

File/lines: `tutorial/08-two-qubit-gates.md:105`.

What is wrong: the tunable-coupler formula uses detunings without defining their signs.

Why it is wrong: cancellation conditions depend on whether `Delta_i = omega_i - omega_c` or `omega_c - omega_i`.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-where $\Delta_i$ are qubit-coupler detunings.
+where $\Delta_i=\omega_i-\omega_c$ are signed qubit-coupler detunings in this convention.
```

### 8. Minor - Residual-ZZ "error" scaling is phase-linear but infidelity is quadratic

File/lines: `tutorial/08-two-qubit-gates.md:183`.

What is wrong: the chapter calls `zeta t` the error.

Why it is wrong: `|zeta|t` is the unwanted coherent conditional phase. For a small coherent phase error, the average infidelity scales as `O[(zeta t)^2]`, not linearly.

Proposed fix:

```diff
--- a/tutorial/08-two-qubit-gates.md
+++ b/tutorial/08-two-qubit-gates.md
@@
-Residual ZZ gives an error $\sim \zeta t$ during idle time.
+Residual ZZ gives an unwanted conditional phase $\sim \zeta t$ during idle time; the small coherent infidelity scales as $O[(\zeta t)^2]$ unless randomized or echoed.
```

## Tutorial 09 - Coherence and Noise

Paired code: `hands-on/03-t1-t2/t1_t2.py`.

### 1. Major - Longitudinal and transverse noise terminology is reversed

File/lines: `tutorial/09-coherence-noise.md:9-10,15,209`.

What is wrong: the chapter says "longitudinal coupling" along `sigma_x/sigma_y` drives `T1`, and "transverse coupling along the qubit axis" `sigma_z` drives dephasing.

Why it is wrong: relative to the qubit quantization axis, transverse noise (`sigma_x/sigma_y`) drives transitions and `T1`; longitudinal `sigma_z` noise shifts the transition frequency and drives pure dephasing. This is the convention used in Krantz et al. and Bylander et al.

Proposed fix:

```diff
--- a/tutorial/09-coherence-noise.md
+++ b/tutorial/09-coherence-noise.md
@@
-- **Longitudinal coupling** (along a transverse direction, $\hat\sigma_x$/$\hat\sigma_y$) can exchange *energy* with the bath. The bath can absorb a photon at $\omega_q$ and de-excite the qubit. This drives **$T_1$ relaxation**.
-- **Transverse coupling along the qubit axis** ($\hat\sigma_z$) conserves energy but modulates the qubit frequency $\omega_q$. No photon is exchanged; instead the phase is scrambled. This drives **pure dephasing**, $T_\phi$.
+- **Transverse coupling** (perpendicular to the qubit axis, $\hat\sigma_x$/$\hat\sigma_y$) can exchange *energy* with the bath. The bath can absorb a photon at $\omega_q$ and de-excite the qubit. This drives **$T_1$ relaxation**.
+- **Longitudinal coupling** (along the qubit axis, $\hat\sigma_z$) conserves energy but modulates the qubit frequency $\omega_q$. No photon is exchanged; instead the phase is scrambled. This drives **pure dephasing**, $T_\phi$.
@@
-    P --> A["Energy loss<br/>|1>-> |0>, photon<br/>(longitudinal bath)"]
+    P --> A["Energy loss<br/>|1>-> |0>, photon<br/>(transverse bath)"]
@@
-- A qubit decoheres because it is weakly coupled to a bath: longitudinal coupling drives $T_1$, $\sigma_z$ coupling drives $T_\phi$.
+- A qubit decoheres because it is weakly coupled to a bath: transverse coupling drives $T_1$, while longitudinal $\sigma_z$ coupling drives $T_\phi$.
```

### 2. Major - PSD and filter-function conventions are mixed

File/lines: `tutorial/09-coherence-noise.md:57-64,73-82,111`.

What is wrong: the chapter mixes a bilateral angular-frequency PSD `S(omega)` with one-sided `per sqrt Hz` noise amplitudes. The filter formula also leaves `tilde g` ambiguous: if it is the Fourier transform of the switching function, the extra `/omega^2` is wrong.

Why it is wrong: one-sided cyclic-frequency PSDs and bilateral angular-frequency PSDs differ by convention factors. Ramsey decay from quasi-static `1/f` flux noise also depends on infrared and ultraviolet cutoffs; the printed `sqrt(2 ln 2)` constant is not a general Ramsey result.

Proposed fix:

```diff
--- a/tutorial/09-coherence-noise.md
+++ b/tutorial/09-coherence-noise.md
@@
-The **Wiener-Khinchin theorem** says the noise **power spectral density (PSD)** is the Fourier transform of that autocorrelation:
+With a bilateral angular-frequency convention, the **Wiener-Khinchin theorem** says the noise **power spectral density (PSD)** is the Fourier transform of that autocorrelation:
@@
-$$S_\Phi(\omega) = A^2 \left(\frac{2\pi \times 1\,\text{Hz}}{|\omega|}\right)^{\alpha}, \qquad \alpha \approx 1,$$
+Noise amplitudes in superconducting qubits are usually quoted as a one-sided cyclic-frequency PSD:
+$$S_\Phi^{(1)}(f) = A_\Phi^2 \left(\frac{1\,\text{Hz}}{f}\right)^{\alpha}, \qquad f>0,\quad \alpha \approx 1,$$
@@
-where $A$ is the noise amplitude, usually quoted in $\mu\Phi_0/\sqrt{\text{Hz}}$ at 1 Hz.
+where $A_\Phi$ is the noise amplitude, usually quoted in micro-$\Phi_0/\sqrt{\text{Hz}}$ at 1 Hz. Convert explicitly before inserting it into a bilateral $S_\Phi(\omega)$ formula.
@@
-$$\chi(t) = \frac{1}{2}\int_0^\infty \frac{d\omega}{\pi}\, S(\omega)\, \frac{|\tilde g(\omega,t)|^2}{\omega^2}, \qquad \langle\sigma_x\rangle \propto e^{-\chi(t)}.$$
+$$G_N(\omega,t)=\int_0^t g_N(t')e^{i\omega t'}dt',$$
+$$\chi(t) = \frac{1}{2}\int_0^\infty \frac{d\omega}{\pi}\, S_{\delta\omega}(\omega)\, |G_N(\omega,t)|^2, \qquad \langle\sigma_x\rangle \propto e^{-\chi(t)}.$$
+Equivalently, if $Y_N(\omega,t)=i\omega G_N(\omega,t)$ is used as the dimensionless filter numerator, write $|Y_N|^2/\omega^2$ instead of $|G_N|^2$.
@@
-$$\langle\sigma_x\rangle \propto e^{-(t/T_2^*)^2}, \qquad \frac{1}{T_2^*} \sim \left|\frac{\partial\omega_q}{\partial\Phi}\right| A\sqrt{2\ln 2}.$$
+$$\langle\sigma_x\rangle \propto e^{-(t/T_2^*)^2}, \qquad \frac{1}{T_2^*} \sim \left|\frac{\partial\omega_q}{\partial\Phi}\right| A_\Phi\sqrt{\ln(f_{\rm uv}/f_{\rm ir})},$$
+up to the stated one-sided/bilateral convention factors.
```

### 3. Minor - The Markovian Ramsey lab is labeled `T2*`

File/lines: `hands-on/03-t1-t2/README.md:19-23,60-69`; `hands-on/03-t1-t2/t1_t2.py:6-11,63,87,101,105`.

What is wrong: the lab labels the simulated Lindblad Ramsey decay as `T2*`.

Why it is wrong: the simulation has no quasi-static shot-to-shot detuning distribution or inhomogeneous broadening. It measures Markovian Ramsey `T2`, with `1/T2 = 1/(2T1) + 1/Tphi`. The code's collapse prefactor is correct; the star notation is the issue.

Proposed fix:

```diff
--- a/hands-on/03-t1-t2/README.md
+++ b/hands-on/03-t1-t2/README.md
@@
-   collapse operators. The fringes decay under an envelope set by T2*.
+   collapse operators. The fringes decay under the Markovian Ramsey envelope set by T2.
@@
-samples of the decay envelope, fit `log` of those peaks to get T2*, and compare
-`1/T2*` against `1/(2*T1) + 1/Tphi`.
+samples of the decay envelope, fit `log` of those peaks to get T2, and compare
+`1/T2` against `1/(2*T1) + 1/Tphi`.
--- a/hands-on/03-t1-t2/t1_t2.py
+++ b/hands-on/03-t1-t2/t1_t2.py
@@
-     envelope set by T2*.
+     envelope set by the Markovian Ramsey T2.
@@
-T2star_fit = -1.0 / slope
+T2_fit = -1.0 / slope
@@
-print(f"  fitted    T2*        = {T2star_fit:.2f} us")
+print(f"  fitted    T2         = {T2_fit:.2f} us")
```

## Tutorial 10 - Measurement Chain

No paired executable code was found for this tutorial.

### 1. Major - Attenuator noise-temperature equation is classical but used in the quantum regime

File/lines: `tutorial/10-measurement-chain.md:63`.

What is wrong: the tutorial writes the physical-temperature cascade and photon-occupation cascade as if they were interchangeable.

Why it is wrong: the exact quantum statement is for photon occupation, `n_out = n_in/A + (1 - 1/A)n(T_i)`. A Rayleigh-Jeans equivalent temperature equals the physical temperature only when `k_B T >> hbar omega`. At 5 GHz and 10 mK this fails badly.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
-$$T_{\text{noise}}^{\text{out}} = \frac{T_{\text{noise}}^{\text{in}}}{A_i} + \left(1 - \frac{1}{A_i}\right) T_i, \qquad \bar n_{\text{out}} = \frac{\bar n_{\text{in}}}{A_i} + \left(1 - \frac{1}{A_i}\right)\bar n(\omega, T_i).$$
+If we use a Rayleigh-Jeans-equivalent noise temperature $T_{\rm RJ}\equiv(\hbar\omega/k_B)\bar n$, then
+$$T_{{\rm RJ},\text{out}} = \frac{T_{{\rm RJ},\text{in}}}{A_i} + \left(1 - \frac{1}{A_i}\right)T_{\rm RJ}(T_i), \qquad
+T_{\rm RJ}(T_i)=\frac{\hbar\omega}{k_B}\bar n(\omega,T_i).$$
+This reduces to the physical temperature $T_i$ only in the classical limit $k_BT_i\gg\hbar\omega$. The exact quantum statement is
+$$\bar n_{\text{out}} = \frac{\bar n_{\text{in}}}{A_i} + \left(1 - \frac{1}{A_i}\right)\bar n(\omega, T_i).$$
```

### 2. Major - Friis arithmetic has a factor-of-10 error

File/lines: `tutorial/10-measurement-chain.md:158`.

What is wrong: `75/(100*10^4)` is printed as `7.5e-6 K`.

Why it is wrong: `75/(100*10^4) = 75/10^6 = 7.5e-5 K`. The final `0.350 K` rounding is unaffected, but the arithmetic line is wrong.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
-$$T_{\text{sys}} = 0.3 + \frac{5}{100} + \frac{75}{100\cdot 10^4} = 0.3 + 0.05 + 7.5\times10^{-6} \approx 0.350\,\text{K}.$$
+$$T_{\text{sys}} = 0.3 + \frac{5}{100} + \frac{75}{100\cdot 10^4} = 0.3 + 0.05 + 7.5\times10^{-5} \approx 0.350\,\text{K}.$$
```

### 3. Major - The 50 dB input attenuation check ignores re-emission

File/lines: `tutorial/10-measurement-chain.md:166`.

What is wrong: the chapter says `892/0.01 ~= 50 dB` cold attenuation is the standard budget and implies the last MXC attenuator sets the floor.

Why it is wrong: that is only a lower bound. Each attenuator also emits thermal photons. With 20 dB at 4 K, 10 dB at 100 mK, and 20 dB at 10 mK at 7 GHz, the exact cascade gives `n_out ~= 0.020`, not below `0.01`. A 20+20+20 dB chain gives `n_out ~= 0.0024`.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
-**Input-side sanity check.** A 7 GHz tone entering at 300 K carries $\bar n(7\text{ GHz}, 300\text{ K}) = 1/(e^{0.336/300}-1) \approx 892$ photons. To push this below ~0.01 at the chip you need $\sim 892/0.01 \approx 10^5 = 50\,$dB of cold attenuation, exactly the standard 40-60 dB staged budget, with the **last 20 dB at the MXC** so the residual line temperature is the MXC attenuator's, not 300 K.
+**Input-side sanity check.** A 7 GHz tone entering at 300 K carries $\bar n(7\text{ GHz}, 300\text{ K}) = 1/(e^{0.336/300}-1) \approx 892$ photons. The naive lower bound for reaching $0.01$ photon is $10\log_{10}(892/0.01)\approx49.5\,$dB, but real staged attenuation must include each attenuator's own re-emission. For example, 20 dB at 4 K, 10 dB at 100 mK, and 20 dB at 10 mK gives $\bar n_{\rm out}\approx0.020$ at 7 GHz; changing the middle attenuator to 20 dB gives $\bar n_{\rm out}\approx0.0024$. Thus 50 dB is a lower bound, while about 60 dB is the usual target for few-$10^{-3}$ occupations.
```

### 4. Major - MXC cooling power is quoted as if available at 10 mK

File/lines: `tutorial/10-measurement-chain.md:44`.

What is wrong: the table gives `10-50 uW` next to `~10 mK`.

Why it is wrong: dilution-refrigerator cooling power is strongly temperature dependent. Vendor and Krinner-style budgets quote tens of microwatts at elevated MXC temperatures such as 20 mK, not at the base temperature.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
-| MXC | ~10 mK | $\sim 10$-$50\ \mu$W | 20 dB | TWPA, isolators, **chip** | NbTi |
+| MXC | ~10 mK base | model-dependent; $\sim 10$-$50\ \mu$W only at elevated MXC temperature, e.g. ~20 mK, not at base | 20 dB | TWPA, isolators, **chip** | NbTi |
```

### 5. Major - Friis discussion omits passive loss before the first amplifier

File/lines: `tutorial/10-measurement-chain.md:113`.

What is wrong: the diagram places isolators before the TWPA, but the Friis discussion starts at the first amplifier as if preceding loss were harmless.

Why it is wrong: passive loss before the first gain attenuates the signal and multiplies downstream input-referred amplifier noise. Even a cold lossy element with negligible occupation degrades quantum efficiency.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
 **A large first-stage gain $G_1$ crushes every downstream contribution.**
+
+Passive loss before the first amplifier must be included as a Friis stage with gain $G=1/L$, not ignored. A cold lossy element with power loss $L$ contributes thermal occupation $(L-1)\bar n(\omega,T)$ when referred to its input and, even when its own thermal occupation is negligible, multiplies all downstream input-referred amplifier noise by $L$.
```

### 6. Minor - Pair-breaking radiation is described too narrowly as THz/far-infrared

File/lines: `tutorial/10-measurement-chain.md:91`.

What is wrong: the chapter implies pair-breaking radiation is only THz/far-infrared.

Why it is wrong: pair breaking begins at `h nu > 2 Delta`. For aluminum, `2 Delta/h` is order 90 GHz. THz photons are above threshold, but the threshold is much lower than THz.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
-| IR / Eccosorb / lossy-coax filter | THz blackbody, **pair-breaking** radiation | far infrared | MXC, right at chip |
+| IR / Eccosorb / lossy-coax filter | photons above the superconducting gap; mm-wave/IR/THz blackbody, **pair-breaking** radiation | mm-wave through infrared | MXC, right at chip |
@@
-Stray far-infrared photons are dangerous in a way attenuators can't fix: a THz photon carries enough energy to **break Cooper pairs**, generating quasiparticles that directly limit $T_1$.
+Stray high-frequency photons are dangerous in a way attenuators can't fix: any photon with $h\nu>2\Delta$ can **break Cooper pairs** (for aluminum, the threshold is order 90 GHz), generating quasiparticles that directly limit $T_1$.
```

### 7. Nit - "Three roles" introduces a four-row table

File/lines: `tutorial/10-measurement-chain.md:85`.

Proposed fix:

```diff
--- a/tutorial/10-measurement-chain.md
+++ b/tutorial/10-measurement-chain.md
@@
-**Filtering is a separate job from attenuation**, and conflating the two is a common mistake. Attenuators are GHz-band devices; they do nothing about radiation far outside that band. Three roles:
+**Filtering is a separate job from attenuation**, and conflating the two is a common mistake. Attenuators are GHz-band devices; they do nothing about radiation far outside that band. Four roles:
```

## Tutorial 11 - Benchmarking

No paired executable code was found for this tutorial.

### 1. Major - RB twirling assumptions omit leakage and in-subspace conditions

File/lines: `tutorial/11-benchmarking.md:60-68`.

What is wrong: the text says averaging an arbitrary error channel over the Clifford group makes it exactly depolarizing.

Why it is wrong: Clifford twirling gives a depolarizing channel for Markovian, trace-preserving noise on the computational subspace. Leakage is outside that model and requires leakage/seepage analysis, as in Wood and Gambetta.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-The deep reason RB works is *twirling*: averaging an arbitrary error channel $\Lambda$ over the Clifford group collapses it to a **depolarizing channel** described by a single parameter $p$.
+The deep reason RB works is *twirling*: for Markovian, trace-preserving errors acting within the computational subspace, averaging $\Lambda$ over the Clifford group collapses it to a **depolarizing channel** described by a single parameter $p$.
@@
-4. Hence $\overline{\Lambda}$ is fixed by *one* number $p$, it is exactly depolarizing: keep $\rho$ with probability $p$, replace it by $\mathbb{I}/d$ with probability $1-p$.
+4. Hence, under those assumptions, $\overline{\Lambda}$ is fixed by *one* number $p$: keep $\rho$ with probability $p$, replace it by $\mathbb{I}/d$ with probability $1-p$.
+5. Leakage is outside this model; it must be measured separately, for example with leakage/seepage RB.
```

### 2. Major - RB is not blind to coherent errors, and dephasing is not uniform shrinkage

File/lines: `tutorial/11-benchmarking.md:146-149,190,201`.

What is wrong: the chapter says RB is blind to coherent errors and says dephasing shrinks the Bloch sphere uniformly.

Why it is wrong: standard RB reports coherent over-rotations through average infidelity; it just does not diagnose coherence, worst-case accumulation, or diamond-norm behavior. Also, dephasing shrinks transverse components, while depolarization shrinks the sphere uniformly.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-- **Incoherent** (depolarizing/dephasing) errors shrink the Bloch sphere uniformly; in fidelity they add roughly **linearly** with depth.
+- **Incoherent** errors randomize rather than apply a fixed rotation. Depolarization shrinks the Bloch sphere uniformly; dephasing shrinks the transverse components. In average fidelity they add roughly **linearly** with depth.
@@
-RB averages over the sphere and is largely **blind** to coherent errors. The SPAM-free tool that separates them is **unitarity (purity) RB**:
+Standard RB reports coherent errors only through their average infidelity; it does not by itself tell you whether the error was coherent, stochastic, or dangerous in worst case. The SPAM-robust tool that separates them is **unitarity (purity) RB**:
@@
-- **"High fidelity = safe gate."** RB is blind to coherent errors; two gates with the same $r$ can diverge in deep circuits.
+- **"High fidelity = safe gate."** RB alone does not diagnose coherent accumulation; two gates with the same $r$ can diverge in deep circuits.
@@
-- A fidelity is meaningful only with context: averaged not worst-case, floored by $T_1/T_2$ ($r_{\lim}$), separate from readout ($F_a$) and crosstalk, and silent about **coherent** errors unless you run unitarity RB.
+- A fidelity is meaningful only with context: averaged not worst-case, floored by $T_1/T_2$ ($r_{\lim}$), separate from readout ($F_a$) and crosstalk, and not diagnostic of **coherent vs stochastic** errors unless you run unitarity RB.
```

### 3. Minor - "SPAM-free" is overstated

File/lines: `tutorial/11-benchmarking.md:56,173,191,199`.

What is wrong: the text says `p` is SPAM-free and cannot depend on SPAM.

Why it is wrong: under the standard RB model, static SPAM is absorbed into `A` and `B`, so `p` is SPAM-robust. Drift, leakage, non-Markovian noise, and sequence-length-dependent readout can bias the decay.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-Here $A$ and $B$ absorb all SPAM into *offset and amplitude*, so the **decay rate $p$ is SPAM-free**, that is the entire point.
+Here $A$ and $B$ absorb time-independent SPAM into *offset and amplitude*, so the **decay rate $p$ is SPAM-robust** under the RB model.
@@
-| $p$ | depolarizing / decay parameter | fit of $A p^m+B$ | **SPAM-free**; this is what RB measures |
+| $p$ | depolarizing / decay parameter | fit of $A p^m+B$ | **SPAM-robust** under the RB model |
@@
-- **"$p$ depends on SPAM."** It doesn't, SPAM lives only in $A$ and $B$.
+- **"$p$ is just readout error."** In the standard RB model, static SPAM lives in $A$ and $B$, not in $p$. Drift, leakage, or model failure still need residual checks.
@@
-- RB reports a **SPAM-free** average error per Clifford because the **twirl** (Clifford = unitary 2-design) collapses any error to one depolarizing $p$.
+- RB reports a **SPAM-robust** average error per Clifford because the **twirl** (Clifford = unitary 2-design) collapses in-subspace Markovian error to one depolarizing $p$.
```

### 4. Minor - Ramsey calibration mixes angular and cyclic frequency notation

File/lines: `tutorial/11-benchmarking.md:23-24,38,43,46`.

What is wrong: `omega` and `delta` are used with MHz/kHz language without explicit `2pi` conversion.

Why it is wrong: if `delta omega` is angular frequency, the Ramsey phase is `delta omega * tau`. If the fitted beat is `Delta f` in Hz, the phase is `2pi Delta f tau`.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-- **Qubit frequency $\omega_q$: coarse.** Drive continuously while sweeping the drive frequency and watch the excited-state population. You get a Lorentzian (continuous-wave spectroscopy); its center is $\omega_q$ to ~MHz precision.
-- **Qubit frequency $\omega_q$: fine, plus $T_2^*$ (Ramsey).** Two $\pi/2$ pulses separated by a free-evolution delay $\tau$ convert a small detuning $\delta$ into an observable beat. The fringe frequency *is* your frequency error; the envelope decay *is* your dephasing time.
+- **Qubit frequency $\omega_q$: coarse.** Drive continuously while sweeping the drive frequency and watch the excited-state population. You get a Lorentzian; its center is $\omega_q/2\pi$ to ~MHz precision when quoted in Hz.
+- **Qubit frequency $\omega_q$: fine, plus $T_2^*$ (Ramsey).** Two $\pi/2$ pulses separated by a delay $\tau$ convert a small detuning into a beat. If the fitted beat is $\Delta f$ in Hz, then $\delta\omega=2\pi\Delta f$.
@@
-$$ P_{\text{Ramsey}}(\tau) = \tfrac{1}{2}\left[\,1 + e^{-\tau/T_2^*}\cos(\delta\,\tau + \phi)\,\right] $$
+$$ P_{\text{Ramsey}}(\tau) = \tfrac{1}{2}\left[\,1 + e^{-\tau/T_2^*}\cos(\delta\omega\,\tau + \phi)\,\right]
+=\tfrac{1}{2}\left[\,1 + e^{-\tau/T_2^*}\cos(2\pi\Delta f\,\tau + \phi)\,\right]. $$
```

### 5. Minor - Per-Clifford and per-native-gate language slips

File/lines: `tutorial/11-benchmarking.md:74,163,189`.

What is wrong: the worked example calls a per-Clifford result a gate fidelity, and the pitfall says "Cliffords/gate" where it means native gates per Clifford.

Why it is wrong: for small independent stochastic errors, `r_native ~= r_Clifford/G`, where `G` is the average native gates per Clifford. This depends on compilation and noise model.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-> **Pitfall.** $r$ is per **Clifford**, not per physical gate. A Clifford compiles to ~1.5-2 native gates, so per-gate error is roughly $r$ divided by that compiling factor.
+> **Pitfall.** $r$ is per **Clifford**, not per physical gate. A single-qubit Clifford often compiles to ~1.5-2 native pulses, so the native-gate error is roughly $r$ divided by the average native-gates-per-Clifford.
@@
-- **Error per Clifford:** $r=\dfrac{(d-1)(1-p)}{d}=\dfrac{(1)(0.001)}{2}=5\times10^{-4}$, a "99.95%" gate.
+- **Error per Clifford:** $r=\dfrac{(d-1)(1-p)}{d}=\dfrac{(1)(0.001)}{2}=5\times10^{-4}$, a "99.95%" Clifford.
@@
-- **"RB gives THE gate error."** No, an *average* over the Clifford group, not a single physical gate and not worst-case. Divide by the ~1.5-2 Cliffords/gate factor for per-gate error.
+- **"RB gives THE gate error."** No, an *average* over the Clifford group, not a single physical gate and not worst-case. Divide by the average native-gates-per-Clifford for a rough per-gate error.
```

### 6. Minor - Coherence floor wording treats `T2` as pure dephasing

File/lines: `tutorial/11-benchmarking.md:157`.

What is wrong: the prose says "amplitude damping plus dephasing (`1/T2`)".

Why it is wrong: `T2` is total transverse coherence, with `1/T2 = 1/(2T1) + 1/Tphi`. The formula itself is correct; the wording is misleading.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-Model the gate as ideal unitary + amplitude damping ($1/T_1$) + dephasing ($1/T_2$) over duration $\tau_g$; averaging the channel fidelity over the Bloch sphere
+Model the gate as ideal unitary plus relaxation and total transverse decay over duration $\tau_g$; $T_2$ already includes the $T_1$ contribution via $1/T_2=1/(2T_1)+1/T_\phi$. Averaging the channel fidelity over the Bloch sphere
```

### 7. Nit - XEB spoofing claim needs model caveat and citation

File/lines: `tutorial/11-benchmarking.md:109,178,200,205-210`.

What is wrong: "XEB is spoofable" is nontrivial but uncited, and the table calls `F_XEB` full-circuit fidelity without the model caveat.

Why it is wrong: linear XEB approximates circuit fidelity under the noisy-mixture/XEB model and Porter-Thomas statistics. A nonzero linear-XEB score is not a proof of faithful sampling; Barak, Chou, and Gao give shallow-circuit spoofing results.

Proposed fix:

```diff
--- a/tutorial/11-benchmarking.md
+++ b/tutorial/11-benchmarking.md
@@
-> **Pitfall.** XEB needs a *trusted classical simulation* of the ideal amplitudes (infeasible past ~50 qubits at depth), assumes the digital error model, and is known to be **spoofable**.
+> **Pitfall.** XEB needs a *trusted classical simulation* of the ideal amplitudes, assumes the digital error model, and shallow-circuit linear-XEB spoofing results are known.
@@
-| $F_{\text{XEB}}$ | full-circuit XEB fidelity | $2^n\langle P_{\text{ideal}}\rangle-1$ | needs classical simulation |
+| $F_{\text{XEB}}$ | linear-XEB estimator | $2^n\langle P_{\text{ideal}}\rangle-1$ | approximates circuit fidelity under the XEB noise model |
@@
 - P. Krantz *et al.*, *A Quantum Engineer's Guide to Superconducting Qubits*, Appl. Phys. Rev. **6**, 021318 (2019), [arXiv:1904.06560](https://arxiv.org/abs/1904.06560).
+- B. Barak, C.-N. Chou, X. Gao, *Spoofing Linear Cross-Entropy Benchmarking in Shallow Quantum Circuits*, [arXiv:2005.02421](https://arxiv.org/abs/2005.02421).
```

## Tutorial 12 - Error Correction

No paired executable code was found for this tutorial.

### 1. Major - Three-qubit repetition codes are labeled with the wrong formal quantum distance

File/lines: `tutorial/12-error-correction.md:90-97,202`.

What is wrong: the table labels the 3-qubit bit-flip and phase-flip repetition codes as formal `[[3,1,3]]` codes, then later says their full quantum distance is 1.

Why it is wrong: for the bit-flip code, `S=<Z1Z2,Z2Z3>`. `Z1` commutes with the stabilizers, is not in the stabilizer, and acts as a weight-1 logical `Z`. The phase-flip code has the dual weight-1 logical `X`. Their full quantum distance is therefore 1, although their biased distance against the designed error type is 3.

Proposed fix:

```diff
--- a/tutorial/12-error-correction.md
+++ b/tutorial/12-error-correction.md
@@
-| Code | $[[n,k,d]]$ | Stabilizers | Corrects | Hardware note |
+| Code | Formal quantum distance | Stabilizers | Corrects | Hardware note |
@@
-| bit-flip | $[[3,1,3]]$ | $Z_1Z_2,\ Z_2Z_3$ | one $X$ | toy |
-| phase-flip | $[[3,1,3]]$ | $X_1X_2,\ X_2X_3$ | one $Z$ | toy (Hadamard dual) |
+| bit-flip repetition | $[[3,1,1]]$; biased $X$-distance 3 | $Z_1Z_2,\ Z_2Z_3$ | one $X$ only | toy |
+| phase-flip repetition | $[[3,1,1]]$; biased $Z$-distance 3 | $X_1X_2,\ X_2X_3$ | one $Z$ only | toy (Hadamard dual) |
@@
-A caveat on the two repetition rows: the $d=3$ there is the distance against the *one* error type each code handles
+The repetition rows are deliberately biased codes: their distance is 3 only against the one error type each code is designed to correct
@@
-- A **stabilizer code** protects the joint $+1$ eigenspace of commuting Paulis; the progression bit-flip -> phase-flip -> Shor $[[9,1,3]]$ -> surface code introduces $[[n,k,d]]$ and $t=\lfloor(d-1)/2\rfloor$.
+- A **stabilizer code** protects the joint $+1$ eigenspace of commuting Paulis; biased repetition codes lead to Shor $[[9,1,3]]$ and then surface codes, where formal $[[n,k,d]]$ distance gives $t=\lfloor(d-1)/2\rfloor$.
```

### 2. Major - Surface-code qubit count is data qubits, not full physical-qubit cost

File/lines: `tutorial/12-error-correction.md:95,166-174`.

What is wrong: `d^2+(d-1)^2` is presented as "physical qubits" and "qubit cost."

Why it is wrong: that expression is the data-qubit count for one planar layout. Syndrome extraction needs measurement ancillas, couplers, and readout. The Acharya et al. distance-7 below-threshold memory used 101 qubits, not just the table's 85 data qubits.

Proposed fix:

```diff
--- a/tutorial/12-error-correction.md
+++ b/tutorial/12-error-correction.md
@@
-| surface | $[[d^2+(d-1)^2,\,1,\,d]]$ | weight-4 $X$ & $Z$ | up to $t$ | 2D nearest-neighbour |
+| surface | $[[d^2+(d-1)^2,\,1,\,d]]$ data qubits for one planar layout | local $X$ & $Z$ checks | up to $t$ | 2D nearest-neighbour |
@@
-| $d$ | exponent $(d{+}1)/2$ | $p_L \sim (0.1)^{\text{exp}}$ | vs. $d{=}3$ | physical qubits $d^2+(d-1)^2$ |
+| $d$ | exponent $(d{+}1)/2$ | $p_L \sim (0.1)^{\text{exp}}$ | vs. $d{=}3$ | data qubits $d^2+(d-1)^2$ |
@@
-- **Step 4: qubit cost.** Reaching $p_L \sim 10^{-5}$ costs $\sim145$ physical qubits for *one* logical qubit, the steep overhead of fault tolerance.
+- **Step 4: qubit cost.** Reaching $p_L \sim 10^{-5}$ costs $\sim145$ data qubits in this planar layout; measurement ancillas and control hardware add comparable overhead.
```

### 3. Major - Threshold formula is used outside its domain and produces probabilities above 1

File/lines: `tutorial/12-error-correction.md:153-155,175,204`.

What is wrong: the above-threshold worked example computes `p_L = 4` and `8`.

Why it is wrong: the expression is a below-threshold scaling ansatz with decoder/noise/prefactor dependence, not a probability formula valid above threshold. Probabilities cannot exceed 1.

Proposed fix:

```diff
--- a/tutorial/12-error-correction.md
+++ b/tutorial/12-error-correction.md
@@
-$$p_L \;\sim\; A\left(\frac{p}{p_{\text{th}}}\right)^{\lfloor (d+1)/2 \rfloor}, \qquad \Lambda \equiv \frac{p_L(d)}{p_L(d+2)} \approx \frac{p_{\text{th}}}{p}.$$
+$$p_L(d) \;\approx\; A_d\left(\frac{p}{p_{\text{th}}}\right)^{\lfloor (d+1)/2 \rfloor}, \qquad \Lambda \equiv \frac{p_L(d)}{p_L(d+2)} \approx \frac{A_d}{A_{d+2}}\frac{p_{\text{th}}}{p}.$$
@@
-**Step 5: contrast above threshold.** If instead $p = 2\% > p_{\text{th}}$, then $p/p_{\text{th}} = 2$ and $p_L \sim 2^{(d+1)/2}$ *grows*: $d{=}3 \to 4$, $d{=}5 \to 8$.
+**Step 5: contrast above threshold.** If instead $p = 2\% > p_{\text{th}}$, the below-threshold scaling no longer gives a valid probability; its formal growth signals that larger distance no longer provides exponential suppression, so logical errors approach order-one rather than improving.
@@
-- The **threshold theorem**: below $p_{\text{th}}$, $p_L$ drops exponentially with $d$; $\Lambda = p_{\text{th}}/p > 1$ is the operational proof that scaling wins.
+- The **threshold theorem**: below $p_{\text{th}}$, $p_L$ drops exponentially with $d$; empirically $\Lambda>1$ is the operational proof that scaling wins.
```

### 4. Minor - Surface-code checks are not all four-body or literally parallel at the gate level

File/lines: `tutorial/12-error-correction.md:101,105,110,128,203`.

What is wrong: the chapter says surface-code checks are four-body and "run in parallel."

Why it is wrong: bulk checks are weight-4, boundary checks have lower weight. Commuting stabilizers have a common eigenspace, but hardware gates sharing a data qubit must be scheduled inside a QEC round.

Proposed fix:

```diff
--- a/tutorial/12-error-correction.md
+++ b/tutorial/12-error-correction.md
@@
-Data qubits ($D$) sit on a lattice; interleaved **measure** (ancilla) qubits each repeatedly measure a local four-body stabilizer:
+Data qubits ($D$) sit on a lattice; interleaved **measure** (ancilla) qubits repeatedly measure local stabilizers. Bulk checks are four-body, while boundary checks have lower weight:
@@
-Why do these commute (so they can run in parallel)?
+Why do these commute (so their eigenvalues can be extracted in the same QEC round)?
@@
-- Commuting stabilizers share an eigenbasis -> a well-defined code space, measurable in parallel every round.
+- Commuting stabilizers share an eigenbasis -> a well-defined code space; hardware still schedules the shared-qubit gates inside each round.
@@
-Each weight-4 check is read by *one* ancilla
+Each bulk weight-4 check is read by *one* ancilla
@@
-- The **surface code** uses only 2D nearest-neighbour weight-4 checks; noisy syndromes force $(2{+}1)$D spacetime decoding (MWPM / neural).
+- The **surface code** uses 2D nearest-neighbour local checks, weight-4 in the bulk and lower weight at boundaries; noisy syndromes force $(2{+}1)$D spacetime decoding.
```

### 5. Minor - Pauli digitization lacks the code-correctability condition

File/lines: `tutorial/12-error-correction.md:67-72,201`.

What is wrong: the chapter says correcting `{X,Y,Z}` suffices immediately after introducing a repetition code that does not correct all three.

Why it is wrong: linearity says correcting a set of Pauli errors corrects their linear combinations only when the recovery satisfies the quantum error-correction conditions for that Pauli set.

Proposed fix:

```diff
--- a/tutorial/12-error-correction.md
+++ b/tutorial/12-error-correction.md
@@
-- The four Paulis $\{I,X,Y,Z\}$ are a complete basis for any $2\times2$ operator
+- Within the computational subspace, the four Paulis $\{I,X,Y,Z\}$ are a complete basis for any $2\times2$ operator
@@
-- What's left is a single, *known* Pauli (up to a stabilizer) that the decoder removes.
+- For a code whose recovery corrects that Pauli set, what's left is a single, *known* Pauli (up to a stabilizer) that the decoder removes.
@@
-Correcting those three corrects *all* small errors.
+In a full single-qubit-error-correcting code, correcting those three corrects arbitrary single-qubit errors.
@@
-- Stabilizer measurement **digitizes** continuous noise: expanding any error in $\{I,X,Y,Z\}$ and collapsing onto one Pauli means correcting $\{X,Y,Z\}$ suffices.
+- Stabilizer measurement **digitizes** continuous noise: for a code that corrects the full single-qubit Pauli set, expanding errors in $\{I,X,Y,Z\}$ and projecting onto a syndrome makes finite recovery possible.
```

### 6. Nit - Stabilizer operators are conflated with measurements

File/lines: `tutorial/12-error-correction.md:12,39`.

What is wrong: the text says the correlation measurements are called stabilizers.

Why it is wrong: stabilizers are commuting Pauli operators; syndrome extraction measures their eigenvalues, usually through ancillas.

Proposed fix:

```diff
--- a/tutorial/12-error-correction.md
+++ b/tutorial/12-error-correction.md
@@
-These correlation measurements are called **stabilizers**.
+The Pauli correlation operators are **stabilizers**; their measured eigenvalues are the **syndrome**.
@@
-Instead of measuring any qubit, we measure two **parity-check stabilizers**:
+Instead of measuring any data qubit directly, we measure the eigenvalues of two **parity-check stabilizer operators**:
```

## Pure Style Preferences

These are not correctness findings and should not block scientific fixes.

- Several chapters use casual analogies effectively, but the mathematical definitions should come before the analogy when a convention is fragile, especially for `sigma_z`, `alpha`, and `chi`.
- ASCII diagrams are useful for Markdown portability. When a diagram is schematic, label it as schematic and avoid implying it came from numerical diagonalization.
- Prefer one notation lane per paragraph: energy (`E`), angular frequency (`omega`), or cyclic frequency (`f`). Switching lanes is where most of the real errors above entered.

## Execution Summary

- Tutorials 01-05: Markdown-only; no direct executable examples in this range.
- Tutorial 06 paired lab:
  - file: `hands-on/04-dispersive-readout/dispersive.py`;
  - command: `cd hands-on\04-dispersive-readout; python dispersive.py`.
- Tutorial 07 paired labs:
  - file: `hands-on/01-bloch-sphere/bloch.py`;
  - command: `cd hands-on\01-bloch-sphere; python bloch.py`;
  - file: `hands-on/02-rabi/rabi.py`;
  - command: `cd hands-on\02-rabi; python rabi.py`.
- Tutorial 08: Markdown-only; no paired executable example found.
- Tutorial 09 paired lab:
  - file: `hands-on/03-t1-t2/t1_t2.py`;
  - command: `cd hands-on\03-t1-t2; python t1_t2.py`.
- Tutorials 10-12: Markdown-only; no paired executable examples found.
- Initial Tutorial 06 run failed before dependency installation with `ModuleNotFoundError: No module named 'matplotlib'`.
- After installing `hands-on/requirements.txt`, the Tutorial 06 lab executed successfully with plotting disabled:
  - reported fields: `|0>` at `I=-0.8000, Q=-0.4000`; `|1>` at `I=+0.8000, Q=-0.4000`;
  - magnitudes: `0.8944` for both;
  - IQ separation: `1.6000`;
  - warning: Matplotlib font-cache permission warning from sandboxed home directory, not a repository code failure.
- The successful run verifies the dimensionless steady-state separation claimed by the lab text, while also exposing the 1000x unit-label/time-axis error described above.
- Tutorial 07 Bloch lab executed successfully with plotting disabled:
  - `|0>`: `<sx>=0`, `<sy>=0`, `<sz>=+1`;
  - `|1>`: `<sx>=0`, `<sy>=0`, `<sz>=-1`;
  - `|+>`: `<sx>=+1`; `|+i>`: `<sy>=+1`;
  - Rabi drive: `Omega/2pi=5.000 MHz`, pi pulse `0.1000 us`, minimum `<sz>=-1.000`.
- Tutorial 07 Rabi lab executed successfully with plotting disabled:
  - input `5 MHz`: extracted `4.995 MHz`, period `200 ns`, pi time `100 ns`;
  - input `10 MHz`: extracted `9.990 MHz`, period `100 ns`, pi time `50 ns`;
  - input `20 MHz`: extracted `19.980 MHz`, period `50 ns`, pi time `25 ns`.
- Tutorial 09 T1/T2 lab executed successfully with plotting disabled:
  - input `T1=30.00 us`, fitted `T1=30.00 us`;
  - predicted Markovian `T2=24.00 us`, fitted envelope `23.99 us`;
  - `1/(2T1)+1/Tphi = 0.04167 1/us`, measured `1/T2=0.04169 1/us`, relative error `0.05%`.
- The repeated Matplotlib warning about inability to write `C:\Users\Marti\.matplotlib\fontlist-v3.11.0.json.matplotlib-lock` is environmental, not a repository code failure.
