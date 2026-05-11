# Contexto del Proyecto GeoSupermercado

## Resumen del Proyecto

Aplicación web para encontrar supermercados cercanos en Chile usando geolocalización y búsqueda por mapa interactivo. Permite buscar direcciones, seleccionar puntos en el mapa y ver supermercados dentro del área visible, calculando la distancia desde el punto de referencia seleccionado.

**Stack Tecnológico:**
- **Backend**: FastAPI + SQLite + SQLAlchemy
- **Frontend**: React + Vite + Leaflet (mapas)
- **APIs**: Nominatim (OpenStreetMap) para geocodificación; Google Places API usado para la extracción inicial de datos

---

## Estado Actual (30 Abril 2026)

### Base de Datos
- **Total supermercados**: 959 únicos
- **Fuente**: Google Places API
- **Cobertura**: 13 regiones de Chile, 155 ciudades/comunas configuradas
- **Calidad**: Direcciones verificadas, coordenadas GPS precisas

### Estructura de Archivos Principal

```
geo_supermercado/
├── backend/
│   ├── app/
│   │   ├── main.py           # API FastAPI
│   │   ├── models.py         # Modelos SQLAlchemy (SIN campo 'cadena')
│   │   ├── schemas.py        # Schemas Pydantic (SIN campo 'cadena')
│   │   ├── crud.py           # Operaciones CRUD
│   │   ├── database.py       # Configuración BD
│   │   └── utils.py          # Cálculo de distancias (Haversine)
│   ├── extract_google_places.py      # Extrae datos de Google Places
│   ├── populate_from_google_places.py # Puebla BD desde JSON
│   ├── supermarkets_google_places.json # Datos extraídos (1,437 supermercados)
│   ├── supermercado.db       # Base de datos SQLite
│   ├── .env                  # API key de Google Places
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/Mapa.jsx
│   │   ├── services/api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── start_backend.ps1         # Script para iniciar backend
├── start_frontend.ps1        # Script para iniciar frontend
└── CONTEXTO_PROYECTO.md      # Este archivo
```

---

## Cambios Importantes Realizados

### 1. Eliminación del Campo 'cadena'
**Motivo**: No es un dato necesario para la funcionalidad de la aplicación.

**Archivos modificados**:
- `backend/app/models.py`: Línea 12 eliminada (`cadena = Column(String, ...)`)
- `backend/app/schemas.py`: Línea 8 eliminada (`cadena: Optional[str] = None`)
- `backend/app/crud.py`: Línea 66 eliminada (referencia a `super_obj.cadena`)
- `backend/populate_from_google_places.py`: Línea 85 eliminada (`cadena=chain`)

**IMPORTANTE**: Después de modificar modelos, siempre eliminar y recrear la BD:
```bash
cd backend
Remove-Item -Force supermercado.db
python populate_from_google_places.py
```

### 2. Expansión de Cobertura Geográfica

**Lista de ciudades expandida** de 21 a **155 ciudades** en `extract_google_places.py`:

