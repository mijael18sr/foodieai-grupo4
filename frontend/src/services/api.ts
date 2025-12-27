import type { AxiosResponse } from 'axios';
import type {
  RecommendationRequest,
  RecommendationResponse,
  HealthResponse,
} from '../types/api';
import { API_CONFIG } from '../constants/config';
import { apiClient } from './client';

export class RestaurantApiService {
  static async getHealth(): Promise<HealthResponse> {
    const response: AxiosResponse<HealthResponse> = await apiClient.get('/api/v1/health/status');
    return response.data;
  }

  static async getDistricts(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await apiClient.get('/api/v1/restaurants/districts');
    return response.data;
  }

  static async getCategories(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await apiClient.get('/api/v1/restaurants/categories');
    return response.data;
  }

  static async getRecommendations(request: RecommendationRequest): Promise<RecommendationResponse> {
    const response: AxiosResponse<RecommendationResponse> = await apiClient.post(
      '/api/v1/recommendations',
      request
    );
    return response.data;
  }

  static async getSimpleRecommendations(
    lat: number,
    long: number,
    category?: string,
    minRating?: number,
    maxDistance?: number,
    topN?: number
  ): Promise<RecommendationResponse> {
    return this.getRecommendations({
      user_location: { lat, long },
      preferences: category ? { category } : undefined,
      filters: { min_rating: minRating, max_distance_km: maxDistance },
      top_n: topN || API_CONFIG.DEFAULT_TOP_N,
    });
  }

  static async testConnection(): Promise<boolean> {
    try {
      await this.getHealth();
      return true;
    } catch {
      return false;
    }
  }
}

export default RestaurantApiService;