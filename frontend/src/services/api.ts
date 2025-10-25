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

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error instanceof Error ? error : new Error(String(error)));
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error(`❌ API Error: ${error.response?.status} ${error.config?.url}`, error.response?.data);
    return Promise.reject(error instanceof Error ? error : new Error(String(error)));
  }
);

export class RestaurantApiService {
  
  /**
   * Get API health status
   */
  static async getHealth(): Promise<HealthResponse> {
    const response: AxiosResponse<HealthResponse> = await apiClient.get('/api/v1/health');
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
    console.log('🌐 API Service: getRecommendations called with:', request);
    
    try {
      const response: AxiosResponse<RecommendationResponse> = await apiClient.post(
        '/api/v1/recommendations',
        request
      );
      console.log('✅ API Service: Success response:', response.data);
      console.log('📊 Recommendations count:', response.data.recommendations?.length || 0);
      return response.data;
    } catch (error) {
      console.error('❌ API Service: Error in getRecommendations:', error);
      throw error;
    }
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
    } catch (error) {
      console.error('API Connection failed:', error);
      return false;
    }
  }
}

// Export default instance
export default RestaurantApiService;