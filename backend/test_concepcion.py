"""
Test para verificar búsqueda de supermercados en Concepción
"""
import requests

# Coordenadas de Concepción
LAT = -36.8270
LNG = -73.0498
RADIO = 10  # km

print("="*70)
print("PROBANDO BÚSQUEDA DE SUPERMERCADOS EN CONCEPCIÓN")
print("="*70)
print(f"\nCoordenadas: {LAT}, {LNG}")
print(f"Radio: {RADIO} km")

url = f"http://localhost:8000/api/supermercados/cercanos?lat={LAT}&lng={LNG}&radio={RADIO}"

try:
    response = requests.get(url, timeout=10)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        supermercados = response.json()
        print(f"\nOK Supermercados encontrados: {len(supermercados)}")
        
        if supermercados:
            print("\nPrimeros 5 supermercados:")
            for i, s in enumerate(supermercados[:5], 1):
                print(f"  {i}. {s['nombre']} - {s['direccion']} ({s['distancia']:.2f} km)")
        else:
            print("\nADVERTENCIA: No se encontraron supermercados en el radio especificado")
    else:
        print(f"\nERROR: {response.status_code}")
        print(f"Detalle: {response.text}")
        
except Exception as e:
    print(f"\nERROR de conexion: {e}")
    print("\n¿Está corriendo el backend? Ejecuta:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")

print("\n" + "="*70)
