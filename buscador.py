import os
import sys
import time
from firecrawl import Firecrawl

api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    sys.exit(1)

app = Firecrawl(api_key=api_key)

# Frases optimizadas: menos es más para el buscador de la API
queries = [
    "Tinker Foundation grants 2026",
    "UNESCO GEM leadership Latin America",
    "Barakat Trust grants 2026",
    "sustainable architecture grants Latin America",
    "bioconstrucción financiamiento 2026"
]

with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO TAGMA (DIAGNÓSTICO 2026) ---\n\n")
    
    for q in queries:
        print(f"Iniciando búsqueda: {q}")
        f.write(f"BUSCANDO: {q}\n")
        try:
            # Buscamos con un límite de 5
            response = app.search(q, limit=5)
            
            # IMPRESIÓN DE DEPURACIÓN: Esto saldrá en tu consola de GitHub
            print(f"Respuesta de Firecrawl para '{q}': {response}")

            # Intentamos extraer datos de 3 formas distintas para no fallar
            items = []
            if isinstance(response, dict):
                items = response.get('data') or response.get('results') or response.get('items', [])
            else:
                items = getattr(response, 'data', getattr(response, 'results', []))

            if not items:
                f.write("Status: El buscador no devolvió resultados para esta frase exacta.\n")
                print(f"Aviso: No se encontraron datos para {q}")
            else:
                for item in items:
                    titulo = item.get('title') or item.get('name', 'Sin título')
                    link = item.get('url') or item.get('link', 'Sin link')
                    f.write(f"  [+] {titulo}\n      Link: {link}\n")
                print(f"Éxito: Se encontraron {len(items)} resultados.")
            
            f.write("\n" + "="*30 + "\n\n")
            time.sleep(20) # Aumentamos a 20s para máxima seguridad con el plan gratis

        except Exception as e:
            f.write(f"Status: Error técnico ({str(e)})\n\n")
            print(f"Error en {q}: {e}")
            time.sleep(30)
