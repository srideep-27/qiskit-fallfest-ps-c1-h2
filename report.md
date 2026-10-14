# H₂ Energy Estimation — PS-C1

## Goal

Estimate the ground-state energy of H₂ near its equilibrium bond length and compare one VQE circuit on two simulated processor layouts.

## Method

The H₂ electronic Hamiltonian was evaluated at a bond length of 0.7414 Å. The exact reference energy was calculated by diagonalizing the Hamiltonian. A UCCSD ansatz and VQE were used to obtain ideal parameters. The optimized circuit was then transpiled for Processor A and Processor B.

Both processor simulations use the configured noise rates: single-qubit depolarizing error 0.001, CX depolarizing error 0.005, and readout error 0.01. The configured shot count is 4096.

## Results

| Measure | Result |
|---|---:|
| Bond length | 0.7414 Å |
| Exact Hamiltonian reference | -1.137279 Hartree |
| Ideal VQE energy | -1.137279 Hartree |
| Noisy energy, Processor A | -0.904377 Hartree |
| Noisy energy, Processor B | -0.904377 Hartree |
| Absolute energy error for each processor | 0.232902 Hartree |

| Processor | Available qubits | Compiled width | Depth | CX gates |
|---|---:|---:|---:|---:|
| A | 5 | 5 | 91 | 56 |
| B | 9 | 9 | 91 | 56 |

## Discussion

The ideal VQE energy matches the exact Hamiltonian reference to the displayed precision. In the saved benchmark results, both noisy simulations report the same energy and absolute error.

Processor B has more available qubits and additional coupling edges, but the current results do not show a reduction in circuit depth or CX-gate count for this circuit. The transpiled circuit metrics and noisy energy calculation should be checked together before drawing a firm conclusion about connectivity. The reported noisy energy evaluates the optimized ideal VQE parameters; it does not demonstrate noise-aware re-optimization.

## Limitations

These results cover one H₂ geometry, one ansatz, one set of transpilation settings, and one configured noise model. They do not establish that the processor layouts perform equally for other circuits or larger problems. The reported metrics do not include a verified SWAP-overhead comparison.

## Conclusion

The saved results show an ideal energy of -1.137279 Hartree and identical reported noisy energies of -0.904377 Hartree for both processor configurations. Before submission, rerun and validate the benchmark to ensure the noisy energy and compiled-circuit metrics are consistently produced by the intended processor configurations.
