# Datos del Proyecto - Instrucciones de Descarga

> **Algunos archivos de datos grandes no están incluidos en el repositorio de GitHub debido a restricciones de tamaño (100MB máx.)**

## Archivos No Incluidos en GitHub

Los siguientes archivos deben descargarse por separado o regenerarse localmente:

### Datasets Principales (>100MB)
- `Lima_Restaurants_2025_08_13.csv` (131.51 MB)
- `Lima_Restaurants_2025_08_13_clean.csv` (131.37 MB)
- `reviews_con_sentimiento.csv` (138.27 MB)
- `modelo_limpio.csv` (51.74 MB)

---

## OPCIÓN A: Descargar Archivos Originales

### 1. Dataset Original desde Kaggle

```bash
# Descargar el dataset original desde:
# https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review

# Colocar el archivo descargado en:
# backend/data/raw/Lima_Restaurants_2025_08_13.csv
```

### 2. Archivos Procesados desde Google Drive/OneDrive

** Enlaces de descarga:** *(Compartir estos enlaces con el equipo)*

- [Lima_Restaurants_2025_08_13_clean.csv](AGREGAR_ENLACE_AQUI)
- [reviews_con_sentimiento.csv](AGREGAR_ENLACE_AQUI)
- [modelo_limpio.csv](AGREGAR_ENLACE_AQUI)

** Ubicaciones correctas:**
```
backend/data/raw/Lima_Restaurants_2025_08_13_clean.csv
backend/data/processed/reviews_con_sentimiento.csv
backend/data/processed/modelo_limpio.csv
```

---

## OPCIÓN B: Regenerar Localmente (Recomendado)

### Regeneración Rápida (5-10 minutos)

```bash
cd backend

# 1. Activar entorno virtual
.venv\Scripts\activate

# 2. Descargar dataset original y colocarlo en data/raw/
# (Lima_Restaurants_2025_08_13.csv desde Kaggle)

# 3. Ejecutar pipeline de limpieza
python scripts/clean_emojis.py # Genera *_clean.csv
python scripts/data_cleaning_pipeline.py # Genera archivos procesados
python reentrenar_modelo_limpio.py # Genera modelo_limpio.csv
```

### Scripts de Regeneración Disponibles

| Script | Genera | Tiempo Estimado |
|--------|--------|-----------------|
| `scripts/clean_emojis.py` | `Lima_Restaurants_2025_08_13_clean.csv` | 2-3 min |
| `scripts/data_cleaning_pipeline.py` | `reviews_con_sentimiento.csv` + otros | 5-7 min |
| `reentrenar_modelo_limpio.py` | `modelo_limpio.csv` | 3-5 min |

---

## Verificar Archivos Completos

### Script de Verificación

```bash
cd backend
python ../verify_github_ready.py
```

### Checklist Manual

```bash
# Verificar que existen estos archivos:
ls backend/data/raw/Lima_Restaurants_2025_08_13_clean.csv # ~131MB
ls backend/data/processed/reviews_con_sentimiento.csv # ~138MB
ls backend/data/processed/modelo_limpio.csv # ~52MB
```

---

## ¿Por qué No Están en GitHub?

### Limitaciones de GitHub
- **Límite por archivo:** 100 MB máximo
- **Aviso de advertencia:** 50 MB
- **Repositorio completo:** Recomendado < 1 GB

### Mejores Prácticas
- ** Incluir:** Código, modelos ML pequeños, configuración
- ** Excluir:** Datasets grandes, archivos temporales, cachés
- ** Regenerar:** Usar scripts para recrear datos procesados

---

## Inicio Rápido para Nuevos Desarrolladores

### Si eres nuevo en el proyecto:

```bash
# 1. Clonar repositorio
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd foodieai-grupo4

# 2. Setup backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 3. Descargar dataset original desde Kaggle a:
# backend/data/raw/Lima_Restaurants_2025_08_13.csv

# 4. Regenerar datos procesados
python scripts/clean_emojis.py
python scripts/data_cleaning_pipeline.py
python reentrenar_modelo_limpio.py

# 5. Iniciar servidor
python start_server.py

# 6. Setup frontend (nueva terminal)
cd ../frontend
npm install
npm run dev
```

** Tiempo total:** 10-15 minutos (incluyendo descarga de Kaggle)

---

## Soporte

### ¿Problemas con los datos?

1. **Verifica las rutas** de los archivos
2. **Ejecuta el script de verificación:** `python verify_github_ready.py`
3. **Revisa el README principal** para troubleshooting
4. **Contacta al equipo** si persisten los problemas

### Enlaces Útiles

- **Dataset Original:** [Kaggle - Lima Restaurant Review](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)
- **GitHub LFS:** [Documentación](https://git-lfs.github.com/) (para futuras versiones)
- **README Principal:** [README.md](../README.md)

---

** Tip:** Una vez que tengas los archivos, el sistema funcionará completamente sin necesidad de internet para las recomendaciones.