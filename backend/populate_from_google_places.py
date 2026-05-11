"""
Script para poblar la base de datos con datos de Google Places
"""

import json
import sys
from sqlalchemy.orm import Session

sys.path.append('.')

from app.database import SessionLocal, engine
from app.models import Base, Supermercado


def load_google_places_data(filename: str = "supermarkets_google_places.json"):
    """
    Carga los datos de Google Places
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"ERROR: Archivo {filename} no encontrado")
        print("Ejecuta primero: python extract_google_places.py")
        return None


def clean_address(address: str) -> tuple:
    """
    Extrae dirección y comuna de la dirección de Google Places.
    
    Las direcciones vienen en diferentes formatos:
    - "Calle 123, Comuna" (2 partes) -> Comuna es la última
    - "Calle, Otra Calle, Comuna" (3+ partes) -> Comuna es la última
    - "Comuna" (1 parte) -> Es solo la comuna, usarla como dirección también
    
    Returns:
        tuple: (direccion, comuna)
    """
    parts = [p.strip() for p in address.split(',')]
    
    if len(parts) == 1:
        # Solo hay una parte, es la comuna/ciudad
        return address, address
    elif len(parts) >= 2:
        # La comuna SIEMPRE es la última parte
        comuna = parts[-1]
        # La dirección es todo menos la última parte
        direccion = ', '.join(parts[:-1])
        return direccion, comuna
    else:
        # Caso por defecto (no debería ocurrir)
        return address, "Sin comuna"


def populate_database(db: Session, data: dict):
    """
    Puebla la base de datos con los datos de Google Places
    """
    print("="*70)
    print("POBLANDO BASE DE DATOS CON DATOS DE GOOGLE PLACES")
    print("="*70)
    
    # Limpiar base de datos
    print("\nLimpiando base de datos...")
    db.query(Supermercado).delete()
    db.commit()
    
    total = 0
    duplicates = 0
    errors = 0
    
    # Conjunto para detectar duplicados
    seen_places = set()
    
    for chain, places in data.items():
        print(f"\n{chain}:")
        
        for place in places:
            try:
                # Si el JSON incluye 'types', aplicar filtro adicional para mayor seguridad
                place_types = place.get('types', None)
                if place_types:
                    if not any(t in ("supermarket",) for t in place_types):
                        # Omitir lugares que no sean tipo 'supermarket'
                        continue

                # Filtrar por user_ratings_total para excluir minimarkets y espacios muy pequeños
                user_ratings_total = place.get('user_ratings_total', 0)
                if user_ratings_total < 50:
                    # Omitir lugares con muy pocas reseñas (probablemente minimarkets o muy pequeños)
                    continue

                # Si el JSON incluye el nombre original, validar que pertenezca a una de las cadenas
                # Esto evita insertar tiendas que no pertenecen a las 13 cadenas
                name = place.get('name', '')
                if name:
                    # Normalizar similitud básica (minúsculas, sin acentos)
                    def _norm(s):
                        import unicodedata
                        s2 = unicodedata.normalize('NFD', s)
                        s2 = ''.join(ch for ch in s2 if unicodedata.category(ch) != 'Mn')
                        return s2.lower()

                    # Ya no imponemos coincidencia estricta por nombre de cadena.
                    # Permitimos supermercados locales siempre que el tipo indique 'supermarket'.
                place_id = place['place_id']
                
                # Evitar duplicados
                if place_id in seen_places:
                    duplicates += 1
                    continue
                
                seen_places.add(place_id)
                
                # Limpiar dirección
                direccion, comuna = clean_address(place['address'])
                
                # Crear supermercado
                supermercado = Supermercado(
                    nombre=place['name'],
                    direccion=direccion,
                    comuna=comuna,
                    latitud=place['lat'],
                    longitud=place['lon'],
                    telefono=''
                )
                
                db.add(supermercado)
                total += 1
                
                if total % 50 == 0:
                    print(f"  Procesados: {total}")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                errors += 1
    
    # Commit final
    db.commit()
    
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Total insertados: {total}")
    print(f"Duplicados omitidos: {duplicates}")
    print(f"Errores: {errors}")
    print("="*70)
    
    return total


def print_database_stats(db: Session):
    """
    Imprime estadísticas de la base de datos
    """
    print("\n" + "="*70)
    print("ESTADÍSTICAS DE LA BASE DE DATOS")
    print("="*70)
    
    total = db.query(Supermercado).count()
    print(f"\nTotal de supermercados: {total}")
    
    print("\nPor nombre:")
    nombres = db.query(Supermercado.nombre).distinct().limit(10).all()
    for (nombre,) in sorted(nombres):
        count = db.query(Supermercado).filter(Supermercado.nombre == nombre).count()
        print(f"  {nombre:40} {count:5} supermercados")
    
    print("\nTop 10 comunas con más supermercados:")
    from sqlalchemy import func
    top_comunas = db.query(
        Supermercado.comuna,
        func.count(Supermercado.id).label('count')
    ).group_by(Supermercado.comuna).order_by(func.count(Supermercado.id).desc()).limit(10).all()
    
    for comuna, count in top_comunas:
        print(f"  {comuna:30} {count:5} supermercados")
    
    print("="*70)


def main():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Cargar datos
    data = load_google_places_data()
    
    if not data:
        return
    
    # Abrir sesión
    db = SessionLocal()
    
    try:
        # Poblar base de datos
        populate_database(db, data)
        
        # Mostrar estadísticas
        print_database_stats(db)
        
        print("\nOK Proceso completado!")
        print("\nAhora puedes:")
        print("1. Iniciar el backend: uvicorn app.main:app --reload")
        print("2. Ver la aplicación en: http://localhost:3000")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
