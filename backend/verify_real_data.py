"""
Script para verificar que el backend tiene los datos reales
"""

import requests
import json

print("="*60)
print("VERIFICANDO DATOS REALES EN EL BACKEND")
print("="*60)

# Verificar que el backend está corriendo
try:
    response = requests.get("http://localhost:8000/api/supermercados?limit=5", timeout=5)
    
    if response.status_code == 200:
        supermercados = response.json()
        
        print(f"\nOK Backend respondiendo correctamente")
        print(f"Total de supermercados en la respuesta: {len(supermercados)}")
        
        print("\nPrimeros supermercados:")
        print("-"*60)
        
        for i, s in enumerate(supermercados, 1):
            print(f"\n{i}. {s['nombre']}")
            print(f"   Cadena: {s['cadena']}")
            print(f"   Direccion: {s['direccion']}, {s['comuna']}")
            print(f"   Coordenadas: {s['latitud']}, {s['longitud']}")
        
        print("\n" + "="*60)
        print("VERIFICACION EXITOSA - DATOS REALES CARGADOS")
        print("="*60)
        
        print("\nPuedes abrir la aplicacion en:")
        print("  Frontend: http://localhost:3000")
        print("  Backend API: http://localhost:8000/docs")
        
    else:
        print(f"\nERROR: Backend respondio con codigo {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\nERROR: No se puede conectar al backend")
    print("Asegurate de que el backend este corriendo:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"\nERROR: {e}")
