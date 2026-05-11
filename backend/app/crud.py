from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .utils import calcular_distancia


def get_supermercados(db: Session, skip: int = 0, limit: int = 100) -> List[models.Supermercado]:
    """Obtiene todos los supermercados"""
    return db.query(models.Supermercado).offset(skip).limit(limit).all()


def get_supermercado(db: Session, supermercado_id: int) -> models.Supermercado:
    """Obtiene un supermercado por ID"""
    return db.query(models.Supermercado).filter(models.Supermercado.id == supermercado_id).first()


def create_supermercado(db: Session, supermercado: schemas.SupermercadoCreate) -> models.Supermercado:
    """Crea un nuevo supermercado"""
    db_supermercado = models.Supermercado(**supermercado.model_dump())
    db.add(db_supermercado)
    db.commit()
    db.refresh(db_supermercado)
    return db_supermercado


def get_supermercados_cercanos(
    db: Session, 
    lat_usuario: float, 
    lng_usuario: float, 
    radio_km: float = 10.0,
    limit: int = 20
) -> List[schemas.SupermercadoCercano]:
    """
    Obtiene supermercados cercanos a una ubicación.
    
    Args:
        db: Session de base de datos
        lat_usuario: Latitud del usuario
        lng_usuario: Longitud del usuario
        radio_km: Radio de búsqueda en kilómetros (default: 10km)
        limit: Máximo número de resultados
    
    Returns:
        Lista de supermercados con distancia calculada, ordenados por distancia
    """
    # Obtener todos los supermercados
    supermercados = db.query(models.Supermercado).all()
    
    # Calcular distancia para cada supermercado
    supermercados_con_distancia = []
    
    for super_obj in supermercados:
        distancia = calcular_distancia(
            lat_usuario, 
            lng_usuario, 
            super_obj.latitud, 
            super_obj.longitud
        )
        
        # Filtrar por radio
        if distancia <= radio_km:
            # Convertir a schema y agregar distancia
            super_dict = {
                "id": super_obj.id,
                "nombre": super_obj.nombre,
                "direccion": super_obj.direccion,
                "comuna": super_obj.comuna,
                "ciudad": super_obj.ciudad,
                "latitud": super_obj.latitud,
                "longitud": super_obj.longitud,
                "telefono": super_obj.telefono,
                "horario": super_obj.horario,
                "created_at": super_obj.created_at,
                "distancia": distancia
            }
            supermercados_con_distancia.append(schemas.SupermercadoCercano(**super_dict))
    
    # Ordenar por distancia
    supermercados_con_distancia.sort(key=lambda x: x.distancia)
    
    # Limitar resultados
    return supermercados_con_distancia[:limit]


def get_supermercados_por_bounds(
    db: Session,
    lat_min: float,
    lat_max: float,
    lng_min: float,
    lng_max: float,
    limit: int = 500
) -> List[models.Supermercado]:
    """
    Obtiene todos los supermercados dentro de un área geográfica (bounds).
    
    Args:
        db: Session de base de datos
        lat_min: Latitud mínima (sur)
        lat_max: Latitud máxima (norte)
        lng_min: Longitud mínima (oeste)
        lng_max: Longitud máxima (este)
        limit: Máximo número de resultados
    
    Returns:
        Lista de supermercados dentro del área
    """
    return db.query(models.Supermercado).filter(
        models.Supermercado.latitud >= lat_min,
        models.Supermercado.latitud <= lat_max,
        models.Supermercado.longitud >= lng_min,
        models.Supermercado.longitud <= lng_max
    ).limit(limit).all()



def get_productos(db: Session, skip: int = 0, limit: int = 100) -> List[models.Producto]:
    """Obtiene todos los productos"""
    return db.query(models.Producto).offset(skip).limit(limit).all()


def buscar_productos(db: Session, termino: str) -> List[models.Producto]:
    """Busca productos por nombre"""
    termino_normalizado = termino.lower().strip()
    return db.query(models.Producto).filter(
        models.Producto.nombre.ilike(f"%{termino_normalizado}%")
    ).all()


def create_producto(db: Session, producto: schemas.ProductoCreate) -> models.Producto:
    """Crea un nuevo producto"""
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def create_precio(db: Session, precio: schemas.PrecioCreate) -> models.Precio:
    """Crea un nuevo precio"""
    db_precio = models.Precio(**precio.model_dump())
    db.add(db_precio)
    db.commit()
    db.refresh(db_precio)
    return db_precio
