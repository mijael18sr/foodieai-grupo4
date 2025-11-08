import { memo } from 'react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  showStats?: boolean;
  totalCategories?: number;
  totalDistricts?: number;
  onToggleSidebar?: () => void;
}

export const Header = memo(function Header({
  title = "FoodieAI",
  subtitle = "Tu Asistente Gastronómico Inteligente",
  showStats = false,
  totalCategories = 0,
  totalDistricts = 0,
  onToggleSidebar,
}: HeaderProps) {
  return (
    <header className="bg-blue-600 shadow-md border-b border-blue-700/20 z-[60]">
      <div className="mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Left section */}
          <div className="flex items-center lg:flex-1">
            {/* Mobile Menu Button */}
            <button
              onClick={onToggleSidebar}
              className="lg:hidden p-2 mr-3 rounded-lg hover:bg-white/10 transition-all duration-200 focus:outline-none"
              aria-label="Toggle sidebar"
            >
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            {/* Logo */}
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center mr-3 flex-shrink-0">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            
            <div className="min-w-0">
              <h1 className="text-lg lg:text-xl font-bold text-white leading-tight">
                {title}
              </h1>
              <p className="text-xs text-blue-100 leading-tight">
                {subtitle}
              </p>
            </div>
          </div>

          {/* Right section */}
          <div className="flex items-center gap-3 lg:gap-4">
            {/* System Status */}
            <div className="hidden lg:flex items-center gap-3">
              <div className="flex items-center gap-2 px-3 py-1 bg-green-500/20 rounded-lg">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-white">En Línea</span>
              </div>
              
              <div className="flex items-center gap-1 text-white/80">
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="text-sm">0.7s</span>
              </div>
            </div>

            {/* Stats */}
            {showStats && (
              <div className="hidden md:flex items-center gap-4">
                <div className="w-px h-6 bg-white/30"></div>
                <div className="text-center">
                  <div className="text-lg font-bold text-white">{totalCategories}</div>
                  <div className="text-xs text-blue-100">Categorías</div>
                </div>
                <div className="w-px h-6 bg-white/30"></div>
                <div className="text-center">
                  <div className="text-lg font-bold text-white">{totalDistricts}</div>
                  <div className="text-xs text-blue-100">Distritos</div>
                </div>
              </div>
            )}

            {/* Auth Buttons */}
            <div className="flex items-center gap-2">
              <button 
                className="flex items-center gap-1 text-white hover:bg-white/10 px-3 py-2 rounded-lg transition-all duration-200"
                onClick={() => {/* TODO: Implement sign in */}}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <span className="text-sm font-medium">Ingresar</span>
              </button>

              <button 
                className="flex items-center gap-1 bg-white text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-lg transition-all duration-200 font-medium"
                onClick={() => {/* TODO: Implement sign up */}}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                <span className="text-sm">Registro</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
});