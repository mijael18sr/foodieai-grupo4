import React from 'react';
import { useApiData } from '../../hooks/useApiData';

interface ExploreProps {
  onNavigate: (viewId: string) => void;
}

export const Explore: React.FC<ExploreProps> = ({ onNavigate }) => {
  const { categories, districts } = useApiData();

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
          🗺️ Explorar Lima Gastronómica
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Descubre la diversidad culinaria de Lima explorando por tipo de cocina o por distrito.
          Tu aventura gastronómica comienza aquí.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 text-center border border-green-200">
          <div className="text-3xl font-bold text-green-800">{categories.length}</div>
          <div className="text-sm text-green-600 font-medium">Tipos de Cocina</div>
        </div>
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 text-center border border-blue-200">
          <div className="text-3xl font-bold text-blue-800">{districts.length}</div>
          <div className="text-sm text-blue-600 font-medium">Distritos</div>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 text-center border border-purple-200">
          <div className="text-3xl font-bold text-purple-800">1000+</div>
          <div className="text-sm text-purple-600 font-medium">Restaurantes</div>
        </div>
        <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-6 text-center border border-orange-200">
          <div className="text-3xl font-bold text-orange-800">4.5⭐</div>
          <div className="text-sm text-orange-600 font-medium">Rating Promedio</div>
        </div>
      </div>

      {/* Exploration Options */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Categories Card */}
        <button 
          className="group bg-gradient-to-br from-green-50 to-emerald-50 rounded-3xl p-8 border border-green-200 hover:border-green-400 cursor-pointer transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 w-full text-left"
          onClick={() => onNavigate('categories')}
        >
          <div className="flex items-center gap-6 mb-6">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
              <span className="text-3xl">🍜</span>
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 group-hover:text-green-800 transition-colors">
                Explorar por Categorías
              </h3>
              <p className="text-gray-600">{categories.length} tipos de cocina disponibles</p>
            </div>
          </div>
          
          <p className="text-gray-700 mb-6 leading-relaxed">
            Descubre restaurantes por tipo de cocina: desde la tradicional comida criolla hasta 
            sabores internacionales como japonesa, italiana, china y más.
          </p>
          
          <div className="flex items-center text-green-700 font-semibold group-hover:text-green-800">
            Explorar Categorías 
            <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </button>

        {/* Districts Card */}
        <button 
          className="group bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-8 border border-blue-200 hover:border-blue-400 cursor-pointer transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 w-full text-left"
          onClick={() => onNavigate('districts')}
        >
          <div className="flex items-center gap-6 mb-6">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
              <span className="text-3xl">🗺️</span>
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-900 group-hover:text-blue-800 transition-colors">
                Explorar por Distritos
              </h3>
              <p className="text-gray-600">{districts.length} distritos de Lima</p>
            </div>
          </div>
          
          <p className="text-gray-700 mb-6 leading-relaxed">
            Explora la oferta gastronómica por zona: desde Miraflores y San Isidro hasta 
            Barranco y el Centro Histórico. Cada distrito tiene su propia personalidad culinaria.
          </p>
          
          <div className="flex items-center text-blue-700 font-semibold group-hover:text-blue-800">
            Explorar Distritos
            <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </button>
      </div>

      {/* Popular Categories Preview */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Categorías Más Populares</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {categories.slice(0, 6).map((category: string) => (
            <div
              key={category}
              className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-200"
            >
              <div className="text-center">
                <div className="text-2xl mb-2">🍽️</div>
                <div className="text-sm font-medium text-gray-800">
                  {category.replaceAll('_', ' ')}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Popular Districts Preview */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Distritos Destacados</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {districts.slice(0, 5).map((district: string) => (
            <div
              key={district}
              className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-200"
            >
              <div className="text-center">
                <div className="text-2xl mb-2">📍</div>
                <div className="text-sm font-medium text-gray-800">
                  {district.replaceAll('_', ' ')}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};