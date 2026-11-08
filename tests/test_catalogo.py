import unittest
from biblioteca_mcp.catalogo import buscar_libro, consultar_disponibilidad

class CatalogoTests(unittest.TestCase):
    def test_buscar_por_categoria(self):
        resultado = buscar_libro("programación")
        self.assertTrue(resultado["ok"])
        self.assertGreater(resultado["cantidad"], 0)

    def test_libro_existente(self):
        resultado = consultar_disponibilidad("LIB-001")
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["ejemplares_disponibles"], 2)

    def test_libro_inexistente(self):
        resultado = consultar_disponibilidad("LIB-999")
        self.assertFalse(resultado["ok"])
        self.assertEqual(resultado["codigo"], "LIBRO_NO_ENCONTRADO")

    def test_identificador_invalido(self):
        resultado = consultar_disponibilidad("XYZ")
        self.assertFalse(resultado["ok"])
        self.assertEqual(resultado["codigo"], "ID_INVALIDO")

    def test_busqueda_sin_resultados(self):
        resultado = buscar_libro("este libro no existe")
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["cantidad"], 0)

if __name__ == "__main__":
    unittest.main()
