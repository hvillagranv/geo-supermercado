"""
Script de prueba para verificar que el backend funciona correctamente
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Prueba el endpoint raíz"""
    print("Probando endpoint raíz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de que el backend esté corriendo en http://localhost:8000")
        return False
    return True

def test_supermercados():
    """Prueba listar todos los supermercados"""
    print("Probando GET /api/supermercados...")
    try:
        response = requests.get(f"{BASE_URL}/api/supermercados")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total de supermercados: {len(data)}")
        if data:
            print(f"Primer supermercado: {data[0]['nombre']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

def test_supermercados_cercanos():
    """Prueba buscar supermercados cercanos"""
    print("Probando GET /api/supermercados/cercanos...")
    # Coordenadas de Plaza de Armas, Santiago
    lat = -33.4372
    lng = -70.6506
    radio = 10
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/supermercados/cercanos",
            params={"lat": lat, "lng": lng, "radio": radio}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Supermercados encontrados en {radio}km: {len(data)}")
        if data:
            print(f"Más cercano: {data[0]['nombre']} - {data[0]['distancia']}km")
        print()
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

if __name__ == "__main__":
    print("=== Test de API Backend ===\n")
    
    if not test_root():
        print("\n[ERROR] El backend no está corriendo.")
        print("Ejecuta: python -m uvicorn app.main:app --reload")
        exit(1)
    
    test_supermercados()
    test_supermercados_cercanos()
    
    print("\n=== Tests completados ===")
