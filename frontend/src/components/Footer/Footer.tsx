import { useState, useEffect, memo } from 'react';
// Centralized icons
import {
  MdRestaurant,
  MdLocationOn,
  MdShare,
  MdRocket,
  MdCategory,
  MdPlace,
  MdStorage,
  MdSpeed,
  MdSchool,
  MdFavorite,
  MdAndroid,
  FaBuilding,
  FaCopyright,
  HiSparkles,
  getIconProps
} from '../Icons';

interface FooterProps {
  onNavigate?: (viewId: string) => void;
  totalCategories?: number;
  totalDistricts?: number;
  sidebarOpen?: boolean;
  windowWidth?: number;
}

export const Footer = memo(function Footer({ 
  onNavigate, 
  totalCategories = 25, 
  totalDistricts = 43,
  sidebarOpen = false,
  windowWidth = 1024
}: FooterProps) {
  const currentYear = new Date().getFullYear();
  const [isFooterVisible, setIsFooterVisible] = useState(false);
  const [isHoveringFooter, setIsHoveringFooter] = useState(false);
  const [isHoveringTrigger, setIsHoveringTrigger] = useState(false);

  // Mostrar footer cuando se hover sobre trigger o footer
  useEffect(() => {
    setIsFooterVisible(isHoveringFooter || isHoveringTrigger);
  }, [isHoveringFooter, isHoveringTrigger]);

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'get-started':
        onNavigate?.('recommendations');
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        break;
      case 'feedback':
        // Future: Open feedback modal
        // TODO: Implement feedback modal
        break;
      case 'share':
        // Native Web Share API if available
        if (navigator.share) {
          navigator.share({
            title: 'Restaurant Recommender AI',
            text: 'Sistema inteligente de recomendaciones gastronómicas para Lima',
            url: globalThis.location.href
          });
        } else {
          // Fallback: Copy to clipboard
          navigator.clipboard.writeText(globalThis.location.href);
          alert('¡Link copiado al portapapeles!');
        }
        break;
    }
  };

  return (
    <>
      {/* Zona trigger mejorada en el borde inferior */}
      <div 
        className={`fixed bottom-0 left-0 right-0 h-10 z-40 transition-all duration-200 ${
          sidebarOpen && windowWidth >= 1024 ? 'footer-trigger-expanded' : 'footer-trigger-collapsed'
        }`}
        role="button"
        tabIndex={0}
        aria-label="Mostrar footer con herramientas"
        onMouseEnter={() => setIsHoveringTrigger(true)}
        onMouseLeave={() => setIsHoveringTrigger(false)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            setIsHoveringTrigger(!isHoveringTrigger);
          }
        }}
        style={{ 
          background: isHoveringTrigger 
            ? 'linear-gradient(to top, rgba(30, 64, 175, 0.05), transparent)' 
            : 'linear-gradient(to top, rgba(30, 64, 175, 0.02), transparent)',
          pointerEvents: 'auto',
          cursor: 'pointer'
        }}
      >
        {/* Indicador visual ultra sutil */}
        <div className={`w-1/3 mx-auto transition-all duration-300 ${
          isHoveringTrigger ? 'h-0.5 opacity-40' : 'h-px opacity-10'
        } bg-gradient-to-r from-transparent via-slate-400 to-transparent`} />
      </div>

      {/* Footer que aparece/desaparece */}
      <footer 
        className={`fixed bottom-0 left-0 right-0 z-30 transition-all duration-300 ease-in-out footer-responsive ${
          sidebarOpen && windowWidth >= 1024 
            ? 'footer-expanded' 
            : 'footer-collapsed'
        } ${
          isFooterVisible 
            ? 'translate-y-0 opacity-100' 
            : 'translate-y-full opacity-0'
        }`}
        onMouseEnter={() => setIsHoveringFooter(true)}
        onMouseLeave={() => setIsHoveringFooter(false)}
        style={{
          background: 'linear-gradient(135deg, rgb(30, 41, 59), rgb(51, 65, 85), rgb(30, 41, 59))',
          backdropFilter: 'blur(12px)',
          borderTop: '1px solid rgba(148, 163, 184, 0.3)',
          boxShadow: '0 -4px 6px -1px rgba(0, 0, 0, 0.1)'
        }}
      >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 sm:py-4">
        
        {/* Quick Actions Bar - Más visible */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-4 mb-4 shadow-2xl border border-blue-400 border-opacity-30">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="text-center sm:text-left">
              <h3 className="text-base sm:text-lg font-bold mb-1 text-white flex items-center gap-2 justify-center sm:justify-start">
                <MdRestaurant {...getIconProps('lg')} />
                ¿Listo para descubrir restaurantes?
              </h3>
              <p className="text-blue-100 text-sm font-medium flex items-center gap-1 justify-center sm:justify-start">
                <MdCategory {...getIconProps('sm')} />
                {totalCategories} categorías 
                <span className="mx-1">•</span>
                <MdPlace {...getIconProps('sm')} />
                {totalDistricts} distritos de Lima
              </p>
            </div>
            <div className="flex gap-3 w-full sm:w-auto justify-center">
              <button 
                onClick={() => handleQuickAction('get-started')}
                className="bg-white text-blue-600 px-4 sm:px-6 py-2.5 sm:py-3 rounded-xl font-bold hover:bg-blue-50 transition-all duration-300 text-sm sm:text-base flex-1 sm:flex-none shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center gap-2 justify-center"
              >
                <MdRocket className="text-lg" />
                Buscar Ahora
              </button>
              <button 
                onClick={() => handleQuickAction('share')}
                className="bg-blue-500 bg-opacity-40 text-white px-4 py-2.5 sm:py-3 rounded-xl hover:bg-opacity-60 transition-all duration-300 text-sm font-semibold shadow-md flex items-center gap-1 justify-center"
                title="Compartir aplicación"
              >
                <MdShare className="text-base" />
                Compartir
              </button>
            </div>
          </div>
        </div>

        {/* Main Footer Content - Compacto */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
          
          {/* About Section - Con iconos React */}
          <div className="text-center sm:text-left">
            <div className="flex items-center gap-2 mb-2 justify-center sm:justify-start">
              <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-md flex items-center justify-center shadow-md">
                <FaBuilding className="w-3 h-3 text-white" />
              </div>
              <h3 className="text-sm font-bold text-slate-100">Restaurant AI</h3>
            </div>
            <p className="text-slate-200 text-xs leading-tight font-medium flex items-center gap-1 justify-center sm:justify-start">
              <HiSparkles className="text-yellow-300 text-sm" />
              IA para encontrar restaurantes perfectos en Lima
            </p>
          </div>

          {/* Quick Stats - Con iconos profesionales */}
          <div className="text-center">
            <div className="grid grid-cols-4 gap-1 sm:gap-2">
              <div className="bg-slate-700 bg-opacity-60 backdrop-blur-sm rounded-lg p-1.5 sm:p-2 border border-slate-500 border-opacity-30 flex flex-col items-center">
                <MdCategory className="text-blue-300 text-base mb-1" />
                <div className="text-sm font-bold text-blue-300">{totalCategories}+</div>
                <div className="text-xs text-slate-200">Cat.</div>
              </div>
              <div className="bg-slate-700 bg-opacity-60 backdrop-blur-sm rounded-lg p-1.5 sm:p-2 border border-slate-500 border-opacity-30 flex flex-col items-center">
                <MdLocationOn className="text-green-300 text-base mb-1" />
                <div className="text-sm font-bold text-green-300">{totalDistricts}</div>
                <div className="text-xs text-slate-200">Dist.</div>
              </div>
              <div className="bg-slate-700 bg-opacity-60 backdrop-blur-sm rounded-lg p-1.5 sm:p-2 border border-slate-500 border-opacity-30 flex flex-col items-center">
                <MdStorage className="text-purple-300 text-base mb-1" />
                <div className="text-sm font-bold text-purple-300">15K+</div>
                <div className="text-xs text-slate-200">Datos</div>
              </div>
              <div className="bg-slate-700 bg-opacity-60 backdrop-blur-sm rounded-lg p-1.5 sm:p-2 border border-slate-500 border-opacity-30 flex flex-col items-center">
                <MdSpeed className="text-orange-300 text-base mb-1" />
                <div className="text-sm font-bold text-orange-300">&lt;1s</div>
                <div className="text-xs text-slate-200">Resp.</div>
              </div>
            </div>
          </div>

          {/* Academic - Con iconos profesionales */}
          <div className="text-center sm:text-right">
            <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg p-2 shadow-lg border border-indigo-400 border-opacity-40 flex flex-col items-center">
              <MdSchool className="text-white text-lg mb-1" />
              <h5 className="font-bold text-white text-xs">UNMSM</h5>
              <p className="text-indigo-100 text-xs font-medium flex items-center gap-1">
                <MdAndroid className="text-xs" />
                Machine Learning
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar - Con iconos profesionales */}
        <div className="border-t border-slate-400 border-opacity-30 pt-2 bg-slate-800 bg-opacity-40 rounded-t-lg">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-1">
            <div className="text-slate-100 text-xs text-center sm:text-left font-medium flex items-center gap-1 justify-center sm:justify-start">
              <FaCopyright className="text-xs" />
              {currentYear} Restaurant AI - UNMSM
            </div>
            <div className="text-slate-200 text-xs font-medium flex items-center gap-1">
              <MdFavorite className="text-red-400 text-sm" />
              <MdAndroid className="text-green-400 text-sm" />
              <MdLocationOn className="text-blue-400 text-sm" />
              Lima
            </div>
          </div>
        </div>
      </div>
    </footer>
    </>
  );
});