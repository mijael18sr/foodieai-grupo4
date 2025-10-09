"""
Repository Interface: Restaurant Repository
Define el contrato para acceso a datos de restaurantes.
Equivalente a @Repository en Spring Boot.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Restaurant


class RestaurantRepository(ABC):
    """
    Interface del Repository de Restaurantes.

    Define los métodos que debe implementar cualquier repositorio
    de restaurantes, sin importar la fuente de datos (CSV, DB, API, etc.)

    Patrón: Repository Pattern
    Similar a: Spring Data JpaRepository
    """

    @abstractmethod
    def find_all(self) -> List[Restaurant]:
        """
        Obtener todos los restaurantes.

        Returns:
            List[Restaurant]: Lista de todos los restaurantes
        """
        pass

    @abstractmethod
    def find_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        """
        Buscar restaurante por ID.

        Args:
            restaurant_id: ID único del restaurante

        Returns:
            Optional[Restaurant]: Restaurante encontrado o None
        """
        pass

    @abstractmethod
    def find_by_district(self, district: str) -> List[Restaurant]:
        """
        Buscar restaurantes por distrito.

        Args:
            district: Nombre del distrito

        Returns:
            List[Restaurant]: Lista de restaurantes en el distrito
        """
        pass

    @abstractmethod
    def find_by_category(self, category: str) -> List[Restaurant]:
        """
        Buscar restaurantes por categoría.

        Args:
            category: Categoría/tipo de comida

        Returns:
            List[Restaurant]: Lista de restaurantes de esa categoría
        """
        pass

    @abstractmethod
    def find_nearby(
            self,
            lat: float,
            long: float,
            radius_km: float
    ) -> List[Restaurant]:
        """
        Buscar restaurantes cercanos a una ubicación.

        Args:
            lat: Latitud
            long: Longitud
            radius_km: Radio de búsqueda en kilómetros

        Returns:
            List[Restaurant]: Lista de restaurantes cercanos
        """
        pass

    @abstractmethod
    def find_by_rating(
            self,
            min_rating: float,
            max_rating: float = 5.0
    ) -> List[Restaurant]:
        """
        Buscar restaurantes por rango de calificación.

        Args:
            min_rating: Calificación mínima
            max_rating: Calificación máxima (default: 5.0)

        Returns:
            List[Restaurant]: Lista de restaurantes en el rango
        """
        pass

    @abstractmethod
    def find_highly_rated(self, min_rating: float = 4.0) -> List[Restaurant]:
        """
        Buscar restaurantes altamente calificados.

        Args:
            min_rating: Calificación mínima (default: 4.0)

        Returns:
            List[Restaurant]: Lista de restaurantes con alta calificación
        """
        pass

    @abstractmethod
    def find_popular(self, min_reviews: int = 50) -> List[Restaurant]:
        """
        Buscar restaurantes populares (muchas reviews).

        Args:
            min_reviews: Número mínimo de reviews (default: 50)

        Returns:
            List[Restaurant]: Lista de restaurantes populares
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """
        Contar total de restaurantes.

        Returns:
            int: Número total de restaurantes
        """
        pass

    @abstractmethod
    def get_categories(self) -> List[str]:
        """
        Obtener lista de categorías únicas.

        Returns:
            List[str]: Lista de categorías disponibles
        """
        pass

    @abstractmethod
    def get_districts(self) -> List[str]:
        """
        Obtener lista de distritos únicos.

        Returns:
            List[str]: Lista de distritos disponibles
        """
        pass