import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Area, AreaChart } from 'recharts';

const ForecastChart = ({ data }) => {
  if (!data || data.length === 0) return <div className="p-6 glass rounded-2xl border-0 animate-pulse h-64">Loading forecast...</div>;

  // Format date to short day names
  const formattedData = data.map(day => ({
      ...day,
      dayName: new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })
  }));

  return (
    <div className="glass rounded-2xl p-6 border-0">
      <h3 className="text-lg font-bold text-gray-800 mb-4">7-Day Weather Trend</h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={formattedData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="dayName" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis yAxisId="left" stroke="#9ca3af" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis yAxisId="right" orientation="right" stroke="#60a5fa" fontSize={12} tickLine={false} axisLine={false} />
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
            <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}/>
            <Area yAxisId="left" type="monotone" dataKey="temperature_max" name="Max Temp (°C)" stroke="#ef4444" fillOpacity={1} fill="url(#colorTemp)" strokeWidth={3} />
            <Area yAxisId="left" type="monotone" dataKey="temperature_min" name="Min Temp (°C)" stroke="#fca5a5" fillOpacity={0} strokeWidth={2} strokeDasharray="5 5" />
            <Line yAxisId="right" type="monotone" dataKey="rainfall_mm" name="Rainfall (mm)" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ForecastChart;
