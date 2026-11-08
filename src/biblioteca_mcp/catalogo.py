"""Acceso y lógica de negocio del catálogo de libros."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG_PATH = PROJECT_ROOT / "data" / "libros.json"
ID_PATTERN = re.compile(r"^LIB-\d{3}$")


class CatalogError(Exception):
    """Error esperado al consultar el catálogo."""


def cargar_libros(ruta: Path | str = DEFAULT_CATALOG_PATH) -> list[dict[str, Any]]:
    """Carga y valida superficialmente el archivo JSON del catálogo."""
    path = Path(ruta)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CatalogError(f"No se encontró el archivo de catálogo: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CatalogError(f"El catálogo JSON no es válido: {exc}") from exc
    if not isinstance(data, list):
        raise CatalogError("El catálogo debe contener una lista de libros.")
    return data


def buscar_libro(texto: str, ruta: Path | str = DEFAULT_CATALOG_PATH) -> dict[str, Any]:
    """
    Busca sin distinguir mayúsculas/minúsculas en título, autor, categoría
    y descripción. Devolver categoría permite búsquedas como 'programación'.
    """
    if not isinstance(texto, str) or not texto.strip():
        return {"ok": False, "mensaje": "El texto de búsqueda no puede estar vacío.", "resultados": []}
    termino = texto.casefold().strip()
    coincidencias = []
    for libro in cargar_libros(ruta):
        campos = ("titulo", "autor", "categoria", "descripcion")
        if any(termino in str(libro.get(campo, "")).casefold() for campo in campos):
            coincidencias.append(libro)
    return {
        "ok": True,
        "consulta": texto.strip(),
        "cantidad": len(coincidencias),
        "resultados": coincidencias,
        "mensaje": f"Se encontraron {len(coincidencias)} libro(s)." if coincidencias else "No se encontraron libros."
    }


def consultar_disponibilidad(libro_id: str, ruta: Path | str = DEFAULT_CATALOG_PATH) -> dict[str, Any]:
    """Consulta los ejemplares disponibles de un libro."""
    if not isinstance(libro_id, str) or not ID_PATTERN.fullmatch(libro_id.strip()):
        return {
            "ok": False, "codigo": "ID_INVALIDO",
            "mensaje": "Identificador inválido. El formato esperado es LIB-001."
        }
    buscado = libro_id.strip().upper()
    for libro in cargar_libros(ruta):
        if libro.get("id") == buscado:
            disponibles = int(libro.get("ejemplares_disponibles", 0))
            return {
                "ok": True, "libro_id": buscado, "titulo": libro.get("titulo"),
                "ejemplares_disponibles": disponibles,
                "disponible": disponibles > 0,
                "mensaje": f"Hay {disponibles} ejemplar(es) disponible(s)."
            }
    return {
        "ok": False, "codigo": "LIBRO_NO_ENCONTRADO",
        "libro_id": buscado, "mensaje": f"No existe un libro con identificador {buscado}."
    }
