"""
Script para extraer TODOS los supermercados de Chile usando Google Places API

IMPORTANTE: Necesitas una API key de Google Cloud Platform
1. Ve a: https://console.cloud.google.com/
2. Crea un proyecto o selecciona uno existente
3. Habilita "Places API"
4. Ve a "Credenciales" y crea una API key
5. Guarda la API key en un archivo .env o usala directamente

COSTOS:
- Gratis: 200 USD mensuales de credito (suficiente para ~40,000 busquedas)
- Nearby Search: $32 por 1000 requests
- Place Details: $17 por 1000 requests
- Este script optimiza para minimizar costos
"""

import os
import sys
import json
import time
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Cargar variables de entorno
load_dotenv()

# Configuracion
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', '')
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
GOOGLE_PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Cadenas de supermercados en Chile
SUPERMARKET_CHAINS = [
    # Grupo Walmart Chile
    "Lider",
    "Ekono",
    "SuperBodega aCuenta",
    
    # Grupo Cencosud
    "Jumbo",
    "Santa Isabel",
    
    # Grupo SMU
    "Unimarc",
    "Mayorista 10",
    "Alvi",
    "OK Market",
    
    # Otros
    "Tottus",
    "Montserrat",
    "Las Brisas",
    "Merkat",
]

# Principales ciudades de Chile para búsqueda
# Formato: (nombre, lat, lng, radio_km)
CITIES_SEARCH = [
    # Región Metropolitana
    ("Santiago Centro", -33.4489, -70.6693, 50),
    
    # Región de Valparaíso
    ("Valparaíso", -33.0472, -71.6127, 30),
    ("Viña del Mar", -33.0245, -71.5518, 20),
    
    # Región del Biobío
    ("Concepción", -36.8270, -73.0498, 30),
    ("Talcahuano", -36.7167, -73.1167, 15),
    ("Los Angeles", -37.4697, -72.3544, 20),
    ("Chillán", -36.6065, -72.1035, 20),
    
    # Región de La Araucanía
    ("Temuco", -38.7359, -72.5904, 25),
    
    # Región de Los Lagos
    ("Puerto Montt", -41.4717, -72.9425, 25),
    ("Osorno", -40.5745, -73.1349, 20),
    
    # Región de Antofagasta
    ("Antofagasta", -23.6509, -70.3975, 25),
    ("Calama", -22.4584, -68.9277, 15),
    
    # Región de Coquimbo
    ("La Serena", -29.9027, -71.2519, 25),
    ("Coquimbo", -29.9533, -71.3394, 15),
    
    # Región de Maule
    ("Talca", -35.4264, -71.6554, 25),
    ("Curicó", -34.9833, -71.2394, 15),
    
    # Región de O'Higgins
    ("Rancagua", -34.1705, -70.7407, 25),
    
    # Región de Ñuble
    ("Chillán", -36.6065, -72.1035, 20),
    
    # Región de Tarapacá
    ("Iquique", -20.2141, -70.1522, 20),
    
    # Región de Arica y Parinacota
    ("Arica", -18.4783, -70.3126, 15),
    
    # Región de Magallanes
    ("Punta Arenas", -53.1638, -70.9171, 20),
]


