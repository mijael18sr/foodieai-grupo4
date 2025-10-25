import { useState, useCallback } from 'react';
import BayesApiService from '../../services/bayesService';
import type { SentimentAnalysisResponse, ModelInfo, ModelMetrics } from '../../types/api';

export function SentimentPanel() {
  const [comment, setComment] = useState('');
  const [result, setResult] = useState<SentimentAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [modelMetrics, setModelMetrics] = useState<ModelMetrics | null>(null);

  const extractErrorMessage = (err: unknown) => {
    // Try to extract axios-style error message safely without using `any`
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
    // Ejecutar análisis al presionar Enter (pero no Shift+Enter para permitir saltos de línea)
    if (e.key === 'Enter' && !e.shiftKey && comment.trim() && !loading) {
      e.preventDefault(); // Prevenir el salto de línea
      handleAnalyze();
    }
  }, [comment, loading, handleAnalyze]);

  const handleClearComment = useCallback(() => {
    setComment('');
    setResult(null);
    setError(null);
    setSuccessMessage('✅ Comentario y resultados limpiados');
    setTimeout(() => setSuccessMessage(null), 3000);
  }, []);

  const handleClearAll = useCallback(() => {
    setComment('');
    setResult(null);
    setError(null);
    setModelInfo(null);
    setModelMetrics(null);
    setSuccessMessage('✅ Todo limpiado - Panel reiniciado');
    setTimeout(() => setSuccessMessage(null), 3000);
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
    <div className="bg-white/80 backdrop-blur-xl rounded-3xl p-4 sm:p-6 lg:p-8 shadow-2xl border border-gray-200/50">
      <div className="text-center mb-4 sm:mb-6">
        <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center mb-3 mx-auto shadow-lg">
          <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h4 className="text-lg sm:text-xl font-bold text-gray-900 mb-1">Análisis de Sentimientos</h4>
        <p className="text-xs sm:text-sm text-gray-600">Descubre el sentimiento de comentarios y reseñas</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
        {/* Sección de análisis de comentarios */}
        <div className="space-y-4 sm:space-y-6">
          <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl p-4 sm:p-6 border border-blue-200">
            <div className="flex items-center gap-2 sm:gap-3 mb-4">
              <div className="w-6 h-6 sm:w-8 sm:h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
              <label htmlFor="sentiment-comment" className="text-base sm:text-lg font-semibold text-blue-900">
                Análisis de Comentario
              </label>
            </div>
            
            <textarea
              id="sentiment-comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={4}
              className="w-full p-3 sm:p-4 rounded-xl border-2 border-blue-200 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-blue-200 focus:border-blue-400 transition-all duration-200 resize-none shadow-sm hover:border-blue-300 text-sm sm:text-base"
              placeholder="Escribe un comentario para analizar su sentimiento...&#10;&#10;Ejemplos:&#10;• &quot;La comida estuvo deliciosa y el servicio excelente&quot;&#10;• &quot;Muy mala experiencia, la comida llegó fría&quot;&#10;• &quot;Normal, nada especial pero aceptable&quot;&#10;&#10;💡 Presiona Enter para analizar o Shift+Enter para nueva línea"
            />

            <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 mt-4">
              <button
                onClick={handleAnalyze}
                disabled={loading || !comment.trim()}
                className="flex-1 px-4 sm:px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-sm sm:text-base"
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span className="hidden sm:inline">Analizando...</span>
                    <span className="sm:hidden">Analizando...</span>
                  </div>
                ) : result ? (
                  <div className="flex items-center justify-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span className="hidden sm:inline">Analizar Nuevo</span>
                    <span className="sm:hidden">Nuevo</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span className="hidden sm:inline">Analizar Sentimiento</span>
                    <span className="sm:hidden">Analizar</span>
                  </div>
                )}
              </button>
              
              <button
                onClick={handleClearComment}
                disabled={!comment.trim() && !result}
                className="px-3 sm:px-4 py-3 bg-red-100 hover:bg-red-200 disabled:bg-gray-100 disabled:text-gray-400 text-red-700 rounded-xl transition-all duration-200 font-medium"
                title="Limpiar comentario y resultados"
              >
                <svg className="w-5 h-5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
              
              <button
                onClick={handleGetModelInfo}
                className="px-3 sm:px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl transition-all duration-200 font-medium"
                title="Ver información del modelo"
              >
                <svg className="w-5 h-5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </button>

              <button
                onClick={handleGetModelMetrics}
                className="px-3 sm:px-4 py-3 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded-xl transition-all duration-200 font-medium"
                title="Ver métricas del modelo IA"
              >
                <svg className="w-5 h-5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </button>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl">
                <div className="flex items-center gap-2 text-red-700">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-medium text-sm">{error}</span>
                </div>
              </div>
            )}

            {successMessage && (
              <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-xl">
                <div className="flex items-center gap-2 text-green-700">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-medium text-sm">{successMessage}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Sección de resultados */}
        <div className="space-y-4 sm:space-y-6">
          <div className="bg-gradient-to-br from-purple-50 to-pink-100 rounded-2xl p-4 sm:p-6 border border-purple-200">
            <div className="flex items-center gap-2 sm:gap-3 mb-4">
              <div className="w-6 h-6 sm:w-8 sm:h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h5 className="text-base sm:text-lg font-semibold text-purple-900">Resultado del Análisis</h5>
            </div>
            
            {!result ? (
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4 mx-auto">
                  <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <p className="text-purple-600 font-medium">Escribe un comentario y analízalo</p>
                <p className="text-purple-500 text-sm mt-2">Los resultados aparecerán aquí</p>
              </div>
            ) : (
              <div className="space-y-4">
                {/* Sentimiento principal */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-purple-100">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm font-medium text-gray-600">Sentimiento Detectado</span>
                    <div className={`px-4 py-2 rounded-full text-lg font-bold ${
                      result.sentiment === 'positivo' ? 'bg-green-100 text-green-700' :
                      result.sentiment === 'negativo' ? 'bg-red-100 text-red-700' :
                      'bg-yellow-100 text-yellow-700'
                    }`}>
                      {result.sentiment === 'positivo' ? '😊 Positivo' :
                       result.sentiment === 'negativo' ? '😞 Negativo' :
                       '😐 Neutro'}
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex items-center justify-between text-sm mb-2">
                      <span className="text-gray-600">Confianza</span>
                      <span className="font-bold text-gray-900">{(result.confidence*100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full transition-all duration-500 ${
                          result.confidence > 0.8 ? 'bg-green-500' :
                          result.confidence > 0.6 ? 'bg-yellow-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${result.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* Probabilidades */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-purple-100">
                  <h6 className="text-sm font-medium text-gray-600 mb-3">Distribución de Probabilidades</h6>
                  <div className="space-y-3">
                    {Object.entries(result.probabilities).map(([sentiment, probability]) => (
                      <div key={sentiment} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="text-sm">
                            {sentiment === 'positivo' ? '😊' :
                             sentiment === 'negativo' ? '😞' : '😐'}
                          </span>
                          <span className="text-sm font-medium capitalize text-gray-700">{sentiment}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full transition-all duration-500 ${
                                sentiment === 'positivo' ? 'bg-green-500' :
                                sentiment === 'negativo' ? 'bg-red-500' :
                                'bg-yellow-500'
                              }`}
                              style={{ width: `${probability * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-mono w-12 text-right">{(probability*100).toFixed(1)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Texto procesado */}
                {result.processed_text && (
                  <div className="bg-white rounded-xl p-4 shadow-sm border border-purple-100">
                    <h6 className="text-xs font-medium text-gray-500 mb-2">Texto Procesado (para análisis)</h6>
                    <code className="text-xs text-gray-600 font-mono break-all">{result.processed_text}</code>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Información del modelo */}
      {modelInfo && (
        <div className="mt-8 p-6 bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-500 mb-1">Modelo de Inteligencia Artificial</div>
              <div className="font-bold text-gray-900 text-lg">
                {modelInfo.model_name} 
                <span className={`ml-3 px-3 py-1 rounded-full text-xs ${
                  modelInfo.is_trained ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                }`}>
                  {modelInfo.is_trained ? '✅ Entrenado' : '❌ No entrenado'}
                </span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500 mb-1">Clases de Sentimiento</div>
              <div className="text-sm text-gray-700 font-medium">{modelInfo.classes.join(' • ')}</div>
            </div>
          </div>
        </div>
      )}

      {/* Métricas del modelo */}
      {modelMetrics && (
        <div className="mt-6 sm:mt-8 p-4 sm:p-6 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl border border-purple-200">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-4 sm:mb-6">
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-purple-600 rounded-xl flex items-center justify-center">
              <svg className="w-4 h-4 sm:w-5 sm:h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h4 className="text-lg sm:text-xl font-bold text-purple-900">Métricas de Rendimiento del Modelo IA</h4>
              <p className="text-purple-600 text-xs sm:text-sm">Indicadores de calidad y precisión del algoritmo Bayesiano</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {/* Métricas principales */}
            <div className="bg-white rounded-xl p-4 sm:p-5 shadow-sm border border-purple-100">
              <div className="flex items-center justify-between mb-3">
                <h5 className="font-semibold text-gray-900 text-sm sm:text-base">Precisión General</h5>
                <span className="text-xl sm:text-2xl">🎯</span>
              </div>
              <div className="text-2xl sm:text-3xl font-bold text-purple-600 mb-1">
                {(modelMetrics.accuracy * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600">Porcentaje de clasificaciones correctas</p>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div 
                  className="bg-purple-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${modelMetrics.accuracy * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
              <div className="flex items-center justify-between mb-3">
                <h5 className="font-semibold text-gray-900">Precisión Macro</h5>
                <span className="text-2xl">⚖️</span>
              </div>
              <div className="text-3xl font-bold text-blue-600 mb-1">
                {(modelMetrics.precision_macro * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600">Precisión promedio entre clases</p>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${modelMetrics.precision_macro * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
              <div className="flex items-center justify-between mb-3">
                <h5 className="font-semibold text-gray-900">Recall Macro</h5>
                <span className="text-2xl">🔍</span>
              </div>
              <div className="text-3xl font-bold text-green-600 mb-1">
                {(modelMetrics.recall_macro * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600">Capacidad de encontrar casos positivos</p>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div 
                  className="bg-green-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${modelMetrics.recall_macro * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
              <div className="flex items-center justify-between mb-3">
                <h5 className="font-semibold text-gray-900">F1-Score Macro</h5>
                <span className="text-2xl">🎲</span>
              </div>
              <div className="text-3xl font-bold text-orange-600 mb-1">
                {(modelMetrics.f1_macro * 100).toFixed(1)}%
              </div>
              <p className="text-sm text-gray-600">Media armónica entre precisión y recall</p>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div 
                  className="bg-orange-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${modelMetrics.f1_macro * 100}%` }}
                ></div>
              </div>
            </div>

            {modelMetrics.cohen_kappa && (
              <div className="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
                <div className="flex items-center justify-between mb-3">
                  <h5 className="font-semibold text-gray-900">Cohen's Kappa</h5>
                  <span className="text-2xl">🤝</span>
                </div>
                <div className="text-3xl font-bold text-indigo-600 mb-1">
                  {modelMetrics.cohen_kappa.toFixed(3)}
                </div>
                <p className="text-sm text-gray-600">Concordancia entre observadores</p>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                  <div 
                    className="bg-indigo-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${Math.max(0, modelMetrics.cohen_kappa * 100)}%` }}
                  ></div>
                </div>
              </div>
            )}

            {modelMetrics.matthews_corrcoef && (
              <div className="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
                <div className="flex items-center justify-between mb-3">
                  <h5 className="font-semibold text-gray-900">Matthews Correlation</h5>
                  <span className="text-2xl">📊</span>
                </div>
                <div className="text-3xl font-bold text-teal-600 mb-1">
                  {modelMetrics.matthews_corrcoef.toFixed(3)}
                </div>
                <p className="text-sm text-gray-600">Coeficiente de correlación de Matthews</p>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                  <div 
                    className="bg-teal-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${Math.max(0, modelMetrics.matthews_corrcoef * 100)}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>

          {modelMetrics.last_evaluation && (
            <div className="mt-6 p-4 bg-purple-100 rounded-xl">
              <div className="flex items-center gap-2 text-purple-700">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm font-medium">
                  Última evaluación: {new Date(modelMetrics.last_evaluation).toLocaleDateString('es-ES', {
                    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
                  })}
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SentimentPanel;
