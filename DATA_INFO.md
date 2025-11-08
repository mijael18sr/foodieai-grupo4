# Información sobre Archivos de Datos

## Archivos Grandes (Excluidos del Repositorio)

Debido a las limitaciones de tamaño de GitHub (100MB), los siguientes archivos de datos están excluidos y deben descargarse por separado:

### Archivos RAW
- `Lima_Restaurants_2025_08_13.csv` (131.51 MB)
- `Lima_Restaurants_2025_08_13_clean.csv` (1,131.74 MB)

### Archivos Procesados
- `modelo_limpio.csv` (51.93 MB) 
- `reviews_con_sentimiento.csv` (1,382.27 MB)

## Archivos Incluidos

### Datos de Restaurantes
- `restaurant_metadata.csv` (0.29 MB) - Metadatos de restaurantes
- `restaurantes_alta_calidad.csv` (0.25 MB) - Restaurantes filtrados
- `restaurantes_limpio.csv` (0.31 MB) - Restaurantes procesados
- `restaurantes_sin_anomalias.csv` (0.34 MB) - Datos sin anomalías

### Datos de Reviews
- `reviews_limpio.csv` (43.96 MB) - Reviews procesadas
- `word_frequency_stats.csv` (0.00 MB) - Estadísticas de frecuencia

### Modelos ML
- `clustering_model.pkl` (0.01 MB) - Modelo de clustering
- `rating_predictor.pkl` (2.54 MB) - Predictor de ratings
- `recommender_system.pkl` (0.00 MB) - Sistema de recomendación
- `sentiment_model.pkl` (1.71 MB) - Modelo de sentimientos

## Instrucciones de Configuración

1. **Clona el repositorio:**
 ```bash
 git clone https://github.com/mijael18sr/foodieai-grupo4.git
 cd restaurant-recommender-ml
 ```

2. **Configura el Backend:**
 ```bash
 cd backend
 python -m venv .venv
 .venv\Scripts\activate
 pip install -r requirements.txt
 python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
 python start_server.py
 ```

3. **Configura el Frontend:**
 ```bash
 cd ../frontend
 npm install
 npm run dev
 ```

4. **Accede a la aplicación:**
 - Frontend: http://localhost:5173
 - Backend API: http://localhost:8000/docs
 - Health Check: http://localhost:8000/api/v1/health

## Notas Importantes

- Los archivos grandes están excluidos del repositorio por límites de GitHub (100MB)
- Los modelos incluidos están pre-entrenados y listos para usar
- **NO es necesario descargar archivos adicionales** para funcionamiento básico
- Para re-entrenar: ejecuta `python reentrenar_modelo_limpio.py`
- Para datos completos: contacta al equipo de desarrollo