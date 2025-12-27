import { apiClient } from './client';

export interface District {
  value: string;
  label: string;
  restaurant_count: number;
  description?: string;
  is_tourist_zone: boolean;
  average_rating?: number;
}

export interface DistrictStatistics {
  total_districts: number;
  total_restaurants: number;
  avg_restaurants_per_district: number;
  avg_rating_across_districts: number;
  most_popular_district: string;
  highest_rated_district: string;
}

export interface DistrictStatisticsResponse {
  summary: DistrictStatistics;
  districts: District[];
}

const FALLBACK_DISTRICTS: District[] = [
  { value: "Miraflores", label: "Miraflores", restaurant_count: 185, is_tourist_zone: true, average_rating: 4.34 },
  { value: "Lince", label: "Lince", restaurant_count: 174, is_tourist_zone: false, average_rating: 4.25 },
  { value: "Magdalena", label: "Magdalena del Mar", restaurant_count: 169, is_tourist_zone: false, average_rating: 4.22 },
  { value: "San_Isidro", label: "San Isidro", restaurant_count: 143, is_tourist_zone: true, average_rating: 4.34 },
  { value: "Barranco", label: "Barranco", restaurant_count: 132, is_tourist_zone: true, average_rating: 4.36 },
  { value: "Surquillo", label: "Surquillo", restaurant_count: 128, is_tourist_zone: false, average_rating: 4.24 },
  { value: "Surco", label: "Santiago de Surco", restaurant_count: 121, is_tourist_zone: false, average_rating: 4.20 },
];

export class DistrictService {
  async getDistrictsForDropdown(): Promise<District[]> {
    try {
      const { data } = await apiClient.get<District[]>('/api/districts/');
      return data;
    } catch {
      return FALLBACK_DISTRICTS;
    }
  }

  async getDistrictInfo(districtName: string): Promise<District> {
    const { data } = await apiClient.get<District>(`/api/districts/${districtName}`);
    return data;
  }

  async getRecommendedDistricts(
    touristZoneOnly = false,
    minRating = 0,
    limit = 5
  ): Promise<District[]> {
    try {
      const { data } = await apiClient.get<District[]>('/api/districts/recommendations/popular', {
        params: { tourist_zone_only: touristZoneOnly, min_rating: minRating, limit }
      });
      return data;
    } catch {
      return [];
    }
  }

  async getDistrictStatistics(): Promise<DistrictStatisticsResponse | null> {
    try {
      const { data } = await apiClient.get<DistrictStatisticsResponse>('/api/districts/statistics/summary');
      return data;
    } catch {
      return null;
    }
  }

  async validateDistrict(districtName: string): Promise<boolean> {
    try {
      await apiClient.head(`/api/districts/${districtName}/validate`);
      return true;
    } catch {
      return false;
    }
  }
}

export const districtService = new DistrictService();
export default districtService;