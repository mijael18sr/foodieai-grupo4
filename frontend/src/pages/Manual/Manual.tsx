import { memo, useState } from 'react';

type TabType = 'pdf' | 'video';

// URL del video en S3
const VIDEO_URL = 'https://foodieai-assets.s3.us-east-2.amazonaws.com/videos/FoodieAI-Tutorial.mp4';

export const Manual = memo(function Manual() {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [activeTab, setActiveTab] = useState<TabType>('pdf');

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = '/manual-usuario.pdf';
    link.download = 'FoodieAI-Manual-Usuario.pdf';
    link.click();
  };

  const handleOpenNewTab = () => {
    if (activeTab === 'pdf') {
      window.open('/manual-usuario.pdf', '_blank');
    } else {
      window.open(VIDEO_URL, '_blank');
    }
  };

  return (
    <div className="min-h-full bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center shadow-lg">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
                  Guía de Usuario
                </h1>
                <p className="text-gray-500 text-sm sm:text-base mt-1">
                  Manual completo y video tutorial de FoodieAI
                </p>
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="flex items-center gap-2 px-4 py-2.5 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors font-medium"
                title={isFullscreen ? 'Salir de pantalla completa' : 'Pantalla completa'}
              >
                {isFullscreen ? (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 9V4.5M9 9H4.5M9 9L3.75 3.75M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 9h4.5M15 9V4.5M15 9l5.25-5.25M15 15h4.5M15 15v4.5m0-4.5l5.25 5.25" />
                    </svg>
                    <span className="hidden sm:inline">Reducir</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15" />
                    </svg>
                    <span className="hidden sm:inline">Expandir</span>
                  </>
                )}
              </button>
              
              <button
                onClick={handleOpenNewTab}
                className="flex items-center gap-2 px-4 py-2.5 bg-blue-100 text-blue-700 rounded-xl hover:bg-blue-200 transition-colors font-medium"
                title="Abrir en nueva pestaña"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                <span className="hidden sm:inline">Nueva pestaña</span>
              </button>
              
              {activeTab === 'pdf' && (
                <button
                  onClick={handleDownload}
                  className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-md hover:shadow-lg font-medium"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  <span>Descargar PDF</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      {!isFullscreen && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-1.5 inline-flex gap-1">
            <button
              onClick={() => setActiveTab('pdf')}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
                activeTab === 'pdf'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Manual PDF
            </button>
            <button
              onClick={() => setActiveTab('video')}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${
                activeTab === 'video'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-md'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Video Tutorial
            </button>
          </div>
        </div>
      )}

      {/* Quick Navigation Cards - Solo mostrar en PDF */}
      {!isFullscreen && activeTab === 'pdf' && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-3">
                <span className="text-xl">🚀</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Inicio Rápido</h3>
              <p className="text-xs text-gray-500 mt-1">Aprende lo básico</p>
            </div>
            
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3">
                <span className="text-xl">🔍</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Buscar</h3>
              <p className="text-xs text-gray-500 mt-1">Encuentra restaurantes</p>
            </div>
            
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-3">
                <span className="text-xl">🤖</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">IA & ML</h3>
              <p className="text-xs text-gray-500 mt-1">Análisis inteligente</p>
            </div>
            
            <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center mb-3">
                <span className="text-xl">⭐</span>
              </div>
              <h3 className="font-semibold text-gray-900 text-sm">Tips</h3>
              <p className="text-xs text-gray-500 mt-1">Mejores prácticas</p>
            </div>
          </div>
        </div>
      )}

      {/* Video Info Cards */}
      {!isFullscreen && activeTab === 'video' && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-100">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Video Tutorial Completo</h2>
                <p className="text-gray-600 mt-1">
                  Aprende a usar FoodieAI paso a paso con nuestra guía visual interactiva
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Content Viewer */}
      <div className={`${isFullscreen ? 'fixed inset-0 z-50 bg-white' : 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8'}`}>
        <div className={`bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden ${isFullscreen ? 'h-full rounded-none' : ''}`}>
          {/* Toolbar */}
          <div className={`px-4 py-3 flex items-center justify-between ${activeTab === 'video' ? 'bg-gradient-to-r from-purple-800 to-pink-800' : 'bg-gray-800'}`}>
            <div className="flex items-center gap-3">
              {activeTab === 'pdf' ? (
                <div className="flex items-center gap-2 text-white">
                  <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8.5 13a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1H9a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1H9a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1H9a.5.5 0 0 1-.5-.5z"/>
                  </svg>
                  <span className="font-medium text-sm">FoodieAI-Manual-Usuario.pdf</span>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-white">
                  <svg className="w-5 h-5 text-pink-400" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                  <span className="font-medium text-sm">FoodieAI - La Guía con IA</span>
                </div>
              )}
            </div>
            
            {isFullscreen && (
              <button
                onClick={() => setIsFullscreen(false)}
                className="text-white hover:text-gray-300 transition-colors p-1"
                title="Cerrar pantalla completa"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          
          {/* Content */}
          <div className={`${isFullscreen ? 'h-[calc(100%-52px)]' : 'h-[70vh] min-h-[500px]'}`}>
            {activeTab === 'pdf' ? (
              <iframe
                src="/manual-usuario.pdf#toolbar=1&navpanes=1&scrollbar=1&view=FitH"
                className="w-full h-full border-0"
                title="Manual de Usuario - FoodieAI"
              />
            ) : (
              <div className="w-full h-full bg-black flex items-center justify-center">
                <video
                  className="w-full h-full"
                  controls
                  controlsList="nodownload"
                  poster=""
                >
                  <source src={VIDEO_URL} type="video/mp4" />
                  Tu navegador no soporta el elemento de video.
                </video>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Help Section */}
      {!isFullscreen && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-6 sm:p-8 text-white">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold">¿Necesitas más ayuda?</h3>
                  <p className="text-blue-100 text-sm mt-1">
                    Si tienes preguntas adicionales, no dudes en contactarnos o revisar nuestra sección de preguntas frecuentes.
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <a
                  href="mailto:soporte@foodieai.com"
                  className="px-5 py-2.5 bg-white text-blue-700 rounded-xl font-medium hover:bg-blue-50 transition-colors"
                >
                  Contactar Soporte
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

export default Manual;
