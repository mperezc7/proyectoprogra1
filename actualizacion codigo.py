# TPO : Registro de asistencia
# 2 usuarios (usuario observador, admin modifica)

from datetime import datetime

def inicializar_asistencia(sesiones):
    return [[0] * len(sesiones) for _ in range(len(estudiantes))]

def agregar_estudiante(estudiantes, sesiones, asistencia, nombre):
    estudiante = {"nombre": nombre, "fecha_baja": None, "justificacion_baja": None}
    estudiantes.append(estudiante)
    asistencia.append([0] * len(sesiones))
    print(f"Estudiante '{nombre}' agregado.")
    return estudiantes, asistencia

def agregar_sesion(sesiones, asistencia, sesion):
    sesiones.append(sesion)
    for fila in asistencia:
        fila.append(0)
    print(f"Sesión '{sesion}' agregada.")
    return sesiones, asistencia

def obtener_fecha():
    return datetime.now()

def verificar_estado_usuario(fecha_baja, fecha_registro):
    if fecha_baja is None:
        return True
    if fecha_registro <= fecha_baja:
        return True
    else:
        return False

def registrar_asistencia(estudiantes, sesiones, asistencia, estudiante_index, sesion_index):
    if estudiante_index < 0 or estudiante_index >= len(estudiantes) or \
       sesion_index < 0 or sesion_index >= len(sesiones):
        print("Índice de estudiante o sesión no válido.")
        return asistencia

    estudiante = estudiantes[estudiante_index]
    fecha_actual = obtener_fecha()

    if verificar_estado_usuario(estudiante["fecha_baja"], fecha_actual):
        asistencia[estudiante_index][sesion_index] = 1  # 1 para presente
        print(f"Asistencia registrada para '{estudiante['nombre']}' en la sesión '{sesiones[sesion_index]}'.")
    else:
        print(f"El estudiante '{estudiante['nombre']}' está dado de baja y no puede registrar asistencia.")
    
    return asistencia

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
    print("\nAsistencia:")
    print("Estudiantes:", [e["nombre"] for e in estudiantes])
    print("Sesiones:", sesiones)
    for i in range(len(estudiantes)):
        print(f"{estudiantes[i]['nombre']}: ", end="")
        for j in range(len(sesiones)):
            print("P" if asistencia[i][j] == 1 else "A", end=" ")
        print()

def main():
    estudiantes = []
    sesiones = []
    asistencia = []

    while True:
        print("\n----- MENÚ -----")
        print("1. Agregar Estudiante")
        print("2. Agregar Sesión")
        print("3. Registrar Asistencia")
        print("4. Mostrar Asistencia")
        print("5. Dar de Baja Estudiante")
        print("6. Contar Estudiantes Vigentes")
        print("7. Calcular Inasistencia de un Estudiante")
        print("8. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre_estudiante = input("Ingrese el nombre del estudiante: ")
            estudiantes, asistencia = agregar_estudiante(estudiantes, sesiones, asistencia, nombre_estudiante)
        elif opcion == '2':
            nombre_sesion = input("Ingrese el nombre de la sesión: ")
            sesiones, asistencia = agregar_sesion(sesiones, asistencia, nombre_sesion)
        elif opcion == '3':
            if not estudiantes or not sesiones:
                print("Debe haber al menos un estudiante y una sesión para registrar asistencia.")
                continue
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input(f"Ingrese el índice del estudiante (0 a {len(estudiantes) - 1}): "))
            for idx, ses in enumerate(sesiones):
                print(f"{idx}: {ses}")
            sesion_index = int(input(f"Ingrese el índice de la sesión (0 a {len(sesiones) - 1}): "))
            asistencia = registrar_asistencia(estudiantes, sesiones, asistencia, estudiante_index, sesion_index)
        elif opcion == '4':
            mostrar_asistencia(estudiantes, sesiones, asistencia)
        elif opcion == '5':
            if not estudiantes:
                print("No hay estudiantes para dar de baja.")
                continue
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input(f"Ingrese el índice del estudiante a dar de baja (0 a {len(estudiantes) - 1}): "))
            estudiantes = dar_de_baja_usuario(estudiantes, estudiante_index)
        elif opcion == '6':
            vigentes = contar_usuarios_vigentes(estudiantes)
            print(f"Cantidad de estudiantes vigentes: {vigentes}")
        elif opcion == '7':
            if not estudiantes or not sesiones:
                print("Debe haber al menos un estudiante y sesiones para calcular inasistencia.")
                continue
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input(f"Ingrese el índice del estudiante (0 a {len(estudiantes) - 1}): "))
            calcular_inasistencia_estudiante(estudiantes, sesiones, asistencia, estudiante_index)
        elif opcion == '8':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()