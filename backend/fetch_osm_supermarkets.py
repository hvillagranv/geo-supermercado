"""
Script para obtener supermercados reales de Chile desde OpenStreetMap
Usando Overpass API
"""

import requests
import json
import time
import sys
from typing import List, Dict

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Configuración de la API de Overpass
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Cadenas de supermercados en Chile
SUPERMARKET_BRANDS = [
    "Lider",
    "Jumbo",
    "Unimarc",
    "Santa Isabel",
    "Tottus",
    "Ekono",
    "Acuenta",
    "SuperBodega aCuenta",
    "Mayorista 10",
    "Alvi",
    "OK Market",
    "Montserrat",
    "Las Brisas"
]


def get_supermarkets_by_brand(brand: str) -> List[Dict]:
    """
    Obtiene supermercados de una marca específica desde OpenStreetMap
    """
    # Query de Overpass API para buscar supermercados por nombre en Chile
    # Usar bounding box de Chile para mejor rendimiento
    overpass_query = f"""
    [out:json][timeout:90];
    (
      node["shop"="supermarket"]["name"~"{brand}",i](-56.0,-76.0,-17.0,-66.0);
      way["shop"="supermarket"]["name"~"{brand}",i](-56.0,-76.0,-17.0,-66.0);
      relation["shop"="supermarket"]["name"~"{brand}",i](-56.0,-76.0,-17.0,-66.0);
    );
    out center tags;
    """
    
    try:
        print(f"Consultando {brand}...")
        response = requests.post(
            OVERPASS_URL,
            data=overpass_query,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        
        supermarkets = []
        for element in data.get('elements', []):
            # Obtener coordenadas
            if element['type'] == 'node':
                lat = element.get('lat')
                lon = element.get('lon')
            elif 'center' in element:
                lat = element['center'].get('lat')
                lon = element['center'].get('lon')
            else:
                continue
            
            tags = element.get('tags', {})
            
            supermarket = {
                'name': tags.get('name', brand),
                'brand': brand,
                'lat': lat,
                'lon': lon,
                'address': tags.get('addr:street', ''),
                'housenumber': tags.get('addr:housenumber', ''),
                'city': tags.get('addr:city', ''),
                'postcode': tags.get('addr:postcode', ''),
                'phone': tags.get('phone', ''),
                'opening_hours': tags.get('opening_hours', ''),
                'website': tags.get('website', ''),
                'osm_id': element.get('id'),
                'osm_type': element.get('type')
            }
            
            # Construir dirección completa
            if supermarket['address'] and supermarket['housenumber']:
                supermarket['full_address'] = f"{supermarket['address']} {supermarket['housenumber']}, {supermarket['city']}"
            elif supermarket['address']:
                supermarket['full_address'] = f"{supermarket['address']}, {supermarket['city']}"
            else:
                supermarket['full_address'] = supermarket['city']
            
            supermarkets.append(supermarket)
        
        print(f"OK {brand}: {len(supermarkets)} supermercados encontrados")
        return supermarkets
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR consultando {brand}: {e}")
        return []
    except Exception as e:
        print(f"ERROR procesando {brand}: {e}")
        return []


def fetch_all_supermarkets() -> Dict[str, List[Dict]]:
    """
    Obtiene todos los supermercados de todas las marcas
    """
    all_supermarkets = {}
    
    for brand in SUPERMARKET_BRANDS:
        supermarkets = get_supermarkets_by_brand(brand)
        if supermarkets:
            all_supermarkets[brand] = supermarkets
        
        # Respetar límites de la API
        time.sleep(2)
    
    return all_supermarkets


def save_to_json(data: Dict, filename: str = "supermarkets_osm.json"):
    """
    Guarda los datos en un archivo JSON
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nOK Datos guardados en {filename}")


def print_statistics(data: Dict):
    """
    Imprime estadísticas de los datos obtenidos
    """
    print("\n" + "="*60)
    print("ESTADÍSTICAS DE SUPERMERCADOS OBTENIDOS")
    print("="*60)
    
    total = 0
    for brand, supermarkets in data.items():
        count = len(supermarkets)
        total += count
        print(f"{brand:20} {count:4} supermercados")
    
    print("-"*60)
    print(f"{'TOTAL':20} {total:4} supermercados")
    print("="*60)
    
    # Estadísticas por ciudad
    cities = {}
    for brand, supermarkets in data.items():
        for s in supermarkets:
            city = s.get('city', 'Sin ciudad')
            if city:
                cities[city] = cities.get(city, 0) + 1
    
    print("\nTOP 10 CIUDADES CON MÁS SUPERMERCADOS:")
    print("-"*60)
    sorted_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]
    for city, count in sorted_cities:
        print(f"{city:30} {count:4} supermercados")
    print("="*60)


def main():
    print("="*60)
    print("OBTENIENDO SUPERMERCADOS REALES DESDE OPENSTREETMAP")
    print("="*60)
    print(f"\nBuscando {len(SUPERMARKET_BRANDS)} cadenas de supermercados en Chile...")
    print()
    
    # Obtener datos
    data = fetch_all_supermarkets()
    
    # Guardar en JSON
    save_to_json(data)
    
    # Mostrar estadísticas
    print_statistics(data)
    
    print("\nOK Proceso completado exitosamente")
    print("\nProximo paso: ejecutar 'populate_from_osm.py' para cargar los datos a la BD")


if __name__ == "__main__":
    main()
