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
import unicodedata

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

# Tipos aceptados devueltos por Google Places que consideramos supermercados
ACCEPTED_PLACE_TYPES = {"supermarket", "grocery_or_supermarket"}


def _normalize_text(s: str) -> str:
    """Normaliza texto para comparación: minúsculas, sin acentos, solo alfanum."""
    if not s:
        return ""
    # Normalizar y remover acentos
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    # Minusculas
    s = s.lower()
    # Mantener solo caracteres alfanuméricos y espacios
    s = ''.join(ch for ch in s if ch.isalnum() or ch.isspace())
    return s

# TODAS las ciudades y comunas importantes de Chile para búsqueda completa
# Formato: (nombre, lat, lng, radio_km)
CITIES_SEARCH = [
    # ===== REGIÓN DE ARICA Y PARINACOTA (XV) =====
    ("Arica", -18.4783, -70.3126, 20),
    ("Putre", -18.1950, -69.5583, 15),
    
    # ===== REGIÓN DE TARAPACÁ (I) =====
    ("Iquique", -20.2141, -70.1522, 25),
    ("Alto Hospicio", -20.2667, -70.1000, 15),
    ("Pozo Almonte", -20.2594, -69.7881, 15),
    
    # ===== REGIÓN DE ANTOFAGASTA (II) =====
    ("Antofagasta", -23.6509, -70.3975, 30),
    ("Calama", -22.4584, -68.9277, 20),
    ("Tocopilla", -22.0922, -70.1989, 15),
    ("Mejillones", -23.0997, -70.4489, 15),
    ("Taltal", -25.4050, -70.4850, 15),
    ("San Pedro de Atacama", -22.9083, -68.2000, 15),
    
    # ===== REGIÓN DE ATACAMA (III) =====
    ("Copiapó", -27.3669, -70.3314, 20),
    ("Vallenar", -28.5708, -70.7581, 15),
    ("Caldera", -27.0656, -70.8211, 15),
    ("Chañaral", -26.3478, -70.6219, 15),
    
    # ===== REGIÓN DE COQUIMBO (IV) =====
    ("La Serena", -29.9027, -71.2519, 30),
    ("Coquimbo", -29.9533, -71.3394, 20),
    ("Ovalle", -30.5978, -71.1992, 20),
    ("Illapel", -31.6333, -71.1667, 15),
    ("Vicuña", -30.0328, -70.7119, 15),
    ("Andacollo", -30.2311, -71.0833, 10),
    ("Monte Patria", -30.6944, -70.9550, 15),
    
    # ===== REGIÓN DE VALPARAÍSO (V) =====
    ("Valparaíso", -33.0472, -71.6127, 30),
    ("Viña del Mar", -33.0245, -71.5518, 25),
    ("Quilpué", -33.0472, -71.4425, 20),
    ("Villa Alemana", -33.0453, -71.3733, 15),
    ("Concón", -32.9250, -71.5189, 15),
    ("Quillota", -32.8833, -71.2500, 20),
    ("La Calera", -32.7833, -71.2000, 15),
    ("San Antonio", -33.5956, -71.6128, 20),
    ("Los Andes", -32.8333, -70.6000, 20),
    ("San Felipe", -32.7500, -70.7167, 20),
    ("Casablanca", -33.3167, -71.4167, 15),
    ("Limache", -33.0167, -71.2667, 15),
    ("Olmué", -33.0000, -71.2000, 10),
    
    # ===== REGIÓN METROPOLITANA (XIII) =====
    ("Santiago Centro", -33.4489, -70.6693, 15),
    ("Maipú", -33.5110, -70.7580, 20),
    ("Puente Alto", -33.6167, -70.5833, 20),
    ("La Florida", -33.5219, -70.5989, 20),
    ("Las Condes", -33.4167, -70.5833, 20),
    ("Providencia", -33.4333, -70.6167, 15),
    ("Ñuñoa", -33.4500, -70.6000, 15),
    ("San Bernardo", -33.5833, -70.7000, 20),
    ("Peñalolén", -33.4833, -70.5167, 15),
    ("La Pintana", -33.5833, -70.6333, 15),
    ("El Bosque", -33.5667, -70.6833, 15),
    ("La Cisterna", -33.5333, -70.6667, 15),
    ("San Miguel", -33.4833, -70.6500, 15),
    ("La Reina", -33.4500, -70.5333, 15),
    ("Macul", -33.4833, -70.6000, 15),
    ("Estación Central", -33.4667, -70.7000, 15),
    ("Recoleta", -33.4000, -70.6333, 15),
    ("Independencia", -33.4167, -70.6667, 15),
    ("Conchalí", -33.3833, -70.6667, 15),
    ("Huechuraba", -33.3667, -70.6333, 15),
    ("Quilicura", -33.3500, -70.7333, 20),
    ("Renca", -33.4000, -70.7333, 15),
    ("Cerro Navia", -33.4167, -70.7333, 15),
    ("Pudahuel", -33.4333, -70.7500, 20),
    ("Lo Prado", -33.4333, -70.7167, 15),
    ("Quinta Normal", -33.4333, -70.7000, 15),
    ("Vitacura", -33.3833, -70.5667, 15),
    ("Lo Barnechea", -33.3500, -70.5167, 20),
    ("San Joaquín", -33.4833, -70.6333, 15),
    ("Pedro Aguirre Cerda", -33.4833, -70.6667, 15),
    ("Cerrillos", -33.5000, -70.7167, 15),
    ("Melipilla", -33.6833, -71.2167, 20),
    ("Talagante", -33.6667, -70.9333, 15),
    ("Peñaflor", -33.6167, -70.8833, 15),
    ("Buin", -33.7333, -70.7333, 15),
    ("Paine", -33.8167, -70.7500, 15),
    ("Colina", -33.2000, -70.6667, 20),
    ("Lampa", -33.2833, -70.8833, 15),
    ("Til Til", -33.0833, -70.9333, 15),
    
    # ===== REGIÓN DE O'HIGGINS (VI) =====
    ("Rancagua", -34.1705, -70.7407, 25),
    ("San Fernando", -34.5833, -70.9833, 20),
    ("Rengo", -34.4000, -70.8667, 15),
    ("Machalí", -34.1833, -70.6500, 15),
    ("Graneros", -34.0667, -70.7333, 10),
    ("Santa Cruz", -34.6333, -71.3667, 15),
    ("Chimbarongo", -34.7167, -71.0333, 15),
    ("Pichilemu", -34.3856, -72.0039, 15),
    ("San Vicente", -34.4333, -71.0833, 15),
    
    # ===== REGIÓN DEL MAULE (VII) =====
    ("Talca", -35.4264, -71.6554, 30),
    ("Curicó", -34.9833, -71.2394, 20),
    ("Linares", -35.8500, -71.5833, 20),
    ("Constitución", -35.3333, -72.4167, 15),
    ("Cauquenes", -35.9667, -72.3167, 15),
    ("Parral", -36.1333, -71.8167, 15),
    ("Molina", -35.1167, -71.2833, 15),
    ("San Javier", -35.5969, -71.7289, 15),
    
    # ===== REGIÓN DE ÑUBLE (XVI) =====
    ("Chillán", -36.6065, -72.1035, 25),
    ("Chillán Viejo", -36.6289, -72.1286, 15),
    ("San Carlos", -36.4244, -71.9578, 20),
    ("Bulnes", -36.7428, -72.2983, 15),
    ("Quirihue", -36.2803, -72.5417, 15),
    ("Yungay", -37.1167, -72.0167, 15),
    
    # ===== REGIÓN DEL BIOBÍO (VIII) =====
    ("Concepción", -36.8270, -73.0498, 30),
    ("Talcahuano", -36.7167, -73.1167, 20),
    ("Los Ángeles", -37.4697, -72.3544, 25),
    ("Coronel", -37.0167, -73.1500, 15),
    ("San Pedro de la Paz", -36.8400, -73.1106, 15),
    ("Chiguayante", -36.9167, -73.0333, 15),
    ("Tomé", -36.6167, -72.9500, 15),
    ("Penco", -36.7333, -72.9833, 15),
    ("Lota", -37.0889, -73.1572, 15),
    ("Hualpén", -36.7833, -73.1000, 15),
    ("Lebu", -37.6044, -73.6508, 15),
    ("Cañete", -37.8000, -73.4000, 15),
    ("Arauco", -37.2464, -73.3172, 15),
    ("Curanilahue", -37.4786, -73.3444, 15),
    ("Nacimiento", -37.5000, -72.6667, 15),
    ("Laja", -37.2833, -72.7167, 15),
    ("Cabrero", -37.0333, -72.4000, 15),
    ("Mulchén", -37.7167, -72.2333, 15),
    
    # ===== REGIÓN DE LA ARAUCANÍA (IX) =====
    ("Temuco", -38.7359, -72.5904, 30),
    ("Padre Las Casas", -38.7667, -72.6000, 15),
    ("Villarrica", -39.2833, -72.2333, 20),
    ("Pucón", -39.2825, -71.9556, 20),
    ("Angol", -37.7956, -72.7114, 20),
    ("Victoria", -38.2333, -72.3333, 15),
    ("Lautaro", -38.5333, -72.4333, 15),
    ("Nueva Imperial", -38.7450, -72.9500, 15),
    ("Carahue", -38.7167, -73.1667, 15),
    ("Pitrufquén", -38.9833, -72.6333, 15),
    ("Gorbea", -39.0950, -72.6775, 15),
    ("Loncoche", -39.3667, -72.6333, 15),
    ("Traiguén", -38.2500, -72.6667, 15),
    ("Collipulli", -37.9544, -72.4350, 15),
    ("Curacautín", -38.4333, -71.8833, 15),
    
    # ===== REGIÓN DE LOS RÍOS (XIV) =====
    ("Valdivia", -39.8142, -73.2459, 25),
    ("La Unión", -40.2936, -73.0825, 15),
    ("Río Bueno", -40.3333, -72.9667, 15),
    ("Panguipulli", -39.6333, -72.3333, 15),
    
    # ===== REGIÓN DE LOS LAGOS (X) =====
    ("Puerto Montt", -41.4717, -72.9425, 30),
    ("Osorno", -40.5745, -73.1349, 25),
    ("Puerto Varas", -41.3167, -72.9833, 20),
    ("Castro", -42.4833, -73.7667, 20),
    ("Ancud", -41.8694, -73.8239, 15),
    ("Calbuco", -41.7667, -73.1333, 15),
    ("Chonchi", -42.6167, -73.7667, 15),
    ("Quellón", -43.1167, -73.6167, 15),
    ("Frutillar", -41.1236, -73.0553, 15),
    ("Llanquihue", -41.2500, -73.0000, 15),
    ("Los Muermos", -41.4000, -73.4667, 15),
    ("Río Negro", -40.7833, -73.2167, 15),
    ("Purranque", -40.9167, -73.1667, 15),
    
    # ===== REGIÓN DE AYSÉN (XI) =====
    ("Coyhaique", -45.5752, -72.0662, 25),
    ("Puerto Aysén", -45.4033, -72.6928, 15),
    ("Chile Chico", -46.5422, -71.7219, 15),
    ("Puerto Cisnes", -44.7444, -72.6975, 10),
    
    # ===== REGIÓN DE MAGALLANES (XII) =====
    ("Punta Arenas", -53.1638, -70.9171, 25),
    ("Puerto Natales", -51.7256, -72.5086, 20),
    ("Porvenir", -53.2969, -70.3669, 15),
    ("Puerto Williams", -54.9333, -67.6167, 10),
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
            filtered_count = 0
            
            for i, (city, lat, lng, radius_km) in enumerate(CITIES_SEARCH, 1):
                progress_pct = (i / total_cities) * 100
                print(f"  [{i}/{total_cities}] ({progress_pct:.1f}%) {city}... ", end='', flush=True)
                
                radius_m = radius_km * 1000
                results = self.search_nearby(chain, lat, lng, radius_m)
                
                print(f"{len(results)} encontrados | Total acumulado: {len(chain_results)}")
                
                for place in results:
                    # Filtrar por types devueltos por Google Places
                    place_types = place.get('types', []) or []
                    if not any(t in ACCEPTED_PLACE_TYPES for t in place_types):
                        filtered_count += 1
                        continue

                    # Filtrar estrictamente por nombre de cadena: el nombre del place debe contener
                    # el token de la cadena buscada (normalizado). Esto asegura que solo guardemos
                    # sucursales que pertenezcan explícitamente a las 13 cadenas definidas.
                    place_name = place.get('name', '')
                    norm_name = _normalize_text(place_name)
                    norm_chain = _normalize_text(chain)
                    if norm_chain not in norm_name:
                        # No corresponde a la cadena buscada -> omitir
                        filtered_count += 1
                        continue

                    place_info = self.extract_place_info(place)

                    # Evitar duplicados usando place_id
                    place_id = place_info['place_id']
                    if place_id not in [p['place_id'] for p in chain_results]:
                        chain_results.append(place_info)
                
                # Mostrar resumen cada 25 ciudades
                if i % 25 == 0:
                    print(f"  >>> PROGRESO: {i}/{total_cities} ciudades completadas - {len(chain_results)} supermercados únicos encontrados")
                
                # Respetar rate limits
                time.sleep(0.5)
            
            # Guardar resultados de esta cadena
            if chain_results:
                self.all_places[chain] = chain_results
                print(f"\n  TOTAL {chain}: {len(chain_results)} supermercados únicos")
                if filtered_count:
                    print(f"  FILTRADOS POR TIPO: {filtered_count} resultados omitidos por no ser 'supermarket'/'grocery_or_supermarket'")
        
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
