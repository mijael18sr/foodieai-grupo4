"""
Health Check Routes
Endpoints para verificar el estado de la API.
"""

from fastapi import APIRouter, status
from datetime import datetime
from src.infrastructure import get_restaurant_repository

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.

    Verifica que la API está funcionando correctamente.
    """
    try:
        # Verificar que el repositorio está disponible
        repo = get_restaurant_repository()
        restaurant_count = repo.count()

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Restaurant Recommender API",
            "version": "1.0.0",
            "data": {
                "restaurants_loaded": restaurant_count,
                "database_status": "connected"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Readiness check.

    Verifica que la API está lista para recibir requests.
    """
    try:
        repo = get_restaurant_repository()
        repo.count()  # Test query

        return {
            "ready": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception:
        return {
            "ready": False,
            "timestamp": datetime.now().isoformat()
        }


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check.

    Verifica que el proceso está vivo.
    """
    return {
        "alive": True,
        "timestamp": datetime.now().isoformat()
    }