"""
scraper.py — Descarga páginas de books.toscrape.com.
"""
import time
import requests
from bs4 import BeautifulSoup
from typing import Generator, Optional

BASE_URL  = "https://books.toscrape.com/"
HEADERS   = {"User-Agent": "MCD505L-BooksScraper/1.0 (educational-project)"}
DELAY_SEG = 0.1   


def fetch(url: str, retries: int = 3, backoff: float = 2.0) -> Optional[str]:
    """
    GET de una URL; devuelve HTML (str) o None si fallan todos los intentos.
    Usa backoff exponencial entre reintentos.
    """
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as exc:
            espera = backoff ** attempt
            print(f"    intento {attempt+1}/{retries} falló ({exc}). Reintentando en {espera:.0f}s…")
            time.sleep(espera)
    print(f"    ✗ No se pudo obtener: {url}")
    return None


# Extrae lista de categorías del sidebar
def get_category_urls() -> list[tuple[str, str]]:
    """
    Extrae todas las categorías del sidebar de la portada.
    Devuelve: [(nombre_categoria, url_categoria), ...]
    """
    html = fetch(BASE_URL)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    return [
        (a.get_text(strip=True), BASE_URL + a["href"])
        for a in soup.select("ul.nav-list > li > ul > li > a")
    ]


# Generador de páginas
def iter_pages(start_url: str) -> Generator[tuple[str, str], None, None]:
    """
    Generador que hace yield de (html, url_actual) para cada página,
    siguiendo el enlace 'next' automáticamente.
    """
    url = start_url
    while url:
        html = fetch(url)
        if html is None:
            return
        yield html, url

        # Resolver URL del botón 'next' (puede ser relativa)
        soup     = BeautifulSoup(html, "html.parser")
        next_btn = soup.select_one("li.next > a")
        if next_btn:
            base = url.rsplit("/", 1)[0] + "/"
            url  = base + next_btn["href"]
        else:
            url = None

        time.sleep(DELAY_SEG)
