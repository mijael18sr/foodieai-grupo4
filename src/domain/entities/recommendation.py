"""
Domain Entity: Recommendation
Representa una recomendación de restaurante.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Recommendation:
    """
    Entidad Recommendation
    Representa una recomendación de restaurante para un usuario.
    """

    # Restaurante recomendado
    restaurant: 'Restaurant'  # Forward reference

    # Score de recomendación (0.0 - 1.0)
    score: float

    # Distancia desde la ubicación del usuario (en km)
    distance_km: float

    # Razón de la recomendación
    reason: str

    # Detalles adicionales (opcional)
    details: Optional[dict] = None

    def __post_init__(self):
        """Validaciones"""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Score must be between 0 and 1, got {self.score}")

        if self.distance_km < 0:
            raise ValueError(f"Distance cannot be negative, got {self.distance_km}")

    @property
    def is_nearby(self) -> bool:
        """Determina si el restaurante está cerca (< 2km)"""
        return self.distance_km < 2.0

    @property
    def is_excellent(self) -> bool:
        """Determina si es una excelente recomendación"""
        return self.score >= 0.8

    def __str__(self) -> str:
        return (f"{self.restaurant.title} - Score: {self.score:.2f} "
                f"({self.distance_km:.1f}km) - {self.reason}")

    def __lt__(self, other):
        """Permite ordenar recomendaciones por score (mayor a menor)"""
        return self.score > other.score  # Invertido para orden descendente