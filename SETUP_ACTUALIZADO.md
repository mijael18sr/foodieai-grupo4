# Guía de Setup Actualizada - Restaurant Recommender

## Cambios Recientes

- **Eliminado:** `wordcloud` del requirements.txt (no se necesita para el funcionamiento)
- **Mantenido:** Todas las dependencias esenciales para ML y API
- **Optimizado:** Dependencies más ligeras para instalación rápida

---

## INICIO RÁPIDO - 3 Minutos

### Comando Todo-en-Uno (Copia y Pega)

```bash
# Backend (Terminal 1)
cd backend
python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
python start_server.py

# Frontend (Terminal 2) - EN OTRA VENTANA
cd frontend
npm install && npm run dev

# Listo: Backend en http://localhost:8000/docs
# Listo: Frontend en http://localhost:5173
```

---

## Dependencias Actualizadas

### Backend (Python) - requirements.txt
```
 fastapi==0.104.1 # API REST moderna
 uvicorn[standard]==0.24.0 # Servidor ASGI
 pandas # Manejo de datos
 scikit-learn # Machine Learning
 nltk>=3.8 # Análisis de sentimientos
 matplotlib # Gráficos
 seaborn # Visualizaciones
 pytest # Testing
 prometheus-client # Monitoring
 wordcloud # ELIMINADO (no necesario)
```

### Frontend (Node.js) - package.json
```
 react@19.1.1 # UI Framework
 typescript@5.9.3 # Tipos estáticos
 vite@7.1.7 # Build tool
 tailwindcss@4.1.14 # CSS Framework
 axios@1.12.2 # Cliente HTTP
 react-router-dom@7.9.4 # Enrutamiento
```

---

## Instrucciones Paso a Paso

### 1⃣ BACKEND

```bash
# Navegar al backend
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias (SIN wordcloud)
pip install -r requirements.txt

# Descargar recursos NLTK
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Verificar instalación
pip list | findstr fastapi
# Debería mostrar: fastapi 0.104.1

# Iniciar servidor
python start_server.py
```

** Resultado esperado:**
```
 Iniciando Restaurant Recommender API...
 Backend URL: http://localhost:8000
 API Docs: http://localhost:8000/docs
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 2⃣ FRONTEND

```bash
# NUEVA VENTANA DE TERMINAL
cd C:\AmbDesarrollo\POSTGRADO-SAN-MARCOS\MACHINE-LEARNING\restaurant-recommender-ml\frontend

# Instalar dependencias Node.js
npm install

# Verificar instalación
npm list react
# Debería mostrar: react@19.1.1

# Iniciar desarrollo
npm run dev
```

** Resultado esperado:**
```
 VITE v7.1.7 ready in 1234 ms
 Local: http://localhost:5173/
 Network: use --host to expose
```

---

## Verificación Final

### Test 1: Backend Health
```bash
# En navegador o PowerShell
Invoke-WebRequest -Uri http://localhost:8000/api/v1/health -UseBasicParsing
```
**Esperado:** `{"status":"healthy"}`

### Test 2: Frontend Loading
```bash
# Abrir navegador en:
http://localhost:5173
```
**Esperado:** Aplicación React carga correctamente

### Test 3: API Docs
```bash
# Abrir navegador en:
http://localhost:8000/docs
```
**Esperado:** Documentación Swagger interactiva

---

## Solución de Problemas

### Error: "No module named 'wordcloud'"

**Causa:** Algún script aún referencia wordcloud 
**Solución:** 
```bash
# Buscar referencias
grep -r "wordcloud" backend/src/
# Comentar o eliminar las líneas que importan wordcloud
```

### Error: "Failed building wheel for X"

**Causa:** Falta compilador C++ para algunos paquetes 
**Solución:**
```bash
# Instalar Microsoft C++ Build Tools
# O usar versiones binarias:
pip install --only-binary=all -r requirements.txt
```

### Error: "Port already in use"

**Solución:**
```bash
# Windows - Matar proceso en puerto
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>
```

---

## Checklist de Verificación

Antes de decir "¡Funciona!":

- [ ] **Python 3.10+** instalado (`python --version`)
- [ ] **Node.js 18+** instalado (`node --version`)
- [ ] **Entorno virtual** activado (ves `(.venv)` en terminal)
- [ ] **Backend deps** instalados (no aparece wordcloud en `pip list`)
- [ ] **Frontend deps** instalados (`npm list` muestra react@19.1.1)
- [ ] **NLTK resources** descargados
- [ ] **Backend** inicia sin errores (puerto 8000)
- [ ] **Frontend** inicia sin errores (puerto 5173)
- [ ] **Health check** responde OK
- [ ] **API Docs** accesibles
- [ ] **Frontend** carga en navegador

---

## URLs de Verificación

Después de ejecutar ambos servidores:

| Servicio | URL | Estado Esperado |
|----------|-----|-----------------|
| **Backend API** | http://localhost:8000 | {"message": "Restaurant Recommender API"} |
| **Health Check** | http://localhost:8000/api/v1/health | {"status": "healthy"} |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Frontend App** | http://localhost:5173 | React App carga |

---

## Siguiente Paso

Una vez que todo funciona:

1. **Probar recomendaciones** en http://localhost:8000/docs
2. **Usar la interfaz** en http://localhost:5173
3. **Ver métricas** del modelo en `/docs`

---

## Comandos de Desarrollo Diario

```bash
# Iniciar desarrollo - Backend
cd backend && .venv\Scripts\activate && python start_server.py

# Iniciar desarrollo - Frontend 
cd frontend && npm run dev

# Test API
cd backend && python test_api_funcionando.py

# Diagnosticar modelo
cd backend && python diagnosticar_modelo.py
```

---

** ¡Proyecto listo sin wordcloud! Todo optimizado y funcionando.**