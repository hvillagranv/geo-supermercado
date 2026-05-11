/**
 * Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine
 * @param {number} lat1 - Latitud del primer punto
 * @param {number} lng1 - Longitud del primer punto
 * @param {number} lat2 - Latitud del segundo punto
 * @param {number} lng2 - Longitud del segundo punto
 * @returns {number} Distancia en kilómetros
 */
export function calcularDistancia(lat1, lng1, lat2, lng2) {
  const R = 6371; // Radio de la Tierra en kilómetros
  
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distancia = R * c;
  
  return distancia;
}

/**
 * Convierte grados a radianes
 * @param {number} grados 
 * @returns {number} Radianes
 */
function toRad(grados) {
  return grados * (Math.PI / 180);
}

/**
 * Agrega distancias a un array de supermercados desde un punto de referencia
 * @param {Array} supermercados - Array de supermercados
 * @param {Array} ubicacionReferencia - [lat, lng] del punto de referencia
 * @returns {Array} Array de supermercados con distancia agregada
 */
export function agregarDistancias(supermercados, ubicacionReferencia) {
  if (!ubicacionReferencia) {
    return supermercados;
  }

  const [latRef, lngRef] = ubicacionReferencia;

  return supermercados.map(super_obj => ({
    ...super_obj,
    distancia: calcularDistancia(
      latRef,
      lngRef,
      super_obj.latitud,
      super_obj.longitud
    )
  }));
}

/**
 * Ordena supermercados por distancia (menor a mayor)
 * @param {Array} supermercados - Array de supermercados con distancia
 * @returns {Array} Array ordenado por distancia
 */
export function ordenarPorDistancia(supermercados) {
  return [...supermercados].sort((a, b) => {
    if (!a.distancia) return 1;
    if (!b.distancia) return -1;
    return a.distancia - b.distancia;
  });
}
