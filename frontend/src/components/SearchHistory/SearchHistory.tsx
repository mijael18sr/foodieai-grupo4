import { memo, useState } from 'react';
import type { SearchHistoryItem } from '../../hooks/useSearchHistory';

interface SearchHistoryProps {
  history: SearchHistoryItem[];
  onRemove: (id: string) => void;
  onClear: () => void;
  onRepeatSearch: (item: SearchHistoryItem) => void;
  onNavigate: (view: string) => void;
}

export const SearchHistory = memo(function SearchHistory({
  history,
  onRemove,
  onClear,
  onRepeatSearch,
  onNavigate,
}: SearchHistoryProps) {
  const [confirmClear, setConfirmClear] = useState(false);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Hace un momento';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    if (diffDays < 7) return `Hace ${diffDays} días`;

    return date.toLocaleDateString('es-PE', {
      day: 'numeric',
      month: 'short',
    });
  };

  const getSearchSummary = (item: SearchHistoryItem) => {
    const parts: string[] = [];
    
    if (item.locationName) {
      parts.push(item.locationName.split(',')[0]);
    }
    
    if (item.preferences?.category) {
      parts.push(item.preferences.category.replace('_', ' '));
    }
    
    if (item.filters?.district) {
      parts.push(item.filters.district.replace('_', ' '));
    }
    
    if (item.filters?.min_rating) {
      parts.push(`⭐ ${item.filters.min_rating}+`);
    }

    return parts.length > 0 ? parts.join(' • ') : 'Búsqueda general';
  };

  if (history.length === 0) {
    return (
      <div className="space-y-8">
        <div className="bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 rounded-2xl p-8 border border-amber-100">
          <div className="text-center max-w-2xl mx-auto">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-amber-500 to-orange-600 rounded-2xl mb-6 shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Búsquedas Recientes
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Aún no has realizado búsquedas. ¡Empieza a explorar restaurantes!
            </p>
            <button
              onClick={() => onNavigate('recommendations')}
              className="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-8 py-3 rounded-full font-semibold hover:from-amber-600 hover:to-orange-700 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              🔍 Nueva Búsqueda
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 rounded-2xl p-8 border border-amber-100">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
              <span className="w-12 h-12 bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </span>
              Búsquedas Recientes
            </h1>
            <p className="text-gray-600">
              {history.length} {history.length === 1 ? 'búsqueda guardada' : 'búsquedas guardadas'}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => onNavigate('recommendations')}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-xl hover:from-amber-600 hover:to-orange-700 transition-all shadow-md"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Nueva
            </button>
            {confirmClear ? (
              <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-xl border border-red-200">
                <span className="text-sm text-gray-700">¿Eliminar todo?</span>
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
        {history.map((item) => (
          <div
            key={item.id}
            className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
          >
            <div className="p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-amber-100 to-orange-100 rounded-xl flex items-center justify-center flex-shrink-0">
                      <svg className="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 truncate">
                        {getSearchSummary(item)}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {item.resultsCount} resultados encontrados
                      </p>
                    </div>
                    <span className="text-xs text-gray-400 flex-shrink-0">
                      {formatDate(item.timestamp)}
                    </span>
                  </div>

                  {item.topResults.length > 0 && (
                    <div className="ml-13 space-y-2">
                      <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">
                        Mejores resultados:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {item.topResults.map((result, idx) => (
                          <span
                            key={result.id}
                            className="inline-flex items-center gap-1 px-2 py-1 bg-gray-50 rounded-lg text-xs text-gray-700"
                          >
                            <span className="text-amber-500">{idx + 1}.</span>
                            <span className="font-medium truncate max-w-[150px]">
                              {result.name}
                            </span>
                            <span className="text-yellow-500">⭐</span>
                            <span>{result.rating.toFixed(1)}</span>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 flex-shrink-0">
                  <button
                    onClick={() => onRepeatSearch(item)}
                    className="w-10 h-10 flex items-center justify-center rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-600 transition-all"
                    title="Repetir búsqueda"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onRemove(item.id)}
                    className="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-100 hover:bg-red-100 text-gray-400 hover:text-red-500 transition-all"
                    title="Eliminar"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center pt-4">
        <button
          onClick={() => onNavigate('home')}
          className="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-8 py-3 rounded-full font-semibold hover:from-amber-600 hover:to-orange-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
        >
          ← Volver al Inicio
        </button>
      </div>
    </div>
  );
});

export default SearchHistory;
