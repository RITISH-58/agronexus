import React from 'react';
import { TrendingUp, TrendingDown, Minus, Lightbulb, ShieldAlert, Target, ShieldCheck, Zap } from 'lucide-react';
import {
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart
} from 'recharts';

const MarketTrendCard = ({ marketData, cropType }) => {
    if (!marketData || !marketData.recommendation) {
        // Fallback for old simple data formatting if present
        return null; 
    }

    const { 
        current_price, 
        forecast_120d: forecast, 
        confidence_percent, 
        risk_score, 
        risk_reasons, 
        recommendation, 
        recommendation_reasonId,
        features = {} 
    } = marketData;

    const isRising = forecast.expected > current_price;
    const isStable = forecast.expected === current_price;

    const displayRecommendation = () => {
        if (recommendation === 'HOLD') {
            return { color: 'text-indigo-700 bg-indigo-100 border-indigo-200', text: 'HOLD INVENTORY', icon: ShieldCheck };
        }
        if (recommendation === 'SELL') {
            return { color: 'text-rose-700 bg-rose-100 border-rose-200', text: 'SELL IMMEDIATELY', icon: TrendingDown };
        }
        return { color: 'text-amber-700 bg-amber-100 border-amber-200', text: 'SELL PARTIAL (50%)', icon: Minus };
    };

    const recStyles = displayRecommendation();
    const RecIcon = recStyles.icon;

    // Generate 120-day smooth forward-looking curve
    const generateForecastCurve = () => {
        const data = [];
        const today = new Date();
        const steps = 6;
        const stepDays = 120 / steps;
        
        for (let i = 0; i <= steps; i++) {
            const date = new Date(today);
            date.setDate(date.getDate() + (i * stepDays));
            const dayLabel = date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
            
            // interpolate between current and expected
            const progress = i / steps;
            const variance = (Math.random() - 0.5) * (current_price * 0.05);
            const val = current_price + ((forecast.expected - current_price) * progress) + variance;
            data.push({ date: dayLabel, price: Math.round(val) });
        }
        return data;
    };

    const forecastHistory = generateForecastCurve();
    
    // Risk score styling
    const riskColor = risk_score > 70 ? 'text-rose-600 bg-rose-50' : risk_score > 40 ? 'text-amber-600 bg-amber-50' : 'text-emerald-600 bg-emerald-50';
    const riskBarColor = risk_score > 70 ? 'bg-rose-500' : risk_score > 40 ? 'bg-amber-500' : 'bg-emerald-500';

    return (
        <div className="glass rounded-2xl p-5 card-hover relative overflow-hidden">
            {/* Background elements */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/[0.03] rounded-full blur-2xl pointer-events-none" />

            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-3">
                    <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 rounded-xl shadow-md">
                        <Zap className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h3 className="text-base font-black text-gray-800 tracking-tight">AI Price Engine</h3>
                        <p className="text-[11px] text-gray-500 font-medium">{cropType} — 120 Day Forecast</p>
                    </div>
                </div>
                
                <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-black shadow-sm ${recStyles.color} border`}>
                    <RecIcon className="w-3.5 h-3.5" />
                    {recStyles.text}
                </div>
            </div>

            {/* Price & Forecast Grid */}
            <div className="grid grid-cols-2 gap-3 mb-5">
                <div className="bg-white/80 border border-black/5 p-4 rounded-2xl shadow-sm">
                    <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">Current Price</p>
                    <div className="flex items-baseline gap-1">
                        <p className="text-2xl font-black text-gray-800">₹{current_price.toLocaleString()}</p>
                        <p className="text-[10px] text-gray-500 font-bold">/ qt</p>
                    </div>
                </div>

                <div className="bg-indigo-50/60 border border-indigo-100 p-4 rounded-2xl shadow-sm">
                    <p className="text-[10px] font-bold text-indigo-600 uppercase tracking-widest mb-1">120d Expected</p>
                    <div className="flex items-baseline gap-1">
                        <p className="text-2xl font-black text-indigo-900">₹{forecast.expected.toLocaleString()}</p>
                        <p className="text-[10px] text-indigo-600 font-bold">/ qt</p>
                    </div>
                    <p className="text-[9px] text-indigo-500/80 font-bold mt-1">Range: ₹{forecast.min} - ₹{forecast.max}</p>
                </div>
            </div>

            {/* AI Chart */}
            <div className="h-40 w-full mb-5">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={forecastHistory} margin={{ top: 5, right: 0, left: -25, bottom: 0 }}>
                        <defs>
                            <linearGradient id="aiGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#6366F1" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                        <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#9CA3AF', fontWeight: 600 }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#9CA3AF', fontWeight: 600 }}
                            domain={['dataMin - 100', 'dataMax + 100']}
                            tickFormatter={(v) => `₹${v}`} />
                        <Tooltip
                            formatter={(value) => [`₹${value.toLocaleString()}`, 'Forecast']}
                            contentStyle={{ borderRadius: '12px', border: '1px solid #E5E7EB', boxShadow: '0 8px 16px rgba(0,0,0,0.05)', fontSize: '11px', fontWeight: 'bold' }}
                        />
                        <Area type="monotone" dataKey="price" stroke="#6366F1"
                            strokeWidth={3} fill="url(#aiGradient)"
                            dot={{ r: 4, fill: '#fff', stroke: '#6366F1', strokeWidth: 2 }}
                            activeDot={{ r: 6 }}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {/* Metrics: Risk & Confidence */}
            <div className="grid grid-cols-2 gap-3 mb-4">
                {/* Risk Score */}
                <div className={`p-3 rounded-xl border ${riskColor} border-opacity-30 flex flex-col justify-center`}>
                    <div className="flex justify-between items-center mb-1.5">
                        <p className="text-[10px] font-bold uppercase tracking-widest flex items-center gap-1.5">
                            <ShieldAlert size={12} /> Risk Score
                        </p>
                        <span className="text-xs font-black">{risk_score}/100</span>
                    </div>
                    <div className="w-full bg-black/5 rounded-full h-1.5">
                        <div className={`h-1.5 rounded-full ${riskBarColor}`} style={{ width: `${risk_score}%` }}></div>
                    </div>
                </div>

                {/* Confidence */}
                <div className="bg-emerald-50/60 border border-emerald-100 p-3 rounded-xl flex flex-col justify-center text-emerald-700">
                    <div className="flex justify-between items-center mb-1.5">
                        <p className="text-[10px] font-bold uppercase tracking-widest flex items-center gap-1.5">
                            <Target size={12} /> Prediction Acc.
                        </p>
                        <span className="text-xs font-black">{confidence_percent}%</span>
                    </div>
                    <div className="w-full bg-black/5 rounded-full h-1.5">
                        <div className="h-1.5 rounded-full bg-emerald-500" style={{ width: `${confidence_percent}%` }}></div>
                    </div>
                </div>
            </div>

            {/* AI Reasoning */}
            <div className="bg-white/90 border border-black/5 p-4 rounded-xl shadow-sm mb-4">
                <div className="flex items-start gap-2.5 mb-2">
                    <Lightbulb className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                    <div>
                        <p className="text-[11px] font-bold text-gray-800 uppercase tracking-widest mb-1">AI Recommendation</p>
                        <p className="text-sm font-semibold text-gray-700 leading-snug">{recommendation_reasonId}</p>
                    </div>
                </div>
                
                {/* Risk Reasons */}
                {risk_reasons && risk_reasons.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-100 space-y-1.5">
                        {risk_reasons.map((r, i) => (
                            <p key={i} className="text-xs text-gray-500 font-medium flex items-center gap-1.5">
                                <span className="w-1 h-1 bg-gray-400 rounded-full"></span> {r}
                            </p>
                        ))}
                    </div>
                )}
            </div>

            {/* Model Inputs Display */}
            <div className="border border-indigo-100 bg-indigo-50/30 p-4 rounded-xl shadow-sm">
                <p className="text-[10px] font-bold text-indigo-800 uppercase tracking-widest mb-3 flex items-center gap-1">
                    <Zap size={12} /> Model Variables (Agmarknet & Sensors)
                </p>
                <div className="grid grid-cols-2 gap-y-3 gap-x-2">
                    <div>
                        <p className="text-[9px] font-bold text-gray-500 uppercase">Mandi / MSP Base</p>
                        <p className="text-xs font-black text-gray-800">₹{features.msp_base || current_price}</p>
                    </div>
                    <div>
                        <p className="text-[9px] font-bold text-gray-500 uppercase">Arrival Volumes</p>
                        <p className="text-xs font-black text-gray-800">{features.arrival_volumes || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-[9px] font-bold text-gray-500 uppercase">Rainfall Deviation</p>
                        <p className="text-xs font-black text-gray-800">{features.rainfall_dev || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-[9px] font-bold text-gray-500 uppercase">Sowing Area (YoY)</p>
                        <p className="text-xs font-black text-gray-800">{features.sowing_data || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-[9px] font-bold text-gray-500 uppercase">Price Volatility</p>
                        <p className="text-xs font-black text-gray-800">{features.volatility || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="text-[9px] font-bold text-gray-500 uppercase">Global Commodity</p>
                        <p className="text-xs font-black text-gray-800">{features.global_commodity || 'Stable'}</p>
                    </div>
                </div>
            </div>
            
            {/* Disclaimer */}
            <p className="text-[9px] text-gray-400 text-center font-medium mt-4">
                Powered by simulated Prophet & XGBoost Market Analysis
            </p>
        </div>
    );
};

export default MarketTrendCard;
