import React, { useState, useEffect } from 'react';
import { Beaker, Info } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const FertilizerCard = ({ fertilizerData }) => {
    const [animate, setAnimate] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setAnimate(true), 200);
        return () => clearTimeout(timer);
    }, []);

    if (!fertilizerData) return null;

    const data = [
        { name: 'Nitrogen (N)', value: fertilizerData.nitrogen_kg_per_acre, color: '#3B82F6' },
        { name: 'Phosphorus (P)', value: fertilizerData.phosphorus_kg_per_acre, color: '#F59E0B' },
        { name: 'Potassium (K)', value: fertilizerData.potassium_kg_per_acre, color: '#10B981' },
    ];

    return (
        <div className="glass rounded-2xl p-5 card-hover">
            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
                <div className="bg-gradient-to-br from-blue-400 to-blue-600 p-2.5 rounded-xl">
                    <Beaker className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-base font-bold text-gray-800">Fertilizer Recommendation</h3>
            </div>

            {/* Donut Chart with NPK center label */}
            <div className="relative" style={{ height: '200px' }}>
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={55}
                            outerRadius={78}
                            paddingAngle={5}
                            dataKey="value"
                            animationDuration={1200}
                            animationBegin={300}
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Pie>
                        <Tooltip
                            formatter={(value) => [`${value} kg/acre`, 'Amount']}
                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', fontSize: '12px' }}
                        />
                    </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                    <span className="text-[10px] text-gray-600 font-bold uppercase tracking-widest">NPK</span>
                    <span className="text-lg font-black text-gray-800">
                        {Math.round(data[0].value/10)}:{Math.round(data[1].value/10)}:{Math.round(data[2].value/10)}
                    </span>
                </div>
            </div>

            {/* N/P/K Legend */}
            <div className="flex justify-center gap-4 mt-2 mb-4">
                {data.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-1.5 text-xs font-semibold text-gray-800">
                        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                        {item.name.split(' ')[0]}: {item.value} kg
                    </div>
                ))}
            </div>

            {/* AI Recommendation */}
            <div className="bg-blue-50/50 p-3.5 rounded-xl border border-blue-100/40">
                <div className="flex items-start gap-2.5">
                    <Info className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div>
                        <p className="text-[10px] font-bold text-blue-700 uppercase tracking-wider mb-1">AI Recommendation</p>
                        <p className="text-xs text-gray-700 leading-relaxed">{fertilizerData.advice}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FertilizerCard;
