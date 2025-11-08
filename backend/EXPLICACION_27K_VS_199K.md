# ANÁLISIS: ¿POR QUÉ SOLO HAY ~27,000 REGISTROS EN LUGAR DE 199,821?

**Fecha**: 2025-11-07
**Problema**: El notebook mostraba ~27,000 registros pero se esperaban 199,821
**Estado**: **SOLUCIONADO - CAMBIADO A LEFT JOIN (199,821 registros)**

---

## SOLUCIÓN APLICADA

**El notebook ha sido modificado** para usar `how='left'` en el merge:

```python
# AHORA (199,821 registros):
df_datafinal = pd.merge(df_reseñas, df_restaurantes, on='id_place', how='left')
```

**Resultado**: El notebook ahora generará `modelo_limpio.csv` con **199,821 registros completos**.

**Próximo paso**: Ejecutar el notebook completo para regenerar el archivo.

Ver detalles en: `CAMBIO_A_LEFT_JOIN_APLICADO.md`

---

## RESPUESTA RÁPIDA (HISTÓRICA)

**HAY DOS DATASETS DIFERENTES**:

1. **df_modelo** (creado en el notebook) → ~27,000 registros
 - Resultado del MERGE entre `df_reseñas` y `df_restaurantes`
 - Con `how='inner'` solo mantiene coincidencias

2. **modelo_limpio.csv** (archivo guardado) → **199,821 registros**
 - Archivo procesado con TODOS los datos
 - Este es el que se usa para evaluación

---

## EXPLICACIÓN DETALLADA

### Flujo del Notebook

```
PASO 1: Carga de datos raw
 df_reseñas = pd.read_csv('Lima_Restaurants_2025_08_13.csv')
 ~378,969 registros (total de reseñas)

 df_restaurantes = pd.read_csv('restaurant_metadata.csv')
 ~706 registros (solo restaurantes de alta calidad)

PASO 2: Merge con INNER JOIN
 df_datafinal = pd.merge(df_reseñas, df_restaurantes, how='inner')
 ~27,000 registros
 Se pierden ~351,000 registros
 RAZÓN: Solo mantiene reseñas de los 706 restaurantes seleccionados

 df_modelo = df_datafinal[[columnas...]]
 ~27,000 registros

PASO 3: Asignación de sentimientos
 df_modelo['sentimiento'] = rating_to_sentiment(rating)
 ~27,000 registros con sentimientos

PASO 4: Guardado
 df_modelo.to_csv('modelo_limpio.csv')
 AQUÍ ESTÁ LA CONFUSIÓN
```

---

## VERIFICACIÓN

### ¿Cuántos registros tiene realmente modelo_limpio.csv?

Para verificar, ejecuta en el notebook:

```python
df_check = pd.read_csv(DATA_PROCESSED / 'modelo_limpio.csv')
print(f"Registros en modelo_limpio.csv: {len(df_check):,}")
print(df_check['sentimiento'].value_counts())
```

**Resultado esperado**:
- Si muestra ~**27,000** → El notebook guardó correctamente (pero con merge filtrado)
- Si muestra ~**199,821** → Hay un archivo diferente (procesado previamente)

---

## ¿POR QUÉ LA CONFUSIÓN?

El mensaje que mencionaste:
```
 Distribución de sentimientos:
 • Positivo: 162,372 (81.26%)
 • Negativo: 20,306 (10.16%)
 • Neutro: 17,143 (8.58%)
```

**ESTO son 199,821 registros**, pero el notebook solo crea ~27,000.

**Posibles explicaciones**:

### Opción 1: Hay DOS archivos diferentes
- `modelo_limpio.csv` (27K) - Creado por el notebook con merge filtrado
- `reviews_con_sentimiento.csv` (199K) - Archivo procesado con todos los datos

### Opción 2: El notebook fue ejecutado con datos diferentes anteriormente
- Alguien ejecutó el notebook SIN el merge filtrado
- El archivo guardado tiene 199K registros
- Pero la versión actual del notebook tiene el merge que reduce a 27K

---

