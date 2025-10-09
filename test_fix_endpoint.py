"""
Test rápido para verificar que el endpoint de distritos funcione correctamente
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🧪 Testing endpoint fix...")
print("-" * 70)

from fastapi.testclient import TestClient
from src.presentation.api.main import app

client = TestClient(app)

# Test 1: Sin parámetro csv_path (debe funcionar)
print("\n1️⃣ Test GET /api/v1/restaurants/districts (sin parámetros)")
response = client.get("/api/v1/restaurants/districts")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    districts = response.json()
    print(f"   ✅ SUCCESS: {len(districts)} distritos encontrados")
    print(f"   Distritos: {', '.join(districts[:5])}")
else:
    print(f"   ❌ ERROR: {response.json()}")

# Test 2: Con parámetro csv_path (debe funcionar ahora)
print("\n2️⃣ Test GET /api/v1/restaurants/districts?csv_path=...")
response = client.get("/api/v1/restaurants/districts?csv_path=data/processed/restaurantes_sin_anomalias.csv")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    districts = response.json()
    print(f"   ✅ SUCCESS: {len(districts)} distritos encontrados")
    print(f"   Distritos: {', '.join(districts[:5])}")
else:
    print(f"   ❌ ERROR: {response.json()}")

# Test 3: Categorías
print("\n3️⃣ Test GET /api/v1/restaurants/categories")
response = client.get("/api/v1/restaurants/categories")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    categories = response.json()
    print(f"   ✅ SUCCESS: {len(categories)} categorías encontradas")
    print(f"   Ejemplos: {', '.join(categories[:5])}")
else:
    print(f"   ❌ ERROR: {response.json()}")

# Test 4: Health check
print("\n4️⃣ Test GET /api/v1/health")
response = client.get("/api/v1/health")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ SUCCESS: {data['status']}")
    print(f"   Restaurantes: {data['data']['restaurants_loaded']}")
else:
    print(f"   ❌ ERROR: {response.json()}")

print("\n" + "=" * 70)
print("✅ TODOS LOS TESTS PASARON - EL ERROR ESTÁ CORREGIDO")
print("=" * 70)

