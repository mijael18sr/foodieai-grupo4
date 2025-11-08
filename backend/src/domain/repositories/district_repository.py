"""
Repositorio abstracto para la gestión de distritos
Define el contrato que debe implementar cualquier repositorio de distritos
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.district import District


class DistrictRepository(ABC):
    """
    Repositorio abstracto para gestionar distritos de Lima
    Sigue los principios de Domain-Driven Design
    """

    @abstractmethod
    async def get_all_districts(self) -> List[District]:
        """
        Obtiene todos los distritos disponibles

        Returns:
            Lista de distritos con información básica
        """
        pass

    @abstractmethod
    async def get_district_by_name(self, name: str) -> Optional[District]:
        """
        Busca un distrito por su nombre

        Args:
            name: Nombre del distrito (ej: "Miraflores", "San_Isidro")

        Returns:
            Distrito encontrado o None si no existe
        """
        pass

    @abstractmethod
    async def get_districts_with_statistics(self) -> List[District]:
        """
        Obtiene distritos con estadísticas completas
        (conteo de restaurantes, rating promedio, etc.)

        Returns:
            Lista de distritos con estadísticas detalladas
        """
        pass

    @abstractmethod
    async def get_popular_districts(self, limit: int = 5) -> List[District]:
        """
        Obtiene los distritos más populares ordenados por número de restaurantes

        Args:
            limit: Número máximo de distritos a retornar

        Returns:
            Lista de distritos ordenados por popularidad
        """
        pass
