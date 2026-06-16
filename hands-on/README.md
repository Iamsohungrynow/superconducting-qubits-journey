# Hands-On Track

These labs let you simulate and run the physics from the tutorial chapters on your own laptop. Each lab is a small, self-contained QuTiP simulation that turns a chapter's equations into something you can plot, tweak, and explore. No hardware, no accounts, and no lab setup are needed. Everything runs locally in pure simulation, so you can start experimenting right away.

## Setup

Install the dependencies with pip:

```
pip install qutip matplotlib numpy scipy
```

Note: the labs use QuTiP's core API, which is identical across QuTiP 4.7+ and 5.x. The labs were verified on qutip 4.7.5, numpy 1.22, scipy 1.6, and matplotlib 3.3.

## Simulation labs (QuTiP)

| Lab | Topic | Theory chapter |
| --- | --- | --- |
| [01-bloch-sphere/](01-bloch-sphere/) | Qubit states and the Bloch sphere | [tutorial/07-single-qubit-gates.md](../tutorial/07-single-qubit-gates.md) |
| [02-rabi/](02-rabi/) | Rabi oscillations | [tutorial/07-single-qubit-gates.md](../tutorial/07-single-qubit-gates.md) |
| [03-t1-t2/](03-t1-t2/) | T1 relaxation and T2 dephasing | [tutorial/09-coherence-noise.md](../tutorial/09-coherence-noise.md) |
| [04-dispersive-readout/](04-dispersive-readout/) | Dispersive readout (qubit-state-dependent cavity) | [tutorial/06-readout.md](../tutorial/06-readout.md) |

## Roadmap

- [x] QuTiP simulation labs: available now
- [ ] Run on real IBM hardware (Qiskit + IBM Quantum): planned
- [ ] Characterize real devices (Qibocal / Qibolab): planned

## See also

- [Repository overview](../README.md)
- [Tutorial chapters](../tutorial/README.md)
