import random

matrizRandom=[]
filas=3
columnas=4
for i in range(filas):
    matrizRandom.append([])
    for j in range(columnas):
        valor=random.randint(1,9)
        matrizRandom[i].append(valor)

print(matrizRandom)

#imprimir matriz elementoxelemento (como una tabla)
for i in range(filas):
    for j in range(columnas):
        print(matrizRandom[i][j], end="\t")
    print()

#mostrar totales por fila
totalesporFila=[]
for i in range(filas):
    suma=0
    for j in range(columnas):
            suma=suma+matrizRandom[i][j]
    totalesporFila.append(suma)
print(totalesporFila)

#mostrar totales por columna
totalesporColumna=[]
for i in range(columnas):
    suma=0
    for j in range(filas):
            suma=suma+matrizRandom[j][i]
    totalesporColumna.append(suma)
print(totalesporColumna)

#matrices para carga de datos(tablas)

encabezados=["Cod", "Desc", "PU", "Cant", "Total"]
productos=2
matrizDatos=[]

for i in range(productos):
     codigo=int(input("Codigo: "))
     descripcion=input("Descripcion: ")
     precioUnitario=int(input("precio unitario: "))
     cantidad=int(input("cantidad: "))
     producto=[codigo, descripcion, precioUnitario, cantidad, precioUnitario*cantidad]
     matrizDatos.append(producto)

print(matrizDatos)

###########################################

#matrices cl1
matriz =[[1,2,3],[4,5,6]] #matriz de 2x3
print(matriz)
print(matriz[0]) #
print(matriz[1][1])

#longitud de la matriz (filas/columnas)
filas=len(matriz)
columnas = len(matriz[0])
print("la matriz tiene", filas ,"filas y ", columnas, "columnas")
print()
#imprimir por fila
for i in range(filas):
    print(matriz[i])
print()

#imprimir matriz elemntop x elemento
for i in range(filas):
    for j in range(columnas):
        print(matriz[i][j])
print()
#imprimir matriz elemntop x elemento(como una tabla)
for i in range(filas):
    for j in range(columnas):
        print(matriz[i][j], end=" ")
    print()

#############################3

#formas de crear una matriz

#append
matriz1=[]
filas=3
columnas=4
for i in range(filas):
    matriz1.append([])
    for j in range(columnas):
        matriz1[i].append(0)

print(matriz1) #[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

#replicando elementos
matriz2=[]
for i in range (filas):
    matriz2.append([0]*columnas)
print(matriz2) #[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

#a tarves de listas por compresion
matriz3=[[0]*columnas for i in range(filas)]
print(matriz3) #[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
