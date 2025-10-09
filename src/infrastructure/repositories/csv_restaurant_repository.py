"""
Repository Implementation: CSV Restaurant Repository
Implementación que lee restaurantes desde archivos CSV.
"""

import pandas as pd
import numpy as np
from typing import List, Optional
from pathlib import Path

from src.domain.entities import Restaurant
from src.domain.repositories import RestaurantRepository


class CSVRestaurantRepository(RestaurantRepository):
    """
    Implementación del RestaurantRepository que lee desde CSV.

    Esta implementación cumple el contrato definido en la interface
    RestaurantRepository, pero lee los datos desde un archivo CSV.

    Patrón: Repository Pattern Implementation
    Similar a: JpaRepository implementation en Spring
    """

    def __init__(self, csv_path: str = 'data/processed/restaurantes_sin_anomalias.csv'):
        """
        Inicializa el repositorio cargando el CSV.

        Args:
            csv_path: Ruta al archivo CSV (puede ser relativa o absoluta)
        """
        # Convertir a Path y hacer absoluta si es relativa
        self.csv_path = Path(csv_path)

        # Si la ruta es relativa, hacerla absoluta desde el directorio del proyecto
        if not self.csv_path.is_absolute():
            # Obtener el directorio raíz del proyecto (4 niveles arriba desde este archivo)
            project_root = Path(__file__).parent.parent.parent.parent
            self.csv_path = project_root / csv_path

        self._df: Optional[pd.DataFrame] = None
        self._restaurants_cache: Optional[List[Restaurant]] = None
        self._load_data()

    def _load_data(self) -> None:
        """Carga los datos desde el CSV."""
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.csv_path}\n"
                f"Please run data wrangling first: python scripts/run_data_wrangling.py"
            )

        self._df = pd.read_csv(self.csv_path)
        print(f"✅ Loaded {len(self._df)} restaurants from {self.csv_path}")

    def _row_to_entity(self, row: pd.Series) -> Restaurant:
        """
        Convierte una fila del DataFrame a una entidad Restaurant.

        Args:
            row: Fila del DataFrame

        Returns:
            Restaurant: Entidad Restaurant
        """
        return Restaurant(
            id=str(row['id_place']),
            title=str(row['title']),
            category=str(row['category']),
            address=str(row['address']),
            district=str(row['district']),
            lat=float(row['lat']),
            long=float(row['long']),
            stars=float(row['stars']),
            reviews=int(row['reviews']),
            phone_number=str(row['phoneNumber']) if pd.notna(row.get('phoneNumber')) else None,
            complete_phone_number=str(row['completePhoneNumber']) if pd.notna(row.get('completePhoneNumber')) else None,
            url=str(row['url']) if pd.notna(row.get('url')) else None,
            url_place=str(row['url_place']) if pd.notna(row.get('url_place')) else None,
            domain=str(row['domain']) if pd.notna(row.get('domain')) else None,
        )

    def _get_all_restaurants(self) -> List[Restaurant]:
        """
        Obtiene todos los restaurantes (con cache).

        Returns:
            List[Restaurant]: Lista de todos los restaurantes
        """
        if self._restaurants_cache is None:
            self._restaurants_cache = [
                self._row_to_entity(row)
                for _, row in self._df.iterrows()
            ]
        return self._restaurants_cache

    def find_all(self) -> List[Restaurant]:
        """Obtener todos los restaurantes."""
        return self._get_all_restaurants()

    def find_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        """Buscar restaurante por ID."""
        result = self._df[self._df['id_place'] == restaurant_id]
        if result.empty:
            return None
        return self._row_to_entity(result.iloc[0])

    def find_by_district(self, district: str) -> List[Restaurant]:
        """Buscar restaurantes por distrito."""
        filtered = self._df[self._df['district'].str.lower() == district.lower()]
        return [self._row_to_entity(row) for _, row in filtered.iterrows()]

    def find_by_category(self, category: str) -> List[Restaurant]:
        """Buscar restaurantes por categoría."""
        filtered = self._df[self._df['category'].str.lower() == category.lower()]
        return [self._row_to_entity(row) for _, row in filtered.iterrows()]

    def find_nearby(
            self,
            lat: float,
            long: float,
            radius_km: float
    ) -> List[Restaurant]:
        """
        Buscar restaurantes cercanos usando distancia euclidiana aproximada.

        Nota: Esta es una aproximación simple. Para producción,
        usar fórmula de Haversine o GeoPandas.
        """

        def calculate_distance(row):
            # Aproximación: 1 grado ≈ 111 km
            lat_diff = (row['lat'] - lat) * 111
            long_diff = (row['long'] - long) * 111 * np.cos(np.radians(lat))
            return np.sqrt(lat_diff ** 2 + long_diff ** 2)

        self._df['distance'] = self._df.apply(calculate_distance, axis=1)
        nearby = self._df[self._df['distance'] <= radius_km].copy()
        nearby = nearby.sort_values('distance')

        return [self._row_to_entity(row) for _, row in nearby.iterrows()]

    def find_by_rating(
            self,
            min_rating: float,
            max_rating: float = 5.0
    ) -> List[Restaurant]:
        """Buscar restaurantes por rango de calificación."""
        filtered = self._df[
            (self._df['stars'] >= min_rating) &
            (self._df['stars'] <= max_rating)
            ]
        return [self._row_to_entity(row) for _, row in filtered.iterrows()]

    def find_highly_rated(self, min_rating: float = 4.0) -> List[Restaurant]:
        """Buscar restaurantes altamente calificados."""
        filtered = self._df[self._df['stars'] >= min_rating]
        filtered = filtered.sort_values('stars', ascending=False)
        return [self._row_to_entity(row) for _, row in filtered.iterrows()]

    def find_popular(self, min_reviews: int = 50) -> List[Restaurant]:
        """Buscar restaurantes populares."""
        filtered = self._df[self._df['reviews'] >= min_reviews]
        filtered = filtered.sort_values('reviews', ascending=False)
        return [self._row_to_entity(row) for _, row in filtered.iterrows()]

    def count(self) -> int:
        """Contar total de restaurantes."""
        return len(self._df)

    def get_categories(self) -> List[str]:
        """Obtener lista de categorías únicas."""
        return sorted(self._df['category'].unique().tolist())

    def get_districts(self) -> List[str]:
        """Obtener lista de distritos únicos."""
        return sorted(self._df['district'].unique().tolist())

    def reload(self) -> None:
        """Recargar datos desde el CSV."""
        self._restaurants_cache = None
        self._load_data()