class GooglePlacesExtractor:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key de Google Places es requerida")
        self.api_key = api_key
        self.all_places = {}
        self.request_count = 0
        
    def search_nearby(self, keyword: str, lat: float, lng: float, radius: int = 25000) -> List[Dict]:
        """
        Busca lugares cercanos usando Nearby Search
        """
        params = {
            'key': self.api_key,
            'location': f"{lat},{lng}",
            'radius': radius,  # en metros
            'keyword': keyword,
            'type': 'supermarket',
            'language': 'es'
        }
        
        results = []
        
        try:
            response = requests.get(GOOGLE_PLACES_URL, params=params, timeout=10)
            response.raise_for_status()
            self.request_count += 1
            
            data = response.json()
            
            if data['status'] == 'OK':
                results.extend(data.get('results', []))
                
                # Manejar paginación (hasta 60 resultados por búsqueda)
                while 'next_page_token' in data:
                    time.sleep(2)  # Requerido por Google antes de usar next_page_token
                    
                    next_params = {
                        'key': self.api_key,
                        'pagetoken': data['next_page_token']
                    }
                    
                    response = requests.get(GOOGLE_PLACES_URL, params=next_params, timeout=10)
                    response.raise_for_status()
                    self.request_count += 1
                    
                    data = response.json()
                    if data['status'] == 'OK':
                        results.extend(data.get('results', []))
                    else:
                        break
                        
            elif data['status'] == 'ZERO_RESULTS':
                pass  # No hay resultados, es normal
            elif data['status'] == 'OVER_QUERY_LIMIT':
                print(f"  ERROR: Límite de consultas excedido")
                raise Exception("Límite de API excedido")
            else:
                print(f"  WARNING: Status {data['status']}")
                
        except Exception as e:
            print(f"  ERROR en búsqueda: {e}")
            
        return results
    
    def extract_place_info(self, place: Dict) -> Dict:
        """
        Extrae información relevante de un lugar
        """
        location = place.get('geometry', {}).get('location', {})
        
        return {
            'place_id': place.get('place_id'),
            'name': place.get('name'),
            'address': place.get('vicinity', ''),
            'lat': location.get('lat'),
            'lon': location.get('lng'),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total', 0),
            'types': place.get('types', []),
            'business_status': place.get('business_status'),
        }
    
    def search_all_supermarkets(self):
        """
        Busca todos los supermercados en todas las ciudades
        """
        print("="*70)
        print("EXTRAYENDO SUPERMERCADOS DE CHILE CON GOOGLE PLACES API")
        print("="*70)
        
        total_cities = len(CITIES_SEARCH)
        total_chains = len(SUPERMARKET_CHAINS)
        
        print(f"\nCiudades a buscar: {total_cities}")
        print(f"Cadenas a buscar: {total_chains}")
        print(f"Búsquedas estimadas: {total_cities * total_chains}")
        print()
        
        for chain in SUPERMARKET_CHAINS:
            print(f"\n{'='*70}")
            print(f"Buscando: {chain}")
            print(f"{'='*70}")
            
            chain_results = []
            
            for i, (city, lat, lng, radius_km) in enumerate(CITIES_SEARCH, 1):
                print(f"  [{i}/{total_cities}] {city}... ", end='', flush=True)
                
                radius_m = radius_km * 1000
                results = self.search_nearby(chain, lat, lng, radius_m)
                
                print(f"{len(results)} encontrados")
                
                for place in results:
                    place_info = self.extract_place_info(place)
                    
                    # Evitar duplicados usando place_id
                    place_id = place_info['place_id']
                    if place_id not in [p['place_id'] for p in chain_results]:
                        chain_results.append(place_info)
                
                # Respetar rate limits
                time.sleep(0.5)
            
            # Guardar resultados de esta cadena
            if chain_results:
                self.all_places[chain] = chain_results
                print(f"\n  TOTAL {chain}: {len(chain_results)} supermercados únicos")
        
        return self.all_places
    
    def save_to_json(self, filename: str = "supermarkets_google_places.json"):
        """
        Guarda los resultados en JSON
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_places, f, ensure_ascii=False, indent=2)
        
        print(f"\nOK Datos guardados en {filename}")
    
    def print_statistics(self):
        """
        Imprime estadísticas de la extracción
        """
        print("\n" + "="*70)
        print("ESTADÍSTICAS DE EXTRACCIÓN")
        print("="*70)
        
        total = 0
        for chain, places in self.all_places.items():
            count = len(places)
            total += count
            print(f"{chain:25} {count:5} supermercados")
        
        print("-"*70)
        print(f"{'TOTAL':25} {total:5} supermercados")
        print(f"\nRequests realizados: {self.request_count}")
        print(f"Costo estimado: ${self.request_count * 0.032:.2f} USD")
        print("="*70)


def main():
    # Verificar API key
    if not GOOGLE_PLACES_API_KEY:
        print("="*70)
        print("ERROR: API KEY DE GOOGLE PLACES NO CONFIGURADA")
        print("="*70)
        print("\nPara obtener una API key:")
        print("1. Ve a: https://console.cloud.google.com/")
        print("2. Crea un proyecto o selecciona uno existente")
        print("3. Habilita 'Places API'")
        print("4. Ve a 'Credenciales' y crea una API key")
        print("5. Crea un archivo .env con:")
        print("   GOOGLE_PLACES_API_KEY=tu_api_key_aqui")
        print("\nO ejecuta:")
        print("   set GOOGLE_PLACES_API_KEY=tu_api_key_aqui (Windows)")
        print("   export GOOGLE_PLACES_API_KEY=tu_api_key_aqui (Linux/Mac)")
        print("="*70)
        return
    
    print(f"\nAPI Key configurada: {GOOGLE_PLACES_API_KEY[:10]}...")
    print("\nIniciando extraccion (esto tomara varios minutos)...")
    
    # Crear extractor
    extractor = GooglePlacesExtractor(GOOGLE_PLACES_API_KEY)
    
    # Extraer todos los supermercados
    extractor.search_all_supermarkets()
    
    # Guardar resultados
    extractor.save_to_json()
    
    # Mostrar estadisticas
    extractor.print_statistics()
    
    print("\nProximo paso: ejecutar 'populate_from_google_places.py'")


if __name__ == "__main__":
    main()
