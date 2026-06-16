from __future__ import annotations
from datetime import datetime
from typing import Optional, Union
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

#Excepcion Dimension error

class DimensionError(Exception):
    """
    Excepción lanzada cuando dos matrices son incompatibles para una operación.

    Attributes:
        operacion: Nombre de la operación que originó el error.
        dim_a:     Dimensiones de la primera matriz como (filas, columnas).
        dim_b:     Dimensiones de la segunda matriz como (filas, columnas).
    """

    def __init__(
        self,
        operacion: str,
        dim_a: tuple[int, int],
        dim_b: tuple[int, int],
    ) -> None:
        """
        Construye el mensaje descriptivo e inicializa la excepción base.

        Args:
            operacion: Nombre legible de la operación fallida.
            dim_a:     Forma de la primera matriz.
            dim_b:     Forma de la segunda matriz.
        """
        self.operacion: str = operacion
        self.dim_a: tuple[int, int] = dim_a
        self.dim_b: tuple[int, int] = dim_b
        mensaje: str = (
            f"[DimensionError] '{operacion}' imposible: "
            f"Matriz A {dim_a[0]}×{dim_a[1]} es incompatible "
            f"con Matriz B {dim_b[0]}×{dim_b[1]}."
        )
        super().__init__(mensaje)


#Clase Matriz

class Matriz:
    """
    Encapsula un array NumPy 2D y expone operaciones matriciales seguras.

    Los atributos de dimensiones y datos son privados; se acceden únicamente
    a través de propiedades (@property) para garantizar encapsulamiento.

    Attributes:
        _filas:    Número de filas (privado).
        _columnas: Número de columnas (privado).
        _datos:    Array NumPy 2D de tipo float (privado).
        nombre:    Etiqueta identificadora (p.ej. "A", "B", "A+B").
    """

    def __init__(
        self,
        filas: int,
        columnas: int,
        datos: Optional[np.ndarray] = None,
        nombre: str = "M",
    ) -> None:
        """
        Inicializa la matriz con dimensiones y valores opcionales.

        Args:
            filas:    Número de filas (debe ser > 0).
            columnas: Número de columnas (debe ser > 0).
            datos:    Array NumPy 2D existente. Si es None se crea una matriz de ceros.
            nombre:   Etiqueta de la matriz para visualización.

        Raises:
            ValueError: Si las dimensiones son inválidas o los datos no coinciden.
        """
        if filas <= 0 or columnas <= 0:
            raise ValueError(
                f"Dimensiones deben ser positivas: recibidas ({filas}×{columnas})."
            )
        self._filas: int = filas
        self._columnas: int = columnas
        self.nombre: str = nombre

        if datos is not None:
            arr = np.array(datos, dtype=float)
            if arr.shape != (filas, columnas):
                raise ValueError(
                    f"Datos incompatibles: esperado ({filas},{columnas}), "
                    f"recibido {arr.shape}."
                )
            self._datos: np.ndarray = arr
        else:
            self._datos = np.zeros((filas, columnas), dtype=float)

    #Propiedades

    @property
    def filas(self) -> int:
        """Número de filas de la matriz (solo lectura)."""
        return self._filas

    @property
    def columnas(self) -> int:
        """Número de columnas de la matriz (solo lectura)."""
        return self._columnas

    @property
    def datos(self) -> np.ndarray:
        """Copia del array NumPy interno (solo lectura)."""
        return self._datos.copy()

    @property
    def forma(self) -> tuple[int, int]:
        """Tupla (filas, columnas) — acceso rápido a las dimensiones."""
        return (self._filas, self._columnas)

    # ── Métodos mágicos ────────────────────────────────────────────────────

    def __str__(self) -> str:
        """
        Representación legible para el usuario con bordes y alineación.

        Returns:
            Cadena formateada con nombre, dimensiones y valores.
        """
        ancho: int = self._columnas * 10 + 4
        linea: str = "─" * ancho
        encabezado: str = f"  Matriz {self.nombre} ({self._filas}×{self._columnas})\n{linea}"
        filas_str: list[str] = [
            "  " + "  ".join(f"{v:8.4f}" for v in fila)
            for fila in self._datos
        ]
        return f"{encabezado}\n" + "\n".join(filas_str) + f"\n{linea}"

    def __repr__(self) -> str:
        """
        Representación técnica útil para depuración.

        Returns:
            Cadena con tipo, nombre, forma y datos NumPy.
        """
        return (
            f"Matriz(nombre={self.nombre!r}, forma={self.forma}, "
            f"datos=np.array({self._datos.tolist()}))"
        )

    # ── Operaciones entre matrices ─────────────────────────────────────────

    def sumar(self, otra: Matriz) -> Matriz:
        """
        Suma elemento a elemento con otra matriz de igual forma.

        Args:
            otra: Segunda operando (igual forma que self).

        Returns:
            Nueva Matriz resultado de A + B.

        Raises:
            DimensionError: Si las formas no coinciden.
        """
        if self.forma != otra.forma:
            raise DimensionError("Suma (A+B)", self.forma, otra.forma)
        return Matriz(self._filas, self._columnas, self._datos + otra._datos, "A+B")

    def restar(self, otra: Matriz) -> Matriz:
        """
        Resta elemento a elemento con otra matriz de igual forma.

        Args:
            otra: Segunda operando (igual forma que self).

        Returns:
            Nueva Matriz resultado de A - B.

        Raises:
            DimensionError: Si las formas no coinciden.
        """
        if self.forma != otra.forma:
            raise DimensionError("Resta (A-B)", self.forma, otra.forma)
        return Matriz(self._filas, self._columnas, self._datos - otra._datos, "A-B")

    def mult_elemento(self, otra: Matriz) -> Matriz:
        """
        Multiplicación elemento a elemento — producto de Hadamard (A ⊙ B).

        Args:
            otra: Segunda operando (igual forma que self).

        Returns:
            Nueva Matriz resultado del producto Hadamard.

        Raises:
            DimensionError: Si las formas no coinciden.
        """
        if self.forma != otra.forma:
            raise DimensionError("Hadamard (A⊙B)", self.forma, otra.forma)
        return Matriz(self._filas, self._columnas, self._datos * otra._datos, "A⊙B")

    def mult_matricial(self, otra: Matriz) -> Matriz:
        """
        Producto matricial estándar — requiere columnas(A) == filas(B).

        Args:
            otra: Segunda operando donde filas == self.columnas.

        Returns:
            Nueva Matriz de forma (self.filas × otra.columnas).

        Raises:
            DimensionError: Si las dimensiones son incompatibles.
        """
        if self._columnas != otra._filas:
            raise DimensionError("Multiplicación Matricial (A×B)", self.forma, otra.forma)
        resultado: np.ndarray = np.dot(self._datos, otra._datos)
        return Matriz(self._filas, otra._columnas, resultado, "A×B")

    def escalar(self, k: float) -> Matriz:
        """
        Multiplica todos los elementos por un escalar k.

        Args:
            k: Valor escalar por el que se multiplica la matriz.

        Returns:
            Nueva Matriz con cada elemento multiplicado por k.
        """
        return Matriz(self._filas, self._columnas, self._datos * k, f"{k}·{self.nombre}")

    def transpuesta(self) -> Matriz:
        """
        Calcula la transpuesta — intercambia filas y columnas.

        Returns:
            Nueva Matriz transpuesta de forma (columnas × filas).
        """
        t: np.ndarray = self._datos.T.copy()
        return Matriz(self._columnas, self._filas, t, f"{self.nombre}ᵀ")

    def determinante(self) -> float:
        """
        Calcula el determinante — solo para matrices cuadradas.

        Returns:
            Valor del determinante como float.

        Raises:
            ValueError: Si la matriz no es cuadrada.
        """
        if self._filas != self._columnas:
            raise ValueError(
                f"Determinante requiere matriz cuadrada. Actual: {self.forma}."
            )
        return float(np.linalg.det(self._datos))

    def inversa(self) -> Matriz:
        """
        Calcula la inversa — solo para matrices cuadradas no singulares.

        Returns:
            Nueva Matriz inversa de igual forma.

        Raises:
            ValueError: Si la matriz no es cuadrada o es singular.
        """
        if self._filas != self._columnas:
            raise ValueError(
                f"Inversa requiere matriz cuadrada. Actual: {self.forma}."
            )
        det: float = self.determinante()
        if abs(det) < 1e-10:
            raise ValueError(
                f"Matriz singular (det ≈ {det:.2e}): no existe la inversa."
            )
        return Matriz(
            self._filas, self._columnas,
            np.linalg.inv(self._datos),
            f"{self.nombre}⁻¹",
        )

    def rango(self) -> int:
        """
        Calcula el rango numérico de la matriz.

        Returns:
            Rango de la matriz como entero.
        """
        return int(np.linalg.matrix_rank(self._datos))

    def to_dataframe(self, encabezados: Optional[list[str]] = None) -> pd.DataFrame:
        """
        Convierte la matriz a un DataFrame de Pandas.

        Args:
            encabezados: Nombres de las columnas. Si es None se generan
                         automáticamente como Col_1, Col_2, ...

        Returns:
            DataFrame con los datos de la matriz.

        Raises:
            ValueError: Si la cantidad de encabezados no coincide con columnas.
        """
        if encabezados is None:
            encabezados = [f"Col_{j + 1}" for j in range(self._columnas)]
        if len(encabezados) != self._columnas:
            raise ValueError(
                f"Se necesitan {self._columnas} encabezados; "
                f"se proporcionaron {len(encabezados)}."
            )
        return pd.DataFrame(
            self._datos,
            columns=encabezados,
            index=[f"Fila_{i + 1}" for i in range(self._filas)],
        )


