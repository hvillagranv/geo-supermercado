"""
Script para verificar supermercados sin comuna
"""
import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models import Supermercado

def main():
    db = SessionLocal()
    
    try:
        # Contar supermercados sin comuna o con "Sin comuna"
        sin_comuna = db.query(Supermercado).filter(
            (Supermercado.comuna == 'Sin comuna') | 
            (Supermercado.comuna == None) |
            (Supermercado.comuna == '')
        ).all()
        
        print(f"Total supermercados sin comuna: {len(sin_comuna)}")
        print("\nEjemplos:")
        for s in sin_comuna[:10]:
            print(f"ID: {s.id}")
            print(f"  Nombre: {s.nombre}")
            print(f"  Dirección: {s.direccion}")
            print(f"  Comuna: '{s.comuna}'")
            print(f"  Coordenadas: ({s.latitud}, {s.longitud})")
            print()
        
        # Mostrar distribución de comunas
        print("\n" + "="*70)
        print("DISTRIBUCIÓN DE COMUNAS")
        print("="*70)
        from sqlalchemy import func
        comunas_count = db.query(
            Supermercado.comuna,
            func.count(Supermercado.id).label('count')
        ).group_by(Supermercado.comuna).order_by(func.count(Supermercado.id).desc()).limit(20).all()
        
        for comuna, count in comunas_count:
            print(f"{comuna:40} {count:5} supermercados")
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
