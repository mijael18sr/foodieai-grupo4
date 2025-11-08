# DATOS DEL PROYECTO

**Estado**: Archivos grandes no incluidos en GitHub (límite 100MB)
**Solución**: Regenerar localmente con scripts incluidos

---

## ARCHIVOS FALTANTES (>100MB)

- `Lima_Restaurants_2025_08_13.csv` (131MB) - Dataset original
- `Lima_Restaurants_2025_08_13_clean.csv` (131MB) - Limpio sin emojis  
- `reviews_con_sentimiento.csv` (138MB) - Con análisis de sentimientos
- `modelo_limpio.csv` (52MB) - Dataset para entrenar ML

---

## REGENERACIÓN RÁPIDA (5-10 min)

### 1. Obtener Dataset Original
Descargar desde [Kaggle - Lima Restaurant Review](https://www.kaggle.com/datasets/bandrehc/lima-restaurant-review)
Colocar en: `backend/data/raw/Lima_Restaurants_2025_08_13.csv`

### 2. Ejecutar Scripts
```bash
cd backend
.venv\Scripts\activate

python scripts/clean_emojis.py                # → *_clean.csv
python scripts/data_cleaning_pipeline.py      # → reviews_con_sentimiento.csv
python reentrenar_modelo_limpio.py           # → modelo_limpio.csv
```

### 3. Verificar
```bash
python ../verify_github_ready.py
```

---

## INICIO RÁPIDO

```bash
# Clonar y setup
git clone https://github.com/mijael18sr/foodieai-grupo4.git
cd foodieai-grupo4/backend

# Instalar dependencias
python -m venv .venv
.venv\Scripts\activate  
pip install -r requirements.txt

# Obtener datos + regenerar + iniciar
# (Descargar CSV de Kaggle primero)
python scripts/clean_emojis.py
python scripts/data_cleaning_pipeline.py
python reentrenar_modelo_limpio.py
python start_server.py
```

**Total**: ~10-15 minutos incluyendo descarga