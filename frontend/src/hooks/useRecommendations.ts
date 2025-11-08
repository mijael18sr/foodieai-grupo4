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
    setLoading(true);
    setError(null);
    
    try {
      const response = await RestaurantApiService.getRecommendations(request);
      setRecommendations(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error getting recommendations';
      setError(errorMessage);
    } finally {
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