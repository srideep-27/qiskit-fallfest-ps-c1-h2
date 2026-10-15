# Qiskit Fall Fest 2026 Phase 1 — PS-C1: H₂ Energy Estimation

## Project overview

This project estimates the ground-state energy of hydrogen (H₂) near its equilibrium bond length. It compares an exact Hamiltonian reference and an ideal variational quantum eigensolver (VQE) result with noisy simulations on two processor layouts.

## Current recorded results

- Bond length: 0.7414 Å
- Exact Hamiltonian reference: -1.137279 Hartree
- Ideal VQE energy: -1.137279 Hartree
- Noisy energy on Processor A: -0.904377 Hartree
- Noisy energy on Processor B: -0.904377 Hartree
- Processor A: 5 physical qubits, compiled width 5, depth 91, 56 CX gates
- Processor B: 9 physical qubits, compiled width 9, depth 91, 56 CX gates

These values describe this circuit and the configured simulated noise model. The noisy runs evaluate the ideal VQE parameters; they are not re-optimized under noise, and they are not results from physical quantum hardware.

## What the project does

1. Builds the four-qubit H₂ Hamiltonian in the STO-3G basis at 0.7414 Å.
2. Finds an exact reference by diagonalizing the Hamiltonian matrix.
3. Uses a UCCSD ansatz and VQE to estimate the ground-state energy.
4. Compiles the same optimized circuit for both processor coupling maps.
5. Applies the configured gate and readout noise settings with 4096 shots.
6. Saves processor metrics to a CSV table and creates an energy comparison chart.

## Setup

Use Python 3.10 or newer. From the project folder, create and activate a virtual environment, then install the packages.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python` and `.\.venv\Scripts\pip.exe` in place of `pip`.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the project

Run these commands from the project folder with the virtual environment active:

```bash
python -m src.benchmark
python -m src.visualization
```

The benchmark refreshes `results/tables/architecture_metrics.csv`. The visualization command refreshes `results/figures/energy_comparison.png`. You can also open `main.ipynb` in VS Code or Jupyter and run its cells to recalculate the results.

## Project files

- `src/problem.py` — H₂ Hamiltonian and molecular constants.
- `src/vqe.py` — standalone ideal VQE calculation.
- `src/benchmark.py` — exact reference, ideal VQE, noisy processor runs, and CSV output.
- `src/processors.py` — processor configurations and noise models.
- `src/visualization.py` — energy comparison chart.
- `processors/` — simulated connectivity, noise, and shot settings.
- `results/` — metrics table and chart.
- `report.md` — methodology, results, interpretation, and limitations.
- `main.ipynb` — runnable notebook summary.
