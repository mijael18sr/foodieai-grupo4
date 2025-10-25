import { useState, useEffect } from 'react';
import RestaurantApiService from '../services/api';

export interface UseApiDataReturn {
  categories: string[];
  districts: string[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useApiData(): UseApiDataReturn {
  const [categories, setCategories] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [categoriesData, districtsData] = await Promise.all([
        RestaurantApiService.getCategories(),
        RestaurantApiService.getDistricts(),
      ]);

      setCategories(categoriesData);
      setDistricts(districtsData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error loading data';
      setError(errorMessage);
      console.error('Error fetching API data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return {
    categories,
    districts,
    loading,
    error,
    refetch: fetchData,
  };
}

export default useApiData;