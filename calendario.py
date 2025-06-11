def calendario_anual(clases,dia,pos,dias_semana):
    c=0
    año = 2025
    #(2025 no es bisiesto)
    meses = {
        "Enero": 31,
        "Febrero": 28,
        "Marzo": 31,
        "Abril": 30,
        "Mayo": 31,
        "Junio": 30,
        "Julio": 31,
        "Agosto": 31,
        "Septiembre": 30,
        "Octubre": 31,
        "Noviembre": 30,
        "Diciembre": 31
    }
    primer_dia = 3  # 0=Dom, 1=Lun, 2=Mar, 3=Mié, 4=Jue, 5=Vie, 6=Sáb
    for mes, dias in meses.items():
        c+=1
        if mes in 'MarzoAbrilMayoJunio': #primercuatri
            # Espacios en blanco para los días antes del primer día del mes
            espacios = ["  "] * primer_dia

            # Crear la lista de días del mes
            dias_del_mes = espacios + [f"{dia:>2}" for dia in range(1, dias + 1)]

            #los días del mes en filas de 7
            for i in range(0, len(dias_del_mes), 7):
                fila = dias_del_mes[i:i + 7]
                
                if pos < len(fila) and fila[pos]!='  ':
                    d=fila[pos]
                    clases.append(f"{d}/{c}/{año}")
        # Actualizar el primer día para el siguiente mes
        primer_dia = (primer_dia + dias) % 7
    return clases
    
def dic_matxcl(materias):
    dias_semana = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
    mat=[]
    clases=[]
    pos=0
    for clave in materias:
        for dia in dias_semana:
            
            if dia in materias[clave]:
                fechas_clases=calendario_anual(clases,dia,pos,dias_semana)
                materias[clave]=fechas_clases
                mat.append(fechas_clases)            
            else:
                pos+=1
        pos=0
    return materias
#print(dic_matxcl())