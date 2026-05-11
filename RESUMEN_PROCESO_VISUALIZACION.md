# Resumen del Proceso, Herramientas y Visualización

Fecha: 11 de Mayo 2026

## Resumen ejecutivo

Este proyecto proporciona una aplicación web para localizar y comparar supermercados en Chile. Se compone de un backend en FastAPI que expone una API REST y un frontend en React que muestra un mapa interactivo (Leaflet). La funcionalidad principal permite buscar una dirección, seleccionar un punto en el mapa o usar la ubicación GPS, y ver todos los supermercados dentro del área visible del mapa, incluyendo la distancia desde el punto de referencia.

## Herramientas y stack

- Backend: Python, FastAPI, SQLAlchemy, SQLite (archivo `supermercado.db`)
- Frontend: React (Vite), Leaflet (react-leaflet) para mapas
- APIs externas: Nominatim (OpenStreetMap) para geocodificación en el buscador; Google Places fue usado para la extracción inicial de datos
- Utilidades: Haversine para cálculo de distancias (implementado en frontend y backend)

## Flujo principal implementado

1. El usuario busca una dirección en el cuadro de búsqueda (autocompletado con Nominatim).
2. Al seleccionar un resultado, la app centra el mapa en esa ubicación y usa el bounding box (si Nominatim lo devuelve) o los bounds visibles del mapa para consultar al backend.
3. El backend responde con todos los supermercados dentro de esos bounds (`/api/supermercados/bounds`).
4. El frontend calcula la distancia desde el punto de referencia (punto seleccionado, clic del mapa o GPS) para cada supermercado usando Haversine, ordena los resultados por distancia y los visualiza:
   - marcadores en el mapa (con popup)
   - lista de tarjetas con badge de distancia

## Endpoints clave

- `GET /api/supermercados` — lista todos los supermercados
- `GET /api/supermercados/bounds?lat_min={}&lat_max={}&lng_min={}&lng_max={}` — supermercados en área
- `GET /api/supermercados/cercanos?lat={}&lng={}&radio={}` — (legacy) búsqueda por radio

## Visualización y UX

- Mapa interactivo con marcadores por supermercado
- Popups en marcadores que muestran nombre, dirección y distancia (si hay punto de referencia)
- Lista lateral con tarjetas ordenadas por distancia
- Buscador de direcciones que: busca mientras se escribe (debounce), ofrece resultados y permite seleccionar (un solo clic) — al seleccionar carga y centra el mapa
- Acciones que gatillan la carga automática de supermercados:
  - seleccionar un resultado en el buscador
  - hacer clic en el mapa
  - usar "Ir a Mi Ubicación"
  - (opcional) botón "Buscar Supermercados en Esta Área" para recargar manualmente

## Notas de implementación importantes

- La búsqueda automática por movimiento del mapa fue deshabilitada para evitar ciclos de carga. Se usa un botón o acciones explícitas del usuario para disparar la carga.
- El cálculo de distancia se hace en frontend para evitar peticiones adicionales al backend; la lógica está en `frontend/src/utils/distancia.js`.
- El backend incluye un endpoint eficiente que filtra por lat/lng bounds (consulta SQL con rangos).

## Archivos relevantes

- backend/app/main.py — definición de endpoints
- backend/app/crud.py — get_supermercados_por_bounds
- frontend/src/components/Mapa.jsx — manejo de mapa, clicks y bounds
- frontend/src/components/BuscadorDireccion.jsx — búsqueda con Nominatim
- frontend/src/utils/distancia.js — cálculos Haversine y utilidades
- frontend/src/services/api.js — cliente axios hacia la API

## Recomendaciones

- Mantener la extracción periódica de Google Places para actualizar datos (script en `backend/`)
- Considerar paginación o límite por bounds en áreas muy densas para evitar saturar el frontend
- Añadir tests end-to-end (Playwright / Cypress) para flujos: búsqueda, selección, cálculo de distancias

---

Archivo generado automáticamente para proporcionar contexto técnico y de UX.
