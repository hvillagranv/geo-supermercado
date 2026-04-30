from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db, Base
from . import models, schemas, crud

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Geo Supermercado API",
    description="API para comparar precios de supermercados en Chile",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "mensaje": "Bienvenido a Geo Supermercado API",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@app.get("/api/supermercados", response_model=List[schemas.Supermercado])
def listar_supermercados(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Lista todos los supermercados"""
    supermercados = crud.get_supermercados(db, skip=skip, limit=limit)
    return supermercados


@app.get("/api/supermercados/cercanos", response_model=List[schemas.SupermercadoCercano])
def obtener_supermercados_cercanos(
    lat: float = Query(..., description="Latitud del usuario"),
    lng: float = Query(..., description="Longitud del usuario"),
    radio: float = Query(10.0, description="Radio de búsqueda en kilómetros"),
    limit: int = Query(20, description="Número máximo de resultados"),
    db: Session = Depends(get_db)
):
    """
    Obtiene supermercados cercanos a la ubicación del usuario.
    
    - **lat**: Latitud del usuario (ej: -33.4489)
    - **lng**: Longitud del usuario (ej: -70.6693)
    - **radio**: Radio de búsqueda en km (default: 10km)
    - **limit**: Máximo número de resultados (default: 20)
    """
    supermercados = crud.get_supermercados_cercanos(
        db=db, 
        lat_usuario=lat, 
        lng_usuario=lng, 
        radio_km=radio,
        limit=limit
    )
    
    if not supermercados:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron supermercados en un radio de {radio}km"
        )
    
    return supermercados


@app.get("/api/supermercados/{supermercado_id}", response_model=schemas.Supermercado)
def obtener_supermercado(
    supermercado_id: int, 
    db: Session = Depends(get_db)
):
    """Obtiene un supermercado específico por ID"""
    supermercado = crud.get_supermercado(db, supermercado_id=supermercado_id)
    if supermercado is None:
        raise HTTPException(status_code=404, detail="Supermercado no encontrado")
    return supermercado


@app.post("/api/supermercados", response_model=schemas.Supermercado)
def crear_supermercado(
    supermercado: schemas.SupermercadoCreate, 
    db: Session = Depends(get_db)
):
    """Crea un nuevo supermercado"""
    return crud.create_supermercado(db=db, supermercado=supermercado)


@app.get("/api/productos", response_model=List[schemas.Producto])
def listar_productos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Lista todos los productos"""
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos


@app.get("/api/productos/buscar", response_model=List[schemas.Producto])
def buscar_productos(
    q: str = Query(..., description="Término de búsqueda"),
    db: Session = Depends(get_db)
):
    """
    Busca productos por nombre.
    
    - **q**: Término de búsqueda (ej: 'arroz', 'leche')
    """
    productos = crud.buscar_productos(db=db, termino=q)
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos")
    return productos


@app.post("/api/productos", response_model=schemas.Producto)
def crear_producto(
    producto: schemas.ProductoCreate, 
    db: Session = Depends(get_db)
):
    """Crea un nuevo producto"""
    return crud.create_producto(db=db, producto=producto)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
