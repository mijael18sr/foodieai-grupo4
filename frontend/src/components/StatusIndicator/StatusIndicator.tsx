import { useState, useEffect } from 'react';
import { checkBackendHealth } from '../../utils';

interface StatusIndicatorProps {
  className?: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ className = '' }) => {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [lastCheck, setLastCheck] = useState<Date>(new Date());

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const health = await checkBackendHealth();
        setIsOnline(health);
        setLastCheck(new Date());
      } catch {
        setIsOnline(false);
        setLastCheck(new Date());
      }
    };

    // Verificar inmediatamente
    checkStatus();

    // Verificar cada 30 segundos
    const interval = setInterval(checkStatus, 30000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    if (isOnline === null) return 'bg-gray-400'; // Checking
    return isOnline ? 'bg-green-500' : 'bg-red-500';
  };

  const getStatusText = () => {
    if (isOnline === null) return 'Verificando...';
    return isOnline ? 'Backend Online' : 'Backend Offline';
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className={`w-2 h-2 rounded-full ${getStatusColor()} animate-pulse`}></div>
      <span className="text-xs text-gray-600">
        {getStatusText()}
      </span>
      {isOnline !== null && (
        <span className="text-xs text-gray-400">
          · {lastCheck.toLocaleTimeString()}
        </span>
      )}
    </div>
  );
};