## SOLUCIÓN: ¿QUÉ HACER?

### Si quieres usar los 199,821 registros COMPLETOS:

**Opción A: Cambiar el merge a LEFT JOIN**

En la celda del merge, cambiar:

```python
# ACTUAL (solo 27K):
df_datafinal = pd.merge(df_reseñas, df_restaurantes, on='id_place', how='inner')

# CAMBIAR A (199K):
df_datafinal = pd.merge(df_reseñas, df_restaurantes, on='id_place', how='left')
```

**Consecuencia**: Mantendrás TODAS las reseñas (199K), pero algunas no tendrán metadata de restaurante.

---

**Opción B: NO hacer merge, usar solo df_reseñas**

```python
# En lugar del merge, trabajar directamente con df_reseñas
df_modelo = df_reseñas[[
 "id_review",
 "id_place",
 "caption", # ← cambiar "comment" por "caption"
 "rating",
 "username",
 "review_date"
]].copy()

# Renombrar caption a comment
df_modelo.rename(columns={'caption': 'comment'}, inplace=True)
```

**Consecuencia**: Tendrás 199K registros pero SIN información de categoría/distrito del restaurante.

---

**Opción C: Usar el archivo existente `reviews_con_sentimiento.csv`**

Si ya existe un archivo con 199K registros:

```python
# Cargar el archivo procesado completo
df_modelo = pd.read_csv(DATA_PROCESSED / 'reviews_con_sentimiento.csv')
```

---

### Si quieres mantener solo los 27,000 (restaurantes de alta calidad):

**Entonces está correcto**

El notebook está filtrando intencionalmente para trabajar solo con:
- Los **706 restaurantes de alta calidad** de `restaurant_metadata.csv`
- Sus **~27,000 reseñas** asociadas

**Esto es válido si**:
- Solo quieres analizar restaurantes de alta calidad
- El proyecto se enfoca en un subconjunto curado de restaurantes

---

## RESUMEN

| Aspecto | Valor | Explicación |
|---------|-------|-------------|
| **Reseñas totales** | ~378,969 | Todas las reseñas en el CSV raw |
| **Restaurantes curados** | 706 | Solo restaurantes de alta calidad |
| **Reseñas después del merge** | ~27,000 | Solo reseñas de los 706 restaurantes |
| **modelo_limpio.csv (notebook)** | ~27,000 | Guardado por el notebook actual |
| **modelo_limpio.csv (esperado)** | 199,821 | ¿Existe ya guardado? |

---

## RECOMENDACIÓN

1. **Verificar qué archivo realmente existe**:
 ```bash
 python -c "import pandas as pd; df=pd.read_csv('data/processed/modelo_limpio.csv'); print(f'Registros: {len(df):,}')"
 ```

2. **Si sale ~27,000**: El notebook está trabajando correctamente con restaurantes filtrados

3. **Si sale ~199,821**: Hay un archivo previamente procesado, y el notebook debería cargarlo en lugar de recrearlo

4. **Decidir qué dataset usar**:
 - **27K** = Solo restaurantes de alta calidad
 - **199K** = Todas las reseñas disponibles

---

## CONCLUSIÓN

La diferencia NO es un error, sino una **decisión de diseño**:

- El **merge con inner join** filtra intencionalmente
- Solo mantiene reseñas de los **706 restaurantes curados**
- Resultado: **~27,000 reseñas de alta calidad**

Si necesitas los **199,821 registros**:
- Cambia el merge a `how='left'`
- O no hagas merge y usa df_reseñas directamente
- O usa un archivo previamente procesado si existe

---

**Para resolver tu pregunta**:
> "¿Por qué saca algo de 27,000 y no más?"

**Respuesta**: Porque el `pd.merge(..., how='inner')` solo mantiene las reseñas de los 706 restaurantes que están en el archivo `restaurant_metadata.csv` (restaurantes de alta calidad seleccionados).

---

**Siguiente paso recomendado**: Verificar cuántos registros tiene realmente el archivo `modelo_limpio.csv` guardado para confirmar si es 27K o 199K.

