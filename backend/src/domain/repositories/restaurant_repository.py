"""
Repository Interface: Restaurant Repository
Define el contrato para acceso a datos de restaurantes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Restaurant


class RestaurantRepository(ABC):
    """Interface del Repository de Restaurantes."""

    @abstractmethod
    def find_all(self) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        pass

    @abstractmethod
    def find_by_district(self, district: str) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_by_category(self, category: str) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_nearby(self, lat: float, long: float, radius_km: float) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_by_rating(self, min_rating: float, max_rating: float = 5.0) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_highly_rated(self, min_rating: float = 4.0) -> List[Restaurant]:
        pass

    @abstractmethod
    def find_popular(self, min_reviews: int = 50) -> List[Restaurant]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def get_categories(self) -> List[str]:
        pass

    @abstractmethod
    def get_districts(self) -> List[str]:
        pass