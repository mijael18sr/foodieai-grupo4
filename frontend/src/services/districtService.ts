/**
 * Servicio para gestión de distritos de Lima
 * Consume la API del backend para obtener información de distritos
 */

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

class DistrictService {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  /**
   * Obtiene todos los distritos para el dropdown
   */
  async getDistrictsForDropdown(): Promise<District[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/districts/`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const districts: District[] = await response.json();
      
      console.log(`✅ Cargados ${districts.length} distritos desde API`);
      return districts;
      
    } catch (error) {
      console.error('❌ Error al obtener distritos:', error);
      
      // Fallback con datos hardcodeados basados en los resultados de la prueba
      return this.getFallbackDistricts();
    }
  }

  /**
   * Obtiene información detallada de un distrito específico
   */
  async getDistrictInfo(districtName: string): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/districts/${districtName}`);
      
      if (!response.ok) {
        throw new Error(`Distrito no encontrado: ${districtName}`);
      }

      return await response.json();
      
    } catch (error) {
      console.error(`❌ Error al obtener información de ${districtName}:`, error);
      throw error;
    }
  }

  /**
   * Obtiene distritos recomendados según criterios
   */
  async getRecommendedDistricts(
    touristZoneOnly: boolean = false,
    minRating: number = 0,
    limit: number = 5
  ): Promise<District[]> {
    try {
      const params = new URLSearchParams({
        tourist_zone_only: touristZoneOnly.toString(),
        min_rating: minRating.toString(),
        limit: limit.toString()
      });

      const response = await fetch(`${this.baseUrl}/api/districts/recommendations/popular?${params}`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      return await response.json();
      
    } catch (error) {
      console.error('❌ Error al obtener distritos recomendados:', error);
      return [];
    }
  }

  /**
   * Obtiene estadísticas completas de distritos
   */
  async getDistrictStatistics(): Promise<DistrictStatisticsResponse | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/districts/statistics/summary`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      return await response.json();
      
    } catch (error) {
      console.error('❌ Error al obtener estadísticas de distritos:', error);
      return null;
    }
  }

  /**
   * Valida si un distrito existe
   */
  async validateDistrict(districtName: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/districts/${districtName}/validate`, {
        method: 'HEAD'
      });
      
      return response.ok;
      
    } catch (error) {
      console.error(`❌ Error al validar distrito ${districtName}:`, error);
      return false;
    }
  }

  /**
   * Datos de fallback basados en los resultados reales de la API
   * Estos datos coinciden exactamente con los del backend
   */
  private getFallbackDistricts(): District[] {
    return [
      {
        value: "Miraflores",
        label: "Miraflores", 
        restaurant_count: 185,
        is_tourist_zone: true,
        average_rating: 4.34,
        description: "Distrito turístico con amplia oferta gastronómica y vista al mar"
      },
      {
        value: "Lince",
        label: "Lince",
        restaurant_count: 174, 
        is_tourist_zone: false,
        average_rating: 4.25,
        description: "Distrito residencial con variada oferta gastronómica local"
      },
      {
        value: "Magdalena",
        label: "Magdalena del Mar",
        restaurant_count: 169,
        is_tourist_zone: false,
        average_rating: 4.22,
        description: "Distrito costero con restaurantes tradicionales y marisquerías"
      },
      {
        value: "San_Isidro", 
        label: "San Isidro",
        restaurant_count: 143,
        is_tourist_zone: true,
        average_rating: 4.34,
        description: "Distrito financiero con restaurantes de alta gama y cocina internacional"
      },
      {
        value: "Barranco",
        label: "Barranco",
        restaurant_count: 132,
        is_tourist_zone: true, 
        average_rating: 4.36,
        description: "Distrito bohemio conocido por su vida nocturna y gastronomía creativa"
      },
      {
        value: "Surquillo",
        label: "Surquillo",
        restaurant_count: 128,
        is_tourist_zone: false,
        average_rating: 4.24,
        description: "Distrito con mercados gastronómicos y cocina popular"
      },
      {
        value: "Surco",
        label: "Santiago de Surco", 
        restaurant_count: 121,
        is_tourist_zone: false,
        average_rating: 4.20,
        description: "Distrito moderno con centros comerciales y restaurantes familiares"
      }
    ];
  }
}

// Singleton instance
export const districtService = new DistrictService();
export default districtService;