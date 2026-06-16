# Parte A: Importaciones 
from datetime import datetime 
# Parte B: Clase CuentaBancaria 
class CuentaBancaria: 
    """Clase base que representa una cuenta bancaria.""" 
    def __init__(self, titular: str, numero_cuenta: str, saldo_inicial: float = 0.0) -> None: 

        """Inicializa una cuenta bancaria.""" 
        self.titular = titular 
        self.numero_cuenta = numero_cuenta 
        self.__saldo = saldo_inicial 
        self.historial: list[str] = [] 
        self._registrar_transaccion(f"Cuenta creada con saldo inicial RD${saldo_inicial:.2f}") 

    @classmethod 
    def crear_cuenta_cero(cls, titular: str, numero_cuenta: str) -> "CuentaBancaria": 
        """Crea una cuenta bancaria con saldo inicial en cero.""" 
        return cls(titular, numero_cuenta, 0.0) 

    def _registrar_transaccion(self, mensaje: str) -> None: 
        """Registra una transacción en el historial con fecha y hora.""" 
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        self.historial.append(f"{fecha_hora} - {mensaje}") 

    def depositar(self, monto: float) -> None: 
        """Deposita dinero en la cuenta si el monto es válido.""" 
        if monto <= 0: 
            print("El monto a depositar debe ser mayor que cero.") 
            return 
        self.__saldo += monto 
        self._registrar_transaccion(f"Depósito realizado: RD${monto:.2f}") 
        print(f"Depósito exitoso. Nuevo saldo: RD${self.__saldo:.2f}") 

    def retirar(self, monto: float) -> None: 
        """Retira dinero de la cuenta si hay saldo suficiente.""" 
        if monto <= 0: 
            print("El monto a retirar debe ser mayor que cero.") 
            return 

        if monto > self.__saldo: 
            print("Fondos insuficientes para realizar el retiro.") 
            self._registrar_transaccion(f"Intento fallido de retiro: RD${monto:.2f}") 
            return 
        self.__saldo -= monto 
        self._registrar_transaccion(f"Retiro realizado: RD${monto:.2f}") 
        print(f"Retiro exitoso. Nuevo saldo: RD${self.__saldo:.2f}") 

    def obtener_saldo(self) -> float: 
        """Retorna el saldo actual de la cuenta.""" 
        return self.__saldo 

    def _actualizar_saldo(self, nuevo_saldo: float) -> None: 
        """Actualiza el saldo de forma controlada.""" 
        self.__saldo = nuevo_saldo 

    def imprimir_historial(self) -> None: 
        """Imprime todas las transacciones registradas.""" 
        print(f"Historial de la cuenta {self.numero_cuenta}:") 
        for movimiento in self.historial: 
            print(movimiento) 
    def __str__(self) -> str: 
        """Retorna una descripción general de la cuenta bancaria.""" 
        return ( 
            f"Cuenta Bancaria | Titular: {self.titular} | " 
            f"Número: {self.numero_cuenta} | Saldo: RD${self.__saldo:.2f}" 
        ) 

# Parte C: Clase CuentaAhorros 

class CuentaAhorros(CuentaBancaria): 
    """Clase que representa una cuenta de ahorros.""" 
    def __init__(self, titular: str, numero_cuenta: str, saldo_inicial: float, tasa_interes: float) -> None: 
        """Inicializa una cuenta de ahorros.""" 
        super().__init__(titular, numero_cuenta, saldo_inicial) 
        self.tasa_interes = tasa_interes 
 
    def calcular_interes(self, meses: int) -> float: 
        """Calcula el saldo final con interés compuesto usando recursión.""" 
        if meses < 0: 
            print("Los meses no pueden ser negativos.") 
            return self.obtener_saldo() 

        if meses == 0: 
            return self.obtener_saldo() 
        saldo_mes_anterior = self.calcular_interes(meses - 1) 
        saldo_final = saldo_mes_anterior * (1 + self.tasa_interes) 
        return round(saldo_final, 2) 
    def __str__(self) -> str: 
        """Retorna una descripción de la cuenta de ahorros.""" 
        return ( 
            f"Cuenta de Ahorros | Titular: {self.titular} | " 
            f"Número: {self.numero_cuenta} | Saldo: RD${self.obtener_saldo():.2f} | " 
            f"Tasa de interés: {self.tasa_interes * 100:.2f}% mensual" 
        ) 

