```
Practica 6/
├── scraper.py              # Descarga páginas con paginación
├── parser.py               # Extrae datos con BeautifulSoup
├── limpieza.py             # Limpia precios y ratings con regex
├── analisis.py             # Análisis pandas + gráfica matplotlib
├── main.py                 # Script orquestador del pipeline
├── requirements.txt        # Dependencias
└── README.md               # Este archivo
```

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
python main.py
```

El pipeline tarda aproximadamente 2–3 minutos (debido a las pausas entre requests).

### Archivos generados

| Archivo              | Descripción                              |
|----------------------|------------------------------------------|
| `catalogo_libros.csv`| DataFrame completo (título/categoría/precio/rating) |
| `grafica_analisis.png`| Gráfica triple: precio por rating, distribución, top categorías |

---

## Preguntas que responde

| # | Pregunta |
|---|----------|
| 1 | ¿Cuál es el precio promedio por categoría? |
| 2 | ¿Cuántos libros hay por nivel de rating (1–5 estrellas)? |
| 3 | ¿Cuáles son los 10 libros más caros? |

---

## Temas que integra

- **Web scraping** — `requests` + `BeautifulSoup`
- **Regex** — limpieza de precios (`£` / `Â£`) y ratings
- **Funcional** — `map()`, comprensiones de listas, `filter()`
- **Módulos / Paquetes** — código separado en `.py` con `__init__.py`
- **pandas** — `groupby`, `nlargest`, `apply`, `to_csv`
- **Visualización** — gráfica triple con `matplotlib`

---

## Descripción de módulos

### `scraper.py`
- `fetch(url)` — GET con reintentos exponenciales
- `get_category_urls()` — extrae las ~50 categorías del sidebar
- `iter_pages(start_url)` — generador que sigue el botón "next"

### `parser.py`
- `extraer_libros(html, categoria)` — devuelve lista de dicts con datos crudos

### `limpieza.py`
- `precio_a_float(txt)` — `'Â£51.77'` → `51.77`
- `rating_a_int(txt)` — `'Three'` → `3`
- `limpiar(df)` — aplica ambas conversiones y elimina duplicados

### `analisis.py`
- `precio_promedio_por_categoria(df)`
- `libros_por_rating(df)`
- `top_10_mas_caros(df)`
- `generar_grafica(df, path)`
- `imprimir_reporte(df)`

---

