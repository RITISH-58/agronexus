import React, { useState } from 'react';
import { Leaf, MapPin, Droplets, Calendar, Ruler, TrendingUp, Loader2, ChevronLeft, Sprout } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { API_BASE_URL } from '../config/api';


const CropPlanForm = () => {
    const { token } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({
        crop_type: '', soil_type: 'Loamy', season: 'Kharif',
        land_acres: '', water_source: 'Medium', location: '', sowing_date: '',
        nitrogen_level: '', phosphorus_level: '', potassium_level: '', soil_ph: ''
    });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault(); setError(''); setLoading(true);
        try {
            const payload = {
                ...formData,
                land_acres: parseFloat(formData.land_acres),
                nitrogen_level: formData.nitrogen_level ? parseFloat(formData.nitrogen_level) : null,
                phosphorus_level: formData.phosphorus_level ? parseFloat(formData.phosphorus_level) : null,
                potassium_level: formData.potassium_level ? parseFloat(formData.potassium_level) : null,
                soil_ph: formData.soil_ph ? parseFloat(formData.soil_ph) : null,
            };
            const response = await fetch(`${API_BASE_URL}/api/crop-plans`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload),
            });
            if (response.ok) { const data = await response.json(); navigate(`/crop-dashboard/${data.plan_id}`); }
            else { const data = await response.json(); setError(data.detail || "Failed to create plan."); }
        } catch { setError("Unable to create crop plan."); }
        finally { setLoading(false); }
    };

    return (
        <div className="min-h-screen px-4 pt-6 pb-4 max-w-lg mx-auto space-y-5 animate-fade-in">
            {/* Header */}
            <div className="flex items-center gap-3">
                <Link to="/" className="w-10 h-10 bg-white rounded-2xl shadow-card flex items-center justify-center active:scale-90 transition-transform">
                    <ChevronLeft size={20} className="text-dark" />
                </Link>
                <div>
                    <h1 className="text-xl font-extrabold text-dark tracking-tight">New Crop Plan</h1>
                    <p className="text-xs text-muted">AI-powered crop intelligence</p>
                </div>
            </div>

            {/* Hero */}
            <div className="img-card rounded-3xl h-32 overflow-hidden">
                <img src="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800&q=80" alt="Farmland" className="w-full h-full object-cover" />
                <div className="absolute inset-0 bg-gradient-to-t from-leaf-800/90 to-transparent z-[1]" />
                <div className="absolute bottom-0 left-0 right-0 z-10 p-4">
                    <p className="text-white font-extrabold text-lg">Plan → Predict → Profit 🌾</p>
                    <p className="text-white text-xs mt-0.5">ML-based yield, fertilizer & risk analysis</p>
                </div>
            </div>

            {error && (
                <div className="bg-red-100 text-red-600 p-3 rounded-2xl text-sm font-medium">{error}</div>
            )}

            {/* Form Cards */}
            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Crop Details */}
                <div className="bg-white rounded-3xl shadow-card p-5 space-y-3">
                    <p className="text-xs font-bold text-muted uppercase tracking-wider flex items-center gap-1.5">
                        <Leaf size={12} className="text-leaf-500" /> Crop Details
                    </p>
                    <div>
                        <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Crop Type</label>
                        <input type="text" name="crop_type" required placeholder="e.g. Rice, Cotton, Wheat"
                            className="input-mobile text-sm" value={formData.crop_type} onChange={handleChange} />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Soil Type</label>
                            <select name="soil_type" className="input-mobile text-sm py-3" value={formData.soil_type} onChange={handleChange}>
                                <option value="Loamy">Loamy</option>
                                <option value="Clay">Clay</option>
                                <option value="Sandy">Sandy</option>
                                <option value="Alluvial">Alluvial</option>
                                <option value="Black">Black</option>
                                <option value="Red">Red</option>
                            </select>
                        </div>
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Season</label>
                            <select name="season" className="input-mobile text-sm py-3" value={formData.season} onChange={handleChange}>
                                <option value="Kharif">Kharif</option>
                                <option value="Rabi">Rabi</option>
                                <option value="Summer">Zaid</option>
                                <option value="Perennial">Perennial</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Location & Environment */}
                <div className="bg-white rounded-3xl shadow-card p-5 space-y-3">
                    <p className="text-xs font-bold text-muted uppercase tracking-wider flex items-center gap-1.5">
                        <MapPin size={12} className="text-olive-500" /> Location & Environment
                    </p>
                    <div>
                        <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Location</label>
                        <input type="text" name="location" required placeholder="City, State"
                            className="input-mobile text-sm" value={formData.location} onChange={handleChange} />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Land (acres)</label>
                            <input type="number" step="0.1" min="0" name="land_acres" required placeholder="0.0"
                                className="input-mobile text-sm" value={formData.land_acres} onChange={handleChange} />
                        </div>
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Sowing Date</label>
                            <input type="date" name="sowing_date" required
                                className="input-mobile text-sm" value={formData.sowing_date} onChange={handleChange} />
                        </div>
                    </div>
                    <div>
                        <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Water Availability</label>
                        <select name="water_source" className="input-mobile text-sm py-3" value={formData.water_source} onChange={handleChange}>
                            <option value="High">High (Canal/Tube Well)</option>
                            <option value="Medium">Medium (Seasonal)</option>
                            <option value="Low">Low (Rainfed)</option>
                        </select>
                    </div>
                </div>

                {/* Soil Analysis (Optional — boosts ML accuracy) */}
                <div className="bg-white rounded-3xl shadow-card p-5 space-y-3">
                    <p className="text-xs font-bold text-muted uppercase tracking-wider flex items-center gap-1.5">
                        <Sprout size={12} className="text-green-600" /> Soil Analysis
                        <span className="text-[9px] text-gray-600 normal-case font-medium ml-auto">Optional • Improves AI accuracy</span>
                    </p>
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Nitrogen (N) kg/ha</label>
                            <input type="number" step="1" min="0" max="300" name="nitrogen_level" placeholder="e.g. 80"
                                className="input-mobile text-sm" value={formData.nitrogen_level} onChange={handleChange} />
                        </div>
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Phosphorus (P) kg/ha</label>
                            <input type="number" step="1" min="0" max="200" name="phosphorus_level" placeholder="e.g. 40"
                                className="input-mobile text-sm" value={formData.phosphorus_level} onChange={handleChange} />
                        </div>
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Potassium (K) kg/ha</label>
                            <input type="number" step="1" min="0" max="250" name="potassium_level" placeholder="e.g. 40"
                                className="input-mobile text-sm" value={formData.potassium_level} onChange={handleChange} />
                        </div>
                        <div>
                            <label className="text-[10px] font-bold text-muted uppercase tracking-wider mb-1 block">Soil pH</label>
                            <input type="number" step="0.1" min="3" max="10" name="soil_ph" placeholder="e.g. 6.5"
                                className="input-mobile text-sm" value={formData.soil_ph} onChange={handleChange} />
                        </div>
                    </div>
                    <p className="text-[10px] text-gray-600 leading-snug">
                        💡 Get these values from your soil test report. If left blank, AI will use regional averages.
                    </p>
                </div>

                <button type="submit" disabled={loading}
                    className="btn-primary w-full flex items-center justify-center gap-2">
                    {loading ? <Loader2 className="animate-spin" size={18} /> : <TrendingUp size={18} />}
                    {loading ? 'Generating Dashboard...' : 'Generate AI Dashboard'}
                </button>
            </form>
        </div>
    );
};

export default CropPlanForm;
