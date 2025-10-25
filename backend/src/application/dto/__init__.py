"""
DTOs Package
Data Transfer Objects para comunicación entre capas.
"""

from .request_dto import (
    UserLocationDTO,
    RecommendationRequestDTO,
    RatingPredictionRequestDTO,
    NearbySearchRequestDTO
)

from .response_dto import (
    RestaurantDTO,
    RecommendationItemDTO,
    RecommendationResponseDTO,
    RatingPredictionResponseDTO,
    AnalyticsResponseDTO
)

from .sentiment_dto import (
    SentimentAnalysisRequestDTO,
    SentimentAnalysisResponseDTO,
    RestaurantSentimentStatsDTO,
    BatchSentimentAnalysisRequestDTO,
    BatchSentimentAnalysisResponseDTO,
    SentimentComparisonRequestDTO,
    SentimentComparisonResponseDTO,
    ReviewDTO
)

__all__ = [
    # Request DTOs
    'UserLocationDTO',
    'RecommendationRequestDTO',
    'RatingPredictionRequestDTO',
    'NearbySearchRequestDTO',
    'SentimentAnalysisRequestDTO',
    'BatchSentimentAnalysisRequestDTO',
    'SentimentComparisonRequestDTO',

    # Response DTOs
    'RestaurantDTO',
    'RecommendationItemDTO',
    'RecommendationResponseDTO',
    'RatingPredictionResponseDTO',
    'AnalyticsResponseDTO',
    'SentimentAnalysisResponseDTO',
    'RestaurantSentimentStatsDTO',
    'BatchSentimentAnalysisResponseDTO',
    'SentimentComparisonResponseDTO',
    'ReviewDTO',
]