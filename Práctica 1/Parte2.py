def ordenar(lista):
    n = len(lista)
    for index in range(n):
        swapped = False
        for j in range(0, n - index -1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                swapped = True
        if not swapped:
            break

lista = []
sumatoria = 0
while True:
    numero = input("Ingrese un numero: ")
    if numero != "":
        numero = int(numero)
        lista.append(numero)
        sumatoria += numero
    elif (len(lista) >= 5) & (numero == ""):
        break
    else:
        print("Debe ingresar un numero")

ordenar(lista)
print(f"Mayor: {lista[len(lista)-1]}\nMenor: {lista[0]}\nPromedio: {sumatoria/len(lista)}")
