"""Test del Recommendation Service"""

from src.infrastructure import get_restaurant_repository
from src.application import RecommendationService, RecommendationRequestDTO, UserLocationDTO

print("=" * 70)
print("🧪 PROBANDO RECOMMENDATION SERVICE")
print("=" * 70)

# Obtener dependencias
restaurant_repo = get_restaurant_repository()

# Crear service (Dependency Injection)
service = RecommendationService(restaurant_repo)

# Test 1: Recomendaciones básicas
print("\n💡 TEST 1: Recomendaciones Básicas")
print("-" * 70)

request = RecommendationRequestDTO(
    user_location=UserLocationDTO(lat=-12.0464, long=-77.0428),
    preferences={'category': 'Peruana'},
    filters={'min_rating': 4.0, 'max_distance_km': 5.0},
    top_n=5
)

response = service.get_recommendations(request)

print(f"✅ Recomendaciones obtenidas: {response.total_found}")
print(f"✅ Tiempo de ejecución: {response.execution_time_ms}ms")
print(f"✅ Candidatos evaluados: {response.metadata['candidates_evaluated']}")

print("\n📋 Top 3 Recomendaciones:")
for i, rec in enumerate(response.recommendations[:3], 1):
    print(f"\n{i}. {rec.restaurant.name}")
    print(f"   Categoría: {rec.restaurant.category}")
    print(f"   Rating: {rec.restaurant.rating}⭐ ({rec.restaurant.reviews} reviews)")
    print(f"   Distancia: {rec.restaurant.distance_km}km")
    print(f"   Score: {rec.score:.3f}")
    print(f"   Razón: {rec.reason}")

# Test 2: Sin filtros (más resultados)
print("\n💡 TEST 2: Sin Filtros de Categoría")
print("-" * 70)

request2 = RecommendationRequestDTO(
    user_location=UserLocationDTO(lat=-12.0464, long=-77.0428),
    preferences={},
    filters={'min_rating': 4.5, 'max_distance_km': 3.0},
    top_n=10
)

response2 = service.get_recommendations(request2)
print(f"✅ Recomendaciones sin filtro de categoría: {response2.total_found}")
print(f"✅ Candidatos evaluados: {response2.metadata['candidates_evaluated']}")

# Test 3: Búsqueda en distrito específico
print("\n💡 TEST 3: Búsqueda en Miraflores")
print("-" * 70)

request3 = RecommendationRequestDTO(
    user_location=UserLocationDTO(lat=-12.1194, long=-77.0350),
    preferences={},
    filters={'district': 'Miraflores', 'min_rating': 4.0},
    top_n=5
)

response3 = service.get_recommendations(request3)
print(f"✅ Restaurantes en Miraflores: {response3.total_found}")

for rec in response3.recommendations[:3]:
    print(f"   • {rec.restaurant.name} - {rec.restaurant.rating}⭐")

print("\n" + "=" * 70)
print("🎉 ¡RECOMMENDATION SERVICE FUNCIONANDO!")
print("=" * 70)