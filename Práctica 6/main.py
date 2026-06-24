"""
main.py — Pipeline principal del Taller Integrador MCD505L · Unidad 6
Ejecuta: python main.py

Pasos:
  1. Scraping por categoría con paginación
  2. Limpieza con regex
  3. Exportar CSV
  4. Análisis con pandas + gráfica
"""
import sys
import time
import pandas as pd

from scraper  import get_category_urls, iter_pages
from parser   import extraer_libros
from limpieza import limpiar
from analisis import generar_grafica, imprimir_reporte

CSV_PATH    = "catalogo_libros.csv"
GRAFICA_PATH = "grafica_analisis.png"


def main() -> None:
    inicio_total = time.time()

    print("=" * 62)
    print("   TALLER INTEGRADOR — Catálogo de books.toscrape.com")
    print("   MCD505L · Laboratorio de IA con Python · Unidad 6")
    print("=" * 62)

    # ── FASE 1: Obtener categorías ────────────────────────────────────────
    print("\n[1/4] Descargando lista de categorías…")
    categorias = get_category_urls()
    if not categorias:
        print("ERROR: No se pudieron obtener las categorías. Verifica la conexión.")
        sys.exit(1)
    print(f"  ✓ {len(categorias)} categorías encontradas.")

    # ── FASE 2: Scraping libro a libro por categoría ───────────────────────
    print(f"\n[2/4] Scrapeando libros (esto toma ~2–3 min)…")
    t_scraping = time.time()
    registros: list[dict] = []

    for idx, (nombre, url) in enumerate(categorias, start=1):
        antes = len(registros)
        for html, _ in iter_pages(url):
            libros_pagina = extraer_libros(html, nombre)
            registros.extend(libros_pagina)
        encontrados = len(registros) - antes
        print(f"  [{idx:02d}/{len(categorias)}] {nombre:<30}  +{encontrados:>3} libros")

    duracion_scraping = time.time() - t_scraping
    print(f"\n  ✓ Total extraído: {len(registros):,} registros en {duracion_scraping:.1f}s")

    # ── FASE 3: Limpieza ──────────────────────────────────────────────────
    print("\n[3/4] Limpiando y estructurando datos…")
    df_raw = pd.DataFrame(registros)
    df     = limpiar(df_raw)

    nulos = df.isnull().sum().sum()
    duplicados_eliminados = len(df_raw) - len(df)
    print(f"  ✓ Registros limpios: {len(df):,}")
    print(f"  ✓ Duplicados/inválidos eliminados: {duplicados_eliminados}")
    print(f"  ✓ Valores nulos restantes: {nulos}")
    print(f"  ✓ Columnas: {list(df.columns)}")
    print(f"  ✓ Rango de precios: £{df['precio'].min():.2f} – £{df['precio'].max():.2f}")

    df.to_csv(CSV_PATH, index=False)
    print(f"  ✓ CSV exportado → {CSV_PATH}")

    # ── FASE 4: Análisis + gráfica ────────────────────────────────────────
    print("\n[4/4] Generando análisis y gráfica…")
    generar_grafica(df, GRAFICA_PATH)
    imprimir_reporte(df)

    # ── Resumen final ─────────────────────────────────────────────────────
    duracion_total = time.time() - inicio_total
    print("=" * 62)
    print(f"  Pipeline completado en {duracion_total:.1f}s")
    print(f"  Archivos generados:")
    print(f"    • {CSV_PATH}")
    print(f"    • {GRAFICA_PATH}")
    print("=" * 62)


if __name__ == "__main__":
    main()
