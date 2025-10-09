"""
Model Loader
Cargador de modelos ML entrenados.
"""

from pathlib import Path
from typing import Optional
import joblib

from src.ml.models import (
    RestaurantClusteringModel,
    RatingPredictorModel,
    RestaurantRecommenderSystem
)


class MLModelLoader:
    """
    Cargador de modelos ML.

    Maneja la carga de modelos entrenados desde disco.
    Implementa Singleton para no cargar múltiples veces.
    """

    _instance: Optional['MLModelLoader'] = None
    _initialized: bool = False

    def __new__(cls):
        """Implementa Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, models_dir: str = 'data/models'):
        """
        Inicializar loader.

        Args:
            models_dir: Directorio con modelos entrenados
        """
        if not MLModelLoader._initialized:
            self.models_dir = Path(models_dir)
            self._clustering_model = None
            self._rating_model = None
            self._recommender_system = None
            MLModelLoader._initialized = True

    def load_clustering_model(self) -> Optional[RestaurantClusteringModel]:
        """
        Cargar modelo de clustering.

        Returns:
            Modelo cargado o None si no existe
        """
        if self._clustering_model is not None:
            return self._clustering_model

        model_path = self.models_dir / 'clustering_model.pkl'

        if not model_path.exists():
            print(f"⚠️  Clustering model no encontrado: {model_path}")
            return None

        try:
            model = RestaurantClusteringModel()
            model.load(str(model_path))
            self._clustering_model = model
            return model
        except Exception as e:
            print(f"❌ Error cargando clustering model: {e}")
            return None

    def load_rating_model(self) -> Optional[RatingPredictorModel]:
        """
        Cargar modelo de predicción de ratings.

        Returns:
            Modelo cargado o None si no existe
        """
        if self._rating_model is not None:
            return self._rating_model

        model_path = self.models_dir / 'rating_predictor.pkl'

        if not model_path.exists():
            print(f"⚠️  Rating model no encontrado: {model_path}")
            return None

        try:
            model = RatingPredictorModel()
            model.load(str(model_path))
            self._rating_model = model
            return model
        except Exception as e:
            print(f"❌ Error cargando rating model: {e}")
            return None

    def load_recommender_system(self) -> Optional[RestaurantRecommenderSystem]:
        """
        Cargar sistema de recomendación.

        Returns:
            Sistema cargado o None si no existe
        """
        if self._recommender_system is not None:
            return self._recommender_system

        model_path = self.models_dir / 'recommender_system.pkl'

        if not model_path.exists():
            print(f"⚠️  Recommender system no encontrado: {model_path}")
            return None

        try:
            system = RestaurantRecommenderSystem()
            system.load(str(model_path))
            self._recommender_system = system
            return system
        except Exception as e:
            print(f"❌ Error cargando recommender system: {e}")
            return None

    def load_all_models(self) -> dict:
        """
        Cargar todos los modelos disponibles.

        Returns:
            Dict con todos los modelos cargados
        """
        print("🤖 Cargando modelos ML...")

        models = {
            'clustering': self.load_clustering_model(),
            'rating_predictor': self.load_rating_model(),
            'recommender_system': self.load_recommender_system()
        }

        loaded_count = sum(1 for m in models.values() if m is not None)
        print(f"✅ {loaded_count}/3 modelos cargados correctamente")

        return models

    def clear_cache(self):
        """Limpiar caché de modelos (útil para recargar)."""
        self._clustering_model = None
        self._rating_model = None
        self._recommender_system = None
        print("🔄 Caché de modelos limpiada")


# Instancia global
ml_model_loader = MLModelLoader()


# Funciones de conveniencia
def get_clustering_model() -> Optional[RestaurantClusteringModel]:
    """Obtener modelo de clustering."""
    return ml_model_loader.load_clustering_model()


def get_rating_model() -> Optional[RatingPredictorModel]:
    """Obtener modelo de predicción de ratings."""
    return ml_model_loader.load_rating_model()


def get_recommender_system() -> Optional[RestaurantRecommenderSystem]:
    """Obtener sistema de recomendación."""
    return ml_model_loader.load_recommender_system()