"""
Dependency Injection Container
Contenedor IoC (Inversion of Control) para gestionar dependencias.
"""

from typing import Optional
from src.domain.repositories import RestaurantRepository, UserRepository, ReviewRepository
from src.infrastructure.repositories import CSVRestaurantRepository, MemoryUserRepository, CSVReviewRepository
from src.ml.models import SentimentAnalysisModel


class Container:
    """
    Contenedor de Inyección de Dependencias.
    Gestiona la creación y ciclo de vida de las dependencias del sistema.
    """

    _instance: Optional['Container'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Container._initialized:
            self._dependencies = {}
            Container._initialized = True
            print("Dependency Injection Container initialized")

    def restaurant_repository(self,
                              csv_path: str = 'data/processed/restaurantes_sin_anomalias.csv') -> RestaurantRepository:
        cache_key = f'restaurant_repository:{csv_path}'
        if cache_key not in self._dependencies:
            self._dependencies[cache_key] = CSVRestaurantRepository(csv_path)
        return self._dependencies[cache_key]

    def user_repository(self) -> UserRepository:
        if 'user_repository' not in self._dependencies:
            self._dependencies['user_repository'] = MemoryUserRepository()
        return self._dependencies['user_repository']

    def review_repository(self,
                         csv_path: str = 'data/processed/modelo_limpio.csv') -> ReviewRepository:
        """Obtener repositorio de reseñas (Singleton)"""
        cache_key = f'review_repository:{csv_path}'
        if cache_key not in self._dependencies:
            self._dependencies[cache_key] = CSVReviewRepository(csv_path)
        return self._dependencies[cache_key]

    def sentiment_model(self,
                       model_path: str = 'data/models/sentiment_model.pkl') -> SentimentAnalysisModel:
        """
        Obtener modelo de análisis de sentimientos (Singleton)

        Por defecto usa el modelo híbrido optimizado en producción:
        - Accuracy: 76.8%
        - Cohen's Kappa: 0.6208 (Sustancial)
        - F1-Score Neutro: 51.6% (mejorado +93%)
        - Balanceado: 52% pos, 26% neg, 22% neu
        """
        cache_key = f'sentiment_model:{model_path}'
        if cache_key not in self._dependencies:
            model = SentimentAnalysisModel()
            try:
                model.load(model_path)
                if model.is_trained:
                    # Log información del modelo cargado
                    metadata = model.metadata or {}
                    model_type = metadata.get('model_type', 'standard')
                    accuracy = metadata.get('test_metrics', {}).get('accuracy', 0)
                    kappa = metadata.get('test_metrics', {}).get('cohen_kappa', 0)

                    print(f"✓ Modelo de sentimientos cargado:")
                    print(f"  • Tipo: {model_type}")
                    print(f"  • Accuracy: {accuracy:.1%}")
                    print(f"  • Cohen's Kappa: {kappa:.4f}")

                    self._dependencies[cache_key] = model
                else:
                    print(f"⚠️ Modelo no entrenado en: {model_path}")
                    raise ValueError(f"Modelo no entrenado: {model_path}")

            except Exception as e:
                print(f"❌ Error cargando modelo de sentimientos: {e}")
                print(f"   Ruta: {model_path}")
                raise RuntimeError(f"No se pudo cargar modelo de sentimientos: {e}")

        return self._dependencies[cache_key]

    def clear(self) -> None:
        self._dependencies.clear()
        Container._initialized = False
        print("Container cleared and reset")

    def reset_repository(self, repository_name: str) -> None:
        if repository_name in self._dependencies:
            del self._dependencies[repository_name]
            print(f"{repository_name} reset")


# Instancia global del container
_container = Container()

# Funciones de acceso rápido para dependency injection
def get_restaurant_repository(csv_path: str = 'data/processed/restaurantes_sin_anomalias.csv') -> RestaurantRepository:
    """Obtener repositorio de restaurantes"""
    return _container.restaurant_repository(csv_path)

def get_user_repository() -> UserRepository:
    """Obtener repositorio de usuarios"""
    return _container.user_repository()

def get_review_repository(csv_path: str = 'data/processed/modelo_limpio.csv') -> ReviewRepository:
    """Obtener repositorio de reseñas"""
    return _container.review_repository(csv_path)

def get_sentiment_model(model_path: str = 'data/models/sentiment_model.pkl') -> SentimentAnalysisModel:
    """
    Obtener modelo de sentimientos optimizado

    En producción usa el modelo híbrido que tiene:
    - Mayor balance entre clases
    - Mejor detección de sentimientos neutros
    - Cohen's Kappa mejorado (0.6208)
    """
    return _container.sentiment_model(model_path)
