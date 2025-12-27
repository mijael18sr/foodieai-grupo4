# 🍽️ FoodieAI Backend - API REST con Machine Learning

> Backend del Sistema de Recomendación de Restaurantes con análisis de sentimientos y ML.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)

## 📋 Contenido

- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Ejecución](#-ejecución)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelos ML](#-modelos-de-machine-learning)
- [Testing](#-testing)
- [Solución de Problemas](#-solución-de-problemas)

---

## 📦 Requisitos

| Requisito | Versión | Verificar |
|-----------|---------|-----------|
| Python | 3.10+ | `python --version` |
| pip | 21+ | `pip --version` |
| Espacio disco | 2GB | - |

---

## 🚀 Instalación

### Paso 1: Crear entorno virtual

```bash
cd backend

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 2: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 3: Descargar recursos NLTK

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Paso 4: Verificar instalación

```bash
python -c "import fastapi; import sklearn; import pandas; print('✅ Instalación correcta')"
```

---

## ▶️ Ejecución

### Modo Desarrollo (con auto-reload)

```bash
python start_server.py
```

### Modo Producción

```bash
uvicorn src.presentation.api.main:app --host 0.0.0.0 --port 8000
```

### Salida esperada

```
🚀 Iniciando Restaurant Recommender API...
📍 Backend URL: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
✅ Modo desarrollo con auto-reload activado
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### URLs disponibles

| Recurso | URL |
|---------|-----|
| API Base | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/api/v1/health |

---

## 📡 API Endpoints

### Health Check

```http
GET /api/v1/health
GET /api/v1/health/status
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "restaurant-recommender-api",
  "version": "2.0.0",
  "data": {
    "restaurants_loaded": 1052,
    "database_status": "connected"
  }
}
```

### Análisis de Sentimientos

```http
POST /api/v1/sentiment/analyze
Content-Type: application/json

{
  "comment": "La comida estuvo deliciosa y el servicio excelente"
}
```

**Respuesta:**
```json
{
  "comment": "La comida estuvo deliciosa y el servicio excelente",
  "sentiment": "positivo",
  "confidence": 0.94,
  "probabilities": {
    "positivo": 0.94,
    "neutro": 0.04,
    "negativo": 0.02
  }
}
```

### Recomendaciones de Restaurantes

```http
POST /api/v1/recommendations
Content-Type: application/json

{
  "user_location": {
    "lat": -12.1191,
    "long": -77.0311
  },
  "preferences": {
    "category": "Peruano"
  },
  "filters": {
    "min_rating": 4.0,
    "max_distance_km": 5,
    "district": "Miraflores"
  },
  "top_n": 10
}
```

### Obtener Categorías

```http
GET /api/v1/categories
```

### Obtener Distritos

```http
GET /api/v1/districts
```

---

## 📁 Estructura del Proyecto

```
backend/
├── data/
│   ├── models/                      # Modelos ML entrenados
│   │   ├── sentiment_model.pkl      # Modelo de sentimientos (84.36% accuracy)
│   │   ├── tfidf_vectorizer.pkl     # Vectorizador TF-IDF
│   │   └── backups/                 # Respaldos de modelos
│   ├── processed/                   # Datos procesados
│   │   ├── restaurantes_limpio.csv  # 1,052 restaurantes
│   │   └── reviews_limpio.csv       # 185,666 reseñas
│   └── raw/                         # Datos originales
│       └── Lima_Restaurants_*.csv
├── src/                             # Código fuente (Clean Architecture)
│   ├── application/                 # Capa de aplicación
│   │   ├── dto/                     # Data Transfer Objects
│   │   ├── services/                # Servicios de aplicación
│   │   └── use_cases/               # Casos de uso
│   ├── domain/                      # Capa de dominio
│   │   ├── entities/                # Entidades de negocio
│   │   └── repositories/            # Interfaces de repositorios
│   ├── infrastructure/              # Capa de infraestructura
│   │   ├── config/                  # Configuraciones
│   │   ├── ml/                      # Implementaciones ML
│   │   └── repositories/            # Implementaciones de repos
│   └── presentation/                # Capa de presentación
│       └── api/                     # REST API (FastAPI)
│           ├── main.py              # Aplicación principal
│           └── routers/             # Endpoints por dominio
├── notebooks/                       # Jupyter notebooks EDA
├── test/                            # Tests unitarios e integración
├── requirements.txt                 # Dependencias Python
├── start_server.py                  # Script de inicio
├── Dockerfile                       # Contenedor Docker
└── README.md                        # Este archivo
```

---

## 🤖 Modelos de Machine Learning

### 1. Análisis de Sentimientos

| Métrica | Valor |
|---------|-------|
| Algoritmo | Multinomial Naive Bayes + TF-IDF |
| Accuracy | 84.36% |
| Precision (Positivo) | 95.8% |
| Recall (Positivo) | 90.1% |
| F1-Score | 84.64% |

**Reentrenar modelo:**
```bash
python reentrenar_modelo_limpio.py
```

### 2. Sistema de Recomendación

| Característica | Descripción |
|----------------|-------------|
| Técnica | Gaussian Naive Bayes |
| Features | Ubicación, categoría, rating, distancia |
| Personalización | Por ubicación y preferencias |

**Diagnosticar modelo:**
```bash
python diagnosticar_modelo.py
```

---

## 📊 MLOps con MLflow

El proyecto incluye integración completa con **MLflow** para tracking de experimentos, versionado de modelos y métricas.

### Iniciar MLflow Server

```bash
# Con Docker Compose
docker-compose --profile mlflow up -d

# O localmente
mlflow server --host 0.0.0.0 --port 5000
```

**MLflow UI:** http://localhost:5000

### Entrenar con Tracking MLflow

```bash
# Entrenamiento con logging automático a MLflow
python src/ml/training/train_with_mlflow.py
```

### Métricas Registradas

| Categoría | Métricas |
|-----------|----------|
| **Generales** | accuracy, f1_score, cohen_kappa, matthews_corrcoef |
| **Por clase** | precision, recall, f1 (positivo/neutro/negativo) |
| **Cross-validation** | cv_mean, cv_std |

### Artefactos Guardados

- `model/` - Modelo sklearn serializado
- `vectorizer/` - TfidfVectorizer
- `confusion_matrix.png` - Matriz de confusión
- `metrics_by_class.png` - Gráfico de métricas

### Estructura de Experimentos

```
📁 Experimento: sentiment-analysis
├── 📊 Run: sentiment-train-20250127-143022
│   ├── Parámetros (18): tfidf_*, lr_*, nb_*
│   ├── Métricas (15): accuracy, f1, precision...
│   ├── Artefactos: model, vectorizer, gráficos
│   └── Tags: model_type, domain, language
└── 📊 Run: sentiment-train-20250126-...
```

### Archivos de Integración

| Archivo | Descripción |
|---------|-------------|
| `src/ml/mlflow_tracking.py` | Manager principal de MLflow |
| `src/ml/mlflow_integration.py` | Decoradores y utilidades |
| `src/ml/training/train_with_mlflow.py` | Script de entrenamiento |

### Variables de Entorno

```bash
# .env
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=sentiment-analysis
```

---

## 🧪 Testing

### Tests rápidos

```bash
# Verificar que la API funciona
python test_api_funcionando.py

# Test de integración completa
python test_integracion_completa.py
```

### Tests con pytest

```bash
# Ejecutar todos los tests
pytest test/ -v

# Con coverage
pytest test/ --cov=src --cov-report=html
```

### Verificar endpoints manualmente

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Análisis de sentimiento
curl -X POST http://localhost:8000/api/v1/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{"comment": "Excelente comida"}'
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'fastapi'"

```bash
# Asegúrate de activar el entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: "sentiment_model.pkl not found"

```bash
python reentrenar_modelo_limpio.py
```

### Error: "NLTK data not found"

```bash
python -c "import nltk; nltk.download('all')"
```

### Error: "No restaurants found"

```bash
# Verificar que existen los datos
ls data/processed/
# Debe mostrar: restaurantes_limpio.csv, reviews_limpio.csv
```

---

## ⚙️ Variables de Entorno

Crear archivo `.env`:

```env
# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Paths
MODEL_PATH=data/models/
DATA_PATH=data/processed/

# CORS
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,https://foodie.softprimesolutions.com
```

---

## 🐳 Docker

### Build

```bash
docker build -t foodieai-backend .
```

### Run

```bash
docker run -d -p 8000:8000 --name foodieai-api foodieai-backend
```

### Verificar

```bash
docker logs foodieai-api
curl http://localhost:8000/api/v1/health
```

---

## 📊 Estadísticas del Dataset

| Métrica | Valor |
|---------|-------|
| Restaurantes | 1,052 |
| Reseñas | 185,666 |
| Distritos | 7 |
| Categorías | 14 |
| Idioma | Español |

### Distritos cubiertos
- Miraflores
- San Isidro
- Barranco
- Surco
- Surquillo
- Lince
- Magdalena

---

## 📚 Documentación Adicional

- [API Swagger](http://localhost:8000/docs) - Documentación interactiva
- [Métricas del Modelo](../METRICAS_MODELO_SENTIMIENTOS.md) - Análisis detallado
- [Notebooks EDA](notebooks/) - Análisis exploratorio

---

## 🔗 Enlaces

- **Producción:** https://foodie.softprimesolutions.com/api/v1
- **Repositorio:** https://github.com/mijael18sr/foodieai-grupo4

---

*Desarrollado para UNMSM - Postgrado en Machine Learning*
