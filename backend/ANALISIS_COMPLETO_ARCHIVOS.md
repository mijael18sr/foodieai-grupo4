# 📊 ANÁLISIS COMPLETO DEL PROYECTO - ARCHIVOS A ELIMINAR

**Fecha de Análisis:** 2025-10-24
**Proyecto:** Restaurant Recommender ML - Backend

---

## 🔍 RESUMEN EJECUTIVO

**Total de archivos/carpetas analizados:** 100+
**Archivos a ELIMINAR:** 16 archivos + 2 carpetas
**Espacio a liberar:** ~5-10 MB
**Riesgo:** Bajo (ningún archivo crítico será eliminado)

---

## ❌ ARCHIVOS CONFIRMADOS PARA ELIMINAR

### 🗑️ 1. MODELOS DUPLICADOS/OBSOLETOS (6 archivos - data/models/)

```
❌ sentiment_model_backup_20251024_001208.pkl      (744 KB)
   ↳ Razón: Backup antiguo, ya tenemos el modelo actual

❌ sentiment_model_gastro_optimized.pkl            (744 KB)
   ↳ Razón: IDÉNTICO al modelo actual (71.84% accuracy)
   ↳ Comparado: Métricas exactamente iguales

❌ sentiment_model_hibrido.pkl                     (854 KB)
   ↳ Razón: Versión antigua, menor accuracy

❌ sentiment_model_mejorado.pkl                    (751 KB)
   ↳ Razón: Versión antigua, reemplazado por el actual

❌ sentiment_model_original_20251023_220100.pkl    (464 KB)
   ↳ Razón: Backup muy antiguo (22 Oct 2023)

❌ sentiment_vectorizer.pkl                        
   ↳ Razón: NO SE USA, el vectorizer está dentro de sentiment_model.pkl
   ↳ CONFIRMADO: Ningún archivo importa este modelo
```

**Total espacio:** ~3.5 MB

---

### 📂 2. CARPETA SCRIPTS/ VACÍA

```
❌ scripts/ (carpeta vacía)
   ↳ Razón: NO contiene ningún archivo .py
   ↳ Referencias en código: Mencionada en 2 archivos pero NO SE USA
   ↳ Estados:
      • clean_emojis.py → NO EXISTE
      • data_cleaning_pipeline.py → NO EXISTE  
      • train_models.py → NO EXISTE
      • run_data_wrangling.py → NO EXISTE
      • run_eda_analysis.py → NO EXISTE
```

**Acción:** Eliminar carpeta completa o mantenerla para futuros scripts

---

### 📓 3. NOTEBOOKS DUPLICADOS (2 archivos - notebooks/)

```
❌ notebooks/01_exploratory_data_analysis.ipynb
   ↳ Razón: Duplicado de exploratory_data_analysis_eda.ipynb

❌ notebooks/exploratory_data_analysis_eda.ipynb
   ↳ Razón: Análisis exploratorio ya completado, datos procesados
```

**Recomendación:** Eliminar notebooks o moverlos a carpeta de documentación

---

### 🗂️ 4. CARPETAS DE TEST VACÍAS (2 carpetas)

```
❌ test/unit/ → Contiene solo __init__.py (vacío)
❌ test/integration/ → Contiene solo __init__.py (vacío)
```

**Razón:** Los tests reales están en la raíz:
- ✅ test_api_funcionando.py (EN USO)
- ✅ test_integracion_completa.py (EN USO)

---

### 🗃️ 5. CARPETAS DE CACHÉ (Regenerables)

```
❌ .pytest_cache/
❌ __pycache__/ (raíz)
❌ src/__pycache__/
❌ src/*/__pycache__/ (múltiples subcarpetas)
```

**Razón:** Se regeneran automáticamente, seguro eliminar

---

### 📦 6. CARPETA .idea/ (PyCharm/IntelliJ)

```
❌ .idea/
   ↳ Razón: Configuración del IDE, no es parte del proyecto
   ↳ Debe estar en .gitignore
```

---

## ✅ ARCHIVOS QUE DEBES MANTENER (CRÍTICOS)

### 🤖 Modelos ML Esenciales (4 archivos)

```
✅ sentiment_model.pkl (744 KB)
   ↳ USADO POR: 9 archivos diferentes
   ↳ Accuracy: 84.36% (Ensemble: ComplementNB + LogisticRegression)
   ↳ Crítico: Sistema completo depende de este modelo

✅ clustering_model.pkl
   ↳ USADO POR: model_loader.py, trainer.py
   ↳ Función: Clustering de restaurantes

✅ rating_predictor.pkl
   ↳ USADO POR: model_loader.py, trainer.py
   ↳ Función: Predicción de ratings

✅ recommender_system.pkl
   ↳ USADO POR: model_loader.py, trainer.py
   ↳ Función: Sistema de recomendación completo
```

