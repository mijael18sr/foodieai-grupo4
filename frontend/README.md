# 🍽️ FoodieAI Frontend - React Application

> Frontend del Sistema de Recomendación de Restaurantes con interfaz moderna y responsiva.

[![React](https://img.shields.io/badge/React-18.3-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-cyan.svg)](https://tailwindcss.com/)
[![Vite](https://img.shields.io/badge/Vite-6.0-purple.svg)](https://vitejs.dev/)

## 📋 Contenido

- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Ejecución](#-ejecución)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Componentes Principales](#-componentes-principales)
- [Hooks Personalizados](#-hooks-personalizados)
- [Build y Deploy](#-build-y-deploy)
- [Solución de Problemas](#-solución-de-problemas)

---

## 📦 Requisitos

| Requisito | Versión | Verificar |
|-----------|---------|-----------|
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Espacio disco | 500MB | - |

---

## 🚀 Instalación

### Paso 1: Instalar dependencias

```bash
cd frontend
npm install
```

### Paso 2: Verificar instalación

```bash
npm list react react-dom typescript
```

**Salida esperada:**
```
├── react@18.3.1
├── react-dom@18.3.1
└── typescript@5.6.3
```

---

## ▶️ Ejecución

### Modo Desarrollo

```bash
npm run dev
```

**Salida esperada:**
```
  VITE v6.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Build de Producción

```bash
npm run build
```

### Preview del Build

```bash
npm run preview
```

---

## 📁 Estructura del Proyecto

```
frontend/
├── public/                          # Archivos estáticos públicos
│   ├── foodieai-icon.svg           # Favicon del sistema
│   └── manual-usuario.pdf          # Manual de usuario PDF
├── src/
│   ├── components/                  # Componentes reutilizables
│   │   ├── AIChat/                 # Chat con IA
│   │   ├── Dashboard/              # Panel principal
│   │   ├── Explore/                # Explorar categorías
│   │   ├── Favorites/              # Mis favoritos ⭐
│   │   ├── Header/                 # Cabecera
│   │   ├── Layout/                 # Layout principal
│   │   ├── LocationPickerMap/      # Mapa interactivo 🗺️
│   │   ├── RecommendationsList/    # Lista de recomendaciones
│   │   ├── RestaurantCard/         # Tarjeta de restaurante
│   │   ├── SearchFilters/          # Filtros de búsqueda
│   │   ├── SearchHistory/          # Historial de búsquedas 📜
│   │   ├── Sentiment/              # Panel de sentimientos
│   │   ├── Sidebar/                # Menú lateral
│   │   └── index.ts                # Exportaciones centralizadas
│   ├── hooks/                       # Custom React Hooks
│   │   ├── useApiData.ts           # Datos de la API
│   │   ├── useFavorites.ts         # Gestión de favoritos ⭐
│   │   ├── useLocalStorage.ts      # Persistencia local
│   │   ├── useLocation.ts          # Geolocalización
│   │   ├── useRecommendations.ts   # Recomendaciones ML
│   │   ├── useSearchHistory.ts     # Historial de búsquedas 📜
│   │   └── index.ts                # Exportaciones
│   ├── pages/                       # Páginas principales
│   │   ├── About/                  # Acerca del sistema
│   │   ├── Home/                   # Página principal
│   │   └── Manual/                 # Manual de usuario
│   ├── services/                    # Servicios API
│   │   └── api.ts                  # Cliente REST
│   ├── types/                       # Tipos TypeScript
│   │   └── api.ts                  # Tipos de la API
│   ├── utils/                       # Utilidades
│   │   └── errorHandler.ts         # Manejo de errores
│   ├── App.tsx                      # Componente raíz
│   ├── main.tsx                     # Entry point
│   └── index.css                    # Estilos globales
├── index.html                       # HTML principal
├── package.json                     # Dependencias y scripts
├── tailwind.config.js               # Configuración Tailwind
├── tsconfig.json                    # Configuración TypeScript
├── vite.config.ts                   # Configuración Vite
└── README.md                        # Este archivo
```

---

## 🧩 Componentes Principales

### Layout

El componente `Layout` proporciona la estructura principal con:
- Header responsivo
- Sidebar colapsable con hover
- Área de contenido principal
- Footer informativo

### Dashboard

Panel principal con:
- Estadísticas del sistema
- Accesos rápidos a funcionalidades
- Estado de conexión con el backend

### SearchFilters

Formulario de búsqueda con:
- Selector de ubicación con mapa interactivo 🗺️
- Botón "Usar mi ubicación actual" (GPS)
- Filtros por categoría, distrito, rating
- Control de distancia máxima

### LocationPickerMap

Mapa interactivo estilo Uber con:
- Marcador arrastrable
- Click para seleccionar ubicación
- Reverse geocoding (dirección automática)
- Botón de centrar en ubicación actual

### Favorites

Sistema de favoritos con:
- Guardar restaurantes favoritos
- Persistencia en localStorage
- Eliminar individual o todos
- Badge con contador en sidebar

### SearchHistory

Historial de búsquedas con:
- Últimas 20 búsquedas guardadas
- Top 3 resultados de cada búsqueda
- Botón "Repetir búsqueda"
- Tiempo relativo (hace X minutos)

### SentimentPanel

Análisis de sentimientos con:
- Input para escribir reseñas
- Resultados con porcentajes de confianza
- Visualización de probabilidades
- Colores por tipo de sentimiento

---

## 🪝 Hooks Personalizados

### useApiData

```typescript
const { categories, districts, loading, error } = useApiData();
```
Obtiene categorías y distritos del backend.

### useRecommendations

```typescript
const { recommendations, loading, error, fetchRecommendations } = useRecommendations();
```
Gestiona las recomendaciones de restaurantes.

### useFavorites

```typescript
const { 
  favorites, 
  addFavorite, 
  removeFavorite, 
  toggleFavorite, 
  isFavorite,
  clearFavorites,
  count 
} = useFavorites();
```
Gestión completa de favoritos con persistencia.

### useSearchHistory

```typescript
const { 
  history, 
  addSearch, 
  removeSearch, 
  clearHistory,
  getRecentSearches 
} = useSearchHistory();
```
Historial de búsquedas con persistencia.

### useLocation

```typescript
const { 
  coords, 
  isGeolocationAvailable, 
  isGeolocationEnabled,
  getPosition 
} = useLocation();
```
Acceso a la geolocalización del navegador.

### useLocalStorage

```typescript
const [value, setValue] = useLocalStorage('key', initialValue);
```
Hook genérico para persistencia en localStorage.

---

## 🎨 Tecnologías UI

### Tailwind CSS

Framework CSS utility-first con configuración personalizada:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
      }
    }
  }
}
```

### Iconos

SVG inline para mejor rendimiento y personalización.

### Animaciones

Transiciones suaves con clases de Tailwind:
- `transition-all duration-300`
- `hover:scale-110`
- `animate-pulse`

---

## 🏗️ Build y Deploy

### Build de Producción

```bash
npm run build
```

**Output:**
```
dist/
├── index.html
└── assets/
    ├── index-*.css    (~125KB)
    ├── index-*.js     (~570KB)
    └── Home-*.js      (~80KB)
```

### Variables de Entorno

Crear `.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=FoodieAI
```

Para producción `.env.production`:

```env
VITE_API_BASE_URL=https://foodie.softprimesolutions.com
VITE_APP_TITLE=FoodieAI
```

### Deploy a Servidor

```bash
# Build
npm run build

# Copiar dist/ al servidor
scp -r dist/* user@server:/var/www/html/
```

---

## 🐳 Docker

### Build

```bash
docker build -t foodieai-frontend .
```

### Run

```bash
docker run -d -p 80:80 --name foodieai-web foodieai-frontend
```

---

## 🧪 Testing

### Linting

```bash
npm run lint
```

### Type Check

```bash
npm run type-check
# o
tsc --noEmit
```

### Tests (si están configurados)

```bash
npm run test
```

---

## 🐛 Solución de Problemas

### Error: "npm install fails"

```bash
# Limpiar cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Error: "Module not found"

```bash
# Reinstalar dependencias
rm -rf node_modules
npm install
```

### Error: "CORS blocked"

Verificar que el backend tenga CORS configurado:
```python
# backend/src/presentation/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: "Map not loading"

Verificar conexión a internet (Leaflet usa tiles de OpenStreetMap).

### Error: "Geolocation denied"

El usuario debe permitir acceso a ubicación en el navegador.

### Build muy grande (>500KB warning)

Es normal para aplicaciones React. El code-splitting está optimizado.

---

## 📱 Responsividad

El diseño es mobile-first y se adapta a:

| Breakpoint | Tamaño | Descripción |
|------------|--------|-------------|
| `sm` | 640px | Móviles grandes |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktop |
| `2xl` | 1536px | Pantallas grandes |

---

## 🔌 Conexión con Backend

### URL Base

```typescript
// src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

### Endpoints utilizados

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/categories` | GET | Lista categorías |
| `/api/v1/districts` | GET | Lista distritos |
| `/api/v1/recommendations` | POST | Obtener recomendaciones |
| `/api/v1/sentiment/analyze` | POST | Análisis de sentimiento |

---

## 📚 Scripts Disponibles

| Script | Comando | Descripción |
|--------|---------|-------------|
| dev | `npm run dev` | Servidor desarrollo |
| build | `npm run build` | Build producción |
| preview | `npm run preview` | Preview del build |
| lint | `npm run lint` | Ejecutar ESLint |

---

## 🔗 Enlaces

- **Producción:** https://foodie.softprimesolutions.com
- **API Docs:** https://foodie.softprimesolutions.com/api/v1/docs
- **Repositorio:** https://github.com/mijael18sr/foodieai-grupo4

---

## 📄 Archivos de Configuración

### vite.config.ts

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### tsconfig.json

- Target: ES2020
- Strict mode: enabled
- Path aliases: `@/*` → `src/*`

### tailwind.config.js

- Content: `./src/**/*.{ts,tsx}`
- Plugins: forms, typography

---

*Desarrollado para UNMSM - Postgrado en Machine Learning*
