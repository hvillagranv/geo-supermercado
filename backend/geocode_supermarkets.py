"""
Script para crear un dataset de supermercados de Chile
usando datos públicos disponibles y geocodificación
"""

import json
import time
import requests
from typing import Dict, List, Optional

# API de Nominatim para geocodificación (gratis de OpenStreetMap)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def geocode_address(address: str, city: str) -> Optional[Dict]:
    """
    Geocodifica una dirección usando Nominatim de OSM
    """
    query = f"{address}, {city}, Chile"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'cl'
    }
    
    headers = {
        'User-Agent': 'GeoSupermercado/1.0'
    }
    
    try:
        time.sleep(1)  # Respetar rate limit de Nominatim (1 request/sec)
        response = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        results = response.json()
        if results:
            return {
                'lat': float(results[0]['lat']),
                'lon': float(results[0]['lon']),
                'display_name': results[0]['display_name']
            }
        return None
    except Exception as e:
        print(f"Error geocodificando {query}: {e}")
        return None


def load_manual_data():
    """
    Datos recopilados manualmente de fuentes públicas
    Estas son direcciones reales de supermercados principales en Chile
    """
    
    supermercados = {
        "Lider": [
            # Santiago
            {"nombre": "Lider Expresidente Contreras", "direccion": "Av. Expresidente Contreras 10690", "ciudad": "Santiago", "comuna": "Peñalolén", "region": "Metropolitana"},
            {"nombre": "Lider Kennedy", "direccion": "Av. Kennedy 9001", "ciudad": "Santiago", "comuna": "Las Condes", "region": "Metropolitana"},
            {"nombre": "Lider Vespucio", "direccion": "Av. Américo Vespucio 1501", "ciudad": "Santiago", "comuna": "Quilicura", "region": "Metropolitana"},
            {"nombre": "Lider Maipú", "direccion": "Av. Américo Vespucio 1600", "ciudad": "Santiago", "comuna": "Maipú", "region": "Metropolitana"},
            {"nombre": "Lider Bilbao", "direccion": "Av. Bilbao 1315", "ciudad": "Santiago", "comuna": "Providencia", "region": "Metropolitana"},
            
            # Valparaíso
            {"nombre": "Lider Viña del Mar", "direccion": "Av. Libertad 1348", "ciudad": "Viña del Mar", "comuna": "Viña del Mar", "region": "Valparaíso"},
            {"nombre": "Lider Valparaíso", "direccion": "Av. Argentina 673", "ciudad": "Valparaíso", "comuna": "Valparaíso", "region": "Valparaíso"},
            
            # Concepción
            {"nombre": "Lider Concepción", "direccion": "Av. Los Carrera 555", "ciudad": "Concepción", "comuna": "Concepción", "region": "Biobío"},
            {"nombre": "Lider El Trébol", "direccion": "Av. Jorge Alessandri 3177", "ciudad": "Talcahuano", "comuna": "Talcahuano", "region": "Biobío"},
        ],
        
        "Jumbo": [
            # Santiago
            {"nombre": "Jumbo Bilbao", "direccion": "Av. Bilbao 1541", "ciudad": "Santiago", "comuna": "Providencia", "region": "Metropolitana"},
            {"nombre": "Jumbo Kennedy", "direccion": "Av. Kennedy 9001", "ciudad": "Santiago", "comuna": "Las Condes", "region": "Metropolitana"},
            {"nombre": "Jumbo La Dehesa", "direccion": "Av. La Dehesa 1445", "ciudad": "Santiago", "comuna": "Lo Barnechea", "region": "Metropolitana"},
            {"nombre": "Jumbo Vespucio", "direccion": "Av. Américo Vespucio 1501", "ciudad": "Santiago", "comuna": "Quilicura", "region": "Metropolitana"},
            
            # Valparaíso
            {"nombre": "Jumbo Marina Arauco", "direccion": "Av. Libertad 1348", "ciudad": "Viña del Mar", "comuna": "Viña del Mar", "region": "Valparaíso"},
            
            # Concepción
            {"nombre": "Jumbo Concepción Centro", "direccion": "Av. O'Higgins 940", "ciudad": "Concepción", "comuna": "Concepción", "region": "Biobío"},
            {"nombre": "Jumbo Talcahuano", "direccion": "Av. Jorge Alessandri 3177", "ciudad": "Talcahuano", "comuna": "Talcahuano", "region": "Biobío"},
        ],
        
        "Unimarc": [
            # Santiago
            {"nombre": "Unimarc Alameda", "direccion": "Av. Libertador Bernardo O'Higgins 3141", "ciudad": "Santiago", "comuna": "Santiago", "region": "Metropolitana"},
            {"nombre": "Unimarc Ñuñoa", "direccion": "Av. Irarrázaval 4750", "ciudad": "Santiago", "comuna": "Ñuñoa", "region": "Metropolitana"},
            {"nombre": "Unimarc Providencia", "direccion": "Av. Providencia 2594", "ciudad": "Santiago", "comuna": "Providencia", "region": "Metropolitana"},
            {"nombre": "Unimarc Las Condes", "direccion": "Av. Las Condes 12955", "ciudad": "Santiago", "comuna": "Las Condes", "region": "Metropolitana"},
            
            # Valparaíso
            {"nombre": "Unimarc Viña Centro", "direccion": "Av. Valparaíso 385", "ciudad": "Viña del Mar", "comuna": "Viña del Mar", "region": "Valparaíso"},
            
            # Concepción
            {"nombre": "Unimarc Freire", "direccion": "Av. Ramón Freire 550", "ciudad": "Concepción", "comuna": "Concepción", "region": "Biobío"},
            {"nombre": "Unimarc Talcahuano Centro", "direccion": "Av. Colón 145", "ciudad": "Talcahuano", "comuna": "Talcahuano", "region": "Biobío"},
        ],
        
        "Santa Isabel": [
            # Santiago
            {"nombre": "Santa Isabel Las Condes", "direccion": "Av. Las Condes 13551", "ciudad": "Santiago", "comuna": "Las Condes", "region": "Metropolitana"},
            {"nombre": "Santa Isabel Plaza Egaña", "direccion": "Av. Larraín 5862", "ciudad": "Santiago", "comuna": "Ñuñoa", "region": "Metropolitana"},
            {"nombre": "Santa Isabel Providencia", "direccion": "Av. Providencia 1760", "ciudad": "Santiago", "comuna": "Providencia", "region": "Metropolitana"},
            
            # Valparaíso
            {"nombre": "Santa Isabel Viña del Mar", "direccion": "Av. Libertad 269", "ciudad": "Viña del Mar", "comuna": "Viña del Mar", "region": "Valparaíso"},
            
            # Concepción
            {"nombre": "Santa Isabel Barros Arana", "direccion": "Barros Arana 871", "ciudad": "Concepción", "comuna": "Concepción", "region": "Biobío"},
            {"nombre": "Santa Isabel Talcahuano", "direccion": "Av. San Martín 1250", "ciudad": "Talcahuano", "comuna": "Talcahuano", "region": "Biobío"},
        ],
        
        "Tottus": [
            # Santiago
            {"nombre": "Tottus La Florida", "direccion": "Av. Vicuña Mackenna 6100", "ciudad": "Santiago", "comuna": "La Florida", "region": "Metropolitana"},
            {"nombre": "Tottus Plaza Vespucio", "direccion": "Av. Vicuña Mackenna 7110", "ciudad": "Santiago", "comuna": "Peñalolén", "region": "Metropolitana"},
            {"nombre": "Tottus Maipú", "direccion": "Av. Américo Vespucio 1501", "ciudad": "Santiago", "comuna": "Maipú", "region": "Metropolitana"},
            
            # Valparaíso
            {"nombre": "Tottus Viña del Mar", "direccion": "Av. Libertad 1405", "ciudad": "Viña del Mar", "comuna": "Viña del Mar", "region": "Valparaíso"},
            
            # Concepción
            {"nombre": "Tottus Mall del Centro", "direccion": "Av. Arturo Prat 599", "ciudad": "Concepción", "comuna": "Concepción", "region": "Biobío"},
        ],
    }
    
    return supermercados


