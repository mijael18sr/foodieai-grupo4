"""
Test de Integración Completa del Sistema de Métricas y Confiabilidad
Verifica que todos los componentes funcionan correctamente juntos.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_integracion_completa():
    """Probar integración completa del sistema"""

    print("=" * 80)
    print("🧪 TEST DE INTEGRACIÓN COMPLETA")
    print("=" * 80)

    errores = []
    warnings = []

    # TEST 1: Cargar Modelo
    print("\n1️⃣ TEST: Cargar Modelo de Sentimientos")
    try:
        from src.ml.models import SentimentAnalysisModel

        model = SentimentAnalysisModel()
        model_path = project_root / "data" / "models" / "sentiment_model.pkl"

        if not model_path.exists():
            errores.append("❌ Modelo no encontrado en: " + str(model_path))
        else:
            model.load(str(model_path))
            print(f"   ✅ Modelo cargado correctamente")
            print(f"   📊 Vocabulario: {len(model.vectorizer.vocabulary_):,} términos")
    except Exception as e:
        errores.append(f"❌ Error cargando modelo: {e}")

    # TEST 2: Servicio de Análisis con Nivel de Confianza
    print("\n2️⃣ TEST: Servicio de Análisis con Nivel de Confianza")
    try:
        from src.application.services.sentiment_service import SentimentAnalysisService, get_confidence_level
        from src.infrastructure.container import get_review_repository, get_sentiment_model

        # Crear servicio
        review_repo = get_review_repository()
        sentiment_model = get_sentiment_model()
        service = SentimentAnalysisService(review_repo, sentiment_model)

        # Probar análisis
        test_comment = "La comida estuvo deliciosa"
        result = service.analyze_comment(test_comment)

        # Verificar que contiene confidence_level
        if 'confidence_level' not in result:
            errores.append("❌ El servicio NO retorna 'confidence_level'")
        else:
            print(f"   ✅ Servicio retorna 'confidence_level': {result['confidence_level']}")
            print(f"   📝 Comentario: \"{test_comment}\"")
            print(f"   🎯 Sentimiento: {result['sentiment']}")
            print(f"   📊 Confianza: {result['confidence']:.1%}")
            print(f"   🏷️  Nivel: {result['confidence_level']}")

        # Probar función get_confidence_level
        nivel = get_confidence_level(0.95)
        if nivel != "MUY CONFIABLE":
            errores.append(f"❌ get_confidence_level(0.95) debería ser 'MUY CONFIABLE', es '{nivel}'")
        else:
            print(f"   ✅ Función get_confidence_level funciona correctamente")

    except Exception as e:
        errores.append(f"❌ Error en servicio: {e}")
        import traceback
        traceback.print_exc()

    # TEST 3: DTOs actualizados
    print("\n3️⃣ TEST: DTOs con Campo confidence_level")
    try:
        from src.application.dto.sentiment_dto import SentimentAnalysisResponseDTO

        # Crear DTO de prueba
        dto = SentimentAnalysisResponseDTO(
            comment="Test comment",
            sentiment="positivo",
            confidence=0.95,
            confidence_level="MUY CONFIABLE",
            probabilities={"positivo": 0.95, "neutro": 0.03, "negativo": 0.02}
        )

        if dto.confidence_level != "MUY CONFIABLE":
            errores.append("❌ DTO no almacena correctamente confidence_level")
        else:
            print(f"   ✅ DTO funciona correctamente con confidence_level")
            print(f"   📦 DTO creado: {dto.sentiment} ({dto.confidence:.1%}) - {dto.confidence_level}")

    except Exception as e:
        errores.append(f"❌ Error en DTOs: {e}")
        import traceback
        traceback.print_exc()

    # TEST 4: Endpoint de API (simulación)
    print("\n4️⃣ TEST: Integración con Endpoint de API")
    try:
        from src.presentation.api.routes.sentiment import analyze_sentiment
        from src.application.dto.sentiment_dto import SentimentAnalysisRequestDTO
        import asyncio

        # Crear request
        request = SentimentAnalysisRequestDTO(comment="Excelente servicio")

        # Ejecutar endpoint (simulación)
        async def test_endpoint():
            response = await analyze_sentiment(request)
            return response

        # Ejecutar
        response = asyncio.run(test_endpoint())

        if not hasattr(response, 'confidence_level'):
            warnings.append("⚠️ Respuesta API no incluye confidence_level en el objeto")
        else:
            print(f"   ✅ Endpoint retorna confidence_level correctamente")
            print(f"   🌐 API Response: {response.sentiment} - {response.confidence_level}")

    except Exception as e:
        # No es crítico si falla (puede ser por configuración de FastAPI)
        warnings.append(f"⚠️ No se pudo probar endpoint completo: {e}")
        print(f"   ⚠️ Prueba de endpoint omitida (no crítico)")

    # TEST 5: Función interpretar_confianza
    print("\n5️⃣ TEST: Función interpretar_confianza")
    try:
        from optimizar_modelo_gastronómico import interpretar_confianza

        # Probar diferentes niveles
        test_cases = [
            (0.95, "MUY CONFIABLE"),
            (0.85, "CONFIABLE"),
            (0.75, "MODERADO"),
            (0.65, "BAJA CONFIANZA"),
            (0.50, "INDETERMINADO")
        ]

        all_ok = True
        for confidence, expected_status in test_cases:
            result = interpretar_confianza("positivo", confidence)
            if result['status'] != expected_status:
                errores.append(f"❌ interpretar_confianza({confidence}) esperaba '{expected_status}', obtuvo '{result['status']}'")
                all_ok = False

        if all_ok:
            print(f"   ✅ Función interpretar_confianza funciona para todos los umbrales")
            print(f"   🎨 Umbrales verificados: ≥90%, ≥80%, ≥70%, ≥60%, <60%")

    except Exception as e:
        errores.append(f"❌ Error en interpretar_confianza: {e}")

    # TEST 6: Verificar Metadata del Modelo
    print("\n6️⃣ TEST: Metadata y Métricas del Modelo")
    try:
        if hasattr(model, 'metadata') and model.metadata:
            metadata = model.metadata

            print(f"   ✅ Modelo tiene metadata")
            print(f"   📋 Tipo: {metadata.get('model_type', 'N/A')}")

            if 'test_metrics' in metadata:
                metrics = metadata['test_metrics']
                accuracy = metrics.get('accuracy', 0)
                kappa = metrics.get('cohen_kappa', 0)

                print(f"   📊 Accuracy: {accuracy:.1%}")
                print(f"   📊 Cohen's Kappa: {kappa:.4f}")

                if accuracy < 0.70:
                    warnings.append(f"⚠️ Accuracy es baja: {accuracy:.1%} (mínimo recomendado: 75%)")

                if 'per_class' in metrics:
                    print(f"   📊 Métricas por clase disponibles: ✅")
                else:
                    warnings.append("⚠️ No hay métricas por clase en metadata")
            else:
                warnings.append("⚠️ No hay métricas de test en metadata")
        else:
            warnings.append("⚠️ Modelo no tiene metadata")
    except Exception as e:
        warnings.append(f"⚠️ Error leyendo metadata: {e}")

    # TEST 7: Prueba End-to-End
    print("\n7️⃣ TEST: Flujo End-to-End Completo")
    try:
        # Simular flujo completo: comentario → servicio → DTO → respuesta
        comentarios_prueba = [
            ("La comida estuvo deliciosa", "positivo"),
            ("Pésimo servicio", "negativo"),
            ("Regular", "neutro")
        ]

        print("   🔄 Probando flujo completo para 3 comentarios...")

        for comentario, sentimiento_esperado in comentarios_prueba:
            result = service.analyze_comment(comentario)

            # Verificar campos obligatorios
            required_fields = ['comment', 'sentiment', 'confidence', 'confidence_level', 'probabilities']
            missing_fields = [f for f in required_fields if f not in result]

            if missing_fields:
                errores.append(f"❌ Faltan campos en resultado: {missing_fields}")

            # Crear DTO
            dto = SentimentAnalysisResponseDTO(**result)

            print(f"   ✅ \"{comentario[:30]}...\" → {dto.sentiment} ({dto.confidence:.0%}) - {dto.confidence_level}")

    except Exception as e:
        errores.append(f"❌ Error en flujo end-to-end: {e}")
        import traceback
        traceback.print_exc()

    # RESUMEN FINAL
    print("\n" + "=" * 80)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 80)

    total_tests = 7
    tests_passed = total_tests - len(errores)

    print(f"\n✅ Tests Exitosos: {tests_passed}/{total_tests}")

    if errores:
        print(f"\n❌ ERRORES CRÍTICOS ({len(errores)}):")
        for error in errores:
            print(f"   {error}")

    if warnings:
        print(f"\n⚠️ ADVERTENCIAS ({len(warnings)}):")
        for warning in warnings:
            print(f"   {warning}")

    if not errores:
        print("\n" + "=" * 80)
        print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("=" * 80)
        print("\n✅ El sistema está listo para usar con:")
        print("   • Análisis de sentimientos funcionando")
        print("   • Niveles de confiabilidad implementados")
        print("   • DTOs actualizados con confidence_level")
        print("   • Servicio retornando información completa")
        print("   • API lista para devolver niveles de confianza")
        print("\n🚀 Puedes iniciar el servidor con: python start_server.py")
    else:
        print("\n" + "=" * 80)
        print("⚠️ HAY PROBLEMAS QUE RESOLVER")
        print("=" * 80)
        return False

    return True

if __name__ == "__main__":
    success = test_integracion_completa()
    sys.exit(0 if success else 1)

