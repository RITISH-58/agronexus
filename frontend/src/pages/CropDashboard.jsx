import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
    ChevronLeft, Calendar, MapPin, Ruler, Droplets,
    Sprout, AlertTriangle, ShieldAlert, BarChart3,
    ShieldCheck, Lightbulb, ChevronDown, ChevronUp,
    TrendingUp, Eye, Zap, Layers
} from 'lucide-react';
import YieldPredictionCard from '../components/YieldPredictionCard';
import FertilizerCard from '../components/FertilizerCard';
import RiskReductionCard from '../components/RiskReductionCard';
import WeatherCard from '../components/WeatherCard';
import PestRiskCard from '../components/PestRiskCard';
import MarketTrendCard from '../components/MarketTrendCard';
import { useTranslation } from 'react-i18next';
import { API_BASE_URL } from '../config/api';


const SkeletonCard = ({ height = 'h-40' }) => (
    <div className={`skeleton-card ${height} w-full`} />
);

const CropDashboard = () => {
    const { t } = useTranslation();
    const { planId } = useParams();
    const { token } = useAuth();
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);
    const [error, setError] = useState('');
    const [alertsExpanded, setAlertsExpanded] = useState(false);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/crop-dashboard/${planId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    setData(await response.json());
                } else {
                    const err = await response.json();
                    setError(err.detail || "Failed to load dashboard data");
                }
            } catch (e) {
                console.error("Dashboard fetch error:", e);
                setError("A network error occurred.");
            } finally {
                setLoading(false);
            }
        };
        if (token && planId) fetchDashboardData();
    }, [planId, token]);

    /* ─── SKELETON LOADING STATE ─── */
    if (loading) {
        return (
            <div className="px-3 pt-3 pb-6 space-y-2">
                <SkeletonCard height="h-28" />
                <SkeletonCard height="h-16" />
                <SkeletonCard height="h-20" />
                <SkeletonCard height="h-16" />
            </div>
        );
    }

    /* ─── ERROR STATE ─── */
    if (error) {
        return (
            <div className="px-3 pt-10">
                <div className="glass rounded-2xl p-8 text-center">
                    <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-red-400 opacity-80" />
                    <p className="text-lg font-bold text-gray-800">{t('error_loading')}</p>
                    <p className="text-sm mt-2 text-gray-700">{error}</p>
                    <Link to="/home" className="mt-6 inline-block btn-primary text-sm">{t('return_home')}</Link>
                </div>
            </div>
        );
    }

    if (!data) return null;

    const { plan_details: plan, weather, weather_alerts, pest_risk, yield_prediction, fertilizer_recommendation, risk_reduction, market_trend, soil_insight } = data;

    const alertSeverity = (type) => {
        const t = (type || '').toLowerCase();
        if (t.includes('heavy') || t.includes('heat') || t.includes('storm') || t.includes('flood')) return 'high';
        if (t.includes('medium') || t.includes('frost')) return 'medium';
        return 'low';
    };

    const severityStyles = {
        high:   { border: 'border-l-red-500',    bg: 'bg-red-50/80',    text: 'text-red-700',    badge: 'bg-red-100 text-red-700', glow: 'glow-alert-high' },
        medium: { border: 'border-l-amber-500',  bg: 'bg-amber-50/80',  text: 'text-amber-700',  badge: 'bg-amber-100 text-amber-700', glow: '' },
        low:    { border: 'border-l-yellow-400',  bg: 'bg-yellow-50/80', text: 'text-yellow-700', badge: 'bg-yellow-100 text-yellow-700', glow: '' },
    };

    // Extract top recommendation for Smart Insight
    const topRecommendation = yield_prediction?.recommendations?.[0];
    const alertCount = weather_alerts?.length || 0;

    // Yield quality badge
    const yieldRatio = yield_prediction ? (yield_prediction.expected_yield_per_acre / (yield_prediction.avg_regional_yield || 1)) : 0;
    let yieldLabel = 'Below Avg';
    let yieldColor = 'text-red-600';
    if (yieldRatio >= 1.1) { yieldLabel = 'Excellent'; yieldColor = 'text-green-600'; }
    else if (yieldRatio >= 0.9) { yieldLabel = 'Good'; yieldColor = 'text-green-600'; }
    else if (yieldRatio >= 0.75) { yieldLabel = 'Average'; yieldColor = 'text-amber-600'; }

    // Market trend
    const marketChange = market_trend?.percentage_change || 0;
    const marketPrice = market_trend?.current_price_qt || 0;

    return (
        <div className="px-3 pt-3 pb-6" style={{ minHeight: '100vh' }}>

            {/* ═══════ 1. COMPACT HEADER ═══════ */}
            <div className="stagger-card stagger-1 glass rounded-2xl p-3 mb-2">
                {/* Top row: back + crop name */}
                <div className="flex items-center gap-2 mb-2">
                    <Link to="/crop-plan" className="w-8 h-8 flex items-center justify-center rounded-xl bg-white/90 border border-black/5 active:scale-90 transition-transform">
                        <ChevronLeft className="w-4 h-4 text-gray-800" />
                    </Link>
                    <div className="bg-gradient-to-br from-green-500 to-green-700 p-1.5 rounded-lg">
                        <Sprout className="w-4 h-4 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <h1 className="text-base font-black text-gray-800 truncate">{plan.crop_type} {t('intelligence')}</h1>
                        <p className="text-[10px] text-green-600 font-semibold">{t('plan_num')}{plan.plan_id}</p>
                    </div>
                </div>

                {/* Compact weather strip */}
                <WeatherCard weather={weather} plan={plan} compact={true} />

                {/* Compact farm detail chips — 2 rows */}
                <div className="flex flex-wrap gap-1.5 mt-2">
                    <div className="flex items-center gap-1 bg-white/85 border border-black/5 px-2 py-1 rounded-lg text-[10px] font-semibold text-gray-800">
                        <MapPin className="w-3 h-3 text-green-500" />
                        {plan.location}
                    </div>
                    <div className="flex items-center gap-1 bg-white/85 border border-black/5 px-2 py-1 rounded-lg text-[10px] font-semibold text-gray-800">
                        <Ruler className="w-3 h-3 text-green-500" />
                        {plan.land_acres} Acres
                    </div>
                    <div className="flex items-center gap-1 bg-white/85 border border-black/5 px-2 py-1 rounded-lg text-[10px] font-semibold text-gray-800">
                        <Calendar className="w-3 h-3 text-green-500" />
                        {t('sown')} {plan.sowing_date}
                    </div>
                    <div className="flex items-center gap-1 bg-white/85 border border-black/5 px-2 py-1 rounded-lg text-[10px] font-semibold text-gray-800">
                        <Droplets className="w-3 h-3 text-blue-400" />
                        {plan.water_source}
                    </div>
                </div>
            </div>

            {/* ═══════ 2. SOIL INSIGHT CARD ═══════ */}
            {soil_insight && (
                <div className="stagger-card stagger-2 glass rounded-2xl p-4 mb-2 border border-leaf-100 bg-gradient-to-br from-white to-leaf-50/50">
                    <div className="flex items-center gap-2 mb-3">
                        <div className="bg-leaf-100 p-1.5 rounded-lg">
                            <Layers className="w-4 h-4 text-leaf-600" />
                        </div>
                        <h2 className="text-sm font-black text-gray-800 tracking-tight">Soil Intelligence</h2>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-2 mb-3">
                        <div className="bg-white p-2 text-center rounded-xl border border-gray-100 shadow-sm">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-0.5">Type</p>
                            <p className="text-xs font-black text-gray-800">{soil_insight.soil_type}</p>
                        </div>
                        <div className="bg-white p-2 text-center rounded-xl border border-gray-100 shadow-sm">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-0.5">Moisture</p>
                            <p className="text-xs font-black text-blue-600">{soil_insight.moisture_level}</p>
                        </div>
                        <div className="bg-white p-2 text-center rounded-xl border border-gray-100 shadow-sm">
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-0.5">Climate</p>
                            <p className="text-xs font-black text-amber-600">{soil_insight.climate}</p>
                        </div>
                    </div>
                    
                    <div className="bg-leaf-50 p-2.5 rounded-xl border border-leaf-100/50 flex gap-2 items-start mt-1">
                        <Sprout className="w-3.5 h-3.5 text-leaf-600 mt-0.5 flex-shrink-0" />
                        <p className="text-[10px] text-gray-700 leading-snug">{soil_insight.explanation}</p>
                    </div>
                </div>
            )}

            {/* ═══════ 3. SMART INSIGHT CARD ═══════ */}
            {topRecommendation && (
                <div className="stagger-card stagger-3 glass rounded-2xl p-3 mb-2">
                    <div className="flex items-center gap-2 mb-1.5">
                        <div className="bg-gradient-to-br from-amber-400 to-orange-500 p-1.5 rounded-lg">
                            <Lightbulb className="w-4 h-4 text-white" />
                        </div>
                        <h3 className="text-sm font-bold text-gray-800">Smart Insight</h3>
                    </div>
                    <p className="text-xs text-gray-700 leading-snug line-clamp-2">
                        <span className="font-bold">{topRecommendation.title}:</span> {topRecommendation.detail}
                    </p>
                </div>
            )}



            {/* ═══════ 5. COLLAPSIBLE WARNING ALERTS ═══════ */}
            <div className="stagger-card stagger-5 glass rounded-2xl p-3 mb-2">
                <button
                    onClick={() => setAlertsExpanded(!alertsExpanded)}
                    className="w-full flex items-center justify-between"
                >
                    <div className="flex items-center gap-2">
                        <ShieldAlert className="w-4 h-4 text-red-500" />
                        <span className="text-sm font-bold text-gray-800">
                            {alertCount > 0 ? `⚠️ ${alertCount} Alert${alertCount > 1 ? 's' : ''}` : '✅ No Alerts'}
                        </span>
                    </div>
                    {alertCount > 0 && (
                        alertsExpanded
                            ? <ChevronUp className="w-4 h-4 text-gray-500" />
                            : <ChevronDown className="w-4 h-4 text-gray-500" />
                    )}
                </button>

                {/* Expanded alert content */}
                {alertsExpanded && alertCount > 0 && (
                    <div className="space-y-2 mt-2 pt-2 border-t border-gray-200/50">
                        {weather_alerts.map((alert, idx) => {
                            const sev = alertSeverity(alert.type);
                            const s = severityStyles[sev];
                            return (
                                <div key={idx} className={`${s.bg} border-l-4 ${s.border} p-2.5 rounded-xl ${s.glow}`}>
                                    <div className="flex items-center gap-2 mb-0.5">
                                        <AlertTriangle className={`w-3 h-3 ${s.text}`} />
                                        <span className={`text-[11px] font-bold ${s.text}`}>{alert.type}</span>
                                        <span className={`text-[9px] px-1.5 py-0.5 rounded-full font-bold ${s.badge}`}>{sev.toUpperCase()}</span>
                                    </div>
                                    <p className={`text-[11px] ${s.text} opacity-80`}>{alert.message || alert.recommendation}</p>
                                    {alert.recommendation && alert.message && (
                                        <p className="text-[10px] bg-white/90 border border-black/5 p-1.5 rounded-lg text-gray-800 mt-1">
                                            <strong>Action:</strong> {alert.recommendation}
                                        </p>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}

                {/* No alerts state */}
                {alertCount === 0 && (
                    <div className="bg-green-50/80 text-green-700 text-[11px] p-2 rounded-xl border border-green-100/50 flex items-center gap-2 mt-2">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        {t('safe_conditions')}
                    </div>
                )}
            </div>

            {/* ═══════ DETAIL CARDS (below fold) ═══════ */}
            <div id="detail-cards" className="space-y-2">

                {/* Yield Intelligence */}
                <div id="yield-section" className="stagger-card stagger-6">
                    <YieldPredictionCard yieldData={yield_prediction} />
                </div>

                {/* Fertilizer */}
                <div className="stagger-card stagger-7">
                    <FertilizerCard fertilizerData={fertilizer_recommendation} />
                </div>

                {/* Pest Risk */}
                <div className="stagger-card stagger-8">
                    <PestRiskCard riskData={pest_risk} />
                </div>

                {/* Market Trend */}
                <div className="stagger-card">
                    <MarketTrendCard marketData={market_trend} cropType={plan.crop_type} />
                </div>

                {/* Risk Reduction */}
                <div className="stagger-card">
                    <RiskReductionCard riskData={risk_reduction} />
                </div>

                {/* Soil Profile */}
                {plan.soil_type && (
                    <div className="stagger-card glass rounded-2xl p-3">
                        <h4 className="text-xs font-bold text-gray-700 mb-2 flex items-center gap-2">
                            <BarChart3 className="w-3.5 h-3.5 text-green-600" />
                            {t('soil_profile')}
                        </h4>
                        <div className="grid grid-cols-3 gap-1.5 text-[11px]">
                            <div className="bg-white/90 border border-black/5 p-2 rounded-xl">
                                <p className="text-gray-500 font-medium text-[9px]">{t('type')}</p>
                                <p className="font-bold text-gray-800 capitalize">{plan.soil_type}</p>
                            </div>
                            <div className="bg-white/90 border border-black/5 p-2 rounded-xl">
                                <p className="text-gray-500 font-medium text-[9px]">Season</p>
                                <p className="font-bold text-gray-800 capitalize">{plan.season}</p>
                            </div>
                            {plan.nitrogen && (
                                <div className="bg-blue-50/60 p-2 rounded-xl">
                                    <p className="text-blue-500 font-medium text-[9px]">N</p>
                                    <p className="font-bold text-gray-800">{plan.nitrogen}</p>
                                </div>
                            )}
                            {plan.phosphorus && (
                                <div className="bg-amber-50/60 p-2 rounded-xl">
                                    <p className="text-amber-500 font-medium text-[9px]">P</p>
                                    <p className="font-bold text-gray-800">{plan.phosphorus}</p>
                                </div>
                            )}
                            {plan.potassium && (
                                <div className="bg-green-50/60 p-2 rounded-xl">
                                    <p className="text-green-500 font-medium text-[9px]">K</p>
                                    <p className="font-bold text-gray-800">{plan.potassium}</p>
                                </div>
                            )}
                            {plan.ph_level && (
                                <div className="bg-purple-50/60 p-2 rounded-xl">
                                    <p className="text-purple-500 font-medium text-[9px]">pH</p>
                                    <p className="font-bold text-gray-800">{plan.ph_level}</p>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CropDashboard;
