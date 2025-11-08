# 📊 Métricas del Modelo de Análisis de Sentimientos

## 🎯 Rendimiento Actual del Modelo

| Métrica | Valor | Estado |
|---------|-------|---------|
| **Precisión General** | **84.4%** | ✅ Excelente |
| **Precisión Macro** | **60.8%** | ⚠️ Mejorable |
| **Precisión Weighted** | **86.1%** | ✅ Excelente |
| **Recall Macro** | **67.8%** | ⚠️ Mejorable |
| **Recall Weighted** | **84.4%** | ✅ Excelente |
| **F1-Score Macro** | **62.5%** | ⚠️ Mejorable |
| **F1-Score Weighted** | **84.6%** | ✅ Excelente |
| **Cohen's Kappa** | **0.561** | ✅ Bueno |
| **Matthews Correlation** | **0.569** | ✅ Bueno |

---

## 📚 Definición y Cálculo de Métricas

### 🎯 **Accuracy (Precisión General)**
**Valor:** 84.4%

**Definición:** Porcentaje de predicciones correctas sobre el total de predicciones.

**Fórmula:**
```
Accuracy = (VP + VN) / (VP + VN + FP + FN)
```

**Interpretación:** De cada 100 comentarios analizados, el modelo clasifica correctamente 84.

---

### ⚖️ **Precision (Precisión)**

#### **Precision Macro: 60.8%**
**Definición:** Promedio simple de la precisión de cada clase.

**Cálculo desde métricas por clase:**
```
Precision Macro = (Precision_Positivo + Precision_Neutro + Precision_Negativo) / 3
Precision Macro = (95.8% + 34.7% + 51.7%) / 3 = 60.8%
```

#### **Precision Weighted: 86.1%**
**Definición:** Promedio ponderado por el número de muestras de cada clase.

**Fórmula:**
```
Precision Weighted = Σ(Precision_i × Support_i) / Total_Samples
```

**Interpretación:** La precisión macro baja indica que las clases minoritarias (neutro/negativo) tienen menor precisión.

---

### 🔍 **Recall (Exhaustividad)**

#### **Recall Macro: 67.8%**
**Definición:** Promedio simple del recall de cada clase.

**Cálculo desde métricas por clase:**
```
Recall Macro = (Recall_Positivo + Recall_Neutro + Recall_Negativo) / 3
Recall Macro = (90.1% + 25.8% + 87.5%) / 3 = 67.8%
```

#### **Recall Weighted: 84.4%**
**Definición:** Promedio ponderado del recall por clase.

**Interpretación:** El modelo encuentra aproximadamente 2/3 de los casos reales de cada sentimiento.

---

### 🎲 **F1-Score (Media Armónica)**

#### **F1-Score Macro: 62.5%**
**Definición:** Media armónica entre precisión y recall, promediada por clase.

