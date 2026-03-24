import React from 'react';
import { Droplets, Wind, CloudRain, Cloud, Thermometer } from 'lucide-react';

const WeatherCard = ({ weather, plan }) => {
  if (!weather) return (
    <div className="skeleton-card h-20 w-full rounded-xl" />
  );

  return (
    <div className="mt-1">
      {/* Temperature highlight row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="bg-gradient-to-br from-blue-400 to-blue-600 p-2 rounded-xl">
            <Thermometer className="w-4 h-4 text-white" />
          </div>
          <div>
            <p className="text-xs text-gray-700 font-medium capitalize">{weather.condition}</p>
            <p className="text-xs text-gray-600">{weather.location}</p>
          </div>
        </div>
        <div className="text-right">
          <span className="text-3xl font-black text-gray-800">{weather.temperature}</span>
          <span className="text-lg font-bold text-gray-600">°C</span>
        </div>
      </div>

      {/* Horizontal weather stats */}
      <div className="flex gap-2 overflow-x-auto pb-1">
        <div className="flex items-center gap-1.5 bg-blue-50/60 px-3 py-2 rounded-xl text-xs font-semibold text-blue-700 whitespace-nowrap">
          <Droplets className="w-3.5 h-3.5" />
          {weather.humidity}%
        </div>
        <div className="flex items-center gap-1.5 bg-gray-50/60 px-3 py-2 rounded-xl text-xs font-semibold text-gray-800 whitespace-nowrap">
          <Wind className="w-3.5 h-3.5" />
          {weather.wind_speed} km/h
        </div>
        <div className="flex items-center gap-1.5 bg-blue-50/60 px-3 py-2 rounded-xl text-xs font-semibold text-blue-600 whitespace-nowrap">
          <CloudRain className="w-3.5 h-3.5" />
          {weather.rain_probability}%
        </div>
        <div className="flex items-center gap-1.5 bg-gray-50/60 px-3 py-2 rounded-xl text-xs font-semibold text-gray-700 whitespace-nowrap">
          <Cloud className="w-3.5 h-3.5" />
          {weather.cloud_coverage}%
        </div>
      </div>
    </div>
  );
};

export default WeatherCard;
