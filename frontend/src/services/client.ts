import axios, { AxiosError } from 'axios';
import type { ApiError } from '../types/api';
import { API_CONFIG } from '../constants/config';

export const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    const message = error.response?.data?.detail 
      || error.message 
      || 'Error de conexión';
    return Promise.reject(new Error(message));
  }
);
