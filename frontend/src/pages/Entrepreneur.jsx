import React, { useState } from 'react';
import { Zap, Users, Trophy, ChevronLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import BuyerFinderTab from '../components/BuyerFinderTab';
import SuccessStoriesTab from '../components/SuccessStoriesTab';
import SmartRecommendTab from '../components/SmartRecommendTab';

const TABS = [
  { id: 'smart', label: 'AI Picks', icon: Zap },
  { id: 'buyers', label: 'Buyers', icon: Users },
  { id: 'stories', label: 'Success', icon: Trophy },
];

const Entrepreneur = () => {
  const [activeTab, setActiveTab] = useState('smart');

  return (
    <div className="min-h-screen px-4 pt-6 pb-4 max-w-lg mx-auto space-y-5 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link to="/" className="w-10 h-10 bg-white rounded-2xl shadow-card flex items-center justify-center active:scale-90 transition-transform">
          <ChevronLeft size={20} className="text-dark" />
        </Link>
        <div>
          <h1 className="text-xl font-extrabold text-dark tracking-tight">Venture Planner</h1>
          <p className="text-xs text-muted">Smart agri-business recommendations</p>
        </div>
      </div>

      {/* Hero Banner */}
      <div className="img-card rounded-3xl h-36 overflow-hidden">
        <img src="https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&q=80" alt="Agriculture" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-wheat-700/90 to-transparent z-[1]" />
        <div className="absolute bottom-0 left-0 right-0 z-10 p-4">
          <p className="text-white font-extrabold text-lg">Convert Crops → Business 💼</p>
          <p className="text-white text-xs mt-0.5">AI-powered venture intelligence</p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-2 bg-cream-200/60 p-1 rounded-2xl">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-xs font-bold transition-all duration-300 ${
              activeTab === tab.id
                ? 'bg-white text-leaf-700 shadow-card'
                : 'text-muted hover:text-dark'
            }`}
          >
            <tab.icon size={14} /> {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="animate-fade-in">
        {activeTab === 'smart' && <SmartRecommendTab />}
        {activeTab === 'buyers' && <BuyerFinderTab />}
        {activeTab === 'stories' && <SuccessStoriesTab />}
      </div>
    </div>
  );
};

export default Entrepreneur;
