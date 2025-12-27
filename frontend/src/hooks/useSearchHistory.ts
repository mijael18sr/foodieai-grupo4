import { useCallback, useMemo } from 'react';
import { useLocalStorage } from './useLocalStorage';
import type { UserLocation, UserPreferences, RecommendationFilters, RecommendationItem } from '../types/api';

export interface SearchHistoryItem {
  id: string;
  timestamp: string;
  location: UserLocation;
  locationName?: string;
  preferences?: UserPreferences;
  filters?: RecommendationFilters;
  resultsCount: number;
  topResults: Array<{
    id: string;
    name: string;
    category: string;
    district: string;
    rating: number;
  }>;
}

interface UseSearchHistoryReturn {
  history: SearchHistoryItem[];
  addSearch: (
    location: UserLocation,
    locationName: string | undefined,
    preferences: UserPreferences | undefined,
    filters: RecommendationFilters | undefined,
    results: RecommendationItem[]
  ) => void;
  removeSearch: (searchId: string) => void;
  clearHistory: () => void;
  getRecentSearches: (limit?: number) => SearchHistoryItem[];
  count: number;
}

const STORAGE_KEY = 'foodieai_search_history';
const MAX_HISTORY = 20;

export function useSearchHistory(): UseSearchHistoryReturn {
  const [history, setHistory] = useLocalStorage<SearchHistoryItem[]>(STORAGE_KEY, []);

  const addSearch = useCallback((
    location: UserLocation,
    locationName: string | undefined,
    preferences: UserPreferences | undefined,
    filters: RecommendationFilters | undefined,
    results: RecommendationItem[]
  ) => {
    const searchItem: SearchHistoryItem = {
      id: `search_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      location,
      locationName,
      preferences,
      filters,
      resultsCount: results.length,
      topResults: results.slice(0, 3).map((r) => ({
        id: r.restaurant.id,
        name: r.restaurant.name,
        category: r.restaurant.category,
        district: r.restaurant.district,
        rating: r.restaurant.rating,
      })),
    };

    setHistory((prev) => {
      const filtered = prev.filter(
        (h) =>
          h.location.lat !== location.lat ||
          h.location.long !== location.long ||
          h.preferences?.category !== preferences?.category ||
          h.filters?.district !== filters?.district
      );
      return [searchItem, ...filtered].slice(0, MAX_HISTORY);
    });
  }, [setHistory]);

  const removeSearch = useCallback((searchId: string) => {
    setHistory((prev) => prev.filter((h) => h.id !== searchId));
  }, [setHistory]);

  const clearHistory = useCallback(() => {
    setHistory([]);
  }, [setHistory]);

  const getRecentSearches = useCallback((limit = 5) => {
    return history.slice(0, limit);
  }, [history]);

  const count = useMemo(() => history.length, [history]);

  return {
    history,
    addSearch,
    removeSearch,
    clearHistory,
    getRecentSearches,
    count,
  };
}
