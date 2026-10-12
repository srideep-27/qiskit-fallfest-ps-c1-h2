\# Qiskit Fall Fest 2026 Phase 1 — PS-C1: H₂ Energy Estimation



This project estimates the ground-state energy of H₂ near its equilibrium bond length and compares a VQE circuit on two simulated processor layouts.



\## Current results



\- Bond length: 0.7414 Å

\- Exact Hamiltonian reference: -1.137279 Hartree

\- Ideal VQE energy: -1.137279 Hartree

\- Noisy energy on Processor A: -0.904377 Hartree

\- Noisy energy on Processor B: -0.904377 Hartree

\- Both compiled circuits: width 5/9, depth 91, and 56 CX gates



See \[`report.md`](report.md) for the method, results, and discussion.



\## Run the project



Open PowerShell in this project folder. Activate the virtual environment:



```powershell

.\\.venv\\Scripts\\Activate.ps1

