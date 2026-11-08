"""Servidor MCP de la biblioteca. El transporte predeterminado es stdio."""
import json
from mcp.server import MCPServer
from biblioteca_mcp.catalogo import buscar_libro as buscar_en_catalogo
from biblioteca_mcp.catalogo import consultar_disponibilidad as consultar_en_catalogo

mcp = MCPServer(
    "biblioteca-mcp",
    instructions=(
        "Servidor de consulta de una biblioteca ficticia. "
        "Usa buscar_libro para encontrar libros por título, autor o categoría; "
        "usa consultar_disponibilidad con el identificador exacto para conocer "
        "los ejemplares disponibles."
    ),
)

@mcp.tool()
def buscar_libro(texto: str) -> str:
    """Busca libros por palabras del título, autor, categoría o descripción.

    Args:
        texto: Palabra o fragmento que se desea buscar. Ejemplos: 'Python',
            'Lucía Herrera' o 'programación'.
    """
    return json.dumps(buscar_en_catalogo(texto), ensure_ascii=False)

@mcp.tool()
def consultar_disponibilidad(libro_id: str) -> str:
    """Devuelve cuántos ejemplares están disponibles para un libro.

    Args:
        libro_id: Identificador del catálogo con formato LIB-001.
    """
    return json.dumps(consultar_en_catalogo(libro_id), ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()
