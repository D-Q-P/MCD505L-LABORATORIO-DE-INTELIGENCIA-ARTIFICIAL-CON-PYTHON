# Parte A: Modulo de Funciones Utilitarias

def calcular_precio_final(
    precio_base: float,
    *descuentos: float,
    impuestos: float = 0.18,
    moneda: str = "DOP",
) -> tuple[float, str]:
    """Calcula el precio final aplicando descuentos sucesivos e impuestos.

    Los descuentos se encadenan: cada uno se aplica sobre el precio ya
    descontado por el anterior, no sobre el precio base. El impuesto se
    aplica una unica vez al final.

    Args:
        precio_base: Precio original del producto antes de descuentos.
        *descuentos: Descuentos expresados como decimales (ej: 0.10 = 10%). Se aplican en el orden en que se reciben.
        impuestos: Tasa de impuesto a aplicar al final. Por defecto 0.18 (18%).
        moneda: Codigo de moneda del precio resultante. Por defecto "DOP".

    Returns:
        Tupla (precio_final, moneda) con el precio redondeado a dos decimales.
    """
    precio = precio_base
    for descuento in descuentos:
        precio *= (1 - descuento)
    precio *= (1 + impuestos)
    return round(precio, 2), moneda


# Mapa de predicados para generar_reporte.
# Cada clave es el nombre del filtro que el caller puede pasar como kwarg.
# Cada valor es una funcion (producto, valor_filtro) -> bool que devuelve
# True si el producto cumple el criterio.
# Agregar un nuevo filtro es solo agregar una entrada aqui.
_FILTROS_SOPORTADOS: dict[str, callable] = {
    "nombre":     lambda p, v: v.lower() in p.nombre.lower(),
    "categoria":  lambda p, v: v.lower() in p.categoria.lower(),
    "precio_min": lambda p, v: p.precio >= v,
    "precio_max": lambda p, v: p.precio <= v,
    "stock_min":  lambda p, v: p.obtener_stock() >= v,
    "stock_max":  lambda p, v: p.obtener_stock() <= v,
}


def generar_reporte(productos: list, **filtros) -> list:
    """
    Filtra una lista de productos segun los criterios indicados e imprime el resultado.

    Aplica todos los filtros reconocidos de forma conjunta (AND logico): un
    producto aparece en el reporte solo si cumple todos los criterios a la vez.
    Los filtros no reconocidos se ignoran. Los resultados se ordenan
    alfabeticamente por nombre.

    Filtros soportados:
        nombre (str): El valor debe estar contenido en el nombre del producto (sin distincion de mayusculas).
        categoria (str):  El valor debe estar contenido en la categoria del producto (sin distincion de mayusculas).
        precio_min (float): Solo productos con precio >= precio_min.
        precio_max (float): Solo productos con precio <= precio_max.
        stock_min (int):  Solo productos con stock >= stock_min.
        stock_max (int):  Solo productos con stock <= stock_max.

    Args:
        productos: Lista de objetos Producto (o subclases) sobre la que aplicar filtros.
        **filtros: Criterios de filtrado como argumentos de palabra clave.

    Returns:
        Lista de productos que cumplen todos los filtros. Tambien imprime
        el reporte en la salida estandar.
    """
    filtros_activos = {k: v for k, v in filtros.items() if k in _FILTROS_SOPORTADOS}

    # all() con generador: corta en el primer predicado que falla
    resultado = sorted(
        (p for p in productos if all(_FILTROS_SOPORTADOS[k](p, v) for k, v in filtros_activos.items())),
        key=lambda p: p.nombre,
    )

    encabezado = ", ".join(f"{k}={v}" for k, v in filtros_activos.items())
    print(f"Reporte  {encabezado}:" if encabezado else "Reporte (sin filtros):")

    if resultado:
        for p in resultado:
            print(" ", p)
        print(f"{len(resultado)} producto(s) encontrado(s).")
    else:
        print(" Sin resultados para los filtros aplicados.")

    return resultado

