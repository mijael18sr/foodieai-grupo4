/**
 * Página de prueba para verificar la integración de distritos
 * Muestra todas las funcionalidades del sistema de distritos
 */
import React, { useState } from 'react';
import { useDistricts } from '../hooks';
import { DistrictSelector } from '../components';
import type { District } from '../services/districtService';

export const DistrictTestPage: React.FC = () => {
  const {
    districts,
    loading,
    error,
    statistics,
    selectedDistrict,
    getDistrictInfo,
    getRecommendedDistricts,
    selectDistrict,
    clearSelection
  } = useDistricts();

  const [districtInfo, setDistrictInfo] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<District[]>([]);
  const [manualSelection, setManualSelection] = useState('');

  const handleGetDistrictInfo = async (districtName: string) => {
    try {
      const info = await getDistrictInfo(districtName);
      setDistrictInfo(info);
    } catch (err) {
      console.error('Error al obtener información:', err);
      setDistrictInfo(null);
    }
  };

  const handleGetRecommendations = async () => {
    const recs = await getRecommendedDistricts({
      touristZoneOnly: true,
      minRating: 4.0,
      limit: 3
    });
    setRecommendations(recs);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🏛️ Sistema de Gestión de Distritos de Lima
          </h1>
          <p className="text-gray-600 mb-8">
            Página de prueba para verificar la integración frontend-backend
          </p>

          {/* Estado general */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-2">Estado de Carga</h3>
              <p className="text-blue-700">
                {loading ? '🔄 Cargando...' : '✅ Datos cargados'}
              </p>
              {error && (
                <p className="text-red-600 text-sm mt-1">❌ {error}</p>
              )}
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-semibold text-green-900 mb-2">Distritos Disponibles</h3>
              <p className="text-green-700 text-2xl font-bold">{districts.length}</p>
              <p className="text-green-600 text-sm">
                {districts.filter(d => d.is_tourist_zone).length} zonas turísticas
              </p>
            </div>

            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-semibold text-purple-900 mb-2">Total Restaurantes</h3>
              <p className="text-purple-700 text-2xl font-bold">
                {statistics?.total_restaurants || 'N/A'}
              </p>
              <p className="text-purple-600 text-sm">
                Promedio: {statistics?.avg_restaurants_per_district || 'N/A'} por distrito
              </p>
            </div>
          </div>

          {/* Selector de distritos avanzado */}
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              🎯 Selector Avanzado de Distritos
            </h2>
            <div className="max-w-md">
              <DistrictSelector
                selectedDistrict={manualSelection}
                onDistrictChange={setManualSelection}
                showStatistics={true}
                allowSearch={true}
                placeholder="Selecciona un distrito para probar..."
              />
            </div>
          </div>

          {/* Lista de distritos */}
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              📍 Lista Completa de Distritos
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {districts.map((district) => (
                <div
                  key={district.value}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    selectedDistrict?.value === district.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-blue-300'
                  }`}
                  onClick={() => selectDistrict(district.value)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                      {district.label}
                      {district.is_tourist_zone && <span>🏛️</span>}
                    </h3>
                  </div>
                  
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>🍽️ {district.restaurant_count} restaurantes</p>
                    {district.average_rating && (
                      <p>⭐ {district.average_rating.toFixed(2)} rating promedio</p>
                    )}
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleGetDistrictInfo(district.value);
                    }}
                    className="mt-3 text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Ver detalles →
                  </button>
                </div>
              ))}
            </div>

            {selectedDistrict && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">
                  Distrito Seleccionado: {selectedDistrict.label}
                </h4>
                <p className="text-blue-700">{selectedDistrict.description}</p>
                <button
                  onClick={clearSelection}
                  className="mt-2 text-blue-600 hover:text-blue-800 text-sm"
                >
                  Limpiar selección
                </button>
              </div>
            )}
          </div>

          {/* Información detallada */}
          {districtInfo && (
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                📊 Información Detallada
              </h2>
              <div className="bg-gray-50 p-6 rounded-lg">
                <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                  {JSON.stringify(districtInfo, null, 2)}
                </pre>
              </div>
            </div>
          )}

          {/* Botones de prueba */}
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              🧪 Pruebas de API
            </h2>
            <div className="flex flex-wrap gap-4">
              <button
                onClick={handleGetRecommendations}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Obtener Recomendaciones (Zonas Turísticas)
              </button>
              
              <button
                onClick={() => handleGetDistrictInfo('Miraflores')}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Información de Miraflores
              </button>
            </div>
          </div>

          {/* Recomendaciones */}
          {recommendations.length > 0 && (
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                🎯 Distritos Recomendados
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {recommendations.map((rec) => (
                  <div key={rec.value} className="bg-green-50 p-4 rounded-lg border border-green-200">
                    <h3 className="font-semibold text-green-900">{rec.label}</h3>
                    <p className="text-green-700 text-sm mt-1">{rec.description}</p>
                    <div className="mt-2 text-sm text-green-600">
                      <p>🍽️ {rec.restaurant_count} restaurantes</p>
                      <p>⭐ {rec.average_rating?.toFixed(2)} rating</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Estadísticas generales */}
          {statistics && (
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                📈 Estadísticas de Lima
              </h2>
              <div className="bg-gray-50 p-6 rounded-lg">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                  <div>
                    <p className="text-2xl font-bold text-blue-600">{statistics.total_districts}</p>
                    <p className="text-sm text-gray-600">Distritos</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-green-600">{statistics.total_restaurants}</p>
                    <p className="text-sm text-gray-600">Restaurantes</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-purple-600">{statistics.avg_restaurants_per_district}</p>
                    <p className="text-sm text-gray-600">Promedio por distrito</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-yellow-600">{statistics.avg_rating_across_districts}</p>
                    <p className="text-sm text-gray-600">Rating promedio</p>
                  </div>
                </div>
                
                <div className="mt-6 text-center">
                  <p className="text-gray-700">
                    <span className="font-semibold">Más popular:</span> {statistics.most_popular_district} | 
                    <span className="font-semibold ml-4">Mejor valorado:</span> {statistics.highest_rated_district}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DistrictTestPage;