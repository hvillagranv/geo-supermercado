import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Endpoints de supermercados
export const supermercadoService = {
  // Obtener todos los supermercados
  getAll: async () => {
    const response = await api.get('/supermercados');
    return response.data;
  },

  // Obtener supermercados cercanos
  getCercanos: async (lat, lng, radio = 10, limit = 20) => {
    const response = await api.get('/supermercados/cercanos', {
      params: { lat, lng, radio, limit }
    });
    return response.data;
  },

  // Obtener un supermercado por ID
  getById: async (id) => {
    const response = await api.get(`/supermercados/${id}`);
    return response.data;
  },
};

// Endpoints de productos
export const productoService = {
  // Obtener todos los productos
  getAll: async () => {
    const response = await api.get('/productos');
    return response.data;
  },

  // Buscar productos
  buscar: async (termino) => {
    const response = await api.get('/productos/buscar', {
      params: { q: termino }
    });
    return response.data;
  },
};
