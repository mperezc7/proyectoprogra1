from datetime import datetime
from calendario import dic_matxcl
import re
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
    if estudiante_index < 0 or estudiante_index >= len(estudiantes) or sesion_index < 0 or sesion_index >= len(sesiones):
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

def validarcorreo():
    usuario=input("Ingrese nombre de usuario para el correo :")
    patron='[a-zA-Z]{2,10}[0-9]{,4}'
    while len(usuario)<=10:       
        if re.match(patron,usuario):
            return usuario+'@uade.edu.ar'
        else:
            usuario=input("Ingrese nombre de usuario(letras y numeros)hasta 10 caracteres :")
def obtener_legajo(estudiantes):
    legajo = [dic['legajo'] for dic in estudiantes if 'legajo' in dic]
    nuevo = max(legajo) + 1 
    return nuevo
def submenu(estudiantes):
    nombre = ""
    legajo = ""
    correo = ""
    finalizar = False

    while not finalizar:
        print("--- Opciones de ingreso ---")
        print("1. Ingresar nombre del estudiante")
        print("2. Obtener legajo del estudiante")
        print("3. Ingresar correo del estudiante")
        print("4. Guardar estudiante")
        print("5. Cancelar")
        try:
            subopcion = input("Seleccione una opción: ").strip()
            assert subopcion in {'1', '2', '3', '4', '5'}, "Opción inválida."

            if subopcion == '1':
                nuevo_nombre= input("Ingrese el nombre del estudiante: ").strip()
                #if partes.isalpha() for partes in nuevo.split()
                
                assert nuevo_nombre.isalpha(), "El nombre no puede estar vacío."
                assert not es_duplicado("nombre", nuevo_nombre, estudiantes), "Nombre ya registrado."
                nombre = nuevo.title()

            elif subopcion == '2':
                nuevo=obtener_legajo(estudiantes)
                print("Legajo: ",nuevo)
                legajo = int(nuevo)

            elif subopcion == '3':
                nuevo_correo=validarcorreo()
                print(nuevo_correo)
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
                nuevo_correo=validarcorreo()
                print(nuevo_correo)
                if es_duplicado("correo", nuevo_correo, estudiantes) == False:
                    estudiante['correo'] = nuevo_correo
                    print("Correo actualizado.")
                    
                else:
                    print("Correo no válido")
                    
            elif opcion == '2':
                nuevo_nombre = input("Nuevo nombre: ").strip()
                
                if nuevo_nombre.isalpha():
                    estudiante['nombre'] = nuevo_nombre.title()
                    print("Nombre actualizado.")
                    
                else:
                    print("Nombre inválido.")
                    
            elif opcion == '3':
                nuevo=obtener_legajo(estudiantes)
                estudiante['legajo']=int(nuevo)
                print("Nuevo legajo: ",estudiante['legajo'])
            elif opcion=='4':#mod materias
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
            print("--- Submenú de Visualización ---")
            print("1. Ver lista detallada (toda la matriz)")
            print("2. Ver lista general (legajo, nombre y correo)")
            eleccion = input("Seleccione una opción: ")
            if eleccion == '1':
                matriz = dic_a_matriz(estudiantes_ordenados)
                for i in list(estudiantes_ordenados[0]):
                    print(f'{i:<20}', end=" ")
                print()
                mostrar_lista_estudiantes(matriz)
            elif eleccion=='2':
                print(f"{'Legajo':<20} {'Nombre':<20} {'Correo':<20}")
                for est in estudiantes_ordenados:
                    fila = list(est.values())[:3]  # slicing
                    print(f"{str(fila[0]):<20} {str(fila[1]):<20} {str(fila[2]):<20}")
                                           
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
    
    materias={'fisica':'Lunes','progra1':'Viernes'}
    materias_fech=dic_matxcl(materias)
    sesiones = ['cl1', 'cl2','cl3', 'cl4','cl5', 'cl6']
    for clave in materias:
        n=len(materias[clave])
    asistencia = [[0]*len(sesiones) for dic in estudiantes]

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