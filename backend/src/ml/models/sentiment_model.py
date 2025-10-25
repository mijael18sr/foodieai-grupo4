"""
Sentiment Analysis Model
Modelo de análisis de sentimientos usando Redes Bayesianas (Naive Bayes).
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from pathlib import Path

# ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB

# NLP
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

from .base_model import BaseMLModel


class SentimentAnalysisModel(BaseMLModel):
    """
    Modelo de análisis de sentimientos con Redes Bayesianas.

    Clasifica comentarios de reseñas en:
    - positivo (rating 4-5)
    - neutro (rating 3)
    - negativo (rating 1-2)

    Utiliza:
    - TF-IDF para vectorización
    - Complement Naive Bayes para clasificación
    - Preprocesamiento con NLTK
    """

    def __init__(self):
        super().__init__("SentimentAnalysisModel")

        # Componentes del modelo
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.classifier: Optional[ComplementNB] = None

        # Preprocesamiento
        self.stemmer = SnowballStemmer('spanish')
        self._setup_stopwords()

        # Clases de sentimiento
        self.sentiment_classes = ['negativo', 'neutro', 'positivo']

    def _setup_stopwords(self):
        """Configurar stopwords personalizadas para español"""
        try:
            stopwords_spanish = set(stopwords.words('spanish'))
        except LookupError:
            nltk.download('stopwords')
            stopwords_spanish = set(stopwords.words('spanish'))

        # Palabras significativas que NO se eliminan (importantes para sentimientos)
        stopwords_significativas = {
            "no", "ni", "nada", "muy", "poco", "mucho", "más", "menos",
            "algo", "ya", "antes", "después", "hasta", "todo", "todos",
            "como", "para", "sin", "con", "pero", "aunque"
        }

        self.stopwords_custom = stopwords_spanish - stopwords_significativas

    def preprocess_text(self, text: str) -> str:
        """
        Preprocesar texto para análisis de sentimientos.

        Args:
            text: Texto original

        Returns:
            Texto preprocesado
        """
        if pd.isna(text) or not text:
            return ""

        # Convertir a minúsculas
        text = str(text).lower()

        # Tokenizar
        try:
            tokens = word_tokenize(text, language='spanish')
        except LookupError:
            nltk.download('punkt')
            tokens = word_tokenize(text, language='spanish')

        # Filtrar y aplicar stemming
        tokens = [
            self.stemmer.stem(word)
            for word in tokens
            if word.isalpha() and word not in self.stopwords_custom
        ]

        return " ".join(tokens)

    def train(self, X: pd.Series, y: pd.Series,
              max_features: int = 5000,
              ngram_range: tuple = (1, 2),
              alpha: float = 1.0) -> 'SentimentAnalysisModel':
        """
        Entrenar modelo de análisis de sentimientos.

        Args:
            X: Serie con comentarios de texto
            y: Serie con sentimientos (positivo, neutro, negativo)
            max_features: Número máximo de características TF-IDF
            ngram_range: Rango de n-gramas (unigramas, bigramas, etc.)
            alpha: Parámetro de suavizado de Laplace

        Returns:
            self: Modelo entrenado
        """
        print(f"\n{'='*80}")
        print(f"ENTRENANDO {self.model_name}")
        print(f"{'='*80}")

        # 1. Preprocesar textos
        print("\n[1/4] Preprocesando textos...")
        X_processed = X.apply(self.preprocess_text)
        print(f"      ✓ {len(X_processed)} comentarios preprocesados")

        # 2. Vectorización TF-IDF
        print("\n[2/4] Vectorización TF-IDF...")
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=5,
            max_df=0.8,
            sublinear_tf=True
        )
        X_tfidf = self.vectorizer.fit_transform(X_processed)
        print(f"      ✓ Vocabulario: {len(self.vectorizer.vocabulary_):,} términos")
        print(f"      ✓ Matriz: {X_tfidf.shape}")

        # 3. Entrenar clasificador
        print("\n[3/4] Entrenando Complement Naive Bayes...")
        self.classifier = ComplementNB(alpha=alpha)
        self.classifier.fit(X_tfidf, y)
        print(f"      ✓ Modelo entrenado")

        # 4. Guardar metadata
        self.is_trained = True
        self.metadata = {
            'max_features': max_features,
            'ngram_range': ngram_range,
            'alpha': alpha,
            'vocab_size': len(self.vectorizer.vocabulary_),
            'n_samples': len(X),
            'sentiment_classes': list(self.classifier.classes_),
            'class_distribution': y.value_counts().to_dict()
        }

        print("\n[4/4] Entrenamiento completado")
        print(f"      ✓ Clases: {list(self.classifier.classes_)}")
        print(f"{'='*80}\n")

        return self

    def predict(self, X: pd.Series) -> np.ndarray:
        """
        Predecir sentimientos para comentarios.

        Args:
            X: Serie con comentarios de texto

        Returns:
            Array con sentimientos predichos
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado. Llama a train() primero.")

        # Preprocesar y vectorizar
        X_processed = X.apply(self.preprocess_text)
        X_tfidf = self.vectorizer.transform(X_processed)

        # Predecir
        return self.classifier.predict(X_tfidf)

    def predict_single(self, text: str) -> Dict[str, Any]:
        """
        Predecir sentimiento para un solo comentario.

        Args:
            text: Comentario a analizar

        Returns:
            Diccionario con predicción completa
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado. Llama a train() primero.")

        # NOTA: El vectorizador TF-IDF ya hace su propio preprocesamiento
        # No usamos preprocess_text() porque el stemming puede dañar las palabras clave
        # El modelo fue entrenado con el texto directamente pasado al TF-IDF

        # Vectorizar directamente (el TF-IDF hace lowercase y tokenización internamente)
        text_vector = self.vectorizer.transform([text])

        # Predecir
        sentiment = self.classifier.predict(text_vector)[0]
        probabilities = self.classifier.predict_proba(text_vector)[0]

        # Crear diccionario de probabilidades
        prob_dict = dict(zip(self.classifier.classes_, probabilities))

        return {
            'text_original': text,
            'text_processed': text.lower(),  # Solo lowercase para mostrar
            'sentiment': sentiment,
            'confidence': float(max(probabilities)),
            'probabilities': {k: float(v) for k, v in prob_dict.items()}
        }

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Predecir sentimientos para múltiples comentarios.

        Args:
            texts: Lista de comentarios

        Returns:
            Lista de predicciones
        """
        return [self.predict_single(text) for text in texts]

    def evaluate(self, X_test: pd.Series, y_test: pd.Series) -> Dict[str, Any]:
        """
        Evaluar modelo con datos de prueba.

        Args:
            X_test: Comentarios de prueba
            y_test: Sentimientos reales

        Returns:
            Diccionario con métricas de evaluación
        """
        from sklearn.metrics import accuracy_score, f1_score, classification_report

        # Predecir
        y_pred = self.predict(X_test)

        # Calcular métricas
        metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'f1_score_weighted': float(f1_score(y_test, y_pred, average='weighted')),
            'f1_score_macro': float(f1_score(y_test, y_pred, average='macro')),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'n_samples': len(y_test)
        }

        return metrics

    def update_test_metrics(self, X_test: pd.Series, y_test: pd.Series) -> None:
        """
        Actualizar metadata del modelo con métricas completas de evaluación.

        Calcula y guarda:
        - Accuracy
        - Precision (macro/weighted)
        - Recall (macro/weighted)
        - F1-Score (macro/weighted)
        - Cohen's Kappa (equivalente a R² para clasificación)
        - Matthews Correlation Coefficient
        - Métricas por clase

        Args:
            X_test: Comentarios de prueba
            y_test: Sentimientos reales
        """
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            classification_report,
            cohen_kappa_score,
            matthews_corrcoef
        )
        from datetime import datetime

        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado.")

        # Predecir
        y_pred = self.predict(X_test)

        # Calcular métricas generales
        accuracy = float(accuracy_score(y_test, y_pred))
        precision_macro = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
        precision_weighted = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
        recall_macro = float(recall_score(y_test, y_pred, average='macro', zero_division=0))
        recall_weighted = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
        f1_macro = float(f1_score(y_test, y_pred, average='macro', zero_division=0))
        f1_weighted = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

        # Métricas adicionales (equivalentes a R² para clasificación)
        cohen_kappa = float(cohen_kappa_score(y_test, y_pred))
        matthews_corr = float(matthews_corrcoef(y_test, y_pred))

        # Reporte por clase
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        # Construir métricas por clase
        per_class = {}
        for clase in ['negativo', 'neutro', 'positivo']:
            if clase in report:
                per_class[clase] = {
                    'precision': float(report[clase]['precision']),
                    'recall': float(report[clase]['recall']),
                    'f1-score': float(report[clase]['f1-score']),
                    'support': int(report[clase]['support'])
                }

        # Actualizar metadata
        if self.metadata is None:
            self.metadata = {}

        self.metadata['test_metrics'] = {
            'accuracy': accuracy,
            'precision_macro': precision_macro,
            'precision_weighted': precision_weighted,
            'recall_macro': recall_macro,
            'recall_weighted': recall_weighted,
            'f1_macro': f1_macro,
            'f1_weighted': f1_weighted,
            'cohen_kappa': cohen_kappa,
            'matthews_corrcoef': matthews_corr,
            'per_class': per_class,
            'n_test_samples': len(y_test),
            'evaluation_date': datetime.now().isoformat()
        }

        print(f"\n✓ Métricas de evaluación actualizadas:")
        print(f"  • Accuracy: {accuracy:.4f}")
        print(f"  • F1-Score (macro): {f1_macro:.4f}")
        print(f"  • Cohen's Kappa: {cohen_kappa:.4f}")
        print(f"  • Matthews Correlation: {matthews_corr:.4f}")

    def get_top_features(self, n: int = 20, sentiment: Optional[str] = None) -> Dict[str, List[tuple]]:
        """
        Obtener las características más importantes por sentimiento.

        Args:
            n: Número de características top
            sentiment: Sentimiento específico (None = todos)

        Returns:
            Diccionario con top features por clase
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado.")

        feature_names = self.vectorizer.get_feature_names_out()
        top_features = {}

        classes = [sentiment] if sentiment else self.classifier.classes_

        for idx, class_name in enumerate(self.classifier.classes_):
            if class_name in classes:
                # Obtener log-probabilities de la clase
                log_probs = self.classifier.feature_log_prob_[idx]

                # Índices de top features
                top_indices = log_probs.argsort()[-n:][::-1]

                # Crear lista de (término, probabilidad)
                top_features[class_name] = [
                    (feature_names[i], float(np.exp(log_probs[i])))
                    for i in top_indices
                ]

        return top_features

    def save(self, path: str) -> None:
        """
        Guardar modelo completo (vectorizador + clasificador).

        Args:
            path: Ruta base para guardar (sin extensión)
        """
        import joblib

        model_path = Path(path)
        model_path.parent.mkdir(parents=True, exist_ok=True)

        # Guardar todo en un solo archivo
        model_data = {
            'classifier': self.classifier,
            'vectorizer': self.vectorizer,
            'metadata': self.metadata,
            'is_trained': self.is_trained,
            'model_name': self.model_name,
            'stopwords_custom': self.stopwords_custom
        }

        joblib.dump(model_data, model_path)
        print(f"✓ Modelo guardado: {model_path}")

    def load(self, path: str) -> 'SentimentAnalysisModel':
        """
        Cargar modelo desde disco.

        Args:
            path: Ruta del modelo guardado

        Returns:
            self: Modelo cargado
        """
        import joblib

        model_path = Path(path)
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")

        model_data = joblib.load(model_path)

        self.classifier = model_data['classifier']
        self.vectorizer = model_data['vectorizer']
        self.metadata = model_data['metadata']
        self.is_trained = model_data['is_trained']
        self.model_name = model_data['model_name']
        self.stopwords_custom = model_data.get('stopwords_custom', self.stopwords_custom)

        print(f"✓ Modelo cargado: {model_path}")
        print(f"  Vocabulario: {len(self.vectorizer.vocabulary_):,} términos")
        print(f"  Clases: {list(self.classifier.classes_)}")

        return self

