# 🚀 Inicio Rápido - 3 Comandos

> **Para nuevos usuarios que clonen el repositorio**

## ⚡ Ejecución Inmediata (5 minutos)

### 🐍 Backend (Terminal 1):
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
python start_server.py
```

### ⚛️ Frontend (Terminal 2):
```bash
cd frontend  
npm install
npm run dev
```

### ✅ Verificar:
- **Backend API:** http://localhost:8000/docs
- **Frontend App:** http://localhost:5173

---

## 🎯 Lo que obtienes:

- **✅ Modelo de IA preentrenado** (84.36% accuracy)
- **✅ Sistema de recomendación** completo
- **✅ API REST** con documentación interactiva
- **✅ Interfaz moderna** React + TypeScript
- **✅ 706 restaurantes** + 378,969 reviews

---

## 🆘 ¿Problemas?

1. **Verifica Python 3.10+:** `python --version`
2. **Verifica Node.js 18+:** `node --version`
3. **Lee el README.md** completo
4. **Ejecuta diagnóstico:** `python backend/diagnosticar_modelo.py`

---

**🌟 ¡Dale una estrella si te gustó el proyecto! ⭐**