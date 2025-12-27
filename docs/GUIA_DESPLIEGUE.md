# 🚀 Guía de Despliegue Paso a Paso
## Sistema de Recomendación de Restaurantes con IA - FoodieAI

> **Proyecto de Machine Learning - UNMSM Postgrado - Grupo 4**  
> Guía completa para desplegar el sistema en entorno local y producción (AWS)

---

## 🌐 URLs de Producción (Live Demo)

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **🍽️ Aplicación Web** | https://foodie.softprimesolutions.com | Frontend React en producción |
| **📚 API Documentation** | http://18.216.22.178:8000/docs | Swagger UI - Documentación interactiva |
| **🔬 MLflow Tracking** | http://18.216.22.178:5000 | UI para tracking de experimentos ML |
| **❤️ Health Check** | http://18.216.22.178:8000/api/v1/health/status | Estado del sistema |

> **Nota:** El proyecto está desplegado en AWS (EC2 + RDS + S3) con dominio configurado en Cloudflare.

---

## 📋 Índice

0. [Arquitectura del Backend - Clean Architecture](#parte-0-arquitectura-del-backend---clean-architecture)
1. [Preparar el Modelo](#parte-1-preparar-el-modelo)
2. [Crear la API](#parte-2-crear-la-api)
3. [Dashboard y Frontend](#parte-3-dashboard-y-frontend)
4. [Diseño y Experiencia de Usuario](#parte-4-diseño-y-experiencia-de-usuario)
5. [Despliegue Local](#parte-5-despliegue-local)
6. [Despliegue en AWS](#parte-6-despliegue-en-aws)
7. [MLOps - Ciclo de Vida del Modelo](#parte-7-mlops---ciclo-de-vida-del-modelo)
8. [Checklist Final](#checklist-final)

---

## Introducción

Esta guía documenta el proceso completo de despliegue del sistema **FoodieAI**, un recomendador de restaurantes que utiliza:

- **Análisis de Sentimientos**: Clasificación de reseñas (positivo/neutro/negativo) con 84.4% accuracy
- **Sistema de Recomendación**: Algoritmo híbrido basado en contenido y filtrado colaborativo
- **Clustering**: Segmentación de restaurantes por características
- **MLOps**: Prácticas de operaciones de ML para gestión del ciclo de vida

### Arquitectura General del Sistema

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            INFRAESTRUCTURA AWS                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│   │  Frontend   │────▶│   Backend   │────▶│  Modelos ML │                   │
│   │ React+Vite  │     │   FastAPI   │     │ scikit-learn│                   │
│   │  (nginx)    │     │   :8000     │     │   .pkl      │                   │
│   └─────────────┘     └──────┬──────┘     └─────────────┘                   │
│                              │                                               │
│                    ┌─────────┴─────────┐                                    │
│                    │                   │                                    │
│              ┌─────▼─────┐       ┌─────▼─────┐                              │
│              │  MLflow   │       │    S3     │                              │
│              │  :5000    │       │ Artifacts │                              │
│              └─────┬─────┘       └───────────┘                              │
│                    │                                                         │
│              ┌─────▼─────┐                                                  │
│              │    RDS    │                                                  │
│              │PostgreSQL │                                                  │
│              └───────────┘                                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │    Cloudflare     │
                    │   DNS + HTTPS     │
                    └───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  GitHub Actions   │
                    │     CI/CD         │
                    └───────────────────┘
```

---

## Parte 0: Arquitectura del Backend - Clean Architecture

### 0.1 Patrón Arquitectónico

El backend implementa **Clean Architecture** (Arquitectura Limpia), también conocida como **Hexagonal Architecture** o **Ports & Adapters**. Este patrón fue propuesto por Robert C. Martin (Uncle Bob) y garantiza:

- **Independencia de frameworks**: La lógica de negocio no depende de FastAPI
- **Testabilidad**: Cada capa puede probarse de forma aislada
- **Independencia de UI**: El dominio no conoce la presentación
- **Independencia de BD**: Se puede cambiar CSV por PostgreSQL sin afectar el dominio

### 0.2 Capas de la Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
│                    (FastAPI Controllers)                        │
│         src/presentation/api/routes/*.py                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│              (Services, Use Cases, DTOs)                        │
│    src/application/services/*.py, use_cases/*.py, dto/*.py      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DOMAIN LAYER                             │
│              (Entities, Repository Interfaces)                  │
│     src/domain/entities/*.py, repositories/*.py                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
│        (Repository Implementations, ML Models, Config)          │
│   src/infrastructure/repositories/*.py, ml/*.py, container.py   │
└─────────────────────────────────────────────────────────────────┘
```

### 0.3 Estructura de Carpetas

```
backend/src/
├── domain/                          # 🎯 CAPA DE DOMINIO (núcleo)
│   ├── entities/                    # Entidades de negocio
│   │   ├── restaurant.py            # @dataclass Restaurant
│   │   ├── review.py                # @dataclass Review
│   │   ├── user.py                  # @dataclass User
│   │   ├── district.py              # @dataclass District
│   │   └── recommendation.py        # @dataclass Recommendation
│   └── repositories/                # Interfaces (contratos)
│       ├── restaurant_repository.py # ABC RestaurantRepository
│       ├── review_repository.py     # ABC ReviewRepository
│       └── user_repository.py       # ABC UserRepository
│
├── application/                     # 📋 CAPA DE APLICACIÓN
│   ├── dto/                         # Data Transfer Objects
│   │   ├── request_dto.py           # DTOs de entrada
│   │   ├── response_dto.py          # DTOs de salida
│   │   └── sentiment_dto.py         # DTOs de sentimiento
│   ├── services/                    # Servicios de negocio
│   │   ├── recommendation_service.py
│   │   ├── sentiment_service.py
│   │   └── district_service.py
│   └── use_cases/                   # Casos de uso
│       └── district_use_cases.py
│
├── infrastructure/                  # 🔧 CAPA DE INFRAESTRUCTURA
│   ├── container.py                 # IoC Container (DI)
│   ├── config/                      # Configuraciones
│   ├── repositories/                # Implementaciones concretas
│   │   ├── csv_restaurant_repository.py  # Lee desde CSV
│   │   ├── csv_review_repository.py
│   │   └── memory_user_repository.py
│   └── ml/                          # Modelos ML
│       └── model_loader.py
│
├── presentation/                    # 🌐 CAPA DE PRESENTACIÓN
│   └── api/
│       ├── main.py                  # FastAPI app
│       ├── routes/                  # Endpoints
│       │   ├── health.py            # /health/*
│       │   ├── sentiment.py         # /sentiment/*
│       │   └── recommendations.py   # /recommendations/*
│       └── district_router.py       # /restaurants/*
│
└── ml/                              # 🤖 MÓDULO ML
    ├── models/                      # Clases de modelos
    │   └── sentiment_model.py
    ├── preprocessing/               # Preprocesamiento
    └── training/                    # Scripts de entrenamiento
```

### 0.4 Componentes Principales

#### **Domain Layer (Capa de Dominio)**

Contiene las **entidades de negocio** y las **interfaces de repositorios**. Es el núcleo de la aplicación y no tiene dependencias externas.

```python
# src/domain/entities/restaurant.py
@dataclass
class Restaurant:
    """Entidad de negocio - Restaurante"""
    id: str
    title: str
    category: str
    district: str
    stars: float
    reviews: int
    
    @property
    def is_highly_rated(self) -> bool:
        """Regla de negocio: calificación alta"""
        return self.stars >= 4.0
```

```python
# src/domain/repositories/restaurant_repository.py
class RestaurantRepository(ABC):
    """Interface del repositorio - Define el contrato"""
    
    @abstractmethod
    def find_all(self) -> List[Restaurant]:
        pass
    
    @abstractmethod
    def find_by_district(self, district: str) -> List[Restaurant]:
        pass
```

#### **Application Layer (Capa de Aplicación)**

Contiene los **servicios** y **casos de uso** que orquestan la lógica de negocio.

```python
# src/application/services/recommendation_service.py
class RecommendationService:
    """Servicio que orquesta la lógica de recomendaciones"""
    
    def __init__(self, restaurant_repository: RestaurantRepository):
        # Dependency Injection - recibe la interface, no la implementación
        self.restaurant_repository = restaurant_repository
    
    def get_recommendations(self, preferences: dict) -> List[Restaurant]:
        restaurants = self.restaurant_repository.find_all()
        # Aplicar lógica de negocio y ML
        return self._rank_restaurants(restaurants, preferences)
```

#### **Infrastructure Layer (Capa de Infraestructura)**

Contiene las **implementaciones concretas** de los repositorios y el **contenedor de inyección de dependencias**.

```python
# src/infrastructure/repositories/csv_restaurant_repository.py
class CSVRestaurantRepository(RestaurantRepository):
    """Implementación concreta que lee desde CSV"""
    
    def __init__(self, csv_path: str):
        self._df = pd.read_csv(csv_path)
    
    def find_all(self) -> List[Restaurant]:
        return [self._row_to_entity(row) for _, row in self._df.iterrows()]
```

```python
# src/infrastructure/container.py
class Container:
    """IoC Container - Gestiona la inyección de dependencias"""
    
    def restaurant_repository(self) -> RestaurantRepository:
        # Retorna la implementación concreta
        return CSVRestaurantRepository('data/processed/restaurantes.csv')
    
    def recommendation_service(self) -> RecommendationService:
        # Inyecta las dependencias
        return RecommendationService(self.restaurant_repository())
```

#### **Presentation Layer (Capa de Presentación)**

Contiene los **endpoints de FastAPI** que exponen la funcionalidad al exterior.

```python
# src/presentation/api/routes/recommendations.py
@router.post("/recommendations")
async def get_recommendations(request: RecommendationRequestDTO):
    """Endpoint que usa el servicio de recomendaciones"""
    service = container.recommendation_service()
    recommendations = service.get_recommendations(request.dict())
    return RecommendationResponseDTO(items=recommendations)
```

### 0.5 Flujo de una Petición

```
HTTP Request
     │
     ▼
┌────────────────┐
│  Presentation  │  1. Recibe request, valida con Pydantic
│   (FastAPI)    │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Application   │  2. Orquesta lógica de negocio
│   (Services)   │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│    Domain      │  3. Aplica reglas de negocio
│  (Entities)    │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Infrastructure │  4. Accede a datos (CSV, ML models)
│ (Repositories) │
└────────────────┘
```

### 0.6 Principios SOLID Aplicados

| Principio | Implementación |
|-----------|----------------|
| **S** - Single Responsibility | Cada clase tiene una sola responsabilidad |
| **O** - Open/Closed | Nuevos repositorios sin modificar existentes |
| **L** - Liskov Substitution | CSVRepository sustituible por DBRepository |
| **I** - Interface Segregation | Interfaces específicas por entidad |
| **D** - Dependency Inversion | Services dependen de interfaces, no implementaciones |

### 0.7 Beneficios de esta Arquitectura

| Beneficio | Descripción |
|-----------|-------------|
| **Testabilidad** | Mock de repositorios para unit tests |
| **Mantenibilidad** | Cambios aislados por capa |
| **Escalabilidad** | Fácil migración de CSV a PostgreSQL |
| **Claridad** | Estructura predecible y organizada |
| **Reutilización** | Servicios reutilizables en diferentes contextos |

---

## Parte 1: Preparar el Modelo

### 1.1 Modelos Entrenados

Nuestro proyecto utiliza **4 modelos** de Machine Learning guardados en formato `.pkl`:

| Modelo | Archivo | Tipo | Uso |
|--------|---------|------|-----|
| **Sentimientos** | `sentiment_model.pkl` | VotingClassifier (scikit-learn) | Clasificación de reseñas |
| **Recomendador** | `recommender_system.pkl` | Híbrido | Sugerencia de restaurantes |
| **Clustering** | `clustering_model.pkl` | K-Means | Segmentación |
| **Rating Predictor** | `rating_predictor.pkl` | Regresión | Predicción de calificaciones |

### 1.2 Ubicación de los Modelos

```
backend/
└── data/
    └── models/
        ├── sentiment_model.pkl          # Modelo principal (84.4% accuracy)
        ├── recommender_system.pkl       # Sistema de recomendación
        ├── clustering_model.pkl         # Clustering de restaurantes
        ├── rating_predictor.pkl         # Predictor de ratings
        └── backups/                     # Respaldos de versiones anteriores
```

### 1.3 Cómo se Guarda el Modelo

```python
import joblib

# Guardar modelo entrenado
joblib.dump(modelo, 'backend/data/models/sentiment_model.pkl')

# Cargar modelo
modelo = joblib.load('backend/data/models/sentiment_model.pkl')
```

### 1.4 Métricas del Modelo de Sentimientos

| Métrica | Valor |
|---------|-------|
| **Accuracy** | 84.4% |
| **Cohen's Kappa** | 0.5606 |
| **Precision (positivo)** | 87% |
| **Recall (positivo)** | 95% |
| **F1-Score** | 85% |

---

## Parte 2: Crear la API

### 2.1 Framework Utilizado

Utilizamos **FastAPI** por sus ventajas:
- Documentación automática (Swagger UI)
- Validación con Pydantic
- Alto rendimiento (async)
- Tipado estático

### 2.2 Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/health/status` | GET | Estado del sistema y modelo |
| `/api/v1/sentiment/analyze` | POST | Analizar sentimiento de texto |
| `/api/v1/recommendations` | POST | Obtener recomendaciones |
| `/api/v1/restaurants/districts` | GET | Listar distritos disponibles |
| `/api/v1/restaurants/categories` | GET | Listar categorías de comida |

### 2.3 Ejemplo: Endpoint de Predicción

**Archivo:** `backend/src/presentation/api/routes/sentiment.py`

```python
@router.post("/analyze")
async def analyze_sentiment(request: SentimentRequest):
    """
    Analiza el sentimiento de un texto de reseña
    
    Returns:
        - sentiment: "positivo", "neutro", "negativo"
        - confidence: 0.0 - 1.0
        - probabilities: probabilidades por clase
    """
    model = get_sentiment_model()
    result = model.predict_single(request.text)
    
    return {
        "sentiment": result["sentiment"],
        "confidence": result["confidence"],
        "probabilities": result["probabilities"]
    }
```

### 2.4 Probar la API Localmente

```bash
# Iniciar el servidor
cd backend
python start_server.py

# Probar con curl
curl -X POST "http://localhost:8000/api/v1/sentiment/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "La comida estuvo deliciosa, excelente servicio"}'

# Respuesta esperada:
{
  "sentiment": "positivo",
  "confidence": 0.92,
  "probabilities": {
    "positivo": 0.92,
    "neutro": 0.06,
    "negativo": 0.02
  }
}
```

### 2.5 Health Check Endpoint

**Archivo:** `backend/src/presentation/api/routes/health.py`

```python
@router.get("/status")
async def health_status():
    """Health check con información del modelo"""
    model = get_sentiment_model()
    
    return {
        "status": "healthy",
        "model": {
            "loaded": True,
            "type": "sentiment_analysis_clean_v2",
            "accuracy": 0.844
        },
        "system": {
            "memory_usage_percent": 67.0,
            "cpu_usage_percent": 8.0
        }
    }
```

---

## Parte 3: Dashboard y Frontend

### 3.1 Tecnologías del Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React** | 19 | Framework UI |
| **Vite** | 6.0 | Build tool |
| **TypeScript** | 5.6 | Tipado estático |
| **TailwindCSS** | 3.4 | Estilos |
| **Recharts** | 2.x | Gráficas interactivas |

### 3.2 Componentes Principales

```
frontend/src/
├── pages/
│   ├── Home/                    # Página principal con búsqueda
│   └── Explore/                 # Exploración de restaurantes
├── components/
│   ├── RestaurantCard.tsx       # Tarjeta de restaurante
│   ├── SearchFilters.tsx        # Filtros de búsqueda
│   ├── SentimentBadge.tsx       # Badge de sentimiento
│   └── RatingStars.tsx          # Estrellas de calificación
└── services/
    └── api.ts                   # Cliente API
```

### 3.3 Gráficas y Visualizaciones

El dashboard incluye:

- **📊 Distribución de Sentimientos**: Gráfico de barras/pie
- **⭐ Ratings Promedio**: Por distrito y categoría
- **🗺️ Mapa de Calor**: Restaurantes por ubicación
- **📈 Tendencias**: Análisis temporal de reseñas

### 3.4 Características de Accesibilidad

- ✅ Contraste de colores WCAG 2.1
- ✅ Tooltips explicativos en gráficas
- ✅ Botones de ayuda (?) con descripciones
- ✅ Navegación por teclado
- ✅ Responsive design (móvil/tablet/desktop)

---

## Parte 4: Diseño y Experiencia de Usuario

### 4.1 Design Thinking Aplicado

**Problema que resuelve:**
> "Encontrar restaurantes de calidad en Lima basándose en experiencias reales de otros comensales"

**Usuario objetivo:**
- Personas buscando restaurantes en Lima
- Turistas y locales
- Personas sin conocimientos técnicos de ML

### 4.2 Flujo de Usuario

```
1. Usuario ingresa a la página
           ▼
2. Selecciona distrito y preferencias
           ▼
3. Sistema analiza sentimientos de reseñas
           ▼
4. Muestra recomendaciones ordenadas por score
           ▼
5. Usuario ve detalles y reseñas destacadas
```

### 4.3 Principios de Diseño Implementados

| Principio | Implementación |
|-----------|----------------|
| **Claridad** | Etiquetas descriptivas, iconos intuitivos |
| **Simplicidad** | Máximo 3 clics para cualquier acción |
| **Feedback** | Loading states, mensajes de éxito/error |
| **Consistencia** | Paleta de colores unificada |

---

## Parte 5: Despliegue Local

### 5.1 Requisitos Previos

| Software | Versión Mínima |
|----------|----------------|
| Python | 3.10+ |
| Node.js | 18+ |
| Git | 2.x |
| Espacio en disco | 5GB |

### 5.2 Paso 1: Clonar Repositorio

```bash
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd restaurant-recommender-ml
```

### 5.3 Paso 2: Configurar Backend

```bash
# Entrar al directorio
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Activar entorno (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar recursos NLTK
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### 5.4 Paso 3: Iniciar Backend

```bash
# Opción 1: Script directo
python start_server.py

# Opción 2: Uvicorn manual
uvicorn src.presentation.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Verificar que funciona:**
```bash
curl http://localhost:8000/api/v1/health/status
```

### 5.5 Paso 4: Configurar Frontend

```bash
# En otra terminal
cd frontend

# Instalar dependencias
npm install

# Iniciar en desarrollo
npm run dev
```

### 5.6 Paso 5: Verificar Despliegue Local

| Servicio | URL | Estado Esperado |
|----------|-----|-----------------|
| Frontend | http://localhost:5173 | Página principal visible |
| Backend API | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/api/v1/health/status | `{"status": "healthy"}` |

---

## Parte 6: Despliegue en AWS

### 6.1 Arquitectura de Producción

```
                    ┌─────────────────┐
                    │   Cloudflare    │
                    │   (DNS + CDN)   │
                    │ foodie.soft...  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │      EC2        │
                    │   t3.micro      │
                    │  18.216.22.178  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌─────▼─────┐        ┌────▼────┐
   │Frontend │         │  Backend  │        │ MLflow  │
   │ :80     │         │  :8000    │        │ :5000   │
   │ (nginx) │         │ (FastAPI) │        │         │
   └─────────┘         └─────┬─────┘        └────┬────┘
                             │                   │
                        ┌────▼────┐         ┌────▼────┐
                        │   S3    │         │   RDS   │
                        │ Assets  │         │PostgreSQL│
                        └─────────┘         └─────────┘
```

### 6.2 Servicios AWS Utilizados

| Servicio | Uso | Tier |
|----------|-----|------|
| **EC2** | Servidor principal | t3.micro (Free Tier) |
| **ECR** | Registro de imágenes Docker | Free Tier |
| **S3** | Assets estáticos y artefactos | Free Tier |
| **RDS** | PostgreSQL para MLflow | db.t3.micro (Free Tier) |

### 6.3 Paso 1: Configurar AWS CLI

```bash
# Instalar AWS CLI
# Windows: descargar de https://aws.amazon.com/cli/

# Configurar credenciales
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region: us-east-2
# Default output format: json
```

### 6.4 Paso 2: Desplegar con Terraform

```bash
cd infrastructure/terraform

# Inicializar Terraform
terraform init

# Ver plan de despliegue
terraform plan

# Aplicar cambios
terraform apply
```

### 6.5 Paso 3: Build y Push de Imágenes Docker

```bash
# Login a ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 937792903641.dkr.ecr.us-east-2.amazonaws.com

# Build Backend
cd backend
docker build -t restaurant-recommender-backend .
docker tag restaurant-recommender-backend:latest 937792903641.dkr.ecr.us-east-2.amazonaws.com/restaurant-recommender-backend:latest
docker push 937792903641.dkr.ecr.us-east-2.amazonaws.com/restaurant-recommender-backend:latest

# Build Frontend
cd ../frontend
docker build -t restaurant-recommender-frontend .
docker tag restaurant-recommender-frontend:latest 937792903641.dkr.ecr.us-east-2.amazonaws.com/restaurant-recommender-frontend:latest
docker push 937792903641.dkr.ecr.us-east-2.amazonaws.com/restaurant-recommender-frontend:latest
```

### 6.6 Paso 4: Desplegar en EC2

```bash
# Conectar a EC2
ssh -i "restaurant-recommender-key.pem" ec2-user@18.216.22.178

# Pull de imágenes
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 937792903641.dkr.ecr.us-east-2.amazonaws.com
docker pull 937792903641.dkr.ecr.us-east-2.amazonaws.com/restaurant-recommender-backend:latest
docker pull 937792903641.dkr.ecr.us-east-2.amazonaws.com/restaurant-recommender-frontend:latest

# Iniciar servicios
docker-compose -f docker-compose.aws.yml up -d
```

---

## Parte 7: MLOps - Ciclo de Vida del Modelo

### 7.1 ¿Qué es MLOps?

**MLOps** (Machine Learning Operations) es un conjunto de prácticas que combina Machine Learning, DevOps y Data Engineering para:

- 🔄 **Automatizar** el ciclo de vida de modelos ML
- 📊 **Trackear** experimentos y versiones de modelos
- 🚀 **Desplegar** modelos de forma reproducible
- 📈 **Monitorear** el rendimiento en producción

### 7.2 Componentes MLOps Implementados

| Componente | Herramienta | Estado | Descripción |
|------------|-------------|--------|-------------|
| **Experiment Tracking** | MLflow + PostgreSQL | ✅ Implementado | Registro de parámetros, métricas y artefactos |
| **Model Versioning** | MLflow Model Registry | ✅ Implementado | Versionado y staging de modelos |
| **Model Serving** | FastAPI + Docker | ✅ Implementado | API REST para inferencia |
| **CI/CD Pipeline** | GitHub Actions | ✅ Implementado | Automatización de tests y deploy |
| **Containerization** | Docker + Docker Compose | ✅ Implementado | Empaquetado reproducible |
| **Infrastructure as Code** | Terraform | ✅ Implementado | Provisioning de AWS |
| **Model Monitoring** | Health Endpoint | ✅ Implementado | Estado del modelo y sistema |
| **Artifact Storage** | S3 + MLflow | ✅ Implementado | Almacenamiento de modelos |
| **Data Versioning** | Git + .pkl | ⚠️ Parcial | Modelos versionados en Git |
| **Automated Retraining** | - | ❌ Pendiente | Reentrenamiento automático |

### 7.3 Arquitectura MLOps

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MLOps Pipeline                                    │
└─────────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Data Prep   │────▶│   Training    │────▶│  Validation   │
│  (notebooks)  │     │ (train_*.py)  │     │ (métricas)    │
└───────────────┘     └───────┬───────┘     └───────┬───────┘
                              │                     │
                              ▼                     ▼
                    ┌─────────────────────────────────────┐
                    │           MLflow Tracking           │
                    │  • Parámetros: max_features, C...   │
                    │  • Métricas: accuracy, f1, kappa    │
                    │  • Artefactos: modelo.pkl           │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        MLflow Model Registry        │
                    │  • Versiones: v1, v2, v3...         │
                    │  • Stages: Staging → Production     │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────┴───────────────────┐
                    │                                     │
                    ▼                                     ▼
          ┌─────────────────┐               ┌─────────────────┐
          │   S3 Artifacts  │               │  RDS PostgreSQL │
          │  (modelos .pkl) │               │  (metadata)     │
          └─────────────────┘               └─────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │          GitHub Actions             │
                    │  • Test Backend (pytest)            │
                    │  • Test Frontend (npm test)         │
                    │  • Build Docker Images              │
                    │  • Push to ECR                      │
                    │  • Deploy to EC2                    │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │        Production (EC2)             │
                    │  • FastAPI serving modelo           │
                    │  • Health check monitoring          │
                    │  • MLflow UI para visualización     │
                    └─────────────────────────────────────┘
```

### 7.4 MLflow - Experiment Tracking

#### Configuración en AWS

MLflow está desplegado con:
- **Backend Store**: PostgreSQL en RDS (`restaurant-recommender-mlflow-db`)
- **Artifact Store**: S3 (`s3://foodie-ai-static-assets/mlflow-artifacts/`)
- **UI**: http://18.216.22.178:5000

#### Integración en Código

**Archivo:** `backend/src/ml/mlflow_integration.py`

```python
import mlflow
from mlflow.tracking import MlflowClient

class MLflowManager:
    """Gestor centralizado de MLflow para tracking de experimentos"""
    
    _instance = None
    
    def __new__(cls, tracking_uri: str = None, experiment_name: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, tracking_uri: str = None, experiment_name: str = None):
        if self._initialized:
            return
        
        self.tracking_uri = tracking_uri or "http://18.216.22.178:5000"
        self.experiment_name = experiment_name or "sentiment-analysis"
        
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)
        
        self.client = MlflowClient()
        self._initialized = True
    
    def start_run(self, run_name: str = None):
        """Inicia un nuevo run de MLflow"""
        return mlflow.start_run(run_name=run_name)
    
    def log_params(self, params: dict):
        """Registra parámetros del modelo"""
        for key, value in params.items():
            mlflow.log_param(key, value)
    
    def log_metrics(self, metrics: dict):
        """Registra métricas del modelo"""
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
    
    def log_model(self, model, artifact_path: str):
        """Registra el modelo entrenado"""
        mlflow.sklearn.log_model(model, artifact_path)
```

#### Ejemplo de Uso

```python
from src.ml.mlflow_integration import MLflowManager

# Inicializar manager
mlflow_manager = MLflowManager()

# Entrenar y registrar
with mlflow_manager.start_run(run_name='sentiment-v2'):
    # Log parámetros
    mlflow_manager.log_params({
        'model_type': 'VotingClassifier',
        'max_features': 15000,
        'ngram_range': '(1,2)'
    })
    
    # Entrenar modelo
    model.fit(X_train, y_train)
    
    # Log métricas
    mlflow_manager.log_metrics({
        'accuracy': 0.844,
        'cohen_kappa': 0.5606,
        'f1_weighted': 0.85
    })
    
    # Log modelo
    mlflow_manager.log_model(model, 'sentiment-model')
```

### 7.5 CI/CD Pipeline (GitHub Actions)

**Archivo:** `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # 1. Pruebas del Backend
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest test/ -v --tb=short

  # 2. Pruebas del Frontend
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install and test
        run: |
          cd frontend
          npm ci
          npm run build

  # 3. Build y Push a ECR
  build-and-push:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-2
      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2
      - name: Build and push images
        run: |
          # Backend
          docker build -t $ECR_REGISTRY/restaurant-recommender-backend:latest ./backend
          docker push $ECR_REGISTRY/restaurant-recommender-backend:latest
          
          # Frontend
          docker build -t $ECR_REGISTRY/restaurant-recommender-frontend:latest ./frontend
          docker push $ECR_REGISTRY/restaurant-recommender-frontend:latest

  # 4. Deploy a EC2
  deploy-ec2:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: 18.216.22.178
          username: ec2-user
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /home/ec2-user/app
            ./deploy.sh
```

### 7.6 Containerización (Docker)

#### Estructura de Dockerfiles

```
project/
├── backend/
│   └── Dockerfile              # Python + FastAPI
├── frontend/
│   └── Dockerfile              # Node + Nginx
├── docker-compose.yml          # Desarrollo local
├── docker-compose.prod.yml     # Producción
└── docker-compose.aws.yml      # AWS con ECR
```

#### Backend Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar recursos NLTK
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "src.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.7 Infrastructure as Code (Terraform)

**Archivo:** `infrastructure/terraform/main.tf`

```hcl
# Proveedor AWS
provider "aws" {
  region = "us-east-2"
}

# EC2 Instance
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = {
    Name = "restaurant-recommender-server"
  }
}

# RDS PostgreSQL para MLflow
resource "aws_db_instance" "mlflow_db" {
  identifier           = "restaurant-recommender-mlflow-db"
  engine               = "postgres"
  engine_version       = "14"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  db_name              = "mlflow"
  username             = "mlflow_admin"
  password             = var.db_password
  skip_final_snapshot  = true
}

# S3 Bucket para artefactos
resource "aws_s3_bucket" "artifacts" {
  bucket = "foodie-ai-static-assets"
}

# ECR Repository
resource "aws_ecr_repository" "backend" {
  name = "restaurant-recommender-backend"
}

resource "aws_ecr_repository" "frontend" {
  name = "restaurant-recommender-frontend"
}
```

### 7.8 Monitoreo del Modelo

#### Health Check Endpoint

El endpoint `/api/v1/health/status` proporciona:

```json
{
  "status": "healthy",
  "model": {
    "loaded": true,
    "type": "sentiment_analysis_clean_v2",
    "accuracy": 0.844,
    "last_training": "2025-12-10"
  },
  "system": {
    "memory_usage_percent": 67.0,
    "cpu_usage_percent": 8.0,
    "disk_usage_percent": 45.0
  },
  "mlflow": {
    "connected": true,
    "tracking_uri": "http://18.216.22.178:5000"
  }
}
```

### 7.9 Versionado de Modelos

Los modelos se versionan mediante:

1. **Git**: Archivos `.pkl` en `backend/data/models/`
2. **MLflow Model Registry**: Versiones con stages (Staging, Production)
3. **Backups**: Carpeta `backend/data/models/backups/`

```
backend/data/models/
├── sentiment_model.pkl              # Modelo actual (v2)
├── recommender_system.pkl           # Recomendador
├── clustering_model.pkl             # Clustering
├── rating_predictor.pkl             # Predictor
└── backups/
    ├── sentiment_model_v1.pkl       # Versión anterior
    └── sentiment_model_20251201.pkl # Por fecha
```

### 7.10 Roadmap MLOps

| Componente | Estado Actual | Próximos Pasos |
|------------|---------------|----------------|
| Experiment Tracking | ✅ MLflow | Añadir más métricas |
| Model Registry | ✅ Básico | Automatizar promoción a Production |
| CI/CD | ✅ GitHub Actions | Añadir smoke tests post-deploy |
| Monitoring | ⚠️ Health check | Implementar Prometheus + Grafana |
| Data Versioning | ⚠️ Manual | Implementar DVC |
| Auto-retraining | ❌ No implementado | Trigger por drift detection |
| A/B Testing | ❌ No implementado | Comparar modelos en producción |

---

## Checklist Final

### ✅ Modelo ML
- [x] Modelo entrenado con accuracy > 80%
- [x] Guardado en formato `.pkl` portable
- [x] Métricas documentadas (accuracy, precision, recall, f1)
- [x] Pruebas de predicción funcionando

### ✅ API Backend
- [x] FastAPI configurado con documentación automática
- [x] Endpoint `/predict` o `/analyze` funcionando
- [x] Health check implementado (`/health/status`)
- [x] CORS configurado para frontend
- [x] Respuestas en formato JSON claro

### ✅ Frontend/Dashboard
- [x] Interfaz responsive (móvil/desktop)
- [x] Gráficas claras con Recharts
- [x] Filtros de búsqueda intuitivos
- [x] Loading states y manejo de errores
- [x] Accesibilidad implementada

### ✅ Experiencia de Usuario
- [x] Etiquetas claras y descriptivas
- [x] Tooltips y ayuda contextual
- [x] Flujo de usuario lógico
- [x] Colores con buen contraste
- [x] Mensajes de feedback al usuario

### ✅ Despliegue Local
- [x] Instrucciones claras en README
- [x] Backend funciona en localhost:8000
- [x] Frontend funciona en localhost:5173
- [x] Todos los endpoints probados

### ✅ Despliegue en Producción (AWS)
- [x] EC2 configurado y corriendo
- [x] Imágenes Docker en ECR
- [x] Dominio configurado (foodie.softprimesolutions.com)
- [x] HTTPS con Cloudflare

### ✅ MLOps
- [x] MLflow configurado con PostgreSQL + S3
- [x] Experiment tracking funcionando
- [x] Model versioning implementado
- [x] CI/CD con GitHub Actions
- [x] Dockerfiles optimizados
- [x] Infrastructure as Code (Terraform)
- [x] Health check con métricas del modelo
- [ ] Data versioning (DVC) - Pendiente
- [ ] Automated retraining - Pendiente

### ✅ Documentación
- [x] README.md completo
- [x] API documentada en Swagger
- [x] Guía de despliegue (este documento)
- [x] Métricas del modelo documentadas
- [x] MLOps documentado

---

## 📞 Soporte

**Repositorio:** https://github.com/mijael18sr/foodieai-grupo4

---

*Documento generado para el Proyecto de Machine Learning - UNMSM Postgrado*  
*Última actualización: Diciembre 2025*
