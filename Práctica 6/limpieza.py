"""
limpieza.py — Convierte precios y ratings a tipos numéricos con expresiones regulares.
MCD505L · Taller Integrador · Unidad 6
"""
import re
import pandas as pd

# Mapa de palabras de rating → entero
RATING_MAP: dict[str, int] = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

# Patrón reutilizable para extraer número decimal de un string de precio
_PRECIO_RE = re.compile(r"[\d]+\.[\d]+|[\d]+")


# Funciones atómicas de conversión
def precio_a_float(txt: str) -> float:
    """
    Convierte un texto de precio a float.
    Ejemplos: 'Â£51.77' → 51.77 | '£12.34' → 12.34 | '9.99' → 9.99
    Devuelve float('nan') si no encuentra número.
    """
    match = _PRECIO_RE.search(txt)
    return float(match.group()) if match else float("nan")


def rating_a_int(txt: str) -> int:
    """
    Convierte la clase CSS de rating a entero.
    Ejemplos: 'Three' → 3 | 'Five' → 5
    Devuelve 0 si el valor no se reconoce.
    """
    return RATING_MAP.get(str(txt).strip().title(), 0)


def normalizar_categoria(txt: str) -> str:
    """Limpia espacios y capitaliza el nombre de categoría."""
    return str(txt).strip().title()


# limpiar el DataFrame completo
def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas las conversiones al DataFrame crudo.

    - precio_raw (str) → precio (float)
    - rating_raw (str) → rating (int)
    - categoria  (str) → normalizada
    - Elimina duplicados exactos
    - Elimina filas con precio o rating inválidos

    Returns:
        DataFrame limpio con columnas: titulo, categoria, precio, rating.
    """
    clean = df.copy()

    # Estilo funcional con .map() y lambdas
    clean["precio"]    = clean["precio_raw"].map(precio_a_float)
    clean["rating"]    = clean["rating_raw"].map(rating_a_int)
    clean["categoria"] = clean["categoria"].map(normalizar_categoria)

    # Eliminar columnas raw (ya no se necesitan)
    clean = clean.drop(columns=["precio_raw", "rating_raw"])

    # Reordenar columnas
    clean = clean[["titulo", "categoria", "precio", "rating"]]

    # Quitar duplicados y filas con datos inválidos
    clean = clean.drop_duplicates()
    clean = clean[clean["precio"].notna() & (clean["rating"] > 0)]
    clean = clean.reset_index(drop=True)

    return clean
