import numpy as np
from qiskit import transpile
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_aer.primitives import Estimator as AerEstimator

from .problem import hamiltonian as original_hamiltonian
from .problem import nuclear_repulsion
from .processors import load_processor

# Match the Hamiltonian's qubit order to Qiskit Nature's Hartree-Fock state.
reordered_terms = []
for label, coefficient in zip(
    original_hamiltonian.paulis.to_labels(),
    original_hamiltonian.coeffs,
):
    reordered_label = label[0] + label[2] + label[1] + label[3]
    reordered_terms.append((reordered_label, coefficient))

hamiltonian = SparsePauliOp.from_list(reordered_terms)
total_hamiltonian = hamiltonian + SparsePauliOp.from_list([
    ("IIII", nuclear_repulsion)
])

# Find the ideal VQE solution once, then compile that same circuit for A and B.
mapper = JordanWignerMapper()
initial_state = HartreeFock(2, (1, 1), mapper)
ansatz = UCCSD(2, (1, 1), mapper, initial_state=initial_state)

solver = VQE(
    estimator=StatevectorEstimator(),
    ansatz=ansatz,
    optimizer=COBYLA(maxiter=500),
    initial_point=np.zeros(ansatz.num_parameters),
)
vqe_result = solver.compute_minimum_eigenvalue(total_hamiltonian)
optimized_circuit = ansatz.assign_parameters(vqe_result.optimal_parameters)

exact_energy = float(
    np.linalg.eigvalsh(total_hamiltonian.to_matrix())[0]
)
print(f"Ideal VQE energy: {vqe_result.optimal_value:.6f} Hartree")
print(f"Exact reference:  {exact_energy:.6f} Hartree")
for filename in [
    "processors/processor_A.json",
    "processors/processor_B.json",
]:
    config, simulator = load_processor(filename)

    directed_edges = []
    for qubit_a, qubit_b in config["coupling_edges"]:
        directed_edges.append([qubit_a, qubit_b])
        directed_edges.append([qubit_b, qubit_a])

    compiled = transpile(
        optimized_circuit,
        basis_gates=config["basis_gates"],
        coupling_map=directed_edges,
        optimization_level=config["transpilation"]["optimization_level"],
        seed_transpiler=config["transpilation"]["seed_transpiler"],
    )

    operations = compiled.count_ops()

    estimator = AerEstimator(
        backend_options={
            "noise_model": simulator.options.noise_model,
            "basis_gates": config["basis_gates"],
            "coupling_map": directed_edges,
        },
        transpile_options={
            "basis_gates": config["basis_gates"],
            "coupling_map": directed_edges,
            "optimization_level": config["transpilation"]["optimization_level"],
            "seed_transpiler": config["transpilation"]["seed_transpiler"],
        },
        run_options={
            "shots": config["transpilation"]["shots"],
            "seed_simulator": 42,
        },
    )

    noisy_result = estimator.run(
        [optimized_circuit],
        [total_hamiltonian],
    ).result()

    noisy_energy = float(np.real(noisy_result.values[0]))
    energy_error = abs(noisy_energy - exact_energy)

    print(
        f"{config['name']}: "
        f"physical qubits={config['num_qubits']}, "
        f"compiled width={compiled.num_qubits}, "
        f"depth={compiled.depth()}, "
        f"CX gates={operations.get('cx', 0)}, "
        f"noisy energy={noisy_energy:.6f} Hartree, "
        f"absolute error={energy_error:.6f} Hartree"
    )
