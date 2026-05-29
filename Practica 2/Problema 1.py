#Padovan
def calcular_padovan(n):
    padovan_list = []
    for i in range(1, sucesion + 1, 1):
        padovan_list.append(1) if i <= 3 else padovan_list.append(padovan_list[i-3] + padovan_list[i-4])
    print(f"El valor de la sucesion padovan para el elemento {sucesion} es: {padovan_list[sucesion-1]}")

sucesion = int(input("Número de sucesion: "))
calcular_padovan(sucesion)