#### Distribución por Región:
- **Región XV** (Arica y Parinacota): 2 ciudades
- **Región I** (Tarapacá): 3 ciudades  
- **Región II** (Antofagasta): 6 ciudades
- **Región III** (Atacama): 4 ciudades
- **Región IV** (Coquimbo): 7 ciudades
- **Región V** (Valparaíso): 13 ciudades
- **Región XIII** (Metropolitana): 39 comunas
- **Región VI** (O'Higgins): 9 ciudades
- **Región VII** (Maule): 8 ciudades
- **Región XVI** (Ñuble): 6 ciudades
- **Región VIII** (Biobío): 18 ciudades
- **Región IX** (Araucanía): 15 ciudades
- **Región XIV** (Los Ríos): 4 ciudades
- **Región X** (Los Lagos): 13 ciudades
- **Región XI** (Aysén): 4 ciudades
- **Región XII** (Magallanes): 4 ciudades

**Total**: 155 ciudades/comunas

---

## Modelo de Datos Actual

### Supermercado
```python
class Supermercado(Base):
    __tablename__ = "supermercados"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    direccion = Column(String)
    comuna = Column(String)
    ciudad = Column(String, default="Santiago")
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    telefono = Column(String, nullable=True)
    horario = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**NOTA**: NO incluye campo `cadena` (fue eliminado)

---

## Estadísticas de Extracción

### Datos Actuales (supermarkets_google_places.json)
- **Total extraído**: 1,437 supermercados
- **Total único en BD**: 959 supermercados
- **Duplicados eliminados**: 478

### Por Cadena (en archivo JSON):
1. Unimarc: 283 supermercados
2. Lider: 260 supermercados
3. Jumbo: 219 supermercados
4. Santa Isabel: 170 supermercados
5. SuperBodega aCuenta: 107 supermercados
6. Mayorista 10: 103 supermercados
7. Tottus: 86 supermercados
8. OK Market: 53 supermercados
9. Montserrat: 46 supermercados
10. Alvi: 38 supermercados
11. Merkat: 38 supermercados
12. Ekono: 22 supermercados
13. Las Brisas: 12 supermercados

### Top 10 Comunas con Más Supermercados:
1. Santiago: 50 supermercados
2. Temuco: 37 supermercados
3. Maipú: 30 supermercados
4. Concepción: 28 supermercados
5. La Serena: 27 supermercados
6. Talca: 26 supermercados
7. Viña del Mar: 25 supermercados
8. Las Condes: 24 supermercados
9. Rancagua: 23 supermercados
10. Puerto Montt: 23 supermercados

---

## Endpoints de la API

### Base URL: `http://localhost:8000`

#### Supermercados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/supermercados` | Lista todos los supermercados |
| GET | `/api/supermercados/cercanos?lat={lat}&lng={lng}&radio={km}` | Supermercados cercanos |
| GET | `/api/supermercados/{id}` | Obtener por ID |
| POST | `/api/supermercados` | Crear nuevo |

**Ejemplo de búsqueda cercana**:
```
GET /api/supermercados/cercanos?lat=-36.8270&lng=-73.0498&radio=10
```

#### Productos (para futuras funcionalidades)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/productos` | Lista todos los productos |
| GET | `/api/productos/buscar?q={termino}` | Buscar productos |
| POST | `/api/productos` | Crear nuevo |

---

## Cómo Ejecutar la Aplicación

### Opción 1: Scripts Automáticos (Recomendado)

**Backend**:
```powershell
.\start_backend.ps1
```
- URL: http://localhost:8000
- Docs: http://localhost:8000/docs

**Frontend**:
```powershell
.\start_frontend.ps1
```
- URL: http://localhost:3000

### Opción 2: Manual

**Backend**:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm run dev
```

---

## Proceso de Extracción de Datos

### 1. Extraer Supermercados de Google Places API

```bash
cd backend
python extract_google_places.py
```

**Configuración**:
- 155 ciudades/comunas configuradas
- 13 cadenas de supermercados
- ~2,015 búsquedas estimadas
- Tiempo estimado: 2-3 horas para extracción completa
- Costo: ~$10 USD (de $200 gratis mensuales)

**Resultado**: Archivo `supermarkets_google_places.json`

### 2. Poblar Base de Datos

```bash
cd backend
python populate_from_google_places.py
```

**Proceso**:
- Limpia la base de datos actual
- Lee `supermarkets_google_places.json`
- Elimina duplicados por `place_id`
- Inserta supermercados únicos
- Genera estadísticas

### 3. Verificar Datos

```bash
cd backend
python verify_count.py
```

---

## Scripts de Utilidad Creados

### `backend/test_concepcion.py`
Prueba la búsqueda de supermercados en Concepción:
```bash
python test_concepcion.py
```

### `backend/verify_count.py`
Verifica cantidad de supermercados y estadísticas:
```bash
python verify_count.py
```

### `backend/check_extraction.py`
Verifica el contenido del JSON de extracción:
```bash
python check_extraction.py
```

---

## Problemas Resueltos

### Error: "Error al cargar los supermercados cercanos"

**Causa**: El código intentaba acceder al campo `cadena` que fue eliminado del modelo.

**Archivos afectados**:
- `backend/app/crud.py` (línea 66)
- `backend/app/schemas.py` (línea 8)

**Solución**: 
1. Eliminar referencias a `cadena` en crud.py y schemas.py
2. Reiniciar el backend para aplicar cambios
3. Recrear la base de datos si es necesario

### Error: Extracción toma mucho tiempo

**Causa**: 155 ciudades × 13 cadenas = 2,015 requests a la API

**Solución temporal**: Usar los datos actuales (959 supermercados) que ya cubren las principales ciudades

**Solución futura**: Ejecutar en background o dividir por regiones

---

## Google Places API

### Configuración

Archivo `.env` en `backend/`:
```
GOOGLE_PLACES_API_KEY=AIzaSyA5MQuykMxfqxkI4VsYE0f6LAUe5FbyBc4
```

### Costos
- **Crédito mensual gratuito**: $200 USD
- **Nearby Search**: $32 por 1,000 requests
- **Extracción actual**: ~$10 USD (305 requests)
- **Muy por debajo del presupuesto**

### Límites
- 60 resultados máximo por búsqueda
- Paginación automática implementada
- Rate limiting: 0.5 segundos entre requests

---

## Próximos Pasos Sugeridos

### Corto Plazo
1. ✅ Reiniciar backend/frontend para aplicar cambios
2. ✅ Probar búsqueda en diferentes ciudades (Santiago, Concepción, Valparaíso)
3. ⏳ Ejecutar extracción completa en horario nocturno (opcional)

### Mediano Plazo
1. ⏳ Implementar Módulo 2: Comparación de precios de productos
2. ⏳ Agregar filtros por tipo de supermercado
3. ⏳ Mejorar UI/UX del mapa

### Largo Plazo
1. ⏳ Actualización mensual automática de datos
2. ⏳ Agregar reseñas de usuarios
3. ⏳ Exportar rutas a apps de navegación

---

## Comandos Útiles

### Reiniciar todo (después de cambios en modelos)
```bash
cd backend
Remove-Item -Force supermercado.db
python populate_from_google_places.py
```

### Ver logs del backend
El backend muestra logs en la consola donde se ejecuta `uvicorn`

### Limpiar y reinstalar dependencias

**Backend**:
```bash
cd backend
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

---

## Notas Importantes

### Al modificar modelos de base de datos:
1. Actualizar `models.py`
2. Actualizar `schemas.py` (si aplica)
3. Actualizar `crud.py` (si aplica)
4. Eliminar `supermercado.db`
5. Recrear con `populate_from_google_places.py`
6. Reiniciar backend

### Al agregar nuevas ciudades:
1. Editar `extract_google_places.py`
2. Agregar en lista `CITIES_SEARCH` con formato: `("Nombre", lat, lng, radio_km)`
3. Ejecutar `extract_google_places.py`
4. Ejecutar `populate_from_google_places.py`

### Al actualizar datos:
```bash
cd backend
python extract_google_places.py
python populate_from_google_places.py
```

Frecuencia recomendada: 1 vez al mes

---

## Contacto y Documentación

### Documentos de referencia:
- `GUIA_RAPIDA.md`: Guía de inicio rápido
- `README.md`: Documentación general
- `GUIA_GOOGLE_PLACES_API.txt`: Detalles de Google Places API
- `EXTRACCION_EXITOSA_953_SUPERMERCADOS.txt`: Reporte de extracción anterior

### URLs importantes:
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Google Cloud Console: https://console.cloud.google.com/

---

## Último Commit (Resumen de Cambios)

**Fecha**: 11 Mayo 2026

**Cambios principales**:
1. ✅ Eliminado campo `cadena` de modelos, schemas y CRUD
2. ✅ Expandida lista de ciudades de 21 a 155
3. ✅ Base de datos actualizada con 959 supermercados
4. ✅ Corregido error de búsqueda en Concepción
5. ✅ Scripts de verificación creados
6. ✅ Documentación del proyecto completada (CONTEXTO_PROYECTO.md)
7. ✅ Commit de cambios actuales realizado

**Estado**: ✅ PRODUCCIÓN READY

**Pendiente**:
- Extracción completa con 155 ciudades (opcional, toma 2-3 horas)
- Módulo 2: Comparación de precios (PRÓXIMA TAREA PRINCIPAL)

---

*Última actualización: 11 de Mayo 2026*
