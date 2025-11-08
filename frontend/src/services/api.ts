import axios from 'axios';
import type { AxiosResponse } from 'axios';
import type {
  RecommendationRequest,
  RecommendationResponse,
  HealthResponse
} from '../types/api';
import { API_CONFIG } from '../constants/config';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for error handling
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error instanceof Error ? error : new Error(String(error)));
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    return Promise.reject(error instanceof Error ? error : new Error(String(error)));
  }
);

export class RestaurantApiService {
  
  /**
   * Get API health status
   */
  static async getHealth(): Promise<HealthResponse> {
    const response: AxiosResponse<HealthResponse> = await apiClient.get('/api/v1/health/status');
    return response.data;
  }

  /**
   * Get all available districts
   */
  static async getDistricts(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await apiClient.get('/api/v1/restaurants/districts');
    return response.data;
  }

  /**
   * Get all available categories
   */
  static async getCategories(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await apiClient.get('/api/v1/restaurants/categories');
    return response.data;
  }

  /**
   * Get personalized restaurant recommendations
   */
  static async getRecommendations(request: RecommendationRequest): Promise<RecommendationResponse> {
    const response: AxiosResponse<RecommendationResponse> = await apiClient.post(
      '/api/v1/recommendations',
      request
    );
    return response.data;
  }

  /**
   * Get restaurant recommendations with simplified parameters
   */
  static async getSimpleRecommendations(
    lat: number,
    long: number,
    category?: string,
    minRating?: number,
    maxDistance?: number,
    topN?: number
  ): Promise<RecommendationResponse> {
    const request: RecommendationRequest = {
      user_location: { lat, long },
      preferences: category ? { category } : undefined,
      filters: {
        min_rating: minRating,
        max_distance_km: maxDistance,
      },
      top_n: topN || API_CONFIG.DEFAULT_TOP_N,
    };

    return this.getRecommendations(request);
  }

  /**
   * Test API connectivity
   */
  static async testConnection(): Promise<boolean> {
    try {
      await this.getHealth();
      return true;
    } catch {
      return false;
    }
  }
}

// Export default instance
export default RestaurantApiService;