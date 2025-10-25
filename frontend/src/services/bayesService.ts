import axios from 'axios';
import type { AxiosResponse } from 'axios';
import { API_CONFIG } from '../constants/config';
import type {
  SentimentAnalysisRequest,
  SentimentAnalysisResponse,
  BatchSentimentAnalysisResponse,
  RestaurantSentimentStats,
  Review,
  ModelInfo,
  ModelMetrics
} from '../types/api';

const bayesClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: { 'Content-Type': 'application/json' }
});

export class BayesApiService {
  static async analyzeComment(comment: string): Promise<SentimentAnalysisResponse> {
    const payload: SentimentAnalysisRequest = { comment };
    const resp: AxiosResponse<SentimentAnalysisResponse> = await bayesClient.post('/api/v1/sentiment/analyze', payload);
    return resp.data;
  }

  static async analyzeBatch(comments: string[]): Promise<BatchSentimentAnalysisResponse> {
    const resp: AxiosResponse<BatchSentimentAnalysisResponse> = await bayesClient.post('/api/v1/sentiment/analyze/batch', { comments });
    return resp.data;
  }

  static async getRestaurantStats(restaurantId: string): Promise<RestaurantSentimentStats> {
    const resp: AxiosResponse<RestaurantSentimentStats> = await bayesClient.get(`/api/v1/sentiment/restaurant/${restaurantId}`);
    return resp.data;
  }

  static async getReviewsBySentiment(restaurantId: string, sentiment: string, limit = 10): Promise<Review[]> {
    const resp: AxiosResponse<Review[]> = await bayesClient.get(`/api/v1/sentiment/restaurant/${restaurantId}/reviews`, {
      params: { sentiment, limit }
    });
    return resp.data;
  }

  static async getTopPositiveReviews(restaurantId: string, limit = 5): Promise<Review[]> {
    const resp: AxiosResponse<Review[]> = await bayesClient.get(`/api/v1/sentiment/restaurant/${restaurantId}/positive`, { params: { limit } });
    return resp.data;
  }

  static async getNegativeReviews(restaurantId: string, limit = 10): Promise<Review[]> {
    const resp: AxiosResponse<Review[]> = await bayesClient.get(`/api/v1/sentiment/restaurant/${restaurantId}/negative`, { params: { limit } });
    return resp.data;
  }

  static async compareRestaurants(ids: string[]): Promise<any> {
    const resp: AxiosResponse<any> = await bayesClient.post('/api/v1/sentiment/compare', { restaurant_ids: ids });
    return resp.data;
  }

  static async getModelInfo(): Promise<ModelInfo> {
    const resp: AxiosResponse<ModelInfo> = await bayesClient.get('/api/v1/sentiment/model/info');
    return resp.data;
  }

  static async getModelMetrics(): Promise<ModelMetrics> {
    const resp: AxiosResponse<ModelMetrics> = await bayesClient.get('/api/v1/sentiment/model/metrics');
    return resp.data;
  }
}

export default BayesApiService;
