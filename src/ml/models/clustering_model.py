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
    """
    Modelo de clustering para agrupar restaurantes similares.

    Usa K-Means para identificar grupos de restaurantes con
    características similares (ubicación, rating, categoría, etc.)
    """

    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        """
        Inicializar modelo de clustering.

        Args:
            n_clusters: Número de clusters deseados
            random_state: Semilla para reproducibilidad
        """
        super().__init__(model_name="restaurant_clustering")
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names = []

    def train(self, X: pd.DataFrame, y=None) -> 'RestaurantClusteringModel':
        """
        Entrenar modelo de clustering.

        Args:
            X: DataFrame con features (lat, long, stars, reviews, etc.)
            y: No usado (clustering es no supervisado)

        Returns:
            self: Modelo entrenado
        """
        print(f"🤖 Entrenando {self.model_name}...")
        print(f"   Datos: {X.shape[0]} registros, {X.shape[1]} features")
        print(f"   Clusters objetivo: {self.n_clusters}")

        # Guardar nombres de features
        self.feature_names = list(X.columns)

        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)

        # Entrenar K-Means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )

        self.model.fit(X_scaled)

        # Calcular métricas
        labels = self.model.labels_
        silhouette = silhouette_score(X_scaled, labels)
        inertia = self.model.inertia_

        # Guardar metadata
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

        print(f"✅ Modelo entrenado exitosamente")
        print(f"   Silhouette Score: {silhouette:.3f}")
        print(f"   Inertia: {inertia:.2f}")
        print(f"   Tamaños de clusters: {self.metadata['cluster_sizes']}")

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predecir cluster para nuevos datos.

        Args:
            X: DataFrame con features

        Returns:
            Array con asignaciones de cluster
        """
        if not self.is_trained:
            raise ValueError("Modelo no entrenado. Ejecuta train() primero.")

        # Asegurar que tenemos las mismas features
        X = X[self.feature_names]

        # Normalizar y predecir
        X_scaled = self.scaler.transform(X)
        clusters = self.model.predict(X_scaled)

        return clusters

    def get_cluster_centers(self) -> np.ndarray:
        """
        Obtener centros de clusters (desnormalizados).

        Returns:
            Array con centros de clusters
        """
        if not self.is_trained:
            raise ValueError("Modelo no entrenado.")

        # Desnormalizar centros
        centers_scaled = self.model.cluster_centers_
        centers = self.scaler.inverse_transform(centers_scaled)

        return centers

    def get_cluster_info(self, cluster_id: int) -> Dict[str, Any]:
        """
        Obtener información sobre un cluster específico.

        Args:
            cluster_id: ID del cluster

        Returns:
            Diccionario con información del cluster
        """
        if not self.is_trained:
            raise ValueError("Modelo no entrenado.")

        if cluster_id >= self.n_clusters:
            raise ValueError(f"Cluster {cluster_id} no existe. Hay {self.n_clusters} clusters.")

        centers = self.get_cluster_centers()
        center = centers[cluster_id]

        return {
            'cluster_id': cluster_id,
            'size': self.metadata['cluster_sizes'].get(cluster_id, 0),
            'center': dict(zip(self.feature_names, center)),
            'percentage': self.metadata['cluster_sizes'].get(cluster_id, 0) / self.metadata['n_samples'] * 100
        }

    def find_similar_by_cluster(
            self,
            reference_features: pd.DataFrame,
            all_features: pd.DataFrame,
            top_n: int = 5
    ) -> np.ndarray:
        """
        Encontrar restaurantes similares basándose en cluster.

        Args:
            reference_features: Features del restaurante de referencia
            all_features: Features de todos los restaurantes
            top_n: Número de resultados a retornar

        Returns:
            Índices de los restaurantes más similares
        """
        # Predecir cluster del restaurante de referencia
        ref_cluster = self.predict(reference_features)[0]

        # Predecir clusters de todos
        all_clusters = self.predict(all_features)

        # Encontrar todos los del mismo cluster
        same_cluster_indices = np.where(all_clusters == ref_cluster)[0]

        # Si hay menos de top_n, retornar todos
        if len(same_cluster_indices) <= top_n:
            return same_cluster_indices

        # Retornar muestra aleatoria
        return np.random.choice(same_cluster_indices, size=top_n, replace=False)

    def get_optimal_clusters(
            self,
            X: pd.DataFrame,
            max_clusters: int = 10
    ) -> Dict[int, float]:
        """
        Encontrar número óptimo de clusters usando Elbow Method.

        Args:
            X: DataFrame con features
            max_clusters: Número máximo de clusters a probar

        Returns:
            Diccionario con inertias por número de clusters
        """
        print("🔍 Buscando número óptimo de clusters...")

        X_scaled = self.scaler.fit_transform(X)
        inertias = {}

        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            kmeans.fit(X_scaled)
            inertias[k] = kmeans.inertia_
            print(f"   K={k}: Inertia={kmeans.inertia_:.2f}")

        return inertias