import { useState, useEffect } from 'react';
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

// Componente para centrar el mapa en la ubicación del usuario
function CenterMap({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.setView(center, 13);
    }
  }, [center, map]);
  return null;
}

export default function Mapa({ supermercados, ubicacionUsuario, onUbicacionChange }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [clickedLocation, setClickedLocation] = useState(null);
  const [isManualLocation, setIsManualLocation] = useState(false);

  // Centro por defecto (Santiago, Plaza de Armas)
  const defaultCenter = [-33.4372, -70.6506];
  const center = ubicacionUsuario || defaultCenter;

  // Manejar click en el mapa
  const handleMapClick = (latlng) => {
    setClickedLocation(latlng);
    setIsManualLocation(true);
    onUbicacionChange(latlng);
    setError(null);
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
        setClickedLocation(null);
        setIsManualLocation(false);
        onUbicacionChange([latitude, longitude]);
        setLoading(false);
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
        <h2>Supermercados Cercanos</h2>
        <div className="btn-group">
          <button 
            onClick={obtenerUbicacion} 
            disabled={loading}
            className="btn-ubicacion"
          >
            {loading ? 'Obteniendo ubicación...' : '📍 Mi Ubicación GPS'}
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
          💡 Haz clic en "Mi Ubicación GPS" o haz clic en cualquier punto del mapa para buscar supermercados
        </div>
      )}

      {isManualLocation && (
        <div className="alert alert-success">
          ✓ Ubicación seleccionada en el mapa. Haz clic en otro punto para cambiar o usa "Resetear" para volver a tu ubicación GPS.
        </div>
      )}

      {error && (
        <div className="alert alert-warning">
          {error}
        </div>
      )}

      <MapContainer 
        center={center} 
        zoom={13} 
        style={{ height: '500px', width: '100%', borderRadius: '8px', cursor: 'crosshair' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <CenterMap center={ubicacionUsuario} />
        <MapClickHandler onMapClick={handleMapClick} />

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
            {supermercados.map((super_obj) => (
              <div key={super_obj.id} className="supermercado-card">
                <div className="card-header">
                  <h4>{super_obj.nombre}</h4>
                  {super_obj.distancia && (
                    <span className="badge">{super_obj.distancia.toFixed(2)} km</span>
                  )}
                </div>
                <p className="direccion">{super_obj.direccion}, {super_obj.comuna}</p>
                {super_obj.telefono && (
                  <p className="telefono">📞 {super_obj.telefono}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
