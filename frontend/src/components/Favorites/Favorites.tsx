import { memo, useState } from 'react';
import type { FavoriteRestaurant } from '../../hooks/useFavorites';

interface FavoritesProps {
  favorites: FavoriteRestaurant[];
  onRemove: (id: string) => void;
  onClear: () => void;
  onNavigate: (view: string) => void;
}

export const Favorites = memo(function Favorites({
  favorites,
  onRemove,
  onClear,
  onNavigate,
}: FavoritesProps) {
  const [confirmClear, setConfirmClear] = useState(false);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-PE', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };

  const getCategoryIcon = (category: string) => {
    const iconMap: Record<string, string> = {
      'Comida_Rapida': '🍔',
      'Parrillas': '🥩',
      'Marisqueria': '🦐',
      'Italiana': '🍝',
      'Chifa': '🥟',
      'Japonesa': '🍣',
      'Criolla': '🇵🇪',
      'Vegetariana': '🥗',
      'Internacional': '🌍',
      'Postres': '🧁',
      'Bar': '🍻',
      'Cafeteria': '☕',
      'Peruana': '🌶️',
      'Peruano': '🌶️',
      'Restaurante': '🍽️',
    };
    return iconMap[category] || '🍽️';
  };

  if (favorites.length === 0) {
    return (
      <div className="space-y-8">
        <div className="bg-gradient-to-br from-pink-50 via-rose-50 to-red-50 rounded-2xl p-8 border border-pink-100">
          <div className="text-center max-w-2xl mx-auto">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-pink-500 to-rose-600 rounded-2xl mb-6 shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Mis Favoritos
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Aún no tienes restaurantes favoritos. Explora y guarda tus lugares preferidos.
            </p>
            <button
              onClick={() => onNavigate('recommendations')}
              className="bg-gradient-to-r from-pink-500 to-rose-600 text-white px-8 py-3 rounded-full font-semibold hover:from-pink-600 hover:to-rose-700 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              🔍 Buscar Restaurantes
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-pink-50 via-rose-50 to-red-50 rounded-2xl p-8 border border-pink-100">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
              <span className="w-12 h-12 bg-gradient-to-br from-pink-500 to-rose-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
              </span>
              Mis Favoritos
            </h1>
            <p className="text-gray-600">
              {favorites.length} {favorites.length === 1 ? 'restaurante guardado' : 'restaurantes guardados'}
            </p>
          </div>
          <div className="flex gap-3">
            {confirmClear ? (
              <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-xl border border-red-200">
                <span className="text-sm text-gray-700">¿Eliminar todos?</span>
                <button
                  onClick={() => {
                    onClear();
                    setConfirmClear(false);
                  }}
                  className="px-3 py-1 bg-red-500 text-white text-sm rounded-lg hover:bg-red-600 transition-colors"
                >
                  Sí
                </button>
                <button
                  onClick={() => setConfirmClear(false)}
                  className="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded-lg hover:bg-gray-300 transition-colors"
                >
                  No
                </button>
              </div>
            ) : (
              <button
                onClick={() => setConfirmClear(true)}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl text-gray-600 hover:bg-red-50 hover:border-red-200 hover:text-red-600 transition-all"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Limpiar
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="grid gap-4">
        {favorites.map((restaurant) => (
          <div
            key={restaurant.id}
            className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
          >
            <div className="p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-4 flex-1 min-w-0">
                  <div className="w-14 h-14 bg-gradient-to-br from-pink-100 to-rose-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl">{getCategoryIcon(restaurant.category)}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-gray-900 text-lg truncate">
                      {restaurant.name}
                    </h3>
                    <div className="flex flex-wrap items-center gap-2 mt-1">
                      <span className="inline-flex items-center px-2 py-0.5 bg-pink-100 text-pink-700 rounded-full text-xs font-medium">
                        {restaurant.category}
                      </span>
                      <span className="inline-flex items-center px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                        📍 {restaurant.district.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
                      <div className="flex items-center gap-1">
                        <span className="text-yellow-500">⭐</span>
                        <span className="font-medium text-gray-700">{restaurant.rating.toFixed(1)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span>💬</span>
                        <span>{restaurant.reviews} reseñas</span>
                      </div>
                      {restaurant.distance_km && (
                        <div className="flex items-center gap-1">
                          <span>📏</span>
                          <span>{restaurant.distance_km.toFixed(1)} km</span>
                        </div>
                      )}
                    </div>
                    {restaurant.address && (
                      <p className="text-sm text-gray-500 mt-2 truncate">
                        {restaurant.address}
                      </p>
                    )}
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <button
                    onClick={() => onRemove(restaurant.id)}
                    className="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-100 hover:bg-red-100 text-gray-400 hover:text-red-500 transition-all"
                    title="Eliminar de favoritos"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                    </svg>
                  </button>
                  <span className="text-xs text-gray-400">
                    {formatDate(restaurant.addedAt)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center pt-4">
        <button
          onClick={() => onNavigate('home')}
          className="bg-gradient-to-r from-pink-500 to-rose-600 text-white px-8 py-3 rounded-full font-semibold hover:from-pink-600 hover:to-rose-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
        >
          ← Volver al Inicio
        </button>
      </div>
    </div>
  );
});

export default Favorites;
