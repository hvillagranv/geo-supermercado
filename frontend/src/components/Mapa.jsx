import { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix para los iconos de Leaflet en React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Icono personalizado para el usuario
const userIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Icono para supermercados
const superIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Icono para ubicación temporal (click en el mapa)
const tempIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Componente para manejar clicks en el mapa
function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick([e.latlng.lat, e.latlng.lng]);
    },
  });
  return null;
}

// Componente para detectar cambios de bounds (zoom y movimiento)
function MapBoundsHandler({ onBoundsChange }) {
  const map = useMap();
  const boundsRef = useRef(null);

  useEffect(() => {
    const updateBounds = () => {
      const bounds = map.getBounds();
      const boundsData = {
        latMin: bounds.getSouth(),
        latMax: bounds.getNorth(),
        lngMin: bounds.getWest(),
        lngMax: bounds.getEast(),
      };
      
      // Solo actualizar si los bounds han cambiado significativamente
      const boundsString = JSON.stringify(boundsData);
      if (boundsRef.current !== boundsString) {
        boundsRef.current = boundsString;
        onBoundsChange(boundsData);
      }
    };

    // Actualizar bounds cuando el mapa termina de moverse
    map.on('moveend', updateBounds);

    // Actualizar bounds inicial
    updateBounds();

    // Cleanup
    return () => {
      map.off('moveend', updateBounds);
    };
  }, [map, onBoundsChange]);

  return null;
}


// Componente para centrar el mapa SOLO cuando se solicita explícitamente
// triggerCenter es un número que se incrementa cada vez que queremos centrar
function CenterMap({ center, triggerCenter }) {
  const map = useMap();
  const lastTriggerRef = useRef(null);
  useEffect(() => {
    if (!center) return;
    if (triggerCenter === lastTriggerRef.current) return; // No re-centrar si el trigger no cambió
    
    lastTriggerRef.current = triggerCenter;
    map.setView(center, 13);
  }, [center, triggerCenter, map]);
  return null;
}

function SelectedSuperCenter({ selected }) {
  const map = useMap();
  const lastRef = useRef(null);
  useEffect(() => {
    if (!selected) return;
    if (lastRef.current === selected.id) return;
    lastRef.current = selected.id;
    // fly to the supermercado once, do not change ubicacionUsuario
    map.flyTo([selected.latitud, selected.longitud], 15, { duration: 0.8 });
  }, [selected, map]);
  return null;
}

