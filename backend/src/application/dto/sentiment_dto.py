"""
Sentiment DTOs
Objetos de transferencia de datos para análisis de sentimientos.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class SentimentAnalysisRequestDTO(BaseModel):
    """DTO para solicitud de análisis de sentimiento de un comentario."""
    comment: str = Field(..., min_length=1, max_length=5000, description="Comentario a analizar")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "La comida estuvo deliciosa y el servicio excelente"
            }
        }


class SentimentAnalysisResponseDTO(BaseModel):
    """DTO para respuesta de análisis de sentimiento."""
    comment: str = Field(..., description="Comentario original")
    sentiment: str = Field(..., description="Sentimiento predicho (positivo/neutro/negativo)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confianza de la predicción")
    confidence_level: Optional[str] = Field(None, description="Nivel de confiabilidad (MUY CONFIABLE/CONFIABLE/MODERADO/BAJA CONFIANZA/INDETERMINADO)")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades por clase")
    processed_text: Optional[str] = Field(None, description="Texto preprocesado")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "La comida estuvo deliciosa y el servicio excelente",
                "sentiment": "positivo",
                "confidence": 0.9234,
                "confidence_level": "MUY CONFIABLE",
                "probabilities": {
                    "positivo": 0.9234,
                    "neutro": 0.0521,
                    "negativo": 0.0245
                },
                "processed_text": "comid delic servici excel"
            }
        }


class ReviewDTO(BaseModel):
    """DTO para una reseña individual."""
    id: str = Field(..., description="ID de la reseña")
    comment: str = Field(..., description="Texto de la reseña")
    rating: int = Field(..., ge=1, le=5, description="Calificación (1-5)")
    username: str = Field(..., description="Nombre del usuario")
    date: Optional[str] = Field(None, description="Fecha de la reseña")
    sentiment: Optional[str] = Field(None, description="Sentimiento analizado")
    confidence: Optional[float] = Field(None, description="Confianza del análisis")


class RestaurantSentimentStatsDTO(BaseModel):
    """DTO para estadísticas de sentimientos de un restaurante."""
    restaurant_id: str = Field(..., description="ID del restaurante")
    total_reviews: int = Field(..., description="Total de reseñas")
    sentiments: Dict[str, int] = Field(..., description="Conteo por sentimiento")
    sentiment_percentages: Dict[str, float] = Field(..., description="Porcentajes por sentimiento")
    avg_confidence: Optional[float] = Field(None, description="Confianza promedio")
    reviews_sample: Optional[List[ReviewDTO]] = Field(None, description="Muestra de reseñas")

    class Config:
        json_schema_extra = {
            "example": {
                "restaurant_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                "total_reviews": 150,
                "sentiments": {
                    "positivo": 120,
                    "neutro": 15,
                    "negativo": 15
                },
                "sentiment_percentages": {
                    "positivo": 80.0,
                    "neutro": 10.0,
                    "negativo": 10.0
                },
                "avg_confidence": 0.8765
            }
        }


class BatchSentimentAnalysisRequestDTO(BaseModel):
    """DTO para análisis de sentimientos en lote."""
    comments: List[str] = Field(..., min_length=1, max_length=100, description="Lista de comentarios")

    class Config:
        json_schema_extra = {
            "example": {
                "comments": [
                    "Excelente comida y servicio",
                    "Muy mala experiencia",
                    "Normal, nada especial"
                ]
            }
        }


class BatchSentimentAnalysisResponseDTO(BaseModel):
    """DTO para respuesta de análisis en lote."""
    total: int = Field(..., description="Total de comentarios analizados")
    results: List[SentimentAnalysisResponseDTO] = Field(..., description="Resultados individuales")
    summary: Dict[str, int] = Field(..., description="Resumen de sentimientos")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 3,
                "results": [
                    {
                        "comment": "Excelente comida",
                        "sentiment": "positivo",
                        "confidence": 0.95,
                        "probabilities": {"positivo": 0.95, "neutro": 0.03, "negativo": 0.02}
                    }
                ],
                "summary": {
                    "positivo": 1,
                    "neutro": 1,
                    "negativo": 1
                }
            }
        }


class SentimentComparisonRequestDTO(BaseModel):
    """DTO para comparación de sentimientos entre restaurantes."""
    restaurant_ids: List[str] = Field(..., min_length=2, max_length=10, description="IDs de restaurantes")

    class Config:
        json_schema_extra = {
            "example": {
                "restaurant_ids": [
                    "ChIJN1t_tDeuEmsRUsoyG83frY4",
                    "ChIJ3S-JXmauEmsRUcIaWtf4MzE"
                ]
            }
        }


class SentimentComparisonResponseDTO(BaseModel):
    """DTO para respuesta de comparación de sentimientos."""
    total_restaurants: int = Field(..., description="Total de restaurantes comparados")
    comparisons: Dict[str, RestaurantSentimentStatsDTO] = Field(..., description="Estadísticas por restaurante")
    ranking: List[Dict] = Field(..., description="Ranking por sentimiento positivo")

    class Config:
        json_schema_extra = {
            "example": {
                "total_restaurants": 2,
                "comparisons": {},
                "ranking": [
                    {
                        "restaurant_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                        "positive_ratio": 0.85,
                        "total_reviews": 150
                    }
                ]
            }
        }


class ModelMetricsPerClassDTO(BaseModel):
    """DTO para métricas por clase de sentimiento."""
    precision: float = Field(..., description="Precisión de la clase")
    recall: float = Field(..., description="Recall de la clase")
    f1_score: float = Field(..., description="F1-Score de la clase")
    support: int = Field(..., description="Número de muestras en test")


class ModelPerformanceMetricsDTO(BaseModel):
    """DTO para métricas completas del modelo de sentimientos."""
    # Métricas generales
    accuracy: float = Field(..., description="Exactitud general del modelo")
    precision_macro: float = Field(..., description="Precisión macro")
    precision_weighted: float = Field(..., description="Precisión ponderada")
    recall_macro: float = Field(..., description="Recall macro")
    recall_weighted: float = Field(..., description="Recall ponderado")
    f1_macro: float = Field(..., description="F1-Score macro")
    f1_weighted: float = Field(..., description="F1-Score ponderado")

    # Métricas avanzadas (equivalentes a R² para clasificación)
    cohen_kappa: Optional[float] = Field(None, description="Coeficiente Kappa de Cohen (equivalente a R² para clasificación)")
    matthews_corrcoef: Optional[float] = Field(None, description="Coeficiente de correlación de Matthews")

    # Métricas por clase
    per_class_metrics: Dict[str, ModelMetricsPerClassDTO] = Field(
        ...,
        description="Métricas detalladas por clase de sentimiento"
    )

    # Información adicional
    last_evaluation: Optional[str] = Field(None, description="Fecha de última evaluación")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "SentimentAnalysisModel",
                "model_type": "Complement Naive Bayes",
                "accuracy": 0.8550,
                "precision_weighted": 0.8567,
                "recall_weighted": 0.8550,
                "f1_score_weighted": 0.8545,
                "cohen_kappa": 0.7825,
                "matthews_corrcoef": 0.7831,
                "metrics_per_class": {
                    "positivo": {
                        "precision": 0.9012,
                        "recall": 0.9234,
                        "f1_score": 0.9122,
                        "support": 850
                    },
                    "neutro": {
                        "precision": 0.6543,
                        "recall": 0.6012,
                        "f1_score": 0.6267,
                        "support": 120
                    },
                    "negativo": {
                        "precision": 0.8234,
                        "recall": 0.7890,
                        "f1_score": 0.8058,
                        "support": 230
                    }
                },
                "total_samples": 1200,
                "training_date": "2025-10-22",
                "vocab_size": 5000
            }
        }
