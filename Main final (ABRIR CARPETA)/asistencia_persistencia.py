import json

def cargar_estudiantes_json():
    """Carga la lista de estudiantes desde 'estudiantes.json'."""
    try:
        with open('estudiantes.json', 'r', encoding='utf-8') as f:#f es el aarchivo, el with cierra automaticamente
            return json.load(f) #leemos el arch estudiantes.json 
    except FileNotFoundError:
        return [] #devuelve una lista con diccionario

def guardar_estudiantes_json(estudiantes): 
    """Guarda la lista de estudiantes en 'estudiantes.json'."""
    with open('estudiantes.json', 'w', encoding='utf-8') as f: #f es el aarchivo, el with cierra automaticamente
        json.dump(estudiantes, f, default=str, indent=4) # guarrdamos el dicc a archivo json
        
def guardar_asistencia_txt(estudiantes, sesiones, asistencia):
    """
    Guarda las asistencias en 'asistencias.txt', ordenado por materia y clase.
    Formato:
    materia
    clase,{número}
    legajo,nombre,estado
    (línea en blanco entre clases)
    """
    with open('asistencias.txt', 'w', encoding='utf-8') as f:
        for mat_idx, materia in enumerate(sesiones):
            f.write(f"{materia}\n")
            
            # Verificar si hay estudiantes y datos de asistencia
            if not asistencia or len(asistencia) == 0:
                continue
                
            # Obtener número de clases para esta materia
            try:
                num_clases = len(asistencia[0][mat_idx]) if asistencia[0][mat_idx] is not None else 0
            except IndexError:
                num_clases = 0
                
            for clase_idx in range(num_clases):
                f.write(f"clase,{clase_idx + 1}\n")
                
                for i, est in enumerate(estudiantes):
                    # Solo procesar si el estudiante está inscrito en la materia
                    if materia in est['materias']:
                        leg = est['legajo']
                        nombre = est['nombre']
                        try:
                            estado = 'P' if asistencia[i][mat_idx][clase_idx] == 1 else 'A'
                        except (IndexError, TypeError):
                            estado = 'A'  # Valor por defecto si hay error
                        f.write(f"{leg},{nombre},{estado}\n")
                
                f.write("\n") 