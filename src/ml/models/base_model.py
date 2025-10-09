"""
Base Model
Clase abstracta base para todos los modelos ML.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import joblib
from pathlib import Path


class BaseMLModel(ABC):
    """
    Clase base abstracta para modelos de Machine Learning.

    Define la interfaz común que deben implementar todos los modelos.
    """

    def __init__(self, model_name: str):
        """
        Inicializar modelo base.

        Args:
            model_name: Nombre identificador del modelo
        """
        self.model_name = model_name
        self.model = None
        self.is_trained = False
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    def train(self, X, y=None) -> 'BaseMLModel':
        """
        Entrenar el modelo.

        Args:
            X: Features de entrenamiento
            y: Target (opcional para modelos no supervisados)

        Returns:
            self: Modelo entrenado
        """
        pass

    @abstractmethod
    def predict(self, X) -> Any:
        """
        Hacer predicciones.

        Args:
            X: Features para predicción

        Returns:
            Predicciones del modelo
        """
        pass

    def save(self, path: str) -> None:
        """
        Guardar modelo en disco.

        Args:
            path: Ruta donde guardar el modelo
        """
        model_path = Path(path)
        model_path.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'model': self.model,
            'metadata': self.metadata,
            'is_trained': self.is_trained,
            'model_name': self.model_name
        }

        joblib.dump(model_data, model_path)
        print(f"✅ Modelo guardado: {model_path}")

    def load(self, path: str) -> 'BaseMLModel':
        """
        Cargar modelo desde disco.

        Args:
            path: Ruta del modelo guardado

        Returns:
            self: Modelo cargado
        """
        model_path = Path(path)

        if not model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")

        model_data = joblib.load(model_path)

        self.model = model_data['model']
        self.metadata = model_data.get('metadata', {})
        self.is_trained = model_data.get('is_trained', False)
        self.model_name = model_data.get('model_name', self.model_name)

        print(f"✅ Modelo cargado: {model_path}")
        return self

    def get_metadata(self) -> Dict[str, Any]:
        """Obtener metadata del modelo."""
        return self.metadata.copy()

    def set_metadata(self, key: str, value: Any) -> None:
        """Establecer valor en metadata."""
        self.metadata[key] = value