# 🍽️ Sistema de Recomendación de Restaurantes - Lima

Sistema inteligente de recomendación de restaurantes usando Machine Learning con arquitectura enterprise en Python.

## 🎯 Características

- ✅ Recomendaciones personalizadas basadas en ubicación
- ✅ Predicción de ratings con Random Forest
- ✅ Clustering de restaurantes similares (K-Means)
- ✅ API REST con FastAPI
- ✅ Clean Architecture
- ✅ MLOps con MLflow
- ✅ Testing completo

## 📊 Dataset

**Fuente**: [Lima Restaurant Review - Kaggle](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)

## 🚀 Inicio Rápido
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar limpieza de datos
python scripts/run_data_wrangling.py

# Entrenar modelos
python scripts/train_models.py

# Iniciar API
uvicorn src.presentation.api.main:app --reload