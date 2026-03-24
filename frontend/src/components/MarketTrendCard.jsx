import React from 'react';
import { TrendingUp, TrendingDown, Minus, Lightbulb } from 'lucide-react';
import {
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart
} from 'recharts';

const MarketTrendCard = ({ marketData, cropType }) => {
    if (!marketData) return null;

    const price = marketData.current_price_qt || 0;
    const change = marketData.percentage_change || 0;
    const isRising = change > 0;
    const isStable = change === 0;

    const generatePriceHistory = () => {
        const data = [];
        const today = new Date();
        for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            const dayLabel = date.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric' });
            const variation = (Math.random() - 0.4) * (price * 0.03);
            const dayPrice = Math.round(price - (i * (price * change / 100 / 7)) + variation);
            data.push({ date: dayLabel, price: dayPrice });
        }
        return data;
    };

    const priceHistory = generatePriceHistory();

    const trendLabel = isRising ? 'Price Likely to Increase' : isStable ? 'Stable Market' : 'Possible Decline';
    const trendColor = isRising ? 'text-green-600' : isStable ? 'text-blue-600' : 'text-red-600';
    const trendBg = isRising ? 'bg-green-50/60 border-green-100/50' : isStable ? 'bg-blue-50/60 border-blue-100/50' : 'bg-red-50/60 border-red-100/50';
    const TrendIcon = isRising ? TrendingUp : isStable ? Minus : TrendingDown;
    const lineColor = isRising ? '#10B981' : isStable ? '#3B82F6' : '#F59E0B';

    return (
        <div className="glass rounded-2xl p-5 card-hover">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                    <div className="bg-gradient-to-br from-amber-400 to-orange-500 p-2.5 rounded-xl">
                        <TrendingUp className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h3 className="text-base font-bold text-gray-800">Market Trend</h3>
                        <p className="text-[11px] text-gray-600">{cropType} — 7 Day</p>
                    </div>
                </div>
                <div className={`flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold ${trendBg} ${trendColor} border`}>
                    <TrendIcon className="w-3.5 h-3.5" />
                    {change > 0 ? '+' : ''}{change}%
                </div>
            </div>

            {/* Price Display */}
            <div className="bg-gradient-to-br from-amber-50/60 to-orange-50/40 p-4 rounded-xl border border-amber-100/40 mb-4">
                <p className="text-[10px] font-bold text-amber-600 uppercase tracking-wider mb-1">Current Price</p>
                <div className="flex items-baseline gap-1">
                    <p className="text-3xl font-black text-gray-800">₹{price.toLocaleString()}</p>
                    <p className="text-xs text-gray-600 font-medium">/ qt</p>
                </div>
            </div>

            {/* Area Chart — full width */}
            <div className="h-44 w-full mb-4">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={priceHistory} margin={{ top: 5, right: 4, left: -20, bottom: 0 }}>
                        <defs>
                            <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={lineColor} stopOpacity={0.25} />
                                <stop offset="95%" stopColor={lineColor} stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                        <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#9CA3AF' }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: '#9CA3AF' }}
                            domain={['dataMin - 200', 'dataMax + 200']}
                            tickFormatter={(v) => `₹${v}`} />
                        <Tooltip
                            formatter={(value) => [`₹${value.toLocaleString()}`, 'Price']}
                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', fontSize: '11px' }}
                        />
                        <Area type="monotone" dataKey="price" stroke={lineColor}
                            strokeWidth={2.5} fill="url(#priceGradient)"
                            dot={{ r: 3, fill: '#fff', stroke: lineColor, strokeWidth: 2 }}
                            activeDot={{ r: 5 }}
                            animationDuration={1500}
                            animationBegin={300}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {/* Forecast + AI Advice */}
            <div className={`p-3 rounded-xl border ${trendBg} mb-3`}>
                <p className="text-[10px] font-bold text-gray-700 uppercase tracking-wider mb-1">Next Week Forecast</p>
                <div className={`flex items-center gap-1.5 ${trendColor} font-bold text-sm`}>
                    <TrendIcon className="w-4 h-4" />
                    {trendLabel}
                </div>
            </div>

            <div className="bg-blue-50/40 p-3 rounded-xl border border-blue-100/30">
                <div className="flex items-start gap-2">
                    <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-xs text-gray-800 leading-relaxed">
                        {isRising
                            ? 'Demand rising due to seasonal supply reduction. Consider holding stock for better prices.'
                            : isStable
                            ? 'Market is stable. Sell gradually for consistent returns.'
                            : 'Market may soften. Consider early selling or processing for value addition.'
                        }
                    </p>
                </div>
            </div>
        </div>
    );
};

export default MarketTrendCard;