#Log

class SesionLog:
    """
    Gestiona el registro de operaciones en un archivo de texto.

    Usa 'finally' en el método 'cerrar()' para garantizar que el archivo
    siempre se cierre correctamente, incluso ante excepciones.

    Attributes:
        ruta:     Ruta del archivo de log.
        _archivo: Manejador del archivo (privado).
    """

    def __init__(self, ruta: str = "sesion_log.txt") -> None:
        """
        Abre el archivo de log y escribe el encabezado de la sesión.

        Args:
            ruta: Nombre o ruta del archivo de log.
        """
        self.ruta: str = ruta
        self._archivo = None
        try:
            self._archivo = open(ruta, "a", encoding="utf-8")
            ts: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._archivo.write(f"\n{'═' * 60}\n")
            self._archivo.write(f"  SESIÓN INICIADA: {ts}\n")
            self._archivo.write(f"{'═' * 60}\n")
            self._archivo.flush()
        except OSError as e:
            print(f"  No se pudo abrir '{ruta}': {e}")

    def registrar(self, mensaje: str, detalle: Optional[str] = None) -> None:
        """
        Escribe una entrada en el log con timestamp actual.

        Args:
            mensaje: Descripción corta de la operación.
            detalle: Resultado o información adicional (opcional).
        """
        if self._archivo is None:
            return
        try:
            ts: str = datetime.now().strftime("%H:%M:%S")
            self._archivo.write(f"\n[{ts}] {mensaje}\n")
            if detalle:
                for linea in detalle.splitlines():
                    self._archivo.write(f"         {linea}\n")
            self._archivo.flush()
        except OSError as e:
            print(f"  Error al escribir en log: {e}")

    def cerrar(self) -> None:
        """
        Cierra el archivo de log.

        Usa 'finally' para garantizar el cierre aunque ocurra un error
        al escribir el pie de la sesión.
        """
        try:
            if self._archivo and not self._archivo.closed:
                ts: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._archivo.write(f"\n{'─' * 60}\n")
                self._archivo.write(f"  SESIÓN CERRADA: {ts}\n")
                self._archivo.write(f"{'─' * 60}\n")
        finally:
            if self._archivo and not self._archivo.closed:
                self._archivo.close()


