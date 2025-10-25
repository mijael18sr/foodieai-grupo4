"""
Clustering Model
Modelo de K-Means para agrupar restaurantes similares.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Optional, Dict, Any
from .base_model import BaseMLModel


class RestaurantClusteringModel(BaseMLModel):
    """Modelo de clustering para agrupar restaurantes similares."""

    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        super().__init__(model_name="restaurant_clustering")
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names = []

    def train(self, X: pd.DataFrame, y=None) -> 'RestaurantClusteringModel':
        print(f"Entrenando {self.model_name}...")
        print(f"   Datos: {X.shape[0]} registros, {X.shape[1]} features")
        print(f"   Clusters objetivo: {self.n_clusters}")

        self.feature_names = list(X.columns)
        X_scaled = self.scaler.fit_transform(X)

        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )

        self.model.fit(X_scaled)

        labels = self.model.labels_
        silhouette = silhouette_score(X_scaled, labels)
        inertia = self.model.inertia_

        self.metadata = {
            'n_clusters': self.n_clusters,
            'silhouette_score': float(silhouette),
            'inertia': float(inertia),
            'n_samples': X.shape[0],
            'n_features': X.shape[1],
            'feature_names': self.feature_names,
            'cluster_sizes': {
                int(i): int(count)
                for i, count in enumerate(np.bincount(labels))
            }
        }

        self.is_trained = True

        print(f"Modelo entrenado exitosamente")
        print(f"   Silhouette Score: {silhouette:.3f}")
        print(f"   Inertia: {inertia:.2f}")
        print(f"   Tamanos de clusters: {self.metadata['cluster_sizes']}")

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_trained:
            raise ValueError("Modelo no entrenado. Ejecuta train() primero.")

        X = X[self.feature_names]
        X_scaled = self.scaler.transform(X)
        clusters = self.model.predict(X_scaled)

        return clusters

    def get_cluster_centers(self) -> np.ndarray:
        if not self.is_trained:
            raise ValueError("Modelo no entrenado.")

        centers_scaled = self.model.cluster_centers_
        centers = self.scaler.inverse_transform(centers_scaled)

        return centers

    def get_cluster_info(self, cluster_id: int) -> Dict[str, Any]:
        if not self.is_trained:
            raise ValueError("Modelo no entrenado.")

        if cluster_id >= self.n_clusters:
            raise ValueError(f"Cluster {cluster_id} no existe. Hay {self.n_clusters} clusters.")

        centers = self.get_cluster_centers()
        center = centers[cluster_id]

        return {
            'cluster_id': cluster_id,
            'center': center.tolist(),
            'size': self.metadata['cluster_sizes'][cluster_id],
            'feature_names': self.feature_names
        }
