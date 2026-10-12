import numpy as np
from qiskit.quantum_info import SparsePauliOp

# H2 Hamiltonian in the STO-3G basis, mapped to four qubits.
# The published coefficients use a bond length of 0.7414 angstrom.
hamiltonian = SparsePauliOp.from_list([
    ("IIII", -0.81262),
    ("IIIZ",  0.17120),
    ("IIZI",  0.17120),
    ("IZII", -0.22279),
    ("ZIII", -0.22279),
    ("IIZZ",  0.16862),
    ("IZIZ",  0.12054),
    ("ZIIZ",  0.16587),
    ("IZZI",  0.16587),
    ("ZIZI",  0.12054),
    ("ZZII",  0.17435),
    ("YYXX", -0.04532),
    ("XYYX",  0.04532),
    ("YXXY",  0.04532),
    ("XXYY", -0.04532),
])

# Diagonalize the Hamiltonian to find its lowest electronic energy.
electronic_energy = np.linalg.eigvalsh(hamiltonian.to_matrix())[0]

# Add the repulsion between the two hydrogen nuclei.
bond_length_angstrom = 0.7414
angstroms_per_bohr = 0.529177210903
nuclear_repulsion = angstroms_per_bohr / bond_length_angstrom

total_energy = electronic_energy + nuclear_repulsion

print(f"Bond length:       {bond_length_angstrom} angstrom")
print(f"Electronic energy: {electronic_energy:.6f} Hartree")
print(f"Nuclear repulsion: {nuclear_repulsion:.6f} Hartree")
print(f"Total H2 energy:   {total_energy:.6f} Hartree")