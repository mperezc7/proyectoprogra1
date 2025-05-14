from datetime import datetime
from .estudiantes import agregar_estudiante, buscar_estudiantes_por_nombre
from .sesiones import agregar_sesion
from .asistencia import registrar_asistencia
def dar_de_baja_usuario(estudiantes, estudiante_index):
    if estudiante_index < 0 or estudiante_index >= len(estudiantes):
        print("Índice de estudiante no válido.")
        return estudiantes

    estudiante = estudiantes[estudiante_index]
    if estudiante["fecha_baja"] is not None:
        print(f"El estudiante '{estudiante['nombre']}' ya fue dado de baja el {estudiante['fecha_baja']}.")
    else:
        estudiante["fecha_baja"] = obtener_fecha()
        justificacion = input(f"Ingrese la justificación de la baja para '{estudiante['nombre']}': ")
        estudiante["justificacion_baja"] = justificacion
        print(f"Estudiante '{estudiante['nombre']}' dado de baja correctamente en {estudiante['fecha_baja']}.")
    
    return estudiantes
def obtener_fecha():
    return datetime.now()
def contar_usuarios_vigentes(estudiantes):
    ahora = datetime.now()
    cantidad_vigentes = 0
    for estudiante in estudiantes:
        fecha_baja = estudiante.get("fecha_baja")
        if fecha_baja is None or fecha_baja > ahora:
            cantidad_vigentes += 1
    return cantidad_vigentes

def calcular_inasistencia_estudiante(estudiantes, sesiones, asistencia, estudiante_index):
    if estudiante_index < 0 or estudiante_index >= len(estudiantes):
        print("Índice de estudiante no válido.")
        return None

    total_sesiones = len(sesiones)
    if total_sesiones == 0:
        print("No hay sesiones registradas.")
        return None

    asistencias = asistencia[estudiante_index]
    cantidad_ausencias = asistencias.count(0)
    porcentaje_inasistencia = (cantidad_ausencias / total_sesiones) * 100

    estudiante = estudiantes[estudiante_index]
    print(f"\nEstudiante: {estudiante['nombre']}")
    print(f"Inasistencia: {porcentaje_inasistencia:.2f}% ({cantidad_ausencias} ausencias de {total_sesiones} sesiones)")

    return porcentaje_inasistencia

def mostrar_asistencia(estudiantes, sesiones, asistencia):
    print("\nAsistencia de Estudiantes:")
    for i, estudiante in enumerate(estudiantes):
        print(f"Nombre: {estudiante['nombre']}, Email: {estudiante['email']}")
        for j, sesion in enumerate(sesiones):
            estado = "Presente" if asistencia[i][j] == 1 else "Ausente"
            print(f"  {sesion}: {estado}")
    print("\n")

def menu():
    estudiantes = []
    sesiones = []
    asistencia = []

    while True:
        print("Menú:")
        print("1. Agregar Estudiante")
        print("2. Agregar Sesión")
        print("3. Registrar Asistencia")
        print("4. Mostrar Asistencia")
        print("5. Buscar Estudiantes")
        print("6. Dar de Baja Estudiante")
        print("7. Contar Estudiantes Vigentes")
        print("8. Calcular Inasistencia de un Estudiante")
        print("9. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del estudiante: ")
            email = input("Ingrese el correo electrónico del estudiante: ")
            agregar_estudiante(estudiantes, nombre, email)

        elif opcion == '2':
            sesion = input("Ingrese el nombre de la sesión: ")
            agregar_sesion(sesiones, sesion)

        elif opcion == '3':
            mostrar_asistencia(estudiantes, sesiones, asistencia)  # Mostrar asistencia antes de registrar
            estudiante_index = int(input("Ingrese el índice del estudiante (0 para el primero): "))
            sesion_index = int(input("Ingrese el índice de la sesión (0 para la primera): "))
            registrar_asistencia(asistencia, estudiante_index, sesion_index)

        elif opcion == '4':
            mostrar_asistencia(estudiantes, sesiones, asistencia)

        elif opcion == '5':
            nombre_busqueda = input("Ingrese el nombre a buscar: ")
            resultados_busqueda = buscar_estudiantes_por_nombre(estudiantes, nombre_busqueda)
            print("Resultados de búsqueda:")
            for estudiante in resultados_busqueda:
                print(estudiante["nombre"])
        elif opcion == '6':
            if not estudiantes:
                print("No hay estudiantes para dar de baja.")
                continue
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input(f"Ingrese el índice del estudiante a dar de baja (0 a {len(estudiantes) - 1}): "))
            estudiantes = dar_de_baja_usuario(estudiantes, estudiante_index)
        elif opcion == '7':
            vigentes = contar_usuarios_vigentes(estudiantes)
            print(f"Cantidad de estudiantes vigentes: {vigentes}")
        elif opcion == '8':
            if not estudiantes or not sesiones:
                print("Debe haber al menos un estudiante y sesiones para calcular inasistencia.")
                continue
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input(f"Ingrese el índice del estudiante (0 a {len(estudiantes) - 1}): "))
            calcular_inasistencia_estudiante(estudiantes, sesiones, asistencia, estudiante_index)
        elif opcion == '9':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")
if __name__ == '__main__':
    menu()