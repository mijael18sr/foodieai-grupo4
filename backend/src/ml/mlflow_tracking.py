"""
MLflow Integration for Restaurant Recommender ML
================================================
Provides model tracking, versioning, and deployment capabilities.
"""

import os
import json
import joblib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# MLflow imports with fallback
try:
    import mlflow
    import mlflow.sklearn
    from mlflow.tracking import MlflowClient
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("Warning: MLflow not installed. Model tracking disabled.")


class MLflowManager:
    """
    Manager class for MLflow integration.
    Handles model tracking, logging, and registry operations.
    """
    
    def __init__(
        self, 
        tracking_uri: Optional[str] = None,
        experiment_name: str = "restaurant-recommender"
    ):
        """
        Initialize MLflow manager.
        
        Args:
            tracking_uri: MLflow tracking server URI
            experiment_name: Name of the experiment
        """
        self.tracking_uri = tracking_uri or os.getenv(
            "MLFLOW_TRACKING_URI", 
            "http://localhost:5000"
        )
        self.experiment_name = experiment_name
        self.client = None
        self._initialized = False
        
        if MLFLOW_AVAILABLE:
            self._initialize()
    
    def _initialize(self):
        """Initialize MLflow connection."""
        try:
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            self.client = MlflowClient(self.tracking_uri)
            self._initialized = True
            print(f"MLflow initialized: {self.tracking_uri}")
        except Exception as e:
            print(f"Warning: Could not connect to MLflow: {e}")
            self._initialized = False
    
    @property
    def is_available(self) -> bool:
        """Check if MLflow is available and initialized."""
        return MLFLOW_AVAILABLE and self._initialized
    
    def log_model_training(
        self,
        model: Any,
        model_name: str,
        metrics: Dict[str, float],
        params: Dict[str, Any],
        artifacts_path: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Log a model training run to MLflow.
        
        Args:
            model: Trained model object
            model_name: Name for the model
            metrics: Dictionary of metrics (accuracy, f1, etc.)
            params: Dictionary of hyperparameters
            artifacts_path: Path to additional artifacts
            tags: Optional tags for the run
            
        Returns:
            Run ID if successful, None otherwise
        """
        if not self.is_available:
            print("MLflow not available. Skipping logging.")
            return None
        
        try:
            with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}") as run:
                # Log parameters
                for key, value in params.items():
                    mlflow.log_param(key, value)
                
                # Log metrics
                for key, value in metrics.items():
                    mlflow.log_metric(key, value)
                
                # Log model
                mlflow.sklearn.log_model(
                    model, 
                    model_name,
                    registered_model_name=model_name
                )
                
                # Log additional artifacts
                if artifacts_path and Path(artifacts_path).exists():
                    mlflow.log_artifacts(artifacts_path)
                
                # Add tags
                if tags:
                    for key, value in tags.items():
                        mlflow.set_tag(key, value)
                
                # Add default tags
                mlflow.set_tag("model_type", model_name)
                mlflow.set_tag("framework", "scikit-learn")
                mlflow.set_tag("environment", os.getenv("ENVIRONMENT", "development"))
                
                print(f"Model logged to MLflow. Run ID: {run.info.run_id}")
                return run.info.run_id
                
        except Exception as e:
            print(f"Error logging to MLflow: {e}")
            return None
    
    def load_model(
        self, 
        model_name: str, 
        version: str = "latest"
    ) -> Optional[Any]:
        """
        Load a model from MLflow registry.
        
        Args:
            model_name: Name of the registered model
            version: Version to load ('latest' or specific version number)
            
        Returns:
            Loaded model or None if not found
        """
        if not self.is_available:
            return None
        
        try:
            if version == "latest":
                model_uri = f"models:/{model_name}/latest"
            else:
                model_uri = f"models:/{model_name}/{version}"
            
            model = mlflow.sklearn.load_model(model_uri)
            print(f"Loaded model: {model_name} (version: {version})")
            return model
            
        except Exception as e:
            print(f"Could not load model from MLflow: {e}")
            return None
    
    def get_latest_run(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about the latest run for a model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with run information
        """
        if not self.is_available:
            return None
        
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if not experiment:
                return None
            
            runs = mlflow.search_runs(
                experiment_ids=[experiment.experiment_id],
                filter_string=f"tags.model_type = '{model_name}'",
                order_by=["start_time DESC"],
                max_results=1
            )
            
            if runs.empty:
                return None
            
            run = runs.iloc[0]
            return {
                "run_id": run["run_id"],
                "start_time": run["start_time"],
                "metrics": {k.replace("metrics.", ""): v for k, v in run.items() if k.startswith("metrics.")},
                "params": {k.replace("params.", ""): v for k, v in run.items() if k.startswith("params.")}
            }
            
        except Exception as e:
            print(f"Error getting latest run: {e}")
            return None
    
    def compare_models(
        self, 
        model_name: str, 
        n_runs: int = 5
    ) -> Optional[list]:
        """
        Compare recent model runs.
        
        Args:
            model_name: Name of the model
            n_runs: Number of runs to compare
            
        Returns:
            List of run comparisons
        """
        if not self.is_available:
            return None
        
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if not experiment:
                return None
            
            runs = mlflow.search_runs(
                experiment_ids=[experiment.experiment_id],
                filter_string=f"tags.model_type = '{model_name}'",
                order_by=["start_time DESC"],
                max_results=n_runs
            )
            
            comparisons = []
            for _, run in runs.iterrows():
                comparisons.append({
                    "run_id": run["run_id"],
                    "start_time": str(run["start_time"]),
                    "accuracy": run.get("metrics.accuracy", None),
                    "f1_score": run.get("metrics.f1_score", None),
                    "precision": run.get("metrics.precision", None),
                    "recall": run.get("metrics.recall", None)
                })
            
            return comparisons
            
        except Exception as e:
            print(f"Error comparing models: {e}")
            return None


# Global MLflow manager instance
mlflow_manager = MLflowManager()


def log_sentiment_model(
    model: Any,
    accuracy: float,
    f1_score: float,
    precision: float,
    recall: float,
    vocab_size: int,
    ngram_range: tuple,
    train_size: int,
    test_size: int
) -> Optional[str]:
    """
    Convenience function to log sentiment model training.
    
    Returns:
        Run ID if successful
    """
    return mlflow_manager.log_model_training(
        model=model,
        model_name="sentiment_model",
        metrics={
            "accuracy": accuracy,
            "f1_score": f1_score,
            "precision": precision,
            "recall": recall
        },
        params={
            "vocab_size": vocab_size,
            "ngram_range": str(ngram_range),
            "train_size": train_size,
            "test_size": test_size,
            "model_type": "VotingClassifier",
            "algorithms": "ComplementNB + LogisticRegression"
        },
        tags={
            "task": "sentiment_analysis",
            "language": "spanish",
            "domain": "restaurant_reviews"
        }
    )


def log_recommender_model(
    model: Any,
    coverage: float,
    diversity: float,
    n_restaurants: int,
    n_features: int
) -> Optional[str]:
    """
    Convenience function to log recommender model training.
    
    Returns:
        Run ID if successful
    """
    return mlflow_manager.log_model_training(
        model=model,
        model_name="recommender_system",
        metrics={
            "coverage": coverage,
            "diversity": diversity
        },
        params={
            "n_restaurants": n_restaurants,
            "n_features": n_features,
            "model_type": "ContentBased"
        },
        tags={
            "task": "recommendation",
            "domain": "restaurants"
        }
    )
