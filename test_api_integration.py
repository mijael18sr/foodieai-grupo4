"""
Test de Integración para verificar que todo funcione correctamente.
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("🧪 TEST DE INTEGRACIÓN - VERIFICACIÓN COMPLETA DEL SISTEMA")
print("=" * 70)
print()

# ============================================
# TEST 1: IMPORTACIONES
# ============================================
print("📦 TEST 1: Verificando importaciones...")
print("-" * 70)

try:
    # Domain Layer
    from src.domain.entities import Restaurant, User, Recommendation
    from src.domain.repositories import RestaurantRepository, UserRepository
    print("✅ Domain Layer importado correctamente")

    # Application Layer
    from src.application.services import RecommendationService
    from src.application.dto import (
        RecommendationRequestDTO,
        RecommendationResponseDTO,
        UserLocationDTO
    )
    print("✅ Application Layer importado correctamente")

    # Infrastructure Layer
    from src.infrastructure.container import Container, get_restaurant_repository
    from src.infrastructure.repositories import CSVRestaurantRepository
    print("✅ Infrastructure Layer importado correctamente")

    # Presentation Layer
    from src.presentation.api.main import app
    print("✅ Presentation Layer (FastAPI) importado correctamente")

    print("✅ TODAS LAS IMPORTACIONES EXITOSAS\n")
except Exception as e:
    print(f"❌ ERROR en importaciones: {e}\n")
    sys.exit(1)

# ============================================
# TEST 2: VERIFICAR DATOS
# ============================================
print("📊 TEST 2: Verificando datos procesados...")
print("-" * 70)

try:
    csv_path = project_root / "data" / "processed" / "restaurantes_sin_anomalias.csv"
    if not csv_path.exists():
        print(f"❌ ERROR: No se encuentra {csv_path}")
        print("   Ejecuta: python scripts/run_data_wrangling.py")
        sys.exit(1)

    import pandas as pd
    df = pd.read_csv(csv_path)
    print(f"✅ Archivo CSV encontrado: {len(df)} restaurantes")
    print(f"   Columnas: {', '.join(df.columns[:5])}...")
    print(f"✅ DATOS VERIFICADOS\n")
except Exception as e:
    print(f"❌ ERROR verificando datos: {e}\n")
    sys.exit(1)

# ============================================
# TEST 3: REPOSITORIO
# ============================================
print("🗄️  TEST 3: Verificando repositorio...")
print("-" * 70)

try:
    repo = get_restaurant_repository()

    # Test: count
    total = repo.count()
    print(f"✅ Total de restaurantes: {total}")

    # Test: categorías
    categories = repo.get_categories()
    print(f"✅ Categorías encontradas: {len(categories)}")
    print(f"   Ejemplos: {', '.join(categories[:5])}")

    # Test: distritos
    districts = repo.get_districts()
    print(f"✅ Distritos encontrados: {len(districts)}")
    print(f"   Ejemplos: {', '.join(districts[:5])}")

    # Test: find_all
    restaurants = repo.find_all()
    print(f"✅ Find all: {len(restaurants)} restaurantes")

    # Test: highly rated
    highly_rated = repo.find_highly_rated(min_rating=4.5)
    print(f"✅ Altamente calificados (>4.5⭐): {len(highly_rated)}")

    print("✅ REPOSITORIO FUNCIONANDO CORRECTAMENTE\n")
except Exception as e:
    print(f"❌ ERROR en repositorio: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================
# TEST 4: ENTIDADES DE DOMINIO
# ============================================
print("🏛️  TEST 4: Verificando entidades de dominio...")
print("-" * 70)

try:
    # Test: Restaurant
    restaurant = Restaurant(
        id="TEST_001",
        title="Test Restaurant",
        category="Italiana",
        address="Av. Test 123",
        district="Miraflores",
        lat=-12.1191,
        long=-77.0350,
        stars=4.5,
        reviews=100
    )
    assert restaurant.is_highly_rated == True
    assert restaurant.is_popular == True
    print(f"✅ Entidad Restaurant: {restaurant}")

    # Test: User
    user = User(
        user_id="USER_001",
        location_lat=-12.0464,
        location_long=-77.0428,
        preferences={"category": "Peruana"}
    )
    assert user.preferred_category == "Peruana"
    print(f"✅ Entidad User: {user}")

    # Test: Recommendation
    recommendation = Recommendation(
        restaurant=restaurant,
        score=0.85,
        distance_km=1.5,
        reason="Excelente opción cerca de ti"
    )
    assert recommendation.is_excellent == True
    assert recommendation.is_nearby == True
    print(f"✅ Entidad Recommendation: {recommendation}")

    print("✅ ENTIDADES DE DOMINIO FUNCIONANDO\n")
except Exception as e:
    print(f"❌ ERROR en entidades: {e}\n")
    sys.exit(1)

# ============================================
# TEST 5: SERVICIO DE RECOMENDACIONES
# ============================================
print("🎯 TEST 5: Verificando servicio de recomendaciones...")
print("-" * 70)

try:
    service = RecommendationService(repo)

    # Crear request
    request = RecommendationRequestDTO(
        user_location=UserLocationDTO(lat=-12.0464, long=-77.0428),
        preferences={"category": "Peruana"},
        filters={"min_rating": 4.0, "max_distance_km": 5.0},
        top_n=5
    )

    # Obtener recomendaciones
    response = service.get_recommendations(request)

    print(f"✅ Recomendaciones generadas: {response.total_found}")
    print(f"   Tiempo de ejecución: {response.execution_time_ms}ms")

    if response.recommendations:
        top = response.recommendations[0]
        print(f"   Top #1: {top.restaurant.name}")
        print(f"           Score: {top.score:.3f}")
        print(f"           Distancia: {top.restaurant.distance_km}km")
        print(f"           Razón: {top.reason}")

    print("✅ SERVICIO DE RECOMENDACIONES FUNCIONANDO\n")
except Exception as e:
    print(f"❌ ERROR en servicio: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================
# TEST 6: API FASTAPI
# ============================================
print("🚀 TEST 6: Verificando API FastAPI...")
print("-" * 70)

try:
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # Test: Root endpoint
    response = client.get("/")
    assert response.status_code == 200
    print(f"✅ GET /: {response.json()['message']}")

    # Test: Health check
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    print(f"✅ GET /api/v1/health: {data['status']}")
    print(f"   Restaurantes cargados: {data['data']['restaurants_loaded']}")

    # Test: Categories
    response = client.get("/api/v1/restaurants/categories")
    assert response.status_code == 200
    categories = response.json()
    print(f"✅ GET /api/v1/restaurants/categories: {len(categories)} categorías")

    # Test: Districts
    response = client.get("/api/v1/restaurants/districts")
    assert response.status_code == 200
    districts = response.json()
    print(f"✅ GET /api/v1/restaurants/districts: {len(districts)} distritos")

    # Test: Recommendations
    payload = {
        "user_location": {"lat": -12.0464, "long": -77.0428},
        "preferences": {"category": "Peruana"},
        "filters": {"min_rating": 4.0, "max_distance_km": 5.0},
        "top_n": 3
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"✅ POST /api/v1/recommendations: {data['total_found']} recomendaciones")
    print(f"   Tiempo: {data['execution_time_ms']}ms")

    print("✅ API FASTAPI FUNCIONANDO PERFECTAMENTE\n")
except Exception as e:
    print(f"❌ ERROR en API: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================
# TEST 7: VERIFICAR PAQUETES ML
# ============================================
print("🤖 TEST 7: Verificando paquetes de Machine Learning...")
print("-" * 70)

try:
    import numpy as np
    import pandas as pd
    import sklearn
    import scipy
    import matplotlib
    import seaborn

    print(f"✅ numpy: {np.__version__}")
    print(f"✅ pandas: {pd.__version__}")
    print(f"✅ scikit-learn: {sklearn.__version__}")
    print(f"✅ scipy: {scipy.__version__}")
    print(f"✅ matplotlib: {matplotlib.__version__}")
    print(f"✅ seaborn: {seaborn.__version__}")

    # Test funcionalidad básica
    arr = np.array([1, 2, 3, 4, 5])
    assert arr.mean() == 3.0
    print("✅ NumPy funcionando correctamente")

    df_test = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    assert len(df_test) == 3
    print("✅ Pandas funcionando correctamente")

    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    print("✅ Scikit-learn funcionando correctamente")

    print("✅ TODOS LOS PAQUETES ML FUNCIONANDO\n")
except Exception as e:
    print(f"❌ ERROR en paquetes ML: {e}\n")
    sys.exit(1)

# ============================================
# RESUMEN FINAL
# ============================================
print("=" * 70)
print("✅ ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
print("=" * 70)
print()
print("📊 RESUMEN:")
print(f"   ✅ Importaciones: OK")
print(f"   ✅ Datos procesados: {total} restaurantes")
print(f"   ✅ Repositorio: {len(categories)} categorías, {len(districts)} distritos")
print(f"   ✅ Entidades de dominio: OK")
print(f"   ✅ Servicio de recomendaciones: OK")
print(f"   ✅ API FastAPI: OK")
print(f"   ✅ Paquetes ML: OK")
print()
print("🎉 EL SISTEMA ESTÁ COMPLETAMENTE FUNCIONAL")
print()
print("🚀 Para iniciar el servidor:")
print("   python -m uvicorn src.presentation.api.main:app --reload")
print()
print("📚 Documentación API:")
print("   http://localhost:8000/docs")
print("=" * 70)

