"""
Entidad del dominio para Distrito
Representa un distrito de Lima con sus características principales
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass(frozen=True)
class District:
    """
    Entidad que representa un distrito de Lima

    Attributes:
        name: Nombre del distrito (ej: "Miraflores", "San_Isidro")
        display_name: Nombre para mostrar al usuario (ej: "Miraflores", "San Isidro")
        restaurant_count: Número total de restaurantes en el distrito
        average_rating: Rating promedio de los restaurantes del distrito
        latitude: Latitud central del distrito
        longitude: Longitud central del distrito
        description: Descripción breve del distrito
    """
    name: str
    display_name: str
    restaurant_count: int
    average_rating: Optional[Decimal] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    description: Optional[str] = None

    def __post_init__(self):
        """Validaciones de negocio"""
        if not self.name:
            raise ValueError("El nombre del distrito es requerido")

        if self.restaurant_count < 0:
            raise ValueError("El conteo de restaurantes no puede ser negativo")

        if self.average_rating is not None and (self.average_rating < 0 or self.average_rating > 5):
            raise ValueError("El rating promedio debe estar entre 0 y 5")

    @property
    def is_tourist_zone(self) -> bool:
        """Determina si el distrito es zona turística"""
        tourist_districts = {"Miraflores", "Barranco", "San_Isidro"}
        return self.name in tourist_districts

    @property
    def formatted_restaurant_count(self) -> str:
        """Formato amigable del conteo de restaurantes"""
        return f"{self.restaurant_count} restaurante{'s' if self.restaurant_count != 1 else ''}"

    def __str__(self) -> str:
        return f"Distrito {self.display_name} ({self.formatted_restaurant_count})"
