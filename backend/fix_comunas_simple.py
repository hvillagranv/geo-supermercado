"""
Script para corregir comunas faltantes - Actualización directa
"""
import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models import Supermercado

def main():
    db = SessionLocal()
    
    try:
        # Obtener supermercados sin comuna
        sin_comuna = db.query(Supermercado).filter(
            (Supermercado.comuna == 'Sin comuna') | 
            (Supermercado.comuna == None) |
            (Supermercado.comuna == '')
        ).all()
        
        print(f"Total supermercados sin comuna: {len(sin_comuna)}")
        print("\nCorrigiendo comunas basándose en la dirección...\n")
        
        actualizados = 0
        
        for s in sin_comuna:
            print(f"ID {s.id}: {s.nombre}")
            print(f"  Dirección: {s.direccion}")
            
            # La dirección en estos casos ES la comuna
            # Ejemplos: "La Serena", "Villa Alemana", "Quilicura", etc.
            comuna_nueva = s.direccion.strip()
            
            if comuna_nueva:
                print(f"  -> Asignando comuna: {comuna_nueva}")
                s.comuna = comuna_nueva
                # Actualizar dirección a "Sin dirección específica" o similar
                s.direccion = f"{s.nombre}, {comuna_nueva}"
                actualizados += 1
            
            print()
        
        # Guardar cambios
        if actualizados > 0:
            db.commit()
            print(f"\n[OK] {actualizados} comunas actualizadas correctamente")
        
        # Verificar resultados
        print("\n" + "="*70)
        print("VERIFICACIÓN FINAL")
        print("="*70)
        
        sin_comuna_final = db.query(Supermercado).filter(
            (Supermercado.comuna == 'Sin comuna') | 
            (Supermercado.comuna == None) |
            (Supermercado.comuna == '')
        ).count()
        
        print(f"\nSupermercados sin comuna: {sin_comuna_final}")
        
        if sin_comuna_final == 0:
            print("[OK] Todos los supermercados tienen comuna asignada!")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
