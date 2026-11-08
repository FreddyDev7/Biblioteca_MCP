# Biblioteca MCP — Cliente y servidor en Python

Proyecto educativo que implementa una biblioteca ficticia con 20 libros en
JSON y dos herramientas MCP:

- `buscar_libro(texto)`: busca por título, autor, categoría o descripción.
- `consultar_disponibilidad(libro_id)`: consulta cuántos ejemplares están disponibles.

Está desarrollado con el **SDK oficial MCP para Python 2.x** y utiliza el
transporte **stdio**. No necesita API key ni conexión a un modelo de lenguaje.

## Requisitos

- Python 3.11 o superior.
- VS Code recomendado.
- Git (para publicar el repositorio).
- Conexión a Internet solo para instalar la dependencia la primera vez.

## Estructura

```text
biblioteca-mcp/
├── .gitignore
├── .vscode/
│   └── mcp.json
├── data/
│   └── libros.json
├── src/
│   └── biblioteca_mcp/
│       ├── __init__.py
│       ├── catalogo.py
│       ├── cliente.py
│       └── server.py
├── tests/
│   ├── test_catalogo.py
│   └── test_mcp.py
├── INVESTIGACION.txt
├── README.md
├── pyproject.toml
└── requirements.txt
```

## 1. Preparar el entorno (Windows / VS Code)

Abre la carpeta del proyecto en VS Code y una terminal PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Si PowerShell bloquea la activación del entorno, puedes ejecutar los comandos
usando directamente `.venv\Scripts\python.exe`, sin activar el entorno.

## 2. Ejecutar el cliente y probar la conexión MCP

Desde la raíz del proyecto:

```powershell
python -m biblioteca_mcp.cliente
```

Si el paquete no se encuentra, comprueba que ejecutaste `pip install -e .`
desde la raíz y que VS Code está usando el intérprete `.venv`.

El cliente inicia automáticamente el servidor como subproceso stdio, descubre
sus herramientas, busca la categoría `programación` y consulta disponibilidad
para cada coincidencia. No abras `server.py` manualmente en otra terminal:
el cliente se encarga de iniciarlo.

## 3. Ejecutar las pruebas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas comprueban:

1. Búsqueda por categoría.
2. Consulta de un libro existente (`LIB-001`).
3. Consulta de un identificador con formato correcto pero inexistente (`LIB-999`).
4. Rechazo de un identificador con formato inválido (`ABC`).
5. Integración cliente-servidor MCP en memoria y descubrimiento de herramientas.

## 4. Inspeccionar el servidor con MCP Inspector (opcional)

Con Node.js instalado:

```powershell
npx -y @modelcontextprotocol/inspector
```

Selecciona conexión local/stdio y configura el comando Python del entorno
virtual con el argumento absoluto a `src/biblioteca_mcp/server.py`.
El Inspector permite listar y ejecutar las herramientas manualmente.

También se incluye `.vscode/mcp.json` como configuración de descubrimiento
de herramientas MCP en VS Code compatible. VS Code requiere una versión
compatible y el modo Agente de GitHub Copilot para invocar herramientas MCP.
La configuración incluida apunta al intérprete del entorno virtual de Windows
(`.venv\\Scripts\\python.exe`). En macOS/Linux, cambia esa ruta por
`${workspaceFolder}/.venv/bin/python`.

## 5. Ejemplo esperado

Búsqueda `programación` devuelve varios libros. Para cada libro el cliente
imprime título, autor, identificador y ejemplares disponibles. Por ejemplo:

```text
Herramientas disponibles: buscar_libro, consultar_disponibilidad

Búsqueda: programación
- Python desde cero — Lucía Herrera [LIB-001]: 2 disponible(s)
...
```

Los resultados exactos dependen del contenido de `data/libros.json`.

## 6. Contrato de las herramientas

### `buscar_libro(texto: str)`

`texto` es obligatorio y debe ser una cadena no vacía. La búsqueda ignora
mayúsculas/minúsculas y revisa título, autor, categoría y descripción.
La respuesta es JSON serializado con `ok`, `cantidad`, `resultados` y `mensaje`.

### `consultar_disponibilidad(libro_id: str)`

`libro_id` es obligatorio. Formato válido: `LIB-001`. La respuesta distingue:

- `ok: true`: libro encontrado, con `ejemplares_disponibles` y `disponible`.
- `codigo: LIBRO_NO_ENCONTRADO`: formato correcto, pero no existe ese ID.
- `codigo: ID_INVALIDO`: formato incorrecto.

## 7. Publicar en GitHub

Crea un repositorio vacío en GitHub y, desde la terminal en la raíz:

```powershell
git init
git add .
git commit -m "Crear servidor y cliente MCP de biblioteca"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/biblioteca-mcp.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu usuario y la URL por la dirección real del
repositorio. No subas `.venv`, claves, tokens ni archivos `.env`.

## 8. ¿Por qué VS Code y no Google Colab?

Se recomienda VS Code. Este proyecto usa stdio: el cliente lanza un proceso
Python local y conversa con él por stdin/stdout. Ese ciclo de vida es natural
en VS Code y permite después conectar el servidor a un host MCP real.

Colab está diseñado para notebooks remotos y añade fricción para lanzar y
mantener procesos stdio. Se puede adaptar, pero no es la opción más clara
para aprender la arquitectura cliente-servidor MCP local.

## 9. Investigación

Lee `INVESTIGACION.txt` para la explicación breve solicitada sobre el cliente,
el servidor y la descripción de argumentos de las herramientas.

## Referencias oficiales

- [SDK oficial MCP para Python](https://py.sdk.modelcontextprotocol.io/)
- [Documentación del cliente](https://py.sdk.modelcontextprotocol.io/client/)
- [Ejecución y transportes del servidor](https://py.sdk.modelcontextprotocol.io/run/)
- [Conectar un servidor a VS Code](https://py.sdk.modelcontextprotocol.io/get-started/real-host/)
- [Repositorio oficial del SDK](https://github.com/modelcontextprotocol/python-sdk)

## Licencia

MIT. Consulta `LICENSE`.
