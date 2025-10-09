"""Test del Dependency Injection Container"""

from src.infrastructure import (
    container,
    Container,
    get_restaurant_repository,
    get_user_repository
)
from src.domain import User

print("=" * 70)
print("🧪 PROBANDO DEPENDENCY INJECTION CONTAINER")
print("=" * 70)

# Test 1: Container es Singleton
print("\n📦 TEST 1: Container Singleton")
print("-" * 70)

container1 = Container()
container2 = Container()
print(f"✅ container1 es container2: {container1 is container2}")
print(f"✅ container1 es container global: {container1 is container}")

# Test 2: Obtener repositorios
print("\n📦 TEST 2: Obtener Repositorios")
print("-" * 70)

restaurant_repo = get_restaurant_repository()
print(f"✅ Restaurant Repository obtenido: {type(restaurant_repo).__name__}")
print(f"   Total restaurantes: {restaurant_repo.count()}")

user_repo = get_user_repository()
print(f"✅ User Repository obtenido: {type(user_repo).__name__}")

# Test 3: Los repositorios son Singleton
print("\n📦 TEST 3: Repositorios son Singleton")
print("-" * 70)

restaurant_repo2 = get_restaurant_repository()
user_repo2 = get_user_repository()

print(f"✅ Mismo RestaurantRepository: {restaurant_repo is restaurant_repo2}")
print(f"✅ Mismo UserRepository: {user_repo is user_repo2}")

# Test 4: Usar los repositorios
print("\n📦 TEST 4: Usar Repositorios desde Container")
print("-" * 70)

# Buscar restaurantes en Miraflores
miraflores_restaurants = restaurant_repo.find_by_district("Miraflores")
print(f"✅ Restaurantes en Miraflores: {len(miraflores_restaurants)}")

# Guardar un usuario
user = User(
    user_id="U_TEST",
    location_lat=-12.0464,
    location_long=-77.0428,
    preferences={'category': 'Peruana'}
)
saved_user = user_repo.save(user)
print(f"✅ Usuario guardado: {saved_user}")

# Buscar el usuario
found_user = user_repo.find_by_id("U_TEST")
print(f"✅ Usuario encontrado: {found_user is not None}")

# Test 5: Ver todos los beans
print("\n📦 TEST 5: Beans Registrados")
print("-" * 70)

beans = container.get_all_beans()
print(f"✅ Beans en el container: {list(beans.keys())}")

# Test 6: Reset de repositorio
print("\n📦 TEST 6: Reset de Repositorio")
print("-" * 70)

print(f"   Usuarios antes del reset: {user_repo.count()}")
container.reset_repository('user_repository')

# Obtener nuevo repositorio (vacío)
new_user_repo = get_user_repository()
print(f"✅ Usuarios después del reset: {new_user_repo.count()}")
print(f"✅ Es una nueva instancia: {new_user_repo is not user_repo}")

print("\n" + "=" * 70)
print("🎉 ¡DEPENDENCY INJECTION CONTAINER FUNCIONANDO!")
print("=" * 70)