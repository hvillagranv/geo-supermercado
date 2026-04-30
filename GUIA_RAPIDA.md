# Guía Rápida de Inicio

## Iniciar la Aplicación

### Opción 1: Scripts Automáticos (Windows)

1. **Iniciar el Backend**:
   - Doble clic en `start_backend.bat`
   - O ejecuta: `.\start_backend.ps1` en PowerShell
   - El backend estará en: http://localhost:8000

2. **Iniciar el Frontend** (en otra terminal):
   - Doble clic en `start_frontend.bat`
   - O ejecuta: `.\start_frontend.ps1` en PowerShell
   - El frontend se abrirá automáticamente en: http://localhost:3000

### Opción 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Verificar que Todo Funciona

### 1. Probar el Backend

Ejecuta el script de prueba:
```bash
cd backend
python test_api.py
```

O visita en tu navegador:
- API Docs: http://localhost:8000/docs
- Endpoint raíz: http://localhost:8000/

### 2. Probar el Frontend

Abre http://localhost:3000 en tu navegador:
1. Haz clic en "📍 Mi Ubicación"
2. Permite el acceso a tu ubicación cuando el navegador lo solicite
3. Verás supermercados cercanos en el mapa
4. Ajusta el radio de búsqueda con el slider

## Estructura de Archivos Creados

```
geo_supermercado/
├── backend/
│   ├── app/
│   │   ├── main.py          # ✅ API FastAPI
│   │   ├── database.py      # ✅ Configuración BD
│   │   ├── models.py        # ✅ Modelos SQLAlchemy
│   │   ├── schemas.py       # ✅ Schemas Pydantic
│   │   ├── crud.py          # ✅ Operaciones CRUD
│   │   └── utils.py         # ✅ Cálculo de distancias
│   ├── populate_db.py       # ✅ Poblar BD con datos
│   ├── test_api.py          # ✅ Script de pruebas
│   ├── requirements.txt     # ✅ Dependencias Python
│   └── supermercado.db      # ✅ Base de datos SQLite
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Mapa.jsx     # ✅ Componente de mapa
│   │   ├── services/
│   │   │   └── api.js       # ✅ Cliente API
│   │   ├── App.jsx          # ✅ Aplicación principal
│   │   ├── App.css          # ✅ Estilos
│   │   └── main.jsx         # ✅ Entry point
│   ├── index.html           # ✅ HTML principal
│   ├── package.json         # ✅ Dependencias Node
│   └── vite.config.js       # ✅ Configuración Vite
│
├── start_backend.bat        # ✅ Script inicio backend
├── start_frontend.bat       # ✅ Script inicio frontend
├── .gitignore              # ✅ Git ignore
└── README.md               # ✅ Documentación
```

## Funcionalidades Implementadas

### Módulo 1: Supermercados Cercanos ✅

- ✅ Backend API con FastAPI
- ✅ Base de datos SQLite con 15 supermercados en Santiago
- ✅ Cálculo de distancias con fórmula de Haversine
- ✅ Endpoint para buscar supermercados cercanos
- ✅ Frontend React con Vite
- ✅ Mapa interactivo con Leaflet
- ✅ Geolocalización del usuario
- ✅ Búsqueda por radio ajustable
- ✅ Lista de supermercados con distancias
- ✅ Diseño responsivo para móviles

## Endpoints de la API

### Supermercados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/supermercados` | Lista todos los supermercados |
| GET | `/api/supermercados/cercanos?lat={lat}&lng={lng}&radio={km}` | Supermercados cercanos |
| GET | `/api/supermercados/{id}` | Obtener por ID |
| POST | `/api/supermercados` | Crear nuevo |

### Productos (para siguiente módulo)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/productos` | Lista todos los productos |
| GET | `/api/productos/buscar?q={termino}` | Buscar productos |
| POST | `/api/productos` | Crear nuevo |

## Próximos Pasos

### Módulo 2: Comparación de Precios (Pendiente)

- [ ] Poblar BD con productos y precios
- [ ] Componente de lista de compras
- [ ] Búsqueda inteligente de productos
- [ ] Comparación de precios entre supermercados
- [ ] Destacar producto más barato
- [ ] Cálculo de ahorro potencial

## Solución de Problemas

### El backend no inicia
```bash
# Verifica que las dependencias estén instaladas
cd backend
pip install -r requirements.txt
```

### El frontend no inicia
```bash
# Reinstala dependencias
cd frontend
rm -rf node_modules
npm install
```

### No se ven supermercados en el mapa
1. Verifica que el backend esté corriendo en http://localhost:8000
2. Abre la consola del navegador (F12) y busca errores
3. Verifica que la base de datos tenga datos:
   ```bash
   cd backend
   python populate_db.py
   ```

### Error de CORS
- El backend ya tiene CORS configurado para desarrollo
- Si persiste, verifica que el frontend llame a `http://localhost:8000`

## Datos de Prueba

La base de datos incluye 15 supermercados en Santiago:
- Lider (4 sucursales)
- Jumbo (4 sucursales)
- Unimarc (2 sucursales)
- Santa Isabel (2 sucursales)
- Tottus (2 sucursales)

Ubicados en: Providencia, Las Condes, Vitacura, Santiago Centro, La Florida, Maipú, Huechuraba, Ñuñoa, Peñalolén.

## Contacto

Para reportar problemas o sugerencias, abre un issue en el repositorio.
