# Ramsey versus Hahn echo from a noise spectrum

Pairs with tutorial chapter 09; see the [learning path](../../tutorial/learning-path.md) and [notation](../../tutorial/00-notation.md).

## What you simulate

Slow fluctuations $\delta f(t)$ of the qubit frequency scramble the phase of a
superposition. For classical, stationary, Gaussian noise the coherence decays as
$e^{-\chi(t)}$ with

$$\chi(t)=\frac{(2\pi)^2}{2}\int_0^\infty S_f(f)\,|G(f,t)|^2\,df ,$$

where $S_f$ is the one-sided power spectral density of the frequency noise (in
Hz$^2$/Hz) and $|G|^2$ is the filter function of the pulse sequence. Ramsey and
Hahn echo differ only in their filters:

$$|G_R|^2=t^2\,\frac{\sin^2(\pi ft)}{(\pi ft)^2},\qquad
|G_E|^2=t^2\,\frac{\sin^4(\pi ft/2)}{(\pi ft/2)^2}.$$

Ramsey passes noise down to DC; the echo filter vanishes at $f=0$. The lab
integrates both against a $1/f$ spectrum, $S_f=(10\text{ kHz})^2/f$ between
1 Hz and 100 MHz. That amplitude is exactly the Chapter 09 worked example: flux
noise of $1\ \mu\Phi_0/\sqrt{\text{Hz}}$ on a $10$ GHz/$\Phi_0$ flank. It then
multiplies by the independent relaxation envelope $e^{-t/2T_1}$ with $T_1=100$ us.

## Predict, then run

The chapter predicts $T_2^*\approx7$ us for Ramsey (with a realistic logarithmic
cutoff factor) and a pure-dephasing echo time $T_2^E=\sqrt{2/\ln2}/(2\pi\cdot10^4\,\text{Hz})\approx27$ us.
Which of the two do you expect to move if the 1 Hz infrared cutoff changes?

From the **repository root**, after the [shared setup](../README.md):

```bash
python hands-on/11-noise-echo/echo.py
```

```bash
python hands-on/run_labs.py 11 --check
```

The first command opens a plot. The second runs without a display and fails if a numerical checkpoint is violated. Both save the figure beside the script.

## The code explained

**Filters on a grid.** `filters(f, t)` returns $|G_R|^2$ and $|G_E|^2$ for every
frequency and time at once. NumPy's `np.sinc(x)` is $\sin(\pi x)/(\pi x)$, so the
formulas read almost exactly as above:

```python
x = f[:, None]*t[None, :]
ramsey = t[None, :]**2*np.sinc(x)**2
echo = t[None, :]**2*np.sin(np.pi*x/2)**2*np.sinc(x/2)**2
```

**The integral.** The dephasing exponent is $2\pi^2\int S_f|G|^2df$, evaluated
with `np.trapezoid` on 12 000 logarithmically spaced frequencies. The script
recomputes it on a grid twice as dense and asserts agreement to 0.2%, a
numerical-convergence check rather than a physics check.

**Physics checks.** It confirms that the echo filter is exactly zero at $f=0$
while the Ramsey filter equals $t^2$ there, and that echo preserves more
coherence than Ramsey at 25 us.

## Expected result

The default grid gives approximately 6.75 us Ramsey and 25.50 us echo 1/e times. These are grid crossings of nonexponential envelopes, not fitted Markovian rates. The echo value combines the 27 us pure-dephasing Gaussian with the $T_1$ envelope.

![Ramsey versus Hahn echo from a noise spectrum](figures/echo.png)

Left: the same noise gives very different coherence depending on the sequence;
the dashed line is the $T_1$-only ceiling $e^{-t/2T_1}$. Right: the two filters at
$t=20$ us; the echo filter falls as $f^2$ toward DC, where $1/f$ noise is largest.

## Experiment

Raise the infrared cutoff from 1 Hz to 100 Hz: Ramsey should improve more than echo. Replace the PSD with a constant and use a sufficiently wide frequency interval: ideal echo should no longer substantially improve white-noise dephasing.

Record your prediction, changed parameter, numerical result, and physical explanation. Edit one parameter at a time. The script's own convergence check recomputes the integral with the default 1 Hz cutoff and 1/f PSD (`dense_f` and `1e8/dense_f`), so change those too or it stops before printing; for the white-noise case also comment out the `assert` that echo beats Ramsey at 25 us, which can fail once the two agree to within cutoff and quadrature error. Restore the defaults before running the full verification suite.

## Model and numerical limits

Frequency is in Hz, time in seconds, and $S_f$ has units Hz$^2$/Hz. The cutoffs are part of the model. The script checks integration convergence and exact DC rejection. Pulses are instantaneous and perfect; the noise is classical, stationary and Gaussian. Telegraph noise from a few strongly coupled defects, or quantum noise at $\omega_q$ (which causes relaxation rather than dephasing), needs a different model.
