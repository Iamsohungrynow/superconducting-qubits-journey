# Before you start: notation and numerical habits

This book uses two kinds of numerical models: circuit spectra and time evolution.
Keep their units separate. Read this page once, then keep it beside your editor.

| Quantity | Meaning | Code convention |
|---|---|---|
| $E_C,E_J$ | energies | Spectrum lab uses $E/h$ in GHz |
| $f$ | cycles per second | MHz = cycles per microsecond |
| $\omega,\Omega,g,\alpha,\chi$ | angular frequencies | Dynamics labs use rad/us, usually `2*np.pi*f_MHz` |
| $H$ in the dynamics scripts | actually $H/\hbar$ | Multiply by time in us to obtain a dimensionless phase |
| $\kappa$ | photon-number decay rate | Population decays as $e^{-\kappa t}$; field as $e^{-\kappa t/2}$ |
| $T_1,T_2,T_\phi$ | time constants | us in labs 01–06; seconds in lab 11 |
| $n$ in a charge basis | signed Cooper-pair number | Integer charge states, including negative integers |
| $a^\dagger a$ | excitation number | Nonnegative oscillator Fock number; different from Cooper-pair number |

For example, `g = 2*np.pi*100` means $g/2\pi=100$ MHz.
The excitation-swap time $\pi/(2g)$ is then 0.0025 us, or 2.5 ns.
In a static diagonalization of $H/h$, no extra $2\pi$ is needed to obtain
transition frequencies from energy differences.

## Ground state and signs

All scripts use `basis(2, 0)` as the ground state and `basis(2, 1)` as the
excited state. Computational $Z=\mathrm{diag}(1,-1)$ gives ground-state
expectation $+1$, so the free qubit Hamiltonian is $-\omega_q Z/2$.
The physical lowering operator is `destroy(2)`, or $|0\rangle\langle1|$.
QuTiP's `sigmam()` uses a spin convention and is not that matrix.

Chapter 05 uses the common atomic convention
$\sigma_z=|e\rangle\langle e|-|g\rangle\langle g|=-Z$.
Substitute $\sigma_z=-Z$ to translate its Hamiltonians into the code.
Chapters 06–07 use computational $Z$ directly.

Detuning is always a **signed difference**, but the pair being compared changes:

| Context | Definition |
|---|---|
| Qubit–cavity (05–06, lab 10) | $\Delta=\omega_q-\omega_r$ |
| Driven qubit (07, Ramsey lab) | $\Delta_d=\omega_d-\omega_q$ |
| Two qubits (08, CZ lab) | $\Delta=\omega_1-\omega_2$ |
| Driven cavity (lab 04) | $\delta=\widetilde\omega_r-\omega_d$ |

For a transmon, $\alpha=\omega_{12}-\omega_{01}<0$.
Its signed half-separation of readout resonances is
$\chi=g^2\alpha/[\Delta(\Delta+\alpha)]$ in second-order perturbation theory.
Writing the resonances as $\widetilde\omega_r\mp\chi$ uses their **dressed midpoint**;
it is not generally the uncoupled cavity frequency. Lab 04 chooses positive
$\chi$ for a simple pointer-field example; the negative-detuning worked
example in the text has negative $\chi$.

## What makes a simulation trustworthy?

1. Predict a limiting case before running: no drive, no coupling, or no noise.
2. Compare a numerical result with an independent analytic identity.
3. Increase the Hilbert-space cutoff and tighten the integrator tolerances.
4. Separate numerical convergence from physical validity. A perfectly converged
   two-level model cannot predict transmon leakage.
5. Check the requested observable. Low final leakage does not establish an X
   gate; a conditional phase near pi does not establish CZ.

The [lab runner](../hands-on/README.md) implements checks of these kinds.
For stochastic simulations, zero observed failures is not a zero failure
probability: zero events in $N$ independent trials gives an approximate 95%
upper bound $3/N$.

[Start the learning path](learning-path.md) · [Chapter index](README.md)
