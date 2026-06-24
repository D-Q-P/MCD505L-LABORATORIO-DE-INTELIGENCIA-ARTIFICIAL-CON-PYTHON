"""
analisis.py — Responde las preguntas del taller con pandas; genera gráfica doble.
MCD505L · Taller Integrador · Unidad 6

Preguntas:
  1. ¿Cuál es el precio promedio por categoría?
  2. ¿Cuántos libros hay por nivel de rating (1 a 5 estrellas)?
  3. ¿Cuáles son los 10 libros más caros?
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # backend sin GUI → guarda a archivo
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Paleta por número de estrellas (1→rojo, 5→azul)
_COLORES_RATING = {
    1: "#d62728",   # rojo
    2: "#ff7f0e",   # naranja
    3: "#f5c518",   # amarillo-dorado
    4: "#2ca02c",   # verde
    5: "#1f77b4",   # azul
}

ESTRELLAS = {1: "★☆☆☆☆", 2: "★★☆☆☆", 3: "★★★☆☆", 4: "★★★★☆", 5: "★★★★★"}

# Q1: Precio promedio por categoría
def precio_promedio_por_categoria(df: pd.DataFrame) -> pd.Series:
    """
    Agrupa por categoría y calcula el precio promedio (redondeado a 2 decimales).
    Devuelve Serie ordenada de mayor a menor precio promedio.
    """
    return (
        df.groupby("categoria")["precio"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .rename("precio_promedio_GBP")
    )


# Q2: Libros por nivel de rating
def libros_por_rating(df: pd.DataFrame) -> pd.Series:
    """
    Cuenta cuántos libros hay por cada nivel de rating (1–5).
    Devuelve Serie indexada por rating (int), ordenada ascendente.
    """
    return (
        df.groupby("rating")
        .size()
        .rename("cantidad_libros")
        .sort_index()
    )


# Q3: Top 10 libros más caros
def top_10_mas_caros(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve los 10 libros con mayor precio.
    Columnas: titulo, categoria, precio, rating.
    """
    return (
        df.nlargest(10, "precio")[["titulo", "categoria", "precio", "rating"]]
        .reset_index(drop=True)
    )


# Generador de gráfica
def generar_grafica(df: pd.DataFrame, output_path: str = "grafica_analisis.png") -> None:
    """
    Genera y guarda una figura con 3 subgráficas:
      - (izquierda) Precio promedio por rating (barras)
      - (centro)    Distribución de libros por rating (pastel)
      - (derecha)   Top 10 categorías más caras (barras horizontales)
    """
    resumen_rating  = df.groupby("rating")["precio"].mean().round(1)
    conteo_rating   = libros_por_rating(df)
    top_categorias  = precio_promedio_por_categoria(df).head(10)

    colores_barras  = [_COLORES_RATING[r] for r in resumen_rating.index]
    colores_pastel  = [_COLORES_RATING[r] for r in conteo_rating.index]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor("#f7f7f7")

    # Subgráfica 1: precio promedio por rating 
    bars = axes[0].bar(
        [ESTRELLAS[r] for r in resumen_rating.index],
        resumen_rating.values,
        color=colores_barras,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    axes[0].bar_label(bars, labels=[f"£{v}" for v in resumen_rating.values],
                      padding=4, fontsize=10, fontweight="bold")
    axes[0].set_title("Precio promedio por rating", fontsize=12, fontweight="bold", pad=12)
    axes[0].set_xlabel("Nivel de rating", fontsize=10)
    axes[0].set_ylabel("Precio promedio (£)", fontsize=10)
    axes[0].set_ylim(0, resumen_rating.max() * 1.22)
    axes[0].yaxis.set_major_formatter(mticker.FormatStrFormatter("£%.0f"))
    axes[0].set_facecolor("#f0f0f0")
    axes[0].grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    axes[0].tick_params(axis="x", labelsize=9)

    # Subgráfica 2: distribución por rating (pastel)
    etiquetas = [f"{ESTRELLAS[r]}\n{v} libros" for r, v in zip(conteo_rating.index, conteo_rating.values)]
    wedges, texts, autotexts = axes[1].pie(
        conteo_rating.values,
        labels=etiquetas,
        colors=colores_pastel,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2},
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    axes[1].set_title("Distribución de libros por rating", fontsize=12, fontweight="bold", pad=12)

    #  Subgráfica 3: top 10 categorías más caras
    top_cat_inv = top_categorias.iloc[::-1]   # invertir para que el mayor quede arriba
    colores_cat = plt.cm.RdYlGn_r([i / len(top_cat_inv) for i in range(len(top_cat_inv))])
    hbars = axes[2].barh(
        top_cat_inv.index,
        top_cat_inv.values,
        color=colores_cat,
        edgecolor="white",
        linewidth=0.8,
    )
    axes[2].bar_label(hbars, labels=[f"£{v:.2f}" for v in top_cat_inv.values],
                      padding=4, fontsize=9)
    axes[2].set_title("Top 10 categorías más caras\n(precio promedio)", fontsize=12, fontweight="bold", pad=12)
    axes[2].set_xlabel("Precio promedio (£)", fontsize=10)
    axes[2].set_facecolor("#f0f0f0")
    axes[2].grid(axis="x", linestyle="--", alpha=0.5)
    axes[2].tick_params(axis="y", labelsize=8)
    axes[2].set_xlim(0, top_cat_inv.max() * 1.18)

    plt.tight_layout(pad=2.5)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Gráfica guardada → {output_path}")


# Imprimirbresultados formateados
def imprimir_reporte(df: pd.DataFrame) -> None:
    """Imprime en consola el reporte completo de las 3 preguntas."""

    sep = "━" * 62

    #  Q1 
    print(f"\n{sep}")
    print("  Q1 · Precio promedio por categoría")
    print(sep)
    prom = precio_promedio_por_categoria(df)
    print(f"\n  {'CATEGORÍA':<38} {'PROMEDIO':>10}")
    print(f"  {'-'*38} {'-'*10}")
    for cat, precio in prom.items():
        print(f"  {cat:<38} £{precio:>8.2f}")

    #  Q2 
    print(f"\n{sep}")
    print("  Q2 · Cantidad de libros por nivel de rating")
    print(sep)
    por_rating = libros_por_rating(df)
    print()
    max_cant = por_rating.max()
    for rating, cantidad in por_rating.items():
        barra   = "█" * round(cantidad / max_cant * 35)
        pct     = cantidad / len(df) * 100
        print(f"  {ESTRELLAS[rating]}  {cantidad:>4} libros  ({pct:4.1f}%)  {barra}")

    # Q3 
    print(f"\n{sep}")
    print("  Q3 · Los 10 libros más caros del catálogo")
    print(sep)
    top10 = top_10_mas_caros(df)
    print()
    for i, row in top10.iterrows():
        stars  = "★" * row["rating"] + "☆" * (5 - row["rating"])
        titulo = (row["titulo"][:43] + "…") if len(row["titulo"]) > 45 else row["titulo"]
        print(f"  {i+1:>2}. £{row['precio']:>5.2f}  {stars}  {titulo}")
        print(f"       ↳ Categoría: {row['categoria']}")

    #  Párrafo de análisis 
    mejor_cat   = prom.idxmax()
    peor_cat    = prom.idxmin()
    rating_top  = por_rating.idxmax()
    print(f"\n{sep}")
    print("  Análisis breve")
    print(sep)
    print(f"""
  El catálogo contiene {len(df):,} libros en {df['categoria'].nunique()} categorías.
  La categoría con mayor precio promedio es "{mejor_cat}" (£{prom.max():.2f}),
  mientras que "{peor_cat}" es la más accesible (£{prom.min():.2f}).
  El nivel de rating más frecuente es {rating_top} {ESTRELLAS[rating_top]}
  con {por_rating[rating_top]:,} libros ({por_rating[rating_top]/len(df)*100:.1f}% del catálogo),
  y el libro más caro cuesta £{df['precio'].max():.2f}.
""")
