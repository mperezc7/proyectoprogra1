from datetime import datetime

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
def dic_a_matriz(lista):
    m=[]
    for dic in lista:
        m.append(list(dic.values()))
    return m
def mostrar_lista_estudiantes(matriz):
    for i in range (len(matriz)):
        for j in range(len(matriz[i])):
            a=matriz[i][j]
            a=str(a)
            print(f'{a:<20}', end=' ')
        print()
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
    estudiantes = [{'legajo':11111, 'nombre':'leo Castillo','correo':'abc1@gmail.edu.ar','materias':['fisica', 'progra1']},
                   {'legajo':11112, 'nombre':'caro Casto','correo':'abc2@gmail.edu.ar','materias':['progra1']},
                   {'legajo':11113, 'nombre':'andres julio','correo':'abc3@gmail.edu.ar','materias':None}]
    materias = ['proga1']
    Nclases=['cl1','cl2']
    asistencia = []

    while True:
        print("\n----- MENÚ -----")
        print("1. Agregar Estudiante")
        print("2. Agregar Clases")
        print("3. Registrar Asistencia")
        print("4. Mostrar Asistencia")
        print("5. Dar de Baja Estudiante")
        print("6. Contar Estudiantes Vigentes")
        print("7. Calcular Inasistencia de un Estudiante")
        print("8. Mostrar lista de estudiantes")
        print("9. Salir")
        
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
           print("\n--- Submenú: Agregar Estudiante ---")
           nombre = ""
           legajo = ""
           correo = ""
           while True:
               print("\n--- Opciones de ingreso ---")
               print("1. Ingresar nombre del estudiante")
               print("2. Ingresar legajo del estudiante")
               print("3. Ingresar correo del estudiante")
               print("4. Guardar estudiante")
               print("5. Cancelar")
               subopcion = input("Seleccione una opción: ")
               if subopcion == '1':
                   nombre = input("Ingrese el nombre del estudiante: ")
               elif subopcion == '2':
                   legajo = input("Ingrese el legajo del estudiante: ")
               elif subopcion == '3':
                   correo = input("Ingrese el correo del estudiante: ")
               elif subopcion == '4':
                   if not (nombre and legajo and correo):
                       print("Faltan datos. Asegúrese de ingresar nombre, legajo y correo.")
                   else:
                       estudiante = {
                           "legajo": legajo,
                           "nombre": nombre,
                           "correo": correo,
                           "fecha_baja": None
                       }
                       estudiantes.append(estudiante)
                       asistencia.append([0] * len(sesiones))
                       print(f"Estudiante '{nombre}' agregado correctamente.")
                       break
               elif subopcion == '5':
                   print("Operación cancelada.")
                   break
               else:
                   print("Opción no válida. Intente de nuevo.")
        elif opcion == '2':
            nombre_clase = input("Ingrese el nombre de la clase: ")
            sesiones, asistencia = agregar_sesion(sesiones, asistencia, nombre_clase)
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
            matriz=dic_a_matriz(estudiantes)
            for i in list(estudiantes[0]):
                print(f'{i:<20}',end=" ")
            print()
            mostrar_lista_estudiantes(matriz)
        elif opcion == '9':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()