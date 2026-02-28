import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const App = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'שלום! אני עוזר ה-Todo החכם שלך. איך אני יכול לעזור היום?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessages(prev => [...prev, { role: 'bot', content: data.response }]);
      } else {
        setMessages(prev => [...prev, { role: 'bot', content: "**אופס!** הייתה שגיאה בשרת." }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "**שגיאת תקשורת.** וודא שהשרת רץ." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([{ role: 'bot', content: 'הצ\'אט נוקה. איך אפשר לעזור?' }]);
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 text-right font-sans" dir="rtl">
      {/* Header */}
      <header className="bg-white shadow-sm px-6 py-4 flex items-center justify-between border-b sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-2 rounded-xl shadow-indigo-200 shadow-lg">
            <Bot size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800">Todo AI Assistant</h1>
            <p className="text-xs text-green-500 font-medium">מחובר למערכת</p>
          </div>
        </div>
        <button
          onClick={clearChat}
          className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
          title="נקה צ'אט"
        >
          <Trash2 size={20} />
        </button>
      </header>

      {/* Chat Window */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-start' : 'justify-end'}`}>
              <div className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'flex-row' : 'flex-row-reverse'}`}>
                <div className={`mt-1 shrink-0 p-1.5 rounded-full h-9 w-9 flex items-center justify-center shadow-sm ${
                  msg.role === 'user' ? 'bg-indigo-100 text-indigo-600' : 'bg-emerald-100 text-emerald-600'
                }`}>
                  {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className={`p-4 rounded-2xl shadow-sm border ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white border-indigo-500 rounded-tr-none'
                    : 'bg-white text-slate-800 border-slate-200 rounded-tl-none'
                }`}>
                  <div className="prose prose-sm max-w-none">
                    <div className={`p-4 rounded-2xl shadow-sm border ${
                        msg.role === 'user'
                            ? 'bg-indigo-600 text-white border-indigo-500 rounded-tr-none'
                            : 'bg-white text-slate-800 border-slate-200 rounded-tl-none'
                        }`}>
                      {/* החלפה של ה-Markdown הבעייתי בטקסט רגיל ומעוצב */}
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {msg.content}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-end pr-12">
              <div className="bg-slate-200/50 px-4 py-2 rounded-full flex items-center gap-2 text-slate-500 text-xs">
                <Loader2 size={14} className="animate-spin" />
                הבוט מעבד נתונים...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="p-4 bg-white border-t">
        <form onSubmit={handleSendMessage} className="max-w-3xl mx-auto flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="איזו משימה להוסיף?"
            className="flex-1 p-4 border border-slate-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50 transition-all text-slate-800 shadow-inner"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-indigo-600 text-white p-4 rounded-2xl hover:bg-indigo-700 disabled:opacity-50 shadow-indigo-200 shadow-lg transition-all active:scale-95"
          >
            {isLoading ? <Loader2 className="animate-spin" /> : <Send size={22} />}
          </button>
        </form>
      </footer>
    </div>
  );
};

export default App;