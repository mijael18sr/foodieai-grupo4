"""
Domain Entity: Review
Representa una reseña de un restaurante con análisis de sentimiento.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class Sentiment(str, Enum):
    """Enumeración de sentimientos posibles"""
    POSITIVE = "positivo"
    NEUTRAL = "neutro"
    NEGATIVE = "negativo"


@dataclass
class Review:
    """
    Entidad Review que representa una reseña de restaurante.
    Incluye análisis de sentimiento calculado por ML.
    """

    # Identificación
    id: str
    id_place: str

    # Contenido
    comment: str
    rating: int

    # Usuario
    username: str

    # Temporal
    review_date: datetime

    # Análisis de Sentimiento (calculado por ML)
    sentiment: Optional[Sentiment] = None
    sentiment_confidence: Optional[float] = None
    sentiment_probabilities: Optional[dict] = None

    # Metadata
    processed_comment: Optional[str] = None

    def __post_init__(self):
        """Validaciones de negocio"""
        if not 1 <= self.rating <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {self.rating}")

        if self.sentiment_confidence is not None:
            if not 0.0 <= self.sentiment_confidence <= 1.0:
                raise ValueError(f"Confidence must be between 0 and 1, got {self.sentiment_confidence}")

    @property
    def is_positive(self) -> bool:
        """Retorna True si el sentimiento es positivo"""
        return self.sentiment == Sentiment.POSITIVE

    @property
    def is_negative(self) -> bool:
        """Retorna True si el sentimiento es negativo"""
        return self.sentiment == Sentiment.NEGATIVE

    @property
    def is_neutral(self) -> bool:
        """Retorna True si el sentimiento es neutro"""
        return self.sentiment == Sentiment.NEUTRAL

    @property
    def has_high_confidence(self) -> bool:
        """Retorna True si la confianza del análisis es alta (>80%)"""
        return self.sentiment_confidence is not None and self.sentiment_confidence > 0.8

    def __str__(self) -> str:
        sentiment_str = f" [{self.sentiment.value}]" if self.sentiment else ""
        return f"Review {self.id} - Rating: {self.rating}{sentiment_str} - {self.comment[:50]}..."

