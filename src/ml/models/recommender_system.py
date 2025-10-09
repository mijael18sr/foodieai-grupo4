"""
Recommender System
Sistema de recomendación híbrido usando ML models.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from .base_model import BaseMLModel
from .clustering_model import RestaurantClusteringModel
from .rating_predictor import RatingPredictorModel


class RestaurantRecommenderSystem(BaseMLModel):
    """
    Sistema de recomendación híbrido para restaurantes.

    Combina:
    - Content-Based Filtering (features del restaurante)
    - Collaborative Filtering (clustering de similares)
    - Rating Prediction (ML para predecir calidad)
    """

    def __init__(
            self,
            clustering_model: Optional[RestaurantClusteringModel] = None,
            rating_model: Optional[RatingPredictorModel] = None,
            weights: Optional[Dict[str, float]] = None
    ):
        """
        Inicializar sistema de recomendación.

        Args:
            clustering_model: Modelo de clustering entrenado
            rating_model: Modelo de predicción de ratings entrenado
            weights: Pesos para cada componente del score
        """
        super().__init__(model_name="restaurant_recommender")

        self.clustering_model = clustering_model
        self.rating_model = rating_model

        # Pesos por defecto para calcular score final
        self.weights = weights or {
            'rating': 0.35,  # Calificación actual/predicha
            'popularity': 0.25,  # Número de reviews
            'distance': 0.20,  # Cercanía geográfica
            'cluster_similarity': 0.15,  # Similaridad por cluster
            'category_match': 0.05  # Match de categoría
        }

        self.restaurants_data = None
        self.is_trained = True  # No requiere entrenamiento adicional

    def train(self, X=None, y=None) -> 'RestaurantRecommenderSystem':
        """
        No requiere entrenamiento propio.
        Los modelos subyacentes ya están entrenados.
        """
        print("✅ Recommender System inicializado")
        print(f"   Clustering Model: {'✓' if self.clustering_model else '✗'}")
        print(f"   Rating Model: {'✓' if self.rating_model else '✗'}")
        return self

    def predict(self, X) -> np.ndarray:
        """No usado directamente. Usar recommend() en su lugar."""
        raise NotImplementedError("Usa método recommend() para obtener recomendaciones")

    def set_restaurants_data(self, restaurants_df: pd.DataFrame) -> None:
        """
        Establecer datos de restaurantes para recomendaciones.

        Args:
            restaurants_df: DataFrame con todos los restaurantes
        """
        self.restaurants_data = restaurants_df.copy()
        print(f"✅ Datos de restaurantes cargados: {len(restaurants_df)} registros")

    def calculate_similarity_score(
            self,
            restaurant_features: pd.Series,
            reference_features: pd.Series
    ) -> float:
        """
        Calcular score de similaridad entre dos restaurantes.

        Args:
            restaurant_features: Features del restaurante candidato
            reference_features: Features del restaurante de referencia

        Returns:
            Score de similaridad [0, 1]
        """
        # Similaridad basada en clustering
        cluster_score = 0.0
        if self.clustering_model and self.clustering_model.is_trained:
            try:
                ref_cluster = self.clustering_model.predict(
                    reference_features.to_frame().T
                )[0]
                rest_cluster = self.clustering_model.predict(
                    restaurant_features.to_frame().T
                )[0]
                cluster_score = 1.0 if ref_cluster == rest_cluster else 0.5
            except:
                cluster_score = 0.5
        else:
            cluster_score = 0.5

        return cluster_score

    def calculate_distance(
            self,
            lat1: float,
            long1: float,
            lat2: float,
            long2: float
    ) -> float:
        """
        Calcular distancia en km (Haversine simplificado).

        Args:
            lat1, long1: Coordenadas punto 1
            lat2, long2: Coordenadas punto 2

        Returns:
            Distancia en km
        """
        # Aproximación simple
        lat_diff = (lat2 - lat1) * 111
        long_diff = (long2 - long1) * 111 * np.cos(np.radians(lat1))
        distance = np.sqrt(lat_diff ** 2 + long_diff ** 2)
        return round(distance, 2)

    def recommend(
            self,
            user_lat: float,
            user_long: float,
            preferences: Dict,
            filters: Dict,
            top_n: int = 10
    ) -> List[Dict]:
        """
        Generar recomendaciones personalizadas.

        Args:
            user_lat: Latitud del usuario
            user_long: Longitud del usuario
            preferences: Preferencias del usuario
            filters: Filtros de búsqueda
            top_n: Número de recomendaciones

        Returns:
            Lista de diccionarios con recomendaciones
        """
        if self.restaurants_data is None:
            raise ValueError("Datos de restaurantes no cargados. Usa set_restaurants_data()")

        candidates = self.restaurants_data.copy()

        # Aplicar filtros
        candidates = self._apply_filters(candidates, filters, preferences)

        if len(candidates) == 0:
            return []

        # Calcular scores para cada candidato
        recommendations = []

        for idx, restaurant in candidates.iterrows():
            score_components = self._calculate_score_components(
                restaurant,
                user_lat,
                user_long,
                preferences
            )

            final_score = sum(
                self.weights[key] * value
                for key, value in score_components.items()
            )

            distance = self.calculate_distance(
                user_lat, user_long,
                restaurant['lat'], restaurant['long']
            )

            recommendations.append({
                'restaurant_id': restaurant['id_place'],
                'restaurant_data': restaurant.to_dict(),
                'score': round(final_score, 3),
                'score_components': score_components,
                'distance_km': distance,
                'reason': self._generate_reason(restaurant, score_components, distance)
            })

        # Ordenar por score y retornar top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)

        return recommendations[:top_n]

    def _apply_filters(
            self,
            candidates: pd.DataFrame,
            filters: Dict,
            preferences: Dict
    ) -> pd.DataFrame:
        """Aplicar filtros a candidatos."""

        # Filtro de categoría
        category = preferences.get('category') or filters.get('category')
        if category:
            candidates = candidates[
                candidates['category'].str.contains(category, case=False, na=False) |
                candidates['category'].str.lower().str.contains(category.lower(), na=False)
                ]

        # Filtro de rating mínimo
        min_rating = filters.get('min_rating', 0.0)
        if min_rating:
            candidates = candidates[candidates['stars'] >= min_rating]

        # Filtro de distrito
        district = filters.get('district')
        if district:
            candidates = candidates[
                candidates['district'].str.lower() == district.lower()
                ]

        # Filtro de distancia máxima
        max_distance = filters.get('max_distance_km')
        if max_distance:
            # Calcular distancias (esto es costoso, considerar optimización)
            # Por ahora, aproximación por bounding box
            pass

        return candidates

    def _calculate_score_components(
            self,
            restaurant: pd.Series,
            user_lat: float,
            user_long: float,
            preferences: Dict
    ) -> Dict[str, float]:
        """
        Calcular componentes individuales del score.

        Returns:
            Dict con scores normalizados [0, 1] para cada componente
        """
        components = {}

        # 1. Rating score
        if self.rating_model and self.rating_model.is_trained:
            # Usar predicción si hay modelo
            try:
                features = self._extract_features_for_prediction(restaurant)
                predicted_rating = self.rating_model.predict(features)[0]
                components['rating'] = predicted_rating / 5.0
            except:
                components['rating'] = restaurant['stars'] / 5.0
        else:
            components['rating'] = restaurant['stars'] / 5.0

        # 2. Popularity score (log scale)
        reviews = restaurant['reviews']
        components['popularity'] = min(np.log10(reviews + 1) / 3.0, 1.0)

        # 3. Distance score (más cerca = mejor)
        distance = self.calculate_distance(
            user_lat, user_long,
            restaurant['lat'], restaurant['long']
        )
        components['distance'] = max(0, 1.0 - (distance / 10.0))

        # 4. Cluster similarity (si hay clustering)
        if self.clustering_model and self.clustering_model.is_trained:
            try:
                # Placeholder: similaridad basada en cluster
                components['cluster_similarity'] = 0.8
            except:
                components['cluster_similarity'] = 0.5
        else:
            components['cluster_similarity'] = 0.5

        # 5. Category match
        preferred_category = preferences.get('category', '')
        if preferred_category:
            category_match = (
                    preferred_category.lower() in restaurant['category'].lower() or
                    restaurant['category'].lower() in preferred_category.lower()
            )
            components['category_match'] = 1.0 if category_match else 0.3
        else:
            components['category_match'] = 0.5

        return components

    def _extract_features_for_prediction(
            self,
            restaurant: pd.Series
    ) -> pd.DataFrame:
        """
        Extraer features necesarias para predicción de rating.

        Args:
            restaurant: Serie con datos del restaurante

        Returns:
            DataFrame con features para el modelo
        """
        # Esto depende de qué features espera tu rating model
        # Ajustar según tus necesidades
        features = pd.DataFrame({
            'lat': [restaurant['lat']],
            'long': [restaurant['long']],
            'reviews': [restaurant['reviews']],
            # Agregar más features según tu modelo
        })

        return features

    def _generate_reason(
            self,
            restaurant: pd.Series,
            score_components: Dict[str, float],
            distance: float
    ) -> str:
        """Generar razón legible para la recomendación."""
        reasons = []

        # Evaluar score total
        total_score = sum(
            self.weights[key] * value
            for key, value in score_components.items()
        )

        if total_score >= 0.8:
            reasons.append("Excelente opción")
        elif total_score >= 0.6:
            reasons.append("Buena opción")
        else:
            reasons.append("Opción disponible")

        # Distancia
        if distance < 1.0:
            reasons.append("muy cerca de ti")
        elif distance < 3.0:
            reasons.append("cerca de ti")

        # Rating
        if restaurant['stars'] >= 4.5:
            reasons.append(f"con {restaurant['stars']}⭐")

        # Popularidad
        if restaurant['reviews'] > 100:
            reasons.append("muy popular")

        # Ubicación
        reasons.append(f"en {restaurant['district']}")

        return " ".join(reasons)