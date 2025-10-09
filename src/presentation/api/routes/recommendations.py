"""
Recommendations Routes
Endpoints para recomendaciones de restaurantes.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.application import RecommendationService, RecommendationRequestDTO, RecommendationResponseDTO
from src.infrastructure import get_restaurant_repository
from src.domain.repositories import RestaurantRepository

router = APIRouter()


def get_recommendation_service(
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repository)
) -> RecommendationService:
    """
    Dependency provider para RecommendationService.

    Equivalente a @Autowired en Spring Boot.
    """
    return RecommendationService(restaurant_repo)


@router.post(
    "/recommendations",
    response_model=RecommendationResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Obtener recomendaciones personalizadas",
    description="Genera recomendaciones de restaurantes basadas en ubicación y preferencias del usuario."
)
async def get_recommendations(
        request: RecommendationRequestDTO,
        service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Endpoint principal de recomendaciones.

    **Parámetros:**
    - user_location: Ubicación del usuario (lat, long)
    - preferences: Preferencias del usuario (categoría, etc.)
    - filters: Filtros de búsqueda (min_rating, max_distance_km, district)
    - top_n: Número de recomendaciones deseadas (1-50)

    **Respuesta:**
    - Lista de restaurantes recomendados ordenados por score
    - Cada recomendación incluye score, distancia y razón
    - Metadata con información de la búsqueda
    """
    try:
        response = service.get_recommendations(request)
        return response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get(
    "/restaurants/categories",
    response_model=list[str],
    summary="Obtener categorías disponibles",
    description="Lista todas las categorías de restaurantes disponibles."
)
async def get_categories(
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repository)
):
    """Obtener lista de categorías."""
    try:
        categories = restaurant_repo.get_categories()
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/restaurants/districts",
    response_model=list[str],
    summary="Obtener distritos disponibles",
    description="Lista todos los distritos con restaurantes."
)
async def get_districts(
        restaurant_repo: RestaurantRepository = Depends(get_restaurant_repository)
):
    """Obtener lista de distritos."""
    try:
        districts = restaurant_repo.get_districts()
        return districts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )