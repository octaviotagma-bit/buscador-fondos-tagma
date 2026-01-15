import os
import sys
import time # Nuevo: Para manejar el tiempo
from firecrawl import Firecrawl

api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    sys.exit(1)

app = Firecrawl(api_key=api_key)

# Usamos las frases que SÍ te funcionaron en el Playground
queries = [
    "international grants funding sustainable education architecture community schools NGOs Latin America 2025-2026",
    "Tinker Foundation institutional grants 2026",
    "UNESCO GEM Regional Edition leadership Latin America",
    "Barakat Trust Grants Programme 2026",
    "site:innpactia.com convocatorias ambientales"
]

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO TAGMA (VERSIÓN MEJORADA 2026) ---\n\n")
    
    for q in queries:
        f.write(f"BUSCANDO: {q}\n")
        try:
            # Buscamos y luego ESPERAMOS para respetar el límite gratuito
            response = app.search(q, limit=5)
            
            # Extraemos los datos según el formato nuevo visto en Playground
            items = []
            if isinstance(response, dict):
                items = response.get('data', [])
            else:
                items = getattr(response, 'data', [])

            if not items:
                f.write("Status: Sin resultados nuevos para este término.\n")
            else:
                for item in items:
                    titulo = item.get('title', 'Sin título')
                    link = item.get('url', 'Sin link')
                    f.write(f"  [+] {titulo}\n      Link: {link}\n")
            
            f.write("\n")
            print(f"Búsqueda exitosa: {q}. Esperando 15 segundos para la siguiente...")
            time.sleep(15) # Esto evita el error de "Rate Limit"

        except Exception as e:
            f.write(f"Status: Pausado o Error ({str(e)})\n\n")
            time.sleep(20) # Si falla, esperamos un poco más
