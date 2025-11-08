/**
 * Hook personalizado para gestionar distritos de Lima
 * Proporciona datos, estado de carga y funciones para interactuar con distritos
 */
import { useState, useEffect, useCallback } from 'react';
import districtService, { District, DistrictStatistics } from '../services/districtService';

interface UseDistrictsReturn {
  districts: District[];
  loading: boolean;
  error: string | null;
  statistics: DistrictStatistics | null;
  selectedDistrict: District | null;
  // Funciones
  refreshDistricts: () => Promise<void>;
  getDistrictInfo: (districtName: string) => Promise<any>;
  getRecommendedDistricts: (filters?: {
    touristZoneOnly?: boolean;
    minRating?: number;
    limit?: number;
  }) => Promise<District[]>;
  selectDistrict: (districtValue: string) => void;
  clearSelection: () => void;
}

export const useDistricts = (): UseDistrictsReturn => {
  const [districts, setDistricts] = useState<District[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statistics, setStatistics] = useState<DistrictStatistics | null>(null);
  const [selectedDistrict, setSelectedDistrict] = useState<District | null>(null);

  /**
   * Carga inicial de distritos
   */
  const loadDistricts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('🔄 Cargando distritos desde API...');
      
      // Cargar distritos y estadísticas en paralelo
      const [districtsData, statsData] = await Promise.all([
        districtService.getDistrictsForDropdown(),
        districtService.getDistrictStatistics()
      ]);
      
      setDistricts(districtsData);
      setStatistics(statsData?.summary || null);
      
      console.log(`✅ ${districtsData.length} distritos cargados correctamente`);
      console.log('📊 Estadísticas:', statsData?.summary);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(`Error al cargar distritos: ${errorMessage}`);
      console.error('❌ Error en useDistricts:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Efecto para carga inicial
   */
  useEffect(() => {
    loadDistricts();
  }, [loadDistricts]);

  /**
   * Refrescar lista de distritos
   */
  const refreshDistricts = useCallback(async () => {
    await loadDistricts();
  }, [loadDistricts]);

  /**
   * Obtener información detallada de un distrito
   */
  const getDistrictInfo = useCallback(async (districtName: string) => {
    try {
      console.log(`🔍 Obteniendo información de ${districtName}...`);
      const info = await districtService.getDistrictInfo(districtName);
      console.log(`✅ Información de ${districtName} obtenida:`, info);
      return info;
    } catch (err) {
      console.error(`❌ Error al obtener información de ${districtName}:`, err);
      throw err;
    }
  }, []);

  /**
   * Obtener distritos recomendados
   */
  const getRecommendedDistricts = useCallback(async (filters?: {
    touristZoneOnly?: boolean;
    minRating?: number;
    limit?: number;
  }) => {
    try {
      console.log('🔍 Obteniendo distritos recomendados...', filters);
      
      const recommendations = await districtService.getRecommendedDistricts(
        filters?.touristZoneOnly || false,
        filters?.minRating || 0,
        filters?.limit || 5
      );
      
      console.log(`✅ ${recommendations.length} distritos recomendados obtenidos`);
      return recommendations;
    } catch (err) {
      console.error('❌ Error al obtener distritos recomendados:', err);
      return [];
    }
  }, []);

  /**
   * Seleccionar un distrito específico
   */
  const selectDistrict = useCallback((districtValue: string) => {
    const district = districts.find(d => d.value === districtValue);
    setSelectedDistrict(district || null);
    
    if (district) {
      console.log(`📍 Distrito seleccionado: ${district.label} (${district.restaurant_count} restaurantes)`);
    }
  }, [districts]);

  /**
   * Limpiar selección
   */
  const clearSelection = useCallback(() => {
    setSelectedDistrict(null);
    console.log('🗑️ Selección de distrito limpiada');
  }, []);

  return {
    districts,
    loading,
    error,
    statistics,
    selectedDistrict,
    refreshDistricts,
    getDistrictInfo,
    getRecommendedDistricts,
    selectDistrict,
    clearSelection
  };
};

/**
 * Hook simplificado que solo retorna la lista de distritos
 * Útil cuando solo necesitas los datos básicos sin funcionalidad extra
 */
export const useDistrictsList = () => {
  const { districts, loading, error } = useDistricts();
  
  return {
    districts,
    loading,
    error
  };
};

/**
 * Hook para obtener estadísticas de distritos
 */
export const useDistrictStatistics = () => {
  const { statistics, loading, error } = useDistricts();
  
  return {
    statistics,
    loading,
    error
  };
};