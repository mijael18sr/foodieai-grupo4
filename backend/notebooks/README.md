# Analisis Exploratorio de Datos (EDA)

Este notebook contiene el analisis completo del dataset de restaurantes de Lima.

## Contenido

### 1. Carga de Datos
- Importacion de 4 datasets procesados
- 706 restaurantes de alta calidad
- 378,969 reviews individuales

### 2. Estadisticas Descriptivas
- Resumen ejecutivo de metricas clave
- Distribucion de variables numericas

### 3. Analisis de Distribuciones
- **Visualizacion 1**: Distribucion de Ratings (histograma, boxplot, KDE)
- **Visualizacion 2**: Distribucion de Reviews (escala normal y logaritmica)

### 4. Analisis Bivariado
- **Visualizacion 3**: Correlacion Reviews vs Rating (scatter + hexbin)
- **Visualizacion 4**: Matriz de correlacion (heatmap)

### 5. Analisis por Categorias
- Top 15 categorias de restaurantes
- Ratings promedio por categoria
- Estadisticas detalladas por categoria

### 6. Analisis Geoespacial
- **Visualizacion 5**: Mapa de calor de restaurantes en Lima
- Distribucion por distritos (Top 20)
- Relacion distancia-rating

### 7. Top Restaurantes
- Top 20 restaurantes por popularity score
- Visualizacion de Top 15

### 8. Analisis de Tiers
- Distribucion por quality tier
- Distribucion por review tier

### 9. Conclusiones
- 8 insights principales del analisis
- Recomendaciones para modelado ML

### 10. Exportacion
- Resumen ejecutivo en texto
- Todas las figuras guardadas en `docs/figures/`

## Como Ejecutar

### Opcion 1: Jupyter Notebook
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### Opcion 2: VS Code
1. Abrir el archivo `.ipynb`
2. Seleccionar kernel de Python
3. Ejecutar todas las celdas (Ctrl+Shift+P → "Run All")

### Opcion 3: Ejecutar como script Python
```bash
python -m jupyter nbconvert --to script notebooks/01_exploratory_data_analysis.ipynb
python notebooks/01_exploratory_data_analysis.py
```

## Archivos Generados

Despues de ejecutar el notebook, se crearan:

```
docs/
├── figures/
│   ├── distribucion_ratings.png
│   ├── distribucion_reviews.png
│   ├── correlacion_reviews_rating.png
│   ├── matriz_correlacion.png
│   ├── categorias_restaurantes.png
│   ├── ratings_por_categoria.png
│   ├── distritos_restaurantes.png
│   ├── mapa_geoespacial.png
│   ├── distancia_vs_rating.png
│   ├── top_restaurantes.png
│   └── distribucion_tiers.png
└── eda_summary.txt
```

## Resultados Principales

### Metricas Clave
- **Rating promedio**: 4.34 estrellas
- **Reviews promedio**: 1,275 por restaurante
- **Popularity score**: 5.16 (escala compuesta)
- **Distritos cubiertos**: 31
- **Categorias**: 19

### Top 5 Restaurantes
1. **Panchita - Miraflores**: 4.6 estrellas (12,925 reviews) - Score: 6.55
2. **Siete Sopas Lince**: 4.3 estrellas (19,373 reviews) - Score: 6.53
3. **Mercado de Magdalena**: 4.2 estrellas (22,080 reviews) - Score: 6.52
4. **Siete Sopas Surquillo**: 4.4 estrellas (15,167 reviews) - Score: 6.49
5. **Punto Azul**: 4.6 estrellas (10,682 reviews) - Score: 6.47

### Insights Clave
- Correlacion debil entre popularidad y calidad (r=0.089)
- Distribucion long-tail en numero de reviews
- Concentracion en zonas urbanas centrales
- La categoria "Restaurante" domina con 31.2%

## Dependencias

```python
pandas >= 1.5.0
numpy >= 1.23.0
matplotlib >= 3.6.0
seaborn >= 0.12.0
```

## Notas

- El analisis usa el dataset `restaurantes_alta_calidad.csv` (filtrado por rating >= 4.0)
- Todas las visualizaciones estan en alta resolucion (300 DPI)
- El resumen ejecutivo se exporta automaticamente a `docs/eda_summary.txt`

## Referencias

- Dataset original: [Kaggle - Lima Restaurant Review](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)
- Notebook completo con codigo y visualizaciones

# 📓 Notebooks - Análisis y Experimentación

Este directorio contiene los Jupyter Notebooks para análisis exploratorio, entrenamiento de modelos y evaluación de resultados.

## 📋 Contenido

### 1. **01_exploratory_data_analysis.ipynb**
Análisis exploratorio de datos de restaurantes de Lima.

**Contenido:**
- Carga de 4 datasets procesados
- 706 restaurantes de alta calidad
- 378,969 reviews individuales
- Estadísticas descriptivas
- Análisis de distribuciones (ratings, reviews)
- Análisis bivariado (correlaciones)

---

### 2. **02_sentiment_analysis_eda.ipynb** 🆕
Análisis exploratorio de reseñas para análisis de sentimientos.

