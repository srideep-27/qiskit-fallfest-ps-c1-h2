"""Four-qubit H2 Hamiltonian and molecular constants."""

import numpy as np
from qiskit.quantum_info import SparsePauliOp

bond_length_angstrom = 0.7414
angstroms_per_bohr = 0.529177210903

# STO-3G H2 electronic Hamiltonian, mapped to four qubits.
hamiltonian = SparsePauliOp.from_list([
    ("IIII", -0.81262),
    ("IIIZ", 0.17120),
    ("IIZI", 0.17120),
    ("IZII", -0.22279),
    ("ZIII", -0.22279),
    ("IIZZ", 0.16862),
    ("IZIZ", 0.12054),
    ("ZIIZ", 0.16587),
    ("IZZI", 0.16587),
    ("ZIZI", 0.12054),
    ("ZZII", 0.17435),
    ("YYXX", -0.04532),
    ("XYYX", 0.04532),
    ("YXXY", 0.04532),
    ("XXYY", -0.04532),
])

electronic_energy = float(np.linalg.eigvalsh(hamiltonian.to_matrix())[0])
nuclear_repulsion = angstroms_per_bohr / bond_length_angstrom
total_energy = electronic_energy + nuclear_repulsion
