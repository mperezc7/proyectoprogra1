nombreProd=input("Nombre del producto:")
Descripcion=input("Descripcion del producto(50c):")
desc=input("desc:")
while len(desc)>50:
    desc=input("desc menos de 50 caracteres:")
PrecioUnitario=float(input("pu0.00:"))
Cantidad=int(input("cantidad"))
Disponibilidad=input("Ingrese si/no segun su disponibilidad:")

total=0.00

print(f'nombreProd cantidad {PrecioUnitario:.2f} total')
