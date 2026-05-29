def encontrar_divisores(n: int):
    divisores = []
    for divisor in range(1,n):
        if n % divisor == 0:
            divisores.append(divisor)

    def semi_perfecto(indice, suma):
        if suma == n:
            return True
        if suma > n or indice >= len(divisores):
            return False
        
        usar = semi_perfecto(indice + 1, suma + divisores[indice])

        no_usar = semi_perfecto(indice + 1, suma)

        return usar or no_usar
    
    return semi_perfecto(0, 0)

numero = int(input("Dame un numero: "))
if encontrar_divisores(numero):
    print("El número es semiperfecto")
else:
    print("El número no es semiperfecto")
