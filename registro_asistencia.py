
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
    return fecha_baja is None or fecha_registro <= fecha_baja

def registrar_asistencia(estudiantes, sesiones, asistencia, estudiante_index, sesion_index):
    if estudiante_index < 0 or estudiante_index >= len(estudiantes) or        sesion_index < 0 or sesion_index >= len(sesiones):
        print("Índice de estudiante o sesión no válido.")
        return asistencia

    estudiante = estudiantes[estudiante_index]
    fecha_actual = obtener_fecha()

    if verificar_estado_usuario(estudiante["fecha_baja"], fecha_actual):
        asistencia[estudiante_index][sesion_index] = 1
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
    return sum(1 for estudiante in estudiantes if estudiante.get("fecha_baja") is None or estudiante["fecha_baja"] > ahora)

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
    return [list(dic.values()) for dic in lista]

def mostrar_lista_estudiantes(matriz):
    for fila in matriz:
        for valor in fila:
            print(f'{str(valor):<20}', end=' ')
        print()

def mostrar_asistencia(estudiantes, sesiones, asistencia):
    print("\nAsistencia:")
    print(f"{'':<20}",end=' ')
    for s in sesiones:
        print(f"{s:<7}",end=' ')
    print()
    for i, est in enumerate(estudiantes):
        print(f"{est['nombre']:<20}: ", end="")
        for j in range(len(sesiones)):
            print("P".ljust(7," ") if asistencia[i][j] == 1 else "A".ljust(7,' '), end=" ")
        print()

def archivo(matriz):
    try:
        with open('estud_matriz.txt','wt',encoding='UTF8') as arch:
            for est in matriz:
                linea = ";".join(map(str, est)) + "\n"
                arch.write(linea)
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")

def es_duplicado(campo, valor, estudiantes):
    return any(str(est[campo]).title() == str(valor).title() for est in estudiantes)

