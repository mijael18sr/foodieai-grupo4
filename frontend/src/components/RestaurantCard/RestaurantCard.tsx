import { memo } from 'react';
import type { RecommendationItem } from '../../types/api';

interface RestaurantCardProps {
  recommendation: RecommendationItem;
  onClick?: () => void;
}

export const RestaurantCard = memo(function RestaurantCard({ recommendation, onClick }: RestaurantCardProps) {
  const { restaurant, score, reason } = recommendation;
  const distance_km = restaurant.distance_km;

  return (
    <button 
      className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer border border-slate-200 hover:border-blue-300 group hover:scale-[1.02] animate-slide-up focus-ring w-full text-left overflow-hidden"
      onClick={onClick}
    >
      <div className="p-6 relative">
        {/* KOSARI-style gradient accent */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600"></div>
        
        {/* Subtle hover background */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50/0 to-blue-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        
        <div className="relative z-10">
          {/* Header */}
          <div className="flex justify-between items-start mb-4">
            <div className="flex-1">
              <h3 className="text-xl font-bold text-slate-800 mb-2 group-hover:text-blue-700 transition-colors">
                {restaurant.name}
              </h3>
              <div className="flex items-center gap-2 mb-2">
                <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-lg text-xs font-semibold border border-blue-200">
                  {restaurant.category}
                </span>
                <span className="text-slate-400 text-sm">•</span>
                <span className="text-slate-600 text-sm font-medium">
                  {restaurant.district}
                </span>
              </div>
            </div>
            
            {/* Rating - KOSARI Style */}
            <div className="flex items-center bg-gradient-to-r from-yellow-400 to-orange-400 px-4 py-2 rounded-xl shadow-md">
              <span className="text-white text-lg mr-1">⭐</span>
              <span className="text-white font-bold text-sm drop-shadow-sm">
                {restaurant.rating.toFixed(1)}
              </span>
            </div>
          </div>

          {/* Address - KOSARI Style */}
          {restaurant.address && (
            <div className="mb-4 flex items-start gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-blue-500 text-sm mt-0.5">📍</span>
              <p className="text-slate-700 text-sm leading-relaxed font-medium">
                {restaurant.address}
              </p>
            </div>
          )}

          {/* Metrics Grid - KOSARI Professional Style */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-gradient-to-br from-slate-100 to-slate-200 rounded-xl p-4 text-center border border-slate-300/50 shadow-sm">
              <div className="text-slate-600 text-xs font-semibold uppercase tracking-wide mb-2">
                Distancia
              </div>
              <div className="text-slate-800 font-bold text-lg">
                {distance_km.toFixed(1)} <span className="text-sm text-slate-600 font-medium">km</span>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl p-4 text-center border border-blue-300/50 shadow-sm">
              <div className="text-blue-700 text-xs font-semibold uppercase tracking-wide mb-2">
                Match Score
              </div>
              <div className="text-blue-800 font-bold text-lg">
                {(score * 100).toFixed(0)}<span className="text-sm text-blue-600 font-medium">%</span>
              </div>
            </div>
          </div>

          {/* Phone - KOSARI Style */}
          {restaurant.phone && (
            <div className="mb-4">
              <div className="bg-green-50 border border-green-200 px-4 py-2 rounded-xl inline-flex items-center gap-3">
                <span className="text-green-600 text-sm">📞</span>
                <span className="text-green-800 text-sm font-semibold">
                  {restaurant.phone}
                </span>
              </div>
            </div>
          )}

          {/* Reasoning - KOSARI Professional Style */}
          <div className="border-t border-slate-200 pt-4 mt-4">
            <div className="mb-3">
              <span className="text-blue-700 text-xs font-bold uppercase tracking-wide flex items-center gap-2">
                <span>🤖</span>
                ¿Por qué te lo recomendamos?
              </span>
            </div>
            <p className="text-slate-600 text-sm leading-relaxed bg-blue-50 p-3 rounded-xl border border-blue-100 italic">
              {reason}
            </p>
          </div>

          {/* Hover indicator - KOSARI Style */}
          <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-2 group-hover:translate-x-0">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-600 to-blue-700 flex items-center justify-center shadow-lg">
              <span className="text-white text-sm font-bold">→</span>
            </div>
          </div>
        </div>
      </div>
    </button>
  );
});

export default RestaurantCard;