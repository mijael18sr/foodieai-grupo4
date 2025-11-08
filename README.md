# Sistema de Recomendación de Restaurantes con IA

> **Proyecto de Machine Learning - UNMSM Postgrado**  
> Sistema inteligente de recomendación de restaurantes en Lima usando análisis de sentimientos y ML.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## Descripción

Sistema de recomendación que utiliza Machine Learning y análisis de sentimientos para sugerir restaurantes en Lima. Combina técnicas de procesamiento de lenguaje natural con algoritmos de recomendación personalizada.

**Características:**
- Análisis de sentimientos con 84.36% accuracy
- Recomendaciones basadas en ubicación y preferencias  
- API REST con FastAPI y frontend React moderno
- 706 restaurantes y 378,969 reviews procesadas

## Inicio Rápido

### Requisitos
- Python 3.10+ y Node.js 18+
- 5GB espacio libre

### Instalación (3 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd restaurant-recommender-ml

# 2. Backend (Terminal 1)
cd backend
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
python start_server.py

# 3. Frontend (Terminal 2)
cd ../frontend
npm install && npm run dev
```

### Acceso
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/health

## Estructura del Proyecto

```
restaurant-recommender-ml/
├── backend/                 # API FastAPI + ML
│   ├── data/               # Datasets y modelos
│   │   ├── models/        # Modelos ML entrenados
│   │   └── processed/     # Datos procesados
│   ├── src/               # Código fuente (Clean Architecture)
│   ├── requirements.txt   # Dependencias Python
│   └── start_server.py   # Iniciar servidor
├── frontend/              # React + TypeScript
│   ├── src/              # Componentes React
│   ├── package.json     # Dependencias Node.js
│   └── vite.config.ts   # Configuración build
└── README.md            # Este archivo
```

## API Endpoints Principales

### Análisis de Sentimientos
```http
POST /api/v1/sentiment/analyze
{
  "text": "La comida estuvo deliciosa y el servicio excelente"
}
```

### Recomendaciones
```http
POST /api/v1/recommendations  
{
  "user_location": {"lat": -12.0464, "lng": -77.0428},
  "preferences": {"category": "Peruana", "min_rating": 4.0},
  "top_n": 10
}
```

## Métricas del Modelo

| Métrica | Valor | Estado |
|---------|-------|--------|
| **Accuracy** | 84.36% | Excelente |
| **Precision (Positivos)** | 95.8% | Muy alto |
| **Recall (Positivos)** | 90.1% | Muy alto |
| **Tiempo respuesta** | <100ms | Rápido |

## Solución de Problemas

### Error: "No module named 'fastapi'"
```bash
cd backend
.venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>
```

### Error: "No se encuentra modelo sentiment_model.pkl"
```bash
cd backend
python reentrenar_modelo_limpio.py
```

## Archivos de Datos

**Incluidos en el repositorio:**
- Modelos ML entrenados (sentiment_model.pkl, etc.)
- Datasets pequeños (<50MB)
- 706 restaurantes procesados

**Excluidos (>100MB):**
- `Lima_Restaurants_2025_08_13.csv` (131MB)
- `reviews_con_sentimiento.csv` (1.3GB)
- Los modelos funcionan sin estos archivos grandes

## Testing

```bash
# Backend
cd backend && python test_api_funcionando.py

# Frontend
cd frontend && npm run test
```

## Tecnologías

**Backend:** Python, FastAPI, Scikit-learn, NLTK, Pandas  
**Frontend:** React 19, TypeScript, Tailwind CSS, Vite  
**ML:** Ensemble (Complement NB + Logistic Regression)  
**Arquitectura:** Clean Architecture, API REST

## Equipo

**UNMSM - Postgrado en Machine Learning**  
Desarrollado con fines académicos y de investigación.

## Enlaces

- **Repositorio:** https://github.com/mijael18sr/foodieai-grupo4
- **Documentación API:** http://localhost:8000/docs (después de iniciar)
- **Demo Frontend:** http://localhost:5173 (después de iniciar)

---

*Para más detalles técnicos, consulta los archivos en /backend y /frontend*

### Opción A: Ejecución Inmediata (Recomendada)

Si quieres ver el proyecto funcionando inmediatamente:

```bash
# 1. Clonar el repositorio
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd restaurant-recommender-ml

