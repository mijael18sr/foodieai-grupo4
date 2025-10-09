"""
Domain Package
Contiene las entidades y contratos del dominio de negocio.
"""

from .entities import Restaurant, User, Recommendation
from .repositories import RestaurantRepository, UserRepository

__all__ = [
    # Entities
    'Restaurant',
    'User',
    'Recommendation',

    # Repositories
    'RestaurantRepository',
    'UserRepository',
]