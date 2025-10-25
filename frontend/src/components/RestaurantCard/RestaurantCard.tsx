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
      className="glass rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-500 cursor-pointer border border-white/20 backdrop-blur-lg group hover:scale-[1.02] animate-slide-up focus-ring w-full text-left"
      onClick={onClick}
    >
      <div className="p-6 relative overflow-hidden">
        {/* Animated background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 via-secondary-500/10 to-accent-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        
        <div className="relative z-10">
          {/* Header */}
          <div className="flex justify-between items-start mb-4">
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-primary-100 transition-colors">
                {restaurant.name}
              </h3>
              <div className="flex items-center gap-2 mb-2">
                <span className="glass-dark px-3 py-1 rounded-full text-xs font-medium text-white/90">
                  {restaurant.category}
                </span>
                <span className="text-white/70 text-sm">•</span>
                <span className="text-white/80 text-sm font-medium">
                  {restaurant.district}
                </span>
              </div>
            </div>
            
            {/* Rating */}
            <div className="flex items-center glass px-4 py-2 rounded-full backdrop-blur-md">
              <span className="text-accent-400 text-lg mr-1">⭐</span>
              <span className="text-black font-bold text-sm">
                {restaurant.rating.toFixed(1)}
              </span>
            </div>
          </div>

          {/* Address */}
          {restaurant.address && (
            <div className="mb-4 flex items-start gap-2">
              <span className="text-secondary-400 text-sm mt-0.5">📍</span>
              <p className="text-white/80 text-sm leading-relaxed">
                {restaurant.address}
              </p>
            </div>
          )}

          {/* Metrics Grid */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="glass-dark rounded-lg p-3 text-center">
              <div className="text-secondary-400 text-xs font-medium uppercase tracking-wide mb-1">
                Distancia
              </div>
              <div className="text-white font-bold">
                {distance_km.toFixed(1)} <span className="text-xs text-white/70">km</span>
              </div>
            </div>
            
            <div className="glass-dark rounded-lg p-3 text-center">
              <div className="text-primary-400 text-xs font-medium uppercase tracking-wide mb-1">
                Match Score
              </div>
              <div className="text-white font-bold">
                {(score * 100).toFixed(0)}<span className="text-xs text-white/70">%</span>
              </div>
            </div>
          </div>

          {/* Phone */}
          {restaurant.phone && (
            <div className="mb-4">
              <div className="glass-dark px-3 py-2 rounded-lg inline-flex items-center gap-2">
                <span className="text-accent-400 text-sm">📞</span>
                <span className="text-white/90 text-sm font-medium">
                  {restaurant.phone}
                </span>
              </div>
            </div>
          )}

          {/* Price Range */}
          {restaurant.price_range && (
            <div className="mb-4">
              <span className="glass px-3 py-2 rounded-full text-sm text-black font-medium inline-flex items-center gap-2">
                <span className="text-accent-400">💰</span>
                {restaurant.price_range}
              </span>
            </div>
          )}

          {/* Reasoning */}
          <div className="border-t border-white/20 pt-4 mt-4">
            <div className="mb-2">
              <span className="text-primary-400 text-xs font-bold uppercase tracking-wide">
                ¿Por qué te lo recomendamos?
              </span>
            </div>
            <p className="text-white/80 text-sm leading-relaxed italic">
              {reason}
            </p>
          </div>

          {/* Hover indicator */}
          <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="w-8 h-8 rounded-full glass-dark flex items-center justify-center">
              <span className="text-white text-sm">→</span>
            </div>
          </div>
        </div>
      </div>
    </button>
  );
});

export default RestaurantCard;