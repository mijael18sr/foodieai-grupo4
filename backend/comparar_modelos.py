"""
Comparación de Modelos: Original vs Gastronómico Optimizado
Muestra las métricas exactas de ambos modelos
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print(" COMPARACIÓN DE MODELOS DE SENTIMIENTOS")
print("=" * 80)

try:
    from src.ml.models import SentimentAnalysisModel

    modelos = [
        ("sentiment_model.pkl", "MODELO ACTUAL EN USO"),
        ("sentiment_model_gastro_optimized.pkl", "MODELO GASTRONÓMICO OPTIMIZADO")
    ]

    resultados = {}

    for modelo_file, nombre in modelos:
        print(f"\n{'=' * 80}")
        print(f" {nombre}")
        print(f" Archivo: {modelo_file}")
        print("=" * 80)

        model_path = project_root / "data" / "models" / modelo_file

        if not model_path.exists():
            print(f" No encontrado")
            continue

        try:
            model = SentimentAnalysisModel()
            model.load(str(model_path))
            print(f" Cargado correctamente")

            # Información básica
            if hasattr(model, 'metadata') and model.metadata:
                metadata = model.metadata

                print(f"\n INFORMACIÓN BÁSICA:")
                print(f" Tipo: {metadata.get('model_type', 'N/A')}")
                print(f" Vocabulario: {metadata.get('vocab_size', 0):,} términos")
                print(f" Muestras: {metadata.get('n_samples', 0):,}")

                # Métricas de test
                if 'test_metrics' in metadata:
                    metrics = metadata['test_metrics']

                    accuracy = metrics.get('accuracy', 0)
                    kappa = metrics.get('cohen_kappa', 0)
                    f1_weighted = metrics.get('f1_weighted', 0)
                    f1_macro = metrics.get('f1_macro', 0)

                    print(f"\n MÉTRICAS PRINCIPALES:")
                    print(f" Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
                    print(f" Cohen's Kappa: {kappa:.4f}")
                    print(f" F1-Score (weighted): {f1_weighted:.4f} ({f1_weighted*100:.2f}%)")
                    print(f" F1-Score (macro): {f1_macro:.4f} ({f1_macro*100:.2f}%)")

                    # Guardar para comparación
                    resultados[nombre] = {
                        'accuracy': accuracy,
                        'kappa': kappa,
                        'f1_weighted': f1_weighted,
                        'f1_macro': f1_macro
                    }

                    # Métricas por clase
                    if 'per_class' in metrics:
                        print(f"\n MÉTRICAS POR CLASE:")

                        for clase in ['positivo', 'neutro', 'negativo']:
                            if clase in metrics['per_class']:
                                cm = metrics['per_class'][clase]
                                print(f"\n {clase.upper()}:")
                                print(f" Precision: {cm['precision']:.4f} ({cm['precision']*100:.1f}%)")
                                print(f" Recall: {cm['recall']:.4f} ({cm['recall']*100:.1f}%)")
                                print(f" F1-Score: {cm['f1-score']:.4f} ({cm['f1-score']*100:.1f}%)")
                                print(f" Support: {cm['support']} muestras")
                else:
                    print(f"\n Sin métricas de test guardadas")
            else:
                print(f"\n Sin metadata")

        except Exception as e:
            print(f" Error cargando: {e}")

    # COMPARACIÓN DIRECTA
    if len(resultados) == 2:
        print(f"\n{'=' * 80}")
        print(" COMPARACIÓN DIRECTA")
        print("=" * 80)

        modelo1_nombre, modelo2_nombre = list(resultados.keys())
        modelo1 = resultados[modelo1_nombre]
        modelo2 = resultados[modelo2_nombre]

        print(f"\n┌────────────────────────┬──────────────────┬──────────────────┬─────────────┐")
        print(f"│ Métrica │ Modelo Actual │ Modelo Optimizado│ Diferencia │")
        print(f"├────────────────────────┼──────────────────┼──────────────────┼─────────────┤")

        metrics_compare = [
            ('Accuracy', 'accuracy'),
            ("Cohen's Kappa", 'kappa'),
            ('F1-Score (weighted)', 'f1_weighted'),
            ('F1-Score (macro)', 'f1_macro')
        ]

        for label, key in metrics_compare:
            val1 = modelo1[key] * 100
            val2 = modelo2[key] * 100
            diff = val2 - val1
            diff_str = f"+{diff:.2f}%" if diff > 0 else f"{diff:.2f}%"

            print(f"│ {label:22s} │ {val1:15.2f}% │ {val2:15.2f}% │ {diff_str:>11s} │")

        print(f"└────────────────────────┴──────────────────┴──────────────────┴─────────────┘")

        # RECOMENDACIÓN
        print(f"\n{'=' * 80}")
        print(" RECOMENDACIÓN")
        print("=" * 80)

        acc_actual = modelo1['accuracy']
        acc_optimizado = modelo2['accuracy']

        if acc_optimizado > acc_actual + 0.02:
            print(f"\n USAR MODELO GASTRONÓMICO OPTIMIZADO")
            print(f" • Accuracy: {acc_optimizado*100:.2f}% (mejora de {(acc_optimizado-acc_actual)*100:.2f}%)")
            print(f" • Mejor rendimiento general")
            print(f"\n Para activar, ejecuta:")
            print(f" copy data\\models\\sentiment_model_gastro_optimized.pkl data\\models\\sentiment_model.pkl")
        elif acc_actual > acc_optimizado + 0.02:
            print(f"\n MANTENER MODELO ACTUAL")
            print(f" • Accuracy: {acc_actual*100:.2f}% (mejor que optimizado)")
            print(f" • El modelo actual es superior")
        else:
            print(f"\n MODELOS SIMILARES")
            print(f" • Diferencia: {abs(acc_optimizado-acc_actual)*100:.2f}%")
            print(f" • Considera A/B testing")
            print(f" • Modelo Actual: {acc_actual*100:.2f}%")
            print(f" • Modelo Optimizado: {acc_optimizado*100:.2f}%")

    # PRUEBA CON EJEMPLOS REALES
    print(f"\n{'=' * 80}")
    print(" PRUEBA CON EJEMPLOS REALES")
    print("=" * 80)

    ejemplos = [
        "La comida estuvo deliciosa y el servicio excelente",
        "Se atienden todos los domingos",
        "Pésimo servicio, muy lento",
        "Regular, nada especial"
    ]

    for modelo_file, nombre in modelos:
        model_path = project_root / "data" / "models" / modelo_file
        if model_path.exists():
            print(f"\n{'─' * 80}")
            print(f" {nombre}")
            print("─" * 80)

            model = SentimentAnalysisModel()
            model.load(str(model_path))

            for ejemplo in ejemplos:
                result = model.predict_single(ejemplo)
                sentiment = result['sentiment'].upper()
                confidence = result['confidence']

                # Determinar nivel
                if confidence >= 0.90:
                    nivel = "MUY CONFIABLE"
                elif confidence >= 0.80:
                    nivel = "CONFIABLE"
                elif confidence >= 0.70:
                    nivel = "MODERADO"
                elif confidence >= 0.60:
                    nivel = "BAJA CONFIANZA"
                else:
                    nivel = "INDETERMINADO"

                print(f"\n \"{ejemplo}\"")
                print(f" → {sentiment} ({confidence:.1%}) - {nivel}")

    print(f"\n{'=' * 80}")
    print(" COMPARACIÓN COMPLETADA")
    print("=" * 80)

except Exception as e:
    print(f"\n ERROR: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona ENTER para salir...")

