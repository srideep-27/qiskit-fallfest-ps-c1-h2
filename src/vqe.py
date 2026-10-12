import numpy as np
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper

from problem import hamiltonian as original_hamiltonian
from problem import nuclear_repulsion


# Reorder the middle two qubits to match Qiskit Nature's
# Hartree-Fock spin-orbital ordering.
reordered_terms = []
for label, coefficient in zip(
    original_hamiltonian.paulis.to_labels(),
    original_hamiltonian.coeffs,
):
    reordered_label = label[0] + label[2] + label[1] + label[3]
    reordered_terms.append((reordered_label, coefficient))

hamiltonian = SparsePauliOp.from_list(reordered_terms)

# Include the hydrogen-nucleus repulsion.
nuclear_term = SparsePauliOp.from_list([
    ("IIII", nuclear_repulsion)
])
total_hamiltonian = hamiltonian + nuclear_term

# H2 has two spatial orbitals and two electrons.
mapper = JordanWignerMapper()
initial_state = HartreeFock(
    num_spatial_orbitals=2,
    num_particles=(1, 1),
    qubit_mapper=mapper,
)
ansatz = UCCSD(
    num_spatial_orbitals=2,
    num_particles=(1, 1),
    qubit_mapper=mapper,
    initial_state=initial_state,
)

vqe = VQE(
    estimator=StatevectorEstimator(),
    ansatz=ansatz,
    optimizer=COBYLA(maxiter=500),
    initial_point=np.zeros(ansatz.num_parameters),
)

result = vqe.compute_minimum_eigenvalue(total_hamiltonian)

exact_energy = (
    np.linalg.eigvalsh(hamiltonian.to_matrix())[0]
    + nuclear_repulsion
)

print(f"Exact reference: {exact_energy:.6f} Hartree")
print(f"VQE energy:      {result.optimal_value:.6f} Hartree")
print(f"VQE parameters:  {ansatz.num_parameters}")