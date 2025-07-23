from datetime import datetime
import re
from asistencia_persistencia import (
    cargar_estudiantes_json,
    guardar_estudiantes_json,
    guardar_asistencia_txt,
)

def convertir_fecha(fecha_str):
    if fecha_str is None:
        return None
    return datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')

def guardar_todo(estudiantes, sesiones, asistencia):
    """Guarda datos de estudiantes en JSON y asistencias en TXT."""
    guardar_estudiantes_json(estudiantes)
    guardar_asistencia_txt(estudiantes, sesiones, asistencia)

def obtener_fecha():
    return datetime.now()

def es_duplicado(campo, valor, estudiantes):
    b=any(str(est[campo]).title() == str(valor).title() for est in estudiantes)
    while b==True:
        print("correo existente")
        valor=validar_correo()
        b=any(str(est[campo]).title() == str(valor).title() for est in estudiantes)
    return valor
        
def validar_correo():
    patron = r'^[a-zA-Z]{2,10}[0-9]{0,4}$'
    while True:
        usuario = input("Ingrese nombre de usuario para el correo: ")
        if re.match(patron, usuario):
            return usuario + '@uade.edu.ar'
        print("Formato inválido. Use 2-10 letras y hasta 4 dígitos.")
def dar_de_baja(estudiantes, asistencia, leg):
    for i, e in enumerate(estudiantes):
        if e['legajo'] == leg:
            if e.get('fecha_baja'):
                print("\nEste estudiante YA estaba dado de baja.")
                eliminar = input("¿Desea eliminarlo PERMANENTEMENTE del sistema? (s/n): ").lower()
                if eliminar == 's':
                    estudiantes.pop(i) 
                    asistencia.pop(i)
                    print("¡Estudiante eliminado permanentemente!")
            else:
                e['fecha_baja'] = obtener_fecha()
                print(f"\nEstudiante {e['nombre']} dado de baja (permanece como registro).")
                print("Nota: Para eliminarlo completamente del sistema,")
                print("deberá darle de baja nuevamente y confirmar eliminación.")
            return estudiantes, asistencia 
    else:
        print("Legajo no encontrado.")
        return estudiantes, asistencia

def obtener_legajo(estudiantes, index=0, max_legajo=11110):
    if index >= len(estudiantes):
        return max_legajo + 1
    legajo_actual = estudiantes[index].get('legajo', None)
    if legajo_actual is not None:
        max_legajo = max(max_legajo, legajo_actual)
    return obtener_legajo(estudiantes, index + 1, max_legajo)

def registrar_asistencia_individual(estudiante, materia_pos, clase_idx, asistencia):
    while True:
        asist = input(f"{estudiante['legajo']} {estudiante['nombre']} (P/A): ").strip().upper()
        if asist in ('P', 'A'):
            asistencia[materia_pos][clase_idx] = 1 if asist == 'P' else 0
            break
        print("Opción inválida. Ingrese 'P' (Presente) o 'A' (Ausente).")
def buscar_estudiante_por_legajo(estudiantes, legajo):
    """Busca un estudiante por legajo y devuelve su índice y datos. Si no existe, retorna None."""
    try:
        legajo = int(legajo)
        for i, e in enumerate(estudiantes):
            if e['legajo'] == legajo:
                return i, e
        return None
    except ValueError:
        return None
def matriz(estudiantes,sesiones):
    asistencia = []
    for estudiante in estudiantes:
        materias_estudiante = estudiante['materias']
        
        asistencia_estudiante = []
        for materia in sesiones:
            if materia in materias_estudiante:
                asistencia_estudiante.append([0] * 7)
            else:
                asistencia_estudiante.append(None)
        asistencia.append(asistencia_estudiante)
    return asistencia
def seleccionar_materia(materias):
    print("\nMaterias disponibles:")
    for idx, materia in enumerate(materias):
        print(f"{idx + 1}. {materia}")
    while True:
        try:
            sel = int(input("Seleccione materia (número): ")) - 1
            if 0 <= sel < len(materias):
                
                return sel,materias[sel]
            print("Error: Número fuera de rango.")
        except ValueError:
            print("Error: Ingrese un número válido.")
def validar_clase():
    try:
        clase = int(input("Clase a modificar (1-7): "))
        if not 1 <= clase <= 7:
            print("Error: La clase debe estar entre 1 y 7.")
            return None
        return clase 
    except ValueError:
        print("Error: Ingrese un número válido.")
        return None

