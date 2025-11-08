# 📊 Información sobre Archivos de Datos

## ⚠️ Archivos Grandes (Excluidos del Repositorio)

Debido a las limitaciones de tamaño de GitHub (100MB), los siguientes archivos de datos están excluidos y deben descargarse por separado:

### 🗂️ Archivos RAW
- `Lima_Restaurants_2025_08_13.csv` (131.51 MB)
- `Lima_Restaurants_2025_08_13_clean.csv` (1,131.74 MB)

### 📈 Archivos Procesados
- `modelo_limpio.csv` (51.93 MB) 
- `reviews_con_sentimiento.csv` (1,382.27 MB)

## ✅ Archivos Incluidos

### 🏪 Datos de Restaurantes
- `restaurant_metadata.csv` (0.29 MB) - Metadatos de restaurantes
- `restaurantes_alta_calidad.csv` (0.25 MB) - Restaurantes filtrados
- `restaurantes_limpio.csv` (0.31 MB) - Restaurantes procesados
- `restaurantes_sin_anomalias.csv` (0.34 MB) - Datos sin anomalías

### 📝 Datos de Reviews
- `reviews_limpio.csv` (43.96 MB) - Reviews procesadas
- `word_frequency_stats.csv` (0.00 MB) - Estadísticas de frecuencia

### 🤖 Modelos ML
- `clustering_model.pkl` (0.01 MB) - Modelo de clustering
- `rating_predictor.pkl` (2.54 MB) - Predictor de ratings
- `recommender_system.pkl` (0.00 MB) - Sistema de recomendación
- `sentiment_model.pkl` (1.71 MB) - Modelo de sentimientos

## 🚀 Instrucciones de Configuración

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/mijael18sr/foodieai-grupo4.git
   cd restaurant-recommender-ml
   ```

2. **Descarga los archivos grandes** desde [enlace a Drive/alternativo]

3. **Coloca los archivos en:**
   - `backend/data/raw/` - Archivos CSV grandes
   - `backend/data/processed/` - Archivos procesados grandes

4. **Instala dependencias:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend  
   cd ../frontend
   npm install
   ```

5. **Ejecuta el proyecto:**
   ```bash
   # Terminal 1: Backend
   cd backend && python start_server.py
   
   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

## 📝 Notas

- Los archivos grandes se regeneran automáticamente durante el entrenamiento
- Los modelos incluidos están pre-entrenados y listos para usar
- Para re-entrenar: ejecuta `python reentrenar_modelo_limpio.py`