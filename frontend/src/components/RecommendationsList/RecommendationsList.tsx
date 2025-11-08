import { memo } from 'react';
import { RestaurantCard } from '../RestaurantCard';
import type { RecommendationResponse } from '../../types/api';

interface RecommendationsListProps {
  recommendations: RecommendationResponse | null;
  loading: boolean;
  error: string | null;
  onRestaurantClick?: (restaurantId: string) => void;
}

export const RecommendationsList = memo(function RecommendationsList({
  recommendations,
  loading,
  error,
  onRestaurantClick,
}: RecommendationsListProps) {
  // Render simple debug info first
  if (loading || error || !recommendations) {
    return (
      <div style={{
        background: 'rgba(255,255,255,0.9)', 
        padding: '20px', 
        margin: '20px 0', 
        borderRadius: '10px',
        color: 'black',
        border: '2px solid #333'
      }}>
        <h2 style={{color: '#333', marginBottom: '10px'}}>🐛 DEBUG INFO</h2>
        <p><strong>Loading:</strong> {String(loading)}</p>
        <p><strong>Error:</strong> {error || 'null'}</p>
        <p><strong>Recommendations:</strong> {recommendations ? 'exists' : 'null'}</p>
        <p><strong>Recommendations count:</strong> {recommendations?.recommendations?.length || 0}</p>
        {loading && <p style={{color: 'blue'}}>🔄 Loading recommendations...</p>}
        {error && <p style={{color: 'red'}}>❌ Error: {error}</p>}
        {!recommendations && !loading && !error && <p style={{color: 'orange'}}>⚠️ No recommendations data</p>}
      </div>
    );
  }
  
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center animate-fade-in">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-t-blue-600 border-r-blue-300 border-b-blue-600 border-l-transparent mx-auto mb-6"></div>
          <div className="absolute inset-0 rounded-full bg-blue-600 opacity-10 animate-pulse"></div>
        </div>
        <div className="space-y-2">
          <p className="text-gray-900 text-xl font-bold">🔍 Buscando las mejores recomendaciones</p>
          <p className="text-gray-600 text-sm">Analizando restaurantes con IA...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-red-200 p-8 text-center animate-slide-up">
        <div className="text-red-500 text-6xl mb-6">❌</div>
        <h3 className="text-gray-900 text-2xl font-bold mb-4">
          Error al obtener recomendaciones
        </h3>
        <p className="text-red-600 mb-6 text-lg">{error}</p>
        <div className="bg-red-50 rounded-lg p-4 text-sm text-gray-700 border border-red-200">
          <p className="mb-2 font-medium text-red-700">💡 Asegúrate de que:</p>
          <ul className="text-left space-y-1 max-w-md mx-auto">
            <li>• El servidor backend esté ejecutándose</li>
            <li>• La URL sea: http://localhost:8000</li>
            <li>• No haya problemas de conectividad</li>
          </ul>
        </div>
      </div>
    );
  }

  if (!recommendations) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center animate-fade-in">
        <div className="text-8xl mb-6">🍽️</div>
        <h3 className="text-gray-900 text-3xl font-bold mb-4">
          ¡Encuentra tu restaurante perfecto!
        </h3>
        <p className="text-gray-600 text-lg max-w-2xl mx-auto leading-relaxed">
          Usa los filtros de arriba para descubrir recomendaciones personalizadas creadas especialmente para ti
        </p>
        <div className="mt-8 flex justify-center">
          <div className="bg-blue-50 rounded-full px-6 py-3 border border-blue-200">
            <p className="text-blue-700 text-sm font-medium">✨ IA lista para ayudarte</p>
          </div>
        </div>
      </div>
    );
  }

  const { recommendations: items, metadata } = recommendations;

  if (items.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-yellow-200 p-10 text-center animate-slide-up">
        <div className="text-yellow-500 text-6xl mb-6">🤔</div>
        <h3 className="text-gray-900 text-2xl font-bold mb-4">
          No encontramos restaurantes con esos criterios
        </h3>
        <p className="text-gray-600 text-lg mb-6 max-w-lg mx-auto">
          Intenta ampliar tu búsqueda cambiando los filtros o aumentando la distancia
        </p>
        <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
          <p className="text-yellow-700 text-sm font-medium">💡 Sugerencias:</p>
          <ul className="text-gray-600 text-sm mt-2 space-y-1">
            <li>• Aumenta la distancia máxima</li>
            <li>• Reduce el rating mínimo</li>
            <li>• Prueba con otra categoría</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Results Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div>
            <h2 className="text-4xl font-bold text-gray-900 mb-3">
              🎯 Recomendaciones Personalizadas
            </h2>
            <p className="text-gray-900 text-lg">
              Encontramos <span className="font-bold text-blue-600 text-xl">{items.length}</span> restaurantes increíbles
            </p>
            <p className="text-gray-600 text-sm mt-1">
              📍 Cerca de ({metadata.user_location.lat.toFixed(4)}, {metadata.user_location.long.toFixed(4)})
            </p>
          </div>
          <div className="bg-blue-50 rounded-lg p-4 text-center border border-blue-200">
            <div className="text-gray-700 text-sm space-y-1">
              <p>🔍 Evaluados: <span className="font-semibold text-blue-600">{metadata.candidates_evaluated}</span></p>
              <p>⏰ {new Date().toLocaleString('es-ES')}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {items.map((recommendation, index) => (
          <div key={recommendation.restaurant.id || index} className="relative group">
            {/* Ranking Badge */}
            <div className="absolute -top-4 -left-4 z-20 bg-blue-600 text-white rounded-2xl w-12 h-12 flex items-center justify-center font-bold text-lg shadow-lg group-hover:scale-110 transition-transform duration-300">
              #{index + 1}
            </div>
            
            <RestaurantCard
              recommendation={recommendation}
              onClick={() => onRestaurantClick?.(recommendation.restaurant.id)}
            />
          </div>
        ))}
      </div>

      {/* Summary Stats */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
          <span className="text-3xl">📊</span>
          <span>Resumen de Resultados</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 rounded-lg p-6 text-center group hover:shadow-md transition-all duration-200 border border-blue-200">
            <div className="text-4xl font-bold text-blue-600 mb-2">
              {items.length}
            </div>
            <div className="text-gray-700 font-medium">Restaurantes encontrados</div>
            <div className="text-blue-500 text-sm mt-1">🏪</div>
          </div>
          
          <div className="bg-green-50 rounded-lg p-6 text-center group hover:shadow-md transition-all duration-200 border border-green-200">
            <div className="text-4xl font-bold text-green-600 mb-2 flex items-center justify-center gap-1">
              {(items.reduce((sum, item) => sum + item.restaurant.rating, 0) / items.length).toFixed(1)}
              <span className="text-2xl">⭐</span>
            </div>
            <div className="text-gray-700 font-medium">Rating promedio</div>
            <div className="text-green-500 text-sm mt-1">⭐</div>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-6 text-center group hover:shadow-md transition-all duration-200 border border-purple-200">
            <div className="text-4xl font-bold text-purple-600 mb-2">
              {(items.reduce((sum, item) => sum + item.distance_km, 0) / items.length).toFixed(1)}
              <span className="text-lg text-gray-500 ml-1">km</span>
            </div>
            <div className="text-gray-700 font-medium">Distancia promedio</div>
            <div className="text-purple-500 text-sm mt-1">📏</div>
          </div>
        </div>
      </div>
    </div>
  );
});