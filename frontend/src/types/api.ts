// API Response Types based on your FastAPI backend

export interface Restaurant {
  id: string;
  name: string;
  category: string;
  district: string;
  rating: number;
  reviews: number;
  distance_km: number;
  address?: string;
  phone?: string;
  url?: string;
}

export interface UserLocation {
  lat: number;
  long: number;
}

export interface RecommendationFilters {
  min_rating?: number;
  max_distance_km?: number;
  district?: string;
}

export interface UserPreferences {
  category?: string;
}

export interface RecommendationRequest {
  user_location: UserLocation;
  preferences?: UserPreferences;
  filters?: RecommendationFilters;
  top_n?: number;
}

export interface RecommendationItem {
  restaurant: Restaurant;
  score: number;
  reason: string;
  details: {
    is_highly_rated: boolean;
    is_popular: boolean;
    is_nearby: boolean;
  };
}

export interface RecommendationResponse {
  recommendations: RecommendationItem[];
  total_found: number;
  execution_time_ms: number;
  metadata: {
    candidates_evaluated: number;
    user_location: UserLocation;
  };
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  service: string;
  version: string;
  data: {
    restaurants_loaded: number;
    database_status: string;
  };
}

export interface ApiError {
  detail: string;
}

// --- Sentiment / Bayesian model types ---
export interface SentimentAnalysisRequest {
  comment: string;
}

export interface SentimentAnalysisResponse {
  comment: string;
  sentiment: string;
  confidence: number;
  probabilities: Record<string, number>;
  processed_text?: string;
}

export interface BatchSentimentAnalysisResponse {
  total: number;
  results: SentimentAnalysisResponse[];
  summary: Record<string, number>;
}

export interface Review {
  id: string;
  comment: string;
  rating: number;
  username: string;
  date?: string;
  sentiment?: string;
  confidence?: number;
}

export interface RestaurantSentimentStats {
  restaurant_id: string;
  total_reviews: number;
  sentiments: Record<string, number>;
  sentiment_percentages: Record<string, number>;
  avg_confidence?: number;
  reviews_sample?: Review[];
}

export interface ModelInfo {
  model_name: string;
  is_trained: boolean;
  metadata: Record<string, unknown> | null;
  classes: string[];
}

export interface ModelMetrics {
  accuracy: number;
  precision_macro: number;
  precision_weighted: number;
  recall_macro: number;
  recall_weighted: number;
  f1_macro: number;
  f1_weighted: number;
  cohen_kappa?: number;
  matthews_corrcoef?: number;
  per_class_metrics: Record<string, {
    precision: number;
    recall: number;
    f1_score: number;
    support: number;
  }>;
  last_evaluation?: string;
}