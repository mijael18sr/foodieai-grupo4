"""
Review Repository Interface
Define el contrato para acceder a las reseñas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Review


class ReviewRepository(ABC):
    """
    Interfaz del repositorio de reseñas.
    Define operaciones para acceder a las reseñas (Port en arquitectura hexagonal).
    """

    @abstractmethod
    def find_by_id(self, review_id: str) -> Optional[Review]:
        """Buscar reseña por ID"""
        pass

    @abstractmethod
    def find_by_restaurant(self, restaurant_id: str) -> List[Review]:
        """Buscar todas las reseñas de un restaurante"""
        pass

    @abstractmethod
    def find_by_sentiment(self, sentiment: str) -> List[Review]:
        """Buscar reseñas por sentimiento"""
        pass

    @abstractmethod
    def find_all(self, limit: Optional[int] = None) -> List[Review]:
        """Obtener todas las reseñas"""
        pass

    @abstractmethod
    def save(self, review: Review) -> Review:
        """Guardar una reseña"""
        pass

    @abstractmethod
    def count_by_restaurant(self, restaurant_id: str) -> int:
        """Contar reseñas de un restaurante"""
        pass

    @abstractmethod
    def get_sentiment_stats(self, restaurant_id: str) -> dict:
        """Obtener estadísticas de sentimientos para un restaurante"""
        pass

