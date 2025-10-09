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
    AnalyticsResponseDTO,
    ErrorResponseDTO
)

__all__ = [
    # Request DTOs
    'UserLocationDTO',
    'RecommendationRequestDTO',
    'RatingPredictionRequestDTO',
    'NearbySearchRequestDTO',

    # Response DTOs
    'RestaurantDTO',
    'RecommendationItemDTO',
    'RecommendationResponseDTO',
    'RatingPredictionResponseDTO',
    'AnalyticsResponseDTO',
    'ErrorResponseDTO',
]