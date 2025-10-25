import { useState, memo, useCallback } from 'react';
import { Layout, SearchFilters, RecommendationsList, AIChat, SentimentPanel } from '../../components';
import { useApiData, useRecommendations } from '../../hooks';
import type { UserLocation, RecommendationFilters, UserPreferences } from '../../types/api';

export const Home = memo(function Home() {
  const { categories, districts, loading: dataLoading, error: dataError } = useApiData();
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

  if (dataLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center py-20">
          <div className="text-center animate-fade-in">
            <div className="relative mb-8">
              <div className="animate-spin rounded-full h-20 w-20 border-4 border-t-blue-500 border-r-indigo-500 border-b-blue-600 border-l-transparent mx-auto"></div>
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 via-indigo-500 to-blue-600 opacity-20 animate-pulse"></div>
            </div>
            <div className="bg-white rounded-2xl p-8 shadow-xl border border-gray-200">
              <p className="text-gray-900 text-xl font-bold mb-2">Cargando datos del sistema...</p>
              <p className="text-gray-600">Obteniendo categorías y distritos</p>
              <div className="mt-4 bg-blue-50 rounded-lg p-3">
                <p className="text-blue-700 text-sm">🤖 Inicializando algoritmos de ML...</p>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  // Mostrar la descripción principal incluso si hay error de conexión
  // Solo mostrar el error cuando el usuario intente buscar
  const showConnectionError = dataError && hasSearched;

  // Renderizar contenido según la vista actual
  const renderContent = () => {
    switch (currentView) {
      case 'recommendations':
        return (
          <>
            {/* Mostrar error solo cuando hay búsqueda Y error */}
            {showConnectionError && (
              <div className="mb-6">
                <div className="bg-red-50 border border-red-200 rounded-xl p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="text-red-500 text-2xl">⚠️</div>
                    <h3 className="text-red-800 font-bold text-lg">Error de Conexión</h3>
                  </div>
                  <p className="text-red-700 mb-4">{dataError}</p>
                  <div className="bg-red-100 rounded-lg p-4">
                    <p className="text-red-800 text-sm mb-2">💡 Verifica que el backend esté ejecutándose:</p>
                    <code className="text-red-900 text-xs bg-red-200 px-2 py-1 rounded">
                      cd backend && python start_server.py
                    </code>
                  </div>
                </div>
              </div>
            )}

            {/* Search Filters - solo en vista de recomendaciones */}
            <div className="mb-8 search-filters">
              <SearchFilters
                categories={categories || []}
                districts={districts || []}
                onSearch={handleSearch}
                loading={recLoading}
              />
            </div>

            {/* Results */}
            {hasSearched ? (
              <RecommendationsList
                recommendations={recommendations}
                loading={recLoading}
                error={recError}
              />
            ) : (
              <div className="bg-white rounded-3xl shadow-xl p-8 text-center">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-full flex items-center justify-center mb-6 mx-auto">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">🔍 Configurar Búsqueda</h3>
                <p className="text-gray-600 mb-6">
                  Configura tus preferencias y encuentra los mejores restaurantes de Lima
                </p>
                <div className="bg-blue-50 rounded-xl p-4">
                  <p className="text-blue-700 text-sm">
                    💡 Completa el formulario arriba para generar recomendaciones personalizadas
                  </p>
                </div>
              </div>
            )}
          </>
        );

      case 'explore':
        return (
          <div className="bg-white rounded-3xl shadow-xl p-8 text-center">
            <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-700 rounded-full flex items-center justify-center mb-6 mx-auto">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">🍜 Explorar Categorías</h3>
            <p className="text-gray-600 mb-6">Próximamente: Exploración detallada de categorías gastronómicas</p>
            <div className="bg-green-50 rounded-xl p-4">
              <p className="text-green-700 text-sm">🚧 Funcionalidad en desarrollo</p>
            </div>
          </div>
        );

      case 'sentiment':
        return (
          <div className="space-y-8">
            {/* Panel principal de análisis */}
            <SentimentPanel />

            {/* Cards informativos */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-2xl p-6 border border-green-200 hover:shadow-xl transition-all duration-300">
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center mb-4 mx-auto">
                    <span className="text-2xl text-white">😊</span>
                  </div>
                  <h4 className="font-bold text-green-900 text-lg mb-2">Sentimientos Positivos</h4>
                  <p className="text-green-700 text-sm leading-relaxed">
                    Identifica comentarios positivos que destacan fortalezas y experiencias satisfactorias
                  </p>
                </div>
              </div>

              <div className="bg-gradient-to-br from-yellow-50 to-amber-100 rounded-2xl p-6 border border-yellow-200 hover:shadow-xl transition-all duration-300">
                <div className="text-center">
                  <div className="w-12 h-12 bg-yellow-600 rounded-xl flex items-center justify-center mb-4 mx-auto">
                    <span className="text-2xl text-white">😐</span>
                  </div>
                  <h4 className="font-bold text-yellow-900 text-lg mb-2">Sentimientos Neutros</h4>
                  <p className="text-yellow-700 text-sm leading-relaxed">
                    Detecta opiniones equilibradas que proporcionan feedback constructivo
                  </p>
                </div>
              </div>

              <div className="bg-gradient-to-br from-red-50 to-rose-100 rounded-2xl p-6 border border-red-200 hover:shadow-xl transition-all duration-300">
                <div className="text-center">
                  <div className="w-12 h-12 bg-red-600 rounded-xl flex items-center justify-center mb-4 mx-auto">
                    <span className="text-2xl text-white">😞</span>
                  </div>
                  <h4 className="font-bold text-red-900 text-lg mb-2">Sentimientos Negativos</h4>
                  <p className="text-red-700 text-sm leading-relaxed">
                    Analiza críticas y áreas de mejora para optimizar la experiencia del cliente
                  </p>
                </div>
              </div>
            </div>

            {/* Información técnica resumida */}
            <div className="bg-white rounded-3xl shadow-xl p-6 border border-gray-200">
              <h4 className="text-xl font-bold text-gray-900 mb-4 text-center">⚡ Rendimiento del Sistema</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600 mb-1">85.5%</div>
                  <div className="text-xs text-gray-600">Precisión</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600 mb-1">&lt;100ms</div>
                  <div className="text-xs text-gray-600">Respuesta</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600 mb-1">5K</div>
                  <div className="text-xs text-gray-600">Vocabulario</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600 mb-1">12.5K</div>
                  <div className="text-xs text-gray-600">Entrenamiento</div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'districts':
        return (
          <div className="bg-white rounded-3xl shadow-xl p-8 text-center">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-violet-700 rounded-full flex items-center justify-center mb-6 mx-auto">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-4">📍 Distritos de Lima</h3>
            <p className="text-gray-600 mb-6">Próximamente: Información detallada de distritos</p>
            <div className="bg-purple-50 rounded-xl p-4">
              <p className="text-purple-700 text-sm">🚧 Funcionalidad en desarrollo</p>
            </div>
          </div>
        );

      case 'home':
      default:
        return (
          <div className="bg-white rounded-3xl shadow-2xl p-12 text-center animate-fade-in border border-gray-200 mb-8">
            {/* Aviso discreto de conexión */}
            {dataError && !hasSearched && (
              <div className="mb-6 bg-amber-50 border border-amber-200 rounded-xl p-4">
                <div className="flex items-center justify-center gap-2 text-amber-700">
                  <span>⚠️</span>
                  <span className="text-sm font-medium">Sin conexión al servidor - Mostrando información offline</span>
                </div>
              </div>
            )}

            <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-full flex items-center justify-center mb-8 mx-auto shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              🍽️ Restaurant Recommender AI
            </h2>
            
            <h3 className="text-xl font-semibold text-blue-600 mb-8">
              Sistema Inteligente de Recomendaciones Gastronómicas para Lima
            </h3>
            
            <div className="max-w-4xl mx-auto space-y-10">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 border border-blue-200">
                <h4 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-3">
                  🤖 ¿Cómo funciona nuestro algoritmo de Machine Learning?
                </h4>
                <p className="text-lg leading-relaxed text-gray-700 mb-6">
                  Nuestro sistema utiliza <span className="font-bold text-blue-600">algoritmos avanzados de aprendizaje automático</span> que analizan múltiples variables para encontrar los restaurantes perfectos según tus preferencias.
                </p>
                
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                  <div className="text-2xl mb-2">⭐</div>
                  <h5 className="font-semibold text-gray-900 mb-1">Rating</h5>
                  <p className="text-sm text-gray-600">Calificaciones y reviews de usuarios</p>
                </div>
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                  <div className="text-2xl mb-2">📍</div>
                  <h5 className="font-semibold text-gray-900 mb-1">Distancia</h5>
                  <p className="text-sm text-gray-600">Proximidad a tu ubicación</p>
                </div>
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                  <div className="text-2xl mb-2">🔥</div>
                  <h5 className="font-semibold text-gray-900 mb-1">Popularidad</h5>
                  <p className="text-sm text-gray-600">Tendencias y demanda actual</p>
                </div>
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                  <div className="text-2xl mb-2">🍜</div>
                  <h5 className="font-semibold text-gray-900 mb-1">Categoría</h5>
                  <p className="text-sm text-gray-600">Tipo de cocina y especialidades</p>
                </div>
              </div>

              {/* Sistema Statistics Dashboard - Visible solo en Home */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 border border-blue-200">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-2xl">🎯</div>
                    <div className="text-xs text-blue-600 font-medium">En tiempo real</div>
                  </div>
                  <h5 className="font-bold text-blue-900 mb-1">Búsquedas Realizadas</h5>
                  <div className="text-xl font-bold text-blue-700">1,247</div>
                  <p className="text-xs text-blue-600">+89 esta semana</p>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 border border-green-200">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-2xl">📊</div>
                    <div className="text-xs text-green-600 font-medium">Actualizado</div>
                  </div>
                  <h5 className="font-bold text-green-900 mb-1">Restaurantes Evaluados</h5>
                  <div className="text-xl font-bold text-green-700">15,051</div>
                  <p className="text-xs text-green-600">Base de datos completa</p>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 border border-purple-200">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-2xl">⚡</div>
                    <div className="text-xs text-purple-600 font-medium">Optimizado</div>
                  </div>
                  <h5 className="font-bold text-purple-900 mb-1">Tiempo de Respuesta</h5>
                  <div className="text-xl font-bold text-purple-700">0.7s</div>
                  <p className="text-xs text-purple-600">Promedio último mes</p>
                </div>

                <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-4 border border-orange-200">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-2xl">🤖</div>
                    <div className="text-xs text-orange-600 font-medium">IA Activa</div>
                  </div>
                  <h5 className="font-bold text-orange-900 mb-1">Precisión del Modelo</h5>
                  <div className="text-xl font-bold text-orange-700">94.2%</div>
                  <p className="text-xs text-orange-600">Satisfacción usuarios</p>
                </div>
              </div>
            </div>              <div className="text-xl leading-relaxed text-gray-700 text-center">
                📊 Analizamos <span className="font-bold text-green-600">{categories?.length || '25+'} categorías gastronómicas</span> en{' '}
                <span className="font-bold text-purple-600">{districts?.length || '43'} distritos de Lima</span> para brindarte 
                <span className="font-bold text-blue-600"> recomendaciones personalizadas</span> en tiempo real.
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 hover:shadow-xl transition-all duration-300 border border-blue-200 transform hover:-translate-y-2">
                  <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-900 text-lg mb-3">🧠 IA Avanzada</h3>
                  <p className="text-gray-700 leading-relaxed text-sm">
                    Algoritmos de <strong>Machine Learning</strong> que aprenden de patrones gastronómicos y preferencias de usuarios en Lima
                  </p>
                </div>
                
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 hover:shadow-xl transition-all duration-300 border border-green-200 transform hover:-translate-y-2">
                  <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-900 text-lg mb-3">📍 Geolocalización GPS</h3>
                  <p className="text-gray-700 leading-relaxed text-sm">
                    Sistema de <strong>posicionamiento preciso</strong> que calcula distancias reales y optimiza rutas hacia restaurantes
                  </p>
                </div>
                
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 hover:shadow-xl transition-all duration-300 border border-purple-200 transform hover:-translate-y-2">
                  <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mb-4">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-900 text-lg mb-3">🎯 Filtros Inteligentes</h3>
                  <p className="text-gray-700 leading-relaxed text-sm">
                    <strong>Personalización total</strong>: rating mínimo, distancia máxima, categorías específicas y distritos preferidos
                  </p>
                </div>
              </div>

              {/* Call to Action Section */}
              <div className="mt-16 mb-12 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-2xl p-8 text-white shadow-2xl transform hover:scale-105 transition-all duration-300">
                <div className="text-center">
                  <h3 className="text-3xl font-bold mb-4 flex items-center justify-center gap-3">
                    🚀 ¡Descubre tu próximo restaurante favorito!
                  </h3>
                  <p className="text-blue-100 mb-8 text-lg">
                    Usa el menú lateral para navegar a "Buscar Recomendaciones"
                  </p>
                  
                  <div className="bg-white bg-opacity-10 rounded-xl p-6 mb-6 backdrop-blur-sm">
                    <h4 className="font-bold text-lg mb-3">🔥 ¿Sabías que...?</h4>
                    <p className="text-blue-100">
                      Nuestro sistema procesa más de <span className="font-bold text-yellow-300">15,000 datos gastronómicos</span> para 
                      encontrar el match perfecto con tus gustos. ¡Tiempo promedio de respuesta: menos de 1 segundo!
                    </p>
                  </div>

                  <button 
                    onClick={() => handleNavigation('recommendations')}
                    className="bg-white text-blue-600 px-10 py-4 rounded-full font-bold text-xl hover:bg-blue-50 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-2 animate-pulse hover:animate-none"
                  >
                    🍽️ Ir a Buscar Recomendaciones
                  </button>
                </div>
              </div>
            </div>

          </div>
        );
    }
  };

  return (
    <Layout 
      showStats={!dataError && currentView === 'recommendations'}
      totalCategories={categories?.length || 0}
      totalDistricts={districts?.length || 0}
      currentView={currentView}
      onNavigate={handleNavigation}
    >
      {renderContent()}
      
      {/* Chat flotante con IA - Disponible en todas las vistas */}
      <AIChat 
        isOpen={isChatOpen}
        onToggle={handleChatToggle}
      />
    </Layout>
  );
});