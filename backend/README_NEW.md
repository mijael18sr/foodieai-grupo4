# Restaurant Recommender ML - Backend

Sistema de recomendación de restaurantes en Lima usando Machine Learning con análisis de sentimientos basado en **Ensemble de Clasificadores Bayesianos**.

---

## 🚀 Estado del Proyecto

✅ **Modelo de Sentimientos Entrenado** - Accuracy: 84.36%  
✅ **Pipeline de Datos Completo** - 378,969 reviews procesadas  
✅ **API REST Funcionando** - FastAPI con Clean Architecture  
✅ **Tests de Integración** - Sistema verificado y funcional

---

## 📁 Estructura del Proyecto

```
backend/
├── data/
│   ├── raw/
│   │   ├── Lima_Restaurants_2025_08_13_clean.csv  # Dataset limpio (378,969 reviews)
│   │   └── restaurant_metadata.csv                # Metadatos
│   ├── processed/
│   │   ├── modelo_limpio.csv                      # Para entrenamiento (199,821)
│   │   ├── restaurantes_limpio.csv                # 706 restaurantes
│   │   ├── reviews_limpio.csv                     # Reviews procesadas
│   │   └── reviews_con_sentimiento.csv            # Con análisis aplicado
│   └── models/
│       ├── sentiment_model.pkl                    # ✅ Modelo principal (84.36%)
│       ├── clustering_model.pkl                   # ✅ Clustering
│       ├── rating_predictor.pkl                   # ✅ Predictor de ratings
│       └── recommender_system.pkl                 # ✅ Recomendador
├── src/                                           # Clean Architecture
│   ├── application/
│   │   ├── services/
│   │   │   ├── sentiment_service.py               # Servicio de sentimientos
│   │   │   └── recommendation_service.py          # Servicio de recomendaciones
│   │   └── dto/                                   # Data Transfer Objects
│   ├── domain/
│   │   ├── entities/                              # Entidades del dominio
│   │   └── repositories/                          # Interfaces
│   ├── infrastructure/
│   │   ├── ml/
│   │   │   └── model_loader.py                    # Cargador de modelos ML
│   │   ├── repositories/                          # Implementaciones CSV
│   │   └── container.py                           # Dependency Injection
│   └── presentation/
│       └── api/
│           ├── main.py                            # App FastAPI
│           └── routes/
│               ├── health.py                      # Health check
│               ├── sentiment.py                   # Análisis de sentimientos
│               └── recommendations.py             # Recomendaciones
├── comparar_modelos.py                            # 🔧 Comparar versiones
├── diagnosticar_modelo.py                         # 🔍 Diagnóstico completo
├── optimizar_modelo_gastronómico.py               # 📊 Guía de optimización
├── reentrenar_modelo_limpio.py                    # 🎯 ENTRENAMIENTO PRINCIPAL
├── start_server.py                                # 🚀 Iniciar servidor
├── test_api_funcionando.py                        # ✅ Tests API
├── test_integracion_completa.py                   # ✅ Tests integración
├── requirements.txt                               # 📦 Dependencias
└── README.md                                      # 📖 Esta documentación
```

---

## 🚀 GUÍA DE INICIO RÁPIDO

### Requisitos Previos

- **Python 3.10+** instalado
- **pip** actualizado
- **Windows CMD o PowerShell**

---

## 📋 CONFIGURACIÓN INICIAL (Paso a Paso)

### PASO 1: Crear Entorno Virtual

```bash
# Navegar a la carpeta del proyecto
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno
# CMD:
.venv\Scripts\activate.bat

# PowerShell:
.venv\Scripts\Activate.ps1
```

**Verificar:** Deberías ver `(.venv)` al inicio de la línea de comandos.

---

### PASO 2: Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Dependencias instaladas:**
- FastAPI + Uvicorn (API REST)
- Pandas + NumPy (Procesamiento de datos)
- Scikit-learn (Machine Learning)
- NLTK (Procesamiento de lenguaje natural)
- Pytest (Testing)

**Tiempo:** 2-5 minutos

---

### PASO 3: Descargar Recursos NLTK

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

---

## 🎯 EJECUTAR EL SERVIDOR

### Si ya tienes los modelos entrenados:

```bash
python start_server.py
```

