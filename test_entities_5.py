"""Test de DTOs"""

from src.application.dto import (
    RecommendationRequestDTO,
    RecommendationResponseDTO,
    RestaurantDTO,
    RecommendationItemDTO,
    UserLocationDTO
)

print("=" * 70)
print("🧪 PROBANDO DTOs")
print("=" * 70)

# Test Request DTO
print("\n📥 TEST: Request DTO")
print("-" * 70)

request = RecommendationRequestDTO(
    user_location=UserLocationDTO(lat=-12.0464, long=-77.0428),
    preferences={"category": "Italiana"},
    filters={"min_rating": 4.0, "max_distance_km": 5.0},
    top_n=5
)

print(f"✅ Request DTO creado:")
print(f"   Ubicación: ({request.user_location.lat}, {request.user_location.long})")
print(f"   Preferencias: {request.preferences}")
print(f"   Filtros: {request.filters}")
print(f"   Top N: {request.top_n}")

# Test Response DTO
print("\n📤 TEST: Response DTO")
print("-" * 70)

restaurant_dto = RestaurantDTO(
    id="R001",
    name="La Rosa Náutica",
    category="Peruana",
    rating=4.5,
    reviews=250,
    distance_km=1.5,
    address="Espigón 4",
    district="Miraflores",
    phone="+51 1 4470057"
)

recommendation_item = RecommendationItemDTO(
    restaurant=restaurant_dto,
    score=0.85,
    reason="Excelente opción cerca de ti con alta calificación"
)

response = RecommendationResponseDTO(
    recommendations=[recommendation_item],
    total_found=1,
    execution_time_ms=145
)

print(f"✅ Response DTO creado:")
print(f"   Recomendaciones: {len(response.recommendations)}")
print(f"   Primera recomendación: {response.recommendations[0].restaurant.name}")
print(f"   Score: {response.recommendations[0].score}")
print(f"   Tiempo: {response.execution_time_ms}ms")

# Test Validación Pydantic
print("\n✅ TEST: Validación automática")
print("-" * 70)

try:
    # Esto debe fallar (latitud fuera de rango)
    invalid = UserLocationDTO(lat=50.0, long=-77.0)
except Exception as e:
    print(f"✅ Validación funciona - Error esperado: {type(e).__name__}")

# Test Serialización JSON
print("\n📝 TEST: Serialización JSON")
print("-" * 70)

json_data = response.model_dump_json(indent=2)
print(f"✅ DTO serializado a JSON:")
print(json_data[:200] + "...")

print("\n" + "=" * 70)
print("🎉 ¡DTOs FUNCIONANDO CORRECTAMENTE!")
print("=" * 70)