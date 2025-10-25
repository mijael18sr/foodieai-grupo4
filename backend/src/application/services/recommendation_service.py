"""
Recommendation Service
Servicio de lógica de negocio para recomendaciones.
"""

import numpy as np
from typing import List, Dict, Any, Union
from src.domain import Restaurant, User, Recommendation
from src.domain.repositories import RestaurantRepository
from src.application.dto import (
    RecommendationRequestDTO,
    RecommendationResponseDTO,
    RecommendationItemDTO,
    RestaurantDTO
)


def convert_numpy_types(obj: Any) -> Any:
    """
    Convierte recursivamente tipos de numpy a tipos nativos de Python.
    Esto resuelve el problema de serialización de Pydantic con tipos numpy.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


class RecommendationService:
    """Service de Recomendaciones con lógica de negocio personalizada."""

    def __init__(
            self,
            restaurant_repository: RestaurantRepository,
            use_ml_models: bool = True
    ):
        """
        Constructor con Dependency Injection.

        Args:
            restaurant_repository: Repositorio de restaurantes (inyectado)
            use_ml_models: Si usar modelos ML (True) o algoritmo simple (False)
        """
        self.restaurant_repository = restaurant_repository
        self.use_ml_models = use_ml_models

        self.clustering_model = None
        self.rating_model = None
        self.recommender_system = None

        if use_ml_models:
            try:
                from src.infrastructure.ml import (
                    get_clustering_model,
                    get_rating_model,
                    get_recommender_system
                )

                self.clustering_model = get_clustering_model()
                self.rating_model = get_rating_model()
                self.recommender_system = get_recommender_system()

                if self.recommender_system:
                    import pandas as pd
                    restaurants_df = pd.DataFrame([
                        {
                            'id_place': r.id,
                            'title': r.title,
                            'category': r.category,
                            'address': r.address,
                            'district': r.district,
                            'lat': r.lat,
                            'long': r.long,
                            'stars': r.stars,
                            'reviews': r.reviews
                        }
                        for r in self.restaurant_repository.find_all()
                    ])
                    self.recommender_system.set_restaurants_data(restaurants_df)

                models_loaded = sum([
                    self.clustering_model is not None,
                    self.rating_model is not None,
                    self.recommender_system is not None
                ])
                print(f"RecommendationService initialized (ML models: {models_loaded}/3)")
            except Exception as e:
                print(f"RecommendationService initialized (ML models disabled: {e})")
                self.use_ml_models = False
        else:
            print("RecommendationService initialized (simple algorithm)")

    def get_recommendations(
            self,
            request: RecommendationRequestDTO
    ) -> RecommendationResponseDTO:
        """
        Obtener recomendaciones personalizadas.

        Args:
            request: DTO con datos de la solicitud

        Returns:
            RecommendationResponseDTO: Respuesta con recomendaciones
        """
        import time
        start_time = time.time()

        user = User(
            user_id=f"temp_{int(time.time())}",
            location_lat=request.user_location.lat,
            location_long=request.user_location.long,
            preferences=request.preferences
        )

        candidates = self._filter_candidates(user, request.filters)

        recommendations = []
        for restaurant in candidates:
            score = self._calculate_recommendation_score(user, restaurant)
            distance = self._calculate_distance(
                user.location_lat,
                user.location_long,
                restaurant.lat,
                restaurant.long
            )
            reason = self._generate_reason(restaurant, score, distance)

            recommendation = Recommendation(
                restaurant=restaurant,
                score=score,
                distance_km=distance,
                reason=reason
            )
            recommendations.append(recommendation)

        recommendations.sort(key=lambda x: x.score, reverse=True)
        top_recommendations = recommendations[:request.top_n]

        recommendation_items = [
            self._to_recommendation_item_dto(rec)
            for rec in top_recommendations
        ]

        execution_time = int((time.time() - start_time) * 1000)

        return RecommendationResponseDTO(
            recommendations=recommendation_items,
            total_found=len(recommendation_items),
            execution_time_ms=execution_time,
            metadata={
                'candidates_evaluated': len(candidates),
                'user_location': {
                    'lat': user.location_lat,
                    'long': user.location_long
                }
            }
        )

    def _filter_candidates(
            self,
            user: User,
            filters: Dict
    ) -> List[Restaurant]:
        """Filtra restaurantes candidatos según preferencias y filtros."""
        candidates = self.restaurant_repository.find_all()

        if user.preferred_category:
            preferred = user.preferred_category.lower()
            candidates = [
                r for r in candidates
                if preferred in r.category.lower() or r.category.lower() in preferred
            ]

        min_rating = filters.get('min_rating', user.min_rating)
        if min_rating:
            candidates = [r for r in candidates if r.stars >= min_rating]

        max_distance = filters.get('max_distance_km', user.max_distance_km)
        if max_distance:
            candidates = [
                r for r in candidates
                if self._calculate_distance(
                    user.location_lat,
                    user.location_long,
                    r.lat,
                    r.long
                ) <= max_distance
            ]

        district = filters.get('district')
        if district:
            candidates = [
                r for r in candidates
                if r.district.lower() == district.lower()
            ]

        return candidates

    def _calculate_recommendation_score(
            self,
            user: User,
            restaurant: Restaurant
    ) -> float:
        """
        Calcula el score de recomendación (0.0 - 1.0).
        Formula: Rating (40%) + Popularidad (30%) + Cercanía (20%) + Categoría (10%)
        """
        rating_score = float(restaurant.stars) / 5.0
        popularity_score = min(float(np.log10(restaurant.reviews + 1)) / 3.0, 1.0)

        distance = self._calculate_distance(
            user.location_lat,
            user.location_long,
            restaurant.lat,
            restaurant.long
        )
        distance_score = max(0.0, 1.0 - (float(distance) / 10.0))

        category_score = 1.0 if (
                user.preferred_category and
                restaurant.category.lower() == user.preferred_category.lower()
        ) else 0.5

        final_score = (
                rating_score * 0.4 +
                popularity_score * 0.3 +
                distance_score * 0.2 +
                category_score * 0.1
        )

        return round(float(final_score), 3)

    def _calculate_distance(
            self,
            lat1: float,
            long1: float,
            lat2: float,
            long2: float
    ) -> float:
        """Calcula distancia aproximada en km usando aproximación euclidiana."""
        lat_diff = (lat2 - lat1) * 111
        long_diff = (long2 - long1) * 111 * float(np.cos(np.radians(lat1)))
        distance = float(np.sqrt(lat_diff ** 2 + long_diff ** 2))
        return round(distance, 2)

    def _generate_reason(
            self,
            restaurant: Restaurant,
            score: float,
            distance: float
    ) -> str:
        """Genera una razón legible para la recomendación."""
        reasons = []

        if score >= 0.8:
            reasons.append("Excelente opción")
        elif score >= 0.6:
            reasons.append("Buena opción")
        else:
            reasons.append("Opción disponible")

        if distance < 1.0:
            reasons.append("muy cerca de ti")
        elif distance < 3.0:
            reasons.append("cerca de ti")

        if restaurant.is_highly_rated:
            reasons.append(f"con {restaurant.stars} estrellas")

        if restaurant.is_popular:
            reasons.append("muy popular")

        reasons.append(f"en {restaurant.district}")

        return " ".join(reasons)

    def _to_recommendation_item_dto(
            self,
            recommendation: Recommendation
    ) -> RecommendationItemDTO:
        """Convierte Recommendation entity a DTO."""
        restaurant = recommendation.restaurant

        # Aplicar conversión de numpy types a tipos nativos
        restaurant_data = {
            'id': convert_numpy_types(restaurant.id),
            'name': convert_numpy_types(restaurant.title),
            'category': convert_numpy_types(restaurant.category),
            'rating': convert_numpy_types(restaurant.stars),
            'reviews': convert_numpy_types(restaurant.reviews),
            'distance_km': convert_numpy_types(recommendation.distance_km),
            'address': convert_numpy_types(restaurant.address),
            'district': convert_numpy_types(restaurant.district),
            'phone': convert_numpy_types(restaurant.phone_number),
            'url': convert_numpy_types(restaurant.url)
        }

        restaurant_dto = RestaurantDTO(**restaurant_data)

        # También convertir los valores del details dict
        details_data = {
            'is_highly_rated': convert_numpy_types(restaurant.is_highly_rated),
            'is_popular': convert_numpy_types(restaurant.is_popular),
            'is_nearby': convert_numpy_types(recommendation.is_nearby)
        }

        return RecommendationItemDTO(
            restaurant=restaurant_dto,
            score=convert_numpy_types(recommendation.score),
            reason=convert_numpy_types(recommendation.reason),
            details=details_data
        )