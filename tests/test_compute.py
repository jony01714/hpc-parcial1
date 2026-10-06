import numpy as np

from src.compute import f, process_chunk, run_sequential


def test_f_valores_conocidos():
    valores = np.array([1.0, 2.0, 4.0])

    esperado = (
        np.sqrt(valores)
        + valores**2
        + np.sin(valores)
        + np.cos(valores)
        + np.log(valores)
    )

    resultado = f(valores)

    np.testing.assert_allclose(resultado, esperado)


def test_run_sequential_igual_a_f():
    data = np.array([1.0, 2.0, 3.0, 4.0])

    esperado = f(data)
    resultado = run_sequential(data)

    np.testing.assert_array_equal(resultado, esperado)


def test_process_chunk_igual_a_f():
    chunk = np.array([2.0, 3.0, 4.0])

    esperado = f(chunk)
    resultado = process_chunk(chunk)

    np.testing.assert_array_equal(resultado, esperado)