#Entrada de datos

def pedir_entero(
    mensaje: str,
    minimo: int = 1,
    maximo: int = 10,
) -> int:
    """
    Solicita un entero al usuario con validación y reintento ilimitado.

    Captura ValueError y TypeError mostrando un mensaje claro en cada intento
    fallido, sin terminar el programa.

    Args:
        mensaje: Texto del prompt mostrado al usuario.
        minimo:  Límite inferior aceptado (inclusivo).
        maximo:  Límite superior aceptado (inclusivo).

    Returns:
        Entero validado dentro del rango [minimo, maximo].
    """
    while True:
        try:
            valor: int = int(input(mensaje))
            if not (minimo <= valor <= maximo):
                raise ValueError(f"Debe estar entre {minimo} y {maximo}.")
            return valor
        except ValueError as e:
            print(f"    Entrada inválida: {e}  →  Intenta de nuevo.")
        except TypeError as e:
            print(f"    Error de tipo: {e}  →  Intenta de nuevo.")


def pedir_float(mensaje: str) -> float:
    """
    Solicita un número real al usuario con validación y reintento ilimitado.

    Captura ValueError y TypeError con mensajes informativos.

    Args:
        mensaje: Texto del prompt mostrado al usuario.

    Returns:
        Float válido ingresado por el usuario.
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("    Valor inválido. Ingresa un número (ej: 3, -2.5, 0.7).")
        except TypeError as e:
            print(f"    Error de tipo: {e}  →  Intenta de nuevo.")


def pedir_dimensiones(etiqueta: str) -> tuple[int, int]:
    """
    Solicita al usuario las dimensiones (filas × columnas) de una matriz.

    Args:
        etiqueta: Identificador de la matriz para el prompt (ej: "A").

    Returns:
        Tupla (filas, columnas) validada con valores entre 1 y 10.
    """
    print(f"\n  Dimensiones de la Matriz {etiqueta}:")
    filas: int = pedir_entero(f"    Filas    [1-10]: ", 1, 10)
    columnas: int = pedir_entero(f"    Columnas [1-10]: ", 1, 10)
    return filas, columnas


def pedir_valores(filas: int, columnas: int, nombre: str) -> Matriz:
    """
    Solicita al usuario el valor de cada celda de una matriz.

    Cada celda está protegida con pedir_float() que maneja errores y reintentos.

    Args:
        filas:    Número de filas de la matriz a construir.
        columnas: Número de columnas de la matriz a construir.
        nombre:   Etiqueta de la matriz para los prompts.

    Returns:
        Instancia de Matriz con los valores ingresados por el usuario.
    """
    print(f"\n  Ingresa los {filas * columnas} valores de la Matriz {nombre} "
          f"({filas}×{columnas}):")
    datos: np.ndarray = np.zeros((filas, columnas), dtype=float)
    for i in range(filas):
        for j in range(columnas):
            datos[i, j] = pedir_float(f"    [{nombre}][{i + 1},{j + 1}]: ")
    return Matriz(filas, columnas, datos, nombre)


#Matplotlib

def _anotar_celda(ax: plt.Axes, matriz: Matriz) -> None:
    """
    Escribe el valor numérico en cada celda del heatmap.

    Args:
        ax:     Ejes de Matplotlib donde dibujar las anotaciones.
        matriz: Matriz cuyos valores se anotarán.
    """
    for i in range(matriz.filas):
        for j in range(matriz.columnas):
            ax.text(
                j, i, f"{matriz.datos[i, j]:.2f}",
                ha="center", va="center",
                fontsize=max(6, 10 - max(matriz.filas, matriz.columnas)),
                color="black", fontweight="bold",
            )


def visualizar_matrices(
    m1: Matriz,
    m2: Matriz,
    ruta: str = "matrices_comparacion.png",
) -> None:
    """
    Genera una figura con dos subplots que compara ambas matrices mediante imshow.

    Cada subplot incluye: título, etiquetas de ejes, valores en celda y colorbar.
    La figura se guarda como PNG y se intenta mostrar en pantalla.

    Args:
        m1:   Primera matriz a comparar.
        m2:   Segunda matriz a comparar.
        ruta: Nombre del archivo PNG de salida.
    """
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Comparación de Matrices", fontsize=14, fontweight="bold", y=1.02)

    configs: list[tuple[plt.Axes, Matriz, str, str]] = [
        (axes[0], m1, "YlOrRd", f"Matriz {m1.nombre}"),
        (axes[1], m2, "YlGnBu", f"Matriz {m2.nombre}"),
    ]

    for ax, mat, cmap, titulo in configs:
        im = ax.imshow(mat.datos, cmap=cmap, aspect="auto")
        ax.set_title(titulo, fontsize=12, fontweight="bold")
        ax.set_xlabel("Columnas", fontsize=10)
        ax.set_ylabel("Filas", fontsize=10)
        ax.set_xticks(range(mat.columnas))
        ax.set_xticklabels([f"C{j + 1}" for j in range(mat.columnas)])
        ax.set_yticks(range(mat.filas))
        ax.set_yticklabels([f"F{i + 1}" for i in range(mat.filas)])
        plt.colorbar(im, ax=ax, label="Valor")
        _anotar_celda(ax, mat)

    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    print(f"  Figura guardada → '{ruta}'.")
    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)


def visualizar_resultado(
    resultado: Matriz,
    titulo: str = "Resultado de Operación",
    ruta: str = "resultado_operacion.png",
) -> None:
    """
    Visualiza una única matriz resultado con heatmap y gráfico de barras agrupadas.

    Incluye: subplots, títulos, etiquetas de ejes, colorbar y línea de cero.

    Args:
        resultado: Matriz a visualizar.
        titulo:    Título principal de la figura.
        ruta:      Nombre del archivo PNG de salida.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(titulo, fontsize=13, fontweight="bold")

    # Subplot 1: heatmap 
    im = ax1.imshow(resultado.datos, cmap="RdYlGn", aspect="auto")
    ax1.set_title(f"Mapa de calor — {resultado.nombre}", fontsize=11)
    ax1.set_xlabel("Columnas", fontsize=10)
    ax1.set_ylabel("Filas", fontsize=10)
    ax1.set_xticks(range(resultado.columnas))
    ax1.set_xticklabels([f"C{j + 1}" for j in range(resultado.columnas)])
    ax1.set_yticks(range(resultado.filas))
    ax1.set_yticklabels([f"F{i + 1}" for i in range(resultado.filas)])
    plt.colorbar(im, ax=ax1, label="Valor")
    _anotar_celda(ax1, resultado)

    # Subplot 2: barras agrupadas por fila
    x: np.ndarray = np.arange(resultado.columnas)
    n_filas: int = resultado.filas
    ancho: float = 0.75 / max(n_filas, 1)
    colores = plt.cm.tab10(np.linspace(0, 0.9, n_filas))

    for i in range(n_filas):
        offset: float = (i - n_filas / 2 + 0.5) * ancho
        ax2.bar(
            x + offset,
            resultado.datos[i],
            width=ancho,
            label=f"Fila {i + 1}",
            color=colores[i],
            alpha=0.85,
            edgecolor="white",
            linewidth=0.4,
        )

    ax2.set_title(f"Barras agrupadas — {resultado.nombre}", fontsize=11)
    ax2.set_xlabel("Columnas", fontsize=10)
    ax2.set_ylabel("Valor", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"C{j + 1}" for j in range(resultado.columnas)])
    ax2.legend(fontsize=8, loc="best")
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    ax2.grid(axis="y", alpha=0.3, linestyle=":")

    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    print(f"  Figura guardada → '{ruta}'.")
    try:
        plt.show()
    except Exception:
        pass
    plt.close(fig)

