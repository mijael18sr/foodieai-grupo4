# Restaurant Recommender - Guía de Estilo y Convenciones

## Convenciones de Nomenclatura

### Archivos y Carpetas
- **Componentes**: PascalCase (`RestaurantCard.tsx`, `SearchFilters.tsx`)
- **Hooks**: camelCase con prefijo "use" (`useApiData.ts`, `useRecommendations.ts`)
- **Utilidades**: camelCase (`index.ts`, `config.ts`)
- **Tipos**: camelCase (`api.ts`, `index.ts`)
- **Carpetas**: PascalCase para componentes, camelCase para otros (`Header/`, `services/`)

### Variables y Funciones
- **Variables**: camelCase (`userName`, `isLoading`, `restaurantData`)
- **Funciones**: camelCase (`fetchData`, `handleClick`, `formatDistance`)
- **Constantes**: UPPER_SNAKE_CASE (`API_CONFIG`, `DEFAULT_LOCATION`)
- **Componentes**: PascalCase (`RestaurantCard`, `SearchFilters`)

### Clases CSS
- **Utilidades Tailwind**: Como están definidas (`bg-blue-500`, `text-center`)
- **Clases personalizadas**: kebab-case (`sidebar-transition`, `footer-responsive`)

### Props y Interfaces
- **Props**: camelCase (`isOpen`, `onToggle`, `restaurantData`)
- **Interfaces**: PascalCase (`Restaurant`, `ApiError`, `UserLocation`)
- **Tipos**: PascalCase (`RecommendationResponse`, `HealthResponse`)

## Estructura de Archivos

```
src/
 components/
 ComponentName/
 ComponentName.tsx
 index.ts
 index.ts
 hooks/
 useHookName.ts
 index.ts
 services/
 api.ts
 index.ts
 types/
 api.ts
 index.ts
 utils/
 index.ts
 helpers.ts
 constants/
 config.ts
 pages/
 PageName/
 PageName.tsx
 index.ts
 index.ts
```

## Convenciones de Código

### React Components
```tsx
// Correcto
export const RestaurantCard = memo(({ restaurant, onSelect }: RestaurantCardProps) => {
 // Component logic
});

// Incorrecto
export default function restaurantCard(props: any) {
 // Component logic
}
```

### Hooks
```tsx
// Correcto
export function useApiData(): UseApiDataReturn {
 const [data, setData] = useState<DataType[]>([]);
 // Hook logic
 return { data, loading, error };
}

// Incorrecto
export const useApiData = () => {
 // Hook logic without types
}
```

### API Services
```tsx
// Correcto
export class RestaurantApiService {
 static async getRecommendations(request: RecommendationRequest): Promise<RecommendationResponse> {
 // Service logic
 }
}

// Incorrecto
export const api = {
 getRecommendations: (data: any) => {
 // Service logic
 }
}
```

### Constants
```tsx
// Correcto
export const API_CONFIG = {
 BASE_URL: 'http://localhost:8000',
 TIMEOUT: 10000,
} as const;

// Incorrecto
export const apiConfig = {
 baseUrl: 'http://localhost:8000',
 timeout: 10000,
};
```

## Convenciones de Git

### Commits
- **feat**: Nueva funcionalidad
- **fix**: Corrección de errores
- **docs**: Documentación
- **style**: Formateo, estilos
- **refactor**: Refactorización
- **test**: Tests
- **chore**: Mantenimiento

Ejemplo: `feat: add restaurant recommendation filters`

### Branches
- **feature/**: Nuevas funcionalidades (`feature/restaurant-filters`)
- **fix/**: Correcciones (`fix/api-timeout-error`)
- **refactor/**: Refactorizaciones (`refactor/component-structure`)

## Convenciones de TypeScript

### Tipos e Interfaces
```tsx
// Interfaces para props y objetos
interface RestaurantCardProps {
 restaurant: Restaurant;
 onSelect: (id: string) => void;
 isSelected?: boolean;
}

// Types para uniones y primitivos
type LoadingState = 'idle' | 'loading' | 'success' | 'error';
type ApiResponse<T> = T | null;
```

### Imports
```tsx
// Correcto - imports agrupados y ordenados
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';

import { RestaurantCard, SearchFilters } from './components';
import { useApiData } from './hooks';
import { RestaurantApiService } from './services';
import type { Restaurant, ApiError } from './types';
```

## Best Practices

### Performance
- Use `memo()` para componentes que renderizan frecuentemente
- Use `useMemo()` y `useCallback()` para cálculos y funciones costosas
- Lazy loading para componentes no críticos
- Code splitting para rutas

### Accessibility
- Usar elementos semánticos HTML
- Agregar `aria-label` y `role` cuando sea necesario
- Soporte para navegación por teclado
- Contraste adecuado de colores

### Error Handling
- Error boundaries para componentes
- Try-catch en funciones async
- Validación de tipos en tiempo de ejecución
- Mensajes de error user-friendly

### Security
- Usar `globalThis` en lugar de `window`
- Validar inputs del usuario
- Sanitizar datos de APIs externas
- No exponer información sensible en el cliente