# A3: Catalogo y operaciones con lambdas y funciones de orden superior
catalogo: list[dict] = [
    {"nombre": "Laptop Lenovo ThinkPad E14",         "precio": 48500.00},
    {"nombre": "Monitor Samsung 24 pulgadas",        "precio": 10500.00},
    {"nombre": "Teclado Mecanico Redragon K552",     "precio":  2450.00},
    {"nombre": "Mouse Logitech G203",                "precio":  1650.00},
    {"nombre": "Memoria USB Kingston 128GB",         "precio":   850.00},
    {"nombre": "Disco SSD Kingston NV2 1TB",         "precio":  4200.00},
    {"nombre": "Audifonos Bluetooth JBL Tune 520BT", "precio":  3200.00},
    {"nombre": "Webcam Logitech C920",               "precio":  4500.00},
    {"nombre": "Curso Python para Principiantes",    "precio":  1500.00},
    {"nombre": "Curso Analisis de Datos con Python", "precio":  2500.00},
]

# Productos con precio mayor a RD$1000
productos_caros: list[dict] = list(
    filter(lambda p: p["precio"] > 1000, catalogo)
)

# Catalogo ordenado por precio ascendente
catalogo_ordenado: list[dict] = sorted(
    catalogo, key=lambda p: p["precio"]
)

# Catalogo con 10% de descuento; {**p, ...} evita mutar los diccionarios originales
catalogo_con_descuento: list[dict] = list(
    map(lambda p: {**p, "precio": round(p["precio"] * 0.90, 2)}, catalogo)
)

# Parte B: Diseno de Clases
class Producto:
    """
    Producto fisico registrado en el inventario de la empresa.

    Gestiona nombre, precio, categoria y stock. El stock es privado y
    solo se modifica a traves de agregar_stock / reducir_stock para
    garantizar su integridad. Mantiene un contador de clase con el
    total de instancias creadas (incluye subclases).

    Attributes:
        total_producto (int): Contador de instancias creadas (atributo de clase).
        nombre (str): Nombre descriptivo del producto.
        precio (float): Precio unitario en la moneda base.
        categoria (str): Categoria del producto.
    """

    total_producto: int = 0

    def __init__(self, nombre: str, precio: float, categoria: str, stock: int) -> None:
        """
        Inicializa el producto e incrementa el contador de instancias.
        Args:
            nombre: Nombre del producto.
            precio: Precio unitario del producto.
            categoria: Categoria del producto.
            stock: Cantidad inicial en inventario (entero no negativo).
        """
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.__stock = stock
        Producto.total_producto += 1

    def agregar_stock(self, cantidad: int) -> None:
        """
        Incrementa el stock en la cantidad indicada.
        Args:
            cantidad: Unidades a agregar. Debe ser un entero positivo.
        """
        if cantidad <= 0:
            print("La cantidad a agregar debe ser positiva.")
            return
        self.__stock += cantidad
        print(f"Stock de {self.nombre} actualizado a {self.__stock} unidades.")

    def reducir_stock(self, cantidad: int) -> None:
        """
        Reduce el stock en la cantidad indicada, con validaciones previas.
        Args:
            cantidad: Unidades a reducir. Debe ser positivo y no superar el stock actual.
        """
        if cantidad <= 0:
            print("La cantidad a reducir debe ser positiva.")
            return
        if cantidad > self.__stock:
            print(f"Stock insuficiente. Cantidad disponible: {self.__stock}.")
            return
        self.__stock -= cantidad
        print(f"Stock de {self.nombre} actualizado a {self.__stock} unidades.")

    def obtener_stock(self) -> int:
        """
        Retorna el stock actual del producto.
        Returns:
            Unidades disponibles actualmente.
        """
        return self.__stock

    def valor_total(self) -> float:
        """
        Calcula el valor monetario total del stock disponible.
        Returns:
            Precio unitario multiplicado por el stock actual.
        """
        return self.precio * self.__stock

    def descripcion(self) -> str:
        """
        Genera una descripcion legible con categoria, precio, stock y valor total.
        Returns:
            Cadena formateada con los datos principales del producto.
        """
        return (
            f"[{self.categoria}] {self.nombre} - "
            f"${self.precio:.2f} x {self.__stock} uds = ${self.valor_total():.2f} DOP"
        )

    def __str__(self) -> str:
        """Delega en descripcion() para la representacion legible del producto."""
        return self.descripcion()


