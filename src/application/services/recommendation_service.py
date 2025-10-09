"""
Recommendation Service
Servicio de lógica de negocio para recomendaciones.
Equivalente a @Service en Spring Boot.
"""

import numpy as np
from typing import List, Dict
from src.domain import Restaurant, User, Recommendation
from src.domain.repositories import RestaurantRepository
from src.application.dto import (
    RecommendationRequestDTO,
    RecommendationResponseDTO,
    RecommendationItemDTO,
    RestaurantDTO
)


class RecommendationService:
    """
    Service de Recomendaciones.

    Contiene la lógica de negocio para generar recomendaciones
    personalizadas de restaurantes.

    Patrón: Service Layer
    Similar a: @Service en Spring Boot
    """

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

        # Cargar modelos ML si están disponibles
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

                # Cargar datos en el recommender system
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
                print(f"✅ RecommendationService initialized (ML models: {models_loaded}/3)")
            except Exception as e:
                print(f"⚠️  RecommendationService initialized (ML models disabled: {e})")
                self.use_ml_models = False
        else:
            print("✅ RecommendationService initialized (simple algorithm)")

    def get_recommendations(
            self,
            request: RecommendationRequestDTO
    ) -> RecommendationResponseDTO:
        """
        Obtener recomendaciones personalizadas.

        Business Logic:
        1. Crear entidad User desde el request
        2. Filtrar candidatos según preferencias
        3. Calcular scores de recomendación
        4. Rankear y retornar top N

        Args:
            request: DTO con datos de la solicitud

        Returns:
            RecommendationResponseDTO: Respuesta con recomendaciones
        """
        import time
        start_time = time.time()

        # 1. Crear entidad User
        user = User(
            user_id=f"temp_{int(time.time())}",
            location_lat=request.user_location.lat,
            location_long=request.user_location.long,
            preferences=request.preferences
        )

        # 2. Filtrar candidatos
        candidates = self._filter_candidates(user, request.filters)

        # 3. Calcular recomendaciones
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

        # 4. Ordenar y obtener top N
        recommendations.sort(key=lambda x: x.score, reverse=True)
        top_recommendations = recommendations[:request.top_n]

        # 5. Convertir a DTOs
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
        """
        Filtra restaurantes candidatos según preferencias y filtros.

        Args:
            user: Usuario solicitante
            filters: Filtros de búsqueda

        Returns:
            List[Restaurant]: Lista de candidatos
        """
        candidates = self.restaurant_repository.find_all()

        # Filtrar por categoría preferida (match flexible)
        if user.preferred_category:
            preferred = user.preferred_category.lower()
            candidates = [
                r for r in candidates
                if preferred in r.category.lower() or r.category.lower() in preferred
            ]

        # Filtrar por rating mínimo
        min_rating = filters.get('min_rating', user.min_rating)
        if min_rating:
            candidates = [r for r in candidates if r.stars >= min_rating]

        # Filtrar por distancia máxima
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

        # Filtrar por distrito
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

        Formula: Score ponderado de múltiples factores
        - Rating del restaurante (40%)
        - Popularidad (reviews) (30%)
        - Cercanía (20%)
        - Categoría match (10%)

        Args:
            user: Usuario
            restaurant: Restaurante

        Returns:
            float: Score entre 0.0 y 1.0
        """
        # Factor 1: Rating normalizado (0-1)
        rating_score = restaurant.stars / 5.0

        # Factor 2: Popularidad normalizada (log scale)
        popularity_score = min(np.log10(restaurant.reviews + 1) / 3.0, 1.0)

        # Factor 3: Distancia (más cerca = mejor)
        distance = self._calculate_distance(
            user.location_lat,
            user.location_long,
            restaurant.lat,
            restaurant.long
        )
        distance_score = max(0.0, 1.0 - (distance / 10.0))  # 10km = score 0

        # Factor 4: Match de categoría
        category_score = 1.0 if (
                user.preferred_category and
                restaurant.category.lower() == user.preferred_category.lower()
        ) else 0.5

        # Score ponderado
        final_score = (
                rating_score * 0.4 +
                popularity_score * 0.3 +
                distance_score * 0.2 +
                category_score * 0.1
        )

        return round(final_score, 3)

    def _calculate_distance(
            self,
            lat1: float,
            long1: float,
            lat2: float,
            long2: float
    ) -> float:
        """
        Calcula distancia aproximada en km.

        Nota: Usa aproximación euclidiana simple.
        Para producción, usar fórmula de Haversine.

        Args:
            lat1, long1: Coordenadas punto 1
            lat2, long2: Coordenadas punto 2

        Returns:
            float: Distancia en km
        """
        # Aproximación: 1 grado ≈ 111 km
        lat_diff = (lat2 - lat1) * 111
        long_diff = (long2 - long1) * 111 * np.cos(np.radians(lat1))
        distance = np.sqrt(lat_diff ** 2 + long_diff ** 2)
        return round(distance, 2)

    def _generate_reason(
            self,
            restaurant: Restaurant,
            score: float,
            distance: float
    ) -> str:
        """
        Genera una razón legible para la recomendación.

        Args:
            restaurant: Restaurante
            score: Score de recomendación
            distance: Distancia en km

        Returns:
            str: Razón de la recomendación
        """
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
            reasons.append(f"con {restaurant.stars}⭐")

        if restaurant.is_popular:
            reasons.append("muy popular")

        reasons.append(f"en {restaurant.district}")

        return " ".join(reasons)

    def _to_recommendation_item_dto(
            self,
            recommendation: Recommendation
    ) -> RecommendationItemDTO:
        """
        Convierte Recommendation entity a DTO.

        Args:
            recommendation: Entidad Recommendation

        Returns:
            RecommendationItemDTO: DTO de recomendación
        """
        restaurant = recommendation.restaurant

        restaurant_dto = RestaurantDTO(
            id=restaurant.id,
            name=restaurant.title,
            category=restaurant.category,
            rating=restaurant.stars,
            reviews=restaurant.reviews,
            distance_km=recommendation.distance_km,
            address=restaurant.address,
            district=restaurant.district,
            phone=restaurant.phone_number,
            url=restaurant.url
        )

        return RecommendationItemDTO(
            restaurant=restaurant_dto,
            score=recommendation.score,
            reason=recommendation.reason,
            details={
                'is_highly_rated': restaurant.is_highly_rated,
                'is_popular': restaurant.is_popular,
                'is_nearby': recommendation.is_nearby
            }
        )