def submenu(estudiantes):
    nombre = ""
    legajo = ""
    correo = ""
    finalizar = False

    while not finalizar:
        print("--- Opciones de ingreso ---")
        print("1. Ingresar nombre del estudiante")
        print("2. Ingresar legajo del estudiante")
        print("3. Ingresar correo del estudiante")
        print("4. Guardar estudiante")
        print("5. Cancelar")
        try:
            subopcion = input("Seleccione una opción: ").strip()
            assert subopcion in {'1', '2', '3', '4', '5'}, "Opción inválida."

            if subopcion == '1':
                nuevo_nombre = input("Ingrese el nombre del estudiante: ").strip()
                assert nuevo_nombre, "El nombre no puede estar vacío."
                assert not es_duplicado("nombre", nuevo_nombre, estudiantes), "Nombre ya registrado."
                nombre = nuevo_nombre.title()

            elif subopcion == '2':
                nuevo_legajo = input("Ingrese el legajo del estudiante: ").strip()
                assert nuevo_legajo.isdigit(), "El legajo debe ser numérico."
                assert not es_duplicado("legajo", nuevo_legajo, estudiantes), "Legajo ya registrado."
                legajo = int(nuevo_legajo)

            elif subopcion == '3':
                nuevo_correo = input("Ingrese el correo del estudiante: ").strip()
                assert "@" in nuevo_correo and "." in nuevo_correo, "Correo no válido."
                assert not es_duplicado("correo", nuevo_correo, estudiantes), "Correo ya registrado."
                correo = nuevo_correo

            elif subopcion == '4':
                assert nombre and legajo and correo, "Faltan datos. Complete nombre, legajo y correo."
                estudiante = {
                    "legajo": legajo,
                    "nombre": nombre,
                    "correo": correo, 
                    "materias": None,
                    "fecha_baja": None,
                }
                estudiantes.append(estudiante)
                print(f"Estudiante '{nombre}' agregado correctamente.")
                finalizar = True

            elif subopcion == '5':
                print("Operación cancelada.")
                finalizar = True

        except AssertionError as error:
            print(f"Error: {error}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

def modificar_datos_estudiante(estudiantes):
    try:
        legajo = input("Ingrese el legajo del estudiante a modificar: ").strip()
        estudiante = next((e for e in estudiantes if str(e['legajo']) == legajo), None)

        if estudiante is None:
            print("No se encontró un estudiante con ese legajo.")
            return

        while True:
            print(f"\n--- Modificar datos de: {estudiante['nombre']} ---")
            print("1. Modificar Correo")
            print("2. Modificar Nombre")
            print("3. Modificar Legajo")
            print("4. Modificar Materias")
            print("5. Volver")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == '1':
                nuevo_correo = input("Nuevo correo: ").strip()
                if "@" in nuevo_correo and "." in nuevo_correo:
                    estudiante['correo'] = nuevo_correo
                    print("Correo actualizado.")
                else:
                    print("Correo no válido.")
            elif opcion == '2':
                nuevo_nombre = input("Nuevo nombre: ").strip()
                if nuevo_nombre:
                    estudiante['nombre'] = nuevo_nombre.title()
                    print("Nombre actualizado.")
                else:
                    print("Nombre inválido.")
            elif opcion == '3':
                nuevo_legajo = input("Nuevo legajo: ").strip()
                if nuevo_legajo.isdigit() and not es_duplicado("legajo", nuevo_legajo, estudiantes):
                    estudiante['legajo'] = int(nuevo_legajo)
                    print("Legajo actualizado.")
                else:
                    print("Legajo inválido o duplicado.")
            elif opcion == '4':
                materias = input("Ingrese las materias separadas por coma: ").strip()
                lista_materias = [m.strip() for m in materias.split(',') if m.strip()]
                estudiante['materias'] = lista_materias if lista_materias else None
                print("Materias actualizadas.")
            elif opcion == '5':
                break
            else:
                print("Opción no válida.")
    except Exception as e:
        print(f"Error al modificar datos: {e}")

def menu_estudiantes(estudiantes, asistencia):
    while True:
        print("\n--- Menú Estudiantes ---")
        print("1. Agregar Estudiante")
        print("2. Dar de Baja Estudiante")
        print("3. Mostrar Lista de Estudiantes")
        print("4. Modificar Datos de Estudiante")
        print("5. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            submenu(estudiantes)
        elif opcion == '2':
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input("Ingrese el índice del estudiante a dar de baja: "))
            dar_de_baja_usuario(estudiantes, estudiante_index)
        elif opcion == '3':
            estudiantes_ordenados = sorted(estudiantes, key=lambda est: est['nombre'].lower())
            matriz = dic_a_matriz(estudiantes_ordenados)
            for i in list(estudiantes_ordenados[0]):
                print(f'{i:<20}', end=" ")
            print()
            mostrar_lista_estudiantes(matriz)
            print("\nPrimeros 3 estudiantes:")
            mostrar_lista_estudiantes(dic_a_matriz(estudiantes_ordenados[:3]))
            print("\nÚltimos 3 estudiantes:")
            mostrar_lista_estudiantes(dic_a_matriz(estudiantes_ordenados[-3:]))
            archivo(matriz)
        elif opcion == '4':
            modificar_datos_estudiante(estudiantes)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def main():
    estudiantes = [{'legajo':11111, 'nombre':'leo Castillo','correo':'abc1@gmail.edu.ar','materias':['fisica', 'progra1'],'fecha_baja':None},
                   {'legajo':11112, 'nombre':'caro Casto','correo':'abc2@gmail.edu.ar','materias':['progra1'],'fecha_baja':None},
                   {'legajo':11113, 'nombre':'andres julio','correo':'abc3@gmail.edu.ar','materias':None,'fecha_baja':None}]
    sesiones = ['cl1', 'cl2']
    asistencia = [[0]*len(sesiones) for _ in estudiantes]

    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Menú Estudiantes")
        print("2. Mostrar Asistencia")
        print("3. Registrar Asistencia")
        print("4. Agregar Clase")
        print("5. Contar Estudiantes Vigentes")
        print("6. Calcular Inasistencia de un Estudiante")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            menu_estudiantes(estudiantes, asistencia)
        elif opcion == '2':
            mostrar_asistencia(estudiantes, sesiones, asistencia)
        elif opcion == '3':
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input("Índice del estudiante: "))
            for idx, ses in enumerate(sesiones):
                print(f"{idx}: {ses}")
            sesion_index = int(input("Índice de la sesión: "))
            registrar_asistencia(estudiantes, sesiones, asistencia, estudiante_index, sesion_index)
        elif opcion == '4':
            nombre_clase = input("Ingrese el nombre de la clase: ")
            sesiones, asistencia = agregar_sesion(sesiones, asistencia, nombre_clase)
        elif opcion == '5':
            print(f"Estudiantes vigentes: {contar_usuarios_vigentes(estudiantes)}")
        elif opcion == '6':
            for idx, est in enumerate(estudiantes):
                print(f"{idx}: {est['nombre']}")
            estudiante_index = int(input("Índice del estudiante: "))
            calcular_inasistencia_estudiante(estudiantes, sesiones, asistencia, estudiante_index)
        elif opcion == '7':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
