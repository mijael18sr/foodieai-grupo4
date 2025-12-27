import { useCallback, useMemo } from 'react';
import { useLocalStorage } from './useLocalStorage';
import type { Restaurant } from '../types/api';

export interface FavoriteRestaurant extends Restaurant {
  addedAt: string;
  notes?: string;
}

interface UseFavoritesReturn {
  favorites: FavoriteRestaurant[];
  addFavorite: (restaurant: Restaurant, notes?: string) => void;
  removeFavorite: (restaurantId: string) => void;
  isFavorite: (restaurantId: string) => boolean;
  toggleFavorite: (restaurant: Restaurant) => void;
  updateNotes: (restaurantId: string, notes: string) => void;
  clearFavorites: () => void;
  count: number;
}

const STORAGE_KEY = 'foodieai_favorites';
const MAX_FAVORITES = 50;

export function useFavorites(): UseFavoritesReturn {
  const [favorites, setFavorites] = useLocalStorage<FavoriteRestaurant[]>(STORAGE_KEY, []);

  const addFavorite = useCallback((restaurant: Restaurant, notes?: string) => {
    setFavorites((prev) => {
      if (prev.some((f) => f.id === restaurant.id)) {
        return prev;
      }
      const newFavorite: FavoriteRestaurant = {
        ...restaurant,
        addedAt: new Date().toISOString(),
        notes,
      };
      const updated = [newFavorite, ...prev];
      return updated.slice(0, MAX_FAVORITES);
    });
  }, [setFavorites]);

  const removeFavorite = useCallback((restaurantId: string) => {
    setFavorites((prev) => prev.filter((f) => f.id !== restaurantId));
  }, [setFavorites]);

  const isFavorite = useCallback((restaurantId: string) => {
    return favorites.some((f) => f.id === restaurantId);
  }, [favorites]);

  const toggleFavorite = useCallback((restaurant: Restaurant) => {
    if (isFavorite(restaurant.id)) {
      removeFavorite(restaurant.id);
    } else {
      addFavorite(restaurant);
    }
  }, [isFavorite, removeFavorite, addFavorite]);

  const updateNotes = useCallback((restaurantId: string, notes: string) => {
    setFavorites((prev) =>
      prev.map((f) => (f.id === restaurantId ? { ...f, notes } : f))
    );
  }, [setFavorites]);

  const clearFavorites = useCallback(() => {
    setFavorites([]);
  }, [setFavorites]);

  const count = useMemo(() => favorites.length, [favorites]);

  return {
    favorites,
    addFavorite,
    removeFavorite,
    isFavorite,
    toggleFavorite,
    updateNotes,
    clearFavorites,
    count,
  };
}
