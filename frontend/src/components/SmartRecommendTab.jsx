import React, { useState } from 'react';
import {
  Search, Sprout, Droplets, Sun, Mountain, BadgeIndianRupee,
  TrendingUp, Target, Zap, Factory, Loader2, ShieldCheck,
  BarChart3, Flame, AlertTriangle, ChevronRight, Star, Filter
} from 'lucide-react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { API_BASE_URL } from '../config/api';


const API = `${API_BASE_URL}/api`;

const SOIL_TYPES = ['Alluvial', 'Black Soil', 'Red Soil', 'Sandy', 'Clay', 'Loamy'];
const SEASONS = ['Kharif', 'Rabi', 'Summer'];
const WATER_OPTIONS = [
  { value: 'Low', label: 'Low (Rain dependent)', icon: '🌧️' },
  { value: 'Medium', label: 'Medium (Borewell)', icon: '💧' },
  { value: 'High', label: 'High (Canal/River)', icon: '🌊' },
];
const BUDGET_OPTIONS = [
  { value: 100000, label: '₹1 Lakh' },
  { value: 300000, label: '₹3 Lakhs' },
  { value: 500000, label: '₹5 Lakhs' },
  { value: 1000000, label: '₹10 Lakhs' },
  { value: 2000000, label: '₹20 Lakhs' },
  { value: 5000000, label: '₹50 Lakhs' },
];

const POPULAR_PRODUCTS = [
  'Milk', 'Rice', 'Wheat', 'Turmeric', 'Potato', 'Tomato', 'Honey',
  'Mushroom', 'Maize', 'Banana', 'Mango', 'Coconut', 'Coffee', 'Tea',
  'Groundnut', 'Soybean', 'Chili', 'Onion', 'Sugarcane', 'Cotton',
  'Ginger', 'Garlic', 'Millets', 'Pulses', 'Mustard',
];

const RISK_COLORS = {
  Low: 'bg-green-100 text-green-700 border-green-200',
  Medium: 'bg-amber-100 text-amber-700 border-amber-200',
  High: 'bg-red-100 text-red-700 border-red-200',
};
const DEMAND_COLORS = {
  'Very High': 'bg-red-100 text-red-700',
  High: 'bg-orange-100 text-orange-700',
  Medium: 'bg-blue-100 text-blue-700',
  Low: 'bg-gray-100 text-gray-800',
};

