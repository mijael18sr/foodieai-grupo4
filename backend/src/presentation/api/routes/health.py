"""
HEALTH CHECK ENDPOINT PARA PRODUCCIÓN
Monitoreo del modelo híbrido optimizado
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import psutil
import os

router = APIRouter(prefix="/health", tags=["Health Check"])

@router.get("/status")
async def health_status():
    """Health check básico del sistema con modelo híbrido"""
    try:
        from src.infrastructure.container import get_sentiment_model

        # Verificar modelo
        model = get_sentiment_model()
        model_status = model.is_trained if model else False

        # Métricas del sistema
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=1)

        # Test rápido del modelo
        test_prediction = None
        if model_status:
            try:
                result = model.predict_single("La comida estuvo excelente")
                test_prediction = {
                    "sentiment": result["sentiment"],
                    "confidence": round(result["confidence"], 3)
                }
            except Exception as e:
                test_prediction = {"error": str(e)}

        # Obtener métricas del modelo híbrido
        model_info = {}
        if model and model.metadata:
            test_metrics = model.metadata.get("test_metrics", {})
            model_info = {
                "type": model.metadata.get("model_type", "standard"),
                "accuracy": round(test_metrics.get("accuracy", 0), 3),
                "cohen_kappa": round(test_metrics.get("cohen_kappa", 0), 4),
                "f1_neutro": round(test_metrics.get("per_class", {}).get("neutro", {}).get("f1-score", 0), 3)
            }

        status = "healthy"
        if not model_status:
            status = "critical"
        elif memory_usage > 90 or cpu_usage > 90:
            status = "warning"

        return {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "model": {
                "loaded": model_status,
                **model_info
            },
            "system": {
                "memory_usage_percent": round(memory_usage, 2),
                "cpu_usage_percent": round(cpu_usage, 2),
                "process_id": os.getpid()
            },
            "test_prediction": test_prediction,
            "version": "hybrid_v1.0"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/metrics/detailed")
async def detailed_metrics():
    """Métricas detalladas del modelo híbrido para monitoreo"""
    try:
        from src.infrastructure.container import get_sentiment_model

        model = get_sentiment_model()
        if not model or not model.is_trained:
            raise HTTPException(status_code=503, detail="Model not available")

        metadata = model.metadata or {}
        test_metrics = metadata.get("test_metrics", {})

        return {
            "model_info": {
                "type": metadata.get("model_type", "standard"),
                "vocab_size": metadata.get("vocab_size", 0),
                "training_samples": metadata.get("n_samples", 0),
                "classes": metadata.get("sentiment_classes", []),
                "balancing_strategy": metadata.get("balancing_strategy", "none"),
                "ensemble_models": metadata.get("ensemble_models", [])
            },
            "performance_metrics": {
                "accuracy": test_metrics.get("accuracy", 0),
                "cohen_kappa": test_metrics.get("cohen_kappa", 0),
                "f1_weighted": test_metrics.get("f1_weighted", 0),
                "f1_macro": test_metrics.get("f1_macro", 0),
                "matthews_corrcoef": test_metrics.get("matthews_corrcoef", 0),
                "precision_weighted": test_metrics.get("precision_weighted", 0),
                "recall_weighted": test_metrics.get("recall_weighted", 0)
            },
            "per_class_metrics": test_metrics.get("per_class", {}),
            "evaluation_info": {
                "last_evaluation": test_metrics.get("evaluation_date", None),
                "test_samples": test_metrics.get("n_test_samples", 0)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.get("/benchmark")
async def run_benchmark():
    """Ejecutar benchmark rápido del modelo híbrido"""
    try:
        from src.infrastructure.container import get_sentiment_model

        model = get_sentiment_model()
        if not model or not model.is_trained:
            raise HTTPException(status_code=503, detail="Model not available")

        # Ejemplos de benchmark
        benchmark_cases = [
            ("positivo", "Excelente comida y servicio increíble"),
            ("negativo", "Pésimo servicio, comida fría y cara"),
            ("neutro", "Normal, nada especial, ni bueno ni malo"),
            ("positivo", "Increíble experiencia gastronómica"),
            ("negativo", "No me gustó para nada"),
            ("neutro", "Está bien, precio promedio"),
            ("positivo", "Totalmente recomendado, delicioso"),
            ("neutro", "Regular, sin más")
        ]

        results = []
        correct = 0
        total_confidence = 0

        for expected, text in benchmark_cases:
            try:
                result = model.predict_single(text)
                predicted = result["sentiment"]
                confidence = result["confidence"]

                is_correct = predicted.lower() == expected.lower()
                if is_correct:
                    correct += 1

                total_confidence += confidence

                results.append({
                    "text": text,
                    "expected": expected,
                    "predicted": predicted,
                    "confidence": round(confidence, 3),
                    "correct": is_correct
                })

            except Exception as e:
                results.append({
                    "text": text,
                    "expected": expected,
                    "error": str(e),
                    "correct": False
                })

        accuracy = correct / len(benchmark_cases)
        avg_confidence = total_confidence / len(benchmark_cases)

        return {
            "benchmark_summary": {
                "total_cases": len(benchmark_cases),
                "correct_predictions": correct,
                "accuracy": round(accuracy, 3),
                "average_confidence": round(avg_confidence, 3)
            },
            "detailed_results": results,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")
