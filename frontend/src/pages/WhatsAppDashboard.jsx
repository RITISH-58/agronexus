import React, { useState, useEffect } from 'react';
import { MessageCircle, Users, Activity, Phone, ArrowLeft, Send } from 'lucide-react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';

const API = `${API_BASE_URL}/api/whatsapp/analytics`;

const WhatsAppDashboard = () => {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState({ total_queries: 0, unique_users: 0, recent_messages: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const { data } = await axios.get(API);
        setAnalytics(data);
      } catch (error) {
        console.error("Failed to fetch WhatsApp analytics", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
    
    // Poll every 10 seconds for real-time feel
    const interval = setInterval(fetchAnalytics, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen pb-safe bg-gradient-to-br from-[#F7F8F2] to-[#E8F5E9] animate-fade-in">
      {/* Header */}
      <div className="bg-[#128C7E] px-5 py-6 rounded-b-[32px] shadow-lg relative overflow-hidden z-10">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10 mix-blend-overlay"></div>
        <div className="relative z-10 flex items-center gap-4">
          <button onClick={() => navigate(-1)} className="p-2 bg-white/20 rounded-full text-white backdrop-blur-sm hover:scale-105 transition-transform">
            <ArrowLeft size={20} className="text-white" />
          </button>
          <div>
            <h1 className="text-2xl font-black text-white drop-shadow-sm flex items-center gap-2">
              Agropreneur AI <MessageCircle size={22} className="text-white" />
            </h1>
            <p className="text-white text-sm font-medium mt-0.5">WhatsApp Assistant Dashboard</p>
          </div>
        </div>
      </div>

      <div className="px-5 pt-6 space-y-6 max-w-lg mx-auto">
        {/* Quick Stats Grid */}
        <div className="grid grid-cols-2 gap-4">
          <div className="glass-card p-5 bg-white flex flex-col items-center justify-center text-center">
            <div className="w-12 h-12 rounded-2xl bg-green-50 text-[#128C7E] flex items-center justify-center mb-3 shadow-sm border border-green-100">
              <MessageCircle size={24} strokeWidth={2.5} />
            </div>
            <p className="text-3xl font-black text-dark tracking-tight">{loading ? '-' : analytics.total_queries}</p>
            <p className="text-[11px] text-gray-700 font-bold uppercase tracking-wider mt-1">Total Queries</p>
          </div>

          <div className="glass-card p-5 bg-white flex flex-col items-center justify-center text-center">
            <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-3 shadow-sm border border-blue-100">
              <Users size={24} strokeWidth={2.5} />
            </div>
            <p className="text-3xl font-black text-dark tracking-tight">{loading ? '-' : analytics.unique_users}</p>
            <p className="text-[11px] text-gray-700 font-bold uppercase tracking-wider mt-1">Farmers Helped</p>
          </div>
        </div>

        {/* Live Chat Preview */}
        <div>
          <div className="flex items-center justify-between mb-4 px-1">
            <h2 className="text-lg font-black text-dark flex items-center gap-2">
              <Activity size={18} className="text-[#128C7E]" /> Live Activity
            </h2>
            <div className="flex items-center gap-1.5 text-xs font-bold text-green-600 bg-green-50 px-2.5 py-1 rounded-full border border-green-200">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Online
            </div>
          </div>

          <div className="glass-card bg-[#E5DDD5] overflow-hidden border border-[#D1D7D9] relative flex flex-col">
            {/* WhatsApp Chat Background Pattern */}
            <div className="absolute inset-0 bg-[url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png')] opacity-100 mix-blend-multiply"></div>
            
            <div className="relative z-10 min-h-[400px] max-h-[500px] overflow-y-auto p-4 space-y-5 custom-scrollbar flex flex-col justify-end">
              {loading ? (
                <div className="text-center text-gray-700 text-sm font-medium w-full py-10 bg-white/85 border border-black/5 rounded-xl backdrop-blur-sm">
                  Loading farmer interactions...
                </div>
              ) : analytics.recent_messages.length === 0 ? (
                <div className="text-center text-gray-700 text-sm font-medium w-full py-10 bg-white/85 border border-black/5 rounded-xl backdrop-blur-sm">
                  No messages yet. Send a WhatsApp message to {import.meta.env.VITE_TWILIO_NUMBER || 'your sandbox'} to see it here!
                </div>
              ) : (
                analytics.recent_messages.map((msg, idx) => (
                  <div key={idx} className="flex flex-col gap-2">
                    {/* Incoming Farmer Message */}
                    <div className="self-start max-w-[85%]">
                      <div className="bg-white rounded-2xl rounded-tl-sm px-3.5 py-2.5 shadow-sm relative">
                        <span className="absolute -left-2 top-0 text-white"><svg viewBox="0 0 8 13" width="8" height="13"><path opacity=".13" d="M5.188 1H0v11.193l6.467-8.625C7.526 2.156 6.958 1 5.188 1z"></path><path fill="currentColor" d="M5.188 0H0v11.193l6.467-8.625C7.526 1.156 6.958 0 5.188 0z"></path></svg></span>
                        <p className="text-xs font-bold text-purple-600 mb-0.5">{msg.sender_name || msg.phone_number}</p>
                        <p className="text-[14px] text-[#111111] leading-snug">{msg.message_body}</p>
                        <p className="text-[10px] text-gray-600 text-right mt-1">
                          {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </p>
                      </div>
                    </div>

                    {/* Outgoing AI Response */}
                    <div className="self-end max-w-[85%] mt-1">
                      <div className="bg-[#DCF8C6] rounded-2xl rounded-tr-sm px-3.5 py-2.5 shadow-sm relative">
                        <span className="absolute -right-2 top-0 text-[#DCF8C6]"><svg viewBox="0 0 8 13" width="8" height="13"><path opacity=".13" fill="#0000000" d="M1.533 3.118L8 11.193V1H2.812C1.042 1 .474 2.156 1.533 3.118z"></path><path fill="currentColor" d="M1.533 2.118L8 10.193V0H2.812C1.042 0 .474 1.156 1.533 2.118z"></path></svg></span>
                        <p className="text-[14px] text-[#111111] leading-snug whitespace-pre-wrap">{msg.response_body}</p>
                        <div className="flex items-center justify-end gap-1 mt-1">
                          <p className="text-[10px] text-green-700/60">
                            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                          <svg viewBox="0 0 16 11" width="16" height="11" fill="#4FC3A1"><path d="M11.8 1L16 5.5L14.7 6.9L11.8 3.7L9.5 6L8.1 4.6L11.8 1ZM6.3 1L10.5 5.5L9.2 6.9L6.3 3.7L4 6L2.6 4.6L6.3 1ZM1.4 6L0 7.4L3.7 11.5L8 6.9L6.7 5.5L3.7 8.7L1.4 6Z"></path></svg>
                        </div>
                      </div>
                    </div>
                  </div>
                )).reverse() // Reverse so newest is at the bottom visually
              )}
            </div>
            
            {/* Fake WhatsApp Input Footer */}
            <div className="bg-[#F0F2F5] p-3 flex items-center gap-3 relative z-10 border-t border-[#D1D7D9]">
              <div className="flex-1 bg-white rounded-full py-2.5 px-4 text-gray-600 text-sm font-medium shadow-sm">
                Farmers message your Twilio number...
              </div>
              <div className="w-11 h-11 bg-[#128C7E] rounded-full flex items-center justify-center text-white shadow-md">
                <Send size={18} className="translate-x-0.5" />
              </div>
            </div>
          </div>
        </div>

        {/* Integration Instructions */}
        <div className="glass-card p-5 bg-white space-y-3">
          <div className="flex items-center gap-2 text-dark font-black">
            <Phone size={18} className="text-[#128C7E]" /> Twilio Webhook Setup
          </div>
          <p className="text-sm font-medium text-gray-800 leading-relaxed">
            Ensure your Twilio WhatsApp Sandbox webhook is configured to endpoint:
            <br/> <span className="inline-block bg-gray-100 text-dark px-2 py-1 rounded-md text-xs font-mono mt-1 w-full truncate border border-gray-200">
              {import.meta.env.VITE_API_URL || 'YOUR_BASE_URL'}/api/whatsapp
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default WhatsAppDashboard;