class ProductoD(Producto):
    """
    Producto digital con stock ilimitado; hereda de Producto.

    El stock no se reduce con las ventas porque el recurso digital puede
    descargarse cualquier numero de veces. Agrega la URL de descarga.

    Attributes:
        url_descargar (str): URL desde la cual el cliente accede al recurso digital.
    """

    def __init__(
        self,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int,
        url_descargar: str,
    ) -> None:
        """
        Inicializa el producto digital con su URL de descarga.
        Args:
            nombre: Nombre del producto.
            precio: Precio de venta.
            categoria: Categoria del producto.
            stock: Stock representativo (no disminuye con ventas).
            url_descargar: URL de acceso al recurso digital.
        """
        super().__init__(nombre, precio, categoria, stock)
        self.url_descargar = url_descargar

    def reducir_stock(self, cantidad: int) -> None:
        """
        Sobreescribe la reduccion: los productos digitales no consumen stock.
        Args:
            cantidad: Ignorado. Se mantiene por compatibilidad con la interfaz base.
        """
        print(f"{self.nombre} es digital - el stock no se reduce.")

    def descripcion(self) -> str:
        """
        Extiende la descripcion base con la URL de descarga.
        Returns:
            Descripcion del producto base mas la URL de descarga.
        """
        return super().descripcion() + f" | Descarga: {self.url_descargar}"


