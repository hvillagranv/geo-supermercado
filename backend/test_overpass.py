"""
Script de prueba para Overpass API
"""

import requests
import json

# Query simple para probar
query = """
[out:json];
node["shop"="supermarket"]["name"~"Jumbo",i](-33.6,-70.8,-33.3,-70.5);
out body;
"""

url = "https://overpass-api.de/api/interpreter"

print("Probando query en Overpass API...")
print(f"URL: {url}")
print(f"Query: {query}")

try:
    response = requests.post(url, data=query.encode('utf-8'), timeout=60)
    print(f"\nStatus code: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResultados: {len(data.get('elements', []))} elementos encontrados")
        
        # Mostrar primeros 3 resultados
        for i, elem in enumerate(data.get('elements', [])[:3]):
            print(f"\n--- Elemento {i+1} ---")
            print(json.dumps(elem, indent=2, ensure_ascii=False))
    else:
        print(f"\nError: {response.text}")
        
except Exception as e:
    print(f"\nError: {e}")
