import asyncio
import json
import unittest
from mcp import Client
from biblioteca_mcp.server import mcp

def parse_result(result):
    if result.is_error:
        raise AssertionError("La herramienta MCP indicó error.")
    return json.loads(result.content[0].text)

class MCPIntegrationTests(unittest.TestCase):
    def test_cliente_lista_y_ejecuta_herramientas(self):
        async def scenario():
            async with Client(mcp) as client:
                tools = await client.list_tools()
                names = {tool.name for tool in tools.tools}
                self.assertIn("buscar_libro", names)
                self.assertIn("consultar_disponibilidad", names)

                found = parse_result(await client.call_tool("buscar_libro", {"texto": "Python"}))
                self.assertGreater(found["cantidad"], 0)

                valid = parse_result(await client.call_tool(
                    "consultar_disponibilidad", {"libro_id": "LIB-001"}))
                self.assertTrue(valid["ok"])

                missing = parse_result(await client.call_tool(
                    "consultar_disponibilidad", {"libro_id": "LIB-999"}))
                self.assertEqual(missing["codigo"], "LIBRO_NO_ENCONTRADO")

                invalid = parse_result(await client.call_tool(
                    "consultar_disponibilidad", {"libro_id": "ABC"}))
                self.assertEqual(invalid["codigo"], "ID_INVALIDO")
        asyncio.run(scenario())

if __name__ == "__main__":
    unittest.main()
