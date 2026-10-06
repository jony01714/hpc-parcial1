\# Guía de Contribución



\## Flujo de Trabajo

\- Crea siempre una rama a partir de `develop`: `git checkout -b feature/nombre-de-tu-rama`.

\- Realiza tus cambios en esa rama sin modificar archivos fuera de tu alcance asignado.



\## Formato de Commits

Usa los siguientes prefijos para los mensajes de commit:

\- `feat:` Nuevas funcionalidades.

\- `fix:` Corrección de errores.

\- `docs:` Cambios en la documentación.

\- `test:` Adición o modificación de pruebas.



\## Pruebas Locales

Antes de hacer push, ejecuta las pruebas localmente:

```bash

pytest tests/

