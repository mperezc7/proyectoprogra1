frutas = ["manzana", "banana", "cereza", "durazno"]
print(frutas[0]) # manzana
print(frutas[2]) # cereza
print(frutas[-1]) # durazno
frutas[1] = "naranja"
print(frutas) # ['manzana', 'naranja', 'cereza', 'durazno']

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
print(dias[-1]) # Viernes
print(dias[-5]) # Lunes
listaNumeros = [1,2,3,4]
listaTexto = ["Hola", "Mundo", "!"]
listaDistintosTipos = ["A", True, 123, 123.12]
listaDeListas = [ [1,2,3], [4,5,6] ]
listaVacia = [ ] # También puede usarse list()
lista = [ ]
for i in range(4):
 lista.append(i**2) # Resultado: [0, 1, 4, 9]
 # Impresión con for

for i in range(len(lista)):
 print(lista[i], end=' ')
# Resultado: 0 1 4 9

# Impresión con while
pos = 0
while pos < len(lista):
 print(lista[pos], end=' ')
 pos += 1
# Resultado: 0 1 4 9 

# Ejemplo: iterar una lista utilizando el subíndice, for y range (para generar una secuencia de valores)
listaVocales = ['a','e','i','o','u']
for i in range(len(listaVocales)):
 print(listaVocales[i], end=" ") # a e i o u 
print() # Salto de línea
# Ejemplo: iterar una lista utilizando el operador in
for valor in listaVocales:
 print(valor, end=" ") # a e i o u

 #numeros = [0,1,2,3,4,5]
 #cuadrados = []
 #for num in numeros:
 #cuadrados.append(num**2)
 #print(cuadrados)
 # [0, 1, 4, 9, 16, 25]

numeros = [0,1,2,3,4,5]
cuadrados = [num**2 for num in numeros]
print(cuadrados) # [0, 1, 4, 9, 16, 25]

lista = [1,-2,5,0,3,4]
listaCuadradosPares = []
for num in lista:
 if num%2==0:
  listaCuadradosPares.append(num**2)
print(listaCuadradosPares) # [4, 0, 16]
 # Su equivalente utilizando listas por comprensión
listaCuadradosParesPorComp = [num**2 for num in lista if num%2==0]
print(listaCuadradosParesPorComp) # [4, 0, 16]

# Elevo al cuadrado los pares y los impares quedan igual
lista = [1,-2,5,0,3,4]
listaPorComp = [num**2 if num%2==0 else num for num in lista]
print(listaPorComp) # [1, 4, 5, 0, 3, 16]

#Listas slicing(rebanadas)
numeros = [2, 34, 25, 1, 19, 23, 48, 19, 38, 9]
print(numeros[2:5]) # [25, 1, 19]
print(numeros[:4]) # [2, 34, 25, 1]
print(numeros[5:]) # [23, 48, 19, 38, 9]
#Podemos utilizar constantes, variables y expresiones aritméticas para calcular el subíndice. Incluso podemos llamar a una función.
#print(lista[funcion():])
#print(lista[inicio:inicio+4])

numeros = [2, 34, 25, 1, 19, 23, 48, 19, 38, 9]

 #Superar índice: No genera error, llega hasta el final o principio de la lista.
print(numeros[1:100]) # [34, 25, 1, 19, 23, 48, 19, 38, 9]
 #Índices Negativos:Podemos utilizar los sub-índices negativos para cortar las listas.
print(numeros[-5:-2]) # [23, 48, 19]
 #Invertir una lista: Colocando-1 como tercer subíndice invertimos una lista.
print(numeros[::-1]) # [9, 38, 19, 48, 23, 19, 1, 25, 34, 2]

#Incremento: Podemos indicar el incremento o paso a realizar entre inicio y fin de los índices. Utilizamos tres sub-índices.
print(numeros[2:7:2]) # [25, 19, 48]
#Incremento negativo: Un incremento negativo, toma los elementos de atrás hacia adelante, invierte el orden.
print(numeros[7:1:-2]) # [19, 23, 1]

lista = [19, 23, 48, 19, 38, 9]
#Reemplazarelementos:
lista[2:4] = [80, 85]
print(lista) # [19, 23, 80, 85, 38, 9]
#Eliminar elementos:podemos eliminar elementos consecutivos sin mucho esfuerzo.
lista[2:4] = []
print(lista) # [19, 23, 38, 9]

#Reemplazar elementos
lista = [19, 23, 48, 19, 38, 9]
lista[2:4] = [80, 85, 101]
print(lista) # [19, 23, 80, 85, 101 , 38, 9]

listaOriginal = [2, 34, 25]
listaCopia = listaOriginal[:]
listaCopia.append(18)
print(listaOriginal) # [2, 34, 25]
print(listaCopia) # [2, 34, 25, 18]
#Podemos recorrer parcialmente una lista utilizando rebanadas:
lista = [19, 23, 48, 19, 38, 9]
for i in lista:
 print(i, end=" ") # 19 23 48 19 38 9 
for i in lista[2:5]:
 print(i, end=" ") # 48 19 38







cad = "Martes"
print("te" in cad) # True
print("ié" not in cad) # True

cadena = "Programación I"
cadena_invertida = cadena[::-1]
print(cadena_invertida) # I nóicamargorP

frase = input("Ingrese una frase: ")
palabras = frase.split() # Partimos la frase en una lista de palabras
palabras.reverse() # Invertimos la lista con reverse
frase = ' '.join(palabras) # Construimos la cadena a partir de la lista
print(frase)
# Resultado:
# Ingrese una frase: Hola cómo estás
# estás cómo Hola

legajo = 11212; nombre = "María"; nota = 10
print("Legajo: %d, Nombre: %s, Nota: %d" %(legajo, nombre, nota))
# Legajo: 11212, Nombre: María, Nota: 10

legajo = 15035; nombre = "Carlos"; nota = 8
print("Legajo: {}, Nombre: {}, Nota: {}".format(legajo, nombre, nota))
# Legajo: 15035, Nombre: Carlos, Nota: 8

dia = 25
mes = "diciembre"
cad = f'Navidad es el {dia} de {mes}'
print(cad) # Navidad es el 25 de diciembre

print(f'{23*2+12}') # 58
mes = "octubre"
print(f'{mes.upper()} tiene {len(mes)} letras') # OCTUBRE tiene 7 letras

num = 25
cad = f'|{num:5}|'
print(cad) # | 25|
num = 25
cad = f'|{num:05}|'
print(cad) # |00025|

num = 8
cad = f'|{num:<5}|'
print(cad) # |8  |
cad = f'|{num:>5}|'
print(cad) # |  8|
cad = f'|{num:^5}|'
print(cad) # | 8 |

texto = "Hola"
cad = f'|{texto:-^8}|'
print(cad) # |--Hola--|
pi = 3.1416
cad = f'{pi:.2f}'
print(cad) # 3.14
print("")