def Reg_Asistencia(estudiantes,sesiones,asistencia):
    pos, materia = seleccionar_materia(sesiones)
    clase = validar_clase()
    if clase is None:
        return
    clase_idx=clase - 1
    estudiantes_inscritos = [(i, e) for i, e in enumerate(estudiantes)if materia in e['materias']]   
    if not estudiantes_inscritos:
        print(f"No hay estudiantes inscritos en {materia}.")
        return

    print(f"\nClase {clase} de {materia}")
    opcion = input("¿Registrar Asistencia toda la clase (C) o un estudiante (E)? ").upper()  
    if opcion == 'C':
        print("\nRegistro completo de asistencia:")
        for i, est in estudiantes_inscritos:
            while True:
               
                estado_actual = asistencia[i][pos][clase_idx] if asistencia[i][pos] is not None else None
                estado_str = 'P' if estado_actual == 1 else 'A' if estado_actual == 0 else 'No registrado'               
                nuevo_estado = input(f"{est['legajo']} {est['nombre']} (Actual: {estado_str}). Nuevo estado (P/A): ").upper().strip()
                
                if nuevo_estado in ('P', 'A'):
                    if asistencia[i][pos] is None:
                        asistencia[i][pos] = [None] * 7                    
                    asistencia[i][pos][clase_idx] = 1 if nuevo_estado == 'P' else 0
                    break
                else:
                    print("Error: Ingrese 'P' o 'A'.")
    elif opcion == 'E':
        print("\nEstudiantes inscritos:")
        for i, est in estudiantes_inscritos: 
            print(f"{est['legajo']}: {est['nombre']}")
        legajo = input("Legajo del estudiante a modificar: ")
        estudiante = next((e for l, e in estudiantes_inscritos if str(e['legajo']) == legajo), None)
        if estudiante:
            idx = estudiantes.index(estudiante)
            estado_actual = asistencia[idx][pos][clase_idx] if asistencia[idx][pos] is not None else None
            estado_str = 'P' if estado_actual == 1 else 'A' if estado_actual == 0 else 'No registrado'
            nuevo_estado = input(f"{estudiante['nombre']} (Actual: {estado_str}). Nuevo estado (P/A): ").upper().strip()
            if nuevo_estado in ('P', 'A'):
                if asistencia[idx][pos] is None:
                    asistencia[idx][pos] = [None] * 7
                asistencia[idx][pos][clase_idx] = 1 if nuevo_estado == 'P' else 0
                print("¡Asistencia actualizada!")
            else:
                print("Error: Estado no válido.")
        else:
            print("Error: Legajo no encontrado.")
    else:
        print("Opción no válida.")
    guardar_todo(estudiantes, sesiones, asistencia)    
# --- Menú Estudiantes ---
def menu_estudiantes(estudiantes, sesiones, asistencia):
    while True:
        print("\n--- Menú Estudiantes ---")
        print("1. Agregar Estudiante")
        print("2. Dar de baja Estudiante")
        print("3. Mostrar Lista")
        print("4. Modificar Datos")
        print("5. Contar Estudiantes Vigentes")
        print("6. Volver")
        op = input("Opción: ")
        if op == '1':
            leg = obtener_legajo(estudiantes)
            nombre = input("Nombre del estudiante: ").strip().title()
            correo=validar_correo()
            correo=es_duplicado('correo',correo, estudiantes)
            materias_input = input("Materias (coma sep.): ").split(',')
            materias = [m.strip() for m in materias_input if m.strip()]
            for m in materias:
                if m not in sesiones:
                    print(f"Error: La materia '{m}' no existe.")
                    continue
            estudiantes.append({
                'legajo': leg,
                'nombre': nombre,
                'correo': correo,
                'materias': materias,
                'fecha_baja': None
            })
            nueva_asistencia = []
            for materia in sesiones:
                if materia in materias:
                    nueva_asistencia.append([0]*7) 
                else:
                    nueva_asistencia.append(None) 
            asistencia.append(nueva_asistencia)
            
            guardar_todo(estudiantes, sesiones, asistencia)
            print(f"Alta de estudiante {nombre} agregado con legajo {leg}.")
        elif op == '2':
            try:
                leg = int(input("Ingrese legajo a dar de baja: "))
            except ValueError:
                print("Legajo inválido.")
                continue
            estudiantes, asistencia = dar_de_baja(estudiantes, asistencia, leg)
            guardar_todo(estudiantes, sesiones, asistencia)
        elif op == '3':
            print(f"{'Legajo':<8}{'Nombre':<20}{'Correo'}")
            for e in sorted(estudiantes, key=lambda x: x['nombre'].lower()):
                if e.get('fecha_baja') is None: 
                    print(f"{e['legajo']:<8}{e['nombre']:<20}{e['correo']}")
        elif op == '4':
            leg = input("Legajo a modificar: ")
            est = next((x for x in estudiantes if str(x['legajo']) == leg), None)
            if not est:
                print("No encontrado.")
                continue
            while True:
                print("1.Correo 2.Nombre 3.Materias 4.Volver")
                o = input("Opción: ")
                if o == '1':
                    correo=validar_correo()
                    est['correo']=es_duplicado('correo',correo, estudiantes)
                    guardar_todo(estudiantes, sesiones, asistencia)
                    print("Correo actualizado.")
                elif o == '2':
                    n = input("Nuevo nombre: ").strip().title()
                    est['nombre'] = n
                    guardar_todo(estudiantes, sesiones, asistencia) 
                    print("Nombre actualizado.")
                elif o == '3':
                    ms = input("Materias (coma sep.): ")
                    materias = [m.strip() for m in ms.split(',') if m.strip()]
                    for m in materias:
                        if m not in sesiones:
                            print(f"Error: La materia '{m}' no existe.")
                            continue
                    est['materias'] = materias
                    nueva_asistencia = []
                    for materia in sesiones:
                        if materia in materias:
                            nueva_asistencia.append([0]*7)
                        else:
                            nueva_asistencia.append(None)                                  
                    idx = estudiantes.index(est)
                    asistencia[idx] = nueva_asistencia                           
                    guardar_todo(estudiantes, sesiones, asistencia)
                    print("Materias actualizadas.")
                elif o == '4':
                    break
                else:
                    print("Inválido.")
        elif op == '5':
            vigentes = sum(1 for e in estudiantes if not e.get('fecha_baja') or (convertir_fecha(e['fecha_baja']) > datetime.now()))
            print(f"Estudiantes vigentes: {vigentes}")
           
            print(len(estudiantes))
        elif op == '6':
            break
        else:
            print("Opción inválida.")

