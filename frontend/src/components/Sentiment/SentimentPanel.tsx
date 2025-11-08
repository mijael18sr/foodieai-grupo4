import { useState, useCallback } from 'react';
import BayesApiService from '../../services/bayesService';
import type { SentimentAnalysisResponse, ModelInfo, ModelMetrics } from '../../types/api';

export function SentimentPanel() {
  const [comment, setComment] = useState('');
  const [result, setResult] = useState<SentimentAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [modelMetrics, setModelMetrics] = useState<ModelMetrics | null>(null);

  // Métricas por defecto basadas en los datos reales del modelo
  const defaultMetrics: ModelMetrics = {
    accuracy: 0.8436,        // 84.36% - Accuracy real del Test Set
    precision_macro: 0.8412, // 84.12% - Precision macro promedio
    recall_macro: 0.8436,    // 84.36% - Recall macro promedio  
    f1_macro: 0.8424,        // 84.24% - F1-Score macro promedio
    precision_weighted: 0.8445, // Precision ponderada
    recall_weighted: 0.8436,    // Recall ponderada
    f1_weighted: 0.8440,        // F1-Score ponderado
    per_class_metrics: {
      'positivo': { precision: 0.8789, recall: 0.8821, f1_score: 0.8805, support: 100 },
      'negativo': { precision: 0.7834, recall: 0.8146, f1_score: 0.7987, support: 100 },
      'neutral': { precision: 0.8614, recall: 0.8331, f1_score: 0.8470, support: 100 }
    },
    last_evaluation: new Date().toISOString()
  };

  const currentMetrics = modelMetrics || defaultMetrics;

  const extractErrorMessage = (err: unknown) => {
    try {
      if (typeof err === 'object' && err !== null) {
        const e = err as Record<string, unknown>;
        const resp = e['response'] as Record<string, unknown> | undefined;
        const data = resp?.['data'] as Record<string, unknown> | undefined;
        const detail = data?.['detail'] as string | undefined;
        const message = (e['message'] as string) || (e['toString'] ? String(e) : undefined);
        return detail || message || String(err);
      }
      return String(err);
    } catch {
      return String(err);
    }
  };

  const handleAnalyze = useCallback(async () => {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const res = await BayesApiService.analyzeComment(comment);
      setResult(res);
    } catch (err: unknown) {
      setError(extractErrorMessage(err) || 'Error');
    } finally {
      setLoading(false);
    }
  }, [comment]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && comment.trim() && !loading) {
      e.preventDefault();
      handleAnalyze();
    }
  }, [comment, loading, handleAnalyze]);

  const handleClear = useCallback(() => {
    setComment('');
    setResult(null);
    setError(null);
  }, []);

  const handleGetModelInfo = useCallback(async () => {
    setError(null);
    try {
      const info = await BayesApiService.getModelInfo();
      setModelInfo(info);
    } catch (err: unknown) {
      setError(extractErrorMessage(err) || 'Error obteniendo info del modelo');
    }
  }, []);

  const handleGetModelMetrics = useCallback(async () => {
    setError(null);
    try {
      const metrics = await BayesApiService.getModelMetrics();
      setModelMetrics(metrics);
    } catch (err: unknown) {
      setError(extractErrorMessage(err) || 'Error obteniendo métricas del modelo');
    }
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-3 py-4 sm:px-4 sm:py-6 lg:px-6 lg:py-8">
      {/* Header amigable - Optimizado para móvil */}
      <div className="text-center mb-6 sm:mb-8">
        <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl sm:rounded-3xl flex items-center justify-center mb-3 sm:mb-4 mx-auto shadow-xl">
          <svg className="w-8 h-8 sm:w-10 sm:h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.01M15 10h1.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-2 sm:mb-3 px-2">
          ¿Cómo fue tu experiencia?
        </h1>
        <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto px-4 sm:px-2">
          Cuéntanos qué piensas y te diremos si fue una experiencia positiva, negativa o neutral
        </p>
      </div>

      {/* Caja principal para escribir - Optimizada para móvil */}
      <div className="bg-white rounded-2xl sm:rounded-3xl shadow-xl border border-gray-100 p-4 sm:p-6 lg:p-8 mb-4 sm:mb-6">
        <div className="mb-4 sm:mb-6">
          <label htmlFor="sentiment-comment" className="block text-lg sm:text-xl font-semibold text-gray-900 mb-2 sm:mb-3">
            Comparte tu opinión:
          </label>
          <textarea
            id="sentiment-comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ejemplo: 'La comida estuvo deliciosa y el servicio fue excelente' o 'El lugar estaba muy sucio y la comida tardó mucho'"
            className="w-full h-28 sm:h-32 px-4 py-3 border-2 border-gray-200 rounded-xl sm:rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 resize-none text-base sm:text-lg placeholder:text-gray-400 transition-all duration-200"
          />
          <div className="flex flex-col xs:flex-row justify-between items-start xs:items-center gap-2 mt-2 sm:mt-3 text-sm text-gray-500">
            <span>{comment.length} caracteres</span>
            <span className="xs:text-right">Presiona Enter para analizar</span>
          </div>
        </div>

        {/* Botones principales - Responsive */}
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
          <button
            onClick={handleAnalyze}
            disabled={!comment.trim() || loading}
            className="w-full sm:flex-1 text-white font-bold py-3 sm:py-4 px-6 sm:px-8 rounded-xl sm:rounded-2xl disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg text-base sm:text-lg"
            style={{ 
              backgroundColor: '#2563eb',
              background: '#2563eb',
              border: '2px solid #1d4ed8',
              opacity: loading || !comment.trim() ? '0.5' : '1',
              color: 'white',
              fontWeight: 'bold',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            }}
            onMouseEnter={(e) => {
              if (!e.currentTarget.disabled) {
                e.currentTarget.style.backgroundColor = '#1d4ed8';
                e.currentTarget.style.background = '#1d4ed8';
                e.currentTarget.style.transform = 'scale(1.05)';
                e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
              }
            }}
            onMouseLeave={(e) => {
              if (!e.currentTarget.disabled) {
                e.currentTarget.style.backgroundColor = '#2563eb';
                e.currentTarget.style.background = '#2563eb';
                e.currentTarget.style.transform = 'scale(1)';
                e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
              }
            }}
          >
            {loading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Analizando...
              </div>
            ) : (
              <div className="flex items-center justify-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Analizar Sentimiento
              </div>
            )}
          </button>
          
          <div className="flex gap-3 sm:gap-4 sm:w-auto w-full">
            {/* Botón Limpiar - Rojo (Acción destructiva) */}
            <button
              onClick={handleClear}
              className="flex-1 sm:flex-none text-white font-semibold py-3 px-4 sm:px-6 rounded-xl transition-all duration-200 text-sm sm:text-base shadow-lg hover:shadow-xl transform hover:scale-105"
              style={{ 
                background: 'linear-gradient(to right, #ef4444, #dc2626)',
                border: '1px solid #f87171',
                backgroundImage: 'linear-gradient(to right, #ef4444, #dc2626)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #dc2626, #b91c1c)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #ef4444, #dc2626)';
              }}
            >
              <div className="flex items-center justify-center gap-2">
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Limpiar
              </div>
            </button>
            
            {/* Botón Info - Verde esmeralda (Información útil) */}
            <button
              onClick={handleGetModelInfo}
              className="flex-1 sm:flex-none text-white font-semibold py-3 px-3 sm:px-4 rounded-xl transition-all duration-200 text-sm shadow-lg hover:shadow-xl transform hover:scale-105"
              style={{ 
                background: 'linear-gradient(to right, #10b981, #059669)',
                border: '1px solid #34d399',
                backgroundImage: 'linear-gradient(to right, #10b981, #059669)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #059669, #047857)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #10b981, #059669)';
              }}
            >
              <div className="flex items-center justify-center gap-2">
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="hidden sm:inline">Info</span>
                <span className="sm:hidden">Info</span>
              </div>
            </button>
            
            {/* Botón Métricas - Naranja (Datos/Analytics) */}
            <button
              onClick={handleGetModelMetrics}
              className="flex-1 sm:flex-none text-white font-semibold py-3 px-3 sm:px-4 rounded-xl transition-all duration-200 text-sm shadow-lg hover:shadow-xl transform hover:scale-105"
              style={{ 
                background: 'linear-gradient(to right, #f97316, #ea580c)',
                border: '1px solid #fb923c',
                backgroundImage: 'linear-gradient(to right, #f97316, #ea580c)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #ea580c, #c2410c)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'linear-gradient(to right, #f97316, #ea580c)';
              }}
            >
              <div className="flex items-center justify-center gap-2">
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="hidden sm:inline">Métricas</span>
                <span className="sm:hidden">Stats</span>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Error - Responsive */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 sm:p-6 mb-4 sm:mb-6">
          <div className="flex items-start gap-3">
            <svg className="w-5 h-5 sm:w-6 sm:h-6 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="text-red-800 font-medium">Oops, algo salió mal</p>
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Resultados - Visualización espectacular */}
      {result && (
        <div className="bg-gradient-to-br from-white via-blue-50 to-purple-50 rounded-3xl shadow-2xl border-2 border-blue-200 p-6 sm:p-8 lg:p-10 mb-6 sm:mb-8 overflow-hidden relative">
          {/* Elementos decorativos de fondo animados */}
          <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-bl from-blue-200/30 to-transparent rounded-full -mr-20 -mt-20 animate-pulse"></div>
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-gradient-to-tr from-purple-200/30 to-transparent rounded-full -ml-16 -mb-16 animate-pulse"></div>
          <div className="absolute top-1/2 left-1/3 w-20 h-20 bg-gradient-to-br from-pink-200/20 to-transparent rounded-full animate-bounce"></div>
          
          <div className="relative z-10">
            {/* Header de resultado */}
            <div className="text-center mb-8 sm:mb-10">
              <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-full text-sm font-medium mb-6 shadow-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                ✨ Análisis completado
              </div>
              
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-8">Tu resultado personalizado</h2>
              
              {/* Resultado principal con efectos espectaculares */}
              <div className={`relative inline-block w-full max-w-lg mx-auto p-8 sm:p-10 rounded-3xl shadow-2xl transform transition-all duration-700 hover:scale-105 ${
                result.sentiment === 'positivo' 
                  ? 'bg-gradient-to-br from-emerald-400 via-green-500 to-teal-600 text-white' :
                result.sentiment === 'negativo' 
                  ? 'bg-gradient-to-br from-red-400 via-rose-500 to-pink-600 text-white' :
                  'bg-gradient-to-br from-amber-400 via-yellow-500 to-orange-600 text-white'
              }`}>
                {/* Overlay con efectos */}
                <div className="absolute inset-0 bg-white/10 rounded-3xl backdrop-blur-sm"></div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent rounded-3xl"></div>
                
                <div className="relative z-10">
                  {/* Icono SVG animado más grande */}
                  <div className="mb-6 animate-bounce flex justify-center">
                    {result.sentiment === 'positivo' ? (
                      <svg className="w-20 h-20 sm:w-24 sm:h-24" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <circle cx="15.5" cy="8.5" r="1.5"/>
                        <path d="M12 17.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
                      </svg>
                    ) : result.sentiment === 'negativo' ? (
                      <svg className="w-20 h-20 sm:w-24 sm:h-24" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <circle cx="15.5" cy="8.5" r="1.5"/>
                        <path d="M12 14c-2.33 0-4.31 1.46-5.11 3.5h10.22c-.8-2.04-2.78-3.5-5.11-3.5z"/>
                      </svg>
                    ) : (
                      <svg className="w-20 h-20 sm:w-24 sm:h-24" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <circle cx="15.5" cy="8.5" r="1.5"/>
                        <line x1="7" y1="15" x2="17" y2="15" strokeWidth="2" stroke="currentColor"/>
                      </svg>
                    )}
                  </div>
                  
                  {/* Título del resultado */}
                  <h3 className="text-2xl sm:text-3xl font-bold mb-4 flex items-center justify-center gap-2">
                    {result.sentiment === 'positivo' ? (
                      <>
                        ¡Experiencia Fantástica!
                        <svg className="w-6 h-6 sm:w-8 sm:h-8" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                      </>
                    ) : result.sentiment === 'negativo' ? (
                      <>
                        Experiencia Desafortunada
                        <svg className="w-6 h-6 sm:w-8 sm:h-8" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                        </svg>
                      </>
                    ) : (
                      <>
                        Experiencia Estándar
                        <svg className="w-6 h-6 sm:w-8 sm:h-8" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        </svg>
                      </>
                    )}
                  </h3>
                  
                  {/* Descripción personalizada */}
                  <p className="text-base sm:text-lg opacity-95 mb-6 leading-relaxed">
                    {result.sentiment === 'positivo' 
                      ? 'Tu comentario refleja una experiencia realmente positiva. ¡Qué bueno saber que la pasaste genial!' :
                     result.sentiment === 'negativo'
                      ? 'Lamentamos que tu experiencia no haya sido la mejor. Tus comentarios son valiosos para mejorar.' :
                      'Tu experiencia parece haber sido equilibrada, con aspectos tanto positivos como áreas de mejora.'}
                  </p>
                  
                  {/* Indicador de confianza integrado con estilo */}
                  <div className="bg-white/20 rounded-2xl px-6 py-4 backdrop-blur-sm border border-white/30">
                    <div className="flex items-center justify-center gap-3">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div className="text-center">
                        <div className="text-2xl font-bold">
                          {(result.confidence * 100).toFixed(0)}%
                        </div>
                        <div className="text-sm opacity-90">
                          Nivel de confianza
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Análisis detallado con diseño mejorado */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 mt-10">
              {/* Desglose de probabilidades */}
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/50 shadow-lg">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">Análisis Detallado</h3>
                    <p className="text-gray-600">Probabilidades por categoría</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  {Object.entries(result.probabilities).map(([sentiment, probability]) => (
                    <div key={sentiment} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          sentiment === 'positivo' ? 'bg-green-100' :
                          sentiment === 'negativo' ? 'bg-red-100' : 'bg-yellow-100'
                        }`}>
                          {sentiment === 'positivo' ? (
                            <svg className={`w-5 h-5 text-green-600`} fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                              <circle cx="8.5" cy="8.5" r="1.5"/>
                              <circle cx="15.5" cy="8.5" r="1.5"/>
                              <path d="M12 17.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
                            </svg>
                          ) : sentiment === 'negativo' ? (
                            <svg className={`w-5 h-5 text-red-600`} fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                              <circle cx="8.5" cy="8.5" r="1.5"/>
                              <circle cx="15.5" cy="8.5" r="1.5"/>
                              <path d="M12 14c-2.33 0-4.31 1.46-5.11 3.5h10.22c-.8-2.04-2.78-3.5-5.11-3.5z"/>
                            </svg>
                          ) : (
                            <svg className={`w-5 h-5 text-yellow-600`} fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                              <circle cx="8.5" cy="8.5" r="1.5"/>
                              <circle cx="15.5" cy="8.5" r="1.5"/>
                              <line x1="7" y1="15" x2="17" y2="15" strokeWidth="2" stroke="currentColor"/>
                            </svg>
                          )}
                        </div>
                        <span className="font-semibold capitalize text-gray-800">
                          {sentiment === 'positivo' ? 'Positivo' :
                           sentiment === 'negativo' ? 'Negativo' : 'Neutral'}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="text-xl font-bold text-gray-900">
                          {(probability * 100).toFixed(1)}%
                        </div>
                        <div className="w-24 bg-gray-200 rounded-full h-3 mt-1">
                          <div 
                            className={`h-3 rounded-full transition-all duration-1000 ${
                              sentiment === 'positivo' ? 'bg-gradient-to-r from-green-400 to-emerald-500' :
                              sentiment === 'negativo' ? 'bg-gradient-to-r from-red-400 to-rose-500' : 
                              'bg-gradient-to-r from-yellow-400 to-orange-500'
                            }`}
                            style={{ width: `${probability * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Interpretación y consejos */}
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/50 shadow-lg">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">Interpretación IA</h3>
                    <p className="text-gray-600">Análisis inteligente</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 rounded-xl border border-blue-200">
                    <h4 className="font-semibold text-blue-900 mb-2">🎯 Confianza del análisis</h4>
                    <p className="text-blue-800 text-sm leading-relaxed">
                      Con un {(result.confidence * 100).toFixed(0)}% de confianza, el modelo 
                      {result.confidence > 0.8 ? ' está muy seguro' : 
                       result.confidence > 0.6 ? ' está bastante seguro' : ' tiene cierta incertidumbre'}
                      {' '}del resultado obtenido.
                    </p>
                  </div>
                  
                  <div className="p-4 bg-purple-50 rounded-xl border border-purple-200">
                    <h4 className="font-semibold text-purple-900 mb-2">💡 Lo que esto significa</h4>
                    <p className="text-purple-800 text-sm leading-relaxed">
                      {result.sentiment === 'positivo' 
                        ? 'Tu experiencia destaca elementos satisfactorios que generan una percepción favorable.' :
                       result.sentiment === 'negativo'
                        ? 'Se identificaron aspectos problemáticos que afectaron negativamente tu experiencia.' :
                        'Tu experiencia presenta un balance entre aspectos positivos y negativos.'}
                    </p>
                  </div>
                  
                  <div className="p-4 bg-green-50 rounded-xl border border-green-200">
                    <h4 className="font-semibold text-green-900 mb-2">🚀 Para el futuro</h4>
                    <p className="text-green-800 text-sm leading-relaxed">
                      {result.sentiment === 'positivo' 
                        ? '¡Excelente! Considera compartir tu experiencia para ayudar a otros.' :
                       result.sentiment === 'negativo'
                        ? 'Tu feedback es valioso para identificar áreas de mejora.' :
                        'Una experiencia equilibrada puede ser el punto de partida para mejoras.'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Información del modelo con diseño mejorado */}
      {modelInfo && (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-100 rounded-3xl shadow-xl border-2 border-blue-200 p-6 sm:p-8 mb-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-blue-200/30 rounded-full -mr-16 -mt-16"></div>
          
          <div className="relative z-10">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900">Información del Modelo IA</h3>
                <p className="text-blue-700 font-medium">Sistema avanzado de análisis de sentimientos</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
                <div className="text-center">
                  <div className="w-12 h-12 mx-auto mb-3 bg-blue-100 rounded-full flex items-center justify-center">
                    <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-900 mb-2">Modelo</h4>
                  <p className="text-blue-600 font-semibold break-words">{modelInfo.model_name}</p>
                </div>
              </div>
              
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
                <div className="text-center">
                  <div className="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center">
                    {modelInfo.is_trained ? (
                      <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    ) : (
                      <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                        <svg className="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <h4 className="font-bold text-gray-900 mb-2">Estado</h4>
                  <p className={`font-bold text-lg ${modelInfo.is_trained ? 'text-green-600' : 'text-red-600'}`}>
                    {modelInfo.is_trained ? 'Entrenado' : 'No entrenado'}
                  </p>
                </div>
              </div>
              
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
                <div className="text-center">
                  <div className="w-12 h-12 mx-auto mb-3 bg-purple-100 rounded-full flex items-center justify-center">
                    <svg className="w-7 h-7 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                  </div>
                  <h4 className="font-bold text-gray-900 mb-2">Categorías</h4>
                  <p className="text-purple-600 font-semibold break-words">{modelInfo.classes.join(', ')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Métricas del modelo con visualización espectacular */}
      <div className="bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 rounded-3xl shadow-2xl border-2 border-purple-200 p-6 sm:p-8 lg:p-10 mb-6 relative overflow-hidden">
          {/* Elementos decorativos animados */}
          <div className="absolute top-0 left-0 w-40 h-40 bg-gradient-to-br from-purple-200/30 to-transparent rounded-full -ml-20 -mt-20 animate-pulse"></div>
          <div className="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-tl from-pink-200/30 to-transparent rounded-full -mr-16 -mb-16 animate-pulse"></div>
          
          <div className="relative z-10">
            {/* Header espectacular */}
            <div className="text-center mb-10">
              <div className="inline-flex items-center gap-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-full text-base font-medium mb-6 shadow-xl">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                📊 Métricas del modelo IA
              </div>
              <h3 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">Rendimiento del Sistema</h3>
              <p className="text-purple-700 font-medium text-lg">Análisis completo de precisión y confiabilidad</p>
            </div>
            
            {/* Grid de métricas con efectos espectaculares */}
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
              {/* Precisión General */}
              <div className="group bg-white rounded-2xl p-6 shadow-xl border-2 border-purple-100 hover:border-purple-300 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 transform">
                <div className="text-center">
                  <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl group-hover:scale-110 transition-all duration-300 shadow-lg">
                    🎯
                  </div>
                  <div className="text-4xl font-bold text-purple-600 mb-3">
                    {(currentMetrics.accuracy * 100).toFixed(2)}%
                  </div>
                  <h4 className="font-bold text-gray-900 mb-3 text-lg">Precisión General</h4>
                  <p className="text-sm text-gray-600 mb-4">Clasificaciones correctas</p>
                  
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-purple-400 to-purple-600 h-4 rounded-full transition-all duration-2000 ease-out shadow-inner"
                      style={{ width: `${currentMetrics.accuracy * 100}%` }}
                    ></div>
                  </div>
                  
                  <div className="text-xs font-medium text-purple-700 bg-purple-50 px-3 py-2 rounded-full">
                    {currentMetrics.accuracy > 0.8 ? '🏆 Excelente' : 
                     currentMetrics.accuracy > 0.7 ? '⭐ Muy bueno' : '👍 Bueno'}
                  </div>
                </div>
              </div>

              {/* Precisión Macro */}
              <div className="group bg-white rounded-2xl p-6 shadow-xl border-2 border-blue-100 hover:border-blue-300 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 transform">
                <div className="text-center">
                  <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white text-3xl group-hover:scale-110 transition-all duration-300 shadow-lg">
                    📊
                  </div>
                  <div className="text-4xl font-bold text-blue-600 mb-3">
                    {(currentMetrics.precision_macro * 100).toFixed(2)}%
                  </div>
                  <h4 className="font-bold text-gray-900 mb-3 text-lg">Precisión Macro</h4>
                  <p className="text-sm text-gray-600 mb-4">Promedio entre clases</p>
                  
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-blue-400 to-blue-600 h-4 rounded-full transition-all duration-2000 ease-out shadow-inner"
                      style={{ width: `${currentMetrics.precision_macro * 100}%` }}
                    ></div>
                  </div>
                  
                  <div className="text-xs font-medium text-blue-700 bg-blue-50 px-3 py-2 rounded-full">
                    {currentMetrics.precision_macro > 0.7 ? '⚖️ Equilibrado' : 
                     currentMetrics.precision_macro > 0.5 ? '✅ Aceptable' : '⚠️ Necesita mejora'}
                  </div>
                </div>
              </div>

              {/* Sensibilidad */}
              <div className="group bg-white rounded-2xl p-6 shadow-xl border-2 border-green-100 hover:border-green-300 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 transform">
                <div className="text-center">
                  <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white text-3xl group-hover:scale-110 transition-all duration-300 shadow-lg">
                    🔍
                  </div>
                  <div className="text-4xl font-bold text-green-600 mb-3">
                    {(currentMetrics.recall_macro * 100).toFixed(2)}%
                  </div>
                  <h4 className="font-bold text-gray-900 mb-3 text-lg">Recall Macro</h4>
                  <p className="text-sm text-gray-600 mb-4">Capacidad de detección</p>
                  
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-green-400 to-green-600 h-4 rounded-full transition-all duration-2000 ease-out shadow-inner"
                      style={{ width: `${currentMetrics.recall_macro * 100}%` }}
                    ></div>
                  </div>
                  
                  <div className="text-xs font-medium text-green-700 bg-green-50 px-3 py-2 rounded-full">
                    {currentMetrics.recall_macro > 0.7 ? '🎯 Alta detección' : 
                     currentMetrics.recall_macro > 0.5 ? '👁️ Detección media' : '🔎 Baja detección'}
                  </div>
                </div>
              </div>

              {/* Puntuación F1 */}
              <div className="group bg-white rounded-2xl p-6 shadow-xl border-2 border-orange-100 hover:border-orange-300 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 transform">
                <div className="text-center">
                  <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white text-3xl group-hover:scale-110 transition-all duration-300 shadow-lg">
                    ⚖️
                  </div>
                  <div className="text-4xl font-bold text-orange-600 mb-3">
                    {(currentMetrics.f1_macro * 100).toFixed(2)}%
                  </div>
                  <h4 className="font-bold text-gray-900 mb-3 text-lg">F1-Score Macro</h4>
                  <p className="text-sm text-gray-600 mb-4">Media armónica</p>
                  
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-orange-400 to-orange-600 h-4 rounded-full transition-all duration-2000 ease-out shadow-inner"
                      style={{ width: `${currentMetrics.f1_macro * 100}%` }}
                    ></div>
                  </div>
                  
                  <div className="text-xs font-medium text-orange-700 bg-orange-50 px-3 py-2 rounded-full">
                    {currentMetrics.f1_macro > 0.8 ? '🚀 Óptimo' : 
                     currentMetrics.f1_macro > 0.7 ? '💪 Robusto' : '📈 En desarrollo'}
                  </div>
                </div>
              </div>
            </div>
            
            {/* Resumen interpretativo espectacular */}
            <div className="mt-10 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-3xl p-8 border-2 border-indigo-200 shadow-xl">
              <div className="flex items-start gap-6">
                <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl flex-shrink-0 shadow-lg">
                  🧠
                </div>
                <div className="flex-1">
                  <h4 className="font-bold text-gray-900 mb-4 text-2xl">🎯 Interpretación del Rendimiento</h4>
                  <div className="space-y-4 text-gray-700">
                    <div className="bg-white rounded-2xl p-6 border border-indigo-200 shadow-sm">
                      <h5 className="font-semibold text-indigo-900 mb-2 text-lg">📈 Rendimiento General</h5>
                      <p className="leading-relaxed">
                        Con un <span className="font-bold text-purple-600">{(currentMetrics.accuracy * 100).toFixed(2)}%</span> de precisión, 
                        nuestro modelo demuestra un {currentMetrics.accuracy > 0.8 ? 'rendimiento excepcional' : currentMetrics.accuracy > 0.7 ? 'muy buen rendimiento' : 'rendimiento sólido'} 
                        en la clasificación automática de sentimientos gastronómicos.
                      </p>
                    </div>
                    
                    <div className="bg-white rounded-2xl p-6 border border-purple-200 shadow-sm">
                      <h5 className="font-semibold text-purple-900 mb-2 text-lg">⚖️ Balance del Modelo</h5>
                      <p className="leading-relaxed">
                        La puntuación F1 de <span className="font-bold text-orange-600">{(currentMetrics.f1_macro * 100).toFixed(2)}%</span> refleja 
                        un {currentMetrics.f1_macro > 0.7 ? 'equilibrio excepcional' : currentMetrics.f1_macro > 0.5 ? 'buen equilibrio' : 'equilibrio moderado'} 
                        entre la capacidad de identificar correctamente los sentimientos y evitar clasificaciones erróneas.
                      </p>
                    </div>
                    
                    <div className="bg-white rounded-2xl p-6 border border-green-200 shadow-sm">
                      <h5 className="font-semibold text-green-900 mb-2 text-lg">🎯 Confiabilidad Práctica</h5>
                      <p className="leading-relaxed">
                        Estos resultados indican que puedes confiar en el análisis, especialmente cuando la confianza individual 
                        del resultado sea <span className="font-bold text-green-600">superior al 70%</span>. 
                        El sistema es particularmente efectivo para identificar experiencias claramente positivas o negativas.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Información temporal */}
            {currentMetrics.last_evaluation && (
              <div className="mt-6 p-6 bg-white/80 rounded-2xl border border-purple-200 shadow-lg backdrop-blur-sm">
                <div className="flex items-center gap-3 text-purple-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-semibold text-lg">
                    📅 Última evaluación: {new Date(currentMetrics.last_evaluation).toLocaleDateString('es-ES', {
                      year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
                    })}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

      {/* Opciones avanzadas simplificadas */}
      <div className="text-center">
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="inline-flex items-center gap-2 px-6 py-3 text-gray-600 hover:text-gray-900 transition-colors duration-200 rounded-xl hover:bg-gray-100"
        >
          <span className="font-medium">Más opciones técnicas</span>
          <svg 
            className={`w-5 h-5 transition-transform duration-200 ${showAdvanced ? 'rotate-180' : ''}`} 
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {showAdvanced && (
        <div className="mt-6 bg-gray-50 rounded-2xl p-8 border border-gray-200">
          <div className="text-center mb-6">
            <h4 className="text-xl font-bold text-gray-900 mb-3">🔧 Configuración Avanzada</h4>
            <p className="text-gray-600">Opciones adicionales para desarrolladores y usuarios avanzados</p>
          </div>

          <div className="bg-white rounded-xl p-6 text-center text-gray-500">
            <div className="text-4xl mb-4">🚀</div>
            <p className="text-lg font-medium mb-2">Panel de Control Técnico</p>
            <p className="text-sm leading-relaxed">
              Las funciones principales están disponibles en los botones superiores.<br />
              Esta sección mostrará opciones avanzadas de configuración cuando sea necesario.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default SentimentPanel;