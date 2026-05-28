def es_perfecto(n):
    if n <= 1:
        return False
    suma_divisor = 0
    for i in range(1, n):
        if n % i == 0:
            suma_divisor += i
    return suma_divisor == n

numero = int(input("Ingresa un número para saber si es PERFECTO: "))
print(f"El número {numero} es PERFECTO") if es_perfecto(numero) else print(f"El número {numero} no es PERFECTO")
