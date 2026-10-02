"""
benchmark.py
Mide el tiempo de ejecucion secuencial y paralela sobre un arreglo grande
de datos, con 1, 2 y 4 workers, 3 repeticiones por configuracion, y guarda
los resultados en results/results.csv (o results/results_heavy.csv con --heavy).
"""
import argparse
import csv
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from compute import (
    process_chunk,
    process_chunk_heavy,
    run_sequential,
    run_sequential_heavy,
)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def run_parallel(data: np.ndarray, n_workers: int, chunk_fn) -> np.ndarray:
    chunks = np.array_split(data, n_workers)
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(chunk_fn, chunks))
    return np.concatenate(results)


def time_once(data: np.ndarray, n_workers: int, seq_fn, chunk_fn) -> float:
    start = time.perf_counter()
    if n_workers == 1:
        seq_fn(data)
    else:
        run_parallel(data, n_workers, chunk_fn)
    return time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser(description="Benchmark secuencial vs paralelo")
    parser.add_argument("--size", type=int, default=20_000_000,
                         help="Cantidad de elementos a procesar")
    parser.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4],
                         help="Cantidades de workers a probar")
    parser.add_argument("--repeats", type=int, default=3,
                         help="Repeticiones por configuracion")
    parser.add_argument("--heavy", action="store_true",
                         help="Usa f_heavy (mayor carga computacional por elemento)")
    args = parser.parse_args()

    seq_fn = run_sequential_heavy if args.heavy else run_sequential
    chunk_fn = process_chunk_heavy if args.heavy else process_chunk
    output_name = "results_heavy.csv" if args.heavy else "results.csv"
    results_path = os.path.join(RESULTS_DIR, output_name)

    data = np.linspace(1.0, args.size, args.size)  # empieza en 1.0, evita log(0)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = []

    for n_workers in args.workers:
        times = []
        for i in range(args.repeats):
            t = time_once(data, n_workers, seq_fn, chunk_fn)
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
    with open(results_path, "w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Resultados guardados en {os.path.relpath(results_path)}")


if __name__ == "__main__":
    main()
