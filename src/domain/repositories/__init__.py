"""
Domain Repositories Package
Contiene las interfaces de los repositorios (contratos).
"""

from .restaurant_repository import RestaurantRepository
from .user_repository import UserRepository

__all__ = [
    'RestaurantRepository',
    'UserRepository',
]