**Fórmula por clase:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
F1 Macro = (F1_Positivo + F1_Neutro + F1_Negativo) / 3
```

#### **F1-Score Weighted: 84.6%**
**Definición:** F1-Score ponderado por el soporte de cada clase.

---

### 🤝 **Cohen's Kappa: 0.561**
**Definición:** Mide la concordancia entre clasificador y realidad, ajustado por el azar.

**Interpretación:**
- **0.0 - 0.20:** Concordancia pobre
- **0.21 - 0.40:** Concordancia débil  
- **0.41 - 0.60:** Concordancia moderada ✅ (Nuestro caso)
- **0.61 - 0.80:** Concordancia buena
- **0.81 - 1.00:** Concordancia casi perfecta

**Equivalente a R² para clasificación.**

---

### 📊 **Matthews Correlation Coefficient: 0.569**
**Definición:** Coeficiente de correlación entre predicciones y valores reales.

**Interpretación:**
- **-1:** Predicciones completamente erróneas
- **0:** Predicciones aleatorias
- **+1:** Predicciones perfectas
- **0.569:** Correlación moderada-alta ✅

---

## 📈 Métricas por Clase de Sentimiento

### 😊 **Sentimientos Positivos**
| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Precision** | **95.8%** | ✅ Excelente: 96 de cada 100 predicciones "positivo" son correctas |
| **Recall** | **90.1%** | ✅ Excelente: Encuentra 90 de cada 100 comentarios positivos reales |
| **F1-Score** | **92.9%** | ✅ Excelente: Balance óptimo entre precisión y recall |
| **Support** | **32,475** | 📊 Clase mayoritaria (81% del dataset) |

### 😐 **Sentimientos Neutros**
| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Precision** | **34.7%** | ⚠️ Baja: Solo 35 de cada 100 predicciones "neutro" son correctas |
| **Recall** | **25.8%** | ⚠️ Baja: Solo encuentra 26 de cada 100 comentarios neutros reales |
| **F1-Score** | **29.6%** | ❌ Deficiente: Necesita mejora urgente |
| **Support** | **3,429** | 📊 Clase minoritaria (8.5% del dataset) |

### 😞 **Sentimientos Negativos**
| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Precision** | **51.7%** | ⚠️ Moderada: 52 de cada 100 predicciones "negativo" son correctas |
| **Recall** | **87.5%** | ✅ Excelente: Encuentra 88 de cada 100 comentarios negativos reales |
| **F1-Score** | **65.0%** | ⚠️ Aceptable: Balance moderado |
| **Support** | **4,061** | 📊 Clase minoritaria (10.1% del dataset) |

---

## 🎯 Análisis de Rendimiento

### ✅ **Fortalezas del Modelo**
1. **Excelente precisión general (84.4%)** - Muy confiable para uso en producción
2. **Detección de sentimientos positivos casi perfecta** (95.8% precisión)
3. **Alta capacidad de encontrar comentarios negativos** (87.5% recall)
4. **Métricas ponderadas sólidas** - Buen rendimiento en la distribución real de datos

### ⚠️ **Áreas de Mejora**
1. **Sentimientos neutros muy problemáticos** (29.6% F1-Score)
2. **Desbalance significativo de clases** (81% positivos vs 8.5% neutros)
3. **Precisión macro baja** (60.8%) indica problemas con clases minoritarias

### 🎯 **Evaluación General**
**BUENO** - Modelo funcional para producción con oportunidades claras de mejora.

---

## 🔧 Recomendaciones para Mejora

### 🎯 **Prioridad Alta**
1. **Balancear dataset:** Aumentar muestras de comentarios neutros y negativos
2. **Mejorar detección de neutros:** Técnicas de oversampling (SMOTE) o data augmentation
3. **Optimizar hiperparámetros:** GridSearchCV para Complement Naive Bayes

### 📊 **Metas Objetivo**
| Métrica Actual | Valor Actual | Meta Objetivo | Mejora Necesaria |
|----------------|--------------|---------------|------------------|
| **Precision Macro** | 60.8% | **70-75%** | +10-15% |
| **Recall Macro** | 67.8% | **70-75%** | +3-8% |
| **F1-Score Macro** | 62.5% | **72-78%** | +10-15% |
| **F1 Neutros** | 29.6% | **50-60%** | +20-30% |

### 🚀 **Plan de Mejora**
1. **Semana 1:** Recolectar 2-3K comentarios neutros balanceados
2. **Semana 2:** Implementar técnicas de data augmentation
3. **Semana 3:** Re-entrenar modelo con dataset balanceado
4. **Semana 4:** A/B testing modelo mejorado vs actual

---

## 🛠️ Implementación Técnica

### 📁 **Ubicación del Código**
- **Modelo:** `backend/src/ml/models/sentiment_model.py`
- **API Métricas:** `backend/src/presentation/api/routes/sentiment.py`
- **Frontend:** `frontend/src/components/Sentiment/SentimentPanel.tsx`

### 🔌 **Endpoint de Métricas**
```bash
GET /api/v1/sentiment/model/metrics
```

### 📊 **Estructura de Respuesta**
```json
{
  "accuracy": 0.844,
  "precision_macro": 0.608,
  "precision_weighted": 0.861,
  "recall_macro": 0.678,
  "recall_weighted": 0.844,
  "f1_macro": 0.625,
  "f1_weighted": 0.846,
  "cohen_kappa": 0.561,
  "matthews_corrcoef": 0.569,
  "per_class_metrics": {
    "positivo": {
      "precision": 0.958,
      "recall": 0.901,
      "f1_score": 0.929,
      "support": 32475
    },
    "neutro": {
      "precision": 0.347,
      "recall": 0.258,
      "f1_score": 0.296,
      "support": 3429
    },
    "negativo": {
      "precision": 0.517,
      "recall": 0.875,
      "f1_score": 0.650,
      "support": 4061
    }
  }
}
```

---

## 📝 Historial de Cambios

### 📅 **2025-10-24**
- ✅ **Corregido:** Precision Macro y Recall Macro mostraban 0.0%
- 🔧 **Implementado:** Cálculo automático desde métricas por clase
- 📊 **Resultado:** Métricas ahora se muestran correctamente en UI

### 📊 **Valores Corregidos**
| Métrica | Antes | Después |
|---------|-------|---------|
| Precision Macro | 0.0% | **60.8%** |
| Recall Macro | 0.0% | **67.8%** |

---

*Documento generado el 24 de Octubre, 2025*  
*Modelo: SentimentAnalysisModel v2 - Complement Naive Bayes*  
*Dataset: Restaurant Reviews Lima (39,965 muestras de test)*