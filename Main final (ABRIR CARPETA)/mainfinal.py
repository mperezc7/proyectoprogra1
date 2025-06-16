from datetime import datetime
import re
from asistencia_persistencia import (
    cargar_estudiantes_json,
    guardar_estudiantes_json,
    guardar_asistencia_txt,
)

# --- Función de guardado combinado ---
def guardar_todo(estudiantes, sesiones, asistencia):
    """Guarda datos de estudiantes en JSON y asistencias en TXT."""
    guardar_estudiantes_json(estudiantes)
    guardar_asistencia_txt(estudiantes, sesiones, asistencia)

# --- Funciones auxiliares ---
def obtener_fecha():
    return datetime.now()

def es_duplicado(campo, valor, estudiantes):
    return any(str(e.get(campo, '')).lower() == str(valor).lower() for e in estudiantes)

def validar_correo():
    patron = r'^[a-zA-Z]{2,10}[0-9]{0,4}$'
    while True:
        usuario = input("Ingrese nombre de usuario para el correo: ")
        if re.match(patron, usuario):
            return usuario + '@uade.edu.ar'
        print("Formato inválido. Use 2-10 letras y hasta 4 dígitos.")

def obtener_legajo(estudiantes):
    legajos = [e['legajo'] for e in estudiantes if 'legajo' in e]
    return max(legajos, default=11110) + 1

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
            correo = validar_correo()
            materias = input("Materias (coma sep.): ").split(',')
            estudiantes.append({
                'legajo': leg,
                'nombre': nombre,
                'correo': correo,
                'materias': [m.strip() for m in materias if m.strip()],
                'fecha_baja': None
            })
            asistencia.append([[0]*7 for _ in sesiones])
            guardar_todo(estudiantes, sesiones, asistencia)
            print(f"Estudiante {nombre} agregado con legajo {leg}.")
        elif op == '2':
            try:
                leg = int(input("Ingrese legajo a dar de baja: "))
            except ValueError:
                print("Legajo inválido.")
                continue
            for e in estudiantes:
                if e['legajo'] == leg:
                    if e.get('fecha_baja'):
                        print("Ya fue dado de baja.")
                    else:
                        e['fecha_baja'] = obtener_fecha()
                        guardar_todo(estudiantes, sesiones, asistencia)
                        print(f"Estudiante {e['nombre']} dado de baja.")
                    break
            else:
                print("Legajo no encontrado.")
        elif op == '3':
            print(f"{'Legajo':<8}{'Nombre':<20}{'Correo'}")
            for e in sorted(estudiantes, key=lambda x: x['nombre'].lower()):
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
                    c = validar_correo()
                    if not es_duplicado('correo', c, estudiantes):
                        est['correo'] = c
                        guardar_todo(estudiantes, sesiones, asistencia)
                        print("Correo actualizado.")
                    else:
                        print("Duplicado.")
                elif o == '2':
                    n = input("Nuevo nombre: ").strip().title()
                    est['nombre'] = n
                    guardar_todo(estudiantes, sesiones, asistencia)
                    print("Nombre actualizado.")
                elif o == '3':
                    ms = input("Materias (coma sep.): ")
                    est['materias'] = [m.strip() for m in ms.split(',') if m.strip()]
                    guardar_todo(estudiantes, sesiones, asistencia)
                    print("Materias actualizadas.")
                elif o == '4':
                    break
                else:
                    print("Inválido.")
        elif op == '5':
            vigentes = sum(1 for e in estudiantes if not e.get('fecha_baja') or e['fecha_baja'] > datetime.now())
            print(f"Estudiantes vigentes: {vigentes}")
        elif op == '6':
            break
        else:
            print("Opción inválida.")

# --- Menú Asistencias ---
def menu_asistencias(estudiantes, sesiones, asistencia, materias):
    while True:
        print("\n--- Menú Asistencias ---")
        print("1. Mostrar Asistencia")
        print("2. Registrar Asistencia")
        print("3. Calcular Inasistencia")
        print("4. Volver")
        op = input("Opción: ")
        if op == '1':
            materias_list = list(materias.keys())
            print("Materias disponibles:")
            for idx, m in enumerate(materias_list): print(f"{idx+1}. {m}")
            try:
                sel = int(input("Seleccione la materia por número: "))
                materia_sel = materias_list[sel-1]
            except (ValueError, IndexError):
                print("Selección inválida.")
                continue
            pos_mat = sesiones.index(materia_sel)
            header = "Nombre".ljust(20) + "".join(f"Clase {c}".ljust(8) for c in range(1,8))
            print(f"\nAsistencia de {materia_sel}:")
            print(header)
            for i, e in enumerate(estudiantes):
                line = e['nombre'].ljust(20)
                for c in range(7):
                    line += ("P" if asistencia[i][pos_mat][c] else "A").ljust(8)
                print(line)
        elif op == '2':
            materias_list = list(materias.keys())
            print("Materias disponibles:")
            for idx, m in enumerate(materias_list): print(f"{idx+1}. {m}")
            try:
                sel = int(input("Seleccione la materia por número: "))
                materia_sel = materias_list[sel-1]
            except (ValueError, IndexError):
                print("Selección inválida.")
                continue
            pos_mat = sesiones.index(materia_sel)
            try:
                clase_sel = int(input("¿Qué clase (1-7) desea tomar? "))
                assert 1 <= clase_sel <= 7
            except:
                print("Clase inválida.")
                continue
            idx_clase = clase_sel - 1
            for i, e in enumerate(estudiantes):
                while True:
                    p = input(f"{e['legajo']} {e['nombre']} (P/A) en {materia_sel} Clase {clase_sel}: ").strip().upper()
                    if p in ('P','A'):
                        asistencia[i][pos_mat][idx_clase] = 1 if p=='P' else 0
                        break
                    print("Opción inválida. Ingrese 'P' o 'A'.")
            guardar_todo(estudiantes, sesiones, asistencia)
            print(f"Asistencia registrada para {materia_sel} Clase {clase_sel}.")
        elif op == '3':
            for idx, e in enumerate(estudiantes): print(f"{idx}:{e['nombre']}")
            try:
                idx = int(input("Índice: "))
            except:
                print("Índice inválido.")
                continue
            total = len(sesiones)*7
            aus = sum(1 for j in range(len(sesiones)) for c in range(7) if asistencia[idx][j][c]==0)
            print(f"{estudiantes[idx]['nombre']} tiene {aus} ausencias de {total} clases.")
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
    asistencia = [[[0]*7 for _ in sesiones] for _ in estudiantes]

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Menu Estudiantes")
        print("2. Menu Asistencias")
        print("3. Agregar Clase")
        print("4. Salir")
        op = input("Opción: ")
        if op=='1': menu_estudiantes(estudiantes,sesiones,asistencia)
        elif op=='2': menu_asistencias(estudiantes,sesiones,asistencia,materias)
        elif op=='3':
            nombre=input("Nombre de la materia: ").strip()
            dia=input("Dia de la materia: ").strip().title()
            materias[nombre]=dia
            sesiones=list(materias.keys())
            for fila in asistencia: fila.append([0]*7)
            guardar_todo(estudiantes,sesiones,asistencia)
            print(f"Materia '{nombre}' agregada para el dia {dia}.")
        elif op=='4':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__=='__main__':
    main()