**Salida esperada:**
```
🚀 Iniciando Restaurant Recommender API...
📍 Backend URL: http://localhost:8000
📖 API Docs: http://localhost:8000/docs
--------------------------------------------------
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Acceder:**
- **Swagger UI:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/health

---

## 🧠 ENTRENAR/REENTRENAR EL MODELO

### Entrenar Modelo de Sentimientos

```bash
python reentrenar_modelo_limpio.py
```

**Proceso:**
1. Carga datos de `data/processed/modelo_limpio.csv` (199,821 reviews)
2. Aplica vectorización TF-IDF (15,000 términos)
3. Entrena 2 clasificadores:
   - Complement Naive Bayes (82.24%)
   - Logistic Regression (83.36%)
4. Crea **Ensemble Voting Classifier** (84.36%) ✅
5. Valida con 6 casos de prueba
6. Guarda en `data/models/sentiment_model.pkl`

**Métricas Esperadas:**

```
✅ Accuracy:            84.36%
✅ Cohen's Kappa:       56.06%
✅ F1-Score (weighted): 84.64%

Por Clase:
  POSITIVO:
    • Precision: 95.8%
    • Recall:    90.1%
    • F1-Score:  92.9%
  
  NEGATIVO:
    • Precision: 51.7%
    • Recall:    87.5%
    • F1-Score:  65.0%
  
  NEUTRO:
    • Precision: 34.7%
    • Recall:    25.8%
    • F1-Score:  29.6%
```

**Tiempo:** 10-15 minutos

**Datos de entrenamiento:**
- Total: 199,821 registros
- Positivos: 162,372 (81.3%)
- Negativos: 20,306 (10.2%)
- Neutros: 17,143 (8.6%)

---

## 🧪 VERIFICAR QUE TODO FUNCIONA

### 1. Health Check

```bash
# PowerShell
Invoke-WebRequest -Uri http://localhost:8000/api/v1/health -UseBasicParsing
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-24T...",
  "models": {
    "sentiment_analysis": {
      "status": "loaded",
      "accuracy": 0.8436
    }
  }
}
```

---

### 2. Test Completo de API

```bash
python test_api_funcionando.py
```

**Verifica:**
- ✅ Servidor respondiendo
- ✅ Health check funcional
- ✅ Endpoint de sentimientos
- ✅ Métricas del modelo
- ✅ Predicciones correctas

---

### 3. Test de Integración

```bash
python test_integracion_completa.py
```

**Verifica:**
- ✅ Carga de modelo
- ✅ Servicio de análisis
- ✅ Niveles de confianza
- ✅ Integración completa

---

## 🔍 DIAGNÓSTICO Y OPTIMIZACIÓN

### 1. Diagnosticar Modelo

```bash
python diagnosticar_modelo.py
```

**Muestra:**
- ✅ Componentes del modelo (Vectorizer, Classifier)
- ✅ Clases y vocabulario (12,000 términos)
- ✅ Predicciones raw con probabilidades
- ✅ Términos importantes en vocabulario
- ✅ Pruebas con ejemplos reales
- ✅ Problemas detectados y soluciones

**Ejemplo de salida:**
```
✅ Modelo cargado correctamente
✓ Vectorizer: TfidfVectorizer
✓ Classifier: LogisticRegression
✓ Vocabulario: 12,000 términos

TEST: Predicciones Raw
  📝 "La comida estuvo deliciosa"
     → positivo (95.2%)