const SmartRecommendTab = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [product, setProduct] = useState('');
  const [soilType, setSoilType] = useState('');
  const [landSize, setLandSize] = useState('');
  const [season, setSeason] = useState('');
  const [water, setWater] = useState('');
  const [budget, setBudget] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [showForm, setShowForm] = useState(true);

  const handleRecommend = async () => {
    if (!product.trim()) return;
    setLoading(true);
    try {
      const { data } = await axios.post(`${API}/venture/entrepreneur/recommend`, {
        product: product.trim(),
        soil_type: soilType || null,
        land_size: landSize ? parseFloat(landSize) : null,
        season: season || null,
        water: water || null,
        budget: budget ? parseFloat(budget) : null,
      });
      setResults(data);
      setShowForm(false);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const resetSearch = () => {
    setResults(null);
    setShowForm(true);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {showForm && (
        <>
          {/* Product Input */}
          <div className="glass rounded-3xl p-6 border-0">
            <div className="flex items-center gap-2 mb-4">
              <Sprout size={20} className="text-green-500" />
              <span className="text-sm font-bold text-gray-700 uppercase tracking-wider">What do you produce?</span>
            </div>
            <input
              type="text"
              placeholder={t('search_product') + "..."}
              className="w-full px-5 py-4 bg-white/90 border border-black/5 border-2 border-white/40 rounded-2xl input-glow text-lg font-medium transition-all duration-300"
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleRecommend()}
            />
            <div className="flex flex-wrap gap-2 mt-3">
              {POPULAR_PRODUCTS.map(p => (
                <button key={p} onClick={() => setProduct(p)}
                  className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all duration-200 active:scale-95 ${
                    product === p
                      ? 'bg-[#4CAF50] text-white border-2 border-[#388E3C] scale-105 shadow-[0_4px_12px_rgba(76,175,80,0.3)]'
                      : 'bg-white text-gray-700 border border-gray-200 hover:border-green-400 hover:scale-105'
                  }`}>
                  {p}
                </button>
              ))}
            </div>
          </div>

          {/* Farm Details */}
          <div className="glass rounded-3xl p-6 border-0 mt-6">
            <div className="flex items-center gap-2 mb-5">
              <Mountain size={20} className="text-green-500" />
              <span className="text-sm font-bold text-gray-700 uppercase tracking-wider">{t('farm_details')}</span>
              <span className="text-xs text-gray-600 ml-2">(Optional — helps refine recommendations)</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Soil Type */}
              <div>
                <label className="text-xs font-bold text-gray-700 uppercase tracking-wider block mb-2">{t('soil_type')}</label>
                <div className="grid grid-cols-3 gap-2">
                  {SOIL_TYPES.map(s => (
                    <button key={s} onClick={() => setSoilType(soilType === s ? '' : s)}
                      className={`p-2.5 rounded-xl text-xs font-bold transition-all duration-200 active:scale-95 ${
                        soilType === s 
                          ? 'bg-[#4CAF50] text-white border-2 border-[#388E3C] scale-105 shadow-[0_4px_12px_rgba(76,175,80,0.3)]' 
                          : 'bg-white text-gray-700 border border-gray-200 hover:border-green-400 hover:scale-105'
                      }`}>{s}</button>
                  ))}
                </div>
              </div>

              {/* Land Size */}
              <div>
                <label className="text-xs font-bold text-gray-700 uppercase tracking-wider block mb-2">{t('land_size')} (Acres)</label>
                <input type="number" step="any" min="0" placeholder="e.g., 5" value={landSize}
                  onChange={(e) => setLandSize(e.target.value)}
                  className="w-full px-4 py-2.5 bg-white/90 border border-black/5 border-2 border-white/50 rounded-xl input-glow transition-all duration-300" />
              </div>

              {/* Season */}
              <div>
                <label className="text-xs font-bold text-gray-700 uppercase tracking-wider block mb-2">{t('season')}</label>
                <div className="flex gap-2">
                  {SEASONS.map(s => (
                    <button key={s} onClick={() => setSeason(season === s ? '' : s)}
                      className={`flex-1 p-2.5 rounded-xl text-xs font-bold transition-all duration-200 active:scale-95 flex items-center justify-center gap-1 ${
                        season === s 
                          ? 'bg-[#4CAF50] text-white border-2 border-[#388E3C] scale-105 shadow-[0_4px_12px_rgba(76,175,80,0.3)]' 
                          : 'bg-white text-gray-700 border border-gray-200 hover:border-green-400 hover:scale-105'
                      }`}>
                      <Sun size={12} />{s}
                    </button>
                  ))}
                </div>
              </div>

              {/* Water */}
              <div>
                <label className="text-xs font-bold text-gray-700 uppercase tracking-wider block mb-2">Water Availability</label>
                <div className="grid grid-cols-3 gap-2">
                  {WATER_OPTIONS.map(w => (
                    <button key={w.value} onClick={() => setWater(water === w.value ? '' : w.value)}
                      className={`p-2.5 rounded-xl text-xs font-bold transition-all duration-200 active:scale-95 flex items-center justify-center gap-1 ${
                        water === w.value 
                          ? 'bg-[#4CAF50] text-white border-2 border-[#388E3C] scale-105 shadow-[0_4px_12px_rgba(76,175,80,0.3)]' 
                          : 'bg-white text-gray-700 border border-gray-200 hover:border-green-400 hover:scale-105'
                      }`}>
                      <span>{w.icon}</span> {w.value}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Budget */}
            <div className="mt-5">
              <label className="text-xs font-bold text-gray-700 uppercase tracking-wider block mb-2">{t('budget')} (₹)</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <BadgeIndianRupee size={16} className="text-gray-400" />
                </div>
                <input
                  type="number"
                  min="0"
                  step="any"
                  placeholder="e.g., 500000"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-white/90 border border-black/5 border-2 border-white/50 rounded-xl input-glow transition-all duration-300"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            onClick={handleRecommend}
            disabled={loading || !product.trim()}
            className="w-full py-4 mt-6 bg-gradient-to-r from-agri-primary via-agri-secondary to-[#4CAF50] text-white rounded-2xl font-bold text-lg shadow-[0_8px_20px_rgba(46,125,50,0.3)] hover:shadow-[0_12px_25px_rgba(46,125,50,0.4)] transition-all duration-300 hover:scale-[1.02] disabled:opacity-90 disabled:hover:scale-100 flex items-center justify-center gap-3"
          >
            {loading ? (
              <><Loader2 size={22} className="animate-spin" /> Analyzing your farm & generating recommendations...</>
            ) : (
              <span className="text-gray-900 font-semibold drop-shadow-sm flex items-center gap-2"><Zap size={22} /> Get Smart Business Recommendations</span>
            )}
          </button>
        </>
      )}

      {/* Results */}
      {results && !showForm && (
        <div className="space-y-6">
          {/* Header */}
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="text-2xl font-black text-gray-800">
                🚀 Recommended for <span className="text-green-600">{product}</span>
              </h2>
              <p className="text-gray-700 text-sm mt-1">
                Found <span className="font-bold text-green-600">{results.total}</span> profitable business opportunities
                {results.total_generated > results.total && ` (from ${results.total_generated} generated)`}
              </p>
            </div>
            <button onClick={resetSearch}
              className="bg-gray-100 text-gray-800 font-bold px-5 py-2.5 rounded-xl hover:bg-gray-200 transition-colors text-sm">
              ← New Search
            </button>
          </div>

          {/* Filter Info */}
          {(results.filters_applied?.length > 0 || results.filters_relaxed?.length > 0) && (
            <div className="flex flex-wrap gap-2 items-center">
              <Filter size={14} className="text-gray-600" />
              {results.filters_applied?.map((f, i) => (
                <span key={i} className="text-xs bg-green-50 text-green-700 px-2.5 py-1 rounded-full font-medium border border-green-100">
                  ✓ {f.type}: {f.value}
                </span>
              ))}
              {results.filters_relaxed?.map((f, i) => (
                <span key={i} className="text-xs bg-amber-50 text-amber-600 px-2.5 py-1 rounded-full font-medium border border-amber-100">
                  ↩ {f} relaxed
                </span>
              ))}
            </div>
          )}

          {/* Recommendation Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
            {results.recommendations?.map((biz, i) => (
              <div 
                key={i} 
                onClick={() => navigate(`/business-details/${biz.id}`)}
                className="glass rounded-2xl overflow-hidden border-0 cursor-pointer group flex flex-col h-full hover:scale-[1.02] transition-transform duration-300 animate-fade-in-up md:shadow-sm hover:shadow-md"
                style={{ animationDelay: `${i * 50}ms` }}
              >
                {/* Image */}
                <div className="h-32 md:h-40 bg-gradient-to-br from-green-100 via-emerald-50 to-teal-100 relative overflow-hidden shrink-0">
                  <img
                    src={biz.image}
                    alt={biz.name}
                    className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity"
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  
                  {/* Score Badge */}
                  <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded-full shadow-sm">
                    <span className="text-[10px] md:text-xs font-black text-green-700">⚡ {biz.score}</span>
                  </div>
                  
                  {/* Rank Badge */}
                  <div className="absolute top-2 left-2 bg-green-600 text-white w-6 h-6 md:w-8 md:h-8 rounded-full flex items-center justify-center font-black text-xs md:text-sm shadow-lg">
                    #{i + 1}
                  </div>
                  
                  <div className="absolute bottom-2 left-2 right-2 flex justify-between items-end">
                    <h3 className="text-white font-bold text-sm md:text-lg drop-shadow-lg leading-tight line-clamp-2 w-4/5">{biz.name}</h3>
                    <div className="w-6 h-6 md:w-8 md:h-8 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-all translate-x-2 group-hover:translate-x-0 shrink-0">
                      <ChevronRight size={14} className="md:w-4 md:h-4" />
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="p-3 md:p-4 flex-1 flex flex-col justify-between">
                  <div className="space-y-3">
                    {/* Badges */}
                    <div className="flex flex-wrap gap-1 md:gap-1.5">
                      <span className={`text-[8px] md:text-[10px] font-bold px-1.5 md:px-2 py-0.5 rounded-full ${DEMAND_COLORS[biz.demand] || 'bg-gray-100 text-gray-800'}`}>
                        {biz.demand} Demand
                      </span>
                      <span className={`text-[8px] md:text-[10px] font-bold px-1.5 md:px-2 py-0.5 rounded-full border ${RISK_COLORS[biz.risk] || ''}`}>
                        {biz.risk} Risk
                      </span>
                      <span className="text-[8px] md:text-[10px] font-bold px-1.5 md:px-2 py-0.5 rounded-full bg-purple-50 text-purple-600 truncate max-w-[80px] md:max-w-none">
                        {biz.category}
                      </span>
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-2 gap-1.5 md:gap-2">
                      <div className="bg-green-50 p-2 md:p-2.5 rounded-xl border border-green-100 flex flex-col justify-center">
                        <p className="text-[8px] md:text-[9px] text-gray-700 font-bold uppercase flex items-center gap-1 mb-0.5">
                          <BadgeIndianRupee size={10} className="w-2.5 h-2.5 md:w-3 md:h-3" /> Investment
                        </p>
                        <p className="font-bold text-xs md:text-sm text-gray-800 line-clamp-1">{biz.investment_range}</p>
                      </div>
                      <div className="bg-blue-50 p-2 md:p-2.5 rounded-xl border border-blue-100 flex flex-col justify-center">
                        <p className="text-[8px] md:text-[9px] text-gray-700 font-bold uppercase flex items-center gap-1 mb-0.5">
                          <TrendingUp size={10} className="w-2.5 h-2.5 md:w-3 md:h-3" /> ROI
                        </p>
                        <p className="font-bold text-xs md:text-sm text-gray-800 line-clamp-1">{biz.roi}</p>
                      </div>
                      <div className="bg-emerald-50 p-2 md:p-2.5 rounded-xl border border-emerald-100 flex flex-col justify-center">
                        <p className="text-[8px] md:text-[9px] text-gray-700 font-bold uppercase flex items-center gap-1 mb-0.5">
                          <BarChart3 size={10} className="w-2.5 h-2.5 md:w-3 md:h-3" /> Income
                        </p>
                        <p className="font-bold text-xs md:text-sm text-gray-800 line-clamp-1">{biz.monthly_income}</p>
                      </div>
                      <div className="bg-purple-50 p-2 md:p-2.5 rounded-xl border border-purple-100 flex flex-col justify-center">
                        <p className="text-[8px] md:text-[9px] text-gray-700 font-bold uppercase flex items-center gap-1 mb-0.5">
                          <Target size={10} className="w-2.5 h-2.5 md:w-3 md:h-3" /> Margin
                        </p>
                        <p className="font-bold text-xs md:text-sm text-gray-800 line-clamp-1">{biz.profit_margin}</p>
                      </div>
                    </div>
                  </div>

                  {/* Spacer to push Score Bar to bottom */}
                  <div className="pt-3 mt-auto">
                    {/* Score Bar */}
                    <div className="flex justify-between text-[8px] md:text-[10px] text-gray-700 mb-1">
                      <span>Match Quality</span>
                      <span className="font-bold text-green-600">{biz.score}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5 md:h-2">
                      <div
                        className="bg-gradient-to-r from-green-500 to-emerald-400 h-1.5 md:h-2 rounded-full transition-all duration-500"
                        style={{ width: `${Math.min(biz.score, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {results.recommendations?.length === 0 && (
            <div className="bg-white rounded-3xl p-12 text-center border border-gray-100">
              <Sprout size={48} className="mx-auto mb-4 text-gray-300" />
              <p className="text-xl font-medium text-gray-600">No matching ventures found</p>
              <p className="text-sm text-gray-600 mt-2">Try a different product or adjust your filters</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SmartRecommendTab;
