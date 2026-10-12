"""Small helper functions for comparing processor benchmark results."""


def absolute_error(energy, reference_energy):
    """Return the distance between an energy result and its reference."""
    return abs(energy - reference_energy)


def make_result_row(
    processor,
    logical_qubits,
    physical_qubits,
    compiled_width,
    depth,
    cx_gates,
    noisy_energy,
    reference_energy,
):
    """Collect one processor's measurements into a dictionary."""
    return {
        "processor": processor,
        "logical_qubits": logical_qubits,
        "physical_qubits": physical_qubits,
        "compiled_width": compiled_width,
        "depth": depth,
        "cx_gates": cx_gates,
        "noisy_energy_hartree": noisy_energy,
        "exact_reference_hartree": reference_energy,
        "absolute_error_hartree": absolute_error(
            noisy_energy, reference_energy
        ),
    }