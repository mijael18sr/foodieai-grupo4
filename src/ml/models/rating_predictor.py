"""
Rating Predictor Model
Modelo de Random Forest para predecir ratings de restaurantes.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Any, Optional
from .base_model import BaseMLModel


class RatingPredictorModel(BaseMLModel):
    """
    Modelo de predicción de ratings usando Random Forest.

    Predice la calificación (stars) de un restaurante basándose en
    sus características (ubicación, categoría, número de reviews, etc.)
    """

    def __init__(
            self,
            n_estimators: int = 100,
            max_depth: Optional[int] = 10,
            random_state: int = 42
    ):
        """
        Inicializar predictor de ratings.

        Args:
            n_estimators: Número de árboles en el bosque
            max_depth: Profundidad máxima de los árboles
            random_state: Semilla para reproducibilidad
        """
        super().__init__(model_name="rating_predictor")
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.feature_names = []

    def train(
            self,
            X: pd.DataFrame,
            y: pd.Series
    ) -> 'RatingPredictorModel':
        """
        Entrenar modelo de predicción de ratings.

        Args:
            X: DataFrame con features
            y: Series con ratings (target)

        Returns:
            self: Modelo entrenado
        """
        print(f"🤖 Entrenando {self.model_name}...")
        print(f"   Datos: {X.shape[0]} registros, {X.shape[1]} features")
        print(f"   Target: ratings de {y.min():.1f} a {y.max():.1f}")

        # Guardar nombres de features
        self.feature_names = list(X.columns)

        # Crear y entrenar modelo
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=-1
        )

        self.model.fit(X, y)

        # Evaluar con validación cruzada
        cv_scores = cross_val_score(
            self.model, X, y,
            cv=5,
            scoring='neg_mean_squared_error'
        )
        cv_rmse = np.sqrt(-cv_scores.mean())

        # Métricas en training set
        y_pred = self.model.predict(X)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        # Feature importance
        feature_importance = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))

        # Guardar metadata
        self.metadata = {
            'n_estimators': self.n_estimators,
            'max_depth': self.max_depth,
            'n_samples': X.shape[0],
            'n_features': X.shape[1],
            'feature_names': self.feature_names,
            'metrics': {
                'train_rmse': float(rmse),
                'train_mae': float(mae),
                'train_r2': float(r2),
                'cv_rmse': float(cv_rmse)
            },
            'feature_importance': {
                k: float(v) for k, v in sorted(
                    feature_importance.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            }
        }

        self.is_trained = True

        print(f"✅ Modelo entrenado exitosamente")
        print(f"   RMSE (train): {rmse:.3f}")
        print(f"   MAE (train): {mae:.3f}")
        print(f"   R² (train): {r2:.3f}")
        print(f"   RMSE (CV): {cv_rmse:.3f}")
        print(f"\n   Top 3 Features:")
        for feat, importance in list(feature_importance.items())[:3]:
            print(f"      {feat}: {importance:.3f}")

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predecir ratings.

        Args:
            X: DataFrame con features

        Returns:
            Array con ratings predichos
        """
        if not self.is_trained:
            raise ValueError("Modelo no entrenado. Ejecuta train() primero.")

        # Asegurar que tenemos las mismas features
        X = X[self.feature_names]

        # Predecir
        predictions = self.model.predict(X)

        # Clip predictions al rango válido [0, 5]
        predictions = np.clip(predictions, 0.0, 5.0)

        return predictions

    def predict_with_confidence(
            self,
            X: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Predecir ratings con intervalos de confianza.

        Args:
            X: DataFrame con features

        Returns:
            Tuple con (predicciones, desviaciones estándar)
        """
        if not self.is_trained:
            raise ValueError("Modelo no entrenado.")

        X = X[self.feature_names]

        # Obtener predicciones de todos los árboles
        all_predictions = np.array([
            tree.predict(X)
            for tree in self.model.estimators_
        ])

        # Calcular media y desviación estándar
        predictions = all_predictions.mean(axis=0)
        std_devs = all_predictions.std(axis=0)

        predictions = np.clip(predictions, 0.0, 5.0)

        return predictions, std_devs