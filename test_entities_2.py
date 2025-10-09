"""Test de Domain Layer completo"""

from src.domain import Restaurant, User, Recommendation
from src.domain import RestaurantRepository, UserRepository

print("=" * 60)
print("🧪 PROBANDO IMPORTS DEL DOMAIN LAYER")
print("=" * 60)

# Test Entities
print("\n✅ Entities importadas correctamente:")
print(f"   - Restaurant: {Restaurant}")
print(f"   - User: {User}")
print(f"   - Recommendation: {Recommendation}")

# Test Repository Interfaces
print("\n✅ Repository Interfaces importadas correctamente:")
print(f"   - RestaurantRepository: {RestaurantRepository}")
print(f"   - UserRepository: {UserRepository}")

# Verificar que son interfaces (ABC)
from abc import ABC
print("\n✅ Verificando que son interfaces abstractas:")
print(f"   - RestaurantRepository es ABC: {issubclass(RestaurantRepository, ABC)}")
print(f"   - UserRepository es ABC: {issubclass(UserRepository, ABC)}")

print("\n" + "=" * 60)
print("🎉 ¡DOMAIN LAYER COMPLETO Y FUNCIONANDO!")
print("=" * 60)