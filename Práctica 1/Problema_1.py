#print("Es par") if int(input("Ingrese un número para saber si es par o impar: ")) % 2 == 0 else print("Es impar")
from bs4 import BeautifulSoup as soup
import requests
url = "https://books.toscrape.com/"
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0"})
print(resp.status_code) # 200 = OK
print(resp.encoding) # utf-8
html = resp.text # contenido HTML como string
# Pasar parametros de consulta (?q=python)
from bs4 import BeautifulSoup
import requests

url = "https://books.toscrape.com/"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

libros = []

for book in soup.select("article.product_pod"):
    titulo = book.select_one("h3 a")["title"]
    precio = book.select_one(".price_color").get_text(strip=True)

    libros.append({
        "titulo": titulo,
        "precio": precio
    })

print(libros[:5])