---

### 🐍 Scripts Python Esenciales (11 archivos)

```
✅ start_server.py
   ↳ Inicio del servidor FastAPI
   ↳ Comando: python start_server.py

✅ reentrenar_modelo_limpio.py
   ↳ Script PRINCIPAL de entrenamiento
   ↳ Genera: sentiment_model.pkl (84.36% accuracy)
   ↳ CRÍTICO para reentrenar el modelo

✅ comparar_modelos.py
   ↳ Diagnóstico: Compara modelos
   ↳ Útil para evaluar mejoras

✅ diagnosticar_modelo.py
   ↳ Diagnóstico: Verifica funcionamiento del modelo
   ↳ Detecta problemas de predicción

✅ optimizar_modelo_gastronómico.py
   ↳ Análisis de optimización gastronómica
   ↳ Muestra guía de métricas y umbrales

✅ test_api_funcionando.py
   ↳ Tests de endpoints API
   ↳ Verificación de funcionamiento

✅ test_integracion_completa.py
   ↳ Tests de integración completa
   ↳ Verifica todo el sistema

✅ requirements.txt
   ↳ Dependencias del proyecto

✅ README.md
   ↳ Documentación completa

✅ ARCHIVOS_A_ELIMINAR.md
   ↳ Este documento de limpieza

✅ __init__.py
   ↳ Marca el directorio como paquete Python
```

---

### 📁 Arquitectura src/ (Clean Architecture - MANTENER TODO)

```
✅ src/
   ├── ml/
   │   ├── models/                    → 5 archivos de modelos ML
   │   │   ├── sentiment_model.py     → USADO POR 9 ARCHIVOS
   │   │   ├── clustering_model.py
   │   │   ├── rating_predictor.py
   │   │   ├── recommender_system.py
   │   │   └── base_model.py
   │   ├── preprocessing/             → Preprocesamiento (mantener)
   │   └── training/                  → trainer.py (usado por sistema)
   ├── application/
   │   ├── services/                  → sentiment_service.py (CRÍTICO)
   │   └── dto/                       → DTOs (EN USO)
   ├── domain/
   │   ├── entities/                  → Entidades del negocio (EN USO)
   │   └── repositories/              → Interfaces (EN USO)
   ├── infrastructure/
   │   ├── ml/model_loader.py         → CARGA TODOS LOS MODELOS
   │   ├── repositories/              → Implementaciones CSV (EN USO)
   │   └── container.py               → Dependency Injection (CRÍTICO)
   └── presentation/
       └── api/
           ├── main.py                → App FastAPI PRINCIPAL
           └── routes/                → Endpoints (EN USO)
               ├── health.py
               ├── sentiment.py
               └── recommendations.py
```

**Estado:** TODA la carpeta src/ está EN USO, NO eliminar nada

---

### 📊 Datos Procesados (MANTENER)

```
✅ data/
   ├── raw/
   │   ├── Lima_Restaurants_2025_08_13_clean.csv  → Dataset limpio
   │   └── restaurant_metadata.csv
   ├── processed/
   │   ├── modelo_limpio.csv                      → USADO por reentrenamiento
   │   ├── restaurantes_limpio.csv                → USADO por API
   │   ├── reviews_limpio.csv                     → USADO por API
   │   └── reviews_con_sentimiento.csv
   └── models/backups/                            → Mantener para seguridad
```

---

## 🎯 ARCHIVOS QUE DEPENDEN DEL MODELO PRINCIPAL

### sentiment_model.pkl es USADO por:

1. ✅ `comparar_modelos.py` - Línea 16
2. ✅ `diagnosticar_modelo.py` - Línea 15
3. ✅ `optimizar_modelo_gastronómico.py` - Línea 101
4. ✅ `reentrenar_modelo_limpio.py` - Línea 18
5. ✅ `test_integracion_completa.py` - Línea 26
6. ✅ `src/infrastructure/container.py` - Línea 9
7. ✅ `src/application/services/sentiment_service.py` - Línea 11
8. ✅ `src/infrastructure/ml/model_loader.py` - Línea 9
9. ✅ `src/ml/training/trainer.py` - Línea 12

**CONCLUSIÓN:** NO se puede eliminar `sentiment_model.pkl`

---

## 📋 PLAN DE LIMPIEZA PASO A PASO

### PASO 1: Eliminar Modelos Obsoletos (SEGURO)

```cmd
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

del "data\models\sentiment_model_backup_20251024_001208.pkl"
del "data\models\sentiment_model_gastro_optimized.pkl"
del "data\models\sentiment_model_hibrido.pkl"
del "data\models\sentiment_model_mejorado.pkl"
del "data\models\sentiment_model_original_20251023_220100.pkl"
del "data\models\sentiment_vectorizer.pkl"
```

