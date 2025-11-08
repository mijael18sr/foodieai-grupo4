"""
API endpoints para gestión de distritos de Lima
Capa de presentación siguiendo Clean Architecture
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
import logging

from ...application.services.district_service import DistrictService
from ...infrastructure.container import Container

logger = logging.getLogger(__name__)

# Router para endpoints de distritos
router = APIRouter(prefix="/api/districts", tags=["districts"])


# DTOs/Schemas para requests y responses
class DistrictResponse(BaseModel):
    """Schema para respuesta de información de distrito"""
    name: str
    display_name: str
    restaurant_count: int
    average_rating: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    is_tourist_zone: bool
    formatted_restaurant_count: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Miraflores",
                "display_name": "Miraflores",
                "restaurant_count": 185,
                "average_rating": 4.2,
                "latitude": -12.1191,
                "longitude": -77.0286,
                "description": "Distrito turístico con amplia oferta gastronómica y vista al mar",
                "is_tourist_zone": True,
                "formatted_restaurant_count": "185 restaurantes"
            }
        }


class DistrictDropdownItem(BaseModel):
    """Schema para items del dropdown de distritos"""
    value: str = Field(..., description="Valor interno del distrito")
    label: str = Field(..., description="Etiqueta a mostrar en el frontend")
    restaurant_count: int = Field(..., description="Número de restaurantes")
    description: Optional[str] = Field(None, description="Descripción del distrito")
    is_tourist_zone: bool = Field(..., description="Si es zona turística")
    average_rating: Optional[float] = Field(None, description="Rating promedio")

    class Config:
        json_schema_extra = {
            "example": {
                "value": "Miraflores",
                "label": "Miraflores",
                "restaurant_count": 185,
                "description": "Distrito turístico con amplia oferta gastronómica y vista al mar",
                "is_tourist_zone": True,
                "average_rating": 4.2
            }
        }


class DistrictStatistics(BaseModel):
    """Schema para estadísticas de distritos"""
    total_districts: int
    total_restaurants: int
    avg_restaurants_per_district: float
    avg_rating_across_districts: float
    most_popular_district: Optional[str]
    highest_rated_district: Optional[str]


class DistrictStatisticsResponse(BaseModel):
    """Schema para respuesta completa de estadísticas"""
    summary: DistrictStatistics
    districts: List[DistrictDropdownItem]


# Dependency injection
async def get_district_service() -> DistrictService:
    """Obtiene el servicio de distritos desde el contenedor DI"""
    container = Container()
    return container.district_service()


@router.get(
    "/",
    response_model=List[DistrictDropdownItem],
    summary="Obtener lista de distritos",
    description="Retorna la lista completa de distritos de Lima disponibles para el dropdown del frontend, ordenados por popularidad (número de restaurantes)"
)
async def get_districts_list(
    district_service: DistrictService = Depends(get_district_service)
) -> List[DistrictDropdownItem]:
    """
    Obtiene la lista de distritos para el dropdown del frontend

    - **Ordenados por popularidad**: Los distritos con más restaurantes aparecen primero
    - **Información completa**: Incluye conteo de restaurantes, rating promedio y descripción
    - **Optimizado para frontend**: Formato listo para usar en componentes de selección
    """
    logger.info("Solicitando lista de distritos para dropdown")

    districts_data = await district_service.get_districts_for_dropdown()

    # Convertir a modelo Pydantic para validación
    districts = [DistrictDropdownItem(**district) for district in districts_data]

    logger.info(f"Retornando {len(districts)} distritos")
    return districts


@router.get(
    "/{district_name}",
    response_model=DistrictResponse,
    summary="Obtener información de un distrito",
    description="Retorna información detallada de un distrito específico incluyendo estadísticas de restaurantes"
)
async def get_district_details(
    district_name: str,
    district_service: DistrictService = Depends(get_district_service)
) -> DistrictResponse:
    """
    Obtiene información detallada de un distrito específico

    - **district_name**: Nombre del distrito (ej: "Miraflores", "San_Isidro")
    - **Información completa**: Incluye ubicación, estadísticas y descripción
    - **Validación automática**: Retorna 404 si el distrito no existe
    """
    logger.info(f"Solicitando información del distrito: {district_name}")

    district_info = await district_service.get_district_info(district_name)

    return DistrictResponse(**district_info)


@router.get(
    "/recommendations/popular",
    response_model=List[DistrictDropdownItem],
    summary="Obtener distritos recomendados",
    description="Retorna distritos recomendados según criterios específicos de filtrado"
)
async def get_recommended_districts(
    tourist_zone_only: bool = Query(
        False,
        description="Solo incluir zonas turísticas (Miraflores, Barranco, San Isidro)"
    ),
    min_rating: float = Query(
        0.0,
        ge=0.0,
        le=5.0,
        description="Rating mínimo promedio de los restaurantes"
    ),
    limit: int = Query(
        5,
        ge=1,
        le=10,
        description="Número máximo de distritos a retornar"
    ),
    district_service: DistrictService = Depends(get_district_service)
) -> List[DistrictDropdownItem]:
    """
    Obtiene distritos recomendados según criterios de filtrado

    - **tourist_zone_only**: Filtrar solo zonas turísticas principales
    - **min_rating**: Rating mínimo promedio de restaurantes en el distrito
    - **limit**: Máximo número de resultados a retornar
    - **Ordenado por calidad**: Los mejores distritos aparecen primero
    """
    logger.info(f"Solicitando distritos recomendados: tourist_zone={tourist_zone_only}, min_rating={min_rating}")

    recommendations = await district_service.get_recommended_districts(
        tourist_zone_only=tourist_zone_only,
        min_rating=min_rating,
        limit=limit
    )

    # Convertir a modelo Pydantic
    districts = [DistrictDropdownItem(**rec) for rec in recommendations]

    logger.info(f"Retornando {len(districts)} distritos recomendados")
    return districts


@router.get(
    "/statistics/summary",
    response_model=DistrictStatisticsResponse,
    summary="Obtener estadísticas de distritos",
    description="Retorna estadísticas completas de todos los distritos incluyendo métricas agregadas"
)
async def get_districts_statistics(
    district_service: DistrictService = Depends(get_district_service)
) -> DistrictStatisticsResponse:
    """
    Obtiene estadísticas completas de los distritos

    - **Métricas agregadas**: Total de distritos, restaurantes, promedios
    - **Análisis comparativo**: Distrito más popular y mejor valorado
    - **Lista completa**: Todos los distritos con información detallada
    - **Para dashboards**: Ideal para paneles de análisis y visualizaciones
    """
    logger.info("Generando estadísticas completas de distritos")

    stats_data = await district_service.get_districts_statistics()

    return DistrictStatisticsResponse(
        summary=DistrictStatistics(**stats_data['summary']),
        districts=[DistrictDropdownItem(**district) for district in stats_data['districts']]
    )


@router.head(
    "/{district_name}/validate",
    summary="Validar existencia de distrito",
    description="Valida si un distrito existe en el sistema (endpoint HEAD optimizado)"
)
async def validate_district_exists(
    district_name: str,
    district_service: DistrictService = Depends(get_district_service)
):
    """
    Valida la existencia de un distrito (método HEAD para optimización)

    - **Respuesta rápida**: Solo headers HTTP, sin body
    - **200**: El distrito existe
    - **404**: El distrito no existe
    - **Optimizado**: Para validaciones rápidas desde el frontend
    """
    logger.info(f"Validando existencia del distrito: {district_name}")

    exists = await district_service.validate_district(district_name)

    if not exists:
        raise HTTPException(status_code=404, detail="Distrito no encontrado")

    return {"status": "ok"}