```

---

### 2. Comparar Modelos

```bash
python comparar_modelos.py
```

**Compara:**
- Modelo actual vs modelo optimizado gastronómico
- Métricas lado a lado (Accuracy, Precision, Recall)
- Pruebas con ejemplos idénticos
- Recomendación de cuál usar

**Útil para:** Evaluar si una nueva versión mejora los resultados

---

### 3. Optimizar Modelo Gastronómico

```bash
python optimizar_modelo_gastronómico.py
```

**Proporciona:**

#### 📊 Guía de Métricas Esperadas
```
Accuracy:     75-85%  (Mínimo: 75%, Recomendado: 80-85%)
Cohen's Kappa: 0.60-0.80
Precision:    73-83%
Recall:       72-82%
F1-Score:     72-82%
```

#### 🎨 Umbrales de Confianza para UI
```
≥ 90%   → ✓✓ MUY CONFIABLE    (Verde)
80-89%  → ✓ CONFIABLE         (Verde)
70-79%  → ⚠ MODERADO          (Amarillo) + botón "Revisar"
60-69%  → ? BAJA CONFIANZA    (Naranja) - Sugerir revisión
< 60%   → ✗ INDETERMINADO     (Rojo) - NO mostrar
```

#### 💡 Ejemplos de Interpretación
```
📝 "La comida estuvo deliciosa" → POSITIVO (95.0%) - MUY CONFIABLE
📝 "Comida regular, nada especial" → NEUTRO (72.0%) - MODERADO
📝 "Se atienden todos los domingos" → NEUTRO (55.0%) - NO MOSTRAR
```

---

## 📊 DATOS DEL PROYECTO

### Dataset Original

**Fuente:** [Lima Restaurant Review - Kaggle](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)

**Estadísticas:**
- 📍 **706 restaurantes** de alta calidad en Lima
- 💬 **378,969 reviews** de clientes
- ⭐ **Ratings:** 1-5 estrellas
- 📝 **Idioma:** Español (Perú)

### Preprocesamiento Aplicado

Los datos incluidos ya tienen:
- ✅ Limpieza de emojis y caracteres especiales
- ✅ Normalización de texto (lowercase, sin acentos)
- ✅ Eliminación de stopwords en español
- ✅ Detección y eliminación de anomalías
- ✅ Balance de clases para entrenamiento
- ✅ Análisis de sentimiento aplicado

---

## 📊 MÉTRICAS ESPERADAS DEL MODELO

### 🎯 Modelo de Sentimientos (Actual: 84.36%)

#### Métricas Generales
```
Accuracy:            84.36%  ✅ (Mínimo: 75%)
Cohen's Kappa:       56.06%
F1-Score (weighted): 84.64%
F1-Score (macro):    62.51%
```

#### Métricas por Clase

**POSITIVO** (Comentarios buenos)
```
Precision: 95.8%  ← De las predicciones positivas, 96% son correctas
Recall:    90.1%  ← Detectamos 90% de los comentarios positivos reales
F1-Score:  92.9%  ← Balance excelente
Support:   32,475 muestras
```

**NEGATIVO** (Comentarios malos)
```
Precision: 51.7%  ← De las predicciones negativas, 52% son correctas
Recall:    87.5%  ← Detectamos 88% de los comentarios negativos reales
F1-Score:  65.0%  ← Balance aceptable
Support:   4,061 muestras
```

**NEUTRO** (Comentarios informativos)
```
Precision: 34.7%  ← Clase más difícil (menos datos)
Recall:    25.8%  ← Difícil de detectar
F1-Score:  29.6%  ← Esperado que sea menor
Support:   3,429 muestras
```

---

## 🏗️ Arquitectura

### Clean Architecture + Domain-Driven Design

```
Presentation Layer (API)
    ↓
Application Layer (Services + DTOs)
    ↓
Domain Layer (Entities + Repositories)
    ↓
Infrastructure Layer (ML + Data Access)
```

### Modelo de Machine Learning

**Tipo:** Ensemble Voting Classifier

**Componentes:**
1. **Complement Naive Bayes** (82.24% accuracy)
   - Optimizado para datos desbalanceados
   - Funciona bien con clases minoritarias

2. **Logistic Regression** (83.36% accuracy)
   - Solver: SAGA
   - Class weight: balanced
   - Max iterations: 1000

3. **Ensemble Final** (84.36% accuracy) ✅
   - Voting: soft (promedia probabilidades)
   - Mejor que cada modelo individual

**Vectorización:**
- TF-IDF con 15,000 términos
- N-gramas: (1, 2) - unigramas y bigramas
- Stopwords en español (NLTK)
- Sublinear TF scaling

---

## 🧹 LIMPIEZA DE ARCHIVOS OBSOLETOS

El proyecto tiene **modelos duplicados** que deben eliminarse.

### Ver Guía Completa de Limpieza

Consulta los documentos:
- ✅ `ARCHIVOS_A_ELIMINAR.md` - Guía rápida con comandos
- ✅ `ANALISIS_COMPLETO_ARCHIVOS.md` - Análisis detallado

### Limpieza Rápida (Eliminar Modelos Obsoletos)

```bash
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

# Eliminar 6 modelos obsoletos
del "data\models\sentiment_model_backup_20251024_001208.pkl"
del "data\models\sentiment_model_gastro_optimized.pkl"
del "data\models\sentiment_model_hibrido.pkl"
del "data\models\sentiment_model_mejorado.pkl"
del "data\models\sentiment_model_original_20251023_220100.pkl"
del "data\models\sentiment_vectorizer.pkl"

