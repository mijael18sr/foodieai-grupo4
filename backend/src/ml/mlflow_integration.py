"""
MLflow Integration Module for Restaurant Recommender ML

Este módulo proporciona funciones para:
- Registrar experimentos de entrenamiento
- Guardar métricas y parámetros
- Versionar modelos
- Gestionar el ciclo de vida de modelos ML
"""

import os
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class MLflowManager:
    """Gestiona la integración con MLflow para tracking y model registry."""
    
    def __init__(
        self,
        tracking_uri: Optional[str] = None,
        experiment_name: str = "restaurant-recommender"
    ):
        """
        Inicializa el manager de MLflow.
        
        Args:
            tracking_uri: URI del servidor MLflow. Si es None, usa variable de entorno.
            experiment_name: Nombre del experimento.
        """
        self.tracking_uri = tracking_uri or os.getenv(
            "MLFLOW_TRACKING_URI", 
            "http://localhost:5000"
        )
        self.experiment_name = experiment_name
        self._setup_mlflow()
    
    def _setup_mlflow(self):
        """Configura la conexión con MLflow."""
        try:
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            self.client = MlflowClient(self.tracking_uri)
            logger.info(f"MLflow configurado: {self.tracking_uri}")
        except Exception as e:
            logger.warning(f"No se pudo conectar a MLflow: {e}. Usando tracking local.")
            mlflow.set_tracking_uri("sqlite:///mlflow.db")
    
    def start_run(
        self,
        run_name: str,
        tags: Optional[Dict[str, str]] = None
    ) -> mlflow.ActiveRun:
        """
        Inicia un nuevo run de MLflow.
        
        Args:
            run_name: Nombre descriptivo del run.
            tags: Tags adicionales para el run.
        
        Returns:
            El run activo de MLflow.
        """
        default_tags = {
            "project": "restaurant-recommender",
            "team": "UNMSM-ML"
        }
        if tags:
            default_tags.update(tags)
        
        return mlflow.start_run(run_name=run_name, tags=default_tags)
    
    def log_params(self, params: Dict[str, Any]):
        """
        Registra parámetros del modelo.
        
        Args:
            params: Diccionario de parámetros.
        """
        for key, value in params.items():
            mlflow.log_param(key, value)
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """
        Registra métricas del modelo.
        
        Args:
            metrics: Diccionario de métricas.
            step: Paso opcional (para métricas en serie temporal).
        """
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
    
    def log_model(
        self,
        model: Any,
        artifact_path: str = "model",
        registered_model_name: Optional[str] = None
    ):
        """
        Registra un modelo sklearn en MLflow.
        
        Args:
            model: Modelo entrenado (sklearn).
            artifact_path: Ruta del artifact.
            registered_model_name: Nombre para registrar en Model Registry.
        """
        mlflow.sklearn.log_model(
            model,
            artifact_path=artifact_path,
            registered_model_name=registered_model_name
        )
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None):
        """
        Registra un archivo como artifact.
        
        Args:
            local_path: Ruta local del archivo.
            artifact_path: Subdirectorio en artifacts.
        """
        mlflow.log_artifact(local_path, artifact_path)
    
    def log_figure(self, figure, artifact_file: str):
        """
        Registra una figura matplotlib.
        
        Args:
            figure: Figura matplotlib.
            artifact_file: Nombre del archivo.
        """
        mlflow.log_figure(figure, artifact_file)
    
    def end_run(self, status: str = "FINISHED"):
        """
        Finaliza el run actual.
        
        Args:
            status: Estado final (FINISHED, FAILED, KILLED).
        """
        mlflow.end_run(status=status)
    
    def get_best_model(
        self,
        metric_name: str = "accuracy",
        model_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Obtiene el mejor modelo basado en una métrica.
        
        Args:
            metric_name: Nombre de la métrica para comparar.
            model_name: Nombre del modelo registrado (opcional).
        
        Returns:
            URI del mejor modelo o None.
        """
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if not experiment:
                return None
            
            runs = mlflow.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=[f"metrics.{metric_name} DESC"],
                max_results=1
            )
            
            if runs.empty:
                return None
            
            best_run_id = runs.iloc[0]["run_id"]
            return f"runs:/{best_run_id}/model"
        except Exception as e:
            logger.error(f"Error obteniendo mejor modelo: {e}")
            return None
    
    def transition_model_stage(
        self,
        model_name: str,
        version: int,
        stage: str = "Production"
    ):
        """
        Transiciona un modelo a un stage (Staging, Production, Archived).
        
        Args:
            model_name: Nombre del modelo registrado.
            version: Versión del modelo.
            stage: Stage destino.
        """
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        logger.info(f"Modelo {model_name} v{version} transicionado a {stage}")


# Singleton instance
_mlflow_manager: Optional[MLflowManager] = None


def get_mlflow_manager() -> MLflowManager:
    """Obtiene la instancia singleton del MLflow manager."""
    global _mlflow_manager
    if _mlflow_manager is None:
        _mlflow_manager = MLflowManager()
    return _mlflow_manager


# Decorador conveniente para experimentos
def track_experiment(
    experiment_name: str = "restaurant-recommender",
    run_name: Optional[str] = None
):
    """
    Decorador para trackear automáticamente una función de entrenamiento.
    
    Uso:
        @track_experiment(run_name="sentiment-training-v1")
        def train_model(params):
            # ... training code ...
            return model, metrics
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager = MLflowManager(experiment_name=experiment_name)
            actual_run_name = run_name or func.__name__
            
            with manager.start_run(run_name=actual_run_name):
                result = func(*args, **kwargs)
                
                # Si la función retorna (model, metrics), loguearlos
                if isinstance(result, tuple) and len(result) == 2:
                    model, metrics = result
                    if isinstance(metrics, dict):
                        manager.log_metrics(metrics)
                    if model is not None:
                        manager.log_model(model)
                
                return result
        return wrapper
    return decorator
