"""
Script de prueba rapida para Google Places API
Verifica que tu API key funciona correctamente
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Cargar .env
load_dotenv()

GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', '')

print("="*70)
print("PRUEBA RAPIDA DE GOOGLE PLACES API")
print("="*70)

if not GOOGLE_PLACES_API_KEY:
    print("\nERROR: No se encontro GOOGLE_PLACES_API_KEY")
    print("\nPasos para configurar:")
    print("1. Copia .env.example a .env")
    print("2. Edita .env y pega tu API key")
    print("3. Guarda el archivo")
    print("\nVer GUIA_GOOGLE_PLACES_API.txt para instrucciones completas")
    exit(1)

print(f"\nOK API Key encontrada: {GOOGLE_PLACES_API_KEY[:10]}...{GOOGLE_PLACES_API_KEY[-5:]}")

# Hacer una busqueda de prueba simple
print("\nProbando busqueda en Santiago...")
print("Buscando: Jumbo cerca de Plaza de Armas, Santiago")

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    'key': GOOGLE_PLACES_API_KEY,
    'location': '-33.4489,-70.6693',  # Plaza de Armas, Santiago
    'radius': 5000,  # 5 km
    'keyword': 'Jumbo',
    'type': 'supermarket',
    'language': 'es'
}

try:
    print("\nRealizando peticion a Google Places API...")
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    print(f"Status code: {response.status_code}")
    print(f"API response status: {data.get('status')}")
    
    if data['status'] == 'OK':
        results = data.get('results', [])
        print(f"\nEXITO! Se encontraron {len(results)} supermercados")
        
        if results:
            print("\nPrimeros 3 resultados:")
            for i, place in enumerate(results[:3], 1):
                print(f"\n{i}. {place['name']}")
                print(f"   Direccion: {place.get('vicinity', 'N/A')}")
                print(f"   Rating: {place.get('rating', 'N/A')}")
                location = place['geometry']['location']
                print(f"   Coordenadas: {location['lat']}, {location['lng']}")
        
        print("\n" + "="*70)
        print("OK TU API KEY FUNCIONA CORRECTAMENTE")
        print("="*70)
        print("\nAhora puedes ejecutar:")
        print("  python extract_google_places.py")
        print("\nEsto extraera TODOS los supermercados de Chile")
        
    elif data['status'] == 'REQUEST_DENIED':
        print("\nERROR: REQUEST_DENIED")
        print("\nPosibles causas:")
        print("1. La API key no es valida")
        print("2. Places API no esta habilitada en tu proyecto")
        print("3. Restricciones de API key muy estrictas")
        print("\nSolucion:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Selecciona tu proyecto")
        print("3. Ve a APIs y servicios > Biblioteca")
        print("4. Busca 'Places API' y HABILITAR")
        
    elif data['status'] == 'OVER_QUERY_LIMIT':
        print("\nERROR: OVER_QUERY_LIMIT")
        print("\nPosibles causas:")
        print("1. Excediste el limite de requests gratuitos")
        print("2. No tienes facturacion habilitada")
        print("\nSolucion:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Ve a Facturacion")
        print("3. Habilita una cuenta de facturacion")
        print("   (Recibes $200 USD gratis mensuales)")
        
    elif data['status'] == 'ZERO_RESULTS':
        print("\nWARNING: No se encontraron resultados")
        print("Esto es raro para Santiago. Verifica los parametros.")
        
    else:
        print(f"\nStatus inesperado: {data['status']}")
        print(f"Mensaje: {data.get('error_message', 'N/A')}")
    
except requests.exceptions.RequestException as e:
    print(f"\nERROR DE CONEXION: {e}")
    print("\nVerifica tu conexion a internet")
    
except Exception as e:
    print(f"\nERROR INESPERADO: {e}")

print("\n" + "="*70)
