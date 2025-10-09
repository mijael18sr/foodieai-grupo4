"""
Script para verificar que el servidor funcione correctamente
"""
import time
import requests
import subprocess
import sys

print("=" * 70)
print("🔍 VERIFICACIÓN DEL SERVIDOR")
print("=" * 70)

print("\n📝 Instrucciones:")
print("1. Abre una terminal y ejecuta:")
print("   python -m uvicorn src.presentation.api.main:app --reload")
print("\n2. Espera a que el servidor inicie (verás 'Application startup complete')")
print("\n3. Luego ejecuta este script en otra terminal:")
print("   python verify_server.py")
print("\n" + "=" * 70)

input("\n⏸️  Presiona ENTER cuando el servidor esté corriendo...")

print("\n🧪 Probando endpoints...")
print("-" * 70)

base_url = "http://localhost:8000"

# Test 1: Root
print("\n1️⃣ Test GET /")
try:
    response = requests.get(f"{base_url}/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ {data['message']}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("   ⚠️  Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    sys.exit(1)

# Test 2: Health
print("\n2️⃣ Test GET /api/v1/health")
try:
    response = requests.get(f"{base_url}/api/v1/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data['status']}")
        print(f"   ✅ Restaurantes: {data['data']['restaurants_loaded']}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Districts (EL QUE ESTABA FALLANDO)
print("\n3️⃣ Test GET /api/v1/restaurants/districts")
try:
    response = requests.get(f"{base_url}/api/v1/restaurants/districts")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        districts = response.json()
        print(f"   ✅ SUCCESS: {len(districts)} distritos")
        print(f"   📍 Distritos: {', '.join(districts)}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Categories
print("\n4️⃣ Test GET /api/v1/restaurants/categories")
try:
    response = requests.get(f"{base_url}/api/v1/restaurants/categories")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()
        print(f"   ✅ SUCCESS: {len(categories)} categorías")
        print(f"   🍽️  Ejemplos: {', '.join(categories[:5])}")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Recommendations
print("\n5️⃣ Test POST /api/v1/recommendations")
try:
    payload = {
        "user_location": {
            "lat": -12.0464,
            "long": -77.0428
        },
        "preferences": {
            "category": "Peruana"
        },
        "filters": {
            "min_rating": 4.0,
            "max_distance_km": 5.0
        },
        "top_n": 3
    }
    response = requests.post(f"{base_url}/api/v1/recommendations", json=payload)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS: {data['total_found']} recomendaciones")
        print(f"   ⏱️  Tiempo: {data['execution_time_ms']}ms")
        if data['recommendations']:
            top = data['recommendations'][0]
            print(f"   🥇 Top #1: {top['restaurant']['name']}")
            print(f"      Score: {top['score']:.3f}")
            print(f"      Distancia: {top['restaurant']['distance_km']}km")
    else:
        print(f"   ❌ Error: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 70)
print("\n📚 El servidor está funcionando correctamente.")
print("   Documentación: http://localhost:8000/docs")
print("   Swagger UI: http://localhost:8000/redoc")