# 2. Backend (Terminal 1)
cd backend
python -m venv .venv
.venv\Scripts\activate # En Windows
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
python start_server.py

# 3. Frontend (Terminal 2)
cd ../frontend
npm install
npm run dev

# 4. ¡Listo! 
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

**⏱ Tiempo total:** 3-5 minutos (ya incluye modelos preentrenados)

---

## INSTALACIÓN COMPLETA PASO A PASO

### Requisitos Previos

- **Python 3.10+** ([Descargar](https://www.python.org/downloads/))
- **Node.js 18+** ([Descargar](https://nodejs.org/))
- **Git** ([Descargar](https://git-scm.com/downloads))
- **5GB espacio libre** (proyecto + dependencias)

### 1⃣ CLONAR EL PROYECTO

```bash
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd restaurant-recommender-ml
```

### 2⃣ CONFIGURAR BACKEND (Python/FastAPI)

```bash
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Descargar recursos de NLTK (para análisis de sentimientos)
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### 3⃣ CONFIGURAR FRONTEND (React/TypeScript)

```bash
cd ../frontend

# Instalar dependencias
npm install

# O usando yarn
yarn install
```

### 4⃣ VERIFICAR DATOS Y MODELOS

Los modelos preentrenados ya están incluidos en el repositorio:

```bash
cd backend

# Verificar modelos ML (deberían existir)
ls data/models/
# sentiment_model.pkl (84.36% accuracy)
# clustering_model.pkl
# rating_predictor.pkl 
# recommender_system.pkl

# Verificar dataset principal
ls data/raw/
# Lima_Restaurants_2025_08_13_clean.csv (378,969 reviews)
```

---

## EJECUCIÓN DEL PROYECTO

### Iniciar Backend (Terminal 1)

```bash
cd backend
.venv\Scripts\activate # Activar entorno virtual
python start_server.py
```

**Salida esperada:**
```
 Iniciando Restaurant Recommender API...
 Backend URL: http://localhost:8000
 API Docs: http://localhost:8000/docs
 Modo desarrollo con auto-reload activado
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Iniciar Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

**Salida esperada:**
```
 Local: http://localhost:5173/
 Network: use --host to expose
 press h + enter to show help
```

### Verificar que funciona

1. **Backend API:** http://localhost:8000/docs
2. **Frontend App:** http://localhost:5173
3. **Health Check:** http://localhost:8000/api/v1/health

---

## TESTING Y VALIDACIÓN

### Backend Testing

```bash
cd backend

# Test básico de API
python test_api_funcionando.py

# Test de integración completo
python test_integracion_completa.py

# Diagnosticar modelo de sentimientos
python diagnosticar_modelo.py

# Comparar modelos
python comparar_modelos.py
```

### Frontend Testing

```bash
cd frontend

# Linting
npm run lint

# Tests unitarios
npm run test

# Coverage
npm run test:coverage
```

---

## DATOS Y MODELOS

### Dataset

- **Fuente:** [Lima Restaurant Reviews - Kaggle](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)
- **706 restaurantes** de alta calidad en Lima
- **378,969 reviews** de clientes reales
- **Ratings:** 1-5 estrellas
- **Idioma:** Español (análisis de sentimiento especializado)

### Modelos de Machine Learning

#### 1. Modelo de Análisis de Sentimientos 
```
Técnica: Ensemble Voting (Complement NB + Logistic Regression)
Accuracy: 84.36% 
Precision Positivos: 95.8%
Recall Positivos: 90.1%
F1-Score: 84.64%
```

#### 2. Sistema de Clustering 
- **Algoritmo:** K-Means con optimización automática
- **Características:** Ubicación, categoría, ratings, sentimientos
- **Grupos:** Segmentación inteligente de restaurantes

#### 3. Predictor de Ratings 
- **Algoritmo:** Random Forest Regressor
- **Input:** Características del restaurante + historial
- **Output:** Rating estimado (1-5 estrellas)

#### 4. Motor de Recomendación 
- **Técnica:** Hybrid (Collaborative + Content-based)
- **Personalización:** Ubicación + preferencias + sentimientos
- **Output:** Top-N recomendaciones rankeadas

---

## ESTRUCTURA DEL PROYECTO

```
restaurant-recommender-ml/
 backend/ # Backend Python/FastAPI
 requirements.txt # Dependencias Python
 start_server.py # Iniciar servidor
 test_api_funcionando.py # Tests de API
 reentrenar_modelo_limpio.py # Entrenar modelo sentimientos
 diagnosticar_modelo.py # Diagnóstico del modelo
 data/ # Datasets y modelos
 raw/ # Datos originales
 Lima_Restaurants_2025_08_13_clean.csv 
 processed/ # Datos procesados 
 models/ # Modelos ML entrenados
 sentiment_model.pkl (84.36% accuracy)
 clustering_model.pkl 
 rating_predictor.pkl 
 recommender_system.pkl 
 src/ # Código fuente (Clean Architecture)
 application/ # Servicios de aplicación
 domain/ # Lógica de negocio 
 infrastructure/ # Implementaciones
 presentation/ # API REST endpoints
 frontend/ # Frontend React/TypeScript
 package.json # Dependencias Node.js
 vite.config.ts # Configuración Vite
 tailwind.config.js # Configuración Tailwind CSS
 src/ # Código fuente React
 components/ # Componentes reutilizables
 pages/ # Páginas principales
 hooks/ # Custom React hooks
 services/ # Cliente API
 types/ # Tipos TypeScript
 README.md # Este archivo
 .gitignore # Archivos ignorados por Git
 METRICAS_MODELO_SENTIMIENTOS.md # Documentación del modelo
```

---

## API ENDPOINTS

### Documentación Interactiva
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints Principales

#### Health Check
```http
GET /api/v1/health
```

#### Análisis de Sentimientos
```http
POST /api/v1/sentiment/analyze
{
 "text": "La comida estuvo deliciosa y el servicio excelente"
}
```

#### Obtener Recomendaciones
```http
POST /api/v1/recommendations
{
 "user_location": {
 "lat": -12.0464,
 "lng": -77.0428
 },
 "preferences": {
 "category": "Peruana",
 "max_distance_km": 5,
 "min_rating": 4.0
 },
 "top_n": 10
}
```

---

## CONFIGURACIÓN AVANZADA

### Variables de Entorno

Crear archivo `.env` en la carpeta `backend/`:

```env
# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# ML Configuration 
MODEL_PATH=data/models/
DATA_PATH=data/

# CORS Configuration
FRONTEND_URL=http://localhost:5173
```

### Configuración del Frontend

Crear archivo `.env.local` en la carpeta `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=Restaurant Recommender
```

---

## SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "No module named 'fastapi'"

```bash
cd backend
.venv\Scripts\activate # Asegúrate de activar el entorno virtual
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>

# Linux/Mac 
lsof -ti:8000 | xargs kill
```

### Error: "No se encuentra el modelo sentiment_model.pkl"

```bash
cd backend
python reentrenar_modelo_limpio.py # Entrenar modelo (10-15 min)
```

### Error: NLTK Data not found

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### Frontend: npm install falla

```bash
# Limpiar cache npm
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## DESPLIEGUE EN PRODUCCIÓN

### Docker (Próximamente)

```bash
# Build y ejecutar con Docker Compose
docker-compose up --build

# Acceder a:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Cloud Deploy

El proyecto está preparado para despliegue en:
- **Frontend:** Vercel, Netlify
- **Backend:** Heroku, Railway, AWS Lambda
- **Database:** PostgreSQL, MongoDB

---

## MÉTRICAS Y RENDIMIENTO

### KPIs del Modelo ML

| Métrica | Valor | Estado |
|---------|-------|--------|
| **Accuracy** | 84.36% | Excelente |
| **Precision (Positivos)** | 95.8% | Muy alto |
| **Recall (Positivos)** | 90.1% | Muy alto |
| **F1-Score** | 84.64% | Balanceado |
| **Tiempo de respuesta** | <100ms | Rápido |

### Estadísticas del Dataset

| Estadística | Valor |
|-------------|-------|
| **Restaurantes totales** | 706 |
| **Reviews totales** | 378,969 |
| **Reviews positivos** | ~70% |
| **Reviews negativos** | ~15% |
| **Reviews neutros** | ~15% |
| **Cobertura Lima** | 43 distritos |

---

## CONTRIBUIR AL PROYECTO

### Setup para Desarrolladores

```bash
# 1. Fork del repositorio
git clone https://github.com/TU-USUARIO/restaurant-recommender-ml.git

# 2. Crear rama para feature
git checkout -b feature/nueva-funcionalidad

# 3. Hacer cambios y commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 4. Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

### Estándares de Código

- **Python:** PEP 8, type hints, docstrings
- **TypeScript:** ESLint, Prettier, interfaces tipadas
- **Git:** Conventional commits
- **Testing:** ≥80% coverage

---

## DOCUMENTACIÓN ADICIONAL

### Recursos Técnicos

- [ Backend README](backend/README.md) - Documentación detallada del backend
- [ Frontend README](frontend/README.md) - Guía del frontend React
- [ Métricas del Modelo](METRICAS_MODELO_SENTIMIENTOS.md) - Análisis detallado del ML
- [ API Documentation](http://localhost:8000/docs) - Swagger interactivo

### Recursos de Aprendizaje

- **Machine Learning:** [Scikit-learn Docs](https://scikit-learn.org/stable/)
- **FastAPI:** [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- **React:** [React 18 Docs](https://reactjs.org/docs/getting-started.html)
- **Clean Architecture:** [Clean Code by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## ‍ EQUIPO DE DESARROLLO

**UNMSM - Postgrado en Machine Learning**

### Desarrolladores

- **Desarrollo Full-Stack & ML Engineering**
- **Análisis de Datos & Feature Engineering** 
- **UI/UX Design & Frontend Development**
- **DevOps & Infrastructure**

---

## LICENCIA

Este proyecto es parte del programa de **Postgrado en Machine Learning de la Universidad Nacional Mayor de San Marcos (UNMSM)**. 

Desarrollado con fines académicos y de investigación.

---

## ROADMAP FUTURO

### Próximas Funcionalidades

- [ ] ** Sistema de Autenticación** (Login/Register)
- [ ] ** Sistema de Favoritos** (Guardar restaurantes)
- [ ] ** Dashboard Analítico** (Métricas avanzadas)
- [ ] ** Chatbot IA** (Recomendaciones conversacionales)
- [ ] ** App Mobile** (React Native)
- [ ] ** Containerización** (Docker + K8s)
- [ ] ** Deploy Cloud** (AWS/GCP)
- [ ] ** A/B Testing** (Optimización de modelos)

### Mejoras ML

- [ ] ** Deep Learning** (BERT para sentimientos)
- [ ] ** AutoML** (Optimización automática)
- [ ] ** Real-time Learning** (Modelos adaptativos)
- [ ] ** Multi-idioma** (English support)

---

## CONTACTO Y SOPORTE

### ¿Necesitas ayuda?

1. ** Revisa el troubleshooting** arriba
2. ** Ejecuta los tests:** `python test_api_funcionando.py`
3. ** Verifica logs** del servidor
4. ** Crea un issue** en GitHub

### Contacto Académico

- **Universidad:** Universidad Nacional Mayor de San Marcos (UNMSM)
- **Programa:** Postgrado en Machine Learning
- **Proyecto:** Sistema de Recomendación de Restaurantes con IA

---

## ¡EMPEZAR AHORA!

### Para la experiencia más rápida:

```bash
# Paso 1: Clonar
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd restaurant-recommender-ml

# Paso 2: Backend (Terminal 1)
cd backend && python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
python start_server.py

# Paso 3: Frontend (Terminal 2) 
cd frontend && npm install && npm run dev

# ¡Listo! 
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

**⏱ Tiempo total: 3-5 minutos**

---

** ¡Dale una estrella al proyecto si te pareció útil! **

---

*Desarrollado con por el equipo de Machine Learning de UNMSM*