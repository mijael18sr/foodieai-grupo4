"""
Response DTOs
Objetos para devolver datos desde la API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class RestaurantDTO(BaseModel):
    """DTO para información de restaurante."""
    id: str
    name: str
    category: str
    rating: float
    reviews: int
    distance_km: Optional[float] = None
    address: str
    district: str
    phone: Optional[str] = None
    url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "R123",
                "name": "La Rosa Náutica",
                "category": "Peruana",
                "rating": 4.5,
                "reviews": 250,
                "distance_km": 1.5,
                "address": "Espigón 4, Costa Verde",
                "district": "Miraflores",
                "phone": "+51 1 4470057",
                "url": "https://example.com"
            }
        }


class RecommendationItemDTO(BaseModel):
    """DTO para un item de recomendación."""
    restaurant: RestaurantDTO
    score: float = Field(..., ge=0.0, le=1.0, description="Score de recomendación")
    reason: str = Field(..., description="Razón de la recomendación")
    details: Optional[Dict] = Field(None, description="Detalles adicionales")


class RecommendationResponseDTO(BaseModel):
    """DTO para respuesta de recomendaciones."""
    recommendations: List[RecommendationItemDTO]
    total_found: int
    execution_time_ms: int
    metadata: Optional[Dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "recommendations": [
                    {
                        "restaurant": {
                            "id": "R123",
                            "name": "La Rosa Náutica",
                            "category": "Peruana",
                            "rating": 4.5,
                            "reviews": 250,
                            "distance_km": 1.5,
                            "address": "Espigón 4",
                            "district": "Miraflores"
                        },
                        "score": 0.85,
                        "reason": "Excelente opción cerca de ti"
                    }
                ],
                "total_found": 5,
                "execution_time_ms": 145
            }
        }


class RatingPredictionResponseDTO(BaseModel):
    """DTO para respuesta de predicción de rating."""
    restaurant_id: Optional[str] = None
    predicted_rating: float = Field(..., ge=0.0, le=5.0)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    model_used: str
    execution_time_ms: int


class AnalyticsResponseDTO(BaseModel):
    """DTO para respuesta de analytics."""
    total_restaurants: int
    total_categories: int
    total_districts: int
    avg_rating: float
    total_reviews: int
    most_popular_category: Optional[str] = None
    most_popular_district: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponseDTO(BaseModel):
    """DTO para respuestas de error."""
    error: str
    message: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)