# Parte D: Clase CuentaCorriente 
class CuentaCorriente(CuentaBancaria): 
    """Clase que representa una cuenta corriente con sobregiro.""" 
    def __init__(self, titular: str, numero_cuenta: str, saldo_inicial: float, limite_sobregiro: float) -> None: 
        """Inicializa una cuenta corriente.""" 
        super().__init__(titular, numero_cuenta, saldo_inicial) 
        self.limite_sobregiro = limite_sobregiro 

    def retirar(self, monto: float) -> None: 
        """Retira dinero permitiendo sobregiro hasta el límite establecido.""" 
        validar_monto = lambda valor: valor > 0 

        if not validar_monto(monto): 
            print("El monto a retirar debe ser mayor que cero.") 
            return 
        saldo_disponible = self.obtener_saldo() + self.limite_sobregiro 

        if monto > saldo_disponible: 
            print("El retiro excede el límite de sobregiro permitido.") 
            self._registrar_transaccion(f"Intento fallido de retiro con sobregiro: RD${monto:.2f}") 
            return 

        nuevo_saldo = self.obtener_saldo() - monto 
        self._actualizar_saldo(nuevo_saldo) 
        self._registrar_transaccion(f"Retiro realizado en cuenta corriente: RD${monto:.2f}") 
        print(f"Retiro exitoso. Nuevo saldo: RD${nuevo_saldo:.2f}") 

    def __str__(self) -> str: 
        """Retorna una descripción de la cuenta corriente.""" 
        return ( 
            f"Cuenta Corriente | Titular: {self.titular} | " 
            f"Número: {self.numero_cuenta} | Saldo: RD${self.obtener_saldo():.2f} | " 
            f"Límite de sobregiro: RD${self.limite_sobregiro:.2f}" 
        ) 

# Parte E: Clase Banco 

class Banco: 
    """Clase que administra las cuentas bancarias.""" 

    def __init__(self, nombre: str) -> None: 
        """Inicializa el banco con una lista privada de cuentas.""" 
        self.nombre = nombre 
        self.__cuentas: list[CuentaBancaria] = [] 

    @staticmethod 
    def validar_numero_cuenta(numero: str) -> bool: 
        """Valida que el número de cuenta tenga 6 dígitos numéricos.""" 
        return numero.isdigit() and len(numero) == 6 

    def abrir_cuenta(self, cuenta: CuentaBancaria) -> None: 
        """Agrega una cuenta al banco si el número es válido.""" 
        if not Banco.validar_numero_cuenta(cuenta.numero_cuenta): 
            print("No se pudo abrir la cuenta. Número de cuenta inválido.") 
            return 

        self.__cuentas.append(cuenta) 
        print(f"Cuenta {cuenta.numero_cuenta} abierta exitosamente.") 

    def cerrar_cuenta(self, numero: str) -> None: 
        """Cierra una cuenta según su número.""" 
        cuenta = self.buscar_cuenta(numero) 

        if cuenta is None: 
            print("No se encontró la cuenta para cerrar.") 
            return 

        self.__cuentas = list(filter(lambda c: c.numero_cuenta != numero, self.__cuentas)) 
        print(f"Cuenta {numero} cerrada exitosamente.") 

    def buscar_cuenta(self, numero: str) -> CuentaBancaria | None: 
        """Busca una cuenta por número usando filter y lambda.""" 
        resultado = list(filter(lambda c: c.numero_cuenta == numero, self.__cuentas)) 
        return resultado[0] if resultado else None 

    def reporte_total(self) -> None: 
        """Imprime el reporte de cuentas y el saldo total del banco.""" 
        print(f"Reporte general del banco {self.nombre}:") 
        cuentas_ordenadas = sorted( 
            self.__cuentas, 
            key=lambda c: c.obtener_saldo(), 
            reverse=True 
        ) 
        total = 0.0 
        for cuenta in cuentas_ordenadas: 
            print(cuenta) 
            total += cuenta.obtener_saldo() 
        print(f"Saldo total del banco: RD${total:.2f}") 

    def cuenta_mayor_saldo(self) -> CuentaBancaria | None: 
        """Retorna la cuenta con mayor saldo usando sorted y lambda.""" 
        if len(self.__cuentas) == 0: 
            return None 

        cuentas_ordenadas = sorted( 
            self.__cuentas, 
            key=lambda c: c.obtener_saldo(), 
            reverse=True 
        ) 
        return cuentas_ordenadas[0] 

