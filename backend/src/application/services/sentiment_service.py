"""
Sentiment Analysis Service
Servicio de lógica de negocio para análisis de sentimientos.
"""

from typing import List, Dict, Any, Optional

from src.domain.entities import Review, Sentiment
from src.domain.repositories import ReviewRepository
from src.ml.models import SentimentAnalysisModel


def get_confidence_level(confidence: float) -> str:
    """
    Determina el nivel de confiabilidad basado en el valor de confianza.

    Args:
        confidence: Valor de confianza (0.0 - 1.0)

    Returns:
        Nivel de confiabilidad como string
    """
    if confidence >= 0.90:
        return "MUY CONFIABLE"
    elif confidence >= 0.80:
        return "CONFIABLE"
    elif confidence >= 0.70:
        return "MODERADO"
    elif confidence >= 0.60:
        return "BAJA CONFIANZA"
    else:
        return "INDETERMINADO"


class SentimentAnalysisService:
    """
    Servicio de análisis de sentimientos.

    Implementa la lógica de negocio para:
    - Analizar sentimientos de comentarios individuales
    - Procesar lotes de reseñas
    - Obtener estadísticas de sentimientos por restaurante
    - Entrenar/actualizar el modelo
    """

    def __init__(
        self,
        review_repository: ReviewRepository,
        sentiment_model: Optional[SentimentAnalysisModel] = None
    ):
        """
        Constructor con Dependency Injection.

        Args:
            review_repository: Repositorio de reseñas (inyectado)
            sentiment_model: Modelo ML de sentimientos (opcional)
        """
        self.review_repository = review_repository
        self.sentiment_model = sentiment_model

    def analyze_comment(self, comment: str) -> Dict[str, Any]:
        """
        Analizar el sentimiento de un comentario individual.

        Args:
            comment: Texto del comentario

        Returns:
            Diccionario con el análisis de sentimiento
        """
        if not self.sentiment_model or not self.sentiment_model.is_trained:
            raise ValueError("El modelo de sentimientos no está disponible o entrenado")

        # Predecir sentimiento
        result = self.sentiment_model.predict_single(comment)

        # Calcular nivel de confiabilidad
        confidence_level = get_confidence_level(result['confidence'])

        return {
            'comment': result['text_original'],
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'confidence_level': confidence_level,
            'probabilities': result['probabilities'],
            'processed_text': result['text_processed']
        }

    def analyze_reviews(self, restaurant_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Analizar sentimientos de todas las reseñas de un restaurante.

        Args:
            restaurant_id: ID del restaurante
            limit: Límite de reseñas a analizar (None = todas)

        Returns:
            Análisis agregado de sentimientos
        """
        # Obtener reseñas del restaurante
        reviews = self.review_repository.find_by_restaurant(restaurant_id)

        if limit:
            reviews = reviews[:limit]

        if not reviews:
            return {
                'restaurant_id': restaurant_id,
                'total_reviews': 0,
                'sentiments': {},
                'avg_confidence': 0.0,
                'reviews_analyzed': []
            }

        # Analizar cada reseña si no tiene sentimiento
        analyzed_reviews = []
        for review in reviews:
            if review.sentiment is None and self.sentiment_model:
                # Analizar sentimiento
                analysis = self.analyze_comment(review.comment)
                review.sentiment = Sentiment(analysis['sentiment'])
                review.sentiment_confidence = analysis['confidence']
                review.sentiment_probabilities = analysis['probabilities']

            analyzed_reviews.append({
                'id': review.id,
                'comment': review.comment[:100] + '...' if len(review.comment) > 100 else review.comment,
                'rating': review.rating,
                'sentiment': review.sentiment.value if review.sentiment else None,
                'confidence': review.sentiment_confidence
            })

        # Calcular estadísticas
        sentiments = {}
        total_confidence = 0.0
        count_with_sentiment = 0

        for review in reviews:
            if review.sentiment:
                sentiment_key = review.sentiment.value
                sentiments[sentiment_key] = sentiments.get(sentiment_key, 0) + 1

            if review.sentiment_confidence:
                total_confidence += review.sentiment_confidence
                count_with_sentiment += 1

        avg_confidence = total_confidence / count_with_sentiment if count_with_sentiment > 0 else 0.0

        # Calcular porcentajes
        total = len(reviews)
        sentiment_percentages = {k: (v / total) * 100 for k, v in sentiments.items()}

        return {
            'restaurant_id': restaurant_id,
            'total_reviews': total,
            'sentiments': sentiments,
            'sentiment_percentages': sentiment_percentages,
            'avg_confidence': round(avg_confidence, 4),
            'reviews_analyzed': analyzed_reviews[:20]
        }

    def get_sentiment_statistics(self, restaurant_id: str) -> Dict[str, Any]:
        """
        Obtener estadísticas de sentimientos para un restaurante.

        Args:
            restaurant_id: ID del restaurante

        Returns:
            Estadísticas de sentimientos
        """
        return self.review_repository.get_sentiment_stats(restaurant_id)

    def get_reviews_by_sentiment(
        self,
        restaurant_id: str,
        sentiment: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Obtener reseñas de un restaurante filtradas por sentimiento.

        Args:
            restaurant_id: ID del restaurante
            sentiment: Sentimiento a filtrar (positivo, neutro, negativo)
            limit: Número máximo de reseñas

        Returns:
            Lista de reseñas
        """
        # Validar sentimiento
        if sentiment not in ['positivo', 'neutro', 'negativo']:
            raise ValueError(f"Sentimiento inválido: {sentiment}")

        # Obtener todas las reseñas del restaurante
        reviews = self.review_repository.find_by_restaurant(restaurant_id)

        # Filtrar por sentimiento
        filtered_reviews = [
            r for r in reviews
            if r.sentiment and r.sentiment.value == sentiment
        ][:limit]

        return [
            {
                'id': review.id,
                'comment': review.comment,
                'rating': review.rating,
                'username': review.username,
                'date': review.review_date.isoformat() if review.review_date else None,
                'sentiment': review.sentiment.value if review.sentiment else None,
                'confidence': review.sentiment_confidence
            }
            for review in filtered_reviews
        ]

    def get_top_positive_reviews(self, restaurant_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtener las reseñas más positivas de un restaurante"""
        return self.get_reviews_by_sentiment(restaurant_id, 'positivo', limit)

    def get_negative_reviews_for_improvement(
        self,
        restaurant_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Obtener reseñas negativas para identificar áreas de mejora.

        Args:
            restaurant_id: ID del restaurante
            limit: Número de reseñas negativas

        Returns:
            Lista de reseñas negativas con alta confianza
        """
        # Obtener reseñas negativas
        reviews = self.get_reviews_by_sentiment(restaurant_id, 'negativo', limit * 2)

        # Ordenar por confianza (las más seguras primero)
        sorted_reviews = sorted(
            reviews,
            key=lambda x: x.get('confidence', 0),
            reverse=True
        )[:limit]

        return sorted_reviews

    def compare_restaurants_sentiment(
        self,
        restaurant_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Comparar sentimientos entre múltiples restaurantes.

        Args:
            restaurant_ids: Lista de IDs de restaurantes

        Returns:
            Comparación de sentimientos
        """
        comparisons = {}

        for restaurant_id in restaurant_ids:
            stats = self.get_sentiment_statistics(restaurant_id)
            comparisons[restaurant_id] = {
                'total_reviews': stats['total'],
                'sentiments': stats['sentiments'],
                'percentages': stats['percentages'],
                'avg_confidence': stats.get('avg_confidence'),
                'positive_ratio': stats['percentages'].get('positivo', 0) / 100
            }

        # Ordenar por ratio positivo
        ranked = sorted(
            comparisons.items(),
            key=lambda x: x[1]['positive_ratio'],
            reverse=True
        )

        return {
            'total_restaurants': len(restaurant_ids),
            'comparisons': dict(comparisons),
            'ranking': [{'restaurant_id': r_id, **data} for r_id, data in ranked]
        }

    def batch_analyze_and_save(
        self,
        reviews: List[Review],
        save: bool = True
    ) -> Dict[str, Any]:
        """
        Analizar sentimientos en lote y opcionalmente guardar.

        Args:
            reviews: Lista de reseñas a analizar
            save: Si True, guarda los resultados en el repositorio

        Returns:
            Resumen del análisis en lote
        """
        if not self.sentiment_model or not self.sentiment_model.is_trained:
            raise ValueError("El modelo de sentimientos no está disponible o entrenado")

        # Filtrar reseñas sin sentimiento
        reviews_to_analyze = [r for r in reviews if r.sentiment is None]

        if not reviews_to_analyze:
            return {
                'total_reviews': len(reviews),
                'already_analyzed': len(reviews),
                'newly_analyzed': 0,
                'saved': False
            }

        # Extraer comentarios
        comments = [r.comment for r in reviews_to_analyze]

        # Analizar en lote
        results = self.sentiment_model.predict_batch(comments)

        # Actualizar reseñas
        for review, result in zip(reviews_to_analyze, results):
            review.sentiment = Sentiment(result['sentiment'])
            review.sentiment_confidence = result['confidence']
            review.sentiment_probabilities = result['probabilities']
            review.processed_comment = result['text_processed']

            if save:
                self.review_repository.save(review)

        return {
            'total_reviews': len(reviews),
            'already_analyzed': len(reviews) - len(reviews_to_analyze),
            'newly_analyzed': len(reviews_to_analyze),
            'saved': save,
            'sentiment_distribution': {
                'positivo': sum(1 for r in results if r['sentiment'] == 'positivo'),
                'neutro': sum(1 for r in results if r['sentiment'] == 'neutro'),
                'negativo': sum(1 for r in results if r['sentiment'] == 'negativo')
            }
        }

