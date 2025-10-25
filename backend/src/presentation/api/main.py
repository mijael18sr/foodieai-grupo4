"""
FastAPI Application Main
Punto de entrada de la aplicación REST API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Importar routers
from src.presentation.api.routes import recommendations, health, sentiment

# Metadata de la API
API_TITLE = "Restaurant Recommender API"
API_DESCRIPTION = """
**Sistema Inteligente de Recomendación de Restaurantes**

Sistema de recomendación de restaurantes en Lima usando Machine Learning.

## Características

* Recomendaciones personalizadas basadas en ubicación y preferencias
* Predicción de ratings con Random Forest
* **Análisis de sentimientos con Redes Bayesianas** 🆕
* Búsqueda geográfica de restaurantes cercanos
* Analytics y estadísticas del sistema

## Arquitectura

- Clean Architecture en Python
- Domain-Driven Design
- Dependency Injection
- Repository Pattern

## Dataset

**Fuente**: [Lima Restaurant Review - Kaggle](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)
"""

API_VERSION = "1.0.0"
API_CONTACT = {
    "name": "UNMSM - Machine Learning",
    "email": "tu-email@unmsm.edu.pe"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager de la aplicación.
    Se ejecuta al iniciar y cerrar la app.
    """
    # Startup
    print("=" * 70)
    print("Starting Restaurant Recommender API...")
    print("=" * 70)

    # Aquí puedes cargar modelos ML, conectar a DB, etc.
    from src.infrastructure import container
    _ = container  # Initialize container
    print("Dependency Container initialized")
    print(f"API Version: {API_VERSION}")

    yield

    # Shutdown
    print("\n" + "=" * 70)
    print("Shutting down Restaurant Recommender API...")
    print("=" * 70)


# Crear aplicación FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    contact=API_CONTACT,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================================
# ROOT ENDPOINT
# =========================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - Información de la API.
    """
    return {
        "message": "Restaurant Recommender API",
        "version": API_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# =========================================================================
# INCLUIR ROUTERS (después de crearlos)
# =========================================================================

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["Recommendations"])
app.include_router(sentiment.router, prefix="/api/v1", tags=["Sentiment Analysis"])


# =========================================================================
# RUN (para desarrollo)
# =========================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )