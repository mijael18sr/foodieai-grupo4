import type { AxiosResponse } from 'axios';
import type {
  SentimentAnalysisRequest,
  SentimentAnalysisResponse,
  BatchSentimentAnalysisResponse,
  RestaurantSentimentStats,
  Review,
  ModelInfo,
  ModelMetrics
} from '../types/api';
import { apiClient } from './client';

export class BayesApiService {
  static async analyzeComment(comment: string): Promise<SentimentAnalysisResponse> {
    const payload: SentimentAnalysisRequest = { comment };
    const resp: AxiosResponse<SentimentAnalysisResponse> = await apiClient.post('/api/v1/sentiment/analyze', payload);
    return resp.data;
  }

  static async analyzeBatch(comments: string[]): Promise<BatchSentimentAnalysisResponse> {
    const resp: AxiosResponse<BatchSentimentAnalysisResponse> = await apiClient.post('/api/v1/sentiment/analyze/batch', { comments });
    return resp.data;
  }

  static async getRestaurantStats(restaurantId: string): Promise<RestaurantSentimentStats> {
    const resp: AxiosResponse<RestaurantSentimentStats> = await apiClient.get(`/api/v1/sentiment/restaurant/${restaurantId}`);
    return resp.data;
  }

  static async getReviewsBySentiment(restaurantId: string, sentiment: string, limit = 10): Promise<Review[]> {
    const resp: AxiosResponse<Review[]> = await apiClient.get(`/api/v1/sentiment/restaurant/${restaurantId}/reviews`, {
      params: { sentiment, limit }
    });
    return resp.data;
  }

  static async getTopPositiveReviews(restaurantId: string, limit = 5): Promise<Review[]> {
    const resp: AxiosResponse<Review[]> = await apiClient.get(`/api/v1/sentiment/restaurant/${restaurantId}/positive`, { params: { limit } });
    return resp.data;
  }

  static async getNegativeReviews(restaurantId: string, limit = 10): Promise<Review[]> {
    const resp: AxiosResponse<Review[]> = await apiClient.get(`/api/v1/sentiment/restaurant/${restaurantId}/negative`, { params: { limit } });
    return resp.data;
  }

  static async compareRestaurants(ids: string[]): Promise<unknown> {
    const resp: AxiosResponse<unknown> = await apiClient.post('/api/v1/sentiment/compare', { restaurant_ids: ids });
    return resp.data;
  }

  static async getModelInfo(): Promise<ModelInfo> {
    const resp: AxiosResponse<ModelInfo> = await apiClient.get('/api/v1/sentiment/model/info');
    return resp.data;
  }

  static async getModelMetrics(): Promise<ModelMetrics> {
    const resp: AxiosResponse<ModelMetrics> = await apiClient.get('/api/v1/sentiment/model/metrics');
    return resp.data;
  }
}

export default BayesApiService;