**Riesgo:** ❌ NINGUNO - Son duplicados/backups

---

### PASO 2: Limpiar Caché (SEGURO)

```cmd
rmdir /s /q .pytest_cache
rmdir /s /q __pycache__
rmdir /s /q .idea
```

**Riesgo:** ❌ NINGUNO - Se regeneran automáticamente

---

### PASO 3: Eliminar Notebooks (OPCIONAL)

```cmd
del "notebooks\01_exploratory_data_analysis.ipynb"
del "notebooks\exploratory_data_analysis_eda.ipynb"
```

**Riesgo:** ⚠️ BAJO - Solo si ya no necesitas análisis exploratorio

---

### PASO 4: Limpiar Carpetas Vacías (OPCIONAL)

```cmd
rmdir /s /q test\unit
rmdir /s /q test\integration
rmdir /s /q scripts
```

**Riesgo:** ⚠️ BAJO - Puedes necesitarlas en el futuro

---

## ✅ VERIFICACIÓN POST-LIMPIEZA

Después de eliminar, ejecuta:

```cmd
# 1. Verificar que el servidor inicia
python start_server.py

# 2. Verificar que los tests pasan
python test_api_funcionando.py
python test_integracion_completa.py

# 3. Diagnosticar el modelo
python diagnosticar_modelo.py
```

**Salida esperada:**
- ✅ Servidor inicia en http://localhost:8000
- ✅ Tests pasan correctamente
- ✅ Modelo carga con 84.36% accuracy

---

## 📊 RESUMEN FINAL

### ELIMINAR CON CONFIANZA (Sin riesgo):
- ✅ 6 modelos obsoletos (data/models/)
- ✅ Carpetas de caché (__pycache__, .pytest_cache, .idea)

### CONSIDERAR ELIMINAR (Riesgo bajo):
- ⚠️ 2 notebooks duplicados
- ⚠️ 3 carpetas vacías (scripts/, test/unit/, test/integration/)

### NUNCA ELIMINAR (Crítico):
- ❌ sentiment_model.pkl (actual - 84.36%)
- ❌ Carpeta src/ completa
- ❌ Scripts principales (start_server.py, reentrenar_modelo_limpio.py, etc.)
- ❌ Datos procesados (data/processed/)
- ❌ requirements.txt, README.md

---

## 🎯 ARQUITECTURA FINAL LIMPIA

```
backend/
├── data/
│   ├── models/
│   │   ├── sentiment_model.pkl          ✅ 744 KB (ÚNICO NECESARIO)
│   │   ├── clustering_model.pkl         ✅
│   │   ├── rating_predictor.pkl         ✅
│   │   ├── recommender_system.pkl       ✅
│   │   └── backups/                     ✅
│   ├── processed/                       ✅ (5 archivos CSV)
│   └── raw/                             ✅ (2 archivos CSV)
├── src/                                 ✅ (Clean Architecture - 30+ archivos)
├── notebooks/                           ⚠️ (Opcional: 1 notebook o eliminar)
├── docs/figures/                        ✅ (Gráficos de análisis)
├── comparar_modelos.py                  ✅
├── diagnosticar_modelo.py               ✅
├── optimizar_modelo_gastronómico.py     ✅
├── reentrenar_modelo_limpio.py          ✅
├── start_server.py                      ✅
├── test_api_funcionando.py              ✅
├── test_integracion_completa.py         ✅
├── requirements.txt                     ✅
├── README.md                            ✅
└── ARCHIVOS_A_ELIMINAR.md              ✅
```

**Total archivos esenciales:** ~50 archivos Python + 4 modelos ML + 7 archivos CSV

---

## ⚠️ ADVERTENCIAS FINALES

1. **NO elimines sentiment_model.pkl** - Es el modelo en producción (84.36%)
2. **NO toques la carpeta src/** - Es la arquitectura principal
3. **Haz backup antes** de eliminar si tienes dudas
4. **Verifica después** que el servidor inicia correctamente

---

## 🚀 COMANDO ÚNICO DE LIMPIEZA (RECOMENDADO)

```cmd
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

REM Eliminar modelos obsoletos
del "data\models\sentiment_model_backup_20251024_001208.pkl"
del "data\models\sentiment_model_gastro_optimized.pkl"
del "data\models\sentiment_model_hibrido.pkl"
del "data\models\sentiment_model_mejorado.pkl"
del "data\models\sentiment_model_original_20251023_220100.pkl"
del "data\models\sentiment_vectorizer.pkl"

REM Limpiar caché
rmdir /s /q .pytest_cache 2>nul
rmdir /s /q .idea 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo.
echo ✅ Limpieza completada
echo 🔍 Verificando servidor...
python start_server.py
```

**Espacio liberado:** ~4-5 MB  
**Tiempo:** 30 segundos

---

**FIN DEL ANÁLISIS**

