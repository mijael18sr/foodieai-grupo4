import { useCallback, useEffect, useState } from 'react';
import { useGeolocated } from 'react-geolocated';

export interface LocationState {
  lat: number;
  long: number;
  accuracy?: number;
  timestamp?: number;
}

export interface UseLocationReturn {
  location: LocationState | null;
  isLoading: boolean;
  isAvailable: boolean;
  isEnabled: boolean;
  error: string | null;
  requestLocation: () => void;
}

const DEFAULT_LOCATION: LocationState = {
  lat: -12.0464,
  long: -77.0428,
};

export function useLocation(): UseLocationReturn {
  const [location, setLocation] = useState<LocationState | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    coords,
    isGeolocationAvailable,
    isGeolocationEnabled,
    positionError,
    getPosition,
  } = useGeolocated({
    suppressLocationOnMount: true,
    positionOptions: {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 300000,
    },
    onSuccess: (position) => {
      setLocation({
        lat: position.coords.latitude,
        long: position.coords.longitude,
        accuracy: position.coords.accuracy,
        timestamp: position.timestamp,
      });
      setIsLoading(false);
      setError(null);
    },
    onError: (error) => {
      setIsLoading(false);
      if (error) {
        switch (error.code) {
          case error.PERMISSION_DENIED:
            setError('Permiso de ubicación denegado');
            break;
          case error.POSITION_UNAVAILABLE:
            setError('Ubicación no disponible');
            break;
          case error.TIMEOUT:
            setError('Tiempo de espera agotado');
            break;
          default:
            setError('Error al obtener ubicación');
        }
      }
      setLocation(DEFAULT_LOCATION);
    },
  });

  useEffect(() => {
    if (coords && !location) {
      setLocation({
        lat: coords.latitude,
        long: coords.longitude,
        accuracy: coords.accuracy ?? undefined,
      });
      setIsLoading(false);
    }
  }, [coords, location]);

  useEffect(() => {
    if (positionError && isLoading) {
      setIsLoading(false);
      setLocation(DEFAULT_LOCATION);
    }
  }, [positionError, isLoading]);

  const requestLocation = useCallback(() => {
    if (!isGeolocationAvailable) {
      setError('Tu navegador no soporta geolocalización');
      setLocation(DEFAULT_LOCATION);
      return;
    }

    setIsLoading(true);
    setError(null);
    getPosition();
  }, [isGeolocationAvailable, getPosition]);

  return {
    location,
    isLoading,
    isAvailable: isGeolocationAvailable,
    isEnabled: isGeolocationEnabled,
    error,
    requestLocation,
  };
}

export default useLocation;
