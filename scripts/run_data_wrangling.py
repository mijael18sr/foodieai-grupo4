
"""
Data Wrangling Script
Script para ejecutar la limpieza completa de datos.

Uso:
    python scripts/run_data_wrangling.py
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import re
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("🧹 DATA WRANGLING - LIMPIEZA DE DATOS")
print("=" * 70)
print()

# ============================================
# CONFIGURACIÓN
# ============================================

RAW_DATA_PATH = project_root / "data" / "raw" / "restaurant_metadata.csv"
OUTPUT_DIR = project_root / "data" / "processed"

# Crear directorio de salida si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# 1. CARGAR DATOS
# ============================================

print("📂 PASO 1: Cargando datos originales...")
print("-" * 70)

if not RAW_DATA_PATH.exists():
    print(f"❌ ERROR: No se encuentra el archivo {RAW_DATA_PATH}")
    print("   Por favor copia restaurant_metadata.csv a data/raw/")
    sys.exit(1)

df = pd.read_csv(RAW_DATA_PATH)
print(f"✅ Datos cargados: {len(df)} registros, {len(df.columns)} columnas")
print()

# ============================================
# 2. ELIMINAR DUPLICADOS
# ============================================

print("🔍 PASO 2: Eliminando duplicados...")
print("-" * 70)

duplicados_antes = len(df)
df = df.drop_duplicates(subset=['title', 'address', 'lat', 'long'], keep='first')
eliminados_duplicados = duplicados_antes - len(df)
print(f"✅ Duplicados eliminados: {eliminados_duplicados}")
print(f"   Registros restantes: {len(df)}")
print()

# ============================================
# 3. LIMPIAR COLUMNAS DE TEXTO
# ============================================

print("🧹 PASO 3: Limpiando columnas de texto...")
print("-" * 70)

def limpiar_texto(texto):
    if pd.isna(texto):
        return texto
    texto = str(texto).strip()
    texto = re.sub(r'\s+', ' ', texto)  # Múltiples espacios a uno
    return texto if texto else np.nan

columnas_texto = ['title', 'category', 'address', 'district', 'domain']
for col in columnas_texto:
    if col in df.columns:
        df[col] = df[col].apply(limpiar_texto)

print("✅ Texto limpiado y espacios normalizados")
print()

# ============================================
# 4. VALIDAR Y LIMPIAR TELÉFONOS
# ============================================

print("📞 PASO 4: Validando teléfonos...")
print("-" * 70)

def validar_telefono(phone):
    if pd.isna(phone):
        return np.nan
    phone = str(phone).strip()
    # Debe tener al menos 7 dígitos
    digitos = re.sub(r'\D', '', phone)
    return phone if len(digitos) >= 7 else np.nan

if 'phoneNumber' in df.columns:
    df['phoneNumber'] = df['phoneNumber'].apply(validar_telefono)
if 'completePhoneNumber' in df.columns:
    df['completePhoneNumber'] = df['completePhoneNumber'].apply(validar_telefono)

telefonos_invalidos = df['phoneNumber'].isna().sum() if 'phoneNumber' in df.columns else 0
print(f"✅ Teléfonos validados (inválidos marcados: {telefonos_invalidos})")
print()

# ============================================
# 5. VALIDAR URLs
# ============================================

print("🌐 PASO 5: Validando URLs...")
print("-" * 70)

def validar_url(url):
    if pd.isna(url):
        return np.nan
    url = str(url).strip()
    if url.startswith('http://') or url.startswith('https://'):
        return url
    return np.nan

if 'url' in df.columns:
    df['url'] = df['url'].apply(validar_url)
if 'url_place' in df.columns:
    df['url_place'] = df['url_place'].apply(validar_url)

urls_invalidas = df['url'].isna().sum() if 'url' in df.columns else 0
print(f"✅ URLs validadas (inválidas marcadas: {urls_invalidas})")
print()

# ============================================
# 6. LIMPIAR RATINGS (STARS Y REVIEWS)
# ============================================

print("⭐ PASO 6: Limpiando ratings...")
print("-" * 70)

# Stars debe estar entre 0 y 5
df.loc[(df['stars'] < 0) | (df['stars'] > 5), 'stars'] = np.nan

# Reviews debe ser positivo
df.loc[df['reviews'] < 0, 'reviews'] = np.nan

# Rellenar valores faltantes con la mediana
df['stars'] = df['stars'].fillna(df['stars'].median())
df['reviews'] = df['reviews'].fillna(0)

print(f"✅ Stars válidos: rango 0-5, mediana={df['stars'].median():.2f}")
print(f"✅ Reviews limpios: no negativos")
print()

# ============================================
# 7. VALIDAR COORDENADAS GEOGRÁFICAS
# ============================================

print("🗺️  PASO 7: Validando coordenadas...")
print("-" * 70)

# Rangos válidos para Perú (aproximadamente)
lat_min, lat_max = -18.5, -0.0
long_min, long_max = -81.5, -68.5

# Marcar coordenadas fuera de rango
coords_invalidas = (
    (df['lat'] < lat_min) | (df['lat'] > lat_max) |
    (df['long'] < long_min) | (df['long'] > long_max) |
    df['lat'].isna() | df['long'].isna()
)

print(f"✅ Coordenadas fuera de Perú: {coords_invalidas.sum()}")

# Rellenar con mediana
if coords_invalidas.sum() > 0:
    df.loc[coords_invalidas, 'lat'] = df['lat'].median()
    df.loc[coords_invalidas, 'long'] = df['long'].median()
print()

# ============================================
# 8. DETECTAR ANOMALÍAS CON MACHINE LEARNING
# ============================================

print("🤖 PASO 8: Detectando anomalías con ML (Isolation Forest)...")
print("-" * 70)

# Preparar datos numéricos
datos_ml = df[['stars', 'reviews', 'lat', 'long']].copy()
datos_ml = datos_ml.fillna(datos_ml.median())

# Normalizar
scaler = StandardScaler()
datos_scaled = scaler.fit_transform(datos_ml)

# Detectar anomalías
iso_forest = IsolationForest(
    contamination=0.05,  # Asume 5% de anomalías
    random_state=42,
    n_estimators=100
)
anomalias = iso_forest.fit_predict(datos_scaled)

df['es_anomalia'] = anomalias == -1
anomalias_detectadas = df['es_anomalia'].sum()
print(f"✅ Anomalías detectadas con ML: {anomalias_detectadas} ({anomalias_detectadas/len(df)*100:.1f}%)")
print()

# ============================================
# 9. ELIMINAR REGISTROS INCOMPLETOS CRÍTICOS
# ============================================

print("❌ PASO 9: Eliminando registros incompletos críticos...")
print("-" * 70)

# Debe tener al menos título y ubicación
registros_criticos = df[
    df['title'].isna() |
    (df['lat'].isna() & df['long'].isna())
]

df_limpio = df[
    df['title'].notna() &
    (df['lat'].notna() | df['long'].notna())
].copy()

print(f"✅ Registros sin título/ubicación eliminados: {len(registros_criticos)}")
print(f"   Registros válidos: {len(df_limpio)}")
print()

# ============================================
# 10. CREAR MÉTRICAS DE CALIDAD
# ============================================

print("📈 PASO 10: Creando métricas de calidad...")
print("-" * 70)

df_limpio['score_calidad'] = 0
if 'phoneNumber' in df_limpio.columns:
    df_limpio['score_calidad'] += df_limpio['phoneNumber'].notna().astype(int) * 20
if 'url' in df_limpio.columns:
    df_limpio['score_calidad'] += df_limpio['url'].notna().astype(int) * 20
df_limpio['score_calidad'] += (df_limpio['reviews'] > 0).astype(int) * 20
df_limpio['score_calidad'] += (df_limpio['stars'] >= 3.5).astype(int) * 20
if 'category' in df_limpio.columns:
    df_limpio['score_calidad'] += df_limpio['category'].notna().astype(int) * 20

print(f"✅ Score promedio de calidad: {df_limpio['score_calidad'].mean():.1f}/100")
print()

# ============================================
# RESUMEN FINAL
# ============================================

print("=" * 70)
print("✅ RESUMEN DE LIMPIEZA COMPLETADA")
print("=" * 70)
print(f"Registros originales:        {len(df)}")
print(f"Duplicados eliminados:       {eliminados_duplicados}")
print(f"Registros incompletos:       {len(registros_criticos)}")
print(f"Anomalías detectadas:        {df_limpio['es_anomalia'].sum()}")
print(f"Registros limpios finales:   {len(df_limpio)}")
print(f"\nTasa de limpieza: {(len(df_limpio)/len(df)*100):.1f}%")
print()

# ============================================
# ANÁLISIS DE COMPLETITUD
# ============================================

print("=" * 70)
print("📊 COMPLETITUD DE DATOS LIMPIOS")
print("=" * 70)
for col in df_limpio.columns:
    if col not in ['es_anomalia', 'score_calidad']:
        completitud = (df_limpio[col].notna().sum() / len(df_limpio) * 100)
        print(f"{col:25s}: {completitud:5.1f}%")
print()

# ============================================
# GUARDAR DATASETS LIMPIOS
# ============================================

print("💾 Guardando datasets limpios...")
print("-" * 70)

# Dataset con anomalías marcadas
output_path_1 = OUTPUT_DIR / 'restaurantes_limpio.csv'
df_limpio.to_csv(output_path_1, index=False)
print(f"✅ {output_path_1}")

# Dataset sin anomalías
df_sin_anomalias = df_limpio[~df_limpio['es_anomalia']].copy()
output_path_2 = OUTPUT_DIR / 'restaurantes_sin_anomalias.csv'
df_sin_anomalias.drop('es_anomalia', axis=1, errors='ignore').to_csv(output_path_2, index=False)
print(f"✅ {output_path_2}")
print(f"   ({len(df_sin_anomalias)} registros)")

# Dataset de alta calidad (score > 60)
df_alta_calidad = df_limpio[df_limpio['score_calidad'] >= 60].copy()
output_path_3 = OUTPUT_DIR / 'restaurantes_alta_calidad.csv'
df_alta_calidad.to_csv(output_path_3, index=False)
print(f"✅ {output_path_3}")
print(f"   ({len(df_alta_calidad)} registros)")

print()
print("=" * 70)
print("🎉 ¡LIMPIEZA COMPLETADA EXITOSAMENTE!")
print("=" * 70)
print()
print("📁 Archivos generados:")
print(f"   1. restaurantes_limpio.csv         ({len(df_limpio)} registros)")
print(f"   2. restaurantes_sin_anomalias.csv  ({len(df_sin_anomalias)} registros)")
print(f"   3. restaurantes_alta_calidad.csv   ({len(df_alta_calidad)} registros)")
print()
print("🚀 Siguiente paso: python scripts/run_eda.py")