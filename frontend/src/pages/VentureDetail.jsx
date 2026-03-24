import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Sprout, BadgeIndianRupee, TrendingUp, Package, Wrench, Factory, CheckCircle2, Users, BarChart3, Droplets, Sun, Mountain, Target } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';

const VentureDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const API = `${API_BASE_URL}/api/venture`;
  const [venture, setVenture] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/${id}`)
      .then(res => setVenture(res.data))
      .catch(() => navigate('/entrepreneur'))
      .finally(() => setLoading(false));
  }, [id, navigate]);

  if (loading) return (
    <div className="flex justify-center items-center py-32">
      <div className="animate-spin h-12 w-12 border-4 border-green-500 border-t-transparent rounded-full" />
    </div>
  );
  if (!venture) return null;

  return (
    <div className="max-w-5xl mx-auto pt-24 pb-16 px-4">
      <button onClick={() => navigate('/entrepreneur')} className="flex items-center gap-2 text-gray-700 hover:text-green-600 transition-colors font-medium mb-8">
        <ArrowLeft size={20} /> Back to Venture Planner
      </button>

      {/* SECTION 1 — Business Overview */}
      <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-gray-100 mb-8">
        <div className="flex flex-wrap gap-3 mb-4">
          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">{venture.crop_name}</span>
          <span className="bg-amber-100 text-amber-700 px-3 py-1 rounded-full text-sm font-bold">{venture.business_category}</span>
          <span className={`px-3 py-1 rounded-full text-sm font-bold ${venture.demand_level === 'Very High' ? 'bg-red-100 text-red-700' : venture.demand_level === 'High' ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'}`}>
            {venture.demand_level} Demand
          </span>
        </div>
        <h1 className="text-3xl md:text-4xl font-black text-gray-800 mb-6">{venture.venture_name}</h1>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Metric icon={<BadgeIndianRupee className="text-amber-500" />} title="Investment" value={venture.investment_range} />
          <Metric icon={<TrendingUp className="text-green-500" />} title="ROI" value={venture.roi_range} />
          <Metric icon={<BarChart3 className="text-blue-500" />} title="Monthly Income" value={venture.monthly_income} />
          <Metric icon={<Target className="text-purple-500" />} title="Profit Margin" value={venture.profit_margin} />
        </div>
        <div className="flex flex-wrap gap-4 mt-6 pt-6 border-t border-gray-100 text-sm text-gray-700">
          <span className="flex items-center gap-1.5 font-medium"><Mountain size={16} className="text-amber-600" /> Soil: {venture.soil_suitability}</span>
          <span className="flex items-center gap-1.5 font-medium"><Droplets size={16} className="text-blue-500" /> Water: {venture.water_requirement}</span>
          <span className="flex items-center gap-1.5 font-medium"><Sun size={16} className="text-orange-500" /> Season: {venture.season_suitability}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* SECTION 2 — Investment Breakdown */}
        <Section title="Investment Breakdown" icon={<BadgeIndianRupee className="text-amber-500" />}>
          <div className="space-y-3">
            {Object.entries(venture.investment_breakdown || {}).map(([k, v]) => (
              <div key={k} className="flex justify-between items-center bg-amber-50/50 p-3 rounded-xl border border-amber-100/50">
                <span className="font-medium text-gray-700">{k}</span>
                <span className="font-bold text-gray-800">{v}</span>
              </div>
            ))}
          </div>
        </Section>

        {/* SECTION 3 — Raw Material */}
        <Section title="Raw Material Required" icon={<Package className="text-orange-500" />}>
          <div className="space-y-3">
            {Object.entries(venture.raw_material_required || {}).map(([k, v]) => (
              <div key={k} className="flex justify-between items-center bg-orange-50/50 p-3 rounded-xl border border-orange-100/50">
                <span className="font-medium text-gray-700">{k}</span>
                <span className="font-bold text-gray-800">{v}</span>
              </div>
            ))}
          </div>
        </Section>

        {/* SECTION 4 — Production Capacity */}
        <Section title="Production Capacity" icon={<Factory className="text-indigo-500" />}>
          <div className="space-y-3">
            {Object.entries(venture.production_capacity || {}).map(([k, v]) => (
              <div key={k} className="flex justify-between items-center bg-indigo-50/50 p-3 rounded-xl border border-indigo-100/50">
                <span className="font-medium text-gray-700">{k}</span>
                <span className="font-bold text-gray-800">{v}</span>
              </div>
            ))}
          </div>
        </Section>

        {/* SECTION 5 — Market Demand */}
        <Section title="Market Demand & Buyers" icon={<Users className="text-purple-500" />}>
          {venture.market_demand?.type && (
            <div className="mb-4">
              <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-2">Major Buyers</span>
              <div className="flex flex-wrap gap-2">
                {venture.market_demand.type.map((b, i) => (
                  <span key={i} className="bg-purple-50 border border-purple-100 text-purple-700 px-3 py-2 rounded-xl text-sm font-bold">{b}</span>
                ))}
              </div>
            </div>
          )}
          {venture.market_demand?.cities && (
            <div>
              <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block mb-2">Target Markets</span>
              <div className="flex flex-wrap gap-2">
                {venture.market_demand.cities.map((c, i) => (
                  <span key={i} className="bg-gray-100 text-gray-700 px-3 py-2 rounded-xl text-sm font-bold">{c}</span>
                ))}
              </div>
            </div>
          )}
        </Section>

        {/* SECTION 6 — Machinery */}
        <Section title="Machinery Required" icon={<Wrench className="text-gray-800" />}>
          <div className="grid grid-cols-1 gap-3">
            {(venture.machinery_required || []).map((m, i) => (
              <div key={i} className="flex items-center gap-3 bg-gray-50 p-3 rounded-xl border border-gray-100">
                <div className="w-8 h-8 bg-gray-200 rounded-lg flex items-center justify-center text-gray-700 font-bold text-sm">{i + 1}</div>
                <span className="font-bold text-gray-800">{m}</span>
              </div>
            ))}
          </div>
        </Section>

        {/* SECTION 7 — Implementation Steps */}
        <Section title="Step-by-Step Implementation" icon={<CheckCircle2 className="text-emerald-500" />} full>
          <div className="space-y-4">
            {(venture.implementation_steps || []).map((step, i) => (
              <div key={i} className="flex gap-4 items-start">
                <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 font-black text-sm flex items-center justify-center shrink-0 shadow-sm">{i + 1}</div>
                <div className="bg-white p-4 rounded-2xl shadow-sm border border-emerald-100 text-gray-700 font-medium flex-1">{step}</div>
              </div>
            ))}
          </div>
        </Section>
      </div>

      {/* CTA */}
      <div className="mt-8 bg-gradient-to-r from-green-600 to-emerald-600 rounded-3xl p-8 text-white text-center">
        <Sprout size={36} className="mx-auto mb-3 opacity-80" />
        <h3 className="text-2xl font-black mb-2">Ready to Start This Venture?</h3>
        <p className="text-green-100 text-sm mb-5">Find buyers for your products and connect with successful farmers</p>
        <button onClick={() => navigate('/entrepreneur')} className="bg-white text-green-700 px-8 py-3 rounded-2xl font-bold hover:bg-green-50 transition-colors">
          Explore Buyer Network →
        </button>
      </div>
    </div>
  );
};

const Metric = ({ icon, title, value }) => (
  <div className="bg-gray-50 p-4 rounded-2xl">
    <div className="flex items-center gap-2 mb-2">{icon}<span className="text-xs font-bold text-gray-600 uppercase tracking-wider">{title}</span></div>
    <div className="text-lg font-black text-gray-800">{value}</div>
  </div>
);

const Section = ({ title, icon, children, full }) => (
  <div className={`bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-gray-100 ${full ? 'md:col-span-2' : ''}`}>
    <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-100">
      <div className="p-2 bg-gray-50 rounded-xl">{icon}</div>
      <h2 className="text-xl font-bold text-gray-800">{title}</h2>
    </div>
    {children}
  </div>
);

export default VentureDetail;
