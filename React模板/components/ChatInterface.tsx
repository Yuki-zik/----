import React, { useState, useEffect, useRef } from 'react';
import { sendMessageToGemini } from '../services/geminiService';
import { ChatMessage } from '../types';

interface ChatInterfaceProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ isOpen, onClose }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'model', text: 'SYNAPSE LINK ESTABLISHED. WAITING FOR INPUT.' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setIsLoading(true);

    try {
        // Construct history for the API
        const history = messages.map(m => ({
            role: m.role,
            parts: [{ text: m.text }]
        }));

      const response = await sendMessageToGemini(userMsg, history);
      setMessages(prev => [...prev, { role: 'model', text: response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'model', text: 'ERROR: SIGNAL INTERRUPTED.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="absolute top-0 right-0 h-full w-full md:w-96 bg-black/90 backdrop-blur-md border-l border-cyan-500/30 flex flex-col z-50 animate-in slide-in-from-right duration-300">
      {/* Header */}
      <div className="p-4 border-b border-cyan-500/30 flex justify-between items-center bg-cyan-950/20">
        <div className="flex items-center gap-2">
            <span className="material-icons text-cyan-400">network_intelligence</span>
            <h2 className="text-cyan-400 font-bold tracking-widest text-sm">SYNAPSE AI CORE</h2>
        </div>
        <button onClick={onClose} className="text-cyan-600 hover:text-cyan-400 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-xs md:text-sm">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 border ${
              msg.role === 'user' 
                ? 'border-cyan-500/50 bg-cyan-900/20 text-cyan-100 rounded-tl-lg rounded-br-lg rounded-bl-lg' 
                : 'border-slate-600 bg-slate-800/50 text-slate-300 rounded-tr-lg rounded-br-lg rounded-bl-lg'
            }`}>
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
             <div className="max-w-[80%] p-3 border border-slate-600 bg-slate-800/50 text-cyan-400 animate-pulse">
              <p>PROCESSING [THINKING MODE ACTIVE]...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-cyan-500/30 bg-black">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="ENTER COMMAND..."
            className="flex-1 bg-slate-900/80 border border-slate-700 text-cyan-100 px-3 py-2 text-sm focus:outline-none focus:border-cyan-500 transition-colors font-mono"
            disabled={isLoading}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className="px-4 py-2 bg-cyan-700 hover:bg-cyan-600 text-white font-bold text-xs tracking-wider transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            SEND
          </button>
        </div>
      </div>
    </div>
  );
};