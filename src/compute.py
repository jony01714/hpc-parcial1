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