export default function Mapa({ supermercados, ubicacionUsuario, onUbicacionChange, onBoundsChange, onMapClickCallback, selectedSupermercado, onSelectSupermercado, centerTrigger, comunaReferencia }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [clickedLocation, setClickedLocation] = useState(null);
  const [isManualLocation, setIsManualLocation] = useState(false);

  // Centro por defecto (Santiago, Plaza de Armas)
  const defaultCenter = [-33.4372, -70.6506];

  // Mantener una referencia estable para el prop `center` que se pasa a MapContainer.
  // Evita que re-renders normales (por ejemplo seleccionar un supermercado) re-centren el mapa
  const centerRef = useRef(ubicacionUsuario || defaultCenter);
  useEffect(() => {
    if (ubicacionUsuario && (
      !centerRef.current || Math.abs(centerRef.current[0] - ubicacionUsuario[0]) > 1e-6 || Math.abs(centerRef.current[1] - ubicacionUsuario[1]) > 1e-6
    )) {
      centerRef.current = ubicacionUsuario;
    }
    // No actualizamos centerRef cuando no hay ubicacionUsuario para mantener el centro inicial estable
  }, [ubicacionUsuario]);

  // Manejar click en el mapa
  const handleMapClick = (latlng) => {
    setClickedLocation(latlng);
    setIsManualLocation(true);
    onUbicacionChange(latlng); // Esto ya incrementa centerTrigger en App
    setError(null);
    // Llamar al callback del padre si existe
    if (onMapClickCallback) {
      onMapClickCallback(latlng);
    }
  };

  // Resetear a ubicación GPS del usuario
  const resetToUserLocation = () => {
    setClickedLocation(null);
    setIsManualLocation(false);
    obtenerUbicacion();
  };

  // Obtener ubicación del usuario
  const obtenerUbicacion = () => {
    setLoading(true);
    setError(null);

    if (!navigator.geolocation) {
      setError('Geolocalización no soportada por tu navegador');
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const ubicacion = [latitude, longitude];
        setClickedLocation(null);
        setIsManualLocation(false);
        onUbicacionChange(ubicacion); // Esto ya incrementa centerTrigger en App
        setLoading(false);
        // Llamar al callback para cargar supermercados
        if (onMapClickCallback) {
          setTimeout(() => {
            onMapClickCallback(ubicacion);
          }, 300);
        }
      },
      (error) => {
        console.error('Error obteniendo ubicación:', error);
        setError('No se pudo obtener tu ubicación. Haz click en el mapa para seleccionar una ubicación.');
        setLoading(false);
      }
    );
  };

  return (
    <div className="mapa-container">
      <div className="mapa-header">
        <h2>Supermercados en el Mapa</h2>
        <div className="btn-group">
          <button 
            onClick={obtenerUbicacion} 
            disabled={loading}
            className="btn-ubicacion"
          >
            {loading ? 'Obteniendo ubicación...' : '📍 Ir a Mi Ubicación'}
          </button>
          {isManualLocation && (
            <button 
              onClick={resetToUserLocation}
              className="btn-reset"
              title="Volver a ubicación GPS"
            >
              🔄 Resetear
            </button>
          )}
        </div>
      </div>

      {/* Instrucción de uso */}
      {!ubicacionUsuario && !loading && (
        <div className="alert alert-info">
          💡 Busca una dirección arriba, haz clic en "Ir a Mi Ubicación", o haz clic en cualquier punto del mapa para ver supermercados cercanos
        </div>
      )}

      {isManualLocation && (
        <div className="alert alert-success">
          ✓ Ubicación seleccionada en el mapa. Mueve el mapa o haz zoom para ver más supermercados.
        </div>
      )}

      {error && (
        <div className="alert alert-warning">
          {error}
        </div>
      )}

      <MapContainer 
        center={centerRef.current}
        zoom={13} 
        style={{ height: '500px', width: '100%', borderRadius: '8px', cursor: 'crosshair' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <CenterMap center={ubicacionUsuario} triggerCenter={centerTrigger} />
        <MapClickHandler onMapClick={handleMapClick} />
        <MapBoundsHandler onBoundsChange={onBoundsChange} />
        {/* No centrar automáticamente al seleccionar un supermercado (opción A).
            SelectedSuperCenter exists but is intentionally not rendered to avoid
            changing the map view and blocking user panning. */}

        {/* Marcador de ubicación del usuario (GPS) */}
        {ubicacionUsuario && !isManualLocation && (
          <Marker position={ubicacionUsuario} icon={userIcon}>
            <Popup>
              <strong>Tu ubicación GPS</strong>
            </Popup>
          </Marker>
        )}

        {/* Marcador de ubicación seleccionada manualmente */}
        {clickedLocation && isManualLocation && (
          <Marker position={clickedLocation} icon={tempIcon}>
            <Popup>
              <strong>Ubicación seleccionada</strong>
              <br />
              <small>Click en el mapa para cambiar</small>
            </Popup>
          </Marker>
        )}

        {/* Marcadores de supermercados */}
        {supermercados.map((super_obj) => (
          <Marker 
            key={super_obj.id} 
            position={[super_obj.latitud, super_obj.longitud]}
            icon={superIcon}
            eventHandlers={{
              click: (e) => {
                // Evitar que el click en el marker se propague al mapa
                // (mapa tiene un handler global de click que cambia la ubicacion de referencia)
                try { e.originalEvent && e.originalEvent.stopPropagation(); } catch (_) {}
                // Seleccionar supermercado pero NO cambiar la ubicacionUsuario
                if (onSelectSupermercado) onSelectSupermercado(super_obj);
              }
            }}
          >
            <Popup>
              <div className="popup-content">
                <h3>{super_obj.nombre}</h3>
                <p><strong>Dirección:</strong> {super_obj.direccion}</p>
                <p><strong>Comuna:</strong> {super_obj.comuna}</p>
                {super_obj.distancia && (
                  <p><strong>Distancia:</strong> {super_obj.distancia.toFixed(2)} km</p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Lista de supermercados */}
      {supermercados.length > 0 && (
        <div className="lista-supermercados">
          <h3>Lista de Supermercados ({supermercados.length})</h3>
          <div className="supermercados-grid">
        {supermercados.map((super_obj) => {
          // Verificar si está en la misma comuna que la referencia
          const mismaComuna = comunaReferencia && super_obj.comuna === comunaReferencia;
          const cardClass = mismaComuna ? "supermercado-card misma-comuna" : "supermercado-card";
          
          return (
            <div key={super_obj.id} className={cardClass} onClick={() => onSelectSupermercado && onSelectSupermercado(super_obj)}>
                <div className="card-header">
                  <h4>{super_obj.nombre}</h4>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    {mismaComuna && (
                      <span className="badge badge-comuna">📍 Misma comuna</span>
                    )}
                    {super_obj.distancia && (
                      <span className="badge">{super_obj.distancia.toFixed(2)} km</span>
                    )}
                  </div>
                </div>
                <p className="direccion">{super_obj.direccion}, {super_obj.comuna}</p>
                {super_obj.telefono && (
                  <p className="telefono">📞 {super_obj.telefono}</p>
                )}
              </div>
          );
        })}
          </div>
        </div>
      )}
    </div>
  );
}
