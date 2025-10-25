"""
Application Package
Capa de aplicación con servicios y DTOs.
"""

from .services import RecommendationService, SentimentAnalysisService
from .dto import (
    # Request DTOs
    RecommendationRequestDTO,
    UserLocationDTO,
    SentimentAnalysisRequestDTO,
    BatchSentimentAnalysisRequestDTO,

    # Response DTOs
    RecommendationResponseDTO,
    RestaurantDTO,
    RecommendationItemDTO,
    SentimentAnalysisResponseDTO,
    RestaurantSentimentStatsDTO,
    ReviewDTO
)

__all__ = [
    # Services
    'RecommendationService',
    'SentimentAnalysisService',

    # Request DTOs
    'RecommendationRequestDTO',
    'UserLocationDTO',
    'SentimentAnalysisRequestDTO',
    'BatchSentimentAnalysisRequestDTO',

    # Response DTOs
    'RecommendationResponseDTO',
    'RestaurantDTO',
    'RecommendationItemDTO',
    'SentimentAnalysisResponseDTO',
    'RestaurantSentimentStatsDTO',
    'ReviewDTO',
]