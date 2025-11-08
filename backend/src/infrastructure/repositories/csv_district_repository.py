"""
Implementación concreta del repositorio de distritos
Accede a los datos reales del CSV de restaurantes
"""
import pandas as pd
from typing import List, Optional
from decimal import Decimal
from pathlib import Path
import asyncio
from functools import lru_cache

from ...domain.entities.district import District
from ...domain.repositories.district_repository import DistrictRepository


class CSVDistrictRepository(DistrictRepository):
    """
    Implementación del repositorio de distritos que lee desde archivos CSV
    Optimizado con cache para mejorar performance
    """

    def __init__(self, data_path: str = "data/processed/restaurantes_limpio.csv"):
        self.data_path = Path(data_path)
        self._df_cache: Optional[pd.DataFrame] = None

    @property
    async def _df(self) -> pd.DataFrame:
        """
        Lazy loading del DataFrame con cache
        """
        if self._df_cache is None:
            # Ejecutar la carga de CSV en un thread separado para no bloquear
            loop = asyncio.get_event_loop()
            self._df_cache = await loop.run_in_executor(
                None,
                self._load_restaurant_data
            )
        return self._df_cache

    def _load_restaurant_data(self) -> pd.DataFrame:
        """
        Carga los datos de restaurantes desde CSV
        """
        try:
            df = pd.read_csv(self.data_path)
            # Validar que tiene las columnas necesarias
            required_columns = ['district', 'stars']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(f"Columnas faltantes en CSV: {missing_columns}")

            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo de datos no encontrado: {self.data_path}")
        except Exception as e:
            raise Exception(f"Error al cargar datos de restaurantes: {e}")

    async def get_all_districts(self) -> List[District]:
        """
        Obtiene todos los distritos únicos del dataset
        """
        df = await self._df

        unique_districts = df['district'].unique()
        districts = []

        for district_name in unique_districts:
            if pd.isna(district_name):
                continue

            # Crear distrito básico sin estadísticas
            district = District(
                name=district_name,
                display_name=self._format_display_name(district_name),
                restaurant_count=0  # Se calculará en get_districts_with_statistics
            )
            districts.append(district)

        return sorted(districts, key=lambda d: d.display_name)

    async def get_district_by_name(self, name: str) -> Optional[District]:
        """
        Busca un distrito específico con estadísticas completas
        """
        df = await self._df

        # Filtrar restaurantes del distrito
        district_data = df[df['district'].str.lower() == name.lower()]

        if district_data.empty:
            return None

        # Calcular estadísticas
        restaurant_count = len(district_data)
        avg_rating = district_data['stars'].mean() if 'stars' in district_data.columns else None

        # Coordenadas promedio (si existen en el dataset)
        latitude = None
        longitude = None
        if 'lat' in district_data.columns and 'long' in district_data.columns:
            latitude = Decimal(str(district_data['lat'].mean()))
            longitude = Decimal(str(district_data['long'].mean()))

        return District(
            name=name,
            display_name=self._format_display_name(name),
            restaurant_count=restaurant_count,
            average_rating=Decimal(str(avg_rating)) if avg_rating else None,
            latitude=latitude,
            longitude=longitude,
            description=self._get_district_description(name)
        )

    async def get_districts_with_statistics(self) -> List[District]:
        """
        Obtiene todos los distritos con estadísticas completas
        """
        df = await self._df

        # Agrupar por distrito y calcular estadísticas
        district_stats = df.groupby('district').agg({
            'stars': ['count', 'mean'],
            'lat': 'mean',
            'long': 'mean'
        }).reset_index()

        # Aplanar nombres de columnas
        district_stats.columns = [
            'district', 'restaurant_count', 'avg_rating', 'avg_latitude', 'avg_longitude'
        ]

        districts = []
        for _, row in district_stats.iterrows():
            district_name = row['district']
            if pd.isna(district_name):
                continue

            district = District(
                name=district_name,
                display_name=self._format_display_name(district_name),
                restaurant_count=int(row['restaurant_count']),
                average_rating=Decimal(str(row['avg_rating'])) if not pd.isna(row['avg_rating']) else None,
                latitude=Decimal(str(row['avg_latitude'])) if not pd.isna(row['avg_latitude']) else None,
                longitude=Decimal(str(row['avg_longitude'])) if not pd.isna(row['avg_longitude']) else None,
                description=self._get_district_description(district_name)
            )
            districts.append(district)

        return districts

    async def get_popular_districts(self, limit: int = 5) -> List[District]:
        """
        Obtiene los distritos más populares por número de restaurantes
        """
        districts = await self.get_districts_with_statistics()

        # Ordenar por número de restaurantes descendente
        popular_districts = sorted(
            districts,
            key=lambda d: d.restaurant_count,
            reverse=True
        )

        return popular_districts[:limit]

    def _format_display_name(self, district_name: str) -> str:
        """
        Formatea el nombre del distrito para display en el frontend
        """
        display_mappings = {
            'San_Isidro': 'San Isidro',
            'Miraflores': 'Miraflores',
            'Barranco': 'Barranco',
            'Lince': 'Lince',
            'Magdalena': 'Magdalena del Mar',
            'Surquillo': 'Surquillo',
            'Surco': 'Santiago de Surco'
        }

        return display_mappings.get(district_name, district_name)

    @lru_cache(maxsize=128)
    def _get_district_description(self, district_name: str) -> str:
        """
        Obtiene descripción del distrito para contexto adicional
        """
        descriptions = {
            'Miraflores': 'Distrito turístico con amplia oferta gastronómica y vista al mar',
            'San_Isidro': 'Distrito financiero con restaurantes de alta gama y cocina internacional',
            'Barranco': 'Distrito bohemio conocido por su vida nocturna y gastronomía creativa',
            'Lince': 'Distrito residencial con variada oferta gastronómica local',
            'Magdalena': 'Distrito costero con restaurantes tradicionales y marisquerías',
            'Surquillo': 'Distrito con mercados gastronómicos y cocina popular',
            'Surco': 'Distrito moderno con centros comerciales y restaurantes familiares'
        }

        return descriptions.get(district_name, f'Distrito con diversa oferta gastronómica en Lima')

    def clear_cache(self):
        """
        Limpia el cache del DataFrame para recargar datos frescos
        """
        self._df_cache = None
        self._get_district_description.cache_clear()
