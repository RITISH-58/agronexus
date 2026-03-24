import React from 'react';
import { ShieldCheck, CheckCircle2, Sprout } from 'lucide-react';

const RiskReductionCard = ({ riskData }) => {
    if (!riskData || !riskData.recommended_companion_crops) return null;

    return (
        <div className="glass rounded-2xl p-5 card-hover">
            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
                <div className="bg-gradient-to-br from-indigo-400 to-indigo-600 p-2.5 rounded-xl">
                    <ShieldCheck className="w-5 h-5 text-white" />
                </div>
                <div>
                    <h3 className="text-base font-bold text-gray-800">Risk Reduction</h3>
                    <p className="text-[11px] text-gray-600">Diversify to minimize exposure</p>
                </div>
            </div>

            {/* Companion Crop Chips */}
            <div className="mb-4">
                <p className="text-[10px] font-bold text-gray-600 uppercase tracking-wider mb-2.5">Companion Crops</p>
                <div className="flex flex-wrap gap-2">
                    {riskData.recommended_companion_crops.map((crop, idx) => (
                        <div key={idx} className="crop-chip flex items-center gap-1.5">
                            <Sprout className="w-3.5 h-3.5 text-green-500" />
                            {crop}
                        </div>
                    ))}
                </div>
            </div>

            {/* Benefits */}
            <div>
                <p className="text-[10px] font-bold text-gray-600 uppercase tracking-wider mb-2.5">Predicted Benefits</p>
                <ul className="space-y-2.5">
                    {riskData.benefits.map((benefit, idx) => (
                        <li key={idx} className="flex gap-2.5 text-xs text-gray-700 items-start">
                            <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                            <span className="leading-snug">{benefit}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default RiskReductionCard;
