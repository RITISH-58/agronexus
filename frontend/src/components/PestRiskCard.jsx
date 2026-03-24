import React, { useState, useEffect } from 'react';
import { Bug, ShieldCheck, AlertOctagon, Shield, Crosshair, Lightbulb } from 'lucide-react';

const PestRiskCard = ({ riskData }) => {
    const [animateBar, setAnimateBar] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setAnimateBar(true), 400);
        return () => clearTimeout(timer);
    }, []);

    if (!riskData) return <div className="skeleton-card h-48 w-full" />;

    const level = (riskData.risk_level || 'low').toLowerCase();

    const styles = {
        high:   { bg: 'bg-red-50/60',    border: 'border-red-200/50',    text: 'text-red-700',    badge: 'bg-red-500',    bar: 'bg-gradient-to-r from-red-400 to-red-500',    width: '100%',  icon: AlertOctagon, cardBg: 'from-red-50/30 to-orange-50/20' },
        medium: { bg: 'bg-amber-50/60',  border: 'border-amber-200/50',  text: 'text-amber-700',  badge: 'bg-amber-500',  bar: 'bg-gradient-to-r from-amber-300 to-amber-500',  width: '60%',   icon: Shield, cardBg: 'from-amber-50/30 to-yellow-50/20' },
        low:    { bg: 'bg-green-50/60',  border: 'border-green-200/50',  text: 'text-green-700',  badge: 'bg-green-500',  bar: 'bg-gradient-to-r from-green-300 to-green-500',  width: '25%',   icon: ShieldCheck, cardBg: 'from-green-50/30 to-emerald-50/20' },
    };

    const s = styles[level] || styles.low;
    const RiskIcon = s.icon;

    return (
        <div className={`glass rounded-2xl card-hover overflow-hidden bg-gradient-to-br ${s.cardBg}`}>
            {/* Header */}
            <div className="px-5 pt-5 pb-3">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <div className="bg-gradient-to-br from-amber-400 to-orange-500 p-2.5 rounded-xl">
                            <Bug className="w-5 h-5 text-white" />
                        </div>
                        <h3 className="text-base font-bold text-gray-800">Pest Risk</h3>
                    </div>
                    <span className={`text-[11px] text-white px-3 py-1 rounded-full font-bold ${s.badge}`}>
                        {riskData.risk_level.toUpperCase()}
                    </span>
                </div>

                {/* Animated Threat Level Bar */}
                <div className="mb-3">
                    <div className="flex justify-between text-xs mb-1.5">
                        <span className="text-gray-700 font-medium">Threat Level</span>
                        <span className={`font-bold ${s.text}`}>{riskData.risk_level}</span>
                    </div>
                    <div className="w-full bg-white/90 border border-black/5 h-2.5 rounded-full overflow-hidden">
                        <div
                            className={`h-full rounded-full ${s.bar}`}
                            style={{
                                width: animateBar ? s.width : '0%',
                                transition: 'width 1s cubic-bezier(0.4, 0, 0.2, 1)'
                            }}
                        />
                    </div>
                </div>
            </div>

            {/* Details */}
            <div className="px-5 pb-5 space-y-2.5">
                <div className="bg-white/85 border border-black/5 p-3 rounded-xl">
                    <p className="text-[10px] font-bold text-gray-600 uppercase tracking-widest mb-0.5">Crop Type</p>
                    <p className="text-sm font-bold text-gray-800 capitalize">{riskData.crop}</p>
                </div>

                <div className="bg-white/85 border border-black/5 p-3 rounded-xl">
                    <p className="text-[10px] font-bold text-gray-600 uppercase tracking-widest mb-0.5">Identified Threat</p>
                    <div className="flex items-center gap-2">
                        <Crosshair className={`w-4 h-4 ${s.text}`} />
                        <p className="text-sm font-bold text-gray-800">{riskData.identified_pest}</p>
                    </div>
                </div>

                <div className="bg-white/85 border border-black/5 p-3 rounded-xl">
                    <div className="flex items-start gap-2">
                        <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                        <div>
                            <p className="text-[10px] font-bold text-blue-600 uppercase tracking-widest mb-0.5">AI Recommendation</p>
                            <p className="text-xs text-gray-700 leading-relaxed">{riskData.recommendation}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PestRiskCard;
