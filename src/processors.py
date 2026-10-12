import json
from pathlib import Path

from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    ReadoutError,
    depolarizing_error,
)


def load_processor(config_path):
    """Load one processor's JSON settings and build its noisy simulator."""
    config_path = Path(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))

    # The JSON lists undirected connections; Qiskit uses both directions.
    directed_edges = []
    for qubit_a, qubit_b in config["coupling_edges"]:
        directed_edges.append([qubit_a, qubit_b])
        directed_edges.append([qubit_b, qubit_a])

    noise = NoiseModel()

    one_qubit_error = depolarizing_error(
        config["noise"]["one_qubit_depolarizing"], 1
    )
    noise.add_all_qubit_quantum_error(
        one_qubit_error, ["rz", "sx", "x"]
    )

    cx_error = depolarizing_error(
        config["noise"]["cx_depolarizing"], 2
    )
    noise.add_all_qubit_quantum_error(cx_error, ["cx"])

    readout_probability = config["noise"]["readout_error"]
    readout_error = ReadoutError([
        [1 - readout_probability, readout_probability],
        [readout_probability, 1 - readout_probability],
    ])
    noise.add_all_qubit_readout_error(readout_error)

    simulator = AerSimulator(
        noise_model=noise,
        basis_gates=config["basis_gates"],
        coupling_map=directed_edges,
    )

    return config, simulator