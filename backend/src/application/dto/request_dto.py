"""
Request DTOs
Objetos para recibir datos de entrada en la API.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict


class UserLocationDTO(BaseModel):
    """DTO para la ubicación del usuario."""
    lat: float = Field(..., ge=-18.5, le=-0.0, description="Latitud (Perú)")
    long: float = Field(..., ge=-81.5, le=-68.5, description="Longitud (Perú)")


class RecommendationRequestDTO(BaseModel):
    """
    DTO para solicitud de recomendaciones.

    Equivalente a un Request Body en Spring Boot.
    """
    user_location: UserLocationDTO = Field(..., description="Ubicación del usuario")
    preferences: Dict = Field(default_factory=dict, description="Preferencias del usuario")
    filters: Dict = Field(default_factory=dict, description="Filtros de búsqueda")
    top_n: int = Field(default=5, ge=1, le=50, description="Número de recomendaciones")

    class Config:
        json_schema_extra = {
            "example": {
                "user_location": {
                    "lat": -12.0464,
                    "long": -77.0428
                },
                "preferences": {
                    "category": "Italiana"
                },
                "filters": {
                    "min_rating": 4.0,
                    "max_distance_km": 5.0
                },
                "top_n": 5
            }
        }


class RatingPredictionRequestDTO(BaseModel):
    """DTO para solicitud de predicción de rating."""
    restaurant_id: Optional[str] = Field(None, description="ID del restaurante")
    features: Dict = Field(..., description="Features para la predicción")

    class Config:
        json_schema_extra = {
            "example": {
                "restaurant_id": "R123",
                "features": {
                    "category": "Italiana",
                    "district": "Miraflores",
                    "reviews": 100
                }
            }
        }


class NearbySearchRequestDTO(BaseModel):
    """DTO para búsqueda de restaurantes cercanos."""
    location: UserLocationDTO = Field(..., description="Ubicación de búsqueda")
    radius_km: float = Field(default=2.0, ge=0.1, le=50.0, description="Radio en km")
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Rating mínimo")
    category: Optional[str] = Field(None, description="Categoría de comida")

    class Config:
        json_schema_extra = {
            "example": {
                "location": {
                    "lat": -12.0464,
                    "long": -77.0428
                },
                "radius_km": 2.0,
                "min_rating": 4.0,
                "category": "Peruana"
            }
        }
