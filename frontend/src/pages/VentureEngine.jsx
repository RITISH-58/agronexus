import React, { useState, useEffect, useCallback } from 'react';
import {
  TrendingUp, Search, BadgeIndianRupee, MapPin, Calculator, Globe2,
  BookOpen, BarChart3, Flame, ChevronRight, Star, Users, Building2,
  Loader2, AlertTriangle, CheckCircle2, ArrowUpRight, Phone, Mail,
  Factory, ShieldCheck, Banknote, Target, Zap, Award
} from 'lucide-react';
import {
  AreaChart, Area, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts';
import axios from 'axios';

const API = `${API_BASE_URL}/api/venture`;

const CROPS = [
  'Rice', 'Turmeric', 'Maize', 'Tomato', 'Chili', 'Millets', 'Cotton', 'Sugarcane',
  'Groundnut', 'Soybean', 'Wheat', 'Banana', 'Coconut', 'Mango', 'Potato', 'Onion',
  'Tea', 'Coffee', 'Pulses'
];

const TABS = [
  { id: 'ideas', label: 'Business Ideas', icon: Factory },
  { id: 'simulator', label: 'Profit Simulator', icon: Calculator },
  { id: 'trends', label: 'Market Trends', icon: TrendingUp },
  { id: 'buyers', label: 'Buyer Finder', icon: MapPin },
  { id: 'loan', label: 'Loan Calculator', icon: Banknote },
  { id: 'export', label: 'Export Insights', icon: Globe2 },
  { id: 'stories', label: 'Success Stories', icon: Award },
];

const DEMAND_COLORS = {
  'Very High': 'bg-red-100 text-red-700 border-red-200',
  'High': 'bg-orange-100 text-orange-700 border-orange-200',
  'Medium': 'bg-yellow-100 text-yellow-700 border-yellow-200',
  'Low': 'bg-gray-100 text-gray-800 border-gray-200',
};

const CHART_COLORS = ['#059669', '#0891b2', '#7c3aed', '#db2777', '#d97706', '#dc2626', '#2563eb', '#16a34a'];

// ─── MAIN COMPONENT ──────────────────────────────────────────
import { API_BASE_URL } from '../config/api';

const VentureEngine = () => {
  const [activeTab, setActiveTab] = useState('ideas');
  const [selectedCrop, setSelectedCrop] = useState('Rice');
  // Setup API
  const API = `${API_BASE_URL}/api/venture`;

  return (
    <div className="max-w-7xl mx-auto pt-24 pb-12 px-4">
      {/* Hero */}
      <div className="text-center mb-8">
        <h1 className="text-4xl md:text-5xl font-black bg-gradient-to-r from-green-700 via-emerald-600 to-teal-600 bg-clip-text text-transparent mb-3">
          🚀 Venture Intelligence Engine
        </h1>
        <p className="text-gray-800 text-lg max-w-3xl mx-auto">
          Transform your crops into profitable agri-ventures. Market analytics, profit simulation, buyer discovery, and financing — all powered by India-scale agricultural datasets.
        </p>
      </div>

      {/* Crop Selector */}
      <div className="flex items-center gap-3 mb-6 overflow-x-auto pb-2">
        <span className="text-sm font-bold text-gray-700 whitespace-nowrap">Crop:</span>
        <div className="flex gap-2">
          {CROPS.map(c => (
            <button key={c} onClick={() => setSelectedCrop(c)}
              className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all whitespace-nowrap ${selectedCrop === c
                  ? 'bg-green-600 text-white shadow-md'
                  : 'bg-white text-gray-800 border border-gray-200 hover:border-green-300 hover:text-green-700'
                }`}>{c}</button>
          ))}
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-1 mb-8 overflow-x-auto pb-2 border-b border-gray-200">
        {TABS.map(tab => {
          const Icon = tab.icon;
          return (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-3 rounded-t-xl text-sm font-semibold transition-all whitespace-nowrap ${activeTab === tab.id
                  ? 'bg-green-600 text-white shadow-md -mb-px'
                  : 'text-gray-700 hover:text-green-700 hover:bg-green-50'
                }`}>
              <Icon size={16} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      {activeTab === 'ideas' && <BusinessIdeasTab crop={selectedCrop} />}
      {activeTab === 'simulator' && <ProfitSimulatorTab crop={selectedCrop} />}
      {activeTab === 'trends' && <MarketTrendsTab crop={selectedCrop} />}
      {activeTab === 'buyers' && <BuyerFinderTab />}
      {activeTab === 'loan' && <LoanCalculatorTab />}
      {activeTab === 'export' && <ExportInsightsTab crop={selectedCrop} />}
      {activeTab === 'stories' && <SuccessStoriesTab crop={selectedCrop} />}
    </div>
  );
};

// ─── SECTION: BUSINESS IDEAS ─────────────────────────────────
const BusinessIdeasTab = ({ crop }) => {
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API}/business-ideas`, { params: { crop } })
      .then(r => setIdeas(r.data.ideas || []))
      .catch(() => setIdeas([]))
      .finally(() => setLoading(false));
  }, [crop]);

  if (loading) return <Spinner />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {ideas.map((biz, i) => (
        <div key={i} className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 border border-gray-100 overflow-hidden group">
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 border-b border-green-100">
            <div className="flex items-center justify-between mb-2">
              <span className={`text-xs font-bold px-2 py-1 rounded-full border ${DEMAND_COLORS[biz.market_demand] || DEMAND_COLORS.Medium}`}>
                {biz.market_demand} Demand
              </span>
              {biz.trending && <span className="text-xs bg-red-100 text-red-600 px-2 py-1 rounded-full font-bold flex items-center gap-1"><Flame size={10} />Trending</span>}
            </div>
            <h3 className="text-lg font-bold text-gray-800 group-hover:text-green-700 transition-colors">{biz.business_name}</h3>
          </div>
          <div className="p-5 space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <InfoChip icon={<BadgeIndianRupee size={14} />} label="Investment" value={biz.investment_display} color="green" />
              <InfoChip icon={<TrendingUp size={14} />} label="ROI" value={biz.roi} color="blue" />
              {biz.monthly_revenue && <InfoChip icon={<BarChart3 size={14} />} label="Revenue/mo" value={biz.monthly_revenue} color="emerald" />}
              {biz.profit_margin && <InfoChip icon={<Target size={14} />} label="Margin" value={biz.profit_margin} color="purple" />}
            </div>
            <p className="text-sm text-gray-800 line-clamp-2">{biz.description}</p>
            {biz.breakeven_period && (
              <div className="text-xs text-gray-700 flex items-center gap-1">
                <CheckCircle2 size={12} className="text-green-500" />Break-even: {biz.breakeven_period}
              </div>
            )}
          </div>
        </div>
      ))}
      {ideas.length === 0 && <EmptyState message={`No business ideas found for ${crop}.`} />}
    </div>
  );
};

// ─── SECTION: PROFIT SIMULATOR ───────────────────────────────
const ProfitSimulatorTab = ({ crop }) => {
  const [ideas, setIdeas] = useState([]);
  const [form, setForm] = useState({
    business_name: '', crop_quantity_tons: 20, processing_capacity_kg_per_day: 500,
    labor_cost_monthly: 30000, electricity_cost_monthly: 8000, market_price_per_kg: 40, rent_monthly: 10000,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`${API}/business-ideas`, { params: { crop } })
      .then(r => {
        const list = r.data.ideas || [];
        setIdeas(list);
        if (list.length > 0) setForm(f => ({ ...f, business_name: list[0].business_name }));
      }).catch(() => { });
  }, [crop]);

  const simulate = () => {
    if (!form.business_name) return;
    setLoading(true);
    axios.post(`${API}/profit-simulation`, form)
      .then(r => setResult(r.data))
      .catch(() => setResult(null))
      .finally(() => setLoading(false));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Input Form */}
      <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
        <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2"><Calculator size={20} className="text-green-600" />Simulation Inputs</h3>
        <div className="space-y-3">
          <div>
            <label className="text-xs font-semibold text-gray-800 block mb-1">Business Type</label>
            <select value={form.business_name} onChange={e => setForm({ ...form, business_name: e.target.value })}
              className="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-green-500 bg-gray-50">
              {ideas.map((b, i) => <option key={i} value={b.business_name}>{b.business_name}</option>)}
            </select>
          </div>
          <NumInput label="Crop Quantity (tons)" value={form.crop_quantity_tons} onChange={v => setForm({ ...form, crop_quantity_tons: v })} />
          <NumInput label="Processing Capacity (kg/day)" value={form.processing_capacity_kg_per_day} onChange={v => setForm({ ...form, processing_capacity_kg_per_day: v })} />
          <NumInput label="Labor Cost (₹/month)" value={form.labor_cost_monthly} onChange={v => setForm({ ...form, labor_cost_monthly: v })} />
          <NumInput label="Electricity (₹/month)" value={form.electricity_cost_monthly} onChange={v => setForm({ ...form, electricity_cost_monthly: v })} />
          <NumInput label="Market Price (₹/kg)" value={form.market_price_per_kg} onChange={v => setForm({ ...form, market_price_per_kg: v })} />
          <NumInput label="Rent (₹/month)" value={form.rent_monthly} onChange={v => setForm({ ...form, rent_monthly: v })} />
          <button onClick={simulate} disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-bold shadow-md hover:shadow-lg transition-all mt-2">
            {loading ? <Loader2 className="animate-spin mx-auto" size={20} /> : '⚡ Simulate Profit'}
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="lg:col-span-2 space-y-6">
        {result ? (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <KpiCard label="Monthly Revenue" value={`₹${(result.monthly_revenue / 1000).toFixed(0)}K`} color="emerald" icon={<BadgeIndianRupee size={18} />} />
              <KpiCard label="Net Profit/mo" value={`₹${(result.net_monthly_profit / 1000).toFixed(0)}K`} color="green" icon={<TrendingUp size={18} />} />
              <KpiCard label="Profit Margin" value={`${result.profit_margin_percent}%`} color="blue" icon={<Target size={18} />} />
              <KpiCard label="Break-even" value={`${result.breakeven_months} mo`} color="purple" icon={<Zap size={18} />} />
            </div>
            {/* Cost Breakdown Pie */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
                <h4 className="font-bold text-gray-800 mb-4">Cost Breakdown</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie data={Object.entries(result.monthly_costs).map(([k, v]) => ({ name: k.replace('_', ' '), value: v }))}
                      cx="50%" cy="50%" outerRadius={90} innerRadius={50} dataKey="value" paddingAngle={2}>
                      {Object.keys(result.monthly_costs).map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                    </Pie>
                    <Tooltip formatter={v => `₹${v.toLocaleString()}`} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              {/* 12-Month Projection */}
              <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
                <h4 className="font-bold text-gray-800 mb-4">12-Month Projection</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={result.monthly_breakdown}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 11 }} tickFormatter={v => `${(v / 1000).toFixed(0)}K`} />
                    <Tooltip formatter={v => `₹${v.toLocaleString()}`} />
                    <Bar dataKey="revenue" fill="#059669" radius={[4, 4, 0, 0]} name="Revenue" />
                    <Bar dataKey="cost" fill="#dc2626" radius={[4, 4, 0, 0]} name="Cost" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        ) : (
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-12 text-center border border-green-100">
            <Calculator size={48} className="mx-auto text-green-300 mb-4" />
            <p className="text-gray-700 text-lg">Configure inputs and click <strong>Simulate Profit</strong> to see detailed projections.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// ─── SECTION: MARKET TRENDS ──────────────────────────────────
const MarketTrendsTab = ({ crop }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API}/market-trends`, { params: { crop } })
      .then(r => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [crop]);

  if (loading) return <Spinner />;
  if (!data || !data.trend_data?.length) return <EmptyState message={`No market data for ${crop}.`} />;

  return (
    <div className="space-y-6">
      {/* KPI Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KpiCard label="Current Price" value={`₹${data.current_price}/qtl`} color="green" icon={<BadgeIndianRupee size={18} />} />
        <KpiCard label="6-Month Change" value={`${data.price_change_percent > 0 ? '+' : ''}${data.price_change_percent}%`}
          color={data.price_change_percent >= 0 ? 'emerald' : 'red'} icon={<TrendingUp size={18} />} />
        <KpiCard label="Predicted Next" value={`₹${data.predicted_next_month}/qtl`} color="blue" icon={<Target size={18} />} />
        <KpiCard label="Demand Forecast" value={data.demand_forecast} color="purple" icon={<BarChart3 size={18} />} />
      </div>

      {/* Chart */}
      <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
        <h4 className="font-bold text-gray-800 mb-1">{crop} — {data.market} Price Trend</h4>
        <p className="text-sm text-gray-700 mb-4">{data.insight}</p>
        <ResponsiveContainer width="100%" height={350}>
          <AreaChart data={data.trend_data}>
            <defs>
              <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#059669" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#059669" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} tickFormatter={v => `₹${v}`} />
            <Tooltip formatter={v => `₹${v}/qtl`} />
            <Area type="monotone" dataKey="price" stroke="#059669" fill="url(#priceGrad)" strokeWidth={2} name="Avg Price" />
            <Line type="monotone" dataKey="max_price" stroke="#0891b2" strokeDasharray="4 4" dot={false} name="Max" />
            <Line type="monotone" dataKey="min_price" stroke="#d97706" strokeDasharray="4 4" dot={false} name="Min" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// ─── SECTION: BUYER FINDER ───────────────────────────────────
const BuyerFinderTab = () => {
  const [product, setProduct] = useState('rice_flour');
  const [location, setLocation] = useState('warangal');
  const [radius, setRadius] = useState(100);
  const [buyers, setBuyers] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchBuyers = () => {
    setLoading(true);
    axios.get(`${API}/buyers`, { params: { product, location, radius } })
      .then(r => setBuyers(r.data.buyers || []))
      .catch(() => setBuyers([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { searchBuyers(); }, []);

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div>
            <label className="text-xs font-semibold text-gray-800 block mb-1">Product Type</label>
            <input value={product} onChange={e => setProduct(e.target.value)} placeholder="e.g. rice_flour"
              className="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-green-500 bg-gray-50" />
          </div>
          <div>
            <label className="text-xs font-semibold text-gray-800 block mb-1">Your Location</label>
            <input value={location} onChange={e => setLocation(e.target.value)} placeholder="e.g. warangal"
              className="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-green-500 bg-gray-50" />
          </div>
          <div>
            <label className="text-xs font-semibold text-gray-800 block mb-1">Radius (km)</label>
            <input type="number" value={radius} onChange={e => setRadius(Number(e.target.value))}
              className="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-green-500 bg-gray-50" />
          </div>
          <button onClick={searchBuyers} className="bg-green-600 text-white px-6 py-2.5 rounded-xl font-bold hover:bg-green-700 transition-all shadow-md flex items-center gap-2 justify-center">
            <Search size={16} /> Find Buyers
          </button>
        </div>
      </div>

      {loading && <Spinner />}

      {/* Buyer Cards */}
      {!loading && buyers.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {buyers.map((b, i) => (
            <div key={i} className="bg-white rounded-2xl shadow-md p-5 border border-gray-100 hover:shadow-lg transition-all">
              <div className="flex items-start justify-between mb-3">
                <h4 className="font-bold text-gray-800">{b.buyer_name}</h4>
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-semibold capitalize">{b.buyer_type}</span>
              </div>
              <div className="space-y-2 text-sm text-gray-800">
                <div className="flex items-center gap-2"><MapPin size={14} className="text-green-500" />{b.location}, {b.state}</div>
                <div className="flex items-center gap-2"><Building2 size={14} className="text-blue-500" />Capacity: {b.annual_capacity}</div>
                <div className="flex items-center gap-2"><Phone size={14} className="text-purple-500" />{b.phone_number}</div>
                <div className="flex items-center gap-2"><Mail size={14} className="text-orange-500" />{b.email}</div>
                {b.distance > 0 && (
                  <div className="flex items-center gap-2 font-semibold text-green-700">
                    <Target size={14} />{b.distance} km away
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
      {!loading && buyers.length === 0 && <EmptyState message="No buyers found. Try different product or location." />}
    </div>
  );
};

// ─── SECTION: LOAN CALCULATOR ────────────────────────────────
const LoanCalculatorTab = () => {
  const [form, setForm] = useState({ total_investment: 500000, own_capital: 150000, interest_rate: 9.0, loan_duration_months: 60 });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculate = () => {
    setLoading(true);
    axios.post(`${API}/loan-calculator`, form)
      .then(r => setResult(r.data))
      .catch(() => setResult(null))
      .finally(() => setLoading(false));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
        <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2"><Banknote size={20} className="text-green-600" />Loan Details</h3>
        <div className="space-y-3">
          <NumInput label="Total Investment (₹)" value={form.total_investment} onChange={v => setForm({ ...form, total_investment: v })} />
          <NumInput label="Own Capital (₹)" value={form.own_capital} onChange={v => setForm({ ...form, own_capital: v })} />
          <NumInput label="Interest Rate (%)" value={form.interest_rate} onChange={v => setForm({ ...form, interest_rate: v })} step={0.5} />
          <NumInput label="Duration (months)" value={form.loan_duration_months} onChange={v => setForm({ ...form, loan_duration_months: v })} />
          <button onClick={calculate} disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-bold shadow-md hover:shadow-lg transition-all mt-2">
            {loading ? <Loader2 className="animate-spin mx-auto" size={20} /> : '💰 Calculate EMI'}
          </button>
        </div>
      </div>

      <div className="lg:col-span-2 space-y-6">
        {result ? (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <KpiCard label="Loan Required" value={`₹${(result.loan_required / 100000).toFixed(1)}L`} color="blue" icon={<Banknote size={18} />} />
              <KpiCard label="Monthly EMI" value={`₹${result.monthly_emi.toLocaleString()}`} color="green" icon={<BadgeIndianRupee size={18} />} />
              <KpiCard label="Total Interest" value={`₹${(result.total_interest / 1000).toFixed(0)}K`} color="orange" icon={<TrendingUp size={18} />} />
              <KpiCard label="Total Repayment" value={`₹${(result.total_repayment / 100000).toFixed(1)}L`} color="purple" icon={<Target size={18} />} />
            </div>
            {/* EMI Chart */}
            <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
              <h4 className="font-bold text-gray-800 mb-4">EMI Schedule (First 12 Months)</h4>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={result.emi_schedule}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 11 }} tickFormatter={v => `${(v / 1000).toFixed(0)}K`} />
                  <Tooltip formatter={v => `₹${v.toLocaleString()}`} />
                  <Bar dataKey="principal" stackId="a" fill="#059669" name="Principal" radius={[0, 0, 0, 0]} />
                  <Bar dataKey="interest" stackId="a" fill="#d97706" name="Interest" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            {/* Government Schemes */}
            {result.eligible_schemes?.length > 0 && (
              <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-2xl p-6 border border-amber-100">
                <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2"><ShieldCheck size={18} className="text-amber-600" />Eligible Government Schemes</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {result.eligible_schemes.map((s, i) => (
                    <div key={i} className="bg-white p-4 rounded-xl border border-amber-100 shadow-sm">
                      <h5 className="font-bold text-sm text-gray-800">{s.name}</h5>
                      <p className="text-xs text-gray-800 mt-1">{s.benefit}</p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-xs font-semibold text-amber-700">Max: {s.max_amount}</span>
                        <a href={s.link} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-600 hover:underline flex items-center gap-1">Apply <ArrowUpRight size={10} /></a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-12 text-center border border-blue-100">
            <Banknote size={48} className="mx-auto text-blue-300 mb-4" />
            <p className="text-gray-700 text-lg">Enter your investment details and click <strong>Calculate EMI</strong>.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// ─── SECTION: EXPORT INSIGHTS ────────────────────────────────
const ExportInsightsTab = ({ crop }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API}/export-opportunities`, { params: { crop } })
      .then(r => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [crop]);

  if (loading) return <Spinner />;
  if (!data || !data.top_destinations?.length) return <EmptyState message={`No export data for ${crop}.`} />;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KpiCard label="Overall Demand" value={data.overall_demand} color="green" icon={<Globe2 size={18} />} />
        <KpiCard label="Price Range" value={data.price_range_per_kg} color="blue" icon={<BadgeIndianRupee size={18} />} />
        <KpiCard label="Total Export Value" value={`₹${data.total_export_value_lakhs}L`} color="emerald" icon={<TrendingUp size={18} />} />
        <KpiCard label="Markets" value={`${data.top_destinations.length} countries`} color="purple" icon={<MapPin size={18} />} />
      </div>

      <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-100">
        <h4 className="font-bold text-gray-800 mb-1">{data.product_name} — Export Destinations</h4>
        <p className="text-sm text-gray-700 mb-4">{data.insight}</p>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.top_destinations} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis type="number" tick={{ fontSize: 11 }} tickFormatter={v => `₹${v}L`} />
            <YAxis dataKey="country" type="category" tick={{ fontSize: 12 }} width={100} />
            <Tooltip formatter={v => `₹${v} Lakhs`} />
            <Bar dataKey="value_lakhs" fill="#059669" radius={[0, 4, 4, 0]} name="Export Value" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Certifications */}
      {data.certifications?.length > 0 && (
        <div className="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-2xl p-6 border border-blue-100">
          <h4 className="font-bold text-gray-800 mb-3">Required Certifications</h4>
          <div className="flex flex-wrap gap-2">
            {data.certifications.map((c, i) => (
              <span key={i} className="px-3 py-1.5 bg-white border border-blue-200 rounded-full text-sm font-medium text-blue-700 shadow-sm">{c}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ─── SECTION: SUCCESS STORIES ────────────────────────────────
const SuccessStoriesTab = ({ crop }) => {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get(`${API}/success-stories`)
      .then(r => setStories(r.data.stories || []))
      .catch(() => setStories([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {stories.map((s, i) => {
        let steps = [];
        try { steps = JSON.parse(s.implementation_steps); } catch { }
        let schemes = [];
        try { schemes = JSON.parse(s.schemes_used); } catch { }
        return (
          <div key={i} className="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden hover:shadow-xl transition-all">
            <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-5 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold">{s.farmer_name}</h3>
                  <p className="text-green-100 text-sm flex items-center gap-1"><MapPin size={12} />{s.location}, {s.state}</p>
                </div>
                <div className="bg-white/20 px-3 py-1.5 rounded-full text-sm font-bold">{s.crop}</div>
              </div>
              <p className="text-white/90 text-sm mt-2 font-semibold">{s.business_type}</p>
            </div>

            <div className="p-5 space-y-4">
              <div className="grid grid-cols-3 gap-3">
                <div className="text-center p-2 bg-green-50 rounded-xl">
                  <p className="text-xs text-gray-700">Investment</p>
                  <p className="font-bold text-green-700 text-sm">{s.investment}</p>
                </div>
                <div className="text-center p-2 bg-blue-50 rounded-xl">
                  <p className="text-xs text-gray-700">Revenue/mo</p>
                  <p className="font-bold text-blue-700 text-sm">{s.monthly_revenue}</p>
                </div>
                <div className="text-center p-2 bg-purple-50 rounded-xl">
                  <p className="text-xs text-gray-700">Annual Profit</p>
                  <p className="font-bold text-purple-700 text-sm">{s.annual_profit}</p>
                </div>
              </div>

              <p className="text-sm text-gray-800">{s.story}</p>

              {steps.length > 0 && (
                <div>
                  <h5 className="text-xs font-bold text-gray-700 uppercase mb-2">Implementation Steps</h5>
                  <div className="space-y-1.5">
                    {steps.map((step, j) => (
                      <div key={j} className="flex items-start gap-2">
                        <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                          <span className="text-[10px] font-bold text-green-700">{j + 1}</span>
                        </div>
                        <p className="text-xs text-gray-800">{step}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {schemes.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {schemes.map((sc, j) => (
                    <span key={j} className="text-xs bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-full font-medium">{sc}</span>
                  ))}
                </div>
              )}

              {s.contact_phone && (
                <div className="pt-2 border-t border-gray-100 flex items-center gap-4 text-xs text-gray-700">
                  <span className="flex items-center gap-1"><Phone size={12} />{s.contact_phone}</span>
                  {s.year_started && <span>Started: {s.year_started}</span>}
                </div>
              )}
            </div>
          </div>
        );
      })}
      {stories.length === 0 && <EmptyState message="No success stories found." />}
    </div>
  );
};

// ─── SHARED COMPONENTS ───────────────────────────────────────
const Spinner = () => (
  <div className="flex justify-center py-16">
    <div className="animate-spin h-10 w-10 border-4 border-green-500 border-t-transparent rounded-full" />
  </div>
);

const EmptyState = ({ message }) => (
  <div className="text-center py-16 text-gray-600 col-span-full">
    <Search size={40} className="mx-auto mb-3 opacity-90" />
    <p className="text-lg">{message}</p>
  </div>
);

const InfoChip = ({ icon, label, value, color }) => (
  <div className={`bg-${color}-50 p-2 rounded-lg border border-${color}-100`}>
    <p className="text-[10px] text-gray-700 flex items-center gap-1">{icon}{label}</p>
    <p className="font-bold text-sm text-gray-800">{value}</p>
  </div>
);

const KpiCard = ({ label, value, color, icon }) => (
  <div className={`bg-${color}-50 p-4 rounded-2xl border border-${color}-100 shadow-sm`}>
    <div className={`text-${color}-600 mb-1`}>{icon}</div>
    <p className="text-xs text-gray-700">{label}</p>
    <p className={`text-xl font-bold text-${color}-700`}>{value}</p>
  </div>
);

const NumInput = ({ label, value, onChange, step = 1 }) => (
  <div>
    <label className="text-xs font-semibold text-gray-800 block mb-1">{label}</label>
    <input type="number" value={value} step={step} onChange={e => onChange(Number(e.target.value))}
      className="w-full px-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-green-500 bg-gray-50" />
  </div>
);

export default VentureEngine;
