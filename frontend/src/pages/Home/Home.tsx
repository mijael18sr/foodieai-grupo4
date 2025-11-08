import { useState, memo, useCallback } from 'react';
import { Layout, SearchFilters, RecommendationsList, AIChat, SentimentPanel, Dashboard, Explore } from '../../components';
import { useApiData, useRecommendations } from '../../hooks';
import type { UserLocation, RecommendationFilters, UserPreferences } from '../../types/api';

export const Home = memo(function Home() {
  const { categories, districts, error: dataError } = useApiData();
  const { recommendations, loading: recLoading, error: recError, fetchRecommendations } = useRecommendations();

  const [hasSearched, setHasSearched] = useState(false);
  const [currentView, setCurrentView] = useState('home');
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleChatToggle = useCallback(() => {
    setIsChatOpen(prev => !prev);
  }, []);

  const handleNavigation = useCallback((viewId: string) => {
    setCurrentView(viewId);
    // Resetear búsqueda cuando cambie de vista
    if (viewId !== 'recommendations') {
      setHasSearched(false);
    }
  }, []);

  const handleSearch = useCallback(async (
    location: UserLocation,
    preferences?: UserPreferences,
    filters?: RecommendationFilters,
    topN?: number
  ) => {
    console.log('🔍 Starting search with params:', { location, preferences, filters, topN });
    setHasSearched(true);
    
    const request = {
      user_location: location,
      preferences,
      filters,
      top_n: topN || 10,
    };

    console.log('📤 Request object:', request);
    await fetchRecommendations(request);
  }, [fetchRecommendations]);

  // Helper functions para categorías
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

  // Función para obtener URL de imagen del backend
  const renderCurrentView = () => {
    switch (currentView) {
      case 'home':
        return (
          <div className="space-y-8">
            {/* Dashboard Component */}
            <Dashboard />

            {/* Navegación rápida */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
              <div 
                className="group bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-200 hover:border-green-400 cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-2"
                onClick={() => handleNavigation('categories')}
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M11 9h2V6h3V4h-3V1h-2v3H8v2h3v3zm-4 9c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zm10 0c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 group-hover:text-green-800 transition-colors">
                      🍜 Categorías
                    </h3>
                    <p className="text-sm text-gray-600">{categories?.length || '25+'} tipos de cocina</p>
                  </div>
                </div>
              </div>

              <div 
                className="group bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200 hover:border-blue-400 cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-2"
                onClick={() => handleNavigation('districts')}
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 group-hover:text-blue-800 transition-colors">
                      📍 Distritos
                    </h3>
                    <p className="text-sm text-gray-600">{districts?.length || 7} zonas de Lima</p>
                  </div>
                </div>
              </div>

              <div 
                className="group bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200 hover:border-purple-400 cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-2"
                onClick={() => handleNavigation('recommendations')}
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 group-hover:text-purple-800 transition-colors">
                      🎯 Buscar
                    </h3>
                    <p className="text-sm text-gray-600">Recomendaciones ML</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'districts':
        return (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-2xl p-8 border border-blue-100">
              <div className="text-center max-w-3xl mx-auto">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mb-6 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Descubre Lima por Distritos
                </h1>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Explora la diversidad gastronómica de Lima. Cada distrito tiene su propia personalidad culinaria y sabores únicos esperándote.
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

            {/* Grid de Distritos */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {districts ? districts.map((district) => (
                <div
                  key={district}
                  className="group bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-2 cursor-pointer"
                  onClick={() => handleNavigation('recommendations')}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="text-3xl">{getDistrictIcon(district)}</div>
                    <div className="text-gray-300 group-hover:text-blue-500 transition-colors">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5-5 5M6 12h12" />
                      </svg>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {district.replaceAll('_', ' ')}
                  </h3>
                  <p className="text-gray-600 mb-4 leading-relaxed">
                    {getDistrictDescription(district)}
                  </p>
                  
                  <div className="pt-4 border-t border-gray-50">
                    <span className="text-sm text-gray-500">Click para explorar restaurantes</span>
                  </div>
                </div>
              )) : (
                <div className="col-span-full text-center py-12">
                  <div className="text-6xl mb-4">🏛️</div>
                  <p className="text-xl text-gray-600">Cargando distritos...</p>
                </div>
              )}
            </div>

            {/* Botón de regreso */}
            <div className="text-center pt-8">
              <button
                onClick={() => handleNavigation('home')}
                className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-full font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                ← Volver al Inicio
              </button>
            </div>
          </div>
        );

      case 'explore':
        return <Explore onNavigate={handleNavigation} />;

      case 'categories':
        return (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 rounded-2xl p-8 border border-green-100">
              <div className="text-center max-w-3xl mx-auto">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-600 to-emerald-600 rounded-2xl mb-6 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Explora por Categorías
                </h1>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Desde la tradicional comida criolla hasta la sofisticada cocina internacional. 
                  Descubre sabores únicos en cada categoría gastronómica.
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

            {/* Grid de Categorías */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {categories ? categories.map((category) => (
                <div
                  key={category}
                  className="group bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer"
                  onClick={() => handleNavigation('recommendations')}
                >
                  <div className="text-center">
                    <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-300">
                      {getCategoryIcon(category)}
                    </div>
                    <h3 className="font-bold text-gray-900 mb-2 group-hover:text-green-600 transition-colors">
                      {category.replaceAll('_', ' ')}
                    </h3>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      {getCategoryDescription(category)}
                    </p>
                  </div>
                </div>
              )) : (
                <div className="col-span-full text-center py-12">
                  <div className="text-6xl mb-4">🍽️</div>
                  <p className="text-xl text-gray-600">Cargando categorías...</p>
                </div>
              )}
            </div>

            {/* Botón de regreso */}
            <div className="text-center pt-8">
              <button
                onClick={() => handleNavigation('home')}
                className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-8 py-3 rounded-full font-semibold hover:from-green-600 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                ← Volver al Inicio
              </button>
            </div>
          </div>
        );

      case 'recommendations':
        return (
          <div className="space-y-8">
            {/* Hero Section para Búsqueda de Recomendaciones */}
            <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-50 rounded-2xl p-8 border border-blue-100">
              <div className="text-center max-w-3xl mx-auto">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mb-6 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h2m5 0h2a2 2 0 002-2V7a2 2 0 00-2-2h-2m-5 4v6m5-6v6m-5 0H9m5 0h5" />
                  </svg>
                </div>
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  Buscar Recomendaciones con IA
                </h1>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Encuentra los mejores restaurantes de Lima personalizados para ti. Nuestro sistema de Machine Learning analiza tus preferencias y ubicación para recomendarte lugares únicos.
                </p>
                
                <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full text-sm font-medium bg-gradient-to-r from-blue-100 to-purple-100 text-blue-700 border border-blue-200">
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  🤖 Powered by Machine Learning
                </div>
              </div>
            </div>

            {/* Componente de Filtros de Búsqueda */}
            <SearchFilters
              categories={categories || []}
              districts={districts || []}
              onSearch={handleSearch}
              loading={recLoading}
            />

            {/* Resultados de Recomendaciones */}
            {hasSearched && (
              <RecommendationsList
                recommendations={recommendations}
                loading={recLoading}
                error={recError}
              />
            )}

            {/* Botón de regreso */}
            <div className="text-center pt-8">
              <button
                onClick={() => handleNavigation('home')}
                className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-full font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                ← Volver al Inicio
              </button>
            </div>
          </div>
        );

      case 'sentiment':
        return (
          <div className="space-y-8">
            {/* Componente Principal de Análisis de Sentimientos */}
            <SentimentPanel />

            {/* Información adicional sobre el sistema */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8 border border-blue-100">
              <div className="text-center max-w-4xl mx-auto">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">¿Cómo funciona nuestro análisis?</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <div className="text-3xl mb-4">📝</div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">1. Escribe tu opinión</h3>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      Comparte detalles sobre tu experiencia gastronómica: comida, servicio, ambiente, etc.
                    </p>
                  </div>
                  
                  <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <div className="text-3xl mb-4">🧠</div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">2. Análisis inteligente</h3>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      Nuestro modelo de IA procesa tu texto y analiza el sentimiento expresado.
                    </p>
                  </div>
                  
                  <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                    <div className="text-3xl mb-4">📊</div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">3. Resultados detallados</h3>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      Recibe una clasificación precisa con porcentajes de confianza y explicaciones.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Botón de regreso */}
            <div className="text-center pt-8">
              <button
                onClick={() => handleNavigation('home')}
                className="bg-gradient-to-r from-purple-500 to-blue-600 text-white px-8 py-3 rounded-full font-semibold hover:from-purple-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                ← Volver al Inicio
              </button>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🤔</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Vista no encontrada</h2>
            <p className="text-gray-600 mb-8">La vista solicitada no existe.</p>
            <button
              onClick={() => handleNavigation('home')}
              className="bg-blue-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-700 transition-colors"
            >
              Ir al Inicio
            </button>
          </div>
        );
    }
  };

  return (
    <Layout 
      currentView={currentView} 
      onNavigate={handleNavigation}
    >
      {renderCurrentView()}
      
      {/* Chat Button */}
      <button
        onClick={handleChatToggle}
        className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-full shadow-2xl hover:shadow-3xl transition-all duration-300 flex items-center justify-center z-50 transform hover:scale-110"
        aria-label="Abrir chat de IA"
      >
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>

      {/* AI Chat */}
      {isChatOpen && (
        <AIChat 
          isOpen={isChatOpen} 
          onToggle={handleChatToggle} 
        />
      )}
    </Layout>
  );
});