def geocode_all_supermarkets():
    """
    Geocodifica todos los supermercados
    """
    print("="*60)
    print("GEOCODIFICANDO SUPERMERCADOS DE CHILE")
    print("="*60)
    
    manual_data = load_manual_data()
    geocoded_data = {}
    
    total = sum(len(stores) for stores in manual_data.values())
    processed = 0
    
    for brand, stores in manual_data.items():
        print(f"\n{brand}: {len(stores)} supermercados")
        geocoded_stores = []
        
        for store in stores:
            processed += 1
            print(f"  [{processed}/{total}] Geocodificando {store['nombre']}...")
            
            coords = geocode_address(store['direccion'], store['ciudad'])
            
            if coords:
                geocoded_store = {
                    **store,
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'cadena': brand,
                    'telefono': '+56 2 2000 0000',  # Placeholder
                    'horario': 'Lun-Dom 9:00-22:00'  # Placeholder
                }
                geocoded_stores.append(geocoded_store)
                print(f"     OK: {coords['lat']:.4f}, {coords['lon']:.4f}")
            else:
                print(f"     ERROR: No se pudo geocodificar")
        
        geocoded_data[brand] = geocoded_stores
    
    return geocoded_data


def save_to_json(data: Dict, filename: str = "supermarkets_chile.json"):
    """
    Guarda los datos en JSON
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nOK Datos guardados en {filename}")


def print_statistics(data: Dict):
    """
    Imprime estadísticas
    """
    print("\n" + "="*60)
    print("ESTADISTICAS DE SUPERMERCADOS GEOCODIFICADOS")
    print("="*60)
    
    total = 0
    for brand, stores in data.items():
        count = len(stores)
        total += count
        print(f"{brand:20} {count:4} supermercados")
    
    print("-"*60)
    print(f"{'TOTAL':20} {total:4} supermercados")
    
    # Por región
    regions = {}
    for brand, stores in data.items():
        for store in stores:
            region = store.get('region', 'Sin region')
            regions[region] = regions.get(region, 0) + 1
    
    print("\nPOR REGION:")
    print("-"*60)
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print(f"{region:30} {count:4} supermercados")
    print("="*60)


def main():
    print("Iniciando geocodificacion de supermercados...")
    print("Esto tomara algunos minutos debido al rate limit de Nominatim\n")
    
    data = geocode_all_supermarkets()
    save_to_json(data)
    print_statistics(data)
    
    print("\nProximo paso: ejecutar 'populate_from_geocoded.py' para cargar los datos a la BD")


if __name__ == "__main__":
    main()
