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
    <header className="relative bg-gray-50 shadow-sm border-b border-gray-200 z-[60]">
      {/* Clean minimal background */}
      <div className="absolute inset-0 bg-gradient-to-r from-gray-100/50 to-blue-100/30"></div>

      <div className="relative">
        <div className="mx-auto px-4 sm:px-6 lg:px-8 py-1.5">
          <div className="flex items-center justify-between">
            {/* Left section: Menu & Title & Logo - Clean */}
            <div className="flex items-center lg:flex-1">
              {/* Mobile Menu Button */}
              <button
                onClick={onToggleSidebar}
                className="lg:hidden p-2 mr-2 rounded-lg hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                aria-label="Toggle sidebar"
              >
                <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>

              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center mr-3 shadow-md flex-shrink-0">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div className="min-w-0">
                <h1 className="text-lg lg:text-xl font-bold text-gray-900 leading-tight">
                  {title}
                </h1>
                <p className="text-xs text-gray-600 leading-tight">
                  {subtitle}
                </p>
              </div>
            </div>

            {/* Right section: Stats & System Status & Auth */}
            <div className="flex items-center gap-4 lg:gap-6">
              {/* System Status Indicators - Always visible but subtle */}
              <div className="hidden lg:flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 rounded-lg border border-green-100">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-xs font-medium text-green-700">Sistema Activo</span>
                </div>
                
                <div className="flex items-center gap-1 text-xs text-gray-500">
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>~0.8s</span>
                </div>
              </div>

              {/* Stats - Clean design */}
              {showStats && (
                <div className="hidden md:flex items-center gap-4">
                  <div className="w-px h-6 bg-gray-200"></div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-blue-600">{totalCategories}</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider">Categorías</div>
                  </div>
                  <div className="w-px h-6 bg-gray-200"></div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-blue-600">{totalDistricts}</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider">Distritos</div>
                  </div>
                </div>
              )}

              {/* Auth Buttons - Compact */}
              <div className="flex items-center gap-2">
                {/* Sign In Button - Compact */}
                <button 
                  className="flex items-center gap-1.5 text-gray-800 hover:text-white hover:bg-gray-700 px-3 py-1.5 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                  onClick={() => {
                    console.log('Sign In clicked');
                  }}
                  aria-label="Iniciar sesión"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  <span className="text-sm font-medium">Sign In</span>
                </button>

                {/* Sign Up Button - Compact */}
                <button 
                  className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg transition-colors duration-200 shadow-sm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                  onClick={() => {
                    console.log('Sign Up clicked');
                  }}
                  aria-label="Registrarse"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                  <span className="text-sm font-medium">Sign Up</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
});