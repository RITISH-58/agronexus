import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, BookOpen, BadgeIndianRupee, TrendingUp, Package, Factory, CheckCircle2, ShieldCheck, MapPin, Eye, Tractor } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';


const API = `${API_BASE_URL}/api/business/blueprint`;

const DEMAND_COLORS = {
  'Very High': 'bg-red-100 text-red-700',
  'Trending': 'bg-orange-100 text-orange-700',
  'High': 'bg-yellow-100 text-yellow-700',
  'Medium': 'bg-blue-100 text-blue-700',
};

const BlueprintDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/${id}`)
      .then(r => setData(r.data))
      .catch(err => {
        console.error(err);
        navigate('/entrepreneur'); // fallback if not found
      })
      .finally(() => setLoading(false));
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-32">
        <div className="animate-spin h-12 w-12 border-4 border-green-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="max-w-5xl mx-auto pt-24 pb-16 px-4">
      {/* Back Button */}
      <button 
        onClick={() => navigate('/entrepreneur')}
        className="flex items-center gap-2 text-gray-700 hover:text-green-600 transition-colors font-medium mb-8"
      >
        <ArrowLeft size={20} /> Back to Search
      </button>

      {/* SECTION 1 - BUSINESS OVERVIEW (Header Section) */}
      <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-gray-100 mb-8">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold tracking-wide uppercase">
            {data.industry_type}
          </span>
          <span className={`px-3 py-1 rounded-full text-sm font-bold ${DEMAND_COLORS[data.demand_level] || DEMAND_COLORS.Medium}`}>
            {data.demand_level} Demand
          </span>
          <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-bold">
            {data.industry_growth_rate}
          </span>
        </div>
        <h1 className="text-3xl md:text-5xl font-black text-gray-800 mb-6">{data.processed_product}</h1>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-8 border-t border-gray-100">
          <Metric title="Total Investment" value={data.investment_range} icon={<BadgeIndianRupee className="text-green-500" size={24}/>} />
          <Metric title="Expected ROI" value={data.roi_range} icon={<TrendingUp className="text-blue-500" size={24}/>} />
          <Metric title="Monthly Revenue" value={data.monthly_revenue} icon={<BadgeIndianRupee className="text-teal-500" size={24}/>} />
          <Metric title="Break-even" value={data.break_even} icon={<CheckCircle2 className="text-orange-500" size={24}/>} />
        </div>
        <div className="flex justify-between items-center mt-6 p-4 rounded-xl bg-gray-50 border border-gray-200">
             <span className="font-bold text-gray-700 uppercase tracking-wide text-sm">Profit Margin</span>
             <span className="font-black text-2xl text-purple-600">{data.profit_margin}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Left Column */}
        <div className="space-y-8">
          
          <SectionCard title="2. Investment Breakdown" icon={<BadgeIndianRupee className="text-amber-500"/>}>
            <ul className="space-y-3">
              {Object.entries(data.investment_breakdown).map(([k, v]) => (
                <li key={k} className="flex justify-between items-center bg-gray-50 p-3 rounded-xl">
                  <span className="text-gray-800 font-medium capitalize">{k.replace('_', ' ')}</span>
                  <span className="font-bold text-gray-800">{v}</span>
                </li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard title="3. Raw Material Requirement" icon={<Tractor className="text-green-600"/>}>
             <ul className="space-y-3">
              {Object.entries(data.raw_material_req).map(([k, v]) => (
                <li key={k} className="flex justify-between items-center bg-green-50/50 p-3 rounded-xl border border-green-100/50">
                  <span className="text-gray-800 font-medium capitalize">{k.replace('_', ' ')}</span>
                  <span className="font-black text-gray-800">{v}</span>
                </li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard title="5. Revenue Projection" icon={<TrendingUp className="text-blue-500"/>}>
             <ul className="space-y-3">
              {Object.entries(data.revenue_projection).map(([k, v]) => (
                <li key={k} className="flex justify-between items-center bg-blue-50/50 p-3 rounded-xl border border-blue-100/50">
                  <span className="text-gray-800 font-medium capitalize">{k.replace('_', ' ')}</span>
                  <span className="font-black text-gray-800 text-lg">{v}</span>
                </li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard title="7. Machinery Required" icon={<Factory className="text-gray-700"/>}>
            <div className="flex flex-wrap gap-2">
              {data.machinery.map((m, i) => (
                <span key={i} className="bg-white border border-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-semibold shadow-sm">
                  {m}
                </span>
              ))}
            </div>
          </SectionCard>

          <SectionCard title="9. Government Schemes" icon={<ShieldCheck className="text-emerald-600"/>}>
            <div className="space-y-4">
              {data.schemes.map((scheme, i) => (
                <div key={i} className="bg-emerald-50 border border-emerald-100 p-4 rounded-2xl flex items-center gap-3">
                  <ShieldCheck className="text-emerald-500 shrink-0" size={24} />
                  <span className="font-bold text-gray-800 text-lg">{scheme}</span>
                </div>
              ))}
            </div>
          </SectionCard>

        </div>

        {/* Right Column */}
        <div className="space-y-8">
          
          <SectionCard title="4. Production Capacity" icon={<Package className="text-purple-500"/>}>
             <ul className="space-y-3">
              {Object.entries(data.production_capacity).map(([k, v]) => (
                <li key={k} className="flex justify-between items-center bg-purple-50/50 p-3 rounded-xl border border-purple-100/50">
                  <span className="text-gray-800 font-medium capitalize">{k.replace('_', ' ')}</span>
                  <span className="font-bold text-gray-800">{v}</span>
                </li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard title="6. Market Demand" icon={<MapPin className="text-red-500"/>}>
            <div className="space-y-5">
              <div>
                <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-1">Demand Level</span>
                <span className="text-xl font-black text-gray-800">{data.market_demand.demand_level}</span>
              </div>
              <div>
                <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-2">Major Buyers</span>
                <div className="flex flex-wrap gap-2">
                  {data.market_demand.buyers.map((b,i) => <span key={i} className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-xs font-bold">{b}</span>)}
                </div>
              </div>
              <div>
                <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-2">Demand Cities</span>
                <p className="text-gray-700 font-medium">{data.market_demand.cities.join(", ")}</p>
              </div>
            </div>
          </SectionCard>

          <SectionCard title="8. Required Skills" icon={<BookOpen className="text-teal-500"/>}>
            <ul className="space-y-3">
              {data.skills_required.map((s, i) => (
                <li key={i} className="flex items-center gap-3 text-gray-800 font-bold bg-teal-50/50 p-3 rounded-xl border border-teal-100/50">
                  <CheckCircle2 size={18} className="text-teal-500 flex-shrink-0" /> {s}
                </li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard title="10. Step-by-Step Implementation" icon={<CheckCircle2 className="text-orange-500"/>}>
            <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-orange-200 before:to-orange-50">
              {data.implementation_steps.map((step, i) => (
                <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-orange-100 text-orange-600 font-black shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                    {i + 1}
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-4 rounded-2xl shadow-sm border border-orange-100 text-gray-700 font-medium ml-4 md:ml-0">
                    {step}
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>

        </div>
      </div>
    </div>
  );
};

const Metric = ({ title, value, icon }) => (
  <div>
    <div className="flex items-center gap-2 mb-2">
      {icon}
      <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">{title}</span>
    </div>
    <div className="text-xl md:text-2xl font-black text-gray-800">{value}</div>
  </div>
);

const SectionCard = ({ title, icon, children }) => (
  <div className="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-gray-100">
    <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-100">
      <div className="p-2 bg-gray-50 rounded-xl">{icon}</div>
      <h2 className="text-xl font-bold text-gray-800">{title}</h2>
    </div>
    {children}
  </div>
);

export default BlueprintDetails;