**Contenido:**
- Exploración del dataset de ~200K reseñas
- Análisis de valores nulos y limpieza
- Distribución de sentimientos (positivo/neutro/negativo)
- Análisis de la variable objetivo
- Mapeo rating → sentimiento
- Análisis de longitud de comentarios
- Análisis de palabras frecuentes
- Nubes de palabras por sentimiento
- Análisis temporal (si aplica)
- Resumen estadístico final

**Output:** Dataset listo para entrenamiento

---

### 3. **03_sentiment_model_training.ipynb** 🆕
Entrenamiento del modelo de análisis de sentimientos con Redes Bayesianas.

**Contenido:**
- Preprocesamiento de texto (NLTK)
- Configuración de stopwords personalizadas
- División train/test estratificada
- Vectorización TF-IDF (unigramas + bigramas)
- Entrenamiento de modelos:
  - Multinomial Naive Bayes
  - Complement Naive Bayes ✅ (seleccionado)
- Comparación de modelos
- Optimización con GridSearchCV
- Análisis de features importantes
- Guardar modelo y metadatos

**Algoritmo Final:** Complement Naive Bayes (optimizado para datos desbalanceados)

**Métricas:**
- Accuracy: ~87%
- F1-Score Weighted: ~87%
- F1-Score Macro: ~70%

**Output:** 
- `sentiment_model_nb.pkl`
- `sentiment_vectorizer.pkl`
- `sentiment_model_metadata.pkl`
- Visualizaciones en `docs/figures/`

---

### 4. **04_sentiment_results_analysis.ipynb** 🆕
Análisis profundo de los resultados del modelo entrenado.

**Contenido:**
- Cargar modelo entrenado y generar predicciones
- Análisis de errores por clase
- Análisis de confianza de predicciones
- Predicciones con baja confianza
- Errores con alta confianza (modelo confiado pero equivocado)
- Análisis por longitud de comentario
- Palabras clave en errores
- Casos límite y ambiguos
- Recomendaciones automáticas de mejora
- Resumen ejecutivo

**Hallazgos Principales:**
- ✅ Excelente rendimiento en sentimientos **positivos** (~90% precision)
- ⚠️ Menor rendimiento en clase **neutro** (datos minoritarios)
- ⚠️ Confusión entre neutro-positivo y neutro-negativo
- ✅ Alta confianza en predicciones correctas

**Recomendaciones:**
- Aplicar balanceo de clases (SMOTE, oversampling)
- Considerar modelos avanzados (BERT) para casos ambiguos
- Análisis manual de errores con alta confianza

---

## 🚀 Orden de Ejecución Recomendado

Para el **análisis de sentimientos**, ejecuta los notebooks en este orden:

```bash
1. 02_sentiment_analysis_eda.ipynb        # Exploración de datos
2. 03_sentiment_model_training.ipynb      # Entrenamiento del modelo
3. 04_sentiment_results_analysis.ipynb    # Análisis de resultados
```

## 🔧 Configuración

### Dependencias Necesarias

```bash
pip install pandas numpy matplotlib seaborn
pip install scikit-learn joblib
pip install nltk wordcloud
```

### Descargar Recursos NLTK

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 📊 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────┐
│                  NOTEBOOKS (Experimentación)                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  02_sentiment_analysis_eda.ipynb                            │
│       ↓                                                      │
│  Exploración y limpieza de datos                            │
│       ↓                                                      │
│  03_sentiment_model_training.ipynb                          │
│       ↓                                                      │
│  Entrenamiento y optimización                               │
│       ↓                                                      │
│  04_sentiment_results_analysis.ipynb                        │
│       ↓                                                      │
│  Evaluación y recomendaciones                               │
│       ↓                                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              CÓDIGO DE PRODUCCIÓN (Clean Architecture)       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  src/ml/models/sentiment_model.py                           │
│  src/application/services/sentiment_service.py              │
│  src/presentation/api/routes/sentiment.py                   │
│                                                              │
│  Scripts:                                                    │
│  - scripts/train_sentiment_analysis.py                      │
│  - scripts/test_sentiment_integration.py                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 💡 Buenas Prácticas

### En Notebooks (Experimentación):
- ✅ Explorar y visualizar datos libremente
- ✅ Probar múltiples algoritmos y parámetros
- ✅ Documentar hallazgos y decisiones
- ✅ Mantener código comentado y explicado

### En Código de Producción:
- ✅ Código limpio y modular (Clean Architecture)
- ✅ Separación de responsabilidades (SOLID)
- ✅ Tests automatizados
- ✅ Manejo de errores robusto
- ✅ Logging y monitoreo

## 📚 Referencias

- **Scikit-learn**: https://scikit-learn.org/
- **NLTK**: https://www.nltk.org/
- **Naive Bayes para NLP**: [Rennie et al. (2003)](https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf)
- **Clean Architecture**: Robert C. Martin

---

**Nota**: Los notebooks son para **experimentación y análisis**. El código de producción está en `src/` siguiendo Clean Architecture.
