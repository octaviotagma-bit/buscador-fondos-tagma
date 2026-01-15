import os
import sys
import time
from firecrawl import Firecrawl

app = Firecrawl(api_key=os.getenv('FIRECRAWL_API_KEY'))

# Dominios madre para TAGMA
dominios = [
    {"url": "https://www.fundsforngos.org", "keyword": "environment"},
    {"url": "https://web.innpactia.com", "keyword": "oportunidades"},
    {"url": "https://nodoka.co", "keyword": "oportunidades"}
]

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO TAGMA (2026) ---\n\n")
    
    for sitio in dominios:
        print(f"Mapeando {sitio['url']}...")
        try:
            # 1. MAPEAMOS para encontrar el link vivo
            map_result = app.map(sitio['url'], search=sitio['keyword'])
            
            # Obtenemos la lista de links (objetos LinkResult)
            links = map_result.get('links', []) if isinstance(map_result, dict) else getattr(map_result, 'links', [])
            
            if links:
                # CORRECCIÓN: Extraemos el atributo .url del objeto LinkResult
                primer_resultado = links[0]
                url_real = primer_resultado.url if hasattr(primer_resultado, 'url') else primer_resultado.get('url')
                
                f.write(f"=== FUENTE: {sitio['url']} ===\n")
                f.write(f"Link detectado: {url_real}\n\n")
                
                # 2. EXTRAEMOS de la URL real
                print(f"Extrayendo de {url_real}...")
                response = app.scrape(url_real, formats=['markdown'])
                
                contenido = response.get('markdown', '') if isinstance(response, dict) else getattr(response, 'markdown', '')
                
                if contenido:
                    # Guardamos los primeros 1500 caracteres
                    f.write(contenido[:1500] + "\n\n")
                else:
                    f.write("Aviso: No se pudo leer el contenido detallado.\n\n")
                
                f.write("-" * 40 + "\n\n")
            else:
                f.write(f"No se encontraron secciones de '{sitio['keyword']}' en {sitio['url']}\n\n")
            
            time.sleep(20) # Seguridad para plan gratuito

        except Exception as e:
            f.write(f"Error en {sitio['url']}: {str(e)}\n\n")

print("¡Proceso finalizado con éxito!")
