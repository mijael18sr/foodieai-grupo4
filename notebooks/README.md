# 📊 Análisis Exploratorio de Datos (EDA)

Este notebook contiene el análisis completo del dataset de restaurantes de Lima.

## 🎯 Contenido

### 1. Carga de Datos
- Importación de 4 datasets procesados
- 706 restaurantes de alta calidad
- 378,969 reviews individuales

### 2. Estadísticas Descriptivas
- Resumen ejecutivo de métricas clave
- Distribución de variables numéricas

### 3. Análisis de Distribuciones
- **Visualización 1**: Distribución de Ratings (histograma, boxplot, KDE)
- **Visualización 2**: Distribución de Reviews (escala normal y logarítmica)

### 4. Análisis Bivariado
- **Visualización 3**: Correlación Reviews vs Rating (scatter + hexbin)
- **Visualización 4**: Matriz de correlación (heatmap)

### 5. Análisis por Categorías
- Top 15 categorías de restaurantes
- Ratings promedio por categoría
- Estadísticas detalladas por categoría

### 6. Análisis Geoespacial
- **Visualización 5**: Mapa de calor de restaurantes en Lima
- Distribución por distritos (Top 20)
- Relación distancia-rating

### 7. Top Restaurantes
- Top 20 restaurantes por popularity score
- Visualización de Top 15

### 8. Análisis de Tiers
- Distribución por quality tier
- Distribución por review tier

### 9. Conclusiones
- 8 insights principales del análisis
- Recomendaciones para modelado ML

### 10. Exportación
- Resumen ejecutivo en texto
- Todas las figuras guardadas en `docs/figures/`

## 🚀 Cómo Ejecutar

### Opción 1: Jupyter Notebook
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### Opción 2: VS Code
1. Abrir el archivo `.ipynb`
2. Seleccionar kernel de Python
3. Ejecutar todas las celdas (Ctrl+Shift+P → "Run All")

### Opción 3: Ejecutar como script Python
```bash
python -m jupyter nbconvert --to script notebooks/01_exploratory_data_analysis.ipynb
python notebooks/01_exploratory_data_analysis.py
```

## 📁 Archivos Generados

Después de ejecutar el notebook, se crearán:

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

## 📊 Resultados Principales

### Métricas Clave
- **Rating promedio**: 4.34 ⭐
- **Reviews promedio**: 1,275 por restaurante
- **Popularity score**: 5.16 (escala compuesta)
- **Distritos cubiertos**: 31
- **Categorías**: 19

### Top 5 Restaurantes
1. **Panchita - Miraflores**: 4.6⭐ (12,925 reviews) - Score: 6.55
2. **Siete Sopas Lince**: 4.3⭐ (19,373 reviews) - Score: 6.53
3. **Mercado de Magdalena**: 4.2⭐ (22,080 reviews) - Score: 6.52
4. **Siete Sopas Surquillo**: 4.4⭐ (15,167 reviews) - Score: 6.49
5. **Punto Azul**: 4.6⭐ (10,682 reviews) - Score: 6.47

### Insights Clave
✅ Correlación débil entre popularidad y calidad (r=0.089)
✅ Distribución long-tail en número de reviews
✅ Concentración en zonas urbanas centrales
✅ La categoría "Restaurante" domina con 31.2%

## 🔧 Dependencias

```python
pandas >= 1.5.0
numpy >= 1.23.0
matplotlib >= 3.6.0
seaborn >= 0.12.0
```

## 📝 Notas

- El análisis usa el dataset `restaurantes_alta_calidad.csv` (filtrado por rating ≥ 4.0)
- Todas las visualizaciones están en alta resolución (300 DPI)
- El resumen ejecutivo se exporta automáticamente a `docs/eda_summary.txt`

## 🔗 Referencias

- Dataset original: [Kaggle - Lima Restaurant Review](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)
- Notebook completo con código y visualizaciones