# Limpiar caché
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
rmdir /s /q .pytest_cache 2>nul
rmdir /s /q .idea 2>nul

echo ✅ Limpieza completada - Espacio liberado: ~5 MB
```

**Resultado:** Solo quedan 4 modelos esenciales

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ Error: "No module named 'fastapi'"

**Causa:** Dependencias no instaladas o entorno no activado.

**Solución:**
```bash
# Activar entorno
.venv\Scripts\activate.bat

# Instalar dependencias
pip install -r requirements.txt
```

---

### ❌ Error: "No se encuentra sentiment_model.pkl"

**Causa:** Modelo no entrenado.

**Solución:**
```bash
python reentrenar_modelo_limpio.py
```

---

### ❌ Error: "Port 8000 already in use"

**Causa:** Puerto ocupado por otro proceso.

**Solución:**
```bash
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Matar proceso (usa el PID)
taskkill /F /PID <NUMERO_PID>

# Reiniciar servidor
python start_server.py
```

---

### ❌ Error: NLTK Data not found

**Causa:** Recursos de NLTK no descargados.

**Solución:**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

---

### ❌ Modelo predice mal ("deliciosa" → neutro)

**Causa:** Modelo desactualizado.

**Solución:**
```bash
# Diagnosticar
python diagnosticar_modelo.py

# Reentrenar
python reentrenar_modelo_limpio.py

# Verificar
python comparar_modelos.py
```

---

### ❌ Accuracy bajo (<75%)

**Causa:** Datos desbalanceados o modelo no optimizado.

**Solución:**
```bash
# El modelo ensemble debería dar ~84% accuracy
python reentrenar_modelo_limpio.py

# Verificar métricas esperadas:
# - Accuracy: 84.36%
# - Precision Positivos: 95.8%
# - Recall Positivos: 90.1%
```

---

## ⚡ COMANDOS RÁPIDOS DE REFERENCIA

### Configuración Inicial (Una vez)
```bash
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### Entrenar Modelo
```bash
python reentrenar_modelo_limpio.py
```

### Ejecutar Servidor
```bash
.venv\Scripts\activate.bat
python start_server.py
```

### Diagnóstico
```bash
python diagnosticar_modelo.py
python comparar_modelos.py
python optimizar_modelo_gastronómico.py
```

### Testing
```bash
python test_api_funcionando.py
python test_integracion_completa.py
```

---

## ✅ Checklist de Verificación

Antes de considerarlo funcionando:

- [ ] Python 3.10+ instalado (`python --version`)
- [ ] Entorno virtual creado y activado (ves `(.venv)`)
- [ ] Dependencias instaladas (`pip list`)
- [ ] NLTK resources descargados
- [ ] Datos procesados existen (`data/processed/modelo_limpio.csv`)
- [ ] Modelo entrenado (`data/models/sentiment_model.pkl`)
- [ ] Accuracy ≥ 84% en reentrenamiento
- [ ] Servidor inicia sin errores
- [ ] API responde (`http://localhost:8000/docs`)
- [ ] Health check OK (`http://localhost:8000/api/v1/health`)
- [ ] Tests pasan correctamente

---

## 🎓 Para Desarrolladores Nuevos

### ¿Primera vez con Python/ML? Empieza aquí:

```bash
# 1. Navegar a la carpeta
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno
.venv\Scripts\activate.bat

# 4. Instalar todo
pip install -r requirements.txt

# 5. Descargar recursos
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# 6. Entrenar modelo (ESPERA 10-15 min)
python reentrenar_modelo_limpio.py

# 7. Iniciar servidor
python start_server.py

# 8. Abrir en navegador
# http://localhost:8000/docs
```

---

## 📞 Contacto y Soporte

**UNMSM - Postgrado Machine Learning**

### ¿Problemas?

1. Revisa [🐛 Solución de Problemas](#-solución-de-problemas-comunes)
2. Verifica el [✅ Checklist](#-checklist-de-verificación)
3. Ejecuta: `python diagnosticar_modelo.py`

---

## 🚀 Siguiente Paso

### Si es tu primera vez:

```bash
python reentrenar_modelo_limpio.py   # 10-15 min
python start_server.py                # Servidor inicia
```

### Si ya tienes todo:

```bash
python start_server.py
```

**Accede a:** http://localhost:8000/docs

¡El proyecto está listo! 🎉

