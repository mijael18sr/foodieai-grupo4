"""
Sentiment Analysis API Routes
Endpoints para análisis de sentimientos de reseñas.
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional

from src.application.dto.sentiment_dto import (
    SentimentAnalysisRequestDTO,
    SentimentAnalysisResponseDTO,
    RestaurantSentimentStatsDTO,
    BatchSentimentAnalysisRequestDTO,
    BatchSentimentAnalysisResponseDTO,
    SentimentComparisonRequestDTO,
    SentimentComparisonResponseDTO,
    ReviewDTO,
    ModelPerformanceMetricsDTO,
    ModelMetricsPerClassDTO
)
from src.application.services.sentiment_service import SentimentAnalysisService
from src.infrastructure.container import get_review_repository, get_sentiment_model

# Router
router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment Analysis"]
)


def get_sentiment_service() -> SentimentAnalysisService:
    """Dependency injection para el servicio de sentimientos."""
    review_repo = get_review_repository()
    sentiment_model = get_sentiment_model()
    return SentimentAnalysisService(review_repo, sentiment_model)


@router.post(
    "/analyze",
    response_model=SentimentAnalysisResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Analizar sentimiento de un comentario",
    description="Analiza el sentimiento de un comentario individual usando el modelo de Redes Bayesianas."
)
async def analyze_sentiment(request: SentimentAnalysisRequestDTO):
    """
    Analizar el sentimiento de un comentario.

    - **comment**: Texto del comentario a analizar

    Retorna el sentimiento predicho (positivo/neutro/negativo) con su confianza.
    """
    try:
        service = get_sentiment_service()
        result = service.analyze_comment(request.comment)

        return SentimentAnalysisResponseDTO(
            comment=result['comment'],
            sentiment=result['sentiment'],
            confidence=result['confidence'],
            confidence_level=result.get('confidence_level'),
            probabilities=result['probabilities'],
            processed_text=result.get('processed_text')
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analizando sentimiento: {str(e)}"
        )


@router.post(
    "/analyze/batch",
    response_model=BatchSentimentAnalysisResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Analizar múltiples comentarios",
    description="Analiza el sentimiento de múltiples comentarios en una sola petición."
)
async def analyze_batch_sentiment(request: BatchSentimentAnalysisRequestDTO):
    """
    Analizar sentimientos de múltiples comentarios.

    - **comments**: Lista de comentarios (máximo 100)

    Retorna análisis individual de cada comentario y un resumen agregado.
    """
    try:
        service = get_sentiment_service()

        results = []
        summary = {"positivo": 0, "neutro": 0, "negativo": 0}

        for comment in request.comments:
            result = service.analyze_comment(comment)
            results.append(SentimentAnalysisResponseDTO(
                comment=result['comment'],
                sentiment=result['sentiment'],
                confidence=result['confidence'],
                probabilities=result['probabilities'],
                processed_text=result.get('processed_text')
            ))
            summary[result['sentiment']] += 1

        return BatchSentimentAnalysisResponseDTO(
            total=len(results),
            results=results,
            summary=summary
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en análisis batch: {str(e)}"
        )


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=RestaurantSentimentStatsDTO,
    status_code=status.HTTP_200_OK,
    summary="Obtener estadísticas de sentimientos de un restaurante",
    description="Obtiene un análisis agregado de todos los sentimientos de las reseñas de un restaurante."
)
async def get_restaurant_sentiment_stats(restaurant_id: str):
    """
    Obtener estadísticas de sentimientos para un restaurante.

    - **restaurant_id**: ID del restaurante

    Retorna:
    - Total de reseñas
    - Distribución de sentimientos
    - Porcentajes
    - Confianza promedio
    """
    try:
        service = get_sentiment_service()
        stats = service.get_sentiment_statistics(restaurant_id)

        if stats['total'] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron reseñas para el restaurante {restaurant_id}"
            )

        return RestaurantSentimentStatsDTO(
            restaurant_id=restaurant_id,
            total_reviews=stats['total'],
            sentiments=stats['sentiments'],
            sentiment_percentages=stats['percentages'],
            avg_confidence=stats.get('avg_confidence')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )


@router.get(
    "/restaurant/{restaurant_id}/reviews",
    response_model=list[ReviewDTO],
    status_code=status.HTTP_200_OK,
    summary="Obtener reseñas filtradas por sentimiento",
    description="Obtiene las reseñas de un restaurante filtradas por un sentimiento específico."
)
async def get_reviews_by_sentiment(
    restaurant_id: str,
    sentiment: str = Query(..., description="Sentimiento a filtrar (positivo/neutro/negativo)"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de reseñas")
):
    """
    Obtener reseñas filtradas por sentimiento.

    - **restaurant_id**: ID del restaurante
    - **sentiment**: Sentimiento a filtrar (positivo, neutro, negativo)
    - **limit**: Número máximo de reseñas (1-50)

    Retorna lista de reseñas con el sentimiento especificado.
    """
    try:
        service = get_sentiment_service()
        reviews = service.get_reviews_by_sentiment(restaurant_id, sentiment, limit)

        return [
            ReviewDTO(
                id=review['id'],
                comment=review['comment'],
                rating=review['rating'],
                username=review['username'],
                date=review.get('date'),
                sentiment=review.get('sentiment'),
                confidence=review.get('confidence')
            )
            for review in reviews
        ]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo reseñas: {str(e)}"
        )


@router.get(
    "/model/info",
    status_code=status.HTTP_200_OK,
    summary="Obtener información del modelo",
    description="Obtiene metadatos del modelo de análisis de sentimientos."
)
async def get_model_info():
    """
    Obtener información del modelo de sentimientos.

    Retorna:
    - Nombre del modelo
    - Estado de entrenamiento
    - Metadatos (vocabulario, clases, etc.)
    """
    try:
        sentiment_model = get_sentiment_model()

        return {
            "model_name": sentiment_model.model_name,
            "is_trained": sentiment_model.is_trained,
            "metadata": sentiment_model.metadata,
            "classes": sentiment_model.sentiment_classes
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo info del modelo: {str(e)}"
        )


@router.get(
    "/model/metrics",
    response_model=ModelPerformanceMetricsDTO,
    status_code=status.HTTP_200_OK,
    summary="Obtener métricas del modelo de sentimientos",
    description="Obtiene las métricas completas del modelo incluyendo precisión, recall, F1-score y métricas equivalentes al R² para clasificación."
)
async def get_model_metrics():
    """
    Obtener métricas completas del modelo de sentimientos.

    Retorna:
    - Accuracy (exactitud general)
    - Precision, Recall, F1-Score (macro y weighted)
    - Cohen's Kappa (equivalente a R² para clasificación)
    - Matthews Correlation Coefficient
    - Métricas detalladas por clase (positivo, neutro, negativo)
    """
    try:
        service = get_sentiment_service()
        model = service.sentiment_model

        if not model.is_trained:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El modelo no está entrenado. Ejecute el entrenamiento primero."
            )

        # Obtener métricas del modelo
        test_metrics = model.metadata.get('test_metrics', {})

        if not test_metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay métricas de evaluación disponibles. Re-entrene el modelo con datos de test."
            )

        # Construir métricas por clase
        per_class_metrics = {}
        per_class_data = test_metrics.get('per_class', {})

        for clase, metrics in per_class_data.items():
            per_class_metrics[clase] = ModelMetricsPerClassDTO(
                precision=metrics.get('precision', 0.0),
                recall=metrics.get('recall', 0.0),
                f1_score=metrics.get('f1-score', 0.0),
                support=metrics.get('support', 0)
            )

        # Calcular métricas macro faltantes desde métricas por clase
        precision_macro = test_metrics.get('precision_macro', 0.0)
        recall_macro = test_metrics.get('recall_macro', 0.0)
        precision_weighted = test_metrics.get('precision_weighted', 0.0)
        recall_weighted = test_metrics.get('recall_weighted', 0.0)

        # Si las métricas macro no están disponibles, calcularlas desde per_class
        if precision_macro == 0.0 and per_class_data:
            precisions = [metrics.get('precision', 0.0) for metrics in per_class_data.values()]
            precision_macro = sum(precisions) / len(precisions) if precisions else 0.0

        if recall_macro == 0.0 and per_class_data:
            recalls = [metrics.get('recall', 0.0) for metrics in per_class_data.values()]
            recall_macro = sum(recalls) / len(recalls) if recalls else 0.0

        if precision_weighted == 0.0 and per_class_data:
            total_support = sum(metrics.get('support', 0) for metrics in per_class_data.values())
            if total_support > 0:
                precision_weighted = sum(
                    metrics.get('precision', 0.0) * metrics.get('support', 0)
                    for metrics in per_class_data.values()
                ) / total_support

        if recall_weighted == 0.0 and per_class_data:
            total_support = sum(metrics.get('support', 0) for metrics in per_class_data.values())
            if total_support > 0:
                recall_weighted = sum(
                    metrics.get('recall', 0.0) * metrics.get('support', 0)
                    for metrics in per_class_data.values()
                ) / total_support

        return ModelPerformanceMetricsDTO(
            accuracy=test_metrics.get('accuracy', 0.0),
            precision_macro=precision_macro,
            precision_weighted=precision_weighted,
            recall_macro=recall_macro,
            recall_weighted=recall_weighted,
            f1_macro=test_metrics.get('f1_macro', 0.0),
            f1_weighted=test_metrics.get('f1_weighted', 0.0),
            cohen_kappa=test_metrics.get('cohen_kappa'),
            matthews_corrcoef=test_metrics.get('matthews_corrcoef'),
            per_class_metrics=per_class_metrics,
            last_evaluation=test_metrics.get('evaluation_date')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo métricas del modelo: {str(e)}"
        )
