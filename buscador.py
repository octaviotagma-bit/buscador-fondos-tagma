import os
import sys
import time
from firecrawl import Firecrawl

# 1. Conexión
app = Firecrawl(api_key=os.getenv('FIRECRAWL_API_KEY'))

# 2. Fuentes directas de TAGMA
fuentes = [
    "https://www.fundsforngos.org/category/environment/",
    "https://www.innpactia.com/convocatorias",
    "https://nodoka.co/oportunidades"
]

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO TAGMA (2026) ---\n\n")
    
    for url in fuentes:
        print(f"Leyendo: {url}...")
        try:
            # CAMBIO CLAVE: usamos .scrape() en lugar de .scrape_url()
            # Pedimos el formato markdown para que sea fácil de leer
            response = app.scrape(url, params={'formats': ['markdown']})
            
            # Extraemos el contenido (el nuevo formato es un objeto Document)
            contenido = response.get('markdown', '') if isinstance(response, dict) else getattr(response, 'markdown', '')

            if contenido:
                f.write(f"=== FUENTE: {url} ===\n")
                # Guardamos los primeros 1000 caracteres para un reporte ágil
                f.write(contenido[:1000] + "\n\n")
            else:
                f.write(f"Sin contenido disponible en {url}\n\n")
            
            # Pausa de seguridad para el plan gratuito
            time.sleep(20) 

        except Exception as e:
            f.write(f"Error en {url}: {str(e)}\n\n")
