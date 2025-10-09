"""
Domain Entities Package
Contiene las entidades de negocio del sistema.
"""

from .restaurant import Restaurant
from .user import User
from .recommendation import Recommendation

__all__ = [
    'Restaurant',
    'User',
    'Recommendation',
]