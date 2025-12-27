"""
ENTRENAMIENTO DE MODELO DE SENTIMIENTOS CON MLFLOW
Versión con tracking completo de experimentos y modelo registry
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print(" ENTRENAMIENTO DE MODELO DE SENTIMIENTOS CON MLFLOW")
print("=" * 80)

# Importaciones
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, cohen_kappa_score,
    f1_score, matthews_corrcoef, confusion_matrix, ConfusionMatrixDisplay
)

# MLflow
try:
    import mlflow
    import mlflow.sklearn
    from mlflow.tracking import MlflowClient
    MLFLOW_AVAILABLE = True
    print(" MLflow disponible para tracking")
except ImportError:
    MLFLOW_AVAILABLE = False
    print(" MLflow no disponible, se usará tracking local")

# Configuración MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = "sentiment-analysis"
MODEL_NAME = "sentiment-model-restaurant"


def setup_mlflow():
    """Configura MLflow tracking."""
    if not MLFLOW_AVAILABLE:
        return None
    
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        
        # Crear o obtener experimento
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        if experiment is None:
            experiment_id = mlflow.create_experiment(
                EXPERIMENT_NAME,
                tags={"project": "restaurant-recommender", "team": "UNMSM-ML"}
            )
        else:
            experiment_id = experiment.experiment_id
        
        mlflow.set_experiment(EXPERIMENT_NAME)
        print(f" MLflow conectado: {MLFLOW_TRACKING_URI}")
        print(f" Experimento: {EXPERIMENT_NAME} (ID: {experiment_id})")
        return MlflowClient(MLFLOW_TRACKING_URI)
    except Exception as e:
        print(f" Error conectando a MLflow: {e}")
        print(" Continuando sin tracking remoto...")
        return None


def train_sentiment_model(data_path: str, mlflow_client=None):
    """
    Entrena el modelo de sentimientos con tracking MLflow.
    
    Args:
        data_path: Ruta al archivo CSV de datos
        mlflow_client: Cliente MLflow opcional
    
    Returns:
        Tupla (modelo, vectorizador, métricas)
    """
    # =========================================================================
    # 1. CARGAR Y PREPARAR DATOS
    # =========================================================================
    print("\n" + "=" * 60)
    print(" FASE 1: CARGA DE DATOS")
    print("=" * 60)
    
    df = pd.read_csv(data_path)
    print(f" Datos cargados: {len(df):,} registros")
    
    # Distribución
    print(f"\n Distribución de clases:")
    dist = df['sentimiento'].value_counts()
    for sent, count in dist.items():
        pct = (count / len(df)) * 100
        print(f" • {sent:10s}: {count:8,} ({pct:5.1f}%)")
    
    X = df['comment']
    y = df['sentimiento']
    
    # Split estratificado
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n Train: {len(X_train):,} | Test: {len(X_test):,}")
    
    # =========================================================================
    # 2. PARÁMETROS DEL MODELO
    # =========================================================================
    print("\n" + "=" * 60)
    print(" FASE 2: CONFIGURACIÓN DEL MODELO")
    print("=" * 60)
    
    # Hiperparámetros (para logging)
    params = {
        # TF-IDF
        "tfidf_max_features": 15000,
        "tfidf_ngram_range_min": 1,
        "tfidf_ngram_range_max": 2,
        "tfidf_min_df": 3,
        "tfidf_max_df": 0.90,
        "tfidf_sublinear_tf": True,
        # Logistic Regression
        "lr_max_iter": 1000,
        "lr_solver": "saga",
        "lr_C": 1.0,
        "lr_class_weight": "balanced",
        # Naive Bayes
        "nb_alpha": 0.1,
        # General
        "test_size": 0.2,
        "random_state": 42,
        "n_samples": len(df)
    }
    
    print(" Hiperparámetros configurados:")
    for key, value in list(params.items())[:5]:
        print(f" • {key}: {value}")
    print(f" ... y {len(params) - 5} más")
    
    # =========================================================================
    # 3. VECTORIZACIÓN
    # =========================================================================
    print("\n" + "=" * 60)
    print(" FASE 3: VECTORIZACIÓN TF-IDF")
    print("=" * 60)
    
    vectorizer = TfidfVectorizer(
        max_features=params["tfidf_max_features"],
        ngram_range=(params["tfidf_ngram_range_min"], params["tfidf_ngram_range_max"]),
        min_df=params["tfidf_min_df"],
        max_df=params["tfidf_max_df"],
        sublinear_tf=params["tfidf_sublinear_tf"],
        strip_accents='unicode',
        lowercase=True,
        use_idf=True,
        smooth_idf=True,
        norm='l2'
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    vocab_size = len(vectorizer.vocabulary_)
    params["actual_vocab_size"] = vocab_size
    
    print(f" Vocabulario: {vocab_size:,} términos")
    print(f" Matriz train: {X_train_tfidf.shape}")
    
    # =========================================================================
    # 4. ENTRENAMIENTO
    # =========================================================================
    print("\n" + "=" * 60)
    print(" FASE 4: ENTRENAMIENTO DEL MODELO")
    print("=" * 60)
    
    # Crear clasificadores
    nb_clf = ComplementNB(alpha=params["nb_alpha"])
    lr_clf = LogisticRegression(
        max_iter=params["lr_max_iter"],
        class_weight=params["lr_class_weight"],
        solver=params["lr_solver"],
        random_state=params["random_state"],
        C=params["lr_C"]
    )
    
    # Entrenar individual para comparar
    print("\n Entrenando Complement Naive Bayes...")
    nb_clf.fit(X_train_tfidf, y_train)
    nb_score = nb_clf.score(X_test_tfidf, y_test)
    print(f" → Accuracy: {nb_score:.4f}")
    
    print("\n Entrenando Logistic Regression...")
    lr_clf.fit(X_train_tfidf, y_train)
    lr_score = lr_clf.score(X_test_tfidf, y_test)
    print(f" → Accuracy: {lr_score:.4f}")
    
    # Ensemble
    print("\n Entrenando Ensemble (Voting)...")
    ensemble = VotingClassifier(
        estimators=[
            ('nb', ComplementNB(alpha=params["nb_alpha"])),
            ('lr', LogisticRegression(
                max_iter=params["lr_max_iter"],
                class_weight=params["lr_class_weight"],
                solver=params["lr_solver"],
                random_state=params["random_state"],
                C=params["lr_C"]
            ))
        ],
        voting='soft'
    )
    ensemble.fit(X_train_tfidf, y_train)
    ensemble_score = ensemble.score(X_test_tfidf, y_test)
    print(f" → Accuracy: {ensemble_score:.4f}")
    
    # Seleccionar mejor
    scores = {
        "naive_bayes": nb_score,
        "logistic_regression": lr_score,
        "ensemble": ensemble_score
    }
    best_model_name = max(scores, key=scores.get)
    
    if best_model_name == "ensemble":
        classifier = ensemble
    elif best_model_name == "logistic_regression":
        classifier = lr_clf
    else:
        classifier = nb_clf
    
    params["selected_model"] = best_model_name
    print(f"\n Modelo seleccionado: {best_model_name} ({scores[best_model_name]:.4f})")
    
    # Cross-validation
    print("\n Validación cruzada (5-fold)...")
    cv_scores = cross_val_score(classifier, X_train_tfidf, y_train, cv=5)
    params["cv_mean"] = float(cv_scores.mean())
    params["cv_std"] = float(cv_scores.std())
    print(f" → CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # =========================================================================
    # 5. EVALUACIÓN
    # =========================================================================
    print("\n" + "=" * 60)
    print(" FASE 5: EVALUACIÓN DEL MODELO")
    print("=" * 60)
    
    y_pred = classifier.predict(X_test_tfidf)
    
    # Métricas principales
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "cohen_kappa": float(cohen_kappa_score(y_test, y_pred)),
        "f1_weighted": float(f1_score(y_test, y_pred, average='weighted')),
        "f1_macro": float(f1_score(y_test, y_pred, average='macro')),
        "matthews_corrcoef": float(matthews_corrcoef(y_test, y_pred)),
        "nb_accuracy": nb_score,
        "lr_accuracy": lr_score,
        "ensemble_accuracy": ensemble_score
    }
    
    print(f"\n Métricas principales:")
    print(f" • Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f" • Cohen's Kappa: {metrics['cohen_kappa']:.4f}")
    print(f" • F1-Score (weighted): {metrics['f1_weighted']:.4f}")
    print(f" • F1-Score (macro): {metrics['f1_macro']:.4f}")
    print(f" • Matthews Correlation: {metrics['matthews_corrcoef']:.4f}")
    
    # Métricas por clase
    report = classification_report(y_test, y_pred, output_dict=True)
    for clase in ['positivo', 'neutro', 'negativo']:
        if clase in report:
            metrics[f"{clase}_precision"] = float(report[clase]['precision'])
            metrics[f"{clase}_recall"] = float(report[clase]['recall'])
            metrics[f"{clase}_f1"] = float(report[clase]['f1-score'])
    
    print(f"\n Métricas por clase:")
    for clase in ['positivo', 'neutro', 'negativo']:
        if clase in report:
            print(f" {clase.upper()}: P={report[clase]['precision']:.3f} | "
                  f"R={report[clase]['recall']:.3f} | F1={report[clase]['f1-score']:.3f}")
    
    # =========================================================================
    # 6. MLFLOW TRACKING
    # =========================================================================
    if MLFLOW_AVAILABLE:
        print("\n" + "=" * 60)
        print(" FASE 6: LOGGING EN MLFLOW")
        print("=" * 60)
        
        try:
            run_name = f"sentiment-train-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            with mlflow.start_run(run_name=run_name) as run:
                # Log parámetros
                mlflow.log_params(params)
                print(f" Parámetros registrados: {len(params)}")
                
                # Log métricas
                mlflow.log_metrics(metrics)
                print(f" Métricas registradas: {len(metrics)}")
                
                # Log modelo
                mlflow.sklearn.log_model(
                    classifier, 
                    "model",
                    registered_model_name=MODEL_NAME
                )
                print(f" Modelo registrado: {MODEL_NAME}")
                
                # Log vectorizador como artifact
                import joblib
                vectorizer_path = "/tmp/vectorizer.pkl"
                joblib.dump(vectorizer, vectorizer_path)
                mlflow.log_artifact(vectorizer_path, "vectorizer")
                print(f" Vectorizador guardado como artifact")
                
                # Crear y guardar matriz de confusión
                fig, ax = plt.subplots(figsize=(8, 6))
                cm = confusion_matrix(y_test, y_pred, labels=['negativo', 'neutro', 'positivo'])
                disp = ConfusionMatrixDisplay(cm, display_labels=['Negativo', 'Neutro', 'Positivo'])
                disp.plot(ax=ax, cmap='Blues', values_format='d')
                ax.set_title(f'Matriz de Confusión - Accuracy: {metrics["accuracy"]:.2%}')
                
                mlflow.log_figure(fig, "confusion_matrix.png")
                plt.close()
                print(f" Matriz de confusión guardada")
                
                # Crear gráfico de métricas por clase
                fig2, ax2 = plt.subplots(figsize=(10, 6))
                clases = ['positivo', 'neutro', 'negativo']
                x = np.arange(len(clases))
                width = 0.25
                
                precision = [report[c]['precision'] for c in clases]
                recall = [report[c]['recall'] for c in clases]
                f1 = [report[c]['f1-score'] for c in clases]
                
                ax2.bar(x - width, precision, width, label='Precision', color='#3498db')
                ax2.bar(x, recall, width, label='Recall', color='#2ecc71')
                ax2.bar(x + width, f1, width, label='F1-Score', color='#e74c3c')
                
                ax2.set_xlabel('Clase')
                ax2.set_ylabel('Score')
                ax2.set_title('Métricas por Clase de Sentimiento')
                ax2.set_xticks(x)
                ax2.set_xticklabels([c.capitalize() for c in clases])
                ax2.legend()
                ax2.set_ylim(0, 1)
                ax2.grid(axis='y', alpha=0.3)
                
                mlflow.log_figure(fig2, "metrics_by_class.png")
                plt.close()
                print(f" Gráfico de métricas guardado")
                
                # Tags adicionales
                mlflow.set_tags({
                    "model_type": "sentiment_analysis",
                    "domain": "restaurant_reviews",
                    "language": "spanish",
                    "best_classifier": best_model_name
                })
                
                print(f"\n Run ID: {run.info.run_id}")
                print(f" Experimento: {EXPERIMENT_NAME}")
                print(f" URL: {MLFLOW_TRACKING_URI}/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}")
                
        except Exception as e:
            print(f" Error en MLflow logging: {e}")
    
    return classifier, vectorizer, metrics, params


def main():
    """Función principal de entrenamiento."""
    # Setup
    mlflow_client = setup_mlflow() if MLFLOW_AVAILABLE else None
    
    # Ruta de datos
    data_path = project_root / "data" / "processed" / "modelo_limpio.csv"
    
    if not data_path.exists():
        print(f" Error: No se encontró {data_path}")
        return
    
    # Entrenar
    classifier, vectorizer, metrics, params = train_sentiment_model(
        str(data_path), 
        mlflow_client
    )
    
    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    print("\n" + "=" * 80)
    print(" ENTRENAMIENTO COMPLETADO")
    print("=" * 80)
    print(f"\n Accuracy Final: {metrics['accuracy']*100:.2f}%")
    print(f" Modelo: {params['selected_model']}")
    print(f" Vocabulario: {params['actual_vocab_size']:,} términos")
    
    if MLFLOW_AVAILABLE:
        print(f"\n Ver resultados en: {MLFLOW_TRACKING_URI}")
        print(f" Experimento: {EXPERIMENT_NAME}")


if __name__ == "__main__":
    main()
