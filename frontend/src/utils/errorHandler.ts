// Patrones de errores causados por extensiones del navegador (Grammarly, Quillbot, etc.)
const EXTENSION_PATTERNS = [
  'insertBefore',
  'removeChild',
  'appendChild',
  'NotFoundError',
  'content.js',
  'hook.js',
  'extension',
  'grammarly',
  'quillbot',
  'message port closed',
  'Cannot read properties of null',
  'not a child of this node',
  'Node was not found',
  'DOMException'
];

export const isExtensionError = (error: unknown): boolean => {
  if (!error) return false;
  
  // Convertir a string de forma segura
  let errorText = '';
  
  if (error instanceof Error) {
    errorText = `${error.name} ${error.message} ${error.stack || ''}`;
  } else if (typeof error === 'string') {
    errorText = error;
  } else if (typeof error === 'object') {
    try {
      errorText = JSON.stringify(error);
    } catch {
      errorText = String(error);
    }
  }
  
  const lowerText = errorText.toLowerCase();
  return EXTENSION_PATTERNS.some(pattern => lowerText.includes(pattern.toLowerCase()));
};

// Parchear métodos del DOM para ignorar errores de extensiones
const patchDOMMethods = (): void => {
  const originalInsertBefore = Node.prototype.insertBefore;
  const originalRemoveChild = Node.prototype.removeChild;
  const originalAppendChild = Node.prototype.appendChild;

  Node.prototype.insertBefore = function<T extends Node>(newNode: T, referenceNode: Node | null): T {
    try {
      return originalInsertBefore.call(this, newNode, referenceNode) as T;
    } catch (e) {
      if (isExtensionError(e)) {
        console.debug('[DOM Patch] Ignorando error insertBefore de extensión');
        return newNode;
      }
      throw e;
    }
  };

  Node.prototype.removeChild = function<T extends Node>(child: T): T {
    try {
      return originalRemoveChild.call(this, child) as T;
    } catch (e) {
      if (isExtensionError(e)) {
        console.debug('[DOM Patch] Ignorando error removeChild de extensión');
        return child;
      }
      throw e;
    }
  };

  Node.prototype.appendChild = function<T extends Node>(node: T): T {
    try {
      return originalAppendChild.call(this, node) as T;
    } catch (e) {
      if (isExtensionError(e)) {
        console.debug('[DOM Patch] Ignorando error appendChild de extensión');
        return node;
      }
      throw e;
    }
  };
};

export const setupGlobalErrorHandlers = (): void => {
  // Parchear métodos del DOM primero
  patchDOMMethods();
  
  // Capturar errores síncronos
  window.addEventListener('error', (e) => {
    if (isExtensionError(e.error) || isExtensionError(e.message)) {
      e.preventDefault();
      e.stopPropagation();
      console.debug('[ErrorHandler] Ignorando error de extensión:', e.message);
      return false;
    }
  }, true);

  // Capturar promesas rechazadas
  window.addEventListener('unhandledrejection', (e) => {
    if (isExtensionError(e.reason)) {
      e.preventDefault();
      console.debug('[ErrorHandler] Ignorando promesa rechazada de extensión');
      return false;
    }
  }, true);
};

