from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure_all()

simulator = AerSimulator()
compiled_circuit = transpile(circuit, simulator)
result = simulator.run(
    compiled_circuit,
    shots=1000,
    seed_simulator=42,
).result()

print("Measurement counts:", result.get_counts())