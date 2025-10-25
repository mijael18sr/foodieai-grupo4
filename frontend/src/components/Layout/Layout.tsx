import { memo, useState, useEffect } from 'react';
import { Header } from '../Header';
import { Sidebar } from '../Sidebar';
import { Footer } from '../Footer';

interface LayoutProps {
  children: React.ReactNode;
  showStats?: boolean;
  totalCategories?: number;
  totalDistricts?: number;
  currentView?: string;
  onNavigate?: (viewId: string) => void;
}

export const Layout = memo(function Layout({
  children,
  showStats = false,
  totalCategories = 0,
  totalDistricts = 0,
  currentView = 'home',
  onNavigate,
}: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isHoveringEdge, setIsHoveringEdge] = useState(false);
  const [isHoveringSidebar, setIsHoveringSidebar] = useState(false);
  const [hasUserInteracted, setHasUserInteracted] = useState(false);
  const [windowWidth, setWindowWidth] = useState(typeof globalThis !== 'undefined' && globalThis.window ? globalThis.window.innerWidth : 1024);

  // Hook para manejar el redimensionamiento de la ventana
  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleMouseEnterEdge = () => {
    // Solo activar en desktop y después de la primera interacción
    if (windowWidth >= 1024 && hasUserInteracted) {
      setIsHoveringEdge(true);
      setSidebarOpen(true);
    }
  };

  const handleMouseLeaveEdge = () => {
    // Solo activar en desktop y después de la primera interacción
    if (windowWidth >= 1024 && hasUserInteracted) {
      setIsHoveringEdge(false);
      // Solo cerrar si no está hovering sobre el sidebar
      if (!isHoveringSidebar) {
        setSidebarOpen(false);
      }
    }
  };

  const handleMouseEnterSidebar = () => {
    // Solo activar en desktop y después de la primera interacción
    if (windowWidth >= 1024 && hasUserInteracted) {
      setIsHoveringSidebar(true);
      setSidebarOpen(true);
    }
  };

  const handleMouseLeaveSidebar = () => {
    // Solo activar en desktop y después de la primera interacción
    if (windowWidth >= 1024 && hasUserInteracted) {
      setIsHoveringSidebar(false);
      // Solo cerrar si no está hovering sobre el edge
      if (!isHoveringEdge) {
        setSidebarOpen(false);
      }
    }
  };

  const handleContentClick = () => {
    // Marcar que el usuario ha interactuado y cerrar sidebar
    setHasUserInteracted(true);
    if (sidebarOpen && !isHoveringSidebar) {
      setSidebarOpen(false);
    }
  };

  const handleSidebarItemClick = () => {
    // Marcar que el usuario ha interactuado al hacer clic en un item del sidebar
    setHasUserInteracted(true);
  };

  const handleToggleSidebar = () => {
    // Marcar que el usuario ha interactuado
    setHasUserInteracted(true);
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <Header 
        showStats={showStats}
        totalCategories={totalCategories}
        totalDistricts={totalDistricts}
        onToggleSidebar={handleToggleSidebar}
      />

      <div className="flex flex-1 relative">
        {/* Zona de activación invisible en el borde izquierdo */}
        <div 
          className="fixed left-0 w-8 z-30 pointer-events-auto opacity-0 hover:opacity-10 bg-blue-500 transition-opacity duration-200"
          style={{ top: 'var(--header-height)', height: 'calc(100vh - var(--header-height))' }}
          onMouseEnter={handleMouseEnterEdge}
          onMouseLeave={handleMouseLeaveEdge}
        />

        {/* Sidebar Container */}
        <nav
          onMouseEnter={handleMouseEnterSidebar}
          onMouseLeave={handleMouseLeaveSidebar}
          aria-label="Sidebar navigation"
        >
          <Sidebar 
            isOpen={sidebarOpen}
            onToggle={handleToggleSidebar}
            onItemClick={handleSidebarItemClick}
            onNavigate={onNavigate}
            activeItem={currentView}
          />
        </nav>

        {/* Main Content */}
        <main 
          className={`flex-1 layout-content content-scale-transition ${
            sidebarOpen && windowWidth >= 1024 
              ? 'layout-content-expanded content-compressed' 
              : 'layout-content-collapsed content-expanded'
          }`}
        >
          {/* Overlay para cerrar con clic */}
          {sidebarOpen && (
            <div
              className="fixed inset-0 z-20 lg:hidden"
              onClick={() => setSidebarOpen(false)}
            />
          )}
          
          {/* Content Area */}
          <div 
            className="main-content-area transition-all duration-300 ease-in-out p-6 relative z-10"
            onClick={handleContentClick}
          >
            {children}
          </div>
        </main>
      </div>

      {/* Footer al pie de página - fuera del main content */}
      <Footer 
        onNavigate={onNavigate}
        totalCategories={totalCategories}
        totalDistricts={totalDistricts}
        sidebarOpen={sidebarOpen}
        windowWidth={windowWidth}
      />
    </div>
  );
});