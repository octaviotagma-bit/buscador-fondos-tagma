import os
import sys
from firecrawl import Firecrawl  # Usamos la clase moderna de 2026

# 1. Conexión segura con la API
api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    print("ERROR: No se encontró la API Key en los Secrets de GitHub.")
    sys.exit(1)

app = Firecrawl(api_key=api_key)

# 2. Búsqueda de fondos para TAGMA
query = "international grants for sustainable architecture and eco-education 2026"
print(f"Buscando: {query}...")

# 3. Ejecutar búsqueda
# En la versión actual, search devuelve directamente lo que necesitamos
response = app.search(query, limit=5)

# 4. Procesar y guardar resultados de forma segura
with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- LISTA DE FONDOS ENCONTRADOS (TAGMA) ---\n\n")
    
    # Esta parte detecta si los datos vienen en una lista o en un objeto
    items = response.get('data', []) if isinstance(response, dict) else getattr(response, 'data', [])
    
    if not items:
        f.write("No se encontraron resultados en esta búsqueda.\n")
    else:
        for item in items:
            # Usamos .get por si algún campo viene vacío
            titulo = item.get('title', 'Sin título')
            link = item.get('url', 'Sin link')
            descripcion = item.get('description', 'Sin descripción')
            
            f.write(f"TÍTULO: {titulo}\n")
            f.write(f"LINK: {link}\n")
            f.write(f"RESUMEN: {descripcion}\n")
            f.write("-" * 30 + "\n")

print("¡Éxito! El archivo resultados_fondos.txt ha sido generado.")
