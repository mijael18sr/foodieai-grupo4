/**
 * Componente avanzado para selección de distritos de Lima
 * Incluye información enriquecida, búsqueda y filtros
 */
import React, { useState, useMemo } from 'react';
import { useApiData } from '../../hooks';

interface DistrictSelectorProps {
  selectedDistrict: string;
  onDistrictChange: (district: string) => void;
  districts?: string[];
  showStatistics?: boolean;
  allowSearch?: boolean;
  filterByTouristZone?: boolean;
  className?: string;
  placeholder?: string;
}

export const DistrictSelector: React.FC<DistrictSelectorProps> = ({
  selectedDistrict,
  onDistrictChange,
  districts: propDistricts,
  showStatistics = true,
  allowSearch = true,
  className = "",
  placeholder = "Seleccionar distrito..."
}) => {
  const { districts: apiDistricts, loading, error } = useApiData();
  const [searchTerm, setSearchTerm] = useState("");

  // Usar districts desde props si están disponibles, si no usar desde API
  const districts = propDistricts || apiDistricts;

  // Filtros aplicados - ahora trabajamos con strings simples
  const filteredDistricts = useMemo(() => {
    if (!districts || districts.length === 0) return [];
    
    let filtered = districts;

    // Filtrar por término de búsqueda
    if (searchTerm.trim()) {
      filtered = filtered.filter((district: string) =>
        district.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    return filtered;
  }, [districts, searchTerm]);

  // Solo mostrar loading si estamos usando la API y no hay props
  if (!propDistricts && loading) {
    return (
      <div className={`district-selector-loading ${className}`}>
        <div className="animate-pulse">
          <div className="h-12 bg-gray-200 rounded-lg mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  // Solo mostrar error si estamos usando la API y no hay props
  if (!propDistricts && error) {
    return (
      <div className={`district-selector-error ${className}`}>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-2 text-red-700">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-medium">Error al cargar distritos</span>
          </div>
          <p className="text-sm text-red-600 mt-1">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`district-selector ${className}`}>
      {/* Filtros de búsqueda */}
      {allowSearch && (
        <div className="mb-4 space-y-3">
          {/* Campo de búsqueda */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Buscar distrito..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            />
          </div>
        </div>
      )}

      {/* Selector principal */}
      <div className="space-y-2">
        <select
          value={selectedDistrict}
          onChange={(e) => onDistrictChange(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-medium"
        >
          <option value="">{placeholder}</option>
          {filteredDistricts.map((district: string) => (
            <option key={district} value={district}>
              {district.replace(/_/g, ' ')}
            </option>
          ))}
        </select>

        {/* Estadísticas rápidas */}
        {showStatistics && (
          <div className="flex flex-wrap gap-2 text-xs text-gray-600">
            <span className="bg-gray-100 px-2 py-1 rounded">
              📊 {filteredDistricts.length} distritos disponibles
            </span>
          </div>
        )}
      </div>

      {/* Información del distrito seleccionado */}
      {selectedDistrict && showStatistics && (
        <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h4 className="font-semibold text-blue-900 flex items-center gap-2">
                📍 {selectedDistrict.replace(/_/g, ' ')}
              </h4>
              
              <p className="text-sm text-blue-700 mt-1">
                Distrito seleccionado de Lima
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DistrictSelector;