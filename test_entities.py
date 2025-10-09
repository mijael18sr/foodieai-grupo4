"""Test rápido de entities"""

from src.domain.entities import Restaurant, User, Recommendation

# Test Restaurant
print("=" * 60)
print("🍽️  PROBANDO ENTITY: RESTAURANT")
print("=" * 60)

restaurant = Restaurant(
    id="R001",
    title="La Rosa Náutica",
    category="Peruana",
    address="Espigón 4, Costa Verde",
    district="Miraflores",
    lat=-12.1317,
    long=-77.0325,
    stars=4.5,
    reviews=250,
    phone_number="+51 1 4470057"
)

print(f"✅ Restaurant creado: {restaurant}")
print(f"   📊 Altamente calificado: {restaurant.is_highly_rated}")
print(f"   🔥 Popular: {restaurant.is_popular}")
print(f"   📞 Tiene contacto: {restaurant.has_contact_info}")

# Test User
print("\n" + "=" * 60)
print("👤 PROBANDO ENTITY: USER")
print("=" * 60)

user = User(
    user_id="U001",
    location_lat=-12.0464,
    location_long=-77.0428,
    preferences={
        'category': 'Italiana',
        'min_rating': 4.0,
        'max_distance_km': 5.0
    }
)

print(f"✅ User creado: {user}")
print(f"   🍝 Categoría preferida: {user.preferred_category}")
print(f"   ⭐ Rating mínimo: {user.min_rating}")
print(f"   📍 Distancia máxima: {user.max_distance_km}km")

# Test Recommendation
print("\n" + "=" * 60)
print("💡 PROBANDO ENTITY: RECOMMENDATION")
print("=" * 60)

recommendation = Recommendation(
    restaurant=restaurant,
    score=0.85,
    distance_km=1.5,
    reason="Excelente opción cerca de ti con alta calificación"
)

print(f"✅ Recommendation creada: {recommendation}")
print(f"   📍 Es cercana: {recommendation.is_nearby}")
print(f"   🌟 Es excelente: {recommendation.is_excellent}")

print("\n" + "=" * 60)
print("🎉 ¡TODAS LAS ENTIDADES FUNCIONAN CORRECTAMENTE!")
print("=" * 60)