#Export csv

def exportar_csv(matriz: Matriz) -> None:
    """
    Exporta una matriz a un archivo CSV usando pandas.DataFrame.to_csv().

    Solicita al usuario el nombre del archivo y los encabezados de columna.
    El nombre y los encabezados son completamente configurables; si el usuario
    no los proporciona se usan valores por defecto.

    Args:
        matriz: Instancia de Matriz a exportar.
    """
    print(f"\n Exportar Matriz {matriz.nombre} "
          f"({matriz.filas}×{matriz.columnas}) a CSV")

    # Nombre del archivo
    nombre_raw: str = input("    Nombre del archivo (sin .csv) [Enter=automático]: ").strip()
    nombre_archivo: str = (
        nombre_raw.replace(" ", "_") if nombre_raw
        else f"matriz_{matriz.nombre.replace('⊙', 'H').replace('×', 'x')}"
    ) + ".csv"

    # Encabezados de columnas
    print(f"    Encabezados (separados por coma, {matriz.columnas} valores, Enter=auto):")
    enc_raw: str = input("    → ").strip()
    encabezados: Optional[list[str]] = None

    if enc_raw:
        candidatos: list[str] = [h.strip() for h in enc_raw.split(",")]
        if len(candidatos) == matriz.columnas:
            encabezados = candidatos
        else:
            print(f"  Se esperaban {matriz.columnas} encabezados; "
                  f"se usarán los automáticos.")

    try:
        df: pd.DataFrame = matriz.to_dataframe(encabezados)
        df.to_csv(nombre_archivo, index=True)
        print(f"  Exportado exitosamente → '{nombre_archivo}'.")
        print(f"\n  Vista previa:\n{df.to_string()}")
    except (OSError, ValueError) as e:
        print(f"  Error al exportar: {e}")

