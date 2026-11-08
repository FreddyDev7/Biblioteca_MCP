"""Cliente MCP de demostración: inicia el servidor local mediante stdio."""
from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path
from mcp import Client, StdioServerParameters

SERVER_FILE = Path(__file__).with_name("server.py")

def leer_respuesta(result) -> dict:
    """Las herramientas devuelven JSON en un bloque de texto."""
    if result.is_error:
        raise RuntimeError("El servidor MCP devolvió un error.")
    for block in result.content:
        if getattr(block, "type", None) == "text":
            return json.loads(block.text)
    raise RuntimeError("La respuesta MCP no contiene un bloque de texto JSON.")

async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_FILE)],
    )
    async with Client(params) as client:
        tools = await client.list_tools()
        print("Herramientas disponibles:", ", ".join(tool.name for tool in tools.tools))

        consulta = "programación"
        print(f"\nBúsqueda: {consulta}")
        encontrados = leer_respuesta(await client.call_tool("buscar_libro", {"texto": consulta}))
        for libro in encontrados["resultados"]:
            disponibilidad = leer_respuesta(
                await client.call_tool("consultar_disponibilidad", {"libro_id": libro["id"]})
            )
            estado = f'{disponibilidad["ejemplares_disponibles"]} disponible(s)'
            print(f'- {libro["titulo"]} — {libro["autor"]} [{libro["id"]}]: {estado}')

if __name__ == "__main__":
    asyncio.run(main())
