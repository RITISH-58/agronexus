import React from 'react';
import { Lightbulb, Sprout, Wind, Droplets } from 'lucide-react';

const FarmingAdvisorCard = ({ adviceData }) => {
  if (!adviceData) return <div className="p-6 glass rounded-2xl border-0 animate-pulse h-40">Generating AI advice...</div>;

  const getIcon = (category) => {
    switch(category.toLowerCase()) {
      case 'irrigation': return <Droplets className="w-5 h-5 text-blue-500 mr-3 mt-0.5 flex-shrink-0" />;
      case 'fertilizer': return <Sprout className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />;
      case 'pesticide': return <Wind className="w-5 h-5 text-purple-500 mr-3 mt-0.5 flex-shrink-0" />;
      default: return <Lightbulb className="w-5 h-5 text-yellow-500 mr-3 mt-0.5 flex-shrink-0" />;
    }
  };

  return (
    <div className="glass card-hover rounded-2xl p-6 border-0">
      <div className="flex items-center mb-6">
        <div className="bg-green-600 p-2 rounded-lg mr-3 shadow-md">
          <Lightbulb className="w-6 h-6 text-white" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-800">AI Farming Advisor</h3>
          <p className="text-xs text-green-600 font-semibold">{adviceData.summary}</p>
        </div>
      </div>

      <div className="space-y-4">
        {adviceData.recommendations.map((rec, idx) => (
          <div key={idx} className="bg-white/90 border border-black/5 p-4 rounded-xl shadow-sm border border-white/50 flex items-start">
            {getIcon(rec.category)}
            <div>
              <h4 className="font-bold text-gray-800 text-sm mb-1">{rec.title}</h4>
              <p className="text-gray-800 text-sm leading-relaxed">{rec.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FarmingAdvisorCard;
