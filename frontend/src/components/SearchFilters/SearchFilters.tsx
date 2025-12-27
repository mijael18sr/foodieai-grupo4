import { useState, memo, useCallback, useEffect } from 'react';
import type { UserLocation, RecommendationFilters, UserPreferences } from '../../types/api';
import { DistrictSelector } from '../DistrictSelector';
import { LocationPickerMap } from '../LocationPickerMap';
import { useLocation } from '../../hooks';

interface SearchFiltersProps {
  categories: string[];
  districts: string[];
  onSearch: (
    location: UserLocation,
    preferences?: UserPreferences,
    filters?: RecommendationFilters,
    topN?: number
  ) => void;
  loading?: boolean;
}

export const SearchFilters = memo(function SearchFilters({
  categories,
  districts,
  onSearch,
  loading = false,
}: SearchFiltersProps) {
  const { location: geoLocation, isLoading: geoLoading, error: geoError, requestLocation } = useLocation();
  
  const [location, setLocation] = useState<UserLocation>({
    lat: -12.0464,
    long: -77.0428
  });
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [minRating, setMinRating] = useState<number>(0);
  const [maxDistance, setMaxDistance] = useState<number>(10);
  const [topN, setTopN] = useState<number>(10);
  const [isMapOpen, setIsMapOpen] = useState(false);
  const [locationAddress, setLocationAddress] = useState<string>('');

  useEffect(() => {
    if (geoLocation) {
      setLocation({ lat: geoLocation.lat, long: geoLocation.long });
    }
  }, [geoLocation]);

  const handleMapConfirm = useCallback((lat: number, lng: number, address?: string) => {
    setLocation({ lat, long: lng });
    if (address) setLocationAddress(address);
  }, []);

  const handleSearch = useCallback(() => {
    const preferences: UserPreferences = selectedCategory 
      ? { category: selectedCategory }
      : {};

    const filters: RecommendationFilters = {
      min_rating: minRating > 0 ? minRating : undefined,
      max_distance_km: maxDistance,
      district: selectedDistrict || undefined,
    };

    onSearch(location, preferences, filters, topN);
  }, [location, selectedCategory, minRating, maxDistance, selectedDistrict, topN, onSearch]);

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8 animate-slide-up">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-lg mb-4 shadow-sm">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-3">
          Configuración de Búsqueda
        </h2>
        <p className="text-gray-600 text-base font-medium">
          Configure los parámetros de búsqueda para obtener recomendaciones personalizadas
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Location - KOSARI Clean Style */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-6 hover:shadow-md transition-shadow duration-200">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-3 mb-4">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-sm">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              </svg>
            </div>
            <span>Ubicación</span>
          </h3>
          
          <div className="space-y-4">
            <div>
              <label htmlFor="latitude" className="block text-sm font-medium text-gray-700 mb-2">
                Latitud
              </label>
              <input
                id="latitude"
                type="number"
                step="0.00001"
                value={location.lat}
                onChange={(e) => setLocation(prev => ({ ...prev, lat: parseFloat(e.target.value) || 0 }))}
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-medium"
                placeholder="-12.0464"
              />
            </div>
            
            <div>
              <label htmlFor="longitude" className="block text-sm font-medium text-gray-700 mb-2">
                Longitud
              </label>
              <input
                id="longitude"
                type="number"
                step="0.00001"
                value={location.long}
                onChange={(e) => setLocation(prev => ({ ...prev, long: parseFloat(e.target.value) || 0 }))}
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-medium"
                placeholder="-77.0428"
              />
            </div>

            <button
              onClick={() => setIsMapOpen(true)}
              className="w-full bg-green-600 text-white px-4 py-3 rounded-lg hover:bg-green-700 transition-colors duration-200 font-semibold shadow-sm hover:shadow-md flex items-center justify-center gap-2"
            >
              🗺️ Seleccionar ubicación en mapa
            </button>
            
            <button
              onClick={requestLocation}
              disabled={geoLoading}
              className="w-full bg-blue-100 text-blue-700 px-4 py-3 rounded-lg hover:bg-blue-200 transition-colors duration-200 font-medium flex items-center justify-center gap-2"
            >
              {geoLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-700 border-t-transparent"></div>
                  Obteniendo...
                </>
              ) : (
                <>📍 Usar GPS automático</>
              )}
            </button>
            
            {locationAddress && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <p className="text-xs text-green-600 font-medium mb-1">📍 Ubicación seleccionada:</p>
                <p className="text-sm text-green-800 line-clamp-2">{locationAddress}</p>
              </div>
            )}
            
            {geoError && (
              <p className="text-sm text-amber-600 flex items-center gap-1">
                <span>⚠️</span> {geoError}
              </p>
            )}
            {geoLocation?.accuracy && !locationAddress && (
              <p className="text-xs text-gray-500">
                Precisión GPS: ±{Math.round(geoLocation.accuracy)}m
              </p>
            )}
          </div>
        </div>

        {/* Preferences */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-3 mb-4">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <span>Preferencias</span>
          </h3>
          
          <div className="space-y-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                Categoría de Comida
              </label>
              <select
                id="category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-medium"
              >
                <option value="">Cualquier categoría</option>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="district" className="block text-sm font-medium text-gray-700 mb-2">
                Distrito de Lima
              </label>
              
              <DistrictSelector
                selectedDistrict={selectedDistrict}
                onDistrictChange={setSelectedDistrict}
                districts={districts}
                showStatistics={true}
                allowSearch={true}
                placeholder="Cualquier distrito de Lima"
                className="w-full"
              />
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-3 mb-4">
            <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
              </svg>
            </div>
            <span>Filtros Avanzados</span>
          </h3>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Rating mínimo: {minRating > 0 ? (
                  <span className="text-yellow-600 font-bold">{minRating.toFixed(1)} ⭐</span>
                ) : (
                  <span className="text-gray-500">Sin filtro</span>
                )}
              </label>
              <input
                type="range"
                min="0"
                max="5"
                step="0.5"
                value={minRating}
                onChange={(e) => setMinRating(parseFloat(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(minRating / 5) * 100}%, #e5e7eb ${(minRating / 5) * 100}%, #e5e7eb 100%)`
                }}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Distancia máxima: <span className="text-blue-600 font-bold">{maxDistance} km</span>
              </label>
              <input
                type="range"
                min="1"
                max="20"
                step="1"
                value={maxDistance}
                onChange={(e) => setMaxDistance(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(maxDistance / 20) * 100}%, #e5e7eb ${(maxDistance / 20) * 100}%, #e5e7eb 100%)`
                }}
              />
            </div>

            <div>
              <label htmlFor="topN" className="block text-sm font-medium text-gray-700 mb-2">
                Número de resultados
              </label>
              <select
                id="topN"
                value={topN}
                onChange={(e) => setTopN(parseInt(e.target.value))}
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-medium"
              >
                <option value={5}>5 resultados</option>
                <option value={10}>10 resultados</option>
                <option value={15}>15 resultados</option>
                <option value={20}>20 resultados</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Search Button */}
      <div className="mt-8 flex justify-center">
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-blue-600 text-white px-12 py-4 rounded-lg hover:bg-blue-700 hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-xl"
        >
          {loading ? (
            <span className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
              Procesando...
            </span>
          ) : (
            'Generar Recomendaciones'
          )}
        </button>
      </div>

      {/* Location Picker Map Modal */}
      <LocationPickerMap
        isOpen={isMapOpen}
        onClose={() => setIsMapOpen(false)}
        onConfirm={handleMapConfirm}
        initialLat={location.lat !== 0 ? location.lat : undefined}
        initialLng={location.long !== 0 ? location.long : undefined}
      />
    </div>
  );
});