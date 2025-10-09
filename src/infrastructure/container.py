"""
Dependency Injection Container
Contenedor IoC (Inversion of Control) para gestionar dependencias.
Equivalente a @Configuration + @Bean en Spring Boot.
"""

from typing import Optional
from src.domain.repositories import RestaurantRepository, UserRepository
from src.infrastructure.repositories import CSVRestaurantRepository, MemoryUserRepository


class Container:
    """
    Contenedor de Inyección de Dependencias.

    Gestiona la creación y ciclo de vida de las dependencias
    del sistema, implementando el patrón Singleton para servicios.

    Patrón: Dependency Injection Container / Service Locator
    Similar a: Spring ApplicationContext
    """

    _instance: Optional['Container'] = None
    _initialized: bool = False

    def __new__(cls):
        """Implementa Singleton para el Container."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa el container (solo una vez)."""
        if not Container._initialized:
            self._dependencies = {}
            Container._initialized = True
            print("✅ Dependency Injection Container initialized")

    # =========================================================================
    # REPOSITORY BEANS
    # =========================================================================

    def restaurant_repository(self,
                              csv_path: str = 'data/processed/restaurantes_sin_anomalias.csv') -> RestaurantRepository:
        """
        Bean: RestaurantRepository (Singleton por csv_path)

        Retorna una instancia del repositorio de restaurantes.
        Cachea por csv_path para permitir múltiples fuentes de datos.
        Equivalente a @Bean en Spring.

        Args:
            csv_path: Ruta al archivo CSV (default: restaurantes_sin_anomalias.csv)

        Returns:
            RestaurantRepository: Instancia del repositorio
        """
        # Usar el csv_path como clave para permitir múltiples repositorios
        cache_key = f'restaurant_repository:{csv_path}'

        if cache_key not in self._dependencies:
            self._dependencies[cache_key] = CSVRestaurantRepository(csv_path)

        return self._dependencies[cache_key]

    def user_repository(self) -> UserRepository:
        """
        Bean: UserRepository (Singleton)

        Retorna una instancia única del repositorio de usuarios.

        Returns:
            UserRepository: Instancia del repositorio
        """
        if 'user_repository' not in self._dependencies:
            self._dependencies['user_repository'] = MemoryUserRepository()
        return self._dependencies['user_repository']

    # =========================================================================
    # UTILIDADES
    # =========================================================================

    def clear(self) -> None:
        """
        Limpia todas las dependencias (útil para testing).
        Recrea el container desde cero.
        """
        self._dependencies.clear()
        Container._initialized = False
        print("🔄 Container cleared and reset")

    def reset_repository(self, repository_name: str) -> None:
        """
        Resetea un repositorio específico.

        Args:
            repository_name: Nombre del repositorio ('restaurant_repository', 'user_repository')
        """
        if repository_name in self._dependencies:
            del self._dependencies[repository_name]
            print(f"🔄 {repository_name} reset")

    def get_all_beans(self) -> dict:
        """
        Obtiene todos los beans registrados.

        Returns:
            dict: Diccionario con todos los beans
        """
        return self._dependencies.copy()


# =========================================================================
# INSTANCIA GLOBAL DEL CONTAINER
# =========================================================================

# Singleton global que puede ser importado
container = Container()


# =========================================================================
# ML MODEL BEANS
# =========================================================================

def clustering_model(self):
    """
    Bean: Clustering Model (Singleton)

    Returns:
        RestaurantClusteringModel: Modelo de clustering
    """
    if 'clustering_model' not in self._dependencies:
        from src.infrastructure.ml import get_clustering_model
        model = get_clustering_model()
        if model:
            self._dependencies['clustering_model'] = model
    return self._dependencies.get('clustering_model')


def rating_model(self):
    """
    Bean: Rating Predictor Model (Singleton)

    Returns:
        RatingPredictorModel: Modelo de predicción
    """
    if 'rating_model' not in self._dependencies:
        from src.infrastructure.ml import get_rating_model
        model = get_rating_model()
        if model:
            self._dependencies['rating_model'] = model
    return self._dependencies.get('rating_model')


def recommender_system(self):
    """
    Bean: Recommender System (Singleton)

    Returns:
        RestaurantRecommenderSystem: Sistema de recomendación
    """
    if 'recommender_system' not in self._dependencies:
        from src.infrastructure.ml import get_recommender_system
        system = get_recommender_system()
        if system:
            # Cargar datos de restaurantes
            repo = self.restaurant_repository()
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
                    'reviews': r.reviews,
                    'phoneNumber': r.phone_number,
                    'url': r.url
                }
                for r in repo.find_all()
            ])
            system.set_restaurants_data(restaurants_df)
            self._dependencies['recommender_system'] = system
    return self._dependencies.get('recommender_system')

# =========================================================================
# FUNCIONES DE CONVENIENCIA
# =========================================================================

def get_restaurant_repository(csv_path: str = 'data/processed/restaurantes_sin_anomalias.csv') -> RestaurantRepository:
    """
    Función de conveniencia para obtener el RestaurantRepository.

    Args:
        csv_path: Ruta al CSV

    Returns:
        RestaurantRepository: Instancia del repositorio
    """
    return container.restaurant_repository(csv_path)


def get_user_repository() -> UserRepository:
    """
    Función de conveniencia para obtener el UserRepository.

    Returns:
        UserRepository: Instancia del repositorio
    """
    return container.user_repository()

def get_clustering_model():
    """Función de conveniencia para obtener clustering model."""
    return container.clustering_model()


def get_rating_model():
    """Función de conveniencia para obtener rating model."""
    return container.rating_model()


def get_recommender_system_from_container():
    """Función de conveniencia para obtener recommender system."""
    return container.recommender_system()