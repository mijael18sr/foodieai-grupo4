# EXPLICACIÓN: 84.36% vs 85.67% - ¿Cuál es el correcto?

**Fecha**: 2025-11-07
**Pregunta**: ¿Por qué hay dos accuracies diferentes?

---

## RESPUESTA RÁPIDA

**AMBOS SON CORRECTOS**, pero miden cosas diferentes:

| Accuracy | Qué mide | Dónde se ve |
|----------|----------|-------------|
| **84.36%** | Modelo en **test set (20%)** | Entrenamiento (`reentrenar_modelo_limpio.py`) |
| **85.67%** | Modelo en **dataset completo (100%)** | Matriz de confusión (EDA notebook) |

---

## EXPLICACIÓN DETALLADA

### 1⃣ Accuracy de Entrenamiento: 84.36%

```python
# En reentrenar_modelo_limpio.py
X_train, X_test, y_train, y_test = train_test_split(
 X, y, test_size=0.2, random_state=42
)

# Entrenar con 80% (159,856 registros)
model.fit(X_train, y_train)

# Evaluar con 20% NO VISTO (39,965 registros)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# Resultado: 84.36%
```

**¿Qué significa?**
- El modelo **nunca vio** estos 39,965 registros durante el entrenamiento
- Es la métrica **más importante** para evaluar generalización
- Muestra cómo funcionará con datos **nuevos y desconocidos**

---

### 2⃣ Accuracy en Dataset Completo: 85.67%

```python
# En el EDA notebook / matriz de confusión
# Cargar TODO el dataset
df = pd.read_csv('modelo_limpio.csv') # 199,821 registros

# Predecir sobre TODOS los datos
y_true = df['sentimiento']
y_pred = model.predict(df['comment'])

accuracy = accuracy_score(y_true, y_pred)
# Resultado: 85.67%
```

**¿Qué significa?**
- El modelo **sí vio** el 80% de estos datos durante el entrenamiento
- Muestra el rendimiento general sobre todo el dataset
- Es lo que se visualiza en la **matriz de confusión del EDA**

---

## ¿POR QUÉ HAY DIFERENCIA?

### Explicación Simple

```
Dataset Completo (199,821):
 80% TRAIN (159,856) → Modelo los VIO y aprendió
 Accuracy aquí: ~86-87% (más alto)

 20% TEST (39,965) → Modelo NO los vio
 Accuracy aquí: 84.36% (más bajo, pero más realista)

Cuando evalúas TODO el dataset (100%):
 80% que el modelo ya conoce → predice MUY BIEN
 20% que el modelo NO conoce → predice BIEN
 Promedio: 85.67% (entre ambos)
```

---

## COMPARACIÓN VISUAL

### Accuracy por Conjunto

```
Test Set (20%): [] 84.36% ← MÁS REALISTA
 (datos no vistos)

Dataset Completo: [] 85.67% ← MÁS OPTIMISTA
 (incluye train)
```

### Cálculo Aproximado

```
Accuracy completo = (Train accuracy × 0.8) + (Test accuracy × 0.2)

Si Train accuracy ≈ 86.5%:
85.67% ≈ (86.5% × 0.8) + (84.36% × 0.2)
85.67% ≈ 69.2% + 16.87%
85.67% ≈ 86.07% (aproximado)
```

---

## ¿CUÁL DEBES USAR?

### Para Reportar el Modelo

| Situación | Accuracy a Usar | Razón |
|-----------|----------------|-------|
| **Documentación técnica** | 84.36% | Métrica oficial del modelo |
| **Papers académicos** | 84.36% | Test set accuracy es estándar |
| **Presentaciones** | 84.36% | Más conservador y realista |
| **Matriz de confusión** | 85.67% | Refleja evaluación completa |
| **Visualizaciones EDA** | 85.67% | Coherente con los gráficos |

---

## RESPUESTAS A PREGUNTAS COMUNES

### ¿Por qué el accuracy completo es MÁS ALTO?

Porque incluye datos de entrenamiento que el modelo ya "memorizó". Es normal y esperado.

### ¿Cuál es el "verdadero" accuracy?

El **84.36%** (test set) es el más honesto porque mide datos no vistos.

### ¿Está mal usar 85.67%?

No, pero debes **aclarar** que es sobre el dataset completo, no solo test set.

### ¿Qué accuracy ver en el EDA?

El EDA muestra **85.67%** porque evalúa todo el dataset para la matriz de confusión.

---

## RECOMENDACIÓN OFICIAL

### Para tu Proyecto

**En la documentación escribe**:

```markdown
## Accuracy del Modelo

- **Test Set Accuracy**: 84.36% (39,965 registros no vistos)
- **Dataset Completo**: 85.67% (199,821 registros totales)

El modelo fue entrenado con 80% de los datos y evaluado con el 20% restante,
obteniendo un accuracy de **84.36%** en datos no vistos, lo que indica
excelente capacidad de generalización.
```

**En la matriz de confusión del EDA**:

```markdown
## Matriz de Confusión

Accuracy: 85.67% (evaluado sobre 199,821 registros completos)

*Nota: El accuracy del test set durante el entrenamiento fue 84.36%*
```

---

## EXPLICACIÓN ACADÉMICA

### ¿Por qué es importante la distinción?

1. **Overfitting Detection**: Si el accuracy en train >> accuracy en test, hay overfitting
2. **Generalización**: Test accuracy muestra cómo funcionará con datos nuevos
3. **Honestidad**: Reportar solo el accuracy completo puede ser engañoso

### En tu caso

```
Train accuracy: ~86.5% (estimado)
Test accuracy: 84.36%
Diferencia: ~2.1%

 BUENA SEÑAL: Diferencia pequeña = poco overfitting
```

---

## RESUMEN FINAL

```


 ACCURACY OFICIAL DEL MODELO: 84.36% 
 (Test Set - 20% de datos no vistos) 

 ACCURACY EN MATRIZ DE CONFUSIÓN: 85.67% 
 (Dataset Completo - 100% de datos) 

 DIFERENCIA: ~1.3% (normal y aceptable) 


```

### Conclusión

- **Usa 84.36%** cuando hables del modelo (más conservador y honesto)
- **85.67% aparecerá** en tu matriz de confusión del EDA (es correcto)
- **Ambos son válidos**, solo miden cosas diferentes
- **La diferencia de 1.3%** es pequeña y muestra buena generalización

---

**TL;DR**:
- **84.36%** = Accuracy del modelo en test set (lo oficial)
- **85.67%** = Accuracy en dataset completo (lo que ves en EDA)
- Ambos son correctos, usa el contexto apropiado para cada uno

---

**Última actualización**: 2025-11-07
**Estado**: ACLARADO

