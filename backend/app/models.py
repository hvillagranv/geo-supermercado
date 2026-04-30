from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Supermercado(Base):
    __tablename__ = "supermercados"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cadena = Column(String, index=True, nullable=True)
    direccion = Column(String)
    comuna = Column(String)
    ciudad = Column(String, default="Santiago")
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    telefono = Column(String, nullable=True)
    horario = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with prices
    precios = relationship("Precio", back_populates="supermercado")


class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    marca = Column(String, nullable=True)
    categoria = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    codigo_barra = Column(String, nullable=True, unique=True)
    unidad_medida = Column(String, default="unidad")  # kg, litro, unidad
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with prices
    precios = relationship("Precio", back_populates="producto")


class Precio(Base):
    __tablename__ = "precios"
    
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    supermercado_id = Column(Integer, ForeignKey("supermercados.id"))
    precio = Column(Float, nullable=False)
    precio_oferta = Column(Float, nullable=True)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)
    url_producto = Column(String, nullable=True)
    
    # Relationships
    producto = relationship("Producto", back_populates="precios")
    supermercado = relationship("Supermercado", back_populates="precios")