#Menu
MENU: dict[str, str] = {
    "1":  "Suma                A + B",
    "2":  "Resta               A - B",
    "3":  "Hadamard (elem.)    A ⊙ B",
    "4":  "Mult. matricial     A × B",
    "5":  "Escalar             k · A",
    "6":  "Escalar             k · B",
    "7":  "Transpuesta         Aᵀ",
    "8":  "Transpuesta         Bᵀ",
    "9":  "Determinante        det(A)",
    "10": "Determinante        det(B)",
    "11": "Inversa             A⁻¹",
    "12": "Inversa             B⁻¹",
    "13": "Rango               rank(A) y rank(B)",
    "14": "Visualizar A y B    → subplots PNG",
    "15": "Visualizar resultado de última operación",
    "16": "Exportar a CSV      (A, B o resultado)",
    "17": "Mostrar matrices actuales",
    "0":  "Salir",
}


def mostrar_menu() -> str:
    """
    Imprime el menú numerado de operaciones y retorna la opción validada.

    Captura ValueError y TypeError con reintento ilimitado.

    Returns:
        Cadena con el número de la opción seleccionada.
    """
    print(f"\n{'═' * 52}")
    print("  CALCULADORA MATRICIAL — MENÚ DE OPERACIONES")
    print(f"{'═' * 52}")
    for k, v in MENU.items():
        print(f"  [{k:>2}]  {v}")
    print(f"{'─' * 52}")

    while True:
        try:
            opcion: str = input("  → Opción: ").strip()
            if opcion not in MENU:
                raise ValueError(f"'{opcion}' no es una opción válida.")
            return opcion
        except ValueError as e:
            print(f"  {e}  Ingresa un número del 0 al {len(MENU) - 1}.")
        except TypeError as e:
            print(f"  Error de tipo: {e}")


