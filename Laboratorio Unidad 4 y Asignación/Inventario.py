# Parte A
def calcular_precio_final(precio_base:float, *descuentos:float, impuestos:float = 0.18, moneda:str = "DOP") -> tuple[float,str]:
    """
    asdadadadasdasdasdsadasdasdd
    """
    precio = precio_base
    for d in descuentos:
        precio *= (1 - d)
    precio *= (1 + impuestos)
    return round(precio,2), moneda

def generar_reporte(**filtros) -> None:
    """
    asdasdadasdasdasdad
    """
    print(" Reporte:")
    if not filtros:
        print("(sin filtros aplicados)")
    for clave, valor in filtros.items():
        print(f" {clave}: {valor}")

catalogo: list[dict] = [
    {"nombre": "Laptop Lenovo ThinkPad E14", "precio": 48500.00},
    {"nombre": "Monitor Samsung 24 pulgadas", "precio": 10500.00},
    {"nombre": "Teclado Mecanico Redragon K552", "precio": 2450.00},
    {"nombre": "Mouse Logitech G203", "precio": 1650.00},
    {"nombre": "Memoria USB Kingston 128GB", "precio": 850.00},
    {"nombre": "Disco SSD Kingston NV2 1TB", "precio": 4200.00},
    {"nombre": "Audifonos Bluetooth JBL Tune 520BT", "precio": 3200.00},
    {"nombre": "Webcam Logitech C920", "precio": 4500.00},
    {"nombre": "Curso Python para Principiantes", "precio": 1500.00},
    {"nombre": "Curso Analisis de Datos con Python", "precio": 2500.00}
]

#productos_caros: list[dict] = list(filter(lambda p: p["precio" > 1000, catalogo]))

#catalogo_ordenado: list[dict] = sorted( catalogo, key=lambda p: p["precio"])


# Parte B
class Producto:
    total_producto: int = 0

    def __init__(self,nombre: str,precio: float,categoria: str,stock: int) -> None:
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.__stock = stock
        Producto.total_producto += 1
    
    def agregar_stock(self, cantidad:int) -> None:
        if cantidad <= 0:
            print("La cantidad a agregar debe ser positiva") 
            return
        self.__stock += cantidad
        print(f"Stock de {self.nombre} actualizado a {self.__stock} unidades.")

    def reducir_stock(self, cantidad:int) -> None:
        if cantidad <= 0: 
            print("La cantidad a reducir debe positivo")
            return
        if cantidad > self.__stock: 
            print(f"stock insuficiente. Cantidad disponible: {self.__stock}")
            return
        self.__stock -= cantidad
        print(f"Stock de {self.nombre} actualizado a {self.__stock} unidades.")
    
    def obtener_stock(self) -> int: return self.__stock

    def valor_total(self) -> float: return self.precio * self.__stock 

    def descripcion(self) -> str:
        return(
            f"[{self.categoria}] {self.nombre}"
            f"${self.precio:.2f} x {self.__stock} DOP = ${self.valor_total():.2f}"
        )
    
    def __str__(self) -> str:
        return self.descripcion()
    
class ProductoD(Producto):
    def __init__(self, nombre: str, precio: float, categoria: str, stock: int, url_descargar: str) -> None:
        super().__init__(nombre, precio, categoria, stock)
        self.url_descargar = url_descargar
    
    def reducir_stock(self, cantidad: int):
        print(f"{self.nombre} es digital - el stock no reduce")

    def descripcion(self):
        return super().descripcion() + f" Descarga: {self.url_descargar}"

class Inventario:
    def __init__(self) -> None:
        self.__productos: list[Producto] = []
    
    def agregar_producto(self, producto: Producto) -> list[Producto]:
        self.__productos.append(producto)

    def buscar_por_nombre(self,nombre: str) -> list[Producto]:
        resultado = list(filter(lambda p: nombre.lower() in p.nombre.lower(), self.__productos))
        if resultado:
            print(f"Resultado para {nombre}: ")
            for p in resultado:
                print(" ", p)
        else:
            print(f"No se encontraron productos con {nombre} de nombre")
        return resultado
    def listar_todos(self) -> None:
        if not self.__productos:
            print("Inventario vacio")
            return
        print("Inventario completo: ")
        for p in sorted(self.__productos, key = lambda p: p.nombre):
            print(" ",p)
        total = sum(map(lambda p: p.valor_total(), self.__productos))
        print(f"Total de instancias creadas: {Producto.total_producto}")
        print(f" Valor total del inventario: ${total:.2f}")


def ejecutar_pruebas() -> None:
    print("Pruebas")
    print("Precio Final")
    precio,moneda = calcular_precio_final(1000.00, 0.10, 0.05)
    print(f"Precio base: RD$1000, Descuentos 10% + 5%, Impuestos = 18%, moneda = DOP")
    print(f"Precio Final: ${precio} {moneda}")

    #print("Prueba 2: Generar reporte")
    #generar_reporte(categoria="Electronica", precio=5000, stock=10)

    print("Prueba 3: productos")
    p1 = Producto("Laptop Lenovo ThinkPad E14", 20000.00, "Electronica", 12)
    p2 = Producto("Escritorio", 7000, "Mueble o algo asi", 1)

    p1.agregar_stock(3)
    p1.reducir_stock(1)
    p1.reducir_stock(1000) #Debe fallar para probar la advertencia

    print("Prueba 4: Productos digitales")
    pd1 = ProductoD("Curso Python para Principiantes", 1500.00,"Educación",999,url_descargar="https://intec.edu.do")
    print(" ",pd1)
    pd1.reducir_stock(50) #No se debe reducir porque es un producto digital
    print(f"Stock tras intentar reducir la cantidad del producto: {pd1.obtener_stock()}")

    print("Prueba 5: inventario")
    inventario = Inventario()
    inventario.agregar_producto(p1)
    inventario.agregar_producto(p2)
    inventario.agregar_producto(pd1)
    inventario.listar_todos()
    inventario.buscar_por_nombre("Laptop Lenovo ThinkPad E14")
    inventario.buscar_por_nombre("Algo") #Debe fallar, porque no existe el producto algo


if __name__ == "__main__":
    ejecutar_pruebas()

        
    

    

        
    



    

    

    