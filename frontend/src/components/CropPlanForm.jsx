import React, { useState } from 'react';
import {
    Droplets, Layers, Sun, Sprout, PaintBucket, CloudRain,
    MapPin, Calendar, Ruler, CheckCircle2, ChevronRight, ChevronLeft, Loader2, Zap
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import { API_BASE_URL } from '../config/api';

const steps = [
    {
        id: 'water_retention',
        title: 'Water Retention',
        question: 'After watering or rain, how long does water stay in your field?',
        icon: Droplets,
        options: [
            { label: 'Stays for long time', value: 'Stays for long time' },
            { label: 'Drains quickly', value: 'Drains quickly' },
            { label: 'Moderate', value: 'Moderate' }
        ]
    },
    {
        id: 'soil_texture',
        title: 'Soil Texture',
        question: 'When you touch wet soil, how does it feel?',
        icon: Layers,
        options: [
            { label: 'Sticky and forms a ball', value: 'Sticky and forms a ball' },
            { label: 'Loose and gritty', value: 'Loose and gritty' },
            { label: 'Soft and crumbly', value: 'Soft and crumbly' }
        ]
    },
    {
        id: 'cracking_behavior',
        title: 'Cracking Behavior',
        question: 'Does your soil develop cracks during summer?',
        icon: Sun,
        options: [
            { label: 'Yes, large cracks', value: 'Yes, large cracks' },
            { label: 'Small cracks', value: 'Small cracks' },
            { label: 'No cracks', value: 'No cracks' }
        ]
    },
    {
        id: 'water_req',
        title: 'Water Requirement',
        question: 'Do your crops need frequent watering?',
        icon: Droplets,
        options: [
            { label: 'Yes', value: 'Yes' },
            { label: 'No', value: 'No' },
            { label: 'Sometimes', value: 'Sometimes' }
        ]
    },
    {
        id: 'crop_perf',
        title: 'Crop Performance',
        question: 'Which crops grow best in your field?',
        icon: Sprout,
        options: [
            { label: 'Paddy', value: 'Paddy' },
            { label: 'Groundnut', value: 'Groundnut' },
            { label: 'Vegetables', value: 'Vegetables' },
            { label: 'Others', value: 'Others' }
        ]
    },
    {
        id: 'soil_color',
        title: 'Soil Color',
        question: 'What is the color of your soil?',
        icon: PaintBucket,
        options: [
            { label: 'Black', value: 'Black' },
            { label: 'Red', value: 'Red' },
            { label: 'Light brown', value: 'Light brown' },
            { label: 'Other', value: 'Other' }
        ]
    },
    {
        id: 'rain_behavior',
        title: 'Rain Behavior',
        question: 'After heavy rain, what happens to your field?',
        icon: CloudRain,
        options: [
            { label: 'Water gets logged', value: 'Water gets logged' },
            { label: 'Drains quickly', value: 'Drains quickly' },
            { label: 'Stays moist', value: 'Stays moist' }
        ]
    }
];

const CropPlanForm = () => {
    const { token } = useAuth();
    const navigate = useNavigate();
    const { t } = useTranslation();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);

    // Core state
    const [formData, setFormData] = useState({
        water_retention: '', soil_texture: '', cracking_behavior: '',
        water_req: '', crop_perf: '', soil_color: '', rain_behavior: '',
        location: '', previous_crop: '', crop_type: '', land_acres: '', sowing_date: '',
        nitrogen_level: '', phosphorus_level: '', potassium_level: '', soil_ph: ''
    });

    const handleOptionSelect = (fieldId, value) => {
        setFormData(prev => ({ ...prev, [fieldId]: value }));
    };

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const submitPlan = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setLoading(true);
        try {
            const payload = { 
                crop: formData.crop_type,
                previous_crop: formData.previous_crop || "rice",
                land_size: parseFloat(formData.land_acres) || 1.0,
            };
            
            const response = await fetch(`${API_BASE_URL}/api/crop-intel`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(payload),
            });
            
            const data = await response.json();
            console.log("API Response:", data);
            
            if (response.ok) {
                setResult({
                  yield: data.yield_per_acre,
                  total: data.total_harvest,
                  price: data.market_price,
                  trend: data.trend,
                  forecast: data.forecast,
                  confidence: data.confidence,
                  soil: data.soil_profile
                });
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                setError(data.error || data.detail || "Invalid crop input");
            }
        } catch {
            setError("Network Error. Cannot connect to AgroNexus AI.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50/50 flex flex-col max-w-lg mx-auto pb-32">
            {/* Header */}
            <div className="bg-white px-4 py-4 sticky top-0 z-20 shadow-sm flex items-center gap-3">
                <button
                    type="button"
                    onClick={() => navigate(-1)}
                    className="w-10 h-10 bg-gray-50 rounded-xl flex items-center justify-center text-gray-600 active:scale-90 transition-transform"
                >
                    <ChevronLeft size={20} />
                </button>
                <div>
                    <h1 className="text-lg font-black text-gray-800 leading-none tracking-tight">Farm Analysis</h1>
                    <p className="text-[10px] text-green-600 font-bold tracking-wide">SMART SOIL DETECTION ENABLED</p>
                </div>
            </div>

            {/* Content Area */}
            <div className="px-3 pt-4">
                {result ? (
                    <div className="bg-white p-5 rounded-3xl shadow-sm border border-gray-100 mb-6 animate-fade-in mx-1">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-black text-gray-800">Intelligence Report</h2>
                            <span className="text-[10px] font-black tracking-widest bg-green-100 text-green-700 px-2 py-1 rounded-md">{result.confidence} CONFIDENCE</span>
                        </div>
                        <div className="grid grid-cols-2 gap-3 pb-4 border-b border-gray-50 mb-4">
                            <div className="bg-leaf-50 p-3 rounded-2xl border-2 border-leaf-100">
                                <p className="text-[10px] font-bold text-leaf-600 uppercase tracking-widest mb-1">Yield / Acre</p>
                                <p className="text-xl font-black text-leaf-800 leading-none">{result.yield}</p>
                            </div>
                            <div className="bg-blue-50 p-3 rounded-2xl border-2 border-blue-100">
                                <p className="text-[10px] font-bold text-blue-600 uppercase tracking-widest mb-1">Total Harvest</p>
                                <p className="text-xl font-black text-blue-800 leading-none">{result.total}</p>
                            </div>
                            <div className="bg-amber-50 p-3 rounded-2xl border-2 border-amber-100">
                                <p className="text-[10px] font-bold text-amber-600 uppercase tracking-widest mb-1">Target Price</p>
                                <p className="text-xl font-black text-amber-800 leading-none">{result.price}</p>
                            </div>
                            <div className="bg-purple-50 p-3 rounded-2xl border-2 border-purple-100">
                                <p className="text-[10px] font-bold text-purple-600 uppercase tracking-widest mb-1">Market Trend</p>
                                <p className="text-lg font-black text-purple-800 leading-tight">{result.trend}</p>
                                <p className="text-[9px] font-bold text-purple-600 mt-1 uppercase truncate">{result.forecast}</p>
                            </div>
                        </div>
                        <button type="button" onClick={() => setResult(null)} className="w-full bg-gray-50 text-gray-700 hover:bg-gray-100 hover:text-gray-900 border border-gray-100 font-extrabold py-3 rounded-xl transition-colors active:scale-95 text-sm tracking-wide">
                            Recalculate Another Field
                        </button>
                    </div>
                ) : (
                    <>
                        <div className="bg-green-50 border border-green-100/50 rounded-2xl p-3 mb-4 shadow-sm flex items-start gap-2.5">
                            <Sprout className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                            <p className="text-xs text-green-800 font-medium leading-relaxed">
                                {t('smart_soil_note', 'Answer a few simple questions to analyze your soil automatically and optimize your yield predictions.')}
                            </p>
                        </div>

                <form id="farm-analysis-form" onSubmit={submitPlan} className="grid grid-cols-2 gap-3 pb-8 animate-fade-in">

                    {/* Basic Info Block */}
                    <div className="col-span-2 space-y-3 mb-2">
                        {/* Location */}
                        <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100 col-span-2">
                            <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
                                <MapPin size={12} /> {t('location', 'Location')}
                            </label>
                            <input type="text" name="location" required placeholder="e.g. Hyderabad, Telangana"
                                className="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-4 py-3 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none transition-shadow"
                                value={formData.location} onChange={handleInputChange} />
                        </div>

                        {/* Split Row 1 */}
                        <div className="grid grid-cols-2 gap-3 col-span-2">
                            <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100 relative">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
                                    <Sprout size={12} /> {t('target_crop', 'Target Crop')}
                                </label>
                                <input type="text" name="crop_type" required placeholder="Enter crop (e.g., rice, cotton)"
                                    className={`w-full bg-gray-50/50 border ${error?.includes('Invalid') ? 'border-red-300 focus:ring-red-400' : 'border-gray-100 focus:ring-leaf-500'} rounded-xl px-3 py-3 text-sm font-semibold outline-none transition-shadow relative z-20`}
                                    value={formData.crop_type} onChange={handleInputChange} />
                                
                                {error && error.includes('Invalid') && (
                                    <div className="absolute top-[85px] left-0 w-full bg-red-50 border border-red-200 rounded-xl p-3 shadow-lg z-30 animate-fade-in">
                                        <p className="text-xs font-bold text-red-600 flex items-center gap-1.5 mb-1.5">
                                            <span>⚠️</span> {error}
                                        </p>
                                        <p className="text-[10px] font-semibold text-red-500/80 leading-relaxed">
                                            Supported crops: rice, cotton, groundnut, maize, wheat, sugarcane, tomato, potato
                                        </p>
                                    </div>
                                )}
                            </div>
                            <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
                                    <Layers size={12} /> {t('previous_crop', 'Previous Crop')}
                                </label>
                                <input type="text" name="previous_crop" placeholder="e.g. Groundnut"
                                    className="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-3 py-3 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none transition-shadow"
                                    value={formData.previous_crop} onChange={handleInputChange} />
                            </div>
                        </div>

                        {/* Split Row 2 */}
                        <div className="grid grid-cols-2 gap-3 col-span-2">
                            <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
                                    <Ruler size={12} /> {t('land_acres', 'Land (Acres)')}
                                </label>
                                <input type="number" step="0.1" min="0.1" name="land_acres" required placeholder="1.5"
                                    className="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-3 py-3 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none transition-shadow"
                                    value={formData.land_acres} onChange={handleInputChange} />
                            </div>
                            <div className="bg-white p-3 rounded-2xl shadow-sm border border-gray-100">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
                                    <Calendar size={12} /> {t('sowing_date', 'Sowing Date')}
                                </label>
                                <input type="date" name="sowing_date" required
                                    className="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-3 py-3 text-sm font-semibold text-gray-700 focus:ring-2 focus:ring-leaf-500 outline-none transition-shadow"
                                    value={formData.sowing_date} onChange={handleInputChange} />
                            </div>
                        </div>
                    </div>

                    <div className="col-span-2 h-4" /> {/* Spacer */}

                    {/* Observational Questions Mapped to Grid */}
                    {steps.map((step) => {
                        const StepIcon = step.icon;
                        return (
                            <div key={step.id} className="col-span-2 bg-white p-4 rounded-3xl shadow-sm border border-gray-100">
                                <div className="flex items-center gap-2 mb-3">
                                    <div className="p-1.5 bg-leaf-50 rounded-lg">
                                        <StepIcon size={16} className="text-leaf-600" />
                                    </div>
                                    <h3 className="text-sm font-extrabold text-gray-800 leading-tight pr-2">{t(step.id, step.question)}</h3>
                                </div>
                                <div className={`grid gap-2 ${step.options.length > 3 ? 'grid-cols-2' : 'grid-cols-3'}`}>
                                    {step.options.map((option, idx) => {
                                        const isSelected = formData[step.id] === option.value;
                                        return (
                                            <button
                                                key={idx}
                                                type="button"
                                                onClick={() => handleOptionSelect(step.id, option.value)}
                                                className={`p-3 rounded-2xl border-2 transition-all active:scale-95 flex items-center justify-center text-center shadow-sm select-none
                                                    ${isSelected ? 'border-leaf-500 bg-leaf-50/50 text-leaf-800' : 'border-gray-50 bg-gray-50 hover:border-gray-200 hover:bg-white text-gray-600'}`}
                                            >
                                                <span className="text-[11px] font-black leading-snug">
                                                    {t(option.value, option.label)}
                                                </span>
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>
                        );
                    })}

                    <div className="col-span-2 h-4" /> {/* Spacer */}

                    {/* Optional Soil Analysis */}
                    <div className="col-span-2 bg-white p-4 rounded-3xl shadow-sm border border-gray-100">
                        <div className="flex items-center justify-between mb-3 border-b border-gray-50 pb-2">
                            <div className="flex items-center gap-2">
                                <Layers size={16} className="text-gray-400" />
                                <h3 className="text-sm font-extrabold text-gray-700 tracking-tight">Technical Soil Analysis</h3>
                            </div>
                            <span className="text-[9px] font-bold text-gray-400 uppercase tracking-widest bg-gray-50 px-2 py-1 rounded-md">Optional</span>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            <div className="bg-gray-50/50 p-2.5 rounded-2xl border border-gray-50">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 flex items-center gap-1.5">N (kg/ha)</label>
                                <input type="number" step="1" name="nitrogen_level" placeholder="e.g. 80"
                                    className="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none"
                                    value={formData.nitrogen_level} onChange={handleInputChange} />
                            </div>
                            <div className="bg-gray-50/50 p-2.5 rounded-2xl border border-gray-50">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 flex items-center gap-1.5">P (kg/ha)</label>
                                <input type="number" step="1" name="phosphorus_level" placeholder="e.g. 40"
                                    className="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none"
                                    value={formData.phosphorus_level} onChange={handleInputChange} />
                            </div>
                            <div className="bg-gray-50/50 p-2.5 rounded-2xl border border-gray-50">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 flex items-center gap-1.5">K (kg/ha)</label>
                                <input type="number" step="1" name="potassium_level" placeholder="e.g. 40"
                                    className="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none"
                                    value={formData.potassium_level} onChange={handleInputChange} />
                            </div>
                            <div className="bg-gray-50/50 p-2.5 rounded-2xl border border-gray-50">
                                <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 flex items-center gap-1.5">Soil pH</label>
                                <input type="number" step="0.1" name="soil_ph" placeholder="e.g. 6.5"
                                    className="w-full bg-white border border-gray-100 rounded-xl px-3 py-2 text-sm font-semibold focus:ring-2 focus:ring-leaf-500 outline-none"
                                    value={formData.soil_ph} onChange={handleInputChange} />
                            </div>
                        </div>
                    </div>

                    {error && !error.includes('Invalid') && (
                        <div className="col-span-2 bg-red-50 text-red-600 p-4 rounded-2xl text-sm font-bold border border-red-100 shadow-sm mt-2 animate-fade-in">
                            {error}
                        </div>
                    )}
                </form>
                    </>
                )}
            </div>

            {/* Relative Submit Footer to ensure scroll clearance */}
            {!result && (
                <div className="mt-4 px-3 pb-32 flex justify-center w-full">
                    <div className="w-full max-w-lg">
                        <button
                            type="submit"
                            form="farm-analysis-form"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-leaf-600 to-leaf-500 hover:from-leaf-700 hover:to-leaf-600 text-white font-black py-4 rounded-[1.35rem] shadow-[0_8px_20px_rgba(46,125,50,0.35)] flex items-center justify-center gap-2.5 active:scale-95 transition-all text-[15px] tracking-wide"
                        >
                            {loading ? <Loader2 className="animate-spin text-white/90" size={20} /> : <Zap size={20} className="text-white fill-white/20" />}
                            {loading ? t('analyzing', 'Analyzing Farm...') : t('analyze_farm', 'Analyze My Farm')}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CropPlanForm;
