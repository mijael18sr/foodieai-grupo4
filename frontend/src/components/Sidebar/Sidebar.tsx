import { memo, useState } from 'react';

interface SidebarItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  badge?: string | number;
  onClick?: () => void;
  isActive?: boolean;
}

interface SidebarProps {
  isOpen?: boolean;
  onToggle?: () => void;
  items?: SidebarItem[];
  onItemClick?: () => void;
  onNavigate?: (itemId: string) => void;
  activeItem?: string;
}

const defaultItems: SidebarItem[] = [
  {
    id: 'home',
    label: 'Inicio',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    ),
    isActive: true,
  },
  {
    id: 'recommendations',
    label: 'Buscar Recomendaciones',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h2m5 0h2a2 2 0 002-2V7a2 2 0 00-2-2h-2m-5 4v6m5-6v6m-5 0H9m5 0h5" />
      </svg>
    ),
    badge: 'NUEVO',
  },
  {
    id: 'sentiment',
    label: 'Análisis de Sentimientos',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
    badge: 'IA',
  },
  {
    id: 'explore',
    label: 'Explorar Categorías',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
      </svg>
    ),
  },
  {
    id: 'districts',
    label: 'Distritos de Lima',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  },
  {
    id: 'favorites',
    label: 'Mis Favoritos',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      </svg>
    ),
    badge: '0',
  },
  {
    id: 'history',
    label: 'Búsquedas Recientes',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    id: 'about',
    label: 'Acerca del Sistema',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
];

export const Sidebar = memo(function Sidebar({
  isOpen = true,
  onToggle,
  items = defaultItems,
  onItemClick,
  onNavigate,
  activeItem: externalActiveItem
}: SidebarProps) {
  const [activeItem, setActiveItem] = useState(externalActiveItem || 'home');

  const handleItemClick = (item: SidebarItem) => {
    setActiveItem(item.id);
    item.onClick?.();
    
    // Notificar al Layout que el usuario ha interactuado
    onItemClick?.();
    
    // Notificar navegación al componente padre
    onNavigate?.(item.id);
    
    // Cerrar sidebar en mobile después de seleccionar un item
    if (window.innerWidth < 1024) { // lg breakpoint
      onToggle?.();
    }
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden transition-opacity duration-300"
          role="button"
          tabIndex={0}
          aria-label="Cerrar sidebar"
          onClick={onToggle}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              onToggle();
            }
          }}
        />
      )}

      {/* Sidebar */}
      <aside 
        className={`fixed left-0 z-30 bg-white shadow-2xl border-r border-gray-200 sidebar-transition flex flex-col ${
          isOpen ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0'
        }`}
        style={{ 
          width: '280px', 
          top: 'var(--header-height)', 
          height: 'calc(100vh - var(--header-height))' 
        }}
      >
        {/* Header - Simplified */}
        <div className="border-b border-gray-200 flex-shrink-0">
          {/* Close button for mobile */}
          <button
            onClick={onToggle}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors ml-auto block"
          >
            <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto flex flex-col">
          {/* Navigation Items */}
          <nav className="p-2 pt-3 flex-1">
            <ul className="space-y-2">
              {items.map((item) => (
              <li key={item.id}>
                <button
                  onClick={() => handleItemClick(item)}
                  className={`w-full flex items-center justify-between p-3 rounded-xl transition-all duration-200 group ${
                    activeItem === item.id
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25'
                      : 'text-gray-700 hover:bg-blue-50 hover:text-blue-700 hover:shadow-sm'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`transition-colors ${
                      activeItem === item.id ? 'text-white' : 'text-gray-600 group-hover:text-blue-600'
                    }`}>
                      {item.icon}
                    </div>
                    <span className="font-semibold text-sm">{item.label}</span>
                  </div>
                  
                  {item.badge && (
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                      activeItem === item.id
                        ? 'bg-blue-500 text-white'
                        : 'bg-blue-100 text-blue-700'
                    }`}>
                      {item.badge}
                    </span>
                  )}
                </button>
              </li>
            ))}
          </ul>
        </nav>

          {/* Footer con sugerencias pegadas al final */}
          <div className="flex-shrink-0">
            {/* Sugerencias útiles */}
            <div className="p-2 mb-2">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-3 border border-blue-100">
                <h3 className="text-sm font-bold text-blue-900 mb-2">💡 Sugerencias</h3>
                <div className="space-y-2">
                  <div className="text-xs text-blue-700 leading-relaxed">
                    <span className="font-medium">🔥 Tip:</span> Usa los filtros avanzados para encontrar exactamente lo que buscas
                  </div>
                  <div className="text-xs text-blue-700 leading-relaxed">
                    <span className="font-medium">⭐ Favoritos:</span> Guarda tus restaurantes preferidos para acceso rápido
                  </div>
                </div>
              </div>
            </div>

            {/* Footer técnico */}
            <div className="p-2 border-t border-blue-100 bg-blue-50">
              <div className="text-center">
                <p className="text-xs text-blue-700 mb-1">Powered by ML & AI</p>
                <div className="flex items-center justify-center gap-2">
                  <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
                  <span className="text-xs font-semibold text-blue-800">Sistema Activo</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
});