import React, { useState } from 'react';
import axios from 'axios';
import { ChevronLeft, Loader2, Sprout, Landmark, Briefcase, ChevronRight } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';

const Schemes = () => {
  const navigate = useNavigate();
  const API_BASE = `${API_BASE_URL}/api`;

  const [formData, setFormData] = useState({
    soil_type: 'black', nitrogen: 40.0, phosphorus: 30.0, potassium: 25.0,
    ph_level: 7.2, land_size: 3.5, water_availability: 'medium',
    state: 'Telangana', district: 'Warangal'
  });
  const [schemes, setSchemes] = useState([]);
  const [crops, setCrops] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('schemes');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    const numericFields = ['nitrogen', 'phosphorus', 'potassium', 'ph_level', 'land_size'];
    setFormData(prev => ({ ...prev, [name]: numericFields.includes(name) ? parseFloat(value) || 0 : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); setError(null);
    setSchemes([]); setCrops([]); setOpportunities([]);
    try {
      const schemeRes = await axios.post(`${API_BASE}/scheme-recommendation`, {
        soil_type: formData.soil_type, land_size: formData.land_size,
        water_availability: formData.water_availability, state: formData.state, district: formData.district
      });
      setSchemes(schemeRes.data.recommended_schemes || []);

      const cropRes = await axios.post(`${API_BASE}/crop-recommendation`, {
        soil_type: formData.soil_type, nitrogen: formData.nitrogen, phosphorus: formData.phosphorus,
        potassium: formData.potassium, ph_level: formData.ph_level,
        water_availability: formData.water_availability, state: formData.state
      });
      const recommendedCrops = cropRes.data.recommended_crops || [];
      setCrops(recommendedCrops);

      if (recommendedCrops.length > 0) {
        const entRes = await axios.post(`${API_BASE}/agro-entrepreneur-opportunities`, {
          recommended_crops: recommendedCrops.map(c => c.crop_name)
        });
        setOpportunities(entRes.data.entrepreneur_opportunities || []);
      }
    } catch (err) {
      setError("Failed to fetch. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { key: 'schemes', label: 'Schemes', count: schemes.length, icon: Landmark },
    { key: 'crops', label: 'Crops', count: crops.length, icon: Sprout },
    { key: 'entrepreneur', label: 'Business', count: opportunities.length, icon: Briefcase },
  ];

  const hasResults = schemes.length > 0 || crops.length > 0 || opportunities.length > 0;

  return (
    <div className="min-h-screen px-4 pt-6 pb-4 max-w-lg mx-auto space-y-5 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link to="/" className="w-10 h-10 bg-white rounded-2xl shadow-card flex items-center justify-center active:scale-90 transition-transform">
          <ChevronLeft size={20} className="text-dark" />
        </Link>
        <div>
          <h1 className="text-xl font-extrabold text-dark tracking-tight">Govt Schemes</h1>
          <p className="text-xs text-muted">Find matching subsidies & programs</p>
        </div>
      </div>

      {/* Hero */}
      <div className="bg-gradient-to-r from-olive-500 to-leaf-600 rounded-3xl p-5 text-white">
        <p className="text-sm font-medium text-white mb-1">🏛️ Smart Recommendation Engine</p>
        <p className="text-lg font-extrabold">Enter your farm details to find the best schemes, crops & business opportunities</p>
      </div>

      {/* Form Card */}
      <div className="bg-white rounded-3xl shadow-card p-5 space-y-4">
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Soil Type</label>
              <select name="soil_type" value={formData.soil_type} onChange={handleInputChange} className="input-mobile text-sm py-3">
                <option value="black">Black</option>
                <option value="red">Red</option>
                <option value="alluvial">Alluvial</option>
                <option value="laterite">Laterite</option>
                <option value="desert">Sandy</option>
              </select>
            </div>
            <div>
              <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Land (acres)</label>
              <input type="number" step="0.1" name="land_size" value={formData.land_size} onChange={handleInputChange} className="input-mobile text-sm py-3" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Water</label>
              <select name="water_availability" value={formData.water_availability} onChange={handleInputChange} className="input-mobile text-sm py-3">
                <option value="good">Good</option>
                <option value="medium">Medium</option>
                <option value="poor">Poor</option>
              </select>
            </div>
            <div>
              <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">State</label>
              <select name="state" value={formData.state} onChange={handleInputChange} className="input-mobile text-sm py-3">
                {['Telangana','Andhra Pradesh','Maharashtra','Karnataka','Tamil Nadu','Madhya Pradesh','Uttar Pradesh','Punjab','Haryana','Rajasthan','Gujarat','Odisha','West Bengal','Bihar','Kerala'].map(s =>
                  <option key={s} value={s}>{s}</option>
                )}
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">District</label>
              <input type="text" name="district" value={formData.district} onChange={handleInputChange} className="input-mobile text-sm py-3" />
            </div>
            <div>
              <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">pH Level</label>
              <input type="number" step="0.1" name="ph_level" value={formData.ph_level} onChange={handleInputChange} className="input-mobile text-sm py-3" />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {['nitrogen','phosphorus','potassium'].map(n => (
              <div key={n}>
                <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">{n.charAt(0).toUpperCase()}</label>
                <input type="number" name={n} value={formData[n]} onChange={handleInputChange} className="input-mobile text-sm py-3" />
              </div>
            ))}
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center gap-2 mt-2">
            {loading ? <><Loader2 className="animate-spin" size={18} /> Analyzing...</> : 'Get Recommendations'}
          </button>
        </form>

        {error && <div className="bg-red-100 text-red-600 p-3 rounded-2xl text-sm font-medium">{error}</div>}
      </div>

      {/* Results */}
      {!loading && hasResults && (
        <div className="space-y-4 animate-fade-in-up">
          {/* Tabs */}
          <div className="flex gap-2 bg-cream-200/60 p-1 rounded-2xl">
            {tabs.map(tab => (
              <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                className={`flex-1 flex items-center justify-center gap-1 py-2.5 rounded-xl text-xs font-bold transition-all ${
                  activeTab === tab.key ? 'bg-white text-leaf-700 shadow-card' : 'text-muted'
                }`}>
                <tab.icon size={13} /> {tab.label} ({tab.count})
              </button>
            ))}
          </div>

          {/* Schemes Tab */}
          {activeTab === 'schemes' && schemes.map((s, i) => (
            <div key={i} className="bg-white rounded-3xl shadow-card p-4 space-y-2 active:scale-[0.98] transition-transform">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-olive-100 rounded-2xl flex items-center justify-center flex-shrink-0">
                  <Landmark size={18} className="text-olive-600" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-sm text-dark leading-tight">{s.name}</h3>
                  <p className="text-xs text-muted mt-1 leading-relaxed">{s.benefit || 'N/A'}</p>
                </div>
              </div>
              {s.link && (
                <a href={s.link} target="_blank" rel="noopener noreferrer"
                   className="w-full py-2.5 bg-leaf-50 text-leaf-700 text-xs font-bold rounded-xl flex items-center justify-center gap-1 hover:bg-leaf-100 transition-colors">
                  Apply Now <ChevronRight size={14} />
                </a>
              )}
            </div>
          ))}

          {/* Crops Tab */}
          {activeTab === 'crops' && (
            <div className="grid grid-cols-2 gap-3">
              {crops.map((c, i) => (
                <div key={i} className="bg-white rounded-3xl shadow-card p-4 text-center space-y-2">
                  <div className="w-10 h-10 bg-leaf-100 rounded-2xl flex items-center justify-center mx-auto">
                    <Sprout size={18} className="text-leaf-600" />
                  </div>
                  <p className="font-bold text-sm text-dark capitalize">{c.crop_name}</p>
                  <div className="w-full bg-cream-300 rounded-full h-1.5">
                    <div className="bg-leaf-500 h-1.5 rounded-full transition-all" style={{ width: `${c.suitability_score}%` }} />
                  </div>
                  <p className="text-[10px] text-leaf-700 font-bold">{c.suitability_score}% match</p>
                </div>
              ))}
            </div>
          )}

          {/* Business Tab */}
          {activeTab === 'entrepreneur' && opportunities.map((o, i) => (
            <div key={i} className="bg-gradient-to-br from-wheat-50 to-cream-200 rounded-3xl shadow-card p-4 space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-lg">💼</span>
                <h3 className="font-bold text-sm text-dark">{o.business_opportunity}</h3>
              </div>
              <p className="text-xs text-muted"><strong>Crop:</strong> {o.crop}</p>
              <p className="text-xs text-muted"><strong>Process:</strong> {o.processing_idea}</p>
              <div className="badge badge-green">💰 {o.expected_profit_potential}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Schemes;
