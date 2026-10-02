import numpy as np

from src.compute import f


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