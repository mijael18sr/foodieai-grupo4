"""
Script de Verificación: Evaluar que el modelo esté listo para usarse
Autor: Sistema ML - Restaurant Recommender
Fecha: 2025-01-05
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

print("="*80)
print("VERIFICACIÓN DE PREREQUISITES PARA EVALUACIÓN DEL MODELO")
print("="*80)

# 1. Verificar estructura de directorios
print("\n[1/5] Verificando estructura de directorios...")
dirs_to_check = [
    backend_dir / 'data' / 'models',
    backend_dir / 'data' / 'processed',
    backend_dir / 'docs' / 'figures',
    backend_dir / 'notebooks'
]

for dir_path in dirs_to_check:
    if dir_path.exists():
        print(f" {dir_path.relative_to(backend_dir)}")
    else:
        print(f" {dir_path.relative_to(backend_dir)} - NO EXISTE")

# 2. Verificar que exista el modelo
print("\n[2/5] Verificando modelo entrenado...")
modelo_path = backend_dir / 'data' / 'models' / 'sentiment_model.pkl'

if modelo_path.exists():
    print(f" sentiment_model.pkl existe")
    file_size = modelo_path.stat().st_size / (1024 * 1024)
    print(f" Tamaño: {file_size:.2f} MB")
else:
    print(f" sentiment_model.pkl NO EXISTE")
    print(f" Debes entrenar el modelo primero")

# 3. Verificar dataset procesado
print("\n[3/5] Verificando dataset procesado...")
dataset_path = backend_dir / 'data' / 'processed' / 'modelo_limpio.csv'

if dataset_path.exists():
    print(f" modelo_limpio.csv existe")
    file_size = dataset_path.stat().st_size / (1024 * 1024)
    print(f" Tamaño: {file_size:.2f} MB")

    # Contar líneas aproximadas
    try:
        import pandas as pd
        df = pd.read_csv(dataset_path, nrows=5)
        print(f" Columnas: {', '.join(df.columns.tolist())}")
    except Exception as e:
        print(f" Error al leer dataset: {e}")
else:
    print(f" modelo_limpio.csv NO EXISTE")
    print(f" Debes ejecutar el notebook completo primero")

# 4. Verificar librerías necesarias
print("\n[4/5] Verificando librerías necesarias...")
libraries = [
    'pandas',
    'numpy',
    'sklearn',
    'matplotlib',
    'seaborn',
    'pickle'
]

missing_libs = []
for lib in libraries:
    try:
        if lib == 'sklearn':
            __import__('sklearn')
        else:
            __import__(lib)
        print(f" {lib}")
    except ImportError:
        print(f" {lib} - NO INSTALADA")
        missing_libs.append(lib)

if missing_libs:
    print(f"\n Instala las librerías faltantes con:")
    print(f" pip install {' '.join(missing_libs)}")

# 5. Intentar cargar el modelo
print("\n[5/5] Intentando cargar el modelo...")
if modelo_path.exists():
    try:
        import pickle
        with open(modelo_path, 'rb') as f:
            modelo = pickle.load(f)

        print(f" Modelo cargado exitosamente")
        print(f" Tipo: {type(modelo).__name__}")

        # Verificar atributos del modelo
        if hasattr(modelo, 'is_trained'):
            print(f" Entrenado: {modelo.is_trained}")

        if hasattr(modelo, 'metadata'):
            metadata = modelo.metadata
            print(f" Metadata:")
            for key, value in metadata.items():
                if isinstance(value, (int, float, str, bool)):
                    print(f" • {key}: {value}")
                elif isinstance(value, dict):
                    print(f" • {key}: {dict(list(value.items())[:3])}")
                elif isinstance(value, list):
                    print(f" • {key}: {value[:3]}")

    except Exception as e:
        print(f" Error al cargar el modelo: {e}")
else:
    print(f" Saltando (modelo no existe)")

# Resumen final
print("\n" + "="*80)
print("RESUMEN DE VERIFICACIÓN")
print("="*80)

all_checks = []
all_checks.append(("Estructura de directorios", all(d.exists() for d in dirs_to_check)))
all_checks.append(("Modelo entrenado", modelo_path.exists()))
all_checks.append(("Dataset procesado", dataset_path.exists()))
all_checks.append(("Librerías instaladas", len(missing_libs) == 0))

if modelo_path.exists():
    try:
        import pickle
        with open(modelo_path, 'rb') as f:
            modelo = pickle.load(f)
        all_checks.append(("Modelo cargable", True))
    except:
        all_checks.append(("Modelo cargable", False))

print()
for check_name, status in all_checks:
    status_icon = "" if status else ""
    print(f"{status_icon} {check_name}")

# Conclusión
print("\n" + "="*80)
if all(status for _, status in all_checks):
    print(" ¡TODO LISTO! Puedes ejecutar la sección de evaluación del notebook.")
else:
    print(" HAY PROBLEMAS. Revisa los items marcados con arriba.")
    print("\n Pasos sugeridos:")
    print(" 1. Ejecuta el notebook completo hasta crear 'modelo_limpio.csv'")
    print(" 2. Entrena el modelo si no existe 'sentiment_model.pkl'")
    print(" 3. Instala las librerías faltantes con pip")

print("="*80)

