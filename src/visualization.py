"""Create a figure comparing noisy processor energies with the reference."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "results" / "tables" / "architecture_metrics.csv"
FIGURE_PATH = PROJECT_ROOT / "results" / "figures" / "energy_comparison.png"


def create_energy_comparison():
    """Read the benchmark CSV and save an energy comparison chart."""
    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    processors = [row["processor"] for row in rows]
    noisy_energies = [
        float(row["noisy_energy_hartree"]) for row in rows
    ]
    reference_energy = float(rows[0]["exact_reference_hartree"])

    plt.figure(figsize=(7, 5))
    plt.bar(processors, noisy_energies, color=["steelblue", "darkorange"])
    plt.axhline(
        reference_energy,
        color="black",
        linestyle="--",
        label=f"Exact reference: {reference_energy:.6f} Hartree",
    )
    plt.ylabel("Energy (Hartree)")
    plt.title("H₂ Noisy Energy by Processor")
    plt.legend()
    plt.tight_layout()

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURE_PATH, dpi=200)
    plt.close()

    print(f"Saved figure to: {FIGURE_PATH}")


if __name__ == "__main__":
    create_energy_comparison()