# 🚀 Guía de Despliegue y Configuración

## 📦 Archivos Esenciales para GitHub

### ✅ Archivos que DEBEN incluirse en el repositorio:

#### 🗂️ Configuración del Proyecto
- `README.md` - Documentación principal ⭐
- `.gitignore` - Archivos a ignorar por Git
- `requirements.txt` - Dependencias Python (backend)
- `package.json` - Dependencias Node.js (frontend)

#### 💾 Datos Críticos 
- `backend/data/raw/Lima_Restaurants_2025_08_13_clean.csv` ⭐
- `backend/data/raw/restaurant_metadata.csv`

#### 🤖 Modelos Preentrenados (INCLUIR)
- `backend/data/models/sentiment_model.pkl` ⭐ (84.36% accuracy)
- `backend/data/models/clustering_model.pkl`
- `backend/data/models/rating_predictor.pkl` 
- `backend/data/models/recommender_system.pkl`

#### 🔧 Scripts Ejecutables
- `backend/start_server.py` ⭐
- `backend/reentrenar_modelo_limpio.py` ⭐
- `backend/test_api_funcionando.py`
- `backend/diagnosticar_modelo.py`

---

## 🚫 Archivos que NO subir a GitHub

### 📁 Carpetas automáticamente excluidas por `.gitignore`:
- `node_modules/` - Dependencias Node.js (se instalan con npm)
- `__pycache__/` - Cache Python
- `.venv/` - Entornos virtuales Python
- `*.log` - Archivos de log
- `.env` - Variables de entorno sensibles

### 💾 Datos que se regeneran:
- `backend/data/processed/` - Se recrean con el pipeline
- `backend/data/models/backups/` - Backups innecesarios

---

## 📋 Checklist Pre-GitHub

### ✅ Antes de hacer el primer commit:

```bash
# 1. Verificar que tienes los archivos esenciales
ls backend/data/models/
# Debe mostrar: sentiment_model.pkl, clustering_model.pkl, rating_predictor.pkl, recommender_system.pkl

ls backend/data/raw/
# Debe mostrar: Lima_Restaurants_2025_08_13_clean.csv

# 2. Verificar que el .gitignore está configurado
cat .gitignore | grep -E "(node_modules|__pycache__|\.venv)"

# 3. Test rápido del backend
cd backend
python -c "import pickle; print('✅ Models OK')"

# 4. Test rápido del frontend  
cd frontend
npm list --depth=0 2>/dev/null && echo "✅ Dependencies OK" || echo "❌ Run npm install"
```

---

## 🔄 Comandos Git Recomendados

### 🆕 Primer setup del repositorio:

```bash
# 1. Inicializar Git (si no está inicializado)
git init

# 2. Agregar remote origin
git remote add origin https://github.com/TU-USUARIO/restaurant-recommender-ml.git

# 3. Agregar todos los archivos esenciales
git add .

# 4. Primer commit
git commit -m "🎉 Initial commit: Restaurant Recommender ML System

✅ Backend FastAPI con modelos preentrenados
✅ Frontend React con TypeScript  
✅ Modelo de sentimientos (84.36% accuracy)
✅ Sistema de recomendación completo
✅ Documentación completa

Funcional desde el primer clone 🚀"

# 5. Push inicial
git push -u origin main
```

### 🔄 Workflow diario de desarrollo:

```bash
# Crear rama para nueva feature
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y agregar
git add .
git commit -m "feat: descripción del cambio"

# Push y crear PR
git push origin feature/nueva-funcionalidad
```

---

## 🌐 Variables de Entorno para Producción

### 📄 `backend/.env.example` (crear este archivo):

```env
# ===========================================
# 🚀 Restaurant Recommender - Backend Config
# ===========================================

# 🌐 Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
ENVIRONMENT=production

# 📊 ML Configuration
MODEL_PATH=data/models/
DATA_PATH=data/
SENTIMENT_MODEL=sentiment_model.pkl
CLUSTERING_MODEL=clustering_model.pkl

# 🔒 CORS Configuration  
FRONTEND_URL=https://tu-app.vercel.app
ALLOWED_ORIGINS=["https://tu-app.vercel.app","http://localhost:3000"]

# 📈 Monitoring (opcional)
ENABLE_METRICS=true
LOG_LEVEL=INFO

# 💾 Database (futuro)
# DATABASE_URL=postgresql://user:pass@localhost:5432/restaurant_db
```

### 📄 `frontend/.env.example` (crear este archivo):

