"""
compute.py
Funcion matematica de prueba y versiones secuencial/paralela para procesarla
sobre un arreglo grande de datos.
"""
import numpy as np


def f(x: np.ndarray) -> np.ndarray:
    """f(x) = sqrt(x) + x^2 + sin(x) + cos(x) + log(x)

    x debe ser > 0 (por el log).
    """
    return np.sqrt(x) + x**2 + np.sin(x) + np.cos(x) + np.log(x)


def process_chunk(chunk: np.ndarray) -> np.ndarray:
    """Aplica f a un sub-arreglo. Es la unidad de trabajo que cada worker
    paralelo ejecuta sobre su porcion de datos."""
    return f(chunk)


def run_sequential(data: np.ndarray) -> np.ndarray:
    """Aplica f a todo el arreglo en un solo proceso, sin dividir el trabajo."""
    return process_chunk(data)


def f_heavy(x: np.ndarray, repetitions: int = 200) -> np.ndarray:
    """Version de f(x) con carga computacional artificialmente mayor.
    Suma series de sin(x*i)/i de forma acotada (no diverge), para que
    el computo por elemento domine sobre el overhead de comunicacion
    entre procesos, a diferencia del benchmark original."""
    total = np.zeros_like(x)
    for i in range(1, repetitions + 1):
        total += np.sin(x * i) / i
    return total


def process_chunk_heavy(chunk: np.ndarray) -> np.ndarray:
    """Equivalente a process_chunk pero usando f_heavy."""
    return f_heavy(chunk)


def run_sequential_heavy(data: np.ndarray) -> np.ndarray:
    """Equivalente a run_sequential pero usando f_heavy."""
    return process_chunk_heavy(data)
