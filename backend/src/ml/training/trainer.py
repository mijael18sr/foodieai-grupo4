"""
Model Training Pipeline
Pipeline para entrenar todos los modelos ML.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
from sklearn.model_selection import train_test_split

from src.ml.models import (
    RestaurantClusteringModel,
    RatingPredictorModel,
    RestaurantRecommenderSystem
)


class ModelTrainer:
    """Pipeline de entrenamiento de modelos ML."""

    def __init__(
            self,
            data_path: str = 'data/processed/restaurantes_sin_anomalias.csv',
            models_dir: str = 'data/models'
    ):
        self.data_path = Path(data_path)
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        self.df = None
        self.clustering_model = None
        self.rating_model = None
        self.recommender_system = None

    def load_data(self) -> pd.DataFrame:
        print("=" * 70)
        print("Cargando datos para entrenamiento...")
        print("=" * 70)

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Datos no encontrados: {self.data_path}\n"
                f"Ejecuta primero: python scripts/run_data_wrangling.py"
            )

        self.df = pd.read_csv(self.data_path)
        print(f"Datos cargados: {len(self.df)} registros")
        print(f"   Columnas: {list(self.df.columns)}")
        print()

        return self.df

    def prepare_features(self) -> Dict[str, pd.DataFrame]:
        print("Preparando features...")
        print("-" * 70)

        clustering_features = self.df[['lat', 'long', 'stars', 'reviews']].copy()
        rating_features = self.df[['lat', 'long', 'reviews']].copy()
        rating_target = self.df['stars'].copy()

        print(f"Clustering features: {clustering_features.shape}")
        print(f"Rating features: {rating_features.shape}")
        print(f"Rating target: {rating_target.shape}")
        print()

        return {
            'clustering_features': clustering_features,
            'rating_features': rating_features,
            'rating_target': rating_target
        }

    def train_clustering_model(
            self,
            features: pd.DataFrame,
            n_clusters: int = 6
    ) -> RestaurantClusteringModel:
        print("\n" + "=" * 70)
        print("ENTRENANDO CLUSTERING MODEL")
        print("=" * 70)

        model = RestaurantClusteringModel(n_clusters=n_clusters)
        model.train(features)

        save_path = self.models_dir / 'clustering_model.pkl'
        model.save(str(save_path))

        self.clustering_model = model
        return model

    def train_rating_model(
            self,
            features: pd.DataFrame,
            target: pd.Series
    ) -> RatingPredictorModel:
        print("\n" + "=" * 70)
        print("ENTRENANDO RATING PREDICTOR")
        print("=" * 70)

        model = RatingPredictorModel(n_estimators=100, max_depth=10)
        model.train(features, target)

        save_path = self.models_dir / 'rating_predictor.pkl'
        model.save(str(save_path))

        self.rating_model = model
        return model

    def build_recommender_system(self) -> RestaurantRecommenderSystem:
        print("\n" + "=" * 70)
        print("CONSTRUYENDO RECOMMENDER SYSTEM")
        print("=" * 70)

        system = RestaurantRecommenderSystem(
            clustering_model=self.clustering_model,
            rating_model=self.rating_model
        )
        system.train()
        system.set_restaurants_data(self.df)

        save_path = self.models_dir / 'recommender_system.pkl'
        system.save(str(save_path))

        self.recommender_system = system
        return system

    def train_all(self) -> Dict[str, Any]:
        print("\n" + "=" * 70)
        print("ENTRENAMIENTO COMPLETO DE MODELOS ML")
        print("=" * 70)

        self.load_data()
        features = self.prepare_features()

        self.train_clustering_model(features['clustering_features'])
        self.train_rating_model(features['rating_features'], features['rating_target'])
        self.build_recommender_system()

        print("\n" + "=" * 70)
        print("ENTRENAMIENTO COMPLETADO")
        print("=" * 70)
        print(f"Modelos guardados en: {self.models_dir}")
        print()

        return {
            'clustering_model': self.clustering_model,
            'rating_model': self.rating_model,
            'recommender_system': self.recommender_system
        }