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
    """
    Pipeline de entrenamiento de modelos ML.

    Coordina el entrenamiento de todos los modelos y guarda
    los resultados.
    """

    def __init__(
            self,
            data_path: str = 'data/processed/restaurantes_sin_anomalias.csv',
            models_dir: str = 'data/models'
    ):
        """
        Inicializar trainer.

        Args:
            data_path: Ruta al CSV limpio
            models_dir: Directorio donde guardar modelos
        """
        self.data_path = Path(data_path)
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        self.df = None
        self.clustering_model = None
        self.rating_model = None
        self.recommender_system = None

    def load_data(self) -> pd.DataFrame:
        """Cargar datos para entrenamiento."""
        print("=" * 70)
        print("📂 Cargando datos para entrenamiento...")
        print("=" * 70)

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Datos no encontrados: {self.data_path}\n"
                f"Ejecuta primero: python scripts/run_data_wrangling.py"
            )

        self.df = pd.read_csv(self.data_path)
        print(f"✅ Datos cargados: {len(self.df)} registros")
        print(f"   Columnas: {list(self.df.columns)}")
        print()

        return self.df

    def prepare_features(self) -> Dict[str, pd.DataFrame]:
        """
        Preparar features para diferentes modelos.

        Returns:
            Dict con features preparadas
        """
        print("🔧 Preparando features...")
        print("-" * 70)

        # Features para clustering (numéricas)
        clustering_features = self.df[['lat', 'long', 'stars', 'reviews']].copy()

        # Features para rating prediction
        rating_features = self.df[['lat', 'long', 'reviews']].copy()
        rating_target = self.df['stars'].copy()

        print(f"✅ Clustering features: {clustering_features.shape}")
        print(f"✅ Rating features: {rating_features.shape}")
        print(f"✅ Rating target: {rating_target.shape}")
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
        """
        Entrenar modelo de clustering.

        Args:
            features: Features para clustering
            n_clusters: Número de clusters

        Returns:
            Modelo entrenado
        """
        print("=" * 70)
        print("🎯 ENTRENANDO: Clustering Model (K-Means)")
        print("=" * 70)

        model = RestaurantClusteringModel(n_clusters=n_clusters)
        model.train(features)

        # Guardar modelo
        model_path = self.models_dir / 'clustering_model.pkl'
        model.save(model_path)

        self.clustering_model = model
        print()

        return model

    def train_rating_model(
            self,
            features: pd.DataFrame,
            target: pd.Series
    ) -> RatingPredictorModel:
        """
        Entrenar modelo de predicción de ratings.

        Args:
            features: Features para predicción
            target: Target (ratings)

        Returns:
            Modelo entrenado
        """
        print("=" * 70)
        print("🎯 ENTRENANDO: Rating Predictor (Random Forest)")
        print("=" * 70)

        model = RatingPredictorModel(n_estimators=100, max_depth=10)
        model.train(features, target)

        # Guardar modelo
        model_path = self.models_dir / 'rating_predictor.pkl'
        model.save(model_path)

        self.rating_model = model
        print()

        return model

    def create_recommender_system(self) -> RestaurantRecommenderSystem:
        """
        Crear sistema de recomendación con modelos entrenados.

        Returns:
            Sistema de recomendación
        """
        print("=" * 70)
        print("🎯 CREANDO: Recommender System")
        print("=" * 70)

        recommender = RestaurantRecommenderSystem(
            clustering_model=self.clustering_model,
            rating_model=self.rating_model
        )

        recommender.set_restaurants_data(self.df)
        recommender.train()

        # Guardar sistema
        system_path = self.models_dir / 'recommender_system.pkl'
        recommender.save(system_path)

        self.recommender_system = recommender
        print()

        return recommender

    def train_all(self) -> Dict[str, Any]:
        """
        Entrenar todos los modelos en secuencia.

        Returns:
            Dict con todos los modelos entrenados
        """
        print("\n")
        print("=" * 70)
        print("🚀 INICIANDO ENTRENAMIENTO COMPLETO DE MODELOS ML")
        print("=" * 70)
        print()

        # 1. Cargar datos
        self.load_data()

        # 2. Preparar features
        features_dict = self.prepare_features()

        # 3. Entrenar clustering
        clustering_model = self.train_clustering_model(
            features_dict['clustering_features']
        )

        # 4. Entrenar rating predictor
        rating_model = self.train_rating_model(
            features_dict['rating_features'],
            features_dict['rating_target']
        )

        # 5. Crear recommender system
        recommender = self.create_recommender_system()

        # Resumen final
        print("=" * 70)
        print("✅ ENTRENAMIENTO COMPLETADO")
        print("=" * 70)
        print(f"\n📁 Modelos guardados en: {self.models_dir}")
        print(f"   1. clustering_model.pkl")
        print(f"   2. rating_predictor.pkl")
        print(f"   3. recommender_system.pkl")
        print()

        return {
            'clustering_model': clustering_model,
            'rating_model': rating_model,
            'recommender_system': recommender
        }