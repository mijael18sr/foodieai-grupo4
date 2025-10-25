"""
Domain Entity: User
Representa un usuario del sistema.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime


@dataclass
class User:
    """Entidad User que representa un usuario que busca recomendaciones."""

    # Identificación
    user_id: str

    # Ubicación actual
    location_lat: float
    location_long: float

    # Preferencias del usuario
    preferences: Dict = field(default_factory=dict)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not (-18.5 <= self.location_lat <= -0.0):
            raise ValueError(f"Latitude outside Peru range: {self.location_lat}")
        if not (-81.5 <= self.location_long <= -68.5):
            raise ValueError(f"Longitude outside Peru range: {self.location_long}")

    def set_preference(self, key: str, value) -> None:
        self.preferences[key] = value

    def get_preference(self, key: str, default=None):
        return self.preferences.get(key, default)

    @property
    def preferred_category(self) -> Optional[str]:
        return self.preferences.get('category')

    @property
    def max_distance_km(self) -> float:
        return self.preferences.get('max_distance_km', 5.0)

    @property
    def min_rating(self) -> float:
        return self.preferences.get('min_rating', 0.0)

    def __str__(self) -> str:
        return f"User {self.user_id} at ({self.location_lat}, {self.location_long})"