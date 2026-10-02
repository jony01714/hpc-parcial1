"""
plot_results.py
Lee los resultados del benchmark (results/results.csv y, si existe,
results/results_heavy.csv) y genera la grafica de rendimiento:
Numero de workers vs. tiempo de ejecucion.
Las imagenes se guardan en results/performance_plot.png
(y results/performance_plot_heavy.png para la carga pesada).
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")  # permite generar la imagen sin abrir ventana
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def load_results(path: str) -> dict:
    """Lee el CSV del benchmark y regresa listas por columna."""
    with open(path, newline="") as f_in:
        rows = list(csv.DictReader(f_in))
    return {
        "workers": [int(r["workers"]) for r in rows],
        "promedio": [float(r["promedio"]) for r in rows],
    }


def plot(data: dict, title: str, output_path: str) -> None:
    """Dibuja workers vs. tiempo promedio y guarda la imagen."""
    workers = data["workers"]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.suptitle(title, fontsize=12)

    ax.bar([str(w) for w in workers], data["promedio"], color="#4C72B0")
    for i, t in enumerate(data["promedio"]):
        ax.text(i, t, f"{t:.3f}s", ha="center", va="bottom", fontsize=9)
    ax.set_title("Tiempo promedio de ejecucion")
    ax.set_xlabel("Workers")
    ax.set_ylabel("Tiempo (s)")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Grafica guardada en {output_path}")


def main():
    experiments = [
        ("results.csv", "performance_plot.png",
         "Rendimiento: f(x) = sqrt(x) + x^2 + sin(x) + cos(x) + log(x)"),
        ("results_heavy.csv", "performance_plot_heavy.png",
         "Rendimiento: carga pesada (f_heavy)"),
    ]

    found_any = False
    for csv_name, png_name, title in experiments:
        csv_path = os.path.join(RESULTS_DIR, csv_name)
        if not os.path.exists(csv_path):
            print(f"No se encontro {csv_path}, se omite.")
            continue
        found_any = True
        plot(load_results(csv_path), title, os.path.join(RESULTS_DIR, png_name))

    if not found_any:
        print("No hay resultados. Primero corre: python3 src/benchmark.py")


if __name__ == "__main__":
    main()
