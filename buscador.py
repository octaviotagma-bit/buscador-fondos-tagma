import os
import sys
from firecrawl import FirecrawlApp

# 1. Conexión con la API usando el Secret
api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    print("Error: No se encontró la API Key en los Secrets.")
    sys.exit(1)

app = FirecrawlApp(api_key=api_key)

# 2. Búsqueda de fondos para TAGMA
query = "international grants for sustainable architecture and eco-education 2026"
print(f"Iniciando búsqueda para: {query}...")

# 3. Función de búsqueda (sin 'params' y con el formato nuevo)
results = app.search(query, limit=5)

# 4. Guardar los resultados (usando el formato de 'objeto' nuevo)
with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- NUEVAS OPORTUNIDADES ENCONTRADAS (TAGMA 2026) ---\n\n")
    
    # Aquí está el cambio clave: 'results.data' en lugar de 'results.get'
    for item in results.data:
        f.write(f"TÍTULO: {item.title}\n")
        f.write(f"LINK: {item.url}\n")
        f.write(f"RESUMEN: {item.description}\n")
        f.write("-" * 30 + "\n")

print("¡Proceso completado! Los resultados están en resultados_fondos.txt")
