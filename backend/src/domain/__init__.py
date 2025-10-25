"""
Domain Package
Contiene las entidades y contratos del dominio de negocio.
"""

from .entities import Restaurant, User, Recommendation, Review, Sentiment
from .repositories import RestaurantRepository, UserRepository, ReviewRepository

__all__ = [
    # Entities
    'Restaurant',
    'User',
    'Recommendation',
    'Review',
    'Sentiment',

    # Repositories
    'RestaurantRepository',
    'UserRepository',
    'ReviewRepository',
]