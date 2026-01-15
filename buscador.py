import os
import sys
import time
from firecrawl import Firecrawl

app = Firecrawl(api_key=os.getenv('FIRECRAWL_API_KEY'))

# Definimos los dominios "madre" para que el robot explore
dominios = [
    {"url": "https://www.fundsforngos.org", "keyword": "environment"},
    {"url": "https://www.innpactia.com", "keyword": "convocatorias"},
    {"url": "https://nodoka.co", "keyword": "oportunidades"}
]

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE INTELIGENTE TAGMA (MAPEO 2026) ---\n\n")
    
    for sitio in dominios:
        print(f"Explorando {sitio['url']}...")
        try:
            # 1. MAPEAMOS para encontrar el link correcto que no sea 404
            map_result = app.map(sitio['url'], search=sitio['keyword'])
            
            # Buscamos el primer link válido que nos devuelva el mapa
            links = map_result.get('links', []) if isinstance(map_result, dict) else getattr(map_result, 'links', [])
            
            if links:
                url_real = links[0] # Tomamos la mejor coincidencia
                f.write(f"LINK ENCONTRADO: {url_real}\n")
                
                # 2. EXTRAEMOS de ese link real
                response = app.scrape(url_real, formats=['markdown'])
                contenido = response.get('markdown', '') if isinstance(response, dict) else getattr(response, 'markdown', '')
                
                if "Manage Consent" in contenido or not contenido:
                    f.write("Aviso: El sitio bloqueó la lectura directa por cookies.\n\n")
                else:
                    f.write(contenido[:1500] + "\n\n")
                
                f.write("-" * 40 + "\n\n")
            else:
                f.write(f"No se encontró una página de '{sitio['keyword']}' activa en {sitio['url']}\n\n")
            
            time.sleep(20)

        except Exception as e:
            f.write(f"Error explorando {sitio['url']}: {str(e)}\n\n")

print("¡Mapeo y extracción finalizados!")
