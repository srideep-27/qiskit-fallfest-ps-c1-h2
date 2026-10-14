# Qiskit Fall Fest 2026 Phase 1 — PS-C1: H₂ Energy Estimation

## Project overview

This project estimates the ground-state energy of H₂ near its equilibrium bond length using the Variational Quantum Eigensolver (VQE). It compares the same optimized circuit on two simulated processor layouts.

## Current results

- Bond length: 0.7414 Å
- Exact Hamiltonian reference: -1.137279 Hartree
- Ideal VQE energy: -1.137279 Hartree
- Noisy energy on Processor A: -0.904377 Hartree
- Noisy energy on Processor B: -0.904377 Hartree
- Processor A: 5 physical qubits, compiled width 5, depth 91, 56 CX gates
- Processor B: 9 physical qubits, compiled width 9, depth 91, 56 CX gates

Both processors produced the same reported noisy energy and absolute error in this run. These results apply to this particular circuit and the configured simulated noise model.

## Report

See [report.md](report.md) for the methodology, benchmark tables, discussion, and limitations.

## Run the project

Open PowerShell in this project folder.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the setup check:

```powershell
python test_setup.py
```

Open `main.ipynb` in VS Code and run its cells to inspect the notebook results.

## Processor configurations

- `processors/processor_A.json`: 5-qubit linear layout
- `processors/processor_B.json`: 9-qubit layout with additional connections

Both configurations use the same configured noise rates and transpilation settings.
