from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SupermercadoBase(BaseModel):
    nombre: str
    cadena: Optional[str] = None
    direccion: str
    comuna: str
    ciudad: str = "Santiago"
    latitud: float
    longitud: float
    telefono: Optional[str] = None
    horario: Optional[str] = None


class SupermercadoCreate(SupermercadoBase):
    pass


class Supermercado(SupermercadoBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SupermercadoCercano(Supermercado):
    distancia: float  # Distance in km


class ProductoBase(BaseModel):
    nombre: str
    marca: Optional[str] = None
    categoria: str
    descripcion: Optional[str] = None
    codigo_barra: Optional[str] = None
    unidad_medida: str = "unidad"


class ProductoCreate(ProductoBase):
    pass


class Producto(ProductoBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PrecioBase(BaseModel):
    producto_id: int
    supermercado_id: int
    precio: float
    precio_oferta: Optional[float] = None
    url_producto: Optional[str] = None


class PrecioCreate(PrecioBase):
    pass


class Precio(PrecioBase):
    id: int
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True
