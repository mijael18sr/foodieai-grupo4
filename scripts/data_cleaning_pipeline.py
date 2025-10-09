"""
Pipeline de Limpieza de Datos - Sistema de Recomendación de Restaurantes
Genera datasets procesados en 2 fases:
FASE 1: Limpieza de metadatos de restaurantes
FASE 2: Limpieza de reviews individuales con análisis de sentimiento
"""
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
import re
from typing import Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataCleaningPipeline:
    """Pipeline completo de limpieza de datos"""

    def __init__(self, raw_path: Path, processed_path: Path):
        self.raw_path = raw_path
        self.processed_path = processed_path
        self.processed_path.mkdir(parents=True, exist_ok=True)

    # ==================== FASE 1: RESTAURANTES ====================

    def fase1_limpieza_basica(self) -> pd.DataFrame:
        """
        FASE 1.1: Limpieza básica de restaurantes
        Output: restaurantes_limpio.csv
        """
        logger.info("=" * 70)
        logger.info("FASE 1.1: LIMPIEZA BÁSICA DE RESTAURANTES")
        logger.info("=" * 70)

        # Cargar datos
        df = pd.read_csv(self.raw_path / 'restaurant_metadata.csv')
        logger.info(f"📂 Datos cargados: {df.shape[0]} restaurantes")

        # 1. Eliminar duplicados
        initial_count = len(df)
        df = df.drop_duplicates(subset=['id_place'])
        logger.info(f"✅ Duplicados eliminados: {initial_count - len(df)}")

        # 2. Renombrar columnas para consistencia
        df.rename(columns={
            'phoneNumber': 'phone_number',
            'completePhoneNumber': 'complete_phone_number'
        }, inplace=True)

        # 3. Normalizar texto
        df['title'] = df['title'].str.strip()
        df['category'] = df['category'].str.strip()
        df['district'] = df['district'].str.strip()
        df['address'] = df['address'].str.strip()

        # 4. Limpiar categorías (extraer tipo principal)
        df['category_clean'] = df['category'].apply(self._extract_main_category)

        # 5. Manejar valores faltantes
        df['reviews'] = df['reviews'].fillna(0).astype(int)
        df['stars'] = df['stars'].fillna(df['stars'].median())

        # Campos de texto opcionales
        text_fields = ['phone_number', 'complete_phone_number', 'domain', 'url']
        for field in text_fields:
            if field in df.columns:
                df[field] = df[field].fillna('No disponible')

        # 6. Validar rangos numéricos
        df = df[(df['stars'] >= 0) & (df['stars'] <= 5)]
        df = df[df['reviews'] >= 0]

        # 7. Validar coordenadas (Lima: lat -13 a -11, long -78 a -76)
        df = df[
            (df['lat'].between(-13, -11)) &
            (df['long'].between(-78, -76))
        ]

        # 8. Crear identificador único numérico
        df.insert(0, 'restaurant_id', range(1, len(df) + 1))

        logger.info(f"✅ Registros finales: {len(df)}")
        logger.info(f"✅ Columnas: {df.shape[1]}")

        # Guardar
        output_file = self.processed_path / 'restaurantes_limpio.csv'
        df.to_csv(output_file, index=False)
        logger.info(f"💾 Guardado: {output_file}")

        return df

    def fase1_deteccion_anomalias(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        FASE 1.2: Detección y eliminación de anomalías
        Output: restaurantes_sin_anomalias.csv
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 1.2: DETECCIÓN Y ELIMINACIÓN DE ANOMALÍAS")
        logger.info("=" * 70)

        initial_count = len(df)

        # 1. Detectar outliers en reviews usando IQR
        Q1_reviews = df['reviews'].quantile(0.25)
        Q3_reviews = df['reviews'].quantile(0.75)
        IQR_reviews = Q3_reviews - Q1_reviews
        upper_bound_reviews = Q3_reviews + 3 * IQR_reviews  # Factor 3 (menos estricto)

        outliers_reviews = df[df['reviews'] > upper_bound_reviews]
        logger.info(f"⚠️  Outliers detectados (reviews > {upper_bound_reviews:.0f}): {len(outliers_reviews)}")

        # NO eliminar outliers de reviews, solo marcar
        df['is_high_volume'] = df['reviews'] > upper_bound_reviews

        # 2. Detectar anomalías en ratings
        # Ratings muy bajos con muchas reviews (posible problema)
        anomaly_low_rating = (df['stars'] < 3.0) & (df['reviews'] > 100)
        logger.info(f"⚠️  Anomalías (rating bajo + muchas reviews): {anomaly_low_rating.sum()}")

        # 3. Detectar coordenadas sospechosas (muy lejos del centro de Lima)
        center_lat, center_long = -12.0464, -77.0428
        df['distance_to_center_km'] = np.sqrt(
            (df['lat'] - center_lat)**2 +
            (df['long'] - center_long)**2
        ) * 111

        # Eliminar restaurantes a más de 30km del centro (probablemente error)
        anomaly_location = df['distance_to_center_km'] > 30
        logger.info(f"⚠️  Anomalías de ubicación (>30km centro): {anomaly_location.sum()}")

        # 4. Detectar títulos sospechosos
        df['title_length'] = df['title'].str.len()
        anomaly_title = (df['title_length'] < 3) | (df['title_length'] > 100)
        logger.info(f"⚠️  Anomalías en título: {anomaly_title.sum()}")

        # 5. Eliminar anomalías críticas (solo ubicación y título)
        df_clean = df[~(anomaly_location | anomaly_title)].copy()

        # Marcar otras anomalías sin eliminar
        df_clean['has_anomaly'] = anomaly_low_rating.loc[df_clean.index]

        removed = initial_count - len(df_clean)
        logger.info(f"❌ Registros eliminados: {removed}")
        logger.info(f"✅ Registros restantes: {len(df_clean)}")

        # Guardar
        output_file = self.processed_path / 'restaurantes_sin_anomalias.csv'
        df_clean.to_csv(output_file, index=False)
        logger.info(f"💾 Guardado: {output_file}")

        return df_clean

    def fase1_filtro_alta_calidad(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        FASE 1.3: Filtro de restaurantes de alta calidad
        Output: restaurantes_alta_calidad.csv
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 1.3: FILTRO DE ALTA CALIDAD")
        logger.info("=" * 70)

        initial_count = len(df)

        # Criterios de alta calidad:
        # 1. Rating >= 4.0 (buena calidad)
        # 2. Al menos 50 reviews (confiabilidad estadística)
        # 3. Sin anomalías críticas

        high_quality = (
            (df['stars'] >= 4.0) &
            (df['reviews'] >= 50) &
            (~df['has_anomaly'])
        )

        df_quality = df[high_quality].copy()

        # Calcular métricas adicionales
        df_quality['popularity_score'] = (
            df_quality['stars'] * 0.6 +
            np.log1p(df_quality['reviews']) * 0.4
        ).round(2)

        df_quality['quality_tier'] = pd.cut(
            df_quality['stars'],
            bins=[0, 4.0, 4.5, 5.0],
            labels=['Bueno', 'Muy Bueno', 'Excelente']
        )

        df_quality['review_tier'] = pd.cut(
            df_quality['reviews'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Bajo', 'Medio', 'Alto', 'Muy Alto']
        )

        # Estadísticas
        logger.info(f"✅ Restaurantes de alta calidad: {len(df_quality)} ({len(df_quality)/initial_count*100:.1f}%)")
        logger.info(f"📊 Rating promedio: {df_quality['stars'].mean():.2f}")
        logger.info(f"📊 Reviews promedio: {df_quality['reviews'].mean():.0f}")
        logger.info(f"📊 Popularity score promedio: {df_quality['popularity_score'].mean():.2f}")

        # Top 5 restaurantes
        logger.info("\n🏆 TOP 5 RESTAURANTES:")
        top5 = df_quality.nlargest(5, 'popularity_score')[
            ['title', 'category_clean', 'stars', 'reviews', 'popularity_score']
        ]
        for idx, row in top5.iterrows():
            logger.info(f"   {row['title']}: ⭐{row['stars']} ({row['reviews']} reviews) - Score: {row['popularity_score']}")

        # Guardar
        output_file = self.processed_path / 'restaurantes_alta_calidad.csv'
        df_quality.to_csv(output_file, index=False)
        logger.info(f"\n💾 Guardado: {output_file}")

        return df_quality

    # ==================== FASE 2: REVIEWS ====================

    def fase2_limpieza_reviews(self) -> pd.DataFrame:
        """
        FASE 2.1: Limpieza de reviews individuales
        Output: reviews_limpio.csv
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 2.1: LIMPIEZA DE REVIEWS INDIVIDUALES")
        logger.info("=" * 70)

        # Cargar reviews
        reviews_file = self.raw_path / 'Lima_Restaurants_2025_08_13.csv'

        if not reviews_file.exists():
            logger.warning(f"⚠️  Archivo de reviews no encontrado: {reviews_file}")
            logger.info("Creando dataset de reviews sintético...")
            return self._create_synthetic_reviews()

        try:
            # Intentar cargar el archivo completo
            logger.info(f"📂 Cargando reviews desde: {reviews_file}")
            df_reviews = pd.read_csv(reviews_file)
            logger.info(f"✅ Reviews cargadas: {len(df_reviews)}")
        except Exception as e:
            logger.warning(f"⚠️  Error cargando reviews completas: {e}")
            logger.info("Cargando muestra de 50,000 reviews...")
            df_reviews = pd.read_csv(reviews_file, nrows=50000)
            logger.info(f"✅ Reviews cargadas (muestra): {len(df_reviews)}")

        initial_count = len(df_reviews)

        # Inspeccionar columnas
        logger.info(f"📋 Columnas disponibles: {df_reviews.columns.tolist()}")

        # Adaptar según estructura real del archivo
        # Asumiendo estructura típica: id_place, reviewer, rating, text, date

        # 1. Eliminar duplicados
        if 'id_place' in df_reviews.columns:
            df_reviews = df_reviews.drop_duplicates()

        # 2. Limpiar texto de reviews
        if 'text' in df_reviews.columns or 'review' in df_reviews.columns:
            text_col = 'text' if 'text' in df_reviews.columns else 'review'
            df_reviews[text_col] = df_reviews[text_col].fillna('')
            df_reviews[text_col] = df_reviews[text_col].astype(str).str.strip()
            df_reviews['review_length'] = df_reviews[text_col].str.len()

            # Eliminar reviews vacías o muy cortas
            df_reviews = df_reviews[df_reviews['review_length'] >= 10]

        # 3. Validar ratings
        if 'rating' in df_reviews.columns or 'stars' in df_reviews.columns:
            rating_col = 'rating' if 'rating' in df_reviews.columns else 'stars'
            df_reviews = df_reviews[
                (df_reviews[rating_col] >= 1) &
                (df_reviews[rating_col] <= 5)
            ]

        # 4. Crear ID único
        df_reviews.insert(0, 'review_id', range(1, len(df_reviews) + 1))

        logger.info(f"❌ Reviews eliminadas: {initial_count - len(df_reviews)}")
        logger.info(f"✅ Reviews limpias: {len(df_reviews)}")

        # Guardar
        output_file = self.processed_path / 'reviews_limpio.csv'
        df_reviews.to_csv(output_file, index=False)
        logger.info(f"💾 Guardado: {output_file}")

        return df_reviews

    def fase2_analisis_sentimiento(self, df_reviews: pd.DataFrame) -> pd.DataFrame:
        """
        FASE 2.2: Análisis de sentimiento en reviews
        Output: reviews_con_sentimiento.csv
        """
        logger.info("\n" + "=" * 70)
        logger.info("FASE 2.2: ANÁLISIS DE SENTIMIENTO")
        logger.info("=" * 70)

        # Identificar columna de texto
        text_col = None
        for col in ['text', 'review', 'comment', 'description']:
            if col in df_reviews.columns:
                text_col = col
                break

        if text_col is None:
            logger.warning("⚠️  No se encontró columna de texto para análisis de sentimiento")
            df_reviews['sentiment'] = 'neutral'
            df_reviews['sentiment_score'] = 0.0
        else:
            logger.info(f"📝 Analizando columna: {text_col}")

            # Análisis de sentimiento basado en palabras clave (método simple)
            df_reviews['sentiment_score'] = df_reviews[text_col].apply(
                self._calculate_sentiment_score
            )

            # Clasificar sentimiento
            df_reviews['sentiment'] = pd.cut(
                df_reviews['sentiment_score'],
                bins=[-float('inf'), -0.3, 0.3, float('inf')],
                labels=['negativo', 'neutral', 'positivo']
            )

        # Estadísticas
        sentiment_counts = df_reviews['sentiment'].value_counts()
        logger.info("\n📊 Distribución de Sentimientos:")
        for sentiment, count in sentiment_counts.items():
            pct = count / len(df_reviews) * 100
            logger.info(f"   {sentiment.capitalize()}: {count} ({pct:.1f}%)")

        logger.info(f"\n📊 Score promedio: {df_reviews['sentiment_score'].mean():.3f}")

        # Guardar
        output_file = self.processed_path / 'reviews_con_sentimiento.csv'
        df_reviews.to_csv(output_file, index=False)
        logger.info(f"\n💾 Guardado: {output_file}")

        return df_reviews

    # ==================== MÉTODOS AUXILIARES ====================

    def _extract_main_category(self, category: str) -> str:
        """Extrae la categoría principal de un texto"""
        if pd.isna(category):
            return 'Otro'

        category = category.lower()

        # Mapeo de categorías
        if 'peruano' in category or 'perú' in category:
            return 'Peruano'
        elif 'italiano' in category or 'pizza' in category:
            return 'Italiano'
        elif 'japonés' in category or 'sushi' in category:
            return 'Japonés'
        elif 'chino' in category or 'chifa' in category:
            return 'Chino'
        elif 'fusión' in category:
            return 'Fusión'
        elif 'alta cocina' in category or 'gourmet' in category:
            return 'Alta Cocina'
        elif 'bar' in category or 'pub' in category:
            return 'Bar/Pub'
        elif 'café' in category or 'cafetería' in category:
            return 'Cafetería'
        elif 'parrilla' in category or 'carne' in category or 'steak' in category:
            return 'Parrilla'
        elif 'venezolano' in category:
            return 'Venezolano'
        elif 'mexicano' in category:
            return 'Mexicano'
        elif 'vasco' in category:
            return 'Vasco'
        elif 'restaurante' in category:
            return 'Restaurante'
        else:
            return 'Otro'

    def _calculate_sentiment_score(self, text: str) -> float:
        """
        Calcula un score de sentimiento simple basado en palabras clave
        Rango: -1 (muy negativo) a +1 (muy positivo)
        """
        if pd.isna(text) or not isinstance(text, str):
            return 0.0

        text = text.lower()

        # Palabras positivas
        positive_words = [
            'excelente', 'bueno', 'buena', 'rico', 'delicioso', 'recomendado',
            'espectacular', 'increíble', 'perfecto', 'maravilloso', 'genial',
            'amor', 'encantó', 'fascinó', 'mejor', 'calidad', 'fresco'
        ]

        # Palabras negativas
        negative_words = [
            'malo', 'mala', 'pésimo', 'horrible', 'terrible', 'caro',
            'frío', 'crudo', 'desagradable', 'sucio', 'lento', 'demora',
            'nunca', 'peor', 'decepción', 'decepcionante'
        ]

        # Contar ocurrencias
        positive_count = sum(text.count(word) for word in positive_words)
        negative_count = sum(text.count(word) for word in negative_words)

        # Calcular score normalizado
        total = positive_count + negative_count
        if total == 0:
            return 0.0

        score = (positive_count - negative_count) / total
        return round(score, 3)

    def _create_synthetic_reviews(self) -> pd.DataFrame:
        """Crea un dataset sintético de reviews si no existe el archivo real"""
        logger.info("Generando 1000 reviews sintéticas...")

        # Cargar restaurantes para obtener IDs
        df_restaurants = pd.read_csv(self.processed_path / 'restaurantes_limpio.csv')

        np.random.seed(42)

        reviews_data = []
        for i in range(1, 1001):
            restaurant_id = np.random.choice(df_restaurants['restaurant_id'])
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.05, 0.15, 0.35, 0.40])

            # Textos de ejemplo
            if rating >= 4:
                text = np.random.choice([
                    "Excelente restaurante, la comida es deliciosa y el servicio muy bueno.",
                    "Muy recomendado, platos frescos y bien preparados.",
                    "Me encantó la experiencia, volveré sin duda."
                ])
            elif rating == 3:
                text = "Bien en general, pero tiene aspectos a mejorar."
            else:
                text = "No fue una buena experiencia, esperaba más."

            reviews_data.append({
                'review_id': i,
                'restaurant_id': restaurant_id,
                'rating': rating,
                'text': text,
                'date': f"2025-0{np.random.randint(1, 9)}-{np.random.randint(1, 28):02d}"
            })

        df_reviews = pd.DataFrame(reviews_data)

        # Guardar
        output_file = self.processed_path / 'reviews_limpio.csv'
        df_reviews.to_csv(output_file, index=False)
        logger.info(f"💾 Guardado: {output_file}")

        return df_reviews

    # ==================== PIPELINE PRINCIPAL ====================

    def run_full_pipeline(self):
        """Ejecuta el pipeline completo de limpieza"""
        logger.info("\n" + "🚀" * 35)
        logger.info("INICIANDO PIPELINE DE LIMPIEZA DE DATOS")
        logger.info("🚀" * 35 + "\n")

        # FASE 1: Restaurantes
        df_limpio = self.fase1_limpieza_basica()
        df_sin_anomalias = self.fase1_deteccion_anomalias(df_limpio)
        df_alta_calidad = self.fase1_filtro_alta_calidad(df_sin_anomalias)

        # FASE 2: Reviews
        df_reviews_limpio = self.fase2_limpieza_reviews()
        df_reviews_sentimiento = self.fase2_analisis_sentimiento(df_reviews_limpio)

        # Resumen final
        logger.info("\n" + "=" * 70)
        logger.info("✅ PIPELINE COMPLETADO")
        logger.info("=" * 70)
        logger.info("\n📁 Archivos generados:")
        logger.info(f"   1. restaurantes_limpio.csv ({len(df_limpio)} registros)")
        logger.info(f"   2. restaurantes_sin_anomalias.csv ({len(df_sin_anomalias)} registros)")
        logger.info(f"   3. restaurantes_alta_calidad.csv ({len(df_alta_calidad)} registros)")
        logger.info(f"   4. reviews_limpio.csv ({len(df_reviews_limpio)} registros)")
        logger.info(f"   5. reviews_con_sentimiento.csv ({len(df_reviews_sentimiento)} registros)")
        logger.info(f"\n📂 Ubicación: {self.processed_path}")
        logger.info("\n" + "🎉" * 35)


def main():
    """Función principal"""
    base_path = Path(__file__).parent.parent
    raw_path = base_path / 'data' / 'raw'
    processed_path = base_path / 'data' / 'processed'

    # Ejecutar pipeline
    pipeline = DataCleaningPipeline(raw_path, processed_path)
    pipeline.run_full_pipeline()


if __name__ == '__main__':
    main()

