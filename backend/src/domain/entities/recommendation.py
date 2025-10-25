"""
Domain Entity: Recommendation
Representa una recomendacion de restaurante.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Recommendation:
    """Entidad Recommendation que representa una recomendacion de restaurante para un usuario."""

    restaurant: 'Restaurant'
    score: float
    distance_km: float
    reason: str
    details: Optional[dict] = None

    def __post_init__(self):
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be between 0 and 1, got {self.score}")
        if self.distance_km < 0:
            raise ValueError(f"Distance cannot be negative, got {self.distance_km}")

    @property
    def is_nearby(self) -> bool:
        return self.distance_km < 2.0

    @property
    def is_excellent(self) -> bool:
        return self.score >= 0.8

    def __str__(self) -> str:
        return (f"{self.restaurant.title} - Score: {self.score:.2f} "
                f"({self.distance_km:.1f}km) - {self.reason}")

    def __lt__(self, other):
        return self.score > other.score
