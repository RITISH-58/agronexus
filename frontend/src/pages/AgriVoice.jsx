import React, { useState, useEffect } from 'react';
import { Phone, PhoneOff, PhoneIncoming, Mic, Volume2, Globe, MessageSquare, Sparkles, ArrowRight, WifiOff, ChevronLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';


const API_BASE = import.meta.env.VITE_API_URL || `${API_BASE_URL}`;

/* Waveform */
const VoiceWaveform = ({ active }) => {
  const [, setTick] = useState(0);
  useEffect(() => {
    if (!active) return;
    const i = setInterval(() => setTick(t => t + 1), 200);
    return () => clearInterval(i);
  }, [active]);

  return (
    <div className="flex items-end justify-center gap-[3px] h-16">
      {[...Array(24)].map((_, i) => (
        <div key={i}
          className={`w-1 rounded-full transition-all duration-150 ${active ? 'bg-gradient-to-t from-leaf-500 to-olive-400' : 'bg-cream-400'}`}
          style={{ height: active ? `${15 + Math.random() * 85}%` : '15%' }}
        />
      ))}
    </div>
  );
};

/* Typing effect */
const useTypingEffect = (text, speed = 25) => {
  const [displayed, setDisplayed] = useState('');
  useEffect(() => {
    if (!text) { setDisplayed(''); return; }
    setDisplayed(''); let i = 0;
    const timer = setInterval(() => { setDisplayed(text.slice(0, i + 1)); i++; if (i >= text.length) clearInterval(timer); }, speed);
    return () => clearInterval(timer);
  }, [text, speed]);
  return displayed;
};

const AgriVoice = () => {
  const [language, setLanguage] = useState('en');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [callState, setCallState] = useState('idle');
  const [transcript, setTranscript] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [callHistory, setCallHistory] = useState([]);
  const [textQuery, setTextQuery] = useState('');
  const [error, setError] = useState('');
  const typedResponse = useTypingEffect(aiResponse);

  const initiateCall = async () => {
    if (!phoneNumber || phoneNumber.length < 10) { setError('Enter valid phone (+91XXXXXXXXXX)'); return; }
    setError(''); setCallState('ringing'); setAiResponse(''); setTranscript('');
    try {
      const res = await fetch(`${API_BASE}/voice/api-call`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: phoneNumber, language }),
      });
      const data = await res.json();
      if (data.success) { setCallState('connected'); setTranscript('Call initiated! Your phone will ring shortly...'); }
      else { setError(data.error || 'Failed'); setCallState('idle'); }
    } catch { setError('Server connection failed'); setCallState('idle'); }
  };

  const sendTextQuery = async () => {
    if (!textQuery.trim()) return;
    setError(''); setCallState('processing'); setTranscript(textQuery); setAiResponse('');
    try {
      const res = await fetch(`${API_BASE}/voice/api-query`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: textQuery, language }),
      });
      const data = await res.json();
      setCallState('responding'); await new Promise(r => setTimeout(r, 600));
      if (data.success) {
        setAiResponse(data.response);
        setCallHistory(prev => [{ id: Date.now(), query: textQuery, response: data.response, lang: language, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 10));
      } else { setAiResponse(data.error || 'Failed'); }
      setCallState('ended');
    } catch { setError('Server connection failed'); setCallState('idle'); }
  };

  return (
    <div className="min-h-screen px-4 pt-6 pb-4 max-w-lg mx-auto space-y-5 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link to="/" className="w-10 h-10 bg-white rounded-2xl shadow-card flex items-center justify-center active:scale-90 transition-transform">
          <ChevronLeft size={20} className="text-dark" />
        </Link>
        <div>
          <h1 className="text-xl font-extrabold text-dark tracking-tight">Buyers</h1>
          <p className="text-xs text-muted">Farm To Fork</p>
        </div>
      </div>

      {/* Language Toggle */}
      <div className="flex gap-2 bg-cream-200/60 p-1 rounded-2xl">
        {[{ code: 'en', label: '🇬🇧 English' }, { code: 'te', label: '🇮🇳 తెలుగు' }].map(l => (
          <button key={l.code} onClick={() => setLanguage(l.code)}
            className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition-all ${language === l.code ? 'bg-white text-leaf-700 shadow-card' : 'text-muted'}`}>
            {l.label}
          </button>
        ))}
      </div>

      {/* Big Mic Button */}
      <div className="flex flex-col items-center py-6 space-y-4">
        <div className="relative">
          <button
            onClick={() => callState === 'idle' ? initiateCall() : setCallState('idle')}
            className={`w-28 h-28 rounded-full flex items-center justify-center shadow-2xl transition-all duration-300 active:scale-90 ${
              callState !== 'idle'
                ? 'bg-red-500 hover:bg-red-600'
                : 'bg-gradient-to-br from-leaf-500 to-olive-600 hover:shadow-glow-green'
            }`}
          >
            {callState !== 'idle'
              ? <PhoneOff size={36} className="text-white" />
              : <Mic size={40} className="text-white" />
            }
          </button>
          {callState !== 'idle' && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              {[0,1,2].map(i => (
                <div key={i} className="absolute w-28 h-28 rounded-full border-2 border-leaf-400/30 animate-ping"
                  style={{ animationDelay: `${i * 0.4}s`, animationDuration: '1.5s' }} />
              ))}
            </div>
          )}
        </div>
        <p className="text-xs text-muted font-medium">
          {callState === 'idle' ? 'Tap to start' : callState === 'ringing' ? '📞 Ringing...' : callState === 'connected' ? '🟢 Connected' : callState === 'processing' ? '🧠 Processing...' : callState === 'responding' ? '🔊 Speaking...' : '✅ Done'}
        </p>
      </div>

      {/* Waveform */}
      <VoiceWaveform active={callState === 'responding' || callState === 'connected'} />

      {/* Transcript & Response */}
      {transcript && (
        <div className="bg-white rounded-3xl shadow-card p-4 space-y-2">
          <div className="flex items-center gap-2 text-[10px] font-bold text-muted uppercase tracking-wider">
            <Mic size={10} /> Your Input
          </div>
          <p className="text-sm text-dark font-medium">{transcript}</p>
        </div>
      )}
      {aiResponse && (
        <div className="bg-gradient-to-br from-leaf-50 to-cream-200 rounded-3xl shadow-card p-4 space-y-2 border border-leaf-200/50">
          <div className="flex items-center gap-2 text-[10px] font-bold text-leaf-600 uppercase tracking-wider">
            <Sparkles size={10} /> AI Response
          </div>
          <p className="text-sm text-dark font-medium leading-relaxed whitespace-pre-wrap">{typedResponse}<span className="animate-pulse">|</span></p>
        </div>
      )}

      {/* Phone Input */}
      <div className="bg-white rounded-3xl shadow-card p-4 space-y-3">
        <p className="text-xs font-bold text-muted uppercase tracking-wider">📞 Call Mode</p>
        <input type="tel" placeholder="+91 XXXXXXXXXX" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)}
          className="input-mobile text-sm" />
        <button onClick={initiateCall} disabled={callState !== 'idle'}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-90">
          <Phone size={16} /> {callState === 'idle' ? 'Call Me Now' : 'In Call...'}
        </button>
      </div>

      {/* Text Query */}
      <div className="bg-white rounded-3xl shadow-card p-4 space-y-3">
        <p className="text-xs font-bold text-muted uppercase tracking-wider">💬 Text Demo</p>
        <div className="flex gap-2">
          <input type="text" placeholder={language === 'te' ? 'మీ ప్రశ్న...' : 'Ask about farming...'}
            value={textQuery} onChange={(e) => setTextQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendTextQuery()}
            className="input-mobile text-sm flex-1" />
          <button onClick={sendTextQuery} disabled={callState === 'processing' || !textQuery.trim()}
            className="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-2xl flex items-center justify-center shadow-lg active:scale-90 disabled:opacity-90 transition-all">
            <ArrowRight size={18} />
          </button>
        </div>
      </div>

      {/* History */}
      {callHistory.length > 0 && (
        <div className="space-y-3">
          <p className="text-xs font-bold text-muted uppercase tracking-wider flex items-center gap-1"><Volume2 size={12} /> Recent</p>
          {callHistory.map(e => (
            <div key={e.id} className="bg-white rounded-2xl shadow-card p-3 space-y-1">
              <p className="text-[10px] text-muted">{e.time} • {e.lang === 'te' ? 'తెలుగు' : 'English'}</p>
              <p className="text-xs font-bold text-dark">Q: {e.query}</p>
              <p className="text-xs text-muted">A: {e.response}</p>
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="fixed bottom-20 left-4 right-4 bg-red-500 text-white px-4 py-3 rounded-2xl shadow-xl text-sm font-medium animate-fade-in-up z-50 flex items-center justify-between">
          <span className="flex items-center gap-2"><WifiOff size={16} /> {error}</span>
          <button onClick={() => setError('')} className="text-xs underline">Dismiss</button>
        </div>
      )}
    </div>
  );
};

export default AgriVoice;