def _mostrar_y_loguear(
    titulo: str,
    resultado: Union[Matriz, float, int],
    log: SesionLog,
) -> None:
    """
    Imprime un resultado en consola y lo registra en el log de sesión.

    Args:
        titulo:    Descripción de la operación realizada.
        resultado: Valor matricial o escalar resultante.
        log:       Instancia de SesionLog activa.
    """
    print(f"\n  ── Resultado: {titulo} ──")
    if isinstance(resultado, Matriz):
        print(resultado)
        log.registrar(titulo, str(resultado))
    else:
        print(f"  = {resultado:.6f}")
        log.registrar(titulo, f"= {resultado:.6f}")


#Main

def main() -> None:
    """
    Punto de entrada del programa.

    Flujo:
    1. Solicita dimensiones y valores de las dos matrices.
    2. Ejecuta el bucle del menú hasta que el usuario elija 0.
    3. Cierra el log en el bloque finally, garantizando su escritura.
    """
    print("CALCULADORA MATRICIAL INTERACTIVA")

    log = SesionLog("sesion_log.txt")
    ultimo_resultado: Optional[Matriz] = None

    try:
        # Ingreso de matrices
        print("\n INGRESO DE LA MATRIZ A")
        fa, ca = pedir_dimensiones("A")
        mat_a: Matriz = pedir_valores(fa, ca, "A")
        log.registrar("Matriz A ingresada", str(mat_a))

        print("\n INGRESO DE LA MATRIZ B")
        fb, cb = pedir_dimensiones("B")
        mat_b: Matriz = pedir_valores(fb, cb, "B")
        log.registrar("Matriz B ingresada", str(mat_b))

        print("\n   Matrices cargadas correctamente.\n")
        print(mat_a)
        print(mat_b)

        # Bucle del menú
        while True:
            opcion: str = mostrar_menu()

            try:
                # Salir 
                if opcion == "0":
                    print("\n  Sesión finalizada. Log guardado en 'sesion_log.txt'.")
                    log.registrar("Sesión cerrada por el usuario.")
                    break

                # Suma 
                elif opcion == "1":
                    ultimo_resultado = mat_a.sumar(mat_b)
                    _mostrar_y_loguear("A + B", ultimo_resultado, log)

                # Resta 
                elif opcion == "2":
                    ultimo_resultado = mat_a.restar(mat_b)
                    _mostrar_y_loguear("A - B", ultimo_resultado, log)

                # Hadamard (mult_elemento)
                elif opcion == "3":
                    ultimo_resultado = mat_a.mult_elemento(mat_b)
                    _mostrar_y_loguear("A ⊙ B (Hadamard)", ultimo_resultado, log)

                # Multiplicación matricial
                elif opcion == "4":
                    ultimo_resultado = mat_a.mult_matricial(mat_b)
                    _mostrar_y_loguear("A × B (matricial)", ultimo_resultado, log)

                # Escalar k·A
                elif opcion == "5":
                    k: float = pedir_float("  Escalar k para A: ")
                    ultimo_resultado = mat_a.escalar(k)
                    _mostrar_y_loguear(f"{k} · A", ultimo_resultado, log)

                # Escalar k·B
                elif opcion == "6":
                    k = pedir_float("  Escalar k para B: ")
                    ultimo_resultado = mat_b.escalar(k)
                    _mostrar_y_loguear(f"{k} · B", ultimo_resultado, log)

                # Transpuesta Aᵀ
                elif opcion == "7":
                    ultimo_resultado = mat_a.transpuesta()
                    _mostrar_y_loguear("Transpuesta Aᵀ", ultimo_resultado, log)

                # Transpuesta Bᵀ
                elif opcion == "8":
                    ultimo_resultado = mat_b.transpuesta()
                    _mostrar_y_loguear("Transpuesta Bᵀ", ultimo_resultado, log)

                # Determinante A 
                elif opcion == "9":
                    det_a: float = mat_a.determinante()
                    _mostrar_y_loguear("det(A)", det_a, log)

                # Determinante B 
                elif opcion == "10":
                    det_b: float = mat_b.determinante()
                    _mostrar_y_loguear("det(B)", det_b, log)

                # Inversa A⁻¹ 
                elif opcion == "11":
                    ultimo_resultado = mat_a.inversa()
                    _mostrar_y_loguear("A⁻¹ (inversa de A)", ultimo_resultado, log)

                # Inversa B⁻¹ 
                elif opcion == "12":
                    ultimo_resultado = mat_b.inversa()
                    _mostrar_y_loguear("B⁻¹ (inversa de B)", ultimo_resultado, log)

                # Rangos 
                elif opcion == "13":
                    ra: int = mat_a.rango()
                    rb: int = mat_b.rango()
                    print(f"\n  Rangos:")
                    print(f"    rank(A) = {ra}")
                    print(f"    rank(B) = {rb}")
                    log.registrar(
                        "Rangos",
                        f"rank(A) = {ra}  |  rank(B) = {rb}",
                    )

                #  Visualización comparativa A y B 
                elif opcion == "14":
                    visualizar_matrices(mat_a, mat_b)
                    log.registrar(
                        "Visualización generada",
                        "matrices_comparacion.png",
                    )

                #  Visualización del último resultado 
                elif opcion == "15":
                    if ultimo_resultado is None:
                        print("  Aún no hay resultado disponible. "
                              "Realiza una operación primero.")
                    else:
                        visualizar_resultado(
                            ultimo_resultado,
                            titulo=f"Resultado: {ultimo_resultado.nombre}",
                            ruta="resultado_operacion.png",
                        )
                        log.registrar(
                            f"Visualización de '{ultimo_resultado.nombre}'",
                            "resultado_operacion.png",
                        )

                #  Exportar a CSV 
                elif opcion == "16":
                    print("\n  ¿Qué matriz deseas exportar?")
                    print("  [1] Matriz A")
                    print("  [2] Matriz B")
                    if ultimo_resultado is not None:
                        print(f"  [3] Último resultado ({ultimo_resultado.nombre})")
                    sub: str = input("  → Opción: ").strip()
                    if sub == "1":
                        exportar_csv(mat_a)
                        log.registrar("CSV exportado: Matriz A")
                    elif sub == "2":
                        exportar_csv(mat_b)
                        log.registrar("CSV exportado: Matriz B")
                    elif sub == "3" and ultimo_resultado is not None:
                        exportar_csv(ultimo_resultado)
                        log.registrar(
                            f"CSV exportado: resultado {ultimo_resultado.nombre}"
                        )
                    else:
                        print("  Opción inválida.")

                # Mostrar matrices actuales 
                elif opcion == "17":
                    print("\n  MATRICES ACTUALES:")
                    print(mat_a)
                    print(mat_b)
                    if ultimo_resultado is not None:
                        print("\n  Último resultado:")
                        print(ultimo_resultado)

            # Manejo de errores dentro del menú (sin terminar el programa)
            except DimensionError as de:
                print(f"\n  {de}")
                log.registrar(f"ERROR de dimensión", str(de))

            except ValueError as ve:
                print(f"\n  Error de valor: {ve}")
                log.registrar(f"ERROR de valor", str(ve))

            except np.linalg.LinAlgError as la:
                print(f"\n  Error de álgebra lineal: {la}")
                log.registrar(f"ERROR de álgebra lineal", str(la))

            except Exception as ex:
                print(f"\n  Error inesperado: {ex}")
                log.registrar(f"ERROR inesperado", str(ex))

    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido (Ctrl+C).")
        log.registrar("Sesión interrumpida por Ctrl+C")

    finally:
        # Siempre se cierra el log, sin importar cómo termine el programa
        log.cerrar()
        print("  Cerrando")

if __name__ == "__main__":
    main()