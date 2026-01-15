import os
import sys
from firecrawl import Firecrawl

# 1. Conexión segura
api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    print("ERROR: No se encontró la API Key.")
    sys.exit(1)

app = Firecrawl(api_key=api_key)

# 2. LISTA DE BÚSQUEDAS (Espectro Total TAGMA)
queries = [
    "subvenciones arquitectura sustentable 2026",
    "international grants for sustainable architecture 2026",
    "funding for environmental education NGOs Latin America",
    "site:innpactia.com fondos",
    "site:nodoka.co arquitectura",
    "site:fundsforngos.org environment",
    "site:grantwatch.com architecture"
]

print(f"Iniciando búsqueda táctica...")

# 3. Procesar y guardar resultados
with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO DE FONDOS TAGMA (2026) ---\n\n")
    
    for q in queries:
        f.write(f"BUSCANDO: {q}\n")
        f.write("-" * (len(q) + 10) + "\n")
        
        try:
            response = app.search(q, limit=5)
            
            # Lógica ultra-robusta para extraer la lista de resultados
            items = []
            if isinstance(response, list):
                items = response
            elif isinstance(response, dict):
                items = response.get('data', response.get('results', []))
            else:
                # Para objetos tipo SearchData, probamos varios atributos comunes
                items = getattr(response, 'data', getattr(response, 'results', []))
            
            if not items:
                f.write("Status: No se encontraron resultados específicos en esta fuente.\n\n")
            else:
                for item in items:
                    # Intentamos leer como diccionario o como objeto
                    titulo = item.get('title') if isinstance(item, dict) else getattr(item, 'title', 'Sin título')
                    link = item.get('url') if isinstance(item, dict) else getattr(item, 'url', 'Sin link')
                    f.write(f"  > {titulo}\n    Link: {link}\n")
                f.write("\n")
                
        except Exception as e:
            f.write(f"Status: Error en la conexión ({str(e)})\n\n")

print("¡Proceso completado! Archivo generado con detalles de cada búsqueda.")
