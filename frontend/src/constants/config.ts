// Application Configuration Constants

export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  TIMEOUT: 10000,
  DEFAULT_TOP_N: 10,
  IMAGES_BASE_URL: 'http://localhost:8000/docs/figures',
} as const;

export const UI_CONFIG = {
  HEADER_HEIGHT: '64px',
  SIDEBAR_WIDTH: '280px', 
  FOOTER_HEIGHT: 'auto',
  MOBILE_BREAKPOINT: 768,
  DESKTOP_BREAKPOINT: 1024,
} as const;

export const ANIMATION_CONFIG = {
  DURATION: {
    FAST: '150ms',
    NORMAL: '300ms',
    SLOW: '500ms',
  },
  EASING: {
    DEFAULT: 'ease-in-out',
    BOUNCE: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;

export const LOCATION_CONFIG = {
  DEFAULT_LOCATION: {
    lat: -12.0464,
    long: -77.0428,
    name: 'Lima, Perú'
  },
  MAX_DISTANCE_KM: 50,
  MIN_RATING: 1,
  MAX_RATING: 5,
} as const;

export const APP_INFO = {
  NAME: 'Restaurant AI',
  DESCRIPTION: 'Sistema inteligente de recomendaciones gastronómicas para Lima',
  VERSION: '1.0.0',
  ORGANIZATION: 'UNMSM',
  PROGRAM: 'Machine Learning',
} as const;

export const MESSAGES = {
  ERRORS: {
    NETWORK: 'Error de conexión. Verifica tu internet.',
    API_TIMEOUT: 'La solicitud tardó demasiado. Inténtalo de nuevo.',
    GENERIC: 'Ha ocurrido un error inesperado.',
    NO_LOCATION: 'No se pudo obtener la ubicación.',
    NO_RECOMMENDATIONS: 'No se encontraron recomendaciones.',
  },
  SUCCESS: {
    LINK_COPIED: '¡Link copiado al portapapeles!',
    LOCATION_FOUND: 'Ubicación detectada correctamente.',
  },
} as const;

export const STORAGE_KEYS = {
  USER_PREFERENCES: 'restaurant_ai_preferences',
  LAST_LOCATION: 'restaurant_ai_last_location',
  SIDEBAR_STATE: 'restaurant_ai_sidebar_state',
} as const;