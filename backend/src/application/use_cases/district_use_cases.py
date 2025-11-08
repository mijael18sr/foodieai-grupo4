"""
Casos de uso para la gestión de distritos
Implementa la lógica de negocio siguiendo Clean Architecture
"""
from typing import List, Optional
from decimal import Decimal
from src.domain.entities.district import District
from src.domain.repositories.district_repository import DistrictRepository


class DistrictUseCases:
    """
    Casos de uso para la gestión de distritos de Lima
    Encapsula toda la lógica de negocio relacionada con distritos
    """

    def __init__(self, district_repository: DistrictRepository):
        self._district_repository = district_repository

    async def get_all_districts_for_frontend(self) -> List[District]:
        """
        Obtiene todos los distritos optimizados para el frontend
        Incluye información de display y conteos

        Returns:
            Lista de distritos con información para el dropdown del frontend
        """
        districts = await self._district_repository.get_districts_with_statistics()

        # Ordenar por número de restaurantes (descendente) para mostrar los más populares primero
        sorted_districts = sorted(
            districts,
            key=lambda d: d.restaurant_count,
            reverse=True
        )

        return sorted_districts

    async def get_district_details(self, district_name: str) -> Optional[District]:
        """
        Obtiene detalles completos de un distrito específico

        Args:
            district_name: Nombre del distrito

        Returns:
            Distrito con información completa o None si no existe
        """
        if not district_name or district_name.strip() == "":
            return None

        # Normalizar el nombre del distrito para búsqueda flexible
        normalized_name = self._normalize_district_name(district_name)

        district = await self._district_repository.get_district_by_name(normalized_name)

        return district

    async def get_recommended_districts(self, user_preferences: Optional[dict] = None) -> List[District]:
        """
        Obtiene distritos recomendados basado en preferencias del usuario

        Args:
            user_preferences: Preferencias del usuario (zona turística, rating mínimo, etc.)

        Returns:
            Lista de distritos recomendados
        """
        all_districts = await self._district_repository.get_districts_with_statistics()

        # Si no hay preferencias, retornar los más populares
        if not user_preferences:
            return await self._district_repository.get_popular_districts()

        filtered_districts = []
        min_rating = user_preferences.get('min_rating', 0)
        tourist_only = user_preferences.get('tourist_zone_only', False)

        for district in all_districts:
            # Filtrar por rating mínimo
            if district.average_rating and district.average_rating < Decimal(str(min_rating)):
                continue

            # Filtrar por zona turística si se requiere
            if tourist_only and not district.is_tourist_zone:
                continue

            filtered_districts.append(district)

        # Ordenar por rating y luego por número de restaurantes
        filtered_districts.sort(
            key=lambda d: (d.average_rating or Decimal('0'), d.restaurant_count),
            reverse=True
        )

        return filtered_districts

    async def validate_district_exists(self, district_name: str) -> bool:
        """
        Valida que un distrito existe en el sistema

        Args:
            district_name: Nombre del distrito a validar

        Returns:
            True si el distrito existe, False en caso contrario
        """
        if not district_name:
            return False

        district = await self.get_district_details(district_name)
        return district is not None

    def _normalize_district_name(self, name: str) -> str:
        """
        Normaliza el nombre del distrito para búsquedas consistentes

        Args:
            name: Nombre original del distrito

        Returns:
            Nombre normalizado
        """
        # Mapeo de nombres comunes a nombres del dataset
        name_mappings = {
            'san isidro': 'San_Isidro',
            'san_isidro': 'San_Isidro',
            'miraflores': 'Miraflores',
            'barranco': 'Barranco',
            'lince': 'Lince',
            'magdalena': 'Magdalena',
            'surquillo': 'Surquillo',
            'surco': 'Surco'
        }

        normalized = name.lower().strip()
        return name_mappings.get(normalized, name.title())

    async def get_district_statistics_summary(self) -> dict:
        """
        Obtiene un resumen estadístico de todos los distritos

        Returns:
            Diccionario con estadísticas generales de distritos
        """
        districts = await self._district_repository.get_districts_with_statistics()

        total_restaurants = sum(d.restaurant_count for d in districts)
        avg_restaurants_per_district = total_restaurants / len(districts) if districts else 0

        ratings = [d.average_rating for d in districts if d.average_rating]
        avg_rating_across_districts = sum(ratings) / len(ratings) if ratings else Decimal('0')

        return {
            'total_districts': len(districts),
            'total_restaurants': total_restaurants,
            'avg_restaurants_per_district': round(avg_restaurants_per_district, 1),
            'avg_rating_across_districts': round(float(avg_rating_across_districts), 2),
            'most_popular_district': max(districts, key=lambda d: d.restaurant_count).name if districts else None,
            'highest_rated_district': max(districts, key=lambda d: d.average_rating or Decimal('0')).name if districts else None
        }
