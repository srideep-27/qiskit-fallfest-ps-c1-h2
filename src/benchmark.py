"""Run the H2 VQE and noisy processor-layout comparison."""

import csv
from pathlib import Path

import numpy as np
from qiskit import transpile
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import Estimator as AerEstimator
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper

from .problem import hamiltonian as original_hamiltonian
from .problem import nuclear_repulsion
from .processors import load_processor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSOR_CONFIGS = [
    PROJECT_ROOT / "processors" / "processor_A.json",
    PROJECT_ROOT / "processors" / "processor_B.json",
]
RESULTS_CSV = PROJECT_ROOT / "results" / "tables" / "architecture_metrics.csv"


def run_benchmark():
    """Compute ideal and noisy energies, then save comparable metrics."""
    # Match the Hamiltonian's qubit order to Qiskit Nature's Hartree-Fock state.
    reordered_terms = []
    for label, coefficient in zip(
        original_hamiltonian.paulis.to_labels(), original_hamiltonian.coeffs
    ):
        reordered_terms.append((label[0] + label[2] + label[1] + label[3], coefficient))

    electronic_hamiltonian = SparsePauliOp.from_list(reordered_terms)
    total_hamiltonian = electronic_hamiltonian + SparsePauliOp.from_list(
        [("IIII", nuclear_repulsion)]
    )
    exact_energy = float(np.linalg.eigvalsh(total_hamiltonian.to_matrix())[0])

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

    print(f"Bond length: {0.7414:.4f} angstrom")
    print(f"Exact reference: {exact_energy:.6f} Hartree")
    print(f"Ideal VQE:       {float(np.real(vqe_result.optimal_value)):.6f} Hartree")

    rows = []
    for config_path in PROCESSOR_CONFIGS:
        config, simulator = load_processor(config_path)
        coupling_map = [
            edge
            for first, second in config["coupling_edges"]
            for edge in ([first, second], [second, first])
        ]
        compiled = transpile(
            optimized_circuit,
            basis_gates=config["basis_gates"],
            coupling_map=coupling_map,
            optimization_level=config["transpilation"]["optimization_level"],
            seed_transpiler=config["transpilation"]["seed_transpiler"],
        )
        estimator = AerEstimator(
            backend_options={
                "noise_model": simulator.options.noise_model,
                "basis_gates": config["basis_gates"],
                "coupling_map": coupling_map,
            },
            transpile_options={
                "basis_gates": config["basis_gates"],
                "coupling_map": coupling_map,
                "optimization_level": config["transpilation"]["optimization_level"],
                "seed_transpiler": config["transpilation"]["seed_transpiler"],
            },
            run_options={
                "shots": config["transpilation"]["shots"],
                "seed_simulator": 42,
            },
        )
        noisy_result = estimator.run(
            [optimized_circuit], [total_hamiltonian]
        ).result()
        noisy_energy = float(np.real(noisy_result.values[0]))
        operations = compiled.count_ops()
        row = {
            "processor": config["name"].replace("Processor ", ""),
            "logical_qubits": optimized_circuit.num_qubits,
            "physical_qubits": config["num_qubits"],
            "compiled_width": compiled.num_qubits,
            "depth": compiled.depth(),
            "cx_gates": operations.get("cx", 0),
            "noisy_energy_hartree": noisy_energy,
            "exact_reference_hartree": exact_energy,
            "absolute_error_hartree": abs(noisy_energy - exact_energy),
        }
        rows.append(row)
        print(
            f"{config['name']}: noisy energy = {noisy_energy:.6f} Hartree, "
            f"absolute error = {row['absolute_error_hartree']:.6f} Hartree, "
            f"depth = {row['depth']}, CX gates = {row['cx_gates']}"
        )

    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved results to {RESULTS_CSV.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    run_benchmark()
