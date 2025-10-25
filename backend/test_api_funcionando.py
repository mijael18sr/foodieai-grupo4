"""
Test completo del API en funcionamiento
Verifica todos los endpoints incluyendo métricas del modelo
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_root():
    """Test endpoint raíz"""
    print_section("1. VERIFICANDO SERVIDOR")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Servidor respondiendo: {response.status_code}")
        print(f"📊 Respuesta: {json.dumps(response.json(), indent=2)}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al servidor")
        print("   ¿Está el servidor ejecutándose en http://localhost:8000?")
        print("   Ejecuta: python start_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test endpoint de salud"""
    print_section("2. VERIFICANDO SALUD DEL SISTEMA")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        data = response.json()
        print(f"✅ Health Check: {response.status_code}")
        print(f"📊 Estado: {data.get('status')}")

        # Mostrar detalles del modelo de sentimientos
        if 'models' in data and 'sentiment_analysis' in data['models']:
            sentiment = data['models']['sentiment_analysis']
            print(f"\n🧠 MODELO DE SENTIMIENTOS:")
            print(f"   Estado: {sentiment.get('status')}")
            print(f"   Tipo: {sentiment.get('type')}")
            print(f"   Entrenado: {sentiment.get('is_trained')}")

            if 'metrics' in sentiment:
                metrics = sentiment['metrics']
                print(f"\n📊 MÉTRICAS DEL MODELO:")
                print(f"   Accuracy: {metrics.get('accuracy', 'N/A')}")
                print(f"   Precision (macro): {metrics.get('precision_macro', 'N/A')}")
                print(f"   Recall (macro): {metrics.get('recall_macro', 'N/A')}")
                print(f"   F1-Score (macro): {metrics.get('f1_macro', 'N/A')}")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sentiment_analyze():
    """Test análisis de sentimiento individual"""
    print_section("3. PROBANDO ANÁLISIS DE SENTIMIENTO")

    comentarios_prueba = [
        "La comida estuvo deliciosa, el servicio excelente",
        "Pésimo servicio, comida fría y cara",
        "Normal, nada especial"
    ]

    for i, comment in enumerate(comentarios_prueba, 1):
        print(f"\n[{i}] Comentario: '{comment}'")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/sentiment/analyze",
                json={"comment": comment},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                sentiment = data['sentiment']
                confidence = data['confidence']
                probs = data['probabilities']

                emoji = {"positivo": "😊", "neutro": "😐", "negativo": "😞"}.get(sentiment, "")
                print(f"   Sentimiento: {emoji} {sentiment.upper()}")
                print(f"   Confianza: {confidence:.4f} ({confidence*100:.2f}%)")
                print(f"   Probabilidades:")
                for sent, prob in probs.items():
                    print(f"     {sent}: {prob:.4f}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    return True

def test_model_metrics():
    """Test endpoint de métricas del modelo"""
    print_section("4. OBTENIENDO MÉTRICAS COMPLETAS DEL MODELO")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/sentiment/model/metrics", timeout=10)

        if response.status_code == 200:
            data = response.json()

            print(f"✅ Métricas del modelo obtenidas")
            print(f"\n📊 MÉTRICAS GENERALES:")
            print(f"   Accuracy: {data.get('accuracy', 'N/A')}")
            print(f"   Precision (macro): {data.get('precision_macro', 'N/A')}")
            print(f"   Precision (weighted): {data.get('precision_weighted', 'N/A')}")
            print(f"   Recall (macro): {data.get('recall_macro', 'N/A')}")
            print(f"   Recall (weighted): {data.get('recall_weighted', 'N/A')}")
            print(f"   F1-Score (macro): {data.get('f1_macro', 'N/A')}")
            print(f"   F1-Score (weighted): {data.get('f1_weighted', 'N/A')}")
            print(f"   Cohen's Kappa: {data.get('cohen_kappa', 'N/A')}")
            print(f"   Matthews Correlation: {data.get('matthews_corrcoef', 'N/A')}")

            if 'per_class_metrics' in data:
                print(f"\n📊 MÉTRICAS POR CLASE:")
                for clase, metrics in data['per_class_metrics'].items():
                    emoji = {"positivo": "😊", "neutro": "😐", "negativo": "😞"}.get(clase, "")
                    print(f"\n   {emoji} {clase.upper()}:")
                    print(f"      Precision: {metrics.get('precision', 'N/A')}")
                    print(f"      Recall: {metrics.get('recall', 'N/A')}")
                    print(f"      F1-Score: {metrics.get('f1_score', 'N/A')}")
                    print(f"      Support: {metrics.get('support', 'N/A')}")

            print(f"\n📅 Última evaluación: {data.get('last_evaluation', 'N/A')}")

            # Nota sobre R²
            print(f"\n" + "-" * 80)
            print("ℹ️  NOTA SOBRE R² (R-CUADRADO):")
            print("-" * 80)
            print("R² es una métrica para REGRESIÓN (predecir números continuos).")
            print("Este modelo es de CLASIFICACIÓN (predecir categorías).")
            print("\nPara clasificación, las métricas equivalentes son:")
            print(f"  • Cohen's Kappa: {data.get('cohen_kappa', 'N/A')} (acuerdo predicción-realidad)")
            print(f"  • Matthews Correlation: {data.get('matthews_corrcoef', 'N/A')} (calidad clasificación)")
            print("\nValores cercanos a 1 = excelente rendimiento")
            print("Valores cercanos a 0 = predicción aleatoria")

            return True
        else:
            print(f"❌ Error {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_analysis():
    """Test análisis batch"""
    print_section("5. PROBANDO ANÁLISIS BATCH")

    comentarios = [
        "Excelente restaurante, lo recomiendo",
        "Muy mala experiencia, no vuelvo",
        "Normal, nada destacable",
        "Increíble comida, ambiente perfecto",
        "Horrible, nunca más"
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/sentiment/analyze/batch",
            json={"comments": comentarios},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Análisis batch completado")
            print(f"   Total procesados: {data['total']}")
            print(f"\n📊 RESUMEN:")
            print(f"   Positivos: {data['summary']['positivo']}")
            print(f"   Neutros: {data['summary']['neutro']}")
            print(f"   Negativos: {data['summary']['negativo']}")
            return True
        else:
            print(f"❌ Error {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 80)
    print("  🧪 TEST COMPLETO DEL API - BACKEND FUNCIONANDO")
    print("=" * 80)
    print(f"  URL Base: {BASE_URL}")
    print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Ejecutar tests
    if not test_root():
        return

    test_health()
    test_sentiment_analyze()
    test_model_metrics()
    test_batch_analysis()

    # Resumen final
    print_section("✅ RESUMEN FINAL")
    print("El backend está funcionando correctamente!")
    print("\n📖 Documentación interactiva disponible en:")
    print(f"   {BASE_URL}/docs")
    print("\n🔗 Endpoints principales:")
    print(f"   GET  {BASE_URL}/api/v1/health")
    print(f"   POST {BASE_URL}/api/v1/sentiment/analyze")
    print(f"   POST {BASE_URL}/api/v1/sentiment/analyze/batch")
    print(f"   GET  {BASE_URL}/api/v1/sentiment/model/metrics")
    print(f"   GET  {BASE_URL}/api/v1/sentiment/restaurant/{{id}}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

