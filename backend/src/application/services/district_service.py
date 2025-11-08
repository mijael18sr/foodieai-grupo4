"""
Servicio de aplicación para gestión de distritos
Orquesta los casos de uso y maneja la coordinación entre componentes
"""
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
import logging

from ..use_cases.district_use_cases import DistrictUseCases
from ...domain.entities.district import District

logger = logging.getLogger(__name__)


class DistrictService:
    """
    Servicio de aplicación para la gestión de distritos
    Proporciona una interfaz de alto nivel para las operaciones con distritos
    """

    def __init__(self, district_use_cases: DistrictUseCases):
        self._district_use_cases = district_use_cases

    async def get_districts_for_dropdown(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de distritos formateada para el dropdown del frontend

        Returns:
            Lista de diccionarios con información para el componente de selección

        Raises:
            HTTPException: Si hay error al obtener los datos
        """
        try:
            districts = await self._district_use_cases.get_all_districts_for_frontend()

            # Formatear para el frontend
            formatted_districts = []
            for district in districts:
                formatted_districts.append({
                    'value': district.name,
                    'label': district.display_name,
                    'restaurant_count': district.restaurant_count,
                    'description': district.description,
                    'is_tourist_zone': district.is_tourist_zone,
                    'average_rating': float(district.average_rating) if district.average_rating else None
                })

            logger.info(f"Retornando {len(formatted_districts)} distritos para dropdown")
            return formatted_districts

        except Exception as e:
            logger.error(f"Error al obtener distritos para dropdown: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error interno al obtener lista de distritos"
            )

    async def get_district_info(self, district_name: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un distrito específico

        Args:
            district_name: Nombre del distrito

        Returns:
            Información completa del distrito

        Raises:
            HTTPException: Si el distrito no existe o hay error en el procesamiento
        """
        try:
            district = await self._district_use_cases.get_district_details(district_name)

            if not district:
                raise HTTPException(
                    status_code=404,
                    detail=f"Distrito '{district_name}' no encontrado"
                )

            return {
                'name': district.name,
                'display_name': district.display_name,
                'restaurant_count': district.restaurant_count,
                'average_rating': float(district.average_rating) if district.average_rating else None,
                'latitude': float(district.latitude) if district.latitude else None,
                'longitude': float(district.longitude) if district.longitude else None,
                'description': district.description,
                'is_tourist_zone': district.is_tourist_zone,
                'formatted_restaurant_count': district.formatted_restaurant_count
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al obtener información del distrito {district_name}: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error interno al obtener información del distrito"
            )

    async def get_recommended_districts(
        self,
        tourist_zone_only: bool = False,
        min_rating: float = 0.0,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Obtiene distritos recomendados según criterios específicos

        Args:
            tourist_zone_only: Solo incluir zonas turísticas
            min_rating: Rating mínimo promedio
            limit: Número máximo de resultados

        Returns:
            Lista de distritos recomendados
        """
        try:
            preferences = {
                'tourist_zone_only': tourist_zone_only,
                'min_rating': min_rating
            }

            districts = await self._district_use_cases.get_recommended_districts(preferences)

            # Formatear y limitar resultados
            recommended = []
            for district in districts[:limit]:
                recommended.append({
                    'name': district.name,
                    'display_name': district.display_name,
                    'restaurant_count': district.restaurant_count,
                    'average_rating': float(district.average_rating) if district.average_rating else None,
                    'description': district.description,
                    'is_tourist_zone': district.is_tourist_zone
                })

            logger.info(f"Retornando {len(recommended)} distritos recomendados")
            return recommended

        except Exception as e:
            logger.error(f"Error al obtener distritos recomendados: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error interno al obtener recomendaciones de distritos"
            )

    async def validate_district(self, district_name: str) -> bool:
        """
        Valida si un distrito existe en el sistema

        Args:
            district_name: Nombre del distrito a validar

        Returns:
            True si existe, False en caso contrario
        """
        try:
            return await self._district_use_cases.validate_district_exists(district_name)
        except Exception as e:
            logger.error(f"Error al validar distrito {district_name}: {e}")
            return False

    async def get_districts_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de los distritos

        Returns:
            Diccionario con estadísticas de todos los distritos
        """
        try:
            stats = await self._district_use_cases.get_district_statistics_summary()

            logger.info("Generando estadísticas de distritos")
            return {
                'summary': stats,
                'districts': await self.get_districts_for_dropdown()
            }

        except Exception as e:
            logger.error(f"Error al generar estadísticas de distritos: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error interno al generar estadísticas de distritos"
            )
