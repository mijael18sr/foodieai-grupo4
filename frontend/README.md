# Frontend - Restaurant Recommender

Interfaz React moderna para el sistema de recomendación de restaurantes de Lima.

## Tecnologías

- **React 19** + **TypeScript** - UI library moderna
- **Vite** - Build tool ultrarrápido
- **Tailwind CSS** - Framework CSS utility-first
- **React Router** - Enrutamiento SPA
- **Axios** - Cliente HTTP para consumir FastAPI
- **React Icons** - Sistema de iconos centralizado
- **Error Boundaries** - Manejo robusto de errores

## Desarrollo

### Instalar dependencias
```bash
npm install
```

### Ejecutar en desarrollo
```bash
npm run dev
```

### Build para producción
```bash
npm run build
```

### Previsualizar build
```bash
npm run preview
```

## Estructura Arquitectural

```
src/
 components/ # Componentes reutilizables
 RestaurantCard/ # Tarjeta de restaurante
 SearchFilters/ # Filtros de búsqueda
 RecommendationsList/ # Lista de recomendaciones
 Icons/ # Sistema de iconos centralizado
 ErrorBoundary/ # Manejo de errores
 Layout/ # Layout principal
 pages/ # Páginas principales
 Home/ # Página principal con lazy loading
 hooks/ # Custom React hooks
 useRecommendations.ts
 useApiData.ts
 services/ # Servicios de API
 api.ts # Cliente FastAPI optimizado
 types/ # Definiciones TypeScript
 api.ts # Tipos de la API
 constants/ # Configuraciones centralizadas
 config.ts # Constantes de la app
 utils/ # Funciones de utilidad
 index.ts # Helpers y utilidades
 App.tsx # Componente raíz con Error Boundary
```

## Funcionalidades {

 files: ['**/*.{ts,tsx}'],

### Búsqueda Inteligente extends: [

- Filtros por categoría, distrito, rating // Other configs...

- Control de distancia máxima // Enable lint rules for React

- Número configurable de resultados reactX.configs['recommended-typescript'],

 // Enable lint rules for React DOM

### Geolocalización reactDom.configs.recommended,

- Ubicación manual (lat/long) ],

- Detección automática GPS languageOptions: {

- Ubicación por defecto (Centro Lima) parserOptions: {

 project: ['./tsconfig.node.json', './tsconfig.app.json'],

### Resultados Visuales tsconfigRootDir: import.meta.dirname,

- Cards de restaurantes con información completa },

- Rankings visuales // other options...

- Métricas de búsqueda },

- Estadísticas de resultados },

])

## API Integration```


El frontend consume la FastAPI backend a través de:

```typescript
// Ejemplo de uso del servicio API
import RestaurantApiService from './services/api';

// Obtener recomendaciones
const recommendations = await RestaurantApiService.getRecommendations({
 user_location: { lat: -12.0464, long: -77.0428 },
 preferences: { category: "Peruana" },
 filters: { min_rating: 4.0, max_distance_km: 5.0 },
 top_n: 10
});
```

---

**Desarrollado con para UNMSM - Machine Learning**