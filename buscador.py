import os
import sys
from firecrawl import Firecrawl

# 1. Conexión segura con la API
api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    print("ERROR: No se encontró la API Key en los Secrets de GitHub.")
    sys.exit(1)

app = Firecrawl(api_key=api_key)

# 2. LISTA DE BÚSQUEDAS DIVERSIFICADA (Español, Inglés y Sitios de la Imagen)
queries = [
    # --- Búsquedas en ESPAÑOL ---
    "subvenciones arquitectura sustentable 2026",
    "financiamiento educación ambiental latinoamérica",
    "fondos para proyectos de bioconstrucción y escuelas",
    "becas para regeneración ecológica y desarrollo comunitario",

    # --- Búsquedas en INGLÉS ---
    "global grants for green building and sustainable design 2026",
    "environmental education funding for NGOs Latin America",
    "sustainable architecture development grants",
    "climate action funding for educational infrastructure",

    # --- Sitios Específicos de la imagen de TAGMA ---
    "site:innpactia.com arquitectura",
    "site:nodoka.co educación ambiental",
    "site:gestionandote.org fondos",
    "site:justicefunds.co grants",
    "site:fundsforngos.org sustainable building",
    "site:grantwatch.com environmental education",
    "site:raci.org.ar fondos ambientales",
    "site:biofin.org funding",
    "site:restor.eco grants"
]

print(f"Iniciando búsqueda estratégica ({len(queries)} consultas)...")

# 3. Procesar y guardar resultados
with open("resultados_fondos.txt", "w", encoding="utf-8") as f:
    f.write("--- REPORTE ESTRATÉGICO DE FONDOS TAGMA (2026) ---\n\n")
    
    for q in queries:
        print(f"Buscando: '{q}'...")
        try:
            response = app.search(q, limit=3) # Buscamos los 3 mejores de cada frase
            
            # Detectamos el formato de respuesta de forma segura
            items = response.get('data', []) if isinstance(response, dict) else getattr(response, 'data', [])
            
            if items:
                f.write(f"=== RESULTADOS PARA: {q} ===\n")
                for item in items:
                    titulo = item.get('title', 'Sin título')
                    link = item.get('url', 'Sin link')
                    f.write(f"- {titulo}\n  Link: {link}\n")
                f.write("\n")
                
        except Exception as e:
            print(f"Error en la búsqueda '{q}': {e}")

print("¡Proceso completado con éxito!")
