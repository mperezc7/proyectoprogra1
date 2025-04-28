def inicializar_asistencia(sesiones, estudiantes):
    return [[0] * len(sesiones) for _ in range(len(estudiantes))]

def registrar_asistencia(asistencia, estudiante_index, sesion_index):
    asistencia[estudiante_index][sesion_index] = 1  # 1 para presente