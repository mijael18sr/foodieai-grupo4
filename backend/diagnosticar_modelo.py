"""
Diagnóstico completo del modelo - Identificar por qué no funciona correctamente
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print(" DIAGNÓSTICO DEL MODELO DE SENTIMIENTOS")
print("=" * 80)

try:
    from src.ml.models import SentimentAnalysisModel
    import numpy as np

    # Cargar modelo
    model = SentimentAnalysisModel()
    model_path = project_root / "data" / "models" / "sentiment_model.pkl"
    model.load(str(model_path))

    print("\n Modelo cargado correctamente")
    print(f" Archivo: {model_path.name}")

    # TEST 1: Verificar componentes del modelo
    print("\n" + "=" * 80)
    print("TEST 1: Componentes del Modelo")
    print("=" * 80)

    print(f" Vectorizer: {type(model.vectorizer).__name__}")
    print(f" Classifier: {type(model.classifier).__name__}")
    print(f" Is Trained: {model.is_trained}")
    print(f" Vocabulario: {len(model.vectorizer.vocabulary_):,} términos")

    # TEST 2: Verificar clases del clasificador
    print("\n" + "=" * 80)
    print("TEST 2: Clases del Clasificador")
    print("=" * 80)

    if hasattr(model.classifier, 'classes_'):
        classes = model.classifier.classes_
        print(f" Clases detectadas: {list(classes)}")

        # Verificar orden de clases
        expected_order = ['negativo', 'neutro', 'positivo']
        if list(classes) != expected_order:
            print(f" PROBLEMA: Orden de clases incorrecto")
            print(f" Esperado: {expected_order}")
            print(f" Actual: {list(classes)}")

    # TEST 3: Verificar preprocesamiento
    print("\n" + "=" * 80)
    print("TEST 3: Pipeline de Preprocesamiento")
    print("=" * 80)

    test_text = "La comida estuvo deliciosa"
    print(f" Texto original: \"{test_text}\"")

    # Verificar si existe método de preprocesamiento
    if hasattr(model, 'preprocess'):
        processed = model.preprocess(test_text)
        print(f" Texto procesado: \"{processed}\"")
    else:
        print(" No hay método preprocess() definido")

    # TEST 4: Verificar predicciones raw
    print("\n" + "=" * 80)
    print("TEST 4: Predicciones Raw del Clasificador")
    print("=" * 80)

    test_cases = [
        "La comida estuvo deliciosa y el servicio excelente",
        "Pésimo servicio, muy lento",
        "Regular, nada especial"
    ]

    for test in test_cases:
        print(f"\n \"{test}\"")

        # Vectorizar
        X = model.vectorizer.transform([test])

        # Predicción
        pred_class = model.classifier.predict(X)[0]

        # Probabilidades
        if hasattr(model.classifier, 'predict_proba'):
            proba = model.classifier.predict_proba(X)[0]
            classes = model.classifier.classes_

            print(f" Predicción raw: {pred_class}")
            print(f" Probabilidades:")
            for cls, prob in zip(classes, proba):
                print(f" {cls}: {prob:.4f} ({prob*100:.1f}%)")
        else:
            print(f" Predicción: {pred_class}")

    # TEST 5: Verificar términos importantes del vocabulario
    print("\n" + "=" * 80)
    print("TEST 5: Términos Importantes en el Vocabulario")
    print("=" * 80)

    vocab = model.vectorizer.vocabulary_

    palabras_clave = {
        'positivas': ['delicioso', 'deliciosa', 'excelente', 'rico', 'bueno', 'sabroso'],
        'negativas': ['pésimo', 'malo', 'horrible', 'terrible', 'feo', 'desagradable'],
        'neutras': ['regular', 'normal', 'aceptable', 'promedio']
    }

    for tipo, palabras in palabras_clave.items():
        print(f"\n {tipo.upper()}:")
        for palabra in palabras:
            if palabra in vocab:
                print(f" '{palabra}' está en vocabulario")
            else:
                print(f" ✗ '{palabra}' NO está en vocabulario")

    # TEST 6: Verificar si el modelo usa preprocesamiento correcto
    print("\n" + "=" * 80)
    print("TEST 6: Método predict_single()")
    print("=" * 80)

    for test in test_cases:
        result = model.predict_single(test)
        print(f"\n \"{test}\"")
        print(f" Sentimiento: {result['sentiment']}")
        print(f" Confianza: {result['confidence']:.1%}")
        print(f" Texto procesado: \"{result['text_processed']}\"")

    # TEST 7: Comparar con modelo de backup si existe
    print("\n" + "=" * 80)
    print("TEST 7: Modelos Disponibles")
    print("=" * 80)

    models_dir = project_root / "data" / "models"
    pkl_files = list(models_dir.glob("sentiment_model*.pkl"))

    print(f"\n Modelos encontrados: {len(pkl_files)}")
    for pkl_file in pkl_files:
        size_kb = pkl_file.stat().st_size / 1024
        print(f" • {pkl_file.name} ({size_kb:.2f} KB)")

    # DIAGNÓSTICO FINAL
    print("\n" + "=" * 80)
    print(" DIAGNÓSTICO Y RECOMENDACIONES")
    print("=" * 80)

    problemas = []

    # Verificar accuracy
    if hasattr(model, 'metadata') and model.metadata:
        accuracy = model.metadata.get('test_metrics', {}).get('accuracy', 0)
        if accuracy < 0.75:
            problemas.append(f"Accuracy bajo: {accuracy*100:.1f}% (mínimo recomendado: 75%)")

    # Verificar predicciones incorrectas
    result1 = model.predict_single("La comida estuvo deliciosa")
    result2 = model.predict_single("Pésimo servicio")

    if result1['sentiment'] != 'positivo':
        problemas.append(f"Predicción incorrecta: 'deliciosa' → {result1['sentiment']} (debería ser 'positivo')")

    if result2['sentiment'] != 'negativo':
        problemas.append(f"Predicción incorrecta: 'pésimo' → {result2['sentiment']} (debería ser 'negativo')")

    if problemas:
        print("\n PROBLEMAS DETECTADOS:")
        for i, problema in enumerate(problemas, 1):
            print(f" {i}. {problema}")

        print("\n SOLUCIONES RECOMENDADAS:")
        print(" 1. Reentrenar el modelo con datos de mejor calidad")
        print(" 2. Verificar que el preprocesamiento no elimine palabras importantes")
        print(" 3. Revisar el balance de clases en los datos de entrenamiento")
        print(" 4. Considerar usar un modelo más robusto (SVM, Random Forest)")
        print(" 5. Aumentar el dataset con más ejemplos claros")
    else:
        print("\n El modelo parece estar funcionando correctamente")

    print("\n" + "=" * 80)

except Exception as e:
    print(f"\n ERROR: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona ENTER para salir...")

