import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
  ArrowLeft, BadgeIndianRupee, TrendingUp, Target, Factory, 
  MapPin, Box, Briefcase, Award, ShieldCheck, Flame, Play,
  Users, Building, Package, ExternalLink, Loader2, Settings
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { API_BASE_URL } from '../config/api';


const API = `${API_BASE_URL}/api`;

const BusinessDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [business, setBusiness] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBusinessDetails = async () => {
      try {
        setLoading(true);
        const { data } = await axios.get(`${API}/venture/business/${id}`);
        setBusiness(data);
      } catch (err) {
        console.error("Failed to fetch business details:", err);
        setError('Could not load the business details. The blueprint might not exist.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchBusinessDetails();
    }
  }, [id]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-green-600 space-y-4">
        <Loader2 size={48} className="animate-spin" />
        <p className="text-xl font-bold">{t('loading_blueprint')}</p>
      </div>
    );
  }

  if (error || !business) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="bg-red-50 text-red-600 p-6 rounded-2xl max-w-md text-center border border-red-100">
          <Flame size={48} className="mx-auto mb-4 text-red-400" />
          <h2 className="text-xl font-bold mb-2">{t('blueprint_not_found')}</h2>
          <p className="text-sm">{error}</p>
          <button 
            onClick={() => navigate('/entrepreneur')}
            className="mt-6 bg-red-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-red-700 transition-colors"
          >
            {t('go_back')}
          </button>
        </div>
      </div>
    );
  }

  const RISK_COLORS = {
    Low: 'bg-green-100 text-green-700',
    Medium: 'bg-amber-100 text-amber-700',
    High: 'bg-red-100 text-red-700',
  };
  
  const DEMAND_COLORS = {
    'Very High': 'bg-red-100 text-red-700',
    High: 'bg-orange-100 text-orange-700',
    Medium: 'bg-blue-100 text-blue-700',
    Low: 'bg-gray-100 text-gray-800',
  };

  return (
    <div className="max-w-7xl mx-auto px-4 pb-24 animate-in fade-in duration-500">
      {/* Top Navigation */}
      <button 
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-700 hover:text-green-600 font-bold mb-6 transition-colors group"
      >
        <div className="w-8 h-8 rounded-full bg-gray-100 group-hover:bg-green-100 flex items-center justify-center transition-colors">
          <ArrowLeft size={16} />
        </div>
        {t('back_recommendations')}
      </button>

      {/* Hero Section */}
      <div className="bg-white rounded-[2rem] overflow-hidden shadow-sm border border-gray-100 mb-8 flex flex-col md:flex-row relative">
        {/* Abstract Background Element */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-green-50 rounded-full blur-3xl -mr-20 -mt-20 opacity-90 pointer-events-none" />
        
        <div className="md:w-1/3 h-64 md:h-autorelative">
           <img 
             src={business.image || `https://source.unsplash.com/600x600/?${encodeURIComponent(business.product || 'agriculture,farm')}`} 
             alt={business.name}
             className="w-full h-full object-cover"
             onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1558448766-2679883d6fdc?auto=format&fit=crop&q=80&w=600' }}
           />
           <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent md:hidden" />
        </div>
        
        <div className="md:w-2/3 p-8 lg:p-12 flex flex-col justify-center relative z-10">
          <div className="flex flex-wrap gap-2 mb-4">
            <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider ${DEMAND_COLORS[business.demand] || 'bg-gray-100 text-gray-800'}`}>
              {business.demand} Demand
            </span>
            <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider ${RISK_COLORS[business.risk] || 'bg-gray-100 text-gray-800'}`}>
              {business.risk} Risk
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider bg-purple-100 text-purple-700">
              {business.category}
            </span>
          </div>
          
          <h1 className="text-3xl lg:text-5xl font-black text-gray-900 leading-tight mb-4">
            {business.name}
          </h1>
          
          <p className="text-lg text-gray-800 leading-relaxed mb-6 max-w-2xl">
            {business.description || `A highly profitable ${business.category?.toLowerCase() || 'agri'} venture focusing on ${business.product?.toLowerCase() || 'agricultural'} value addition.`}
          </p>

          <div className="flex flex-wrap gap-6 items-center border-t border-gray-100 pt-6">
            <div>
              <p className="text-xs font-bold text-gray-600 uppercase tracking-wider mb-1">Raw Material</p>
              <p className="font-bold text-gray-800 flex items-center gap-2">
                <br className="text-green-500" /> {business.product}
              </p>
            </div>
            <div className="w-px h-8 bg-gray-200 hidden sm:block" />
            <div>
              <p className="text-xs font-bold text-gray-600 uppercase tracking-wider mb-1">Relevance Score</p>
              <p className="font-black text-green-600 flex items-center gap-1 text-xl">
                ⚡ {business.score} <span className="text-sm text-gray-600 font-bold">/ 100</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column - Financials & Quick Stats */}
        <div className="lg:col-span-1 space-y-8">
          
          {/* Financial Highlights */}
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-black text-gray-800 mb-5 flex items-center gap-2">
              <BadgeIndianRupee className="text-green-500" /> {t('financial_projections')}
            </h3>
            
            <div className="space-y-4">
              <div className="bg-green-50 rounded-2xl p-4 border border-green-100">
                <p className="text-xs font-bold text-green-700 uppercase tracking-wider mb-1">{t('est_investment')}</p>
                <p className="text-2xl font-black text-green-900">{business.investment_range}</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-blue-50 rounded-2xl p-4 border border-blue-100">
                  <p className="text-[10px] font-bold text-blue-700 uppercase tracking-wider flex items-center gap-1 mb-1">
                    <TrendingUp size={12} /> {t('expected_roi')}
                  </p>
                  <p className="text-lg font-black text-blue-900">{business.roi}</p>
                </div>
                <div className="bg-emerald-50 rounded-2xl p-4 border border-emerald-100">
                  <p className="text-[10px] font-bold text-emerald-700 uppercase tracking-wider flex items-center gap-1 mb-1">
                    <Target size={12} /> {t('profit_margin')}
                  </p>
                  <p className="text-lg font-black text-emerald-900">{business.profit_margin}</p>
                </div>
              </div>

              <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-5 text-white shadow-lg">
                <p className="text-xs font-bold text-gray-600 uppercase tracking-wider mb-1">{t('est_monthly_income')}</p>
                <p className="text-3xl font-black text-green-400">{business.monthly_income}</p>
                <p className="text-xs text-gray-600 mt-2 flex items-center gap-1">
                  <Flame size={12} className="text-orange-400" /> Highly lucrative
                </p>
              </div>
            </div>
          </div>

          {/* Operational Requirements */}
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-black text-gray-800 mb-5 flex items-center gap-2">
              <Settings className="text-green-500" /> {t('operational_needs')}
            </h3>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <div className="p-2 bg-gray-50 rounded-lg"><MapPin size={18} className="text-gray-700" /></div>
                <div>
                  <p className="text-sm font-bold text-gray-800">{t('min_land')}</p>
                  <p className="text-sm text-gray-700">{business.min_land_acres} Acres required</p>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="p-2 bg-gray-50 rounded-lg"><Box size={18} className="text-blue-500" /></div>
                <div>
                  <p className="text-sm font-bold text-gray-800">{t('water_req')}</p>
                  <p className="text-sm text-gray-700">{business.water_requirement} Level</p>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="p-2 bg-gray-50 rounded-lg"><TrendingUp size={18} className="text-emerald-500" /></div>
                <div>
                  <p className="text-sm font-bold text-gray-800">{t('export_potential')}</p>
                  <p className="text-sm text-gray-700">~{business.export_growth}% Annual Growth</p>
                </div>
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column - Deep Dive */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Setup Steps Timeline */}
          <div className="bg-white rounded-3xl p-6 lg:p-8 shadow-sm border border-gray-100">
            <h3 className="text-xl font-black text-gray-800 mb-6 flex items-center gap-2">
              <Play className="text-green-500" fill="currentColor" /> {t('implementation_roadmap')}
            </h3>
            
            <div className="relative border-l-2 border-green-100 ml-3 md:ml-4 space-y-8 py-2">
              {(business?.setup_steps || []).map((step, idx) => (
                <div key={idx} className="relative pl-8">
                  <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-green-500 ring-4 ring-white shadow-sm" />
                  <div className="bg-gray-50 rounded-2xl p-5 border border-gray-100 hover:border-green-200 transition-colors">
                    <h4 className="font-bold text-gray-800 text-lg mb-2 flex items-center gap-2">
                      <span className="text-green-600 text-sm">Step {idx + 1}:</span> {step.title}
                    </h4>
                    <p className="text-gray-800 leading-relaxed text-sm">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Equipment & Requirements Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            {/* Machinery */}
            <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-black text-gray-800 mb-5 flex items-center gap-2">
                <Factory className="text-blue-500" /> {t('req_machinery')}
              </h3>
              <ul className="space-y-3">
                {(business?.equipment || ["Basic Processing Unit", "Packaging Material", "Storage Facility"]).map((eq, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-800">
                    <ShieldCheck size={16} className="text-blue-400 shrink-0 mt-0.5" />
                    <span className="font-medium text-gray-700">{eq}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Target Buyers */}
            <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-black text-gray-800 mb-5 flex items-center gap-2">
                <Users className="text-purple-500" /> {t('target_buyers')}
              </h3>
              <ul className="space-y-3">
                {(business?.buyers || ["Local Markets", "Wholesalers", "Retail Chains"]).map((buyer, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-800 border-b border-gray-50 pb-2 last:border-0">
                    <Briefcase size={16} className="text-purple-400 shrink-0 mt-0.5" />
                    <span className="font-medium text-gray-700">{buyer}</span>
                  </li>
                ))}
              </ul>
            </div>
            
          </div>

          {/* Subsidies & Marketing */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Government Schemes */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-3xl p-6 shadow-sm border border-green-100">
               <h3 className="text-lg font-black text-green-900 mb-4 flex items-center gap-2">
                <Award className="text-green-600" /> {t('applicable_subsidies')}
              </h3>
              <div className="space-y-3">
                {(business?.subsidies || ["PMFME Scheme", "Agriculture Infrastructure Fund"]).map((sub, i) => (
                  <div key={i} className="bg-white/90 border border-black/5 backdrop-blur-sm rounded-xl p-3 border border-green-200/50 flex items-start gap-2">
                     <span className="text-green-600 font-black mt-0.5">•</span>
                     <p className="text-sm font-bold text-green-800">{sub}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Marketing Strategy */}
            <div className="bg-gradient-to-br from-orange-50 to-amber-50 rounded-3xl p-6 shadow-sm border border-orange-100">
               <h3 className="text-lg font-black text-orange-900 mb-4 flex items-center gap-2">
                <Target className="text-orange-600" /> {t('sales_marketing')}
              </h3>
              <ul className="space-y-2">
                {(business?.marketing_strategy || ["B2B Tie-ups", "Direct to Consumer"]).map((strat, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm font-medium text-orange-800 bg-white/85 border border-black/5 px-3 py-2 rounded-lg">
                    <Target size={14} className="text-orange-500" /> {strat}
                  </li>
                ))}
              </ul>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default BusinessDetails;
