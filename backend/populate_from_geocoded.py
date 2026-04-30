"""
Script para poblar la base de datos con supermercados reales geocodificados
"""

import json
import sys
from sqlalchemy.orm import Session

# Agregar el directorio app al path
sys.path.append('.')

from app.database import SessionLocal, engine
from app.models import Base, Supermercado


def clear_database(db: Session):
    """
    Limpia todos los supermercados existentes
    """
    print("Limpiando base de datos...")
    db.query(Supermercado).delete()
    db.commit()
    print("OK Base de datos limpiada")


def load_geocoded_data(filename: str = "supermarkets_chile.json"):
    """
    Carga los datos geocodificados desde el archivo JSON
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"ERROR: Archivo {filename} no encontrado")
        print("Ejecuta primero: python geocode_supermarkets.py")
        return None


def populate_database(db: Session, data: dict):
    """
    Puebla la base de datos con los supermercados geocodificados
    """
    total = 0
    
    for brand, stores in data.items():
        print(f"\nAgregando {brand}:")
        
        for store in stores:
            try:
                # Crear instancia de Supermercado
                supermercado = Supermercado(
                    nombre=store['nombre'],
                    cadena=brand,
                    direccion=store['direccion'],
                    comuna=store['comuna'],
                    latitud=store['lat'],
                    longitud=store['lon'],
                    telefono=store.get('telefono', ''),
                    horario=store.get('horario', 'Lun-Dom 9:00-22:00')
                )
                
                db.add(supermercado)
                print(f"  OK {store['nombre']}")
                total += 1
                
            except Exception as e:
                print(f"  ERROR al agregar {store['nombre']}: {e}")
    
    # Confirmar cambios
    db.commit()
    return total


def print_summary(db: Session):
    """
    Imprime resumen de la base de datos
    """
    print("\n" + "="*60)
    print("RESUMEN DE LA BASE DE DATOS")
    print("="*60)
    
    # Total de supermercados
    total = db.query(Supermercado).count()
    print(f"Total de supermercados: {total}")
    
    # Por cadena
    print("\nPor cadena:")
    cadenas = db.query(Supermercado.cadena).distinct().all()
    for (cadena,) in cadenas:
        count = db.query(Supermercado).filter(Supermercado.cadena == cadena).count()
        print(f"  {cadena:20} {count:3} supermercados")
    
    # Por región (inferida de comuna)
    print("\nPor region:")
    regiones = {
        'Metropolitana': ['Santiago', 'Providencia', 'Las Condes', 'Ñuñoa', 
                         'Peñalolén', 'Maipú', 'Quilicura', 'La Florida', 'Lo Barnechea'],
        'Biobío': ['Concepción', 'Talcahuano', 'San Pedro de la Paz', 
                  'Chiguayante', 'Coronel', 'Lota', 'Penco', 'Tomé'],
        'Valparaíso': ['Viña del Mar', 'Valparaíso']
    }
    
    for region, comunas in regiones.items():
        count = db.query(Supermercado).filter(Supermercado.comuna.in_(comunas)).count()
        print(f"  {region:20} {count:3} supermercados")
    
    print("="*60)


def main():
    print("="*60)
    print("POBLANDO BASE DE DATOS CON SUPERMERCADOS REALES")
    print("="*60)
    
    # Crear tablas si no existen
    print("\nCreando tablas...")
    Base.metadata.create_all(bind=engine)
    
    # Abrir sesión
    db = SessionLocal()
    
    try:
        # Limpiar base de datos existente
        clear_database(db)
        
        # Cargar datos geocodificados
        print("\nCargando datos geocodificados...")
        data = load_geocoded_data()
        
        if not data:
            print("ERROR: No se pudieron cargar los datos")
            return
        
        # Poblar base de datos
        print("\nPoblando base de datos...")
        total = populate_database(db, data)
        
        print(f"\nOK Se agregaron {total} supermercados a la base de datos")
        
        # Mostrar resumen
        print_summary(db)
        
        print("\nOK Proceso completado exitosamente!")
        print("\nAhora puedes:")
        print("1. Iniciar el backend: uvicorn app.main:app --reload")
        print("2. Abrir la aplicacion en: http://localhost:3000")
        print("3. Ver los supermercados reales en el mapa")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
