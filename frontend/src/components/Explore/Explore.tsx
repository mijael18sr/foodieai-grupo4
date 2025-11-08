import { memo } from 'react';
import { useApiData } from '../../hooks';

interface ExploreProps {
  onNavigate?: (viewId: string) => void;
}

export const Explore = memo(function Explore({ onNavigate }: ExploreProps) {
  const { categories, districts, error: dataError } = useApiData();

  // Helper function para descripciones de categorías
  const getCategoryDescription = (category: string) => {
    const descriptions = {
      'Comida_Rapida': 'Opciones rápidas y deliciosas',
      'Parrillas': 'Carnes a la parrilla y asados',
      'Marisqueria': 'Pescados y mariscos frescos',
      'Italiana': 'Pastas, pizzas y sabores mediterráneos',
      'Chifa': 'Fusión peruano-china tradicional',
      'Japonesa': 'Sushi, ramen y cocina nipona',
      'Criolla': 'Sabores tradicionales peruanos',
      'Vegetariana': 'Opciones saludables y naturales',
      'Internacional': 'Cocina de todo el mundo',
      'Postres': 'Dulces y repostería artesanal',
      'Bar': 'Tragos y aperitivos',
      'Cafeteria': 'Café, té y bocadillos',
      'Peruana': 'Lo mejor de la gastronomía nacional',
      'Francesa': 'Elegancia y sofisticación culinaria',
      'Americana': 'Hamburguesas, BBQ y clásicos',
      'China': 'Auténticos sabores orientales',
      'Mexicana': 'Picante y tradicional',
      'Fusion': 'Creatividad e innovación gastronómica',
      'India': 'Especias y curry tradicional',
      'Brasilera': 'Sabores tropicales del Brasil',
      'Argentina': 'Carnes premium y empanadas'
    };
    return descriptions[category as keyof typeof descriptions] || 'Descubre nuevos sabores';
  };

  const getCategoryIcon = (category: string) => {
    const iconMap = {
      'Comida_Rapida': '🍔',
      'Parrillas': '🥩',
      'Marisqueria': '🦐',
      'Italiana': '🍝',
      'Chifa': '🥟',
      'Japonesa': '🍣',
      'Criolla': '🇵🇪',
      'Vegetariana': '🥗',
      'Internacional': '🌍',
      'Postres': '🧁',
      'Bar': '🍻',
      'Cafeteria': '☕',
      'Peruana': '🌶️',
      'Francesa': '🥐',
      'Americana': '🍟',
      'China': '🥢',
      'Mexicana': '🌮',
      'Fusion': '👨‍🍳',
      'India': '🍛',
      'Brasilera': '🇧🇷',
      'Argentina': '🥖'
    };
    return iconMap[category as keyof typeof iconMap] || '🍽️';
  };

  // Helper function para descripciones de distritos
  const getDistrictDescription = (district: string) => {
    const descriptions = {
      'Miraflores': 'Zona bohemia y moderna con gran variedad gastronómica',
      'San_Isidro': 'Elegancia y alta cocina en el corazón financiero',
      'Barranco': 'Arte, cultura y sabores únicos frente al mar',
      'Surco': 'Tradición y modernidad en armonía culinaria',
      'La_Molina': 'Opciones familiares y espacios amplios',
      'San_Borja': 'Variedad gastronómica en ambiente tranquilo',
      'Lince': 'Sabores auténticos y precios accesibles'
    };
    return descriptions[district as keyof typeof descriptions] || 'Explora este distrito';
  };

  const getDistrictIcon = (district: string) => {
    const iconMap = {
      'Miraflores': '🌊',
      'San_Isidro': '🏢',
      'Barranco': '🎨',
      'Surco': '🏘️',
      'La_Molina': '🌳',
      'San_Borja': '🏛️',
      'Lince': '🏪'
    };
    return iconMap[district as keyof typeof iconMap] || '📍';
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 rounded-2xl p-8 border border-green-100">
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-600 to-emerald-600 rounded-2xl mb-6 shadow-lg">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Explora por Categorías y Distritos
          </h1>
          <p className="text-lg text-gray-600 mb-6 leading-relaxed">
            Descubre la diversidad gastronómica de Lima. Explora por tipo de cocina o por ubicación para encontrar exactamente lo que buscas.
          </p>
          
          {/* Estado de conexión */}
          <div className={`inline-flex items-center gap-3 px-4 py-2 rounded-full text-sm font-medium ${
            dataError 
              ? 'bg-amber-100 text-amber-800 border border-amber-200' 
              : 'bg-green-100 text-green-800 border border-green-200'
          }`}>
            <div className={`w-2 h-2 rounded-full ${dataError ? 'bg-amber-500' : 'bg-green-500'} animate-pulse`}></div>
            {dataError ? 'Modo Sin Conexión' : 'Datos Actualizados'}
          </div>
        </div>
      </div>

      {/* Selector de vista */}
      <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
        <div className="text-center max-w-4xl mx-auto mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">¿Qué te gustaría explorar?</h2>
          <p className="text-gray-600">Elige tu forma favorita de descubrir nuevos restaurantes</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Explorar por Categorías */}
          <div 
            className="group bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 border border-green-200 hover:border-green-400 cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-2"
            onClick={() => onNavigate?.('categories')}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                onNavigate?.('categories');
              }
            }}
          >
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-green-800 transition-colors">
                🍜 Tipos de Cocina
              </h3>
              
              <p className="text-gray-700 mb-6 leading-relaxed">
                Descubre restaurantes por especialidad gastronómica. Desde comida criolla tradicional hasta alta cocina internacional.
              </p>
              
              <div className="bg-white rounded-xl p-4 mb-6 shadow-sm border border-green-100">
                <div className="text-3xl font-bold text-green-600 mb-2">{categories?.length || '25+'}</div>
                <div className="text-sm text-gray-600">Categorías disponibles</div>
              </div>
              
              <div className="flex flex-wrap gap-2 justify-center">
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">Criolla</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">Italiana</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">Japonesa</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">Chifa</span>
              </div>
            </div>
          </div>

          {/* Explorar por Distritos */}
          <div 
            className="group bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 border border-blue-200 hover:border-blue-400 cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-2"
            onClick={() => onNavigate?.('districts')}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                onNavigate?.('districts');
              }
            }}
          >
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              
              <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-blue-800 transition-colors">
                📍 Por Ubicación
              </h3>
              
              <p className="text-gray-700 mb-6 leading-relaxed">
                Explora restaurantes por distrito. Cada zona de Lima tiene su propia personalidad gastronómica única.
              </p>
              
              <div className="bg-white rounded-xl p-4 mb-6 shadow-sm border border-blue-100">
                <div className="text-3xl font-bold text-blue-600 mb-2">{districts?.length || '7'}</div>
                <div className="text-sm text-gray-600">Distritos cubiertos</div>
              </div>
              
              <div className="flex flex-wrap gap-2 justify-center">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">Miraflores</span>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">Barranco</span>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">San Isidro</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Resumen estadístico */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 border border-indigo-100">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Resumen de Exploración</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div className="text-3xl mb-3">🍽️</div>
              <div className="text-2xl font-bold text-indigo-600 mb-2">
                {((categories?.length || 25) * (districts?.length || 7))}+
              </div>
              <div className="text-gray-600 text-sm">Combinaciones posibles</div>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div className="text-3xl mb-3">⭐</div>
              <div className="text-2xl font-bold text-green-600 mb-2">4.2+</div>
              <div className="text-gray-600 text-sm">Calificación promedio</div>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div className="text-3xl mb-3">🎯</div>
              <div className="text-2xl font-bold text-orange-600 mb-2">92%</div>
              <div className="text-gray-600 text-sm">Precisión del sistema</div>
            </div>
          </div>
        </div>
      </div>

      {/* Botón de regreso */}
      <div className="text-center pt-8">
        <button
          onClick={() => onNavigate?.('home')}
          className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-8 py-3 rounded-full font-semibold hover:from-green-600 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
        >
          ← Volver al Dashboard
        </button>
      </div>
    </div>
  );
});