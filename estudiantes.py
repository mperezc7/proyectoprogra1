import re

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.search(patron, email) is not None

def agregar_estudiante(estudiantes, nombre, email):
    if validar_email(email):
        estudiantes.append({"nombre": nombre, "email": email})
        print(f"Estudiante agregado: {nombre}, Email: {email}")
    else:
        print(f"Error: El correo electrónico '{email}' no es válido.")

def buscar_estudiantes_por_nombre(estudiantes, patron):
    return list(filter(lambda e: re.search(patron, e["nombre"], re.IGNORECASE), estudiantes))
