import { useState, useEffect, useCallback } from 'react';
import Mapa from './components/Mapa';
import BuscadorDireccion from './components/BuscadorDireccion';
import { supermercadoService } from './services/api';
import { agregarDistancias, ordenarPorDistancia } from './utils/distancia';
import './App.css';

function App() {
  const [supermercados, setSupermercados] = useState([]);
  const [ubicacionUsuario, setUbicacionUsuario] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [direccionBuscada, setDireccionBuscada] = useState(null);
  const [mapBounds, setMapBounds] = useState(null);

  // Carga supermercados usando los bounds actuales o unos pasados como override
  // Carga supermercados usando los bounds actuales o unos pasados como override
  // opcionalmente acepta una ubicacionReferencia para calcular distancias inmediatamente
  const cargarSupermercadosPorBounds = async (boundsOverride = null, ubicacionReferencia = null) => {
    const boundsToUse = boundsOverride || mapBounds;
    if (!boundsToUse) return;

    setLoading(true);
    setError(null);
    try {
      const { latMin, latMax, lngMin, lngMax } = boundsToUse;
      let data = await supermercadoService.getPorBounds(latMin, latMax, lngMin, lngMax);

      const referencia = ubicacionReferencia || ubicacionUsuario;
      // Si hay una ubicación de referencia, calcular distancias y ordenar
      if (referencia) {
        data = agregarDistancias(data, referencia);
        data = ordenarPorDistancia(data);
      }

      setSupermercados(data);
      setError(null);
    } catch (err) {
      console.error('Error cargando supermercados:', err);
      setError('Error al cargar los supermercados');
      setSupermercados([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUbicacionChange = (nuevaUbicacion) => {
    setUbicacionUsuario(nuevaUbicacion);
  };

  const handleBoundsChange = useCallback((bounds) => {
    setMapBounds(bounds);
  }, []);

  // ubicacion: [lat, lng]
  // bbox: optional array [south, north, west, east] from Nominatim
  const handleDireccionSeleccionada = (ubicacion, nombreDireccion, bbox = null) => {
    setUbicacionUsuario(ubicacion);
    setDireccionBuscada(nombreDireccion);

    // Si se proporciona bbox, convertir a los nombres usados por la API y usarlo
    if (bbox && bbox.length === 4) {
      const [south, north, west, east] = bbox.map(Number);
      const boundsOverride = {
        latMin: south,
        latMax: north,
        lngMin: west,
        lngMax: east,
      };

      // Cargar supermercados usando los bounds del resultado
      setTimeout(() => {
        cargarSupermercadosPorBounds(boundsOverride, ubicacion);
      }, 300);
      return;
    }

    // Si no hay bbox, esperar a que el mapa centre y use los bounds actuales
    setTimeout(() => {
      cargarSupermercadosPorBounds(null, ubicacion);
    }, 300);
  };

  const handleBuscarEnArea = () => {
    cargarSupermercadosPorBounds();
  };

  const handleMapClick = (ubicacion) => {
    handleUbicacionChange(ubicacion);
    // Cargar supermercados automáticamente al hacer clic en el mapa
    setTimeout(() => {
      cargarSupermercadosPorBounds(null, ubicacion);
    }, 300);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🛒 Geo Supermercado</h1>
        <p className="subtitle">Encuentra los supermercados más cercanos en Chile</p>
      </header>

      <main className="app-main">
        {/* Buscador de dirección */}
        <BuscadorDireccion onDireccionSeleccionada={handleDireccionSeleccionada} />

        {/* Mostrar dirección buscada */}
        {direccionBuscada && (
          <div className="alert alert-info">
            📍 Punto de referencia: <strong>{direccionBuscada}</strong>
            <br />
            <small>Las distancias se calculan desde este punto</small>
          </div>
        )}

        {/* Mostrar ubicación GPS como referencia */}
        {ubicacionUsuario && !direccionBuscada && (
          <div className="alert alert-info">
            📍 Mostrando distancias desde tu ubicación seleccionada
          </div>
        )}

        {/* Botón para buscar supermercados en el área visible */}
        {mapBounds && (
          <div className="controls">
            <button 
              onClick={handleBuscarEnArea}
              disabled={loading}
              className="btn-buscar-area"
            >
              {loading ? '🔍 Buscando...' : '🔍 Buscar Supermercados en Esta Área'}
            </button>
            <p className="info-text">
              💡 También puedes buscar una dirección arriba, hacer clic en el mapa, o usar "Ir a Mi Ubicación" para cargar supermercados automáticamente
            </p>
          </div>
        )}

        {/* Mensaje de error */}
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {/* Mapa */}
        <Mapa 
          supermercados={supermercados}
          ubicacionUsuario={ubicacionUsuario}
          onUbicacionChange={handleUbicacionChange}
          onBoundsChange={handleBoundsChange}
          onMapClickCallback={handleMapClick}
        />
      </main>

      <footer className="app-footer">
        <p>Geo Supermercado v1.0 - Comparador de precios en Chile</p>
      </footer>
    </div>
  );
}

export default App;
