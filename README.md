# Geo Supermercado

Aplicación web para comparar precios de supermercados en Chile.

## Características

- 🗺️ Visualización de supermercados cercanos en mapa interactivo
- 📍 Geolocalización del usuario
- 🖱️ Click en cualquier punto del mapa para buscar supermercados
- 🔍 Búsqueda por radio de distancia (1-50 km)
- 📱 Diseño responsivo para móviles
- 🇨🇱 Cobertura: TODO Chile (con Google Places API)
- 🏪 33 supermercados actuales / 600-800 con extracción completa
- 🎯 Datos reales con direcciones verificables

## Stack Tecnológico

### Backend
- FastAPI
- SQLAlchemy + SQLite
- Python 3.x

### Frontend
- React 18
- Vite
- Leaflet (mapas)
- Axios

## Instalación

### Backend

1. Navegar a la carpeta backend:
```bash
cd backend
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Poblar la base de datos:

**OPCIÓN A: Dataset actual (33 supermercados reales - LISTO PARA USAR)**
```bash
# Ya están cargados 33 supermercados reales
# Para recargarlos:
python populate_from_geocoded.py
```

**OPCIÓN B: Extracción completa con Google Places API (600-800 supermercados)**
```bash
# 1. Configurar API key (ver GUIA_GOOGLE_PLACES_API.txt)
# 2. Copiar .env.example a .env y agregar tu API key
# 3. Probar API key
python test_google_places.py

# 4. Extraer todos los supermercados (toma ~30 min)
python extract_google_places.py

# 5. Poblar base de datos
python populate_from_google_places.py
```

**OPCIÓN C: Datasets legacy (para referencia)**
```bash
# 15 supermercados de Santiago (legacy)
python populate_db.py

# 26 supermercados de la Región del Biobío (legacy)
python populate_biobio.py
```

4. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

El backend estará disponible en: http://localhost:8000
Documentación API: http://localhost:8000/docs

### Frontend

1. Navegar a la carpeta frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Iniciar el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en: http://localhost:3000

## Uso

1. Inicia el backend (puerto 8000)
2. Inicia el frontend (puerto 3000)
3. Abre http://localhost:3000 en tu navegador
4. Haz clic en "Mi Ubicación" para obtener supermercados cercanos
5. Ajusta el radio de búsqueda según necesites

## API Endpoints

### Supermercados

- `GET /api/supermercados` - Listar todos los supermercados
- `GET /api/supermercados/cercanos?lat={lat}&lng={lng}&radio={km}` - Supermercados cercanos
- `GET /api/supermercados/{id}` - Obtener un supermercado por ID
- `POST /api/supermercados` - Crear un nuevo supermercado

### Productos (próximamente)

- `GET /api/productos` - Listar todos los productos
- `GET /api/productos/buscar?q={termino}` - Buscar productos
- `POST /api/productos` - Crear un nuevo producto

## Estructura del Proyecto

```
geo_supermercado/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── database.py      # Database config
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # CRUD operations
│   │   └── utils.py         # Utilities (distancia, etc.)
│   │
│   ├── Scripts de poblamiento:
│   │   ├── populate_from_geocoded.py      # 33 supermercados actuales ✅
│   │   ├── extract_google_places.py       # Extracción con Google Places
│   │   ├── populate_from_google_places.py # Poblar desde Google Places
│   │   ├── geocode_supermarkets.py        # Geocodificar direcciones
│   │   ├── populate_db.py                 # Legacy Santiago
│   │   └── populate_biobio.py             # Legacy Biobío
│   │
│   ├── Scripts de prueba:
│   │   ├── test_google_places.py          # Probar API key
│   │   ├── verify_real_data.py            # Verificar BD
│   │   ├── test_api.py                    # Probar endpoints
│   │   └── test_biobio.py                 # Probar región Biobío
│   │
│   ├── .env.example         # Ejemplo configuración Google Places
│   ├── requirements.txt     # Dependencias Python
│   └── supermercado.db      # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Mapa.jsx     # Componente de mapa interactivo
│   │   ├── services/
│   │   │   └── api.js       # Cliente API
│   │   ├── App.jsx          # App principal
│   │   ├── App.css          # Estilos
│   │   └── main.jsx         # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── Documentación:
│   ├── README.md                          # Este archivo
│   ├── GUIA_RAPIDA.md                     # Guía rápida de inicio
│   ├── GUIA_GOOGLE_PLACES_API.txt         # Guía completa Google Places
│   ├── SOLUCION_EXTRACCION_COMPLETA.txt   # Resumen de solución
│   ├── ACTUALIZACION_DATOS_REALES.txt     # Cambios implementados
│   ├── NUEVA_FUNCIONALIDAD_CLICK_MAPA.txt # Click en mapa
│   └── INSTRUCCIONES_PRUEBA.txt           # Instrucciones de prueba
│
└── Scripts de inicio:
    ├── start_backend.bat / .ps1           # Iniciar backend
    └── start_frontend.bat / .ps1          # Iniciar frontend
```

## Extracción de Supermercados

### Datos Actuales (33 supermercados) ✅
- Región Metropolitana: 18 supermercados
- Región del Biobío: 9 supermercados  
- Región de Valparaíso: 6 supermercados
- **Todos con direcciones reales y geocodificadas**

### Extracción Completa (600-800 supermercados)

**Con Google Places API:**
1. Lee `GUIA_GOOGLE_PLACES_API.txt` para instrucciones completas
2. Configurar API key en `.env`
3. Ejecutar `python extract_google_places.py`
4. Costo: ~$11 USD (cubierto por $200 USD gratis mensuales)
5. Cobertura: TODO Chile, 13 regiones, 20+ ciudades

Ver `SOLUCION_EXTRACCION_COMPLETA.txt` para más detalles.

## Próximas Funcionalidades

- [x] Mapa interactivo con Leaflet
- [x] Geolocalización GPS
- [x] Click manual en mapa
- [x] Datos reales geocodificados
- [x] Sistema de extracción con Google Places API
- [ ] Módulo de comparación de precios
- [ ] Web scraping de precios de productos
- [ ] Búsqueda inteligente de productos
- [ ] Histórico de precios
- [ ] Modo oscuro
- [ ] Filtros avanzados
- [ ] Reviews de usuarios
- [ ] App móvil

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue o PR.

## Licencia

MIT
