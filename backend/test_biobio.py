"""
Script de prueba para verificar supermercados de la Región del Biobío
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_supermercados_biobio():
    """Prueba búsqueda de supermercados en diferentes comunas del Biobío"""
    
    ubicaciones = {
        "Concepción Centro": {"lat": -36.8270, "lng": -73.0498, "nombre": "Plaza de la Independencia"},
        "Talcahuano": {"lat": -36.7130, "lng": -73.1140, "nombre": "Mall Plaza El Trébol"},
        "San Pedro de la Paz": {"lat": -36.8485, "lng": -73.0965, "nombre": "Mall Plaza Los Ángeles"},
        "Chiguayante": {"lat": -36.9225, "lng": -73.0295, "nombre": "Centro Chiguayante"},
        "Coronel": {"lat": -37.0285, "lng": -73.1510, "nombre": "Centro Coronel"},
        "Lota": {"lat": -37.0895, "lng": -73.1565, "nombre": "Centro Lota"},
        "Penco": {"lat": -36.7385, "lng": -72.9965, "nombre": "Centro Penco"},
        "Tomé": {"lat": -36.6165, "lng": -72.9575, "nombre": "Centro Tomé"}
    }
    
    print("="*80)
    print("PRUEBA DE SUPERMERCADOS - REGIÓN DEL BIOBÍO")
    print("="*80)
    
    for comuna, datos in ubicaciones.items():
        print(f"\n{'-'*80}")
        print(f"[UBICACION] {comuna} ({datos['nombre']})")
        print(f"   Coordenadas: {datos['lat']}, {datos['lng']}")
        print(f"{'-'*80}")
        
        try:
            # Buscar supermercados en un radio de 5km
            response = requests.get(
                f"{BASE_URL}/api/supermercados/cercanos",
                params={
                    "lat": datos['lat'], 
                    "lng": datos['lng'], 
                    "radio": 5,
                    "limit": 10
                }
            )
            
            if response.status_code == 200:
                supermercados = response.json()
                print(f"[OK] Encontrados {len(supermercados)} supermercados en 5km:\n")
                
                for i, super_obj in enumerate(supermercados, 1):
                    print(f"   {i}. {super_obj['nombre']}")
                    print(f"      Direccion: {super_obj['direccion']}, {super_obj['comuna']}")
                    print(f"      Cadena: {super_obj['cadena']}")
                    print(f"      Distancia: {super_obj['distancia']} km")
                    if super_obj.get('telefono'):
                        print(f"      Telefono: {super_obj['telefono']}")
                    print()
                    
            elif response.status_code == 404:
                print(f"[AVISO] No se encontraron supermercados en 5km")
            else:
                print(f"[ERROR] Error: {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Error de conexion: {e}")
    
    print("\n" + "="*80)
    print("RESUMEN GENERAL")
    print("="*80)
    
    try:
        # Contar todos los supermercados por ciudad
        response = requests.get(f"{BASE_URL}/api/supermercados")
        if response.status_code == 200:
            todos = response.json()
            
            # Filtrar por Biobío
            biobio = [s for s in todos if s['ciudad'] in ['Concepción', 'Talcahuano', 'San Pedro de la Paz', 
                                                            'Chiguayante', 'Coronel', 'Lota', 'Penco', 'Tomé']]
            santiago = [s for s in todos if s['ciudad'] == 'Santiago']
            
            print(f"\n[RESUMEN] Total de supermercados en la base de datos: {len(todos)}")
            print(f"   - Region del Biobio: {len(biobio)}")
            print(f"   - Region Metropolitana (Santiago): {len(santiago)}")
            
            # Distribución por cadena en Biobío
            print(f"\n[CADENAS] Distribucion por cadena en Biobio:")
            cadenas = {}
            for s in biobio:
                cadenas[s['cadena']] = cadenas.get(s['cadena'], 0) + 1
            
            for cadena, count in sorted(cadenas.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {cadena}: {count} supermercados")
                
    except Exception as e:
        print(f"Error obteniendo resumen: {e}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n[TEST] Iniciando pruebas de supermercados del Biobio...\n")
    test_supermercados_biobio()
    print("\n[OK] Pruebas completadas!\n")
