import json

def cargar_estudiantes_json():
    """Carga la lista de estudiantes desde 'estudiantes.json'."""
    try:
        with open('estudiantes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_estudiantes_json(estudiantes):
    """Guarda la lista de estudiantes en 'estudiantes.json'."""
    with open('estudiantes.json', 'w', encoding='utf-8') as f:
        json.dump(estudiantes, f, default=str, indent=4)

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
            num_clases = len(asistencia[0][mat_idx])
            for clase_idx in range(num_clases):
                numero = clase_idx + 1
                f.write(f"clase,{numero}\n")
                for i, est in enumerate(estudiantes):
                    leg = est.get('legajo', '')
                    nombre = est.get('nombre', '')
                    estado = 'P' if asistencia[i][mat_idx][clase_idx] else 'A'
                    f.write(f"{leg},{nombre},{estado}\n")
                f.write("\n")
