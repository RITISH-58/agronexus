import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
    ChevronLeft, Calendar, MapPin, Ruler, Droplets,
    Sprout, AlertTriangle, ShieldAlert, BarChart3,
    ShieldCheck
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
            <div className="px-4 pt-6 pb-10 space-y-4">
                <SkeletonCard height="h-36" />
                <SkeletonCard height="h-28" />
                <SkeletonCard height="h-64" />
                <SkeletonCard height="h-56" />
                <SkeletonCard height="h-48" />
                <SkeletonCard height="h-56" />
                <SkeletonCard height="h-32" />
                <SkeletonCard height="h-24" />
            </div>
        );
    }

    /* ─── ERROR STATE ─── */
    if (error) {
        return (
            <div className="px-4 pt-10">
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

    const { plan_details: plan, weather, weather_alerts, pest_risk, yield_prediction, fertilizer_recommendation, risk_reduction, market_trend } = data;

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

    return (
        <div className="px-4 pt-4 pb-10" style={{ minHeight: '100vh' }}>

            {/* ═══════ 1. HEADER CARD ═══════ */}
            <div className="stagger-card stagger-1 glass rounded-2xl p-4 mb-4">
                {/* Top row: back + crop name */}
                <div className="flex items-center gap-3 mb-3">
                    <Link to="/crop-plan" className="w-9 h-9 flex items-center justify-center rounded-xl bg-white/90 border border-black/5 active:scale-90 transition-transform">
                        <ChevronLeft className="w-5 h-5 text-gray-800" />
                    </Link>
                    <div className="bg-gradient-to-br from-green-500 to-green-700 p-2 rounded-xl">
                        <Sprout className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <h1 className="text-lg font-black text-gray-800 truncate">{plan.crop_type} {t('intelligence')}</h1>
                        <p className="text-[11px] text-green-600 font-semibold">{t('plan_num')}{plan.plan_id}</p>
                    </div>
                </div>

                {/* Weather + Location summary */}
                <WeatherCard weather={weather} plan={plan} />

                {/* Meta pills */}
                <div className="flex flex-wrap gap-2 mt-3">
                    <div className="flex items-center gap-1.5 bg-white/85 border border-black/5 px-3 py-1.5 rounded-lg text-xs font-semibold text-gray-800">
                        <MapPin className="w-3.5 h-3.5 text-green-500" />
                        {plan.location}
                    </div>
                    <div className="flex items-center gap-1.5 bg-white/85 border border-black/5 px-3 py-1.5 rounded-lg text-xs font-semibold text-gray-800">
                        <Ruler className="w-3.5 h-3.5 text-green-500" />
                        {plan.land_acres} Acres
                    </div>
                    <div className="flex items-center gap-1.5 bg-white/85 border border-black/5 px-3 py-1.5 rounded-lg text-xs font-semibold text-gray-800">
                        <Calendar className="w-3.5 h-3.5 text-green-500" />
                        {t('sown')} {plan.sowing_date}
                    </div>
                    <div className="flex items-center gap-1.5 bg-white/85 border border-black/5 px-3 py-1.5 rounded-lg text-xs font-semibold text-gray-800">
                        <Droplets className="w-3.5 h-3.5 text-blue-400" />
                        {plan.water_source} {t('water')}
                    </div>
                </div>
            </div>

            {/* ═══════ 2. WARNING ALERTS ═══════ */}
            <div className="stagger-card stagger-2 glass rounded-2xl p-4 mb-4">
                <h3 className="text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4 text-red-500" />
                    {t('warning_alerts')}
                </h3>
                {(!weather_alerts || weather_alerts.length === 0) ? (
                    <div className="bg-green-50/80 text-green-700 text-xs p-3 rounded-xl border border-green-100/50 flex items-center gap-2">
                        <ShieldCheck className="w-4 h-4" />
                        {t('safe_conditions')}
                    </div>
                ) : (
                    <div className="space-y-2">
                        {weather_alerts.map((alert, idx) => {
                            const sev = alertSeverity(alert.type);
                            const s = severityStyles[sev];
                            return (
                                <div key={idx} className={`${s.bg} border-l-4 ${s.border} p-3 rounded-xl ${s.glow}`}>
                                    <div className="flex items-center gap-2 mb-1">
                                        <AlertTriangle className={`w-3.5 h-3.5 ${s.text}`} />
                                        <span className={`text-xs font-bold ${s.text}`}>{alert.type}</span>
                                        <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold ${s.badge}`}>{sev.toUpperCase()}</span>
                                    </div>
                                    <p className={`text-xs ${s.text} opacity-80 mb-1`}>{alert.message || alert.recommendation}</p>
                                    {alert.recommendation && alert.message && (
                                        <p className="text-[11px] bg-white/90 border border-black/5 p-2 rounded-lg text-gray-800">
                                            <strong>Action:</strong> {alert.recommendation}
                                        </p>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            {/* ═══════ 3. YIELD INTELLIGENCE ═══════ */}
            <div className="stagger-card stagger-3 mb-4">
                <YieldPredictionCard yieldData={yield_prediction} />
            </div>

            {/* ═══════ 4. FERTILIZER ═══════ */}
            <div className="stagger-card stagger-4 mb-4">
                <FertilizerCard fertilizerData={fertilizer_recommendation} />
            </div>

            {/* ═══════ 5. PEST RISK ═══════ */}
            <div className="stagger-card stagger-5 mb-4">
                <PestRiskCard riskData={pest_risk} />
            </div>

            {/* ═══════ 6. MARKET TREND ═══════ */}
            <div className="stagger-card stagger-6 mb-4">
                <MarketTrendCard marketData={market_trend} cropType={plan.crop_type} />
            </div>

            {/* ═══════ 7. RISK REDUCTION ═══════ */}
            <div className="stagger-card stagger-7 mb-4">
                <RiskReductionCard riskData={risk_reduction} />
            </div>

            {/* ═══════ 8. SOIL PROFILE ═══════ */}
            {plan.soil_type && (
                <div className="stagger-card stagger-8 glass rounded-2xl p-4 mb-4">
                    <h4 className="text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
                        <BarChart3 className="w-4 h-4 text-green-600" />
                        {t('soil_profile')}
                    </h4>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="bg-white/90 border border-black/5 p-3 rounded-xl">
                            <p className="text-gray-600 font-medium mb-0.5">{t('type')}</p>
                            <p className="font-bold text-gray-800 capitalize">{plan.soil_type}</p>
                        </div>
                        <div className="bg-white/90 border border-black/5 p-3 rounded-xl">
                            <p className="text-gray-600 font-medium mb-0.5">Season</p>
                            <p className="font-bold text-gray-800 capitalize">{plan.season}</p>
                        </div>
                        {plan.nitrogen && (
                            <div className="bg-blue-50/60 p-3 rounded-xl">
                                <p className="text-blue-500 font-medium mb-0.5">N</p>
                                <p className="font-bold text-gray-800">{plan.nitrogen}</p>
                            </div>
                        )}
                        {plan.phosphorus && (
                            <div className="bg-amber-50/60 p-3 rounded-xl">
                                <p className="text-amber-500 font-medium mb-0.5">P</p>
                                <p className="font-bold text-gray-800">{plan.phosphorus}</p>
                            </div>
                        )}
                        {plan.potassium && (
                            <div className="bg-green-50/60 p-3 rounded-xl">
                                <p className="text-green-500 font-medium mb-0.5">K</p>
                                <p className="font-bold text-gray-800">{plan.potassium}</p>
                            </div>
                        )}
                        {plan.ph_level && (
                            <div className="bg-purple-50/60 p-3 rounded-xl">
                                <p className="text-purple-500 font-medium mb-0.5">pH</p>
                                <p className="font-bold text-gray-800">{plan.ph_level}</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CropDashboard;
