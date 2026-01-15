import os
import sys
import time
from firecrawl import Firecrawl

app = Firecrawl(api_key=os.getenv('FIRECRAWL_API_KEY'))

# LISTA DE OBJETIVOS (Tus fuentes de la imagen)
fuentes = [
    "https://www.fundsforngos.org/category/environment/",
    "https://www.innpactia.com/convocatorias",
    "https://nodoka.co/oportunidades",
    "https://www.grantwatch.com/cat/13/environment-grants.html",
    "https://www.raci.org.ar/novedades-de-cooperacion-internacional"
]

print(f"Iniciando extracción de {len(fuentes)} fuentes expertas...")

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE DE EXTRACCIÓN DIRECTA TAGMA (2026) ---\n\n")
    
    for url in fuentes:
        f.write(f"PROCESANDO FUENTE: {url}\n")
        f.write("=" * 40 + "\n")
        
        try:
            # Usamos Scrape para leer la web directamente (esto es lo que funcionó en Playground)
            # Pedimos el formato 'markdown' que es el más legible
            response = app.scrape_url(url, params={'formats': ['markdown']})
            
            # Extraemos el texto
            contenido = response.get('markdown', '')

            if contenido:
                # Tomamos los primeros 1500 caracteres (lo más relevante del inicio)
                f.write(contenido[:1500] + "\n\n")
                print(f"Éxito en {url}")
            else:
                f.write("No se pudo extraer texto de esta fuente hoy.\n\n")

            # MUY IMPORTANTE: Esperamos 15 segundos para no agotar tu plan gratuito
            time.sleep(15) 

        except Exception as e:
            f.write(f"Error técnico en {url}: {str(e)}\n\n")
            time.sleep(20)

print("¡Extracción completa! Revisa el archivo de resultados.")
