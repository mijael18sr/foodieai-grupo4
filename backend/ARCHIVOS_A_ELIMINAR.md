# 🗑️ ARCHIVOS A ELIMINAR MANUALMENTE

## Modelos Duplicados/Obsoletos en `data/models/`

Elimina estos archivos **MANUALMENTE** (uno por uno):

```
data/models/sentiment_model_backup_20251024_001208.pkl
data/models/sentiment_model_gastro_optimized.pkl
data/models/sentiment_model_hibrido.pkl
data/models/sentiment_model_mejorado.pkl
data/models/sentiment_model_original_20251023_220100.pkl
data/models/sentiment_vectorizer.pkl
```

### ✅ Comando para eliminar (PowerShell):

```powershell
# Navega a la carpeta del proyecto
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

# Elimina los modelos obsoletos UNO POR UNO
Remove-Item "data\models\sentiment_model_backup_20251024_001208.pkl"
Remove-Item "data\models\sentiment_model_gastro_optimized.pkl"
Remove-Item "data\models\sentiment_model_hibrido.pkl"
Remove-Item "data\models\sentiment_model_mejorado.pkl"
Remove-Item "data\models\sentiment_model_original_20251023_220100.pkl"
Remove-Item "data\models\sentiment_vectorizer.pkl"
```

### ✅ Comando para eliminar (CMD):

```cmd
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

del "data\models\sentiment_model_backup_20251024_001208.pkl"
del "data\models\sentiment_model_gastro_optimized.pkl"
del "data\models\sentiment_model_hibrido.pkl"
del "data\models\sentiment_model_mejorado.pkl"
del "data\models\sentiment_model_original_20251023_220100.pkl"
del "data\models\sentiment_vectorizer.pkl"
```

---

## 📂 MODELOS QUE DEBES MANTENER

✅ **NO elimines estos archivos:**

```
data/models/sentiment_model.pkl              ← Modelo actual (84.36% accuracy)
data/models/clustering_model.pkl             ← Clustering de restaurantes
data/models/rating_predictor.pkl             ← Predictor de ratings
data/models/recommender_system.pkl           ← Sistema de recomendación
data/models/backups/                         ← Carpeta de backups (mantener)
```

---

## 🧹 Otras Limpiezas Opcionales

### Carpetas de caché (seguro eliminar):

```powershell
# PowerShell
Remove-Item -Recurse -Force ".pytest_cache"
Remove-Item -Recurse -Force "__pycache__"
Remove-Item -Recurse -Force "src\__pycache__"
```

```cmd
# CMD
rmdir /s /q .pytest_cache
rmdir /s /q __pycache__
rmdir /s /q src\__pycache__
```

**Nota:** Estas carpetas se regeneran automáticamente, es seguro eliminarlas.

---

## ✅ Estructura Final Limpia

Después de la limpieza, tendrás:

```
backend/
├── data/
│   ├── models/
│   │   ├── sentiment_model.pkl          ✅ (84.36% accuracy)
│   │   ├── clustering_model.pkl         ✅
│   │   ├── rating_predictor.pkl         ✅
│   │   ├── recommender_system.pkl       ✅
│   │   └── backups/                     ✅
│   ├── processed/                       ✅
│   └── raw/                             ✅
├── src/                                 ✅ (Arquitectura Clean)
├── comparar_modelos.py                  ✅ (Diagnóstico)
├── diagnosticar_modelo.py               ✅ (Diagnóstico)
├── optimizar_modelo_gastronómico.py     ✅ (Diagnóstico)
├── reentrenar_modelo_limpio.py          ✅ (Entrenamiento)
├── start_server.py                      ✅ (Servidor)
├── test_api_funcionando.py              ✅ (Testing)
├── test_integracion_completa.py         ✅ (Testing)
├── requirements.txt                     ✅
└── README.md                            ✅
```

---

## 🎯 Resumen

**Total de archivos a eliminar:** 6 modelos obsoletos

**Espacio liberado:** ~4-5 MB

**Tiempo estimado:** 2 minutos

---

## ⚠️ IMPORTANTE

- ✅ Elimina **MANUALMENTE** uno por uno para evitar errores
- ✅ NO elimines `sentiment_model.pkl` (es el modelo actual en uso)
- ✅ NO elimines la carpeta `backups/`
- ✅ Después de eliminar, reinicia el servidor: `python start_server.py`

