import { useState, useRef, useEffect, memo } from 'react';
import './AIChat.css';

interface Message {
  id: string;
  text: string;
  isAI: boolean;
  timestamp: Date;
}

interface AIChatProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const AIChat = memo(function AIChat({ isOpen, onToggle }: AIChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '¡Hola! 👋 Soy tu asistente gastronómico con IA. Estoy aquí para ayudarte a encontrar el restaurante perfecto según tu estado de ánimo y preferencias. ¿Cómo te sientes hoy?',
      isAI: true,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateAIResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    // Respuestas sentimentales y gastronómicas
    if (lowerMessage.includes('triste') || lowerMessage.includes('sad') || lowerMessage.includes('deprimido')) {
      return '😔 Entiendo que te sientes triste. ¿Qué tal si buscamos un lugar acogedor con comida reconfortante? Te recomiendo probar algunos restaurantes con ambiente cálido y platos que alegran el corazón. ¿Prefieres comida casera peruana o algo internacional?';
    }
    
    if (lowerMessage.includes('feliz') || lowerMessage.includes('happy') || lowerMessage.includes('alegre') || lowerMessage.includes('contento')) {
      return '😊 ¡Qué bueno que estés feliz! Es el momento perfecto para probar algo nuevo y emocionante. ¿Te animas a descubrir una nueva cocina? Podríamos buscar restaurantes con ambientes vibrantes y platos innovadores.';
    }
    
    if (lowerMessage.includes('estresado') || lowerMessage.includes('cansado') || lowerMessage.includes('agotado')) {
      return '😌 Parece que necesitas relajarte. Te sugiero buscar restaurantes con ambientes tranquilos y serenos. ¿Qué te parece un lugar con vista al mar o un jardín? La comida fresca y saludable también puede ayudarte a sentirte mejor.';
    }
    
    if (lowerMessage.includes('romantic') || lowerMessage.includes('cita') || lowerMessage.includes('pareja') || lowerMessage.includes('romántico')) {
      return '💕 ¡Perfecto para una cita romántica! Busquemos restaurantes con ambiente íntimo, iluminación suave y excelente comida. ¿Prefieres cocina italiana, francesa, o algo más exótico? También podemos filtrar por lugares con vista panorámica.';
    }
    
    if (lowerMessage.includes('celebr') || lowerMessage.includes('cumpleaños') || lowerMessage.includes('fiesta')) {
      return '🎉 ¡Es hora de celebrar! Busquemos lugares con ambiente festivo y excelente servicio. ¿Qué tipo de celebración es? Podemos encontrar restaurantes con espacios privados, música en vivo, o terrazas con vista espectacular.';
    }
    
    if (lowerMessage.includes('trabajo') || lowerMessage.includes('negocio') || lowerMessage.includes('cliente')) {
      return '💼 Para reuniones de trabajo necesitas lugares profesionales pero cómodos. Te ayudo a encontrar restaurantes con ambientes apropiados para negocios, buena acústica y servicio eficiente. ¿Prefieres algo más formal o casual?';
    }
    
    if (lowerMessage.includes('familia') || lowerMessage.includes('niños') || lowerMessage.includes('kids')) {
      return '👨‍👩‍👧‍👦 ¡Perfecto para salir en familia! Busquemos restaurantes family-friendly con menús para niños, espacios amplios y ambiente relajado. ¿Los niños tienen alguna preferencia especial de comida?';
    }
    
    if (lowerMessage.includes('comida') || lowerMessage.includes('hambre') || lowerMessage.includes('comer')) {
      return '🍽️ ¡Excelente! ¿Qué tipo de cocina te apetece hoy? Tenemos opciones de comida peruana, italiana, asiática, mexicana y mucho más. También puedo ayudarte según tu presupuesto y ubicación preferida.';
    }
    
    if (lowerMessage.includes('gracias') || lowerMessage.includes('thank')) {
      return '¡De nada! 😊 Estoy aquí para ayudarte a encontrar experiencias gastronómicas increíbles. ¿Hay algo más en lo que pueda asistirte? Recuerda que puedes usar el menú "Buscar Recomendaciones" para filtros más específicos.';
    }
    
    if (lowerMessage.includes('precio') || lowerMessage.includes('barato') || lowerMessage.includes('económico') || lowerMessage.includes('caro')) {
      return '💰 Entiendo que el presupuesto es importante. Puedo ayudarte a encontrar excelentes opciones en diferentes rangos de precio. ¿Prefieres opciones económicas, de rango medio, o estás dispuesto a invertir en una experiencia premium?';
    }
    
    // Respuesta por defecto
    const responses = [
      '🤔 Interesante... Cuéntame más sobre tus gustos. ¿Hay algún tipo de cocina que te llame la atención últimamente?',
      '✨ Me encanta conocer nuevas preferencias. ¿Prefieres ambientes tranquilos o más animados para comer?',
      '🍴 Basándome en tu mensaje, creo que podemos encontrar algo perfecto para ti. ¿Tienes alguna zona preferida de Lima?',
      '💡 ¡Excelente pregunta! Para darte la mejor recomendación, ¿podrías contarme un poco sobre tu estado de ánimo actual?'
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isAI: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Simular tiempo de respuesta de IA
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: generateAIResponse(inputText),
        isAI: true,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={onToggle}
          className="group bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-full p-4 shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-50"
          aria-label="Abrir chat de IA"
        >
          <div className="relative">
            <svg className="w-6 h-6 transition-transform duration-300 group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full"></div>
          </div>
          
          {/* Tooltip */}
          <div className="absolute bottom-full right-0 mb-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
            <div className="bg-gray-900 text-white text-sm rounded-lg px-3 py-2 whitespace-nowrap shadow-lg">
              💬 Conversa con IA Gastronómica
              <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
            </div>
          </div>
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 w-96 max-w-[90vw] h-[500px] max-h-[80vh]">
      <div className="flex flex-col h-full bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden animate-in slide-in-from-bottom-4 fade-in duration-300">
        {/* Header */}
        <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-base">Asistente IA</h3>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <p className="text-sm text-blue-200">En línea</p>
              </div>
            </div>
          </div>
          
          <button
            onClick={onToggle}
            className="text-white/80 hover:text-white hover:bg-white/10 p-2 rounded-full transition-all duration-200"
            aria-label="Minimizar chat"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isAI ? 'justify-start' : 'justify-end'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  message.isAI
                    ? 'bg-white text-gray-800 shadow-sm border border-gray-200'
                  : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md'
              }`}
            >
              {message.text}
              <div className={`text-xs mt-2 opacity-70 ${message.isAI ? 'text-gray-500' : 'text-blue-100'}`}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-200">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

        {/* Input */}
        <div className="p-4 bg-white border-t border-gray-200">
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Cuéntame cómo te sientes..."
              className="flex-1 border border-gray-300 rounded-full px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isTyping}
              className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-300 disabled:to-gray-400 text-white rounded-full p-3 transition-all duration-200 disabled:cursor-not-allowed flex-shrink-0 transform hover:scale-105"
            >
              <svg className="w-5 h-5 rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
});