class Inventario:
    """
    Gestor de productos de tipo Producto o sus subclases.

    Mantiene una lista privada de productos. Los metodos de reporte
    delegan en la funcion utilitaria generar_reporte() de la Parte A,
    evitando duplicar la logica de filtrado.
    """

    def __init__(self) -> None:
        """
        Inicializa un inventario vacio.
        """
        self.__productos: list[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        """
        Registra un producto en el inventario.
        Args:
            producto: Instancia de Producto o cualquiera de sus subclases.
        """
        self.__productos.append(producto)

    def listar_todos(self) -> None:
        """
        Imprime todos los productos ordenados alfabeticamente, con totales.

        Muestra el valor total del inventario y el numero de instancias creadas.
        """
        if not self.__productos:
            print("Inventario vacio.")
            return
        print("Inventario completo:")
        for p in sorted(self.__productos, key=lambda p: p.nombre):
            print(" ", p)
        total = sum(p.valor_total() for p in self.__productos)
        print(f"Total de instancias creadas: {Producto.total_producto}")
        print(f"Valor total del inventario: ${total:.2f} DOP")

    def buscar_por_nombre(self, nombre: str) -> list[Producto]:
        """
        Busca productos cuyo nombre contenga la cadena indicada.
        Delega en generar_reporte usando el filtro 'nombre'.
        Args:
            nombre: Subcadena a buscar (sin distincion de mayusculas).

        Returns:
            Lista de productos coincidentes.
        """
        return generar_reporte(self.__productos, nombre=nombre)

    def reporte_filtrado(self, **filtros) -> list[Producto]:
        """
        Genera un reporte del inventario aplicando los filtros indicados.
        Delega directamente en generar_reporte(). Ver esa funcion para
        la lista completa de filtros soportados (categoria, precio_min,
        precio_max, stock_min, stock_max, nombre).

        Args:
            **filtros: Criterios de filtrado como argumentos de palabra clave.

        Returns:
            Lista de productos que cumplen todos los filtros.
        """
        return generar_reporte(self.__productos, **filtros)

    def reporte_stock_bajo(self, minimo: int = 5) -> list[Producto]:
        """
        Identifica productos con stock por debajo del umbral indicado.
        Delega en generar_reporte usando el filtro 'stock_max'.
        Args:
            minimo: Los productos con stock estrictamente menor a este
                    valor se incluyen en el reporte. Por defecto 5.

        Returns:
            Lista de productos con stock bajo.
        """
        return generar_reporte(self.__productos, stock_max=minimo - 1)



# Pruebas del sistema


def ejecutar_pruebas() -> None:
    """
    Pruebas que cubre todas las funciones y clases del sistema.

    Prueba 1: calcular_precio_final con multiples descuentos.
    Prueba 2: generar_reporte directamente con filtros sobre una lista.
    Prueba 3: Operaciones lambda sobre el catalogo (filter, sorted, map).
    Prueba 4: Producto fisico con manejo de stock.
    Prueba 5: ProductoD con intento de reduccion de stock.
    Prueba 6: Inventario con listar, buscar, reporte filtrado y stock bajo.
    """

    # --- Prueba 1: calcular_precio_final ---
    print("Prueba 1: calcular_precio_final")
    precio, moneda = calcular_precio_final(1000.00, 0.10, 0.05)
    print("  Precio base: RD$1000.00 | Descuentos: 10% + 5% | Impuestos: 18%")
    print(f"  Precio final: ${precio} {moneda}")

    # --- Prueba 2: generar_reporte ---
    print("\nPrueba 2: generar_reporte con lista de diccionarios del catalogo")
    # Para esta prueba usamos objetos simples que tienen los atributos necesarios;
    # generar_reporte trabaja sobre cualquier lista de Productos.
    p_test = [
        Producto("Monitor Samsung 24 pulgadas", 10500.00, "Electronica", 8),
        Producto("Teclado Mecanico Redragon K552", 2450.00, "Electronica", 15),
        Producto("Silla Ergonomica", 12000.00, "Mobiliario", 3),
    ]
    generar_reporte(p_test, categoria="Electronica", precio_max=5000)

    # --- Prueba 3: lambdas y funciones de orden superior ---
    print("\nPrueba 3: lambdas sobre el catalogo")
    print(f"  Productos con precio > 1000: {len(productos_caros)} de {len(catalogo)}")
    print(f"  Mas barato: {catalogo_ordenado[0]['nombre']} (${catalogo_ordenado[0]['precio']:.2f})")
    print(f"  Precio con 10% descuento - {catalogo[0]['nombre']}: ${catalogo_con_descuento[0]['precio']:.2f}")

    # --- Prueba 4: Producto fisico ---
    print("\nPrueba 4: Producto fisico")
    p1 = Producto("Laptop Lenovo ThinkPad E14", 20000.00, "Electronica", 12)
    p2 = Producto("Escritorio", 7000.00, "Mobiliario", 1)
    p1.agregar_stock(3)
    p1.reducir_stock(2)
    p1.reducir_stock(1000)  # Debe fallar: stock insuficiente

    # --- Prueba 5: ProductoD ---
    print("\nPrueba 5: ProductoD")
    pd1 = ProductoD(
        "Curso Python para Principiantes",
        1500.00,
        "Educacion",
        999,
        url_descargar="https://intec.edu.do",
    )
    print(" ", pd1)
    pd1.reducir_stock(50)  # No debe reducir el stock
    print(f"  Stock tras intento de reduccion: {pd1.obtener_stock()}")

    # --- Prueba 6: Inventario ---
    print("\nPrueba 6: Inventario")
    inventario = Inventario()
    inventario.agregar_producto(p1)
    inventario.agregar_producto(p2)
    inventario.agregar_producto(pd1)

    print()
    inventario.listar_todos()

    print()
    inventario.buscar_por_nombre("Laptop")       # Debe encontrar p1
    print()
    inventario.buscar_por_nombre("Algo")         # Sin resultados

    print()
    inventario.reporte_filtrado(categoria="Electronica")

    print()
    inventario.reporte_filtrado(precio_min=5000, precio_max=25000)

    print()
    inventario.reporte_stock_bajo(minimo=5)      # p2 (stock=1) debe aparecer


if __name__ == "__main__":
    ejecutar_pruebas()