# Parte F: Pruebas del sistema 
if __name__ == "__main__": 
    print("Prueba 1: Crear cuentas") 
    cuenta_ahorros = CuentaAhorros("David Quezada", "123456", 10000.00, 0.02) 
    cuenta_ahorros2 = CuentaAhorros("Nissa Gutierrez", "222333", 15000.00, 0.015) 
    cuenta_corriente = CuentaCorriente("Elian Rosario", "654321", 5000.00, 3000.00) 
    cuenta_demo = CuentaBancaria.crear_cuenta_cero("Cliente Demo", "111222") 
 
    print(cuenta_ahorros) 
    print(cuenta_ahorros2) 
    print(cuenta_corriente) 
    print(cuenta_demo) 

    print("\nPrueba 2: Depósitos") 
    cuenta_ahorros.depositar(2000.00) 
    cuenta_ahorros2.depositar(1000.00) 
    cuenta_corriente.depositar(1500.00) 

    print("\nPrueba 3: Retiros normales") 
    cuenta_ahorros.retirar(1000.00) 
    cuenta_corriente.retirar(2000.00) 

    print("\nPrueba 4: Sobregiro permitido") 
    cuenta_corriente.retirar(7000.00) 

    print("\nPrueba 5: Sobregiro no permitido") 
    cuenta_corriente.retirar(10000.00) 

    print("\nPrueba 6: Cálculo de interés con recursión") 
    saldo_1_mes = cuenta_ahorros.calcular_interes(1) 
    saldo_6_meses = cuenta_ahorros.calcular_interes(6) 
    saldo_12_meses = cuenta_ahorros.calcular_interes(12) 

    print(f"Saldo estimado luego de 1 mes: RD${saldo_1_mes:.2f}") 
    print(f"Saldo estimado luego de 6 meses: RD${saldo_6_meses:.2f}") 
    print(f"Saldo estimado luego de 12 meses: RD${saldo_12_meses:.2f}") 

    print("\nPrueba 7: Crear banco y registrar cuentas") 
    banco = Banco("Banco Python") 

    banco.abrir_cuenta(cuenta_ahorros) 
    banco.abrir_cuenta(cuenta_ahorros2) 
    banco.abrir_cuenta(cuenta_corriente) 
    banco.abrir_cuenta(cuenta_demo) 

    banco.reporte_total() 

    print("\nPrueba 8: Cuenta con mayor saldo") 
    mayor = banco.cuenta_mayor_saldo() 
 
    if mayor is not None: 
        print(mayor) 

    print("\nPrueba 9: Imprimir historial") 
    cuenta_corriente.imprimir_historial() 

    print("\nPrueba 10: Demostrar polimorfismo") 
    lista_cuentas: list[CuentaBancaria] = [ 
        cuenta_ahorros, 
        cuenta_ahorros2, 
        cuenta_corriente, 
        cuenta_demo 
    ] 

    for cuenta in lista_cuentas: 
        print(cuenta) 

    print("\nPrueba 11: Validar número de cuenta") 
    print("Número válido 123456:", Banco.validar_numero_cuenta("123456")) 
    print("Número inválido ABC123:", Banco.validar_numero_cuenta("ABC123")) 

    print("\nPrueba 12: Buscar y cerrar cuenta") 
    cuenta_buscada = banco.buscar_cuenta("111222") 

    if cuenta_buscada is not None: 
        print("Cuenta encontrada:") 
        print(cuenta_buscada) 

    banco.cerrar_cuenta("111222") 
    print("\nReporte luego de cerrar la cuenta demo:") 

    banco.reporte_total() 

 