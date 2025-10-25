"""
Recommender System
Sistema de recomendacion hibrido usando ML models.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from .base_model import BaseMLModel
from .clustering_model import RestaurantClusteringModel
from .rating_predictor import RatingPredictorModel


class RestaurantRecommenderSystem(BaseMLModel):
    """Sistema de recomendacion hibrido para restaurantes."""

    def __init__(
            self,
            clustering_model: Optional[RestaurantClusteringModel] = None,
            rating_model: Optional[RatingPredictorModel] = None,
            weights: Optional[Dict[str, float]] = None
    ):
        super().__init__(model_name="restaurant_recommender")

        self.clustering_model = clustering_model
        self.rating_model = rating_model

        self.weights = weights or {
            'rating': 0.35,
            'popularity': 0.25,
            'distance': 0.20,
            'cluster_similarity': 0.15,
            'category_match': 0.05
        }

        self.restaurants_data = None
        self.is_trained = True

    def train(self, X=None, y=None) -> 'RestaurantRecommenderSystem':
        print("Recommender System inicializado")
        print(f"   Clustering Model: {'OK' if self.clustering_model else 'No'}")
        print(f"   Rating Model: {'OK' if self.rating_model else 'No'}")
        return self

    def predict(self, X) -> np.ndarray:
        raise NotImplementedError("Usa metodo recommend() para obtener recomendaciones")

    def set_restaurants_data(self, restaurants_df: pd.DataFrame) -> None:
        self.restaurants_data = restaurants_df.copy()
        print(f"Datos de restaurantes cargados: {len(restaurants_df)} registros")

    def calculate_similarity_score(
            self,
            restaurant_features: pd.Series,
            reference_features: pd.Series
    ) -> float:
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
        if self.restaurants_data is None:
            raise ValueError("No hay datos de restaurantes. Usa set_restaurants_data() primero.")

        candidates = self.restaurants_data.copy()

        if 'category' in preferences:
            candidates = candidates[
                candidates['category'].str.contains(preferences['category'], case=False, na=False)
            ]

        if 'min_rating' in filters:
            candidates = candidates[candidates['stars'] >= filters['min_rating']]

        candidates['distance'] = candidates.apply(
            lambda row: self.calculate_distance(
                user_lat, user_long, row['lat'], row['long']
            ),
            axis=1
        )

        if 'max_distance_km' in filters:
            candidates = candidates[candidates['distance'] <= filters['max_distance_km']]

        candidates['score'] = candidates.apply(
            lambda row: self._calculate_recommendation_score(row, user_lat, user_long, preferences),
            axis=1
        )

        recommendations = candidates.nlargest(top_n, 'score')

        return recommendations.to_dict('records')

    def _calculate_recommendation_score(
            self,
            restaurant: pd.Series,
            user_lat: float,
            user_long: float,
            preferences: Dict
    ) -> float:
        rating_score = restaurant['stars'] / 5.0
        popularity_score = min(np.log10(restaurant['reviews'] + 1) / 3.0, 1.0)
        distance_score = max(0.0, 1.0 - (restaurant.get('distance', 0) / 10.0))

        category_score = 0.5
        if 'category' in preferences:
            if preferences['category'].lower() in restaurant['category'].lower():
                category_score = 1.0

        final_score = (
            rating_score * self.weights['rating'] +
            popularity_score * self.weights['popularity'] +
            distance_score * self.weights['distance'] +
            category_score * self.weights['category_match']
        )

        return round(final_score, 3)