# --- Menú Asistencias ---
def menu_asistencias(estudiantes, sesiones, asistencia):
    while True:
        print("\n--- Menú Asistencias ---")
        print("1. Mostrar Asistencia")
        print("2. Registrar Asistencia")
        print("3. Calcular Inasistencia")
        print("4. Volver")
        op = input("Opción: ")
        if op == '1':
            pos,materia=seleccionar_materia(sesiones) #materia
            
            estudiantes_inscritos = [(i, e) for i, e in enumerate(estudiantes) if materia in e['materias']]
            if not estudiantes_inscritos:
                print(f"\nNo hay estudiantes inscritos en {materia}.")
                continue
            print(f"\nAsistencia de {materia}:")
            print("Nombre".ljust(20) + "".join(f"Clase {c + 1}".ljust(8) for c in range(7)))
            for i, e in estudiantes_inscritos:
                line = e['nombre'].ljust(20)
                for c in range(7):
                    line += ("P" if asistencia[i][pos][c] == 1 else "A").ljust(8)
                print(line)
        elif op == '2':
            print("\n--- Registro de Asistencia ---")
            Reg_Asistencia(estudiantes,sesiones,asistencia)
        elif op == '3':
            print("\nEstudiantes registrados:")
            for e in estudiantes:
                print(f"Legajo: {e['legajo']} - Nombre: {e['nombre']}")
            legajo = input("\nIngrese el legajo del estudiante: ")
            estudiante = next((e for e in estudiantes if str(e['legajo']) == legajo), None)
            if not estudiante:
                print("Error: Legajo no encontrado.")
                continue
            print(f"\nAsistencia de {estudiante['nombre']}:")
            
            for materia in estudiante['materias']:
                try:
                    pos_mat = sesiones.index(materia)
                    if asistencia[estudiantes.index(estudiante)][pos_mat] is not None:
                      
                        total_clases = 7 
                        presentes = sum(asistencia[estudiantes.index(estudiante)][pos_mat])
                        porcentaje = (presentes / total_clases) * 100
                        print(f"- {materia}: {porcentaje:.1f}% de asistencia")
                except ValueError:
                    print(f"Error: Datos inconsistentes en {materia}.")
           
        elif op == '4':
            return
        else:
            print("Opción inválida.")

# --- MAIN --- 
def main():
    estudiantes = cargar_estudiantes_json()
    if not estudiantes:
        estudiantes = [
            {'legajo':11111,'nombre':'Leo Castillo','correo':'abc1@uade.edu.ar','materias':['fisica','progra1'],'fecha_baja':None},
            {'legajo':11112,'nombre':'Caro Casto','correo':'abc2@uade.edu.ar','materias':['progra1'],'fecha_baja':None},
            {'legajo':11113,'nombre':'Andres Julio','correo':'abc3@uade.edu.ar','materias':['fisica'],'fecha_baja':None}
        ]
        guardar_estudiantes_json(estudiantes)

    materias = {'fisica':'Lunes','progra1':'Viernes'}
    sesiones = list(materias.keys())
    asistencia = matriz(estudiantes,sesiones)
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Menu Estudiantes")
        print("2. Menu Asistencias")
        print("3. Agregar Materia")
        print("4. Salir")
        op = input("Opción: ")
        if op=='1': menu_estudiantes(estudiantes,sesiones,asistencia)
        elif op=='2': menu_asistencias(estudiantes,sesiones,asistencia)
        elif op=='3':
            lista_dia=['Lunes','Martes','Miercoles','Jueves','Viernes']
            nombre=input("Nombre de la materia: ").strip()
            dia=input("Dia de la materia: ").strip().title()
            
            if nombre in materias:
                print("Error: La materia ya existe.")
                continue
            
            if dia in lista_dia:
                if dia in materias.values():
                    print("Error: El día ya está asignado a otra materia.")
                    continue
                materias[nombre] = dia
                sesiones.append(nombre)
                for estudiante_asistencia in asistencia:
                    estudiante_asistencia.append([0]*7)
                guardar_todo(estudiantes, sesiones, asistencia)
                print(f"Materia '{nombre}' agregada para el día {dia}.")
            else:
                print("Dia no reconocido")
        elif op=='4':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__=='__main__':
    main()