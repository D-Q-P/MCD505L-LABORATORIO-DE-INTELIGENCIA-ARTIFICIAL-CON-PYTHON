import random as rand

numero_magico = rand.randint(1,10)
intentos = 0
print(f"El numero magico es: {numero_magico}")
while True:
    intentos += 1
    numero = int(input("Adivina el número: "))
    if numero == numero_magico:
        print(f"!Correcto¡ Lo lograste en {intentos} intentos ")
        break
    elif (numero - numero_magico) < 0:
        print("Muy bajo")
    else:
        print("Muy alto")