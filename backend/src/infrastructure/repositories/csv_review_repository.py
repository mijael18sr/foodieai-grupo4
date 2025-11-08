"""
CSV Review Repository Implementation
Implementación del repositorio de reseñas usando archivos CSV.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.domain.repositories import ReviewRepository
from src.domain.entities import Review, Sentiment


class CSVReviewRepository(ReviewRepository):
    """
    Implementación del repositorio de reseñas usando CSV.
    Adaptador para la capa de infraestructura.
    """

    def __init__(self, csv_path: str = 'data/processed/modelo_limpio.csv'):
        """
        Inicializar repositorio CSV.

        Args:
            csv_path: Ruta al archivo CSV con las reseñas
        """
        self.csv_path = Path(csv_path)
        self._df: Optional[pd.DataFrame] = None
        self._load_data()

    def _load_data(self) -> None:
        """Cargar datos desde el archivo CSV"""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Archivo de reseñas no encontrado: {self.csv_path}")

        try:
            self._df = pd.read_csv(self.csv_path)

            # Validar columnas requeridas
            required_cols = ['id_review', 'id_place', 'rating']
            missing_cols = [col for col in required_cols if col not in self._df.columns]

            if missing_cols:
                raise ValueError(f"Columnas faltantes en CSV: {missing_cols}")

            # La columna de texto puede ser 'comment', 'caption' o 'text'
            if 'comment' in self._df.columns:
                self.text_column = 'comment'
            elif 'caption' in self._df.columns:
                self.text_column = 'caption'
            else:
                raise ValueError("No se encontró columna de texto (comment/caption)")

            # Columna de username puede tener diferentes nombres
            if 'username' not in self._df.columns and 'user' in self._df.columns:
                self._df['username'] = self._df['user']

            # Agregar username vacío si no existe
            if 'username' not in self._df.columns:
                self._df['username'] = 'Usuario Anónimo'

            # Convertir fechas
            if 'review_date' in self._df.columns:
                self._df['review_date'] = pd.to_datetime(self._df['review_date'], errors='coerce')

            print(f" Reseñas cargadas: {len(self._df):,} registros desde {self.csv_path}")
            print(f" - Columna de texto: '{self.text_column}'")

        except Exception as e:
            raise Exception(f"Error cargando reseñas desde CSV: {e}")

    def _row_to_entity(self, row: pd.Series) -> Review:
        """
        Convertir una fila del DataFrame a entidad Review.

        Args:
            row: Fila del DataFrame

        Returns:
            Entidad Review
        """
        # Convertir sentimiento a enum si existe
        sentiment = None
        if 'sentimiento' in row and pd.notna(row['sentimiento']):
            sentiment_str = str(row['sentimiento']).lower()
            if sentiment_str in ['positivo', 'neutro', 'negativo']:
                sentiment = Sentiment(sentiment_str)

        # Extraer probabilidades si existen
        sentiment_probs = None
        if all(col in row for col in ['prob_positivo', 'prob_neutro', 'prob_negativo']):
            sentiment_probs = {
                'positivo': float(row['prob_positivo']) if pd.notna(row['prob_positivo']) else None,
                'neutro': float(row['prob_neutro']) if pd.notna(row['prob_neutro']) else None,
                'negativo': float(row['prob_negativo']) if pd.notna(row['prob_negativo']) else None
            }

        # Calcular confianza si existen probabilidades
        sentiment_confidence = None

        if sentiment_probs and any(v is not None for v in sentiment_probs.values()):
            sentiment_confidence = max(v for v in sentiment_probs.values() if v is not None)

        # Obtener el texto del comentario (puede ser 'caption' o 'comment')
        comment_text = str(row.get(self.text_column, row.get('comment', '')))

        return Review(
            id=str(row['id_review']),
            id_place=str(row['id_place']),
            comment=comment_text,
            rating=int(row['rating']),
            username=str(row['username']),
            review_date=row.get('review_date', datetime.now()),
            sentiment=sentiment,
            sentiment_confidence=sentiment_confidence,
            sentiment_probabilities=sentiment_probs,
            processed_comment=row.get('comment_processed', None)
        )

    def find_by_id(self, review_id: str) -> Optional[Review]:
        """Buscar reseña por ID"""
        result = self._df[self._df['id_review'] == review_id]
        if result.empty:
            return None
        return self._row_to_entity(result.iloc[0])

    def find_by_restaurant(self, restaurant_id: str) -> List[Review]:
        """Buscar todas las reseñas de un restaurante"""
        results = self._df[self._df['id_place'] == restaurant_id]
        return [self._row_to_entity(row) for _, row in results.iterrows()]

    def find_by_sentiment(self, sentiment: str) -> List[Review]:
        """Buscar reseñas por sentimiento"""
        if 'sentimiento' not in self._df.columns:
            return []

        results = self._df[self._df['sentimiento'].str.lower() == sentiment.lower()]
        return [self._row_to_entity(row) for _, row in results.iterrows()]

    def find_all(self, limit: Optional[int] = None) -> List[Review]:
        """Obtener todas las reseñas"""
        df_subset = self._df.head(limit) if limit else self._df
        return [self._row_to_entity(row) for _, row in df_subset.iterrows()]

    def save(self, review: Review) -> Review:
        """
        Guardar una reseña (agregar o actualizar).

        Nota: Esta implementación guarda en memoria. Para persistir,
        se debe llamar a save_to_csv().
        """
        # Convertir entidad a diccionario
        review_dict = {
            'id_review': review.id,
            'id_place': review.id_place,
            self.text_column: review.comment,
            'rating': review.rating,
            'username': review.username,
            'review_date': review.review_date,
            'sentiment': review.sentiment.value if review.sentiment else None,
            'sentiment_confidence': review.sentiment_confidence,
            'comment_processed': review.processed_comment
        }

        # Agregar probabilidades si existen
        if review.sentiment_probabilities:
            review_dict.update({
                'prob_positivo': review.sentiment_probabilities.get('positivo'),
                'prob_neutro': review.sentiment_probabilities.get('neutro'),
                'prob_negativo': review.sentiment_probabilities.get('negativo')
            })

        # Verificar si existe
        existing_idx = self._df[self._df['id_review'] == review.id].index

        if not existing_idx.empty:
            # Actualizar
            for col, val in review_dict.items():
                if col in self._df.columns:
                    self._df.loc[existing_idx[0], col] = val
        else:
            # Agregar nueva fila
            new_row = pd.DataFrame([review_dict])
            self._df = pd.concat([self._df, new_row], ignore_index=True)

        return review

    def save_to_csv(self, output_path: Optional[str] = None) -> None:
        """
        Guardar DataFrame actual a CSV.

        Args:
            output_path: Ruta de salida (si es None, usa la ruta original)
        """
        path = Path(output_path) if output_path else self.csv_path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._df.to_csv(path, index=False)
        print(f" Reseñas guardadas en: {path}")

    def count_by_restaurant(self, restaurant_id: str) -> int:
        """Contar reseñas de un restaurante"""
        return len(self._df[self._df['id_place'] == restaurant_id])

    def get_sentiment_stats(self, restaurant_id: str) -> dict:
        """Obtener estadísticas de sentimientos para un restaurante"""
        if 'sentimiento' not in self._df.columns:
            return {
                'total': 0,
                'sentiments': {},
                'percentages': {}
            }

        reviews = self._df[self._df['id_place'] == restaurant_id]
        total = len(reviews)

        if total == 0:
            return {
                'total': 0,
                'sentiments': {},
                'percentages': {}
            }

        # Contar por sentimiento
        sentiment_counts = reviews['sentimiento'].value_counts().to_dict()

        # Calcular porcentajes
        sentiment_percentages = {
            k: (v / total) * 100
            for k, v in sentiment_counts.items()
        }

        # Confianza promedio si existe
        avg_confidence = None
        confidence_col = None

        # Buscar columna de confianza (puede tener diferentes nombres)
        for col in ['sentiment_confidence', 'sentimiento_confidence', 'confidence']:
            if col in reviews.columns:
                confidence_col = col
                break

        if confidence_col:
            avg_confidence = reviews[confidence_col].mean()

        return {
            'total': total,
            'sentiments': sentiment_counts,
            'percentages': sentiment_percentages,
            'avg_confidence': float(avg_confidence) if pd.notna(avg_confidence) else None
        }

    def reload(self) -> None:
        """Recargar datos desde el archivo CSV"""
        self._load_data()

