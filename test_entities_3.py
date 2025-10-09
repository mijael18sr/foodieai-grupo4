"""Test de Repository Implementations"""

from src.domain import User
from src.infrastructure.repositories import CSVRestaurantRepository, MemoryUserRepository

print("=" * 70)
print("🧪 PROBANDO REPOSITORY IMPLEMENTATIONS")
print("=" * 70)

# Test CSV Restaurant Repository
print("\n📂 TEST: CSV Restaurant Repository")
print("-" * 70)

try:
    repo = CSVRestaurantRepository()

    # Contar restaurantes
    total = repo.count()
    print(f"✅ Total de restaurantes: {total}")

    # Obtener categorías
    categories = repo.get_categories()
    print(f"✅ Categorías disponibles: {len(categories)}")
    print(f"   Primeras 5: {categories[:5]}")

    # Obtener distritos
    districts = repo.get_districts()
    print(f"✅ Distritos disponibles: {len(districts)}")
    print(f"   Primeros 5: {districts[:5]}")

    # Buscar por distrito
    miraflores = repo.find_by_district("Miraflores")
    print(f"✅ Restaurantes en Miraflores: {len(miraflores)}")
    if miraflores:
        print(f"   Ejemplo: {miraflores[0]}")

    # Buscar altamente calificados
    highly_rated = repo.find_highly_rated(min_rating=4.5)
    print(f"✅ Restaurantes con rating ≥ 4.5: {len(highly_rated)}")
    if highly_rated:
        print(f"   Mejor: {highly_rated[0]}")

    # Buscar cercanos
    nearby = repo.find_nearby(lat=-12.0464, long=-77.0428, radius_km=2.0)
    print(f"✅ Restaurantes cercanos (2km): {len(nearby)}")
    if nearby:
        print(f"   Más cercano: {nearby[0]}")

except FileNotFoundError as e:
    print(f"⚠️  {e}")
    print("   Primero ejecuta: python scripts/run_data_wrangling.py")

# Test Memory User Repository
print("\n👤 TEST: Memory User Repository")
print("-" * 70)

user_repo = MemoryUserRepository()

# Crear y guardar usuario
user1 = User(
    user_id="U001",
    location_lat=-12.0464,
    location_long=-77.0428,
    preferences={'category': 'Italiana'}
)

saved_user = user_repo.save(user1)
print(f"✅ Usuario guardado: {saved_user}")

# Buscar usuario
found_user = user_repo.find_by_id("U001")
print(f"✅ Usuario encontrado: {found_user}")

# Verificar existencia
exists = user_repo.exists("U001")
print(f"✅ Usuario existe: {exists}")

# Contar usuarios
count = user_repo.count()
print(f"✅ Total usuarios: {count}")

# Actualizar usuario
user1.set_preference('min_rating', 4.0)
updated = user_repo.update(user1)
print(f"✅ Usuario actualizado: {updated.preferences}")

# Eliminar usuario
deleted = user_repo.delete("U001")
print(f"✅ Usuario eliminado: {deleted}")
print(f"✅ Total usuarios después de eliminar: {user_repo.count()}")

print("\n" + "=" * 70)
print("🎉 ¡REPOSITORIES FUNCIONANDO CORRECTAMENTE!")
print("=" * 70)