
import unittest

class TestAsistencia(unittest.TestCase):
    def test_estado_usuario_activo(self):
        from datetime import datetime, timedelta
        from main import verificar_estado_usuario
        hoy = datetime.now()
        self.assertTrue(verificar_estado_usuario(None, hoy))
        self.assertTrue(verificar_estado_usuario(hoy + timedelta(days=1), hoy))
        self.assertFalse(verificar_estado_usuario(hoy - timedelta(days=1), hoy))

    def test_guardar_y_cargar_estudiantes_json(self):
        from main import guardar_estudiantes_json, cargar_estudiantes_json
        estudiantes = [{"legajo": 1, "nombre": "Test Alumno", "correo": "test@uade.edu.ar", "materias": [], "fecha_baja": None}]
        guardar_estudiantes_json(estudiantes, "test_estudiantes.json")
        cargados = cargar_estudiantes_json("test_estudiantes.json")
        self.assertEqual(estudiantes, cargados)

if __name__ == "__main__":
    unittest.main()
