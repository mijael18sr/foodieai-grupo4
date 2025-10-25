import { useState, useEffect } from 'react';
import RestaurantApiService from '../services/api';
import type { RecommendationResponse, RecommendationRequest } from '../types/api';

export interface UseRecommendationsOptions {
  autoFetch?: boolean;
  defaultLocation?: { lat: number; long: number };
}

export interface UseRecommendationsReturn {
  recommendations: RecommendationResponse | null;
  loading: boolean;
  error: string | null;
  fetchRecommendations: (request: RecommendationRequest) => Promise<void>;
  fetchSimpleRecommendations: (
    lat: number,
    long: number,
    category?: string,
    minRating?: number,
    maxDistance?: number,
    topN?: number
  ) => Promise<void>;
  clearError: () => void;
}

export function useRecommendations(options: UseRecommendationsOptions = {}): UseRecommendationsReturn {
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const clearError = () => setError(null);

  const fetchRecommendations = async (request: RecommendationRequest) => {
    console.log('🚀 fetchRecommendations started with request:', request);
    setLoading(true);
    setError(null);
    
    try {
      console.log('📡 Calling API...');
      const response = await RestaurantApiService.getRecommendations(request);
      console.log('✅ API Response received:', response);
      setRecommendations(response);
      console.log('📊 Recommendations set in state');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error getting recommendations';
      console.error('❌ Error fetching recommendations:', err);
      console.error('🔍 Error details:', {
        message: errorMessage,
        stack: err instanceof Error ? err.stack : 'No stack trace',
        request: request
      });
      setError(errorMessage);
    } finally {
      console.log('🏁 fetchRecommendations finished, loading set to false');
      setLoading(false);
    }
  };

  const fetchSimpleRecommendations = async (
    lat: number,
    long: number,
    category?: string,
    minRating?: number,
    maxDistance?: number,
    topN?: number
  ) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await RestaurantApiService.getSimpleRecommendations(
        lat,
        long,
        category,
        minRating,
        maxDistance,
        topN
      );
      setRecommendations(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error getting recommendations';
      setError(errorMessage);
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  // Auto-fetch with default location if specified
  useEffect(() => {
    if (options.autoFetch && options.defaultLocation) {
      fetchSimpleRecommendations(
        options.defaultLocation.lat,
        options.defaultLocation.long
      );
    }
  }, [options.autoFetch, options.defaultLocation]);

  return {
    recommendations,
    loading,
    error,
    fetchRecommendations,
    fetchSimpleRecommendations,
    clearError,
  };
}

export default useRecommendations;