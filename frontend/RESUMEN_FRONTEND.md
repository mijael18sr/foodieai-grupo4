# FRONTEND - RESTAURANT RECOMMENDER

**Tecnología**: React 19 + TypeScript + Tailwind CSS
**Build Tool**: Vite
**Fecha**: Noviembre 2025

---

## STACK TECNOLÓGICO

### Core
- **React 19** - UI library moderna
- **TypeScript** - Tipado estático
- **Vite** - Build tool ultrarrápido
- **Tailwind CSS** - Framework CSS utility-first

### Librerías Adicionales
- **React Router** - Enrutamiento SPA
- **Axios** - Cliente HTTP para FastAPI
- **React Icons** - Sistema de iconos
- **Error Boundaries** - Manejo de errores

---

## COMANDOS PRINCIPALES

```bash
npm install          # Instalar dependencias
npm run dev          # Desarrollo (localhost:5173)
npm run build        # Build para producción
npm run preview      # Previsualizar build
```

---

## ARQUITECTURA

```
src/
├── components/      # Componentes reutilizables
│   ├── RestaurantCard/
│   ├── SearchFilters/
│   ├── RecommendationsList/
│   └── ErrorBoundary/
├── pages/          # Páginas principales
│   └── Home/
├── hooks/          # Custom React hooks
├── services/       # Cliente API
├── types/          # Definiciones TypeScript
├── constants/      # Configuraciones
└── utils/          # Funciones utilidad
```

---

## FUNCIONALIDADES

### Búsqueda Inteligente
- Filtros por categoría, distrito, rating
- Control de distancia máxima
- Número configurable de resultados

### Geolocalización
- Ubicación manual (lat/long)
- Detección automática GPS
- Ubicación por defecto (Centro Lima)

### Resultados Visuales
- Cards de restaurantes con información completa
- Rankings visuales y métricas
- Estadísticas de resultados

## SISTEMA DE ICONOS

### Centralizado en `/src/components/Icons/`
- **Material Design Icons (MD)**: Restaurantes, ubicación, navegación
- **Font Awesome Icons (FA)**: Edificios, usuarios, redes sociales  
- **Heroicons (HI)**: Efectos especiales, comunicación

### Uso
```tsx
import { MdRestaurant, FaBuilding, getIconProps } from '../components/Icons';

// Básico
<MdRestaurant className="text-xl text-blue-600" />

// Con helper
<MdRestaurant {...getIconProps('lg', 'primary')} />
```

### Tamaños y Colores
- **Tamaños**: xs(12px), sm(16px), md(20px), lg(24px), xl(32px), 2xl(48px)
- **Colores**: primary, secondary, success, warning, error, white, black

---

## INTEGRACIÓN CON API

```typescript
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

## CONVENCIONES DE CÓDIGO

### Nomenclatura
- **Componentes**: PascalCase (`RestaurantCard.tsx`)
- **Hooks**: camelCase con "use" (`useApiData.ts`)
- **Variables**: camelCase (`userName`, `isLoading`)
- **Constantes**: UPPER_SNAKE_CASE (`API_CONFIG`)

### Estructura de Componentes
```tsx
export const RestaurantCard = memo(({ 
  restaurant, 
  onSelect 
}: RestaurantCardProps) => {
  // Component logic
});
```

### TypeScript
```tsx
// Interfaces para props
interface RestaurantCardProps {
  restaurant: Restaurant;
  onSelect: (id: string) => void;
  isSelected?: boolean;
}

// Types para uniones
type LoadingState = 'idle' | 'loading' | 'success' | 'error';
```

---

## BEST PRACTICES

### Performance
- `memo()` para componentes que renderizan frecuentemente
- `useMemo()` y `useCallback()` para optimizaciones
- Lazy loading y code splitting

### Accesibilidad
- Elementos semánticos HTML
- `aria-label` y `role` apropiados
- Navegación por teclado
- Contraste adecuado

### Error Handling
- Error boundaries para componentes
- Try-catch en funciones async
- Validación de tipos
- Mensajes user-friendly

---

## COMMITS Y BRANCHES

### Convenciones de Commit
- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Documentación
- `style:` Formateo/estilos
- `refactor:` Refactorización

### Branches
- `feature/` - Nuevas funcionalidades
- `fix/` - Correcciones
- `refactor/` - Refactorizaciones

---

**Desarrollado para UNMSM - Machine Learning**