"""
Infrastructure Package
Implementaciones de infraestructura (repositorios, configuración, etc.)
"""

from .repositories import CSVRestaurantRepository, MemoryUserRepository
from .container import Container, container, get_restaurant_repository, get_user_repository

__all__ = [
    # Repositories
    'CSVRestaurantRepository',
    'MemoryUserRepository',

    # Container
    'Container',
    'container',
    'get_restaurant_repository',
    'get_user_repository',
]