import os
from firecrawl import FirecrawlApp

# 1. Conexión con la API usando el Secret que creaste
api_key = os.getenv('FIRECRAWL_API_KEY')
app = FirecrawlApp(api_key=api_key)

# 2. Definimos la búsqueda (Query)
# Buscamos fondos internacionales para 2026
query = "international grants for sustainable architecture and eco-education 2026"

print(f"Iniciando búsqueda para: {query}...")

# 3. Usamos la función SEARCH (busca y extrae contenido de los mejores resultados)
results = app.search(query, params={'limit': 5})

# 4. Guardamos los resultados en un archivo de texto
with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- NUEVAS OPORTUNIDADES ENCONTRADAS ---\n\n")
    for item in results.get('data', []):
        f.write(f"TÍTULO: {item.get('title')}\n")
        f.write(f"LINK: {item.get('url')}\n")
        f.write(f"RESUMEN: {item.get('description')}\n")
        f.write("-" * 30 + "\n")

print("Proceso completado. Resultados guardados en resultados_fondos.txt")
