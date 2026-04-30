import { useState, useEffect } from 'react';
import Mapa from './components/Mapa';
import { supermercadoService } from './services/api';
import './App.css';

function App() {
  const [supermercados, setSupermercados] = useState([]);
  const [ubicacionUsuario, setUbicacionUsuario] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [radio, setRadio] = useState(10); // Radio de búsqueda en km

  // Cargar supermercados cercanos cuando cambia la ubicación
  useEffect(() => {
    if (ubicacionUsuario) {
      cargarSupermercadosCercanos();
    } else {
      // Cargar todos los supermercados si no hay ubicación
      cargarTodosSupermercados();
    }
  }, [ubicacionUsuario, radio]);

  const cargarTodosSupermercados = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await supermercadoService.getAll();
      setSupermercados(data);
    } catch (err) {
      console.error('Error cargando supermercados:', err);
      setError('Error al cargar los supermercados');
    } finally {
      setLoading(false);
    }
  };

  const cargarSupermercadosCercanos = async () => {
    if (!ubicacionUsuario) return;

    setLoading(true);
    setError(null);
    try {
      const [lat, lng] = ubicacionUsuario;
      const data = await supermercadoService.getCercanos(lat, lng, radio);
      setSupermercados(data);
    } catch (err) {
      console.error('Error cargando supermercados cercanos:', err);
      if (err.response?.status === 404) {
        setError(`No se encontraron supermercados en un radio de ${radio} km`);
        setSupermercados([]);
      } else {
        setError('Error al cargar los supermercados cercanos');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUbicacionChange = (nuevaUbicacion) => {
    setUbicacionUsuario(nuevaUbicacion);
  };

  const handleRadioChange = (e) => {
    setRadio(Number(e.target.value));
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🛒 Geo Supermercado</h1>
        <p className="subtitle">Encuentra los supermercados más cercanos en Chile</p>
      </header>

      <main className="app-main">
        {/* Control de radio de búsqueda */}
        {ubicacionUsuario && (
          <div className="controls">
            <label htmlFor="radio-busqueda">
              Radio de búsqueda: <strong>{radio} km</strong>
            </label>
            <input 
              id="radio-busqueda"
              type="range" 
              min="1" 
              max="50" 
              value={radio}
              onChange={handleRadioChange}
              className="slider"
            />
            <div className="radio-labels">
              <span>1 km</span>
              <span>50 km</span>
            </div>
          </div>
        )}

        {/* Mensaje de error */}
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {/* Loading spinner */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Cargando supermercados...</p>
          </div>
        )}

        {/* Mapa */}
        {!loading && (
          <Mapa 
            supermercados={supermercados}
            ubicacionUsuario={ubicacionUsuario}
            onUbicacionChange={handleUbicacionChange}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>Geo Supermercado v1.0 - Comparador de precios en Chile</p>
      </footer>
    </div>
  );
}

export default App;
