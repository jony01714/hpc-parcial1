"""
benchmark.py
Mide el tiempo de ejecucion secuencial y paralela de compute.f sobre un
arreglo grande de datos, con 1, 2 y 4 workers, 3 repeticiones por
configuracion, y guarda los resultados en results/results.csv.
"""
import argparse
import csv
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from compute import process_chunk, run_sequential

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "results.csv")


def run_parallel(data: np.ndarray, n_workers: int) -> np.ndarray:
    """Divide data en n_workers partes y las procesa en paralelo con
    ProcessPoolExecutor. Reensambla el resultado en el orden original."""
    chunks = np.array_split(data, n_workers)
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(process_chunk, chunks))
    return np.concatenate(results)


def time_once(data: np.ndarray, n_workers: int) -> float:
    start = time.perf_counter()
    if n_workers == 1:
        run_sequential(data)
    else:
        run_parallel(data, n_workers)
    return time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser(description="Benchmark secuencial vs paralelo")
    parser.add_argument("--size", type=int, default=20_000_000,
                         help="Cantidad de elementos a procesar")
    parser.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4],
                         help="Cantidades de workers a probar")
    parser.add_argument("--repeats", type=int, default=3,
                         help="Repeticiones por configuracion")
    args = parser.parse_args()

    data = np.linspace(1.0, args.size, args.size)  # empieza en 1.0, evita log(0)

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    rows = []

    for n_workers in args.workers:
        times = []
        for i in range(args.repeats):
            t = time_once(data, n_workers)
            times.append(t)
            print(f"workers={n_workers} prueba={i+1} tiempo={t:.4f}s")
        avg = sum(times) / len(times)
        row = {"workers": n_workers, "promedio": avg}
        for i, t in enumerate(times):
            row[f"prueba_{i+1}"] = t
        rows.append(row)
        print(f"-> workers={n_workers} promedio={avg:.4f}s\n")

    t1 = next(r["promedio"] for r in rows if r["workers"] == 1)
    for r in rows:
        r["speedup"] = t1 / r["promedio"]
        r["eficiencia"] = r["speedup"] / r["workers"]

    fieldnames = ["workers"] + [f"prueba_{i+1}" for i in range(args.repeats)] + ["promedio", "speedup", "eficiencia"]
    with open(RESULTS_PATH, "w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Resultados guardados en {RESULTS_PATH}")


if __name__ == "__main__":
    main()
