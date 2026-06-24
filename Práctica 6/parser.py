"""
parser.py — Extrae título, precio, rating y categoría de cada libro.
"""
from bs4 import BeautifulSoup

# Palabras de rating en el HTML → número de estrellas
RATING_MAP: dict[str, int] = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}


def extraer_libros(html: str, categoria: str = "Sin categoría") -> list[dict]:
    """
    Extrae todos los libros de una página de listado del catálogo.

    Args:
        html:      HTML de la página (una sola página de listado).
        categoria: Nombre de la categoría a la que pertenecen estos libros.

    Returns:
        Lista de dicts con claves: titulo, precio_raw, rating_raw, categoria.
        Los valores raw se limpian después en limpieza.py.
    """
    soup = BeautifulSoup(html, "html.parser")

    # List comprenhension: procesamos cada <article class="product_pod">
    return [
        {
            "titulo":     article.h3.a["title"],
            "precio_raw": article.select_one(".price_color").get_text(strip=True),
            "rating_raw": article.select_one("p.star-rating")["class"][1],
            "categoria":  categoria,
        }
        for article in soup.select("article.product_pod")
    ]

def extraer_categorias_html(html: str) -> list[str]:
    """
    (Utilidad) Extrae los nombres de categorías listados en el sidebar.
    Principalmente para inspección o validación.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [a.get_text(strip=True) for a in soup.select("ul.nav-list > li > ul > li > a")]
