import { useState, useEffect, useRef } from 'react';

export default function BuscadorDireccion({ onDireccionSeleccionada }) {
  const [busqueda, setBusqueda] = useState('');
  const [resultados, setResultados] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mostrarResultados, setMostrarResultados] = useState(false);
  const timeoutRef = useRef(null);
  const ignorarBusquedaRef = useRef(false);

  // Función para buscar dirección
  const buscarDireccion = async (query) => {
    if (!query.trim() || query.trim().length < 3) {
      setResultados([]);
      setMostrarResultados(false);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Usar Nominatim API de OpenStreetMap para geocodificación
      // Agregar "Chile" a la búsqueda para mejores resultados
      const searchQuery = query.includes('Chile') ? query : `${query}, Chile`;
      const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchQuery)}&format=json&limit=5&countrycodes=cl&addressdetails=1`;
      
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'GeoSupermercado/1.0'
        }
      });

      if (!response.ok) {
        throw new Error('Error al buscar la dirección');
      }

      const data = await response.json();
      
      if (data.length === 0) {
        setError('No se encontraron resultados.');
        setResultados([]);
        setMostrarResultados(false);
      } else {
        setResultados(data);
        setMostrarResultados(true);
        setError(null);
      }
    } catch (err) {
      console.error('Error en búsqueda:', err);
      setError('Error al buscar la dirección.');
      setResultados([]);
      setMostrarResultados(false);
    } finally {
      setLoading(false);
    }
  };

  // Efecto para búsqueda automática con debounce
  useEffect(() => {
    // Si se debe ignorar esta búsqueda (porque se seleccionó un resultado)
    if (ignorarBusquedaRef.current) {
      ignorarBusquedaRef.current = false;
      return;
    }

    // Limpiar timeout anterior
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Si el campo está vacío, limpiar resultados
    if (!busqueda.trim()) {
      setResultados([]);
      setMostrarResultados(false);
      setError(null);
      setLoading(false);
      return;
    }

    // Esperar 500ms después de que el usuario deje de escribir
    timeoutRef.current = setTimeout(() => {
      buscarDireccion(busqueda);
    }, 500);

    // Cleanup
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [busqueda]);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Buscar inmediatamente al presionar Enter
    if (busqueda.trim().length >= 3) {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      buscarDireccion(busqueda);
    }
  };

  const seleccionarDireccion = (resultado) => {
    const lat = parseFloat(resultado.lat);
    const lng = parseFloat(resultado.lon);
    
    // Formatear el nombre de la dirección
    const direccion = resultado.display_name;
    
    // Limpiar timeout pendiente para evitar búsquedas adicionales
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    // Marcar para ignorar el siguiente useEffect
    ignorarBusquedaRef.current = true;
    
    // Limpiar y cerrar primero
    setMostrarResultados(false);
    setResultados([]);
    setError(null);
    setBusqueda(resultado.display_name.split(',')[0]);
    
    // Llamar al callback con la ubicación y boundingbox (si existe)
    // Nominatim devuelve boundingbox como [south, north, west, east]
    const bbox = resultado.boundingbox || null;
    onDireccionSeleccionada([lat, lng], direccion, bbox);
  };

  const limpiarBusqueda = () => {
    setBusqueda('');
    setResultados([]);
    setError(null);
    setMostrarResultados(false);
  };

  return (
    <div className="buscador-direccion">
      <form onSubmit={handleSubmit} className="buscador-form">
        <div className="input-group">
          <input
            type="text"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            placeholder="Buscar ciudad o dirección en Chile..."
            className="input-busqueda"
            disabled={loading}
          />
          {loading && (
            <div className="loading-indicator">
              <div className="mini-spinner"></div>
            </div>
          )}
          {busqueda && !loading && (
            <button
              type="button"
              onClick={limpiarBusqueda}
              className="btn-limpiar"
              title="Limpiar"
            >
              ✕
            </button>
          )}
        </div>
      </form>

      {error && (
        <div className="alert alert-warning-small">
          {error}
        </div>
      )}

      {mostrarResultados && resultados.length > 0 && (
        <div className="resultados-busqueda">
          <h4>Resultados de búsqueda:</h4>
          <ul className="lista-resultados">
            {resultados.map((resultado, index) => (
              <li
                key={index}
                onClick={() => seleccionarDireccion(resultado)}
                className="resultado-item"
              >
                <div className="resultado-nombre">
                  {resultado.display_name}
                </div>
                <div className="resultado-tipo">
                  {resultado.type === 'city' && '🏙️ Ciudad'}
                  {resultado.type === 'town' && '🏘️ Pueblo'}
                  {resultado.type === 'village' && '🏡 Villa'}
                  {resultado.type === 'administrative' && '📍 Región'}
                  {!['city', 'town', 'village', 'administrative'].includes(resultado.type) && '📍 Lugar'}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
