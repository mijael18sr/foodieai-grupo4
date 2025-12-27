import { Component, type ReactNode } from 'react';
import { isExtensionError } from '../../utils/errorHandler';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: unknown): State {
    // Ignorar errores de extensiones del navegador
    if (isExtensionError(error)) {
      console.debug('[ErrorBoundary] Ignorando error de extensión del navegador');
      return { hasError: false };
    }
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Si es error de extensión, no hacer nada
    if (isExtensionError(error)) {
      console.debug('[ErrorBoundary] Error de extensión capturado y ignorado:', error.message);
      // Resetear el estado a sin error
      this.setState({ hasError: false });
      return;
    }
    
    // Solo logear errores reales
    console.error('[ErrorBoundary] Error real capturado:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Algo salió mal</h2>
            <p className="text-gray-600 mb-4">Ha ocurrido un error inesperado.</p>
            <button
              onClick={() => globalThis.location.reload()}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Recargar página
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;