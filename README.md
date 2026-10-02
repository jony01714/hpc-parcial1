# HPC Parcial 1 — Comparación de ejecución secuencial vs. paralela

## Objetivo

Comparar la ejecución secuencial y paralela de una función matemática sobre un arreglo grande de datos, midiendo tiempo de ejecución, speedup y eficiencia con 1, 2 y 4 workers.

## Estructura del repositorio

```
hpc-parcial1/
├── src/
│ ├── compute.py # funcion f(x) y logica secuencial/paralela
│ ├── benchmark.py # mide tiempos, calcula speedup y eficiencia
│ └── plot_results.py # genera grafica de resultados
├── results/
│ ├── results.csv # resultados del benchmark (no versionado)
│ └── performance_plot.png # grafica generada (no versionado)
├── analisis.ipynb # notebook con desarrollo, experimentacion y graficas
├── requirements.txt
└── README.md
```

## Requisitos

```bash
pip install -r requirements.txt
```

## Cómo ejecutar

> **Nota:** en la máquina usada para el desarrollo solo existe el comando `python3` (no `python`), por eso los ejemplos usan `python3`. Dentro de un entorno virtual activado, `python` también funciona.

```bash
python3 src/benchmark.py --size 20000000 --workers 1 2 4 --repeats 3
python3 src/benchmark.py --heavy --size 2000000 --workers 1 2 4 --repeats 3
python3 src/plot_results.py
```

O abrir `analisis.ipynb`, que corre ambos pasos y muestra resultados y gráfica inline.

## Metodología

- **Función de prueba:** f(x) = sqrt(x) + x² + sin(x) + cos(x) + log(x)
- **Secuencial:** un solo proceso procesa todo el arreglo.
- **Paralela:** `ProcessPoolExecutor` divide el arreglo en `n_workers` partes y las procesa en paralelo.
- Cada configuración (1, 2, 4 workers) se corre 3 veces; se reporta el promedio.
- **Speedup:** S_p = T_1 / T_p
- **Eficiencia:** E_p = S_p / p

## Resultados

_(completar después de correr el benchmark: tabla de tiempos, speedup y eficiencia, y referencia a la gráfica en `results/performance_plot.png`)_

## Análisis

_(responder brevemente, con base en los resultados obtenidos)_

1. ¿La ejecución paralela fue más rápida que la secuencial?
2. ¿Qué número de workers obtuvo el menor tiempo?
3. ¿Duplicar el número de workers duplicó el rendimiento? ¿Por qué?
4. ¿Por qué el problema seleccionado puede paralelizarse?
5. ¿En qué momento agregar más workers deja de ser beneficioso?
6. ¿Qué limitaciones tiene el hardware utilizado?
7. ¿Este experimento representa HPC o solamente demuestra principios utilizados en HPC? Justifiquen.

## Flujo de trabajo (GitFlow)

- `main`: versión final estable que se entrega.
- `develop`: rama de integración de todas las features antes de pasar a main.
- `feature/*`: una rama por persona/tarea, con Pull Request hacia develop.

## Equipo

- Jonathan Gonzalez — implementación secuencial y paralela, benchmark
- Javier Yael Narváez Olguín — gráfica de rendimiento
- [Nombre compañero 2] — análisis de resultados
