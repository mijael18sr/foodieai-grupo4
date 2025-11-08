# Sistema de Iconos Centralizado

## Descripción
El sistema de iconos centralizado en `/src/components/Icons/` proporciona una forma organizada y consistente de manejar todos los iconos en la aplicación.

## Beneficios

### **Organización**
- Todos los iconos en un solo lugar
- Categorización por familia de iconos
- Fácil búsqueda y descubrimiento

### **Mantenibilidad**
- Cambios globales desde un solo archivo
- Actualizaciones de versiones simplificadas
- Mejor control de dependencias

### **Performance**
- Tree-shaking automático
- Solo se importan iconos utilizados
- Bundle size optimizado

### **Consistencia**
- Tamaños estandarizados
- Colores predefinidos
- Propiedades unificadas

## Uso Básico

### Importación Simple
```tsx
import { MdRestaurant, FaBuilding, HiSparkles } from '../components/Icons';

// Uso directo
<MdRestaurant className="text-xl text-blue-600" />
```

### Importación con Utilidades
```tsx
import { MdRestaurant, getIconProps } from '../components/Icons';

// Uso con propiedades estandarizadas
<MdRestaurant {...getIconProps('lg', 'primary')} />
```

### Importación desde Componentes
```tsx
import { MdRestaurant, MdShare, iconSizes } from '../components';

// Uso con tamaños predefinidos
<MdRestaurant size={iconSizes.md} />
```

## Categorías de Iconos

### Material Design Icons (MD)
```tsx
import { 
 MdRestaurant, // Restaurantes y comida
 MdLocationOn, // Ubicación y mapas
 MdShare, // Compartir y redes
 MdRocket, // Acciones y navegación
 MdCategory, // Organización
 MdStorage, // Datos y almacenamiento
 MdSpeed, // Performance y velocidad
 MdSchool, // Educación y academia
} from '../components/Icons';
```

### Font Awesome Icons (FA)
```tsx
import { 
 FaBuilding, // Edificios y estructura
 FaCopyright, // Legal y copyright
 FaUser, // Usuarios y perfiles
 FaHeart, // Emociones y favoritos
 FaGithub, // Redes sociales
} from '../components/Icons';
```

### Heroicons (HI)
```tsx
import { 
 HiSparkles, // Efectos especiales
 HiLightBulb, // Ideas e innovación
 HiChat, // Comunicación
 HiThumbUp, // Feedback y reacciones
} from '../components/Icons';
```

## Tamaños Estándar

```tsx
export const iconSizes = {
 xs: '12px', // Iconos muy pequeños
 sm: '16px', // Iconos pequeños en texto
 md: '20px', // Tamaño por defecto
 lg: '24px', // Iconos destacados
 xl: '32px', // Iconos grandes
 '2xl': '48px', // Iconos muy grandes
} as const;
```

## Colores Predefinidos

```tsx
export const iconColors = {
 primary: 'text-blue-600', // Color principal
 secondary: 'text-gray-600', // Color secundario
 success: 'text-green-600', // Éxito y confirmación
 warning: 'text-yellow-600', // Advertencias
 error: 'text-red-600', // Errores
 white: 'text-white', // Iconos en fondos oscuros
 black: 'text-black', // Iconos en fondos claros
} as const;
```

## Función Helper

### getIconProps(size, color)
```tsx
// Uso básico
<MdRestaurant {...getIconProps()} /> // md, sin color
<MdRestaurant {...getIconProps('lg')} /> // lg, sin color 
<MdRestaurant {...getIconProps('sm', 'primary')} /> // sm, azul

// Equivalente manual
<MdRestaurant size="16px" className="text-blue-600" />
```

## Ejemplos de Uso

### En Componentes de UI
```tsx
// Button con icono
<button className="flex items-center gap-2">
 <MdRocket {...getIconProps('sm', 'white')} />
 Buscar Restaurantes
</button>

// Stats con iconos categorizados
<div className="stat-item">
 <MdCategory {...getIconProps('md', 'primary')} />
 <span>{categoriesCount} Categorías</span>
</div>
```

### En Navegación
```tsx
// Sidebar navigation
const navItems = [
 { icon: MdHome, label: 'Inicio', path: '/' },
 { icon: MdRestaurant, label: 'Restaurantes', path: '/restaurants' },
 { icon: MdLocationOn, label: 'Mapa', path: '/map' },
];

{navItems.map(item => (
 <NavItem key={item.path}>
 <item.icon {...getIconProps('md', 'secondary')} />
 {item.label}
 </NavItem>
))}
```

### En Footer
```tsx
// Social media icons
<div className="social-links">
 <FaGithub {...getIconProps('lg')} />
 <FaLinkedin {...getIconProps('lg')} />
 <FaTwitter {...getIconProps('lg')} />
</div>

// Footer stats
<MdStorage {...getIconProps('sm', 'success')} />
<span>15K+ Datos</span>
```

## Agregar Nuevos Iconos

### 1. Instalar Nueva Familia (si es necesario)
```bash
npm install react-icons
```

### 2. Agregar al Archivo Central
```tsx
// En /src/components/Icons/index.ts
export {
 // ... iconos existentes
 NuevoIcono,
 OtroIconoNuevo,
} from 'react-icons/nueva-familia';
```

### 3. Documentar Categoría
Agregar la nueva categoría a esta documentación con ejemplos de uso.

## Best Practices

### **Hacer**
- Usar iconos del sistema centralizado
- Aplicar tamaños y colores consistentes
- Documentar nuevos iconos agregados
- Usar semantic naming para iconos personalizados

### **Evitar**
- Importar directamente desde react-icons
- Tamaños y colores hardcodeados inconsistentes
- Duplicar iconos existentes
- Mezclar diferentes estilos de iconos sin criterio

## Migración desde Iconos Dispersos

### Antes ()
```tsx
import { MdRestaurant } from 'react-icons/md';
import { FaBuilding } from 'react-icons/fa';

<MdRestaurant className="text-xl text-blue-600" />
<FaBuilding style={{ fontSize: '20px', color: '#1f2937' }} />
```

### Después ()
```tsx
import { MdRestaurant, FaBuilding, getIconProps } from '../components/Icons';

<MdRestaurant {...getIconProps('lg', 'primary')} />
<FaBuilding {...getIconProps('md', 'secondary')} />
```

Este sistema proporciona una base sólida para el manejo de iconos escalable y mantenible en toda la aplicación.