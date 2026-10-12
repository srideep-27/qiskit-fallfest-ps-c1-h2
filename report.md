\# H₂ Ground-State Energy and Processor Comparison



\## Goal



We estimated the ground-state energy of the hydrogen molecule (H₂) near its equilibrium bond length and compared how the same VQE circuit runs on two simulated processor layouts.



\## Method



We used an H₂ electronic Hamiltonian at a bond length of 0.7414 Å. The exact reference energy was calculated by diagonalizing this Hamiltonian. We then used a UCCSD VQE calculation to estimate the energy and transpiled the resulting circuit for Processor A and Processor B.



Both processor simulations used the same noise settings. The circuit was evaluated with 4096 shots.



\## Results



| Measure | Result |

|---|---:|

| Bond length | 0.7414 Å |

| Exact reference energy | -1.137279 Hartree |

| Ideal VQE energy | -1.137279 Hartree |

| Noisy energy, Processor A | -0.904377 Hartree |

| Noisy energy, Processor B | -0.904377 Hartree |

| Absolute error for each processor | 0.232902 Hartree |



| Processor | Available qubits | Compiled circuit width | Circuit depth | CX gates |

|---|---:|---:|---:|---:|

| A | 5 | 5 | 91 | 56 |

| B | 9 | 9 | 91 | 56 |



\## Discussion



The ideal VQE result matches the exact reference to the precision shown. With noise enabled, both processor simulations produced the same energy and absolute error in this run.



The equality is expected for this particular circuit and layout comparison. The calculation uses four logical qubits, and Processor B's connectivity includes the same four-qubit chain used by Processor A. The transpiler therefore produced circuits with the same depth and CX-gate count on both layouts. The extra qubits on Processor B did not help this small example.



The noisy results show a noticeable shift from the ideal energy. The reported noisy energies evaluate the ideal VQE parameters on the noisy simulators; the parameters were not re-optimized under noise. These results compare this circuit on the two configured layouts and do not establish that the processors perform equally for larger problems or other circuits.



\## Conclusion



For this four-qubit H₂ calculation, ideal VQE reproduced the exact reference energy. Under the configured noise, both processor layouts gave the same measured energy because the transpiled circuits had identical width, depth, and CX-gate count. A larger circuit or a layout that forces different routing would be needed to show a connectivity advantage for Processor B.

