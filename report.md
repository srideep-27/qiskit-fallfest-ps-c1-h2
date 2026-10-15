# H₂ Energy Estimation — PS-C1

## Goal

Estimate the ground-state energy of H₂ near its equilibrium bond length and compare the same VQE circuit on two simulated processor layouts.

## Method

The molecule is modeled at a bond length of 0.7414 Å with a four-qubit Hamiltonian in the STO-3G basis. The exact reference is calculated by diagonalizing the Hamiltonian. VQE with a UCCSD ansatz finds ideal circuit parameters, and the optimized circuit is compiled for Processor A (5 qubits) and Processor B (9 qubits).

Both processor simulations use the same configured noise rates: single-qubit depolarizing error 0.001, CX depolarizing error 0.005, and readout error 0.01. The shot count is 4096. The noisy runs evaluate the ideal VQE parameters; they do not re-optimize them under noise.

## Results

| Measure | Result |
|---|---:|
| Bond length | 0.7414 Å |
| Exact Hamiltonian reference | -1.137279 Hartree |
| Ideal VQE energy | -1.137279 Hartree |
| Noisy energy, Processor A | -0.904377 Hartree |
| Noisy energy, Processor B | -0.904377 Hartree |
| Absolute error for either processor | 0.232902 Hartree |

| Processor | Available qubits | Compiled width | Circuit depth | CX gates |
|---|---:|---:|---:|---:|
| A | 5 | 5 | 91 | 56 |
| B | 9 | 9 | 91 | 56 |

Full precision values are in `results/tables/architecture_metrics.csv`. The chart is `results/figures/energy_comparison.png`.

## Discussion

The ideal VQE energy matches the exact reference to the displayed precision. The noisy energy is less negative, showing the effect of the configured gate and readout errors in this simulation.

Both processor simulations produced the same energy and circuit depth in this run. The four-qubit circuit fits the same connected chain on both layouts, so the additional qubits on Processor B did not change this small calculation. The reported metrics do not include a separate verified SWAP-overhead comparison.

## Limitations

These results cover one H₂ geometry, one ansatz, one set of transpilation settings, and one configured noise model. They are simulation results, not measurements on physical quantum hardware, and do not establish how the layouts compare for larger circuits. The ideal VQE parameters were not re-optimized under noise.

## Reproduce the results

Follow the setup instructions in `README.md`. Run `python -m src.benchmark` to update the CSV, then `python -m src.visualization` to regenerate the chart.