```env
# ===========================================
# ⚛️ Restaurant Recommender - Frontend Config  
# ===========================================

# 🌐 API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000

# 🎨 App Configuration
VITE_APP_NAME="Restaurant Recommender"
VITE_APP_VERSION="1.0.0"
VITE_APP_DESCRIPTION="Sistema IA de Recomendación de Restaurantes"

# 📍 Maps Configuration (futuro)
# VITE_GOOGLE_MAPS_API_KEY=tu-api-key
# VITE_DEFAULT_LAT=-12.0464
# VITE_DEFAULT_LNG=-77.0428

# 🔧 Development
VITE_ENABLE_DEVTOOLS=false
```

---

## 🐳 Preparación para Docker (Futuro)

### 📄 `Dockerfile.backend`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar recursos NLTK
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Copiar código
COPY backend/ .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["python", "start_server.py"]
```

### 📄 `Dockerfile.frontend`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Instalar dependencias
COPY frontend/package*.json ./
RUN npm ci

# Build app
COPY frontend/ .
RUN npm run build

# Servidor Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 📄 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: 
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./backend/data:/app/data

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend  
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_BASE_URL=http://localhost:8000
```

---

## ☁️ Deploy en Plataformas Cloud

### 🟢 Vercel (Frontend React)

1. **Conectar repositorio** a Vercel
2. **Framework preset:** Vite
3. **Build command:** `npm run build`
4. **Output directory:** `dist`
5. **Environment variables:** Agregar desde `.env.example`

### 🟣 Railway/Heroku (Backend FastAPI)

```bash
# 1. Instalar CLI
npm install -g railway

# 2. Login y deploy
railway login
railway init
railway up
```

**Variables de entorno en Railway:**
```
API_HOST=0.0.0.0
API_PORT=$PORT
DEBUG=false
ENVIRONMENT=production
```

### ⚡ Netlify (Frontend alternativo)

```bash
# 1. Build settings
Build command: npm run build
Publish directory: dist
```

---

## 📊 Monitoring y Logs

### 📈 Métricas importantes a monitorear:

```python
# En production, agregar logging:
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Métricas de rendimiento
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logging.info(f"Request {request.url} processed in {process_time:.4f}s")
    return response
```

---

## ⚡ Performance Tips

### 🚀 Backend Optimization:

1. **Lazy loading de modelos:**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1)
   def load_model():
       return joblib.load('sentiment_model.pkl')
   ```

2. **Async endpoints:**
   ```python
   @app.post("/recommendations")
   async def get_recommendations(request: RecommendationRequest):
       # Procesar async
   ```

3. **Cache con Redis** (futuro)

### ⚛️ Frontend Optimization:

1. **Lazy loading de componentes:**
   ```tsx
   const HomePage = lazy(() => import('./pages/HomePage'));
   ```

2. **Memoización:**
   ```tsx
   const MemoizedCard = memo(RestaurantCard);
   ```

3. **Bundle optimization en `vite.config.ts`:**
   ```ts
   export default defineConfig({
     build: {
       chunkSizeWarningLimit: 1000,
       rollupOptions: {
         output: {
           manualChunks(id) {
             if (id.includes('node_modules')) {
               return 'vendor';
             }
           }
         }
       }
     }
   });
   ```

---

## 🔒 Security Checklist

### ✅ Backend Security:

- [ ] **CORS** configurado correctamente
- [ ] **Rate limiting** implementado
- [ ] **Input validation** con Pydantic
- [ ] **Error handling** sin información sensible
- [ ] **HTTPS** en producción

### ✅ Frontend Security:

- [ ] **Environment variables** no sensibles en build
- [ ] **CSP headers** configurados
- [ ] **Sanitización** de inputs del usuario
- [ ] **HTTPS** obligatorio

---

## 🎯 Recursos Post-Deploy

### 📊 Analytics y Monitoring:

- **Backend:** Sentry, New Relic
- **Frontend:** Google Analytics, Hotjar  
- **Infrastructure:** Grafana, Prometheus

### 📱 SEO y Performance:

- **Lighthouse CI** para métricas
- **Meta tags** optimizados
- **Open Graph** para social media

---

## ✅ Final Checklist

Antes de considerar el proyecto "GitHub Ready":

### 📋 Documentación:
- [ ] ✅ README.md completo y claro
- [ ] ✅ .gitignore configurado
- [ ] ✅ Dependencias documentadas (requirements.txt, package.json)
- [ ] ✅ Ejemplos de .env files

### 🤖 Funcionalidad:
- [ ] ✅ Modelos ML incluidos y funcionando
- [ ] ✅ Backend API documentada (Swagger)
- [ ] ✅ Frontend compilando sin errores
- [ ] ✅ Tests básicos pasando

### 🚀 Usabilidad:
- [ ] ✅ Instrucciones de instalación claras
- [ ] ✅ Comandos de inicio simples
- [ ] ✅ Troubleshooting documentado
- [ ] ✅ Ejemplos de uso incluidos

---

**🎉 ¡Proyecto listo para compartir en GitHub! 🚀**