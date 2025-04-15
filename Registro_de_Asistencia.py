#TPO : Registro de asistencia
#2usuarios(usu observador, adm modifica)

def inicializar_asistencia(sesiones):
    return [[0] * len(sesiones) for _ in range(len(estudiantes))]

def agregar_estudiante(estudiantes, sesiones, asistencia, nombre):
    estudiantes.append(nombre)
    # Inicializar la fila de asistencia para el nuevo estudiante
    # Asegurarse de que la fila tenga el mismo número de columnas que sesiones
    asistencia.append([0] * len(sesiones))
    print(f"Estudiante '{nombre}' agregado.")
    return estudiantes, asistencia

def agregar_sesion(sesiones, asistencia, sesion):
    sesiones.append(sesion)
    # Agregar una nueva columna en la matriz de asistencia
    for fila in asistencia:
        fila.append(0)
    print(f"Sesión '{sesion}' agregada.")
    return sesiones, asistencia

def registrar_asistencia(estudiantes, sesiones, asistencia, estudiante_index, sesion_index):
    if estudiante_index < 0 or estudiante_index >= len(estudiantes) or \
       sesion_index < 0 or sesion_index >= len(sesiones):
        print("Índice de estudiante o sesión no válido.")
        return asistencia
    asistencia[estudiante_index][sesion_index] = 1  # 1 para presente
    print(f"Asistencia registrada para '{estudiantes[estudiante_index]}' en la sesión '{sesiones[sesion_index]}'.")
    return asistencia

def mostrar_asistencia(estudiantes, sesiones, asistencia):
    print("Asistencia:")
    for i in range(len(estudiantes)):
        print(f"{estudiantes[i]}: ", end="")
        for j in range(len(sesiones)):
            print("P" if asistencia[i][j] == 1 else "A", end=" ")
        print()  # Nueva línea

def main():
    estudiantes = []
    sesiones = []
    asistencia = []

    while True:
        print("\n1. Agregar Estudiante")
        print("2. Agregar Sesión")
        print("3. Registrar Asistencia")
        print("4. Mostrar Asistencia")
        print("5. Salir")
        
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
            estudiante_index = int(input("Ingrese el índice del estudiante (0 a {}): ".format(len(estudiantes) - 1)))
            sesion_index = int(input("Ingrese el índice de la sesión (0 a {}): ".format(len(sesiones) - 1)))
            asistencia = registrar_asistencia(estudiantes, sesiones, asistencia, estudiante_index, sesion_index)
        elif opcion == '4':
            mostrar_asistencia(estudiantes, sesiones, asistencia)
        elif opcion == '5':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
