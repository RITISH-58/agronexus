import React, { useState, useEffect } from 'react';
import { TrendingUp, AlertTriangle, CheckCircle, Lightbulb, Zap, Droplets, Leaf, RotateCcw } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts';

const IMPACT_COLORS = { high: 'text-red-600 bg-red-50 border-red-200', medium: 'text-amber-600 bg-amber-50 border-amber-200', low: 'text-green-600 bg-green-50 border-green-200' };
const TYPE_ICONS = { fertilizer: <Leaf size={14} />, soil: <Zap size={14} />, irrigation: <Droplets size={14} />, management: <AlertTriangle size={14} />, crop_switch: <RotateCcw size={14} /> };

const YieldPredictionCard = ({ yieldData }) => {
    const [animateRing, setAnimateRing] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setAnimateRing(true), 300);
        return () => clearTimeout(timer);
    }, []);

    if (!yieldData) return null;

    const { expected_yield_per_acre, total_expected_yield, unit, confidence_score,
            avg_regional_yield, optimal_yield, recommendations } = yieldData;

    const chartData = [
        { name: 'Regional', yield: Math.round(avg_regional_yield * 100) / 100 },
        { name: 'Your Farm', yield: Math.round(expected_yield_per_acre * 100) / 100 },
        { name: 'Optimal', yield: Math.round(optimal_yield * 100) / 100 }
    ];

    const BAR_COLORS = ['#94A3B8', '#10B981', '#3B82F6'];

    const yieldRatio = expected_yield_per_acre / (avg_regional_yield || 1);
    let qualityBadge = { label: 'Below Average', color: 'bg-red-100 text-red-700', icon: <AlertTriangle size={12} /> };
    if (yieldRatio >= 1.1) qualityBadge = { label: 'Excellent', color: 'bg-green-100 text-green-700', icon: <CheckCircle size={12} /> };
    else if (yieldRatio >= 0.9) qualityBadge = { label: 'Good', color: 'bg-emerald-100 text-emerald-700', icon: <CheckCircle size={12} /> };
    else if (yieldRatio >= 0.75) qualityBadge = { label: 'Average', color: 'bg-amber-100 text-amber-700', icon: <Lightbulb size={12} /> };

    const circumference = 2 * Math.PI * 28;
    const progress = animateRing ? ((confidence_score || 0) / 100) * circumference : 0;

    return (
        <div className="glass rounded-2xl p-5 card-hover">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                    <div className="bg-gradient-to-br from-green-400 to-emerald-600 p-2.5 rounded-xl">
                        <TrendingUp className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h3 className="text-base font-bold text-gray-800">Yield Intelligence</h3>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full inline-flex items-center gap-1 ${qualityBadge.color}`}>
                            {qualityBadge.icon} {qualityBadge.label}
                        </span>
                    </div>
                </div>

                {/* Animated Confidence Ring */}
                <div className="relative w-16 h-16 flex items-center justify-center flex-shrink-0">
                    <svg className="w-16 h-16 -rotate-90" viewBox="0 0 64 64">
                        <circle cx="32" cy="32" r="28" fill="none" stroke="#E5E7EB" strokeWidth="4" />
                        <circle cx="32" cy="32" r="28" fill="none"
                            stroke={confidence_score >= 75 ? '#10B981' : confidence_score >= 50 ? '#F59E0B' : '#EF4444'}
                            strokeWidth="4" strokeLinecap="round"
                            strokeDasharray={circumference}
                            strokeDashoffset={circumference - progress}
                            style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1)' }}
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-sm font-black text-gray-800">{Math.round(confidence_score || 0)}%</span>
                        <span className="text-[8px] text-gray-600 font-bold uppercase">Conf.</span>
                    </div>
                </div>
            </div>

            {/* Yield Numbers — 2-card grid */}
            <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-white/90 border border-black/5 p-3.5 rounded-xl border border-gray-100/50">
                    <p className="text-[10px] font-bold text-gray-600 uppercase tracking-wider mb-1">Per Acre Yield</p>
                    <p className="text-xl font-black text-gray-800">{expected_yield_per_acre}</p>
                    <p className="text-xs text-gray-600">{unit}</p>
                </div>
                <div className="bg-green-50/60 p-3.5 rounded-xl border border-green-100/50">
                    <p className="text-[10px] font-bold text-green-600 uppercase tracking-wider mb-1">Total Harvest</p>
                    <p className="text-xl font-black text-green-700">{total_expected_yield}</p>
                    <p className="text-xs text-green-500">{unit}</p>
                </div>
            </div>

            {/* Bar Chart */}
            <div className="h-44 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 8, right: 4, left: -24, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#6B7280', fontWeight: 600 }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#9CA3AF' }} />
                        <Tooltip
                            cursor={{ fill: 'rgba(0,0,0,0.03)' }}
                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', fontSize: '12px' }}
                            formatter={(value) => [`${value} ${unit}`, 'Yield']}
                        />
                        <Bar dataKey="yield" radius={[8, 8, 0, 0]} barSize={36} animationDuration={1200} animationBegin={400}>
                            {chartData.map((_, idx) => (
                                <Cell key={idx} fill={BAR_COLORS[idx]} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* AI Recommendations */}
            {recommendations && recommendations.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-100/50">
                    <h4 className="text-xs font-bold text-gray-800 mb-2 flex items-center gap-1.5">
                        <Lightbulb size={13} className="text-amber-500" />
                        AI Recommendations
                    </h4>
                    <div className="space-y-2">
                        {recommendations.map((rec, idx) => (
                            <div key={idx} className={`p-3 rounded-xl border text-xs ${IMPACT_COLORS[rec.impact] || IMPACT_COLORS.low}`}>
                                <div className="flex items-center gap-2 mb-1">
                                    {TYPE_ICONS[rec.type] || <Lightbulb size={14} />}
                                    <span className="font-bold">{rec.title}</span>
                                    <span className="ml-auto text-[9px] font-bold uppercase opacity-100">{rec.impact}</span>
                                </div>
                                <p className="opacity-80 leading-snug">{rec.detail}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default YieldPredictionCard;
