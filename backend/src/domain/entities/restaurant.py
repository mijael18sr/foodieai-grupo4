"""
Domain Entity: Restaurant
Representa un restaurante en el sistema.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Restaurant:
    """
    Entidad Restaurant - Equivalente a @Entity en Spring Boot
    Representa un restaurante con toda su información.
    """

    # Identificación
    id: str
    title: str

    # Categorización
    category: str

    # Ubicación
    address: str
    district: str
    lat: float
    long: float

    # Calificaciones
    stars: float
    reviews: int

    # Contacto (opcionales)
    phone_number: Optional[str] = None
    complete_phone_number: Optional[str] = None
    url: Optional[str] = None
    url_place: Optional[str] = None
    domain: Optional[str] = None

    # Metadata
    created_at: datetime = None

    def __post_init__(self):
        """Validaciones de negocio"""
        if self.stars < 0 or self.stars > 5:
            raise ValueError(f"Stars must be between 0 and 5, got {self.stars}")

        if self.reviews < 0:
            raise ValueError(f"Reviews cannot be negative, got {self.reviews}")

        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def is_highly_rated(self) -> bool:
        """Determina si el restaurante está altamente calificado"""
        return self.stars >= 4.0

    @property
    def is_popular(self) -> bool:
        """Determina si el restaurante es popular (muchas reviews)"""
        return self.reviews >= 50

    @property
    def has_contact_info(self) -> bool:
        """Verifica si tiene información de contacto"""
        return self.phone_number is not None or self.url is not None

    def __str__(self) -> str:
        return f"{self.title} ({self.category}) - {self.stars} stars ({self.reviews} reviews)"
