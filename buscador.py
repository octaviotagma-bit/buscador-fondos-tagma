import os
import sys
import time
from firecrawl import Firecrawl

# 1. Conexión con la API
app = Firecrawl(api_key=os.getenv('FIRECRAWL_API_KEY'))

# 2. Tus fuentes estratégicas (puedes sumar más de tu lista)
fuentes = [
    "https://www.fundsforngos.org/category/environment/",
    "https://www.innpactia.com/convocatorias",
    "https://nodoka.co/oportunidades"
]

print(f"Iniciando extracción de {len(fuentes)} sitios...")

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO TAGMA (MODO EXTRACCIÓN 2026) ---\n\n")
    
    for url in fuentes:
        print(f"Leyendo: {url}")
        try:
            # CAMBIO CLAVE: Eliminamos 'params=' y pasamos 'formats' directamente
            response = app.scrape(url, formats=['markdown'])
            
            # Extraemos el contenido del objeto de respuesta
            # En 2026, 'response' suele ser un diccionario o un objeto con atributo 'markdown'
            contenido = ""
            if isinstance(response, dict):
                contenido = response.get('markdown', '')
            else:
                contenido = getattr(response, 'markdown', '')

            if contenido:
                f.write(f"=== FUENTE: {url} ===\n")
                # Guardamos los primeros 1200 caracteres para ver los títulos y links
                f.write(contenido[:1200] + "\n\n")
                f.write("-" * 40 + "\n\n")
                print(f"Éxito: Datos obtenidos de {url}")
            else:
                f.write(f"Aviso: No se encontró texto legible en {url}\n\n")
            
            # Pausa necesaria para no saturar tu plan gratuito (Rate Limit)
            time.sleep(20) 

        except Exception as e:
            f.write(f"Error en {url}: {str(e)}\n\n")
            print(f"Fallo en {url}: {e}")

print("¡Proceso terminado! El archivo resultados_fondos.txt ya tiene los datos.")
