import React, { useState, useEffect } from 'react';
import WeatherCard from '../components/WeatherCard';
import ForecastChart from '../components/ForecastChart';
import { useTranslation } from 'react-i18next';
import { API_BASE_URL } from '../config/api';


const API = `${API_BASE_URL}/api`;

// Color helper
const riskColor = (level) => {
  switch ((level || '').toLowerCase()) {
    case 'high': return { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-800', badge: 'bg-red-600' };
    case 'medium': return { bg: 'bg-amber-50', border: 'border-amber-200', text: 'text-amber-800', badge: 'bg-amber-500' };
    default: return { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-800', badge: 'bg-green-500' };
  }
};

const WeatherIntelligence = () => {
  const { t } = useTranslation();
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [hazards, setHazards] = useState([]);
  const [pestRisk, setPestRisk] = useState(null);
  const [diseaseRisk, setDiseaseRisk] = useState(null);
  const [irrigation, setIrrigation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState('Hyderabad');
  const [searchInput, setSearchInput] = useState('');
  const [indiaError, setIndiaError] = useState('');
  const [crop, setCrop] = useState('Rice');

  const fetchAll = async (loc) => {
    setLoading(true);
    setIndiaError('');
    try {
      // 1 — Weather core data
      const [wRes, fRes, aRes, hRes] = await Promise.all([
        fetch(`${API}/weather/current?location=${encodeURIComponent(loc)}`),
        fetch(`${API}/weather/forecast?location=${encodeURIComponent(loc)}`),
        fetch(`${API}/weather/alerts?location=${encodeURIComponent(loc)}`),
        fetch(`${API}/weather/hazards?location=${encodeURIComponent(loc)}`)
      ]);

      if (!wRes.ok) {
        const err = await wRes.json();
        if (wRes.status === 400) { setIndiaError(err.detail); setLoading(false); return; }
      }

      const weatherData = await wRes.json();
      const forecastData = await fRes.json();
      const alertsData = await aRes.json();
      const hazardsData = await hRes.json();

      setWeather(weatherData);
      setForecast(forecastData);
      setAlerts(alertsData.alerts || []);
      setHazards(hazardsData.hazards || []);

      // 2 — Intelligence analysis (uses weather data)
      const t = weatherData.temperature;
      const h = weatherData.humidity;
      const r = forecastData[0]?.rainfall_mm || 0;
      const cc = weatherData.cloud_coverage || 50;

      const [pRes, dRes, iRes] = await Promise.all([
        fetch(`${API}/weather/pest-risk`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ crop, temperature: t, humidity: h, rainfall_mm: r }) }),
        fetch(`${API}/weather/disease-risk`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ crop, temperature: t, humidity: h, rainfall_mm: r, cloud_coverage: cc }) }),
        fetch(`${API}/weather/irrigation-advice`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ crop, temperature: t, humidity: h, rain_forecast_mm: r, recent_rainfall_mm: 0 }) })
      ]);

      setPestRisk(await pRes.json());
      setDiseaseRisk(await dRes.json());
      setIrrigation(await iRes.json());

    } catch (err) {
      console.error("Weather fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchAll(location); }, [location, crop]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      setLocation(searchInput.trim());
      setSearchInput('');
    }
  };

  // --- RENDER ---
  return (
    <div className="pt-24 min-h-screen pb-12" style={{ background: 'linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 50%, #f0fdf4 100%)' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* --------- HEADER --------- */}
        <div className="mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight flex items-center gap-2">
              <Cloud className="w-8 h-8 text-blue-500" />
              {t('weather_title')}
            </h1>
            <p className="text-gray-700 mt-1">{t('weather_subtitle')}</p>
          </div>

          <div className="flex gap-3 items-center w-full md:w-auto">
            {/* Crop Select */}
            <select value={crop} onChange={(e) => setCrop(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg bg-white shadow-sm text-sm focus:ring-blue-500">
              {['Rice','Wheat','Cotton','Maize','Tomato','Chili','Potato','Sugarcane','Millets','Pulses','Groundnut','Turmeric'].map(c =>
                <option key={c} value={c}>{c}</option>
              )}
            </select>

            {/* Location Search */}
            <form onSubmit={handleSearch} className="flex relative flex-1 md:flex-none">
              <input type="text" placeholder={t('search_city')}
                className="w-full md:w-56 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 shadow-sm"
                value={searchInput} onChange={(e) => setSearchInput(e.target.value)} />
              <MapPin className="w-5 h-5 text-gray-600 absolute left-3 top-2.5" />
              <button type="submit" className="ml-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 shadow-sm transition">
                <Search className="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>

        {/* India-only error */}
        {indiaError && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl flex items-center gap-3">
            <AlertTriangle className="w-6 h-6 flex-shrink-0" />
            <p className="font-medium">{indiaError}</p>
          </div>
        )}

        {loading ? (
          <div className="flex flex-col justify-center items-center h-64 gap-4">
            <Loader2 className="w-12 h-12 animate-spin text-blue-600" />
            <p className="text-gray-700">{t('fetch_intel')} <strong>{location}</strong>...</p>
          </div>
        ) : !indiaError && (
          <div className="space-y-8">

            {/* ═══════════ SECTION 1: WEATHER + ALERTS ═══════════ */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1">
                <WeatherCard weather={weather} />
                {/* UV Index badge */}
                {weather?.uv_index && (
                  <div className="mt-3 bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-800 flex items-center gap-2">
                      <Sun className="w-4 h-4 text-yellow-500" /> {t('uv_index')}
                    </span>
                    <span className={`text-lg font-bold ${weather.uv_index > 8 ? 'text-red-600' : weather.uv_index > 5 ? 'text-orange-500' : 'text-green-600'}`}>
                      {weather.uv_index}
                    </span>
                  </div>
                )}
              </div>

              <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2 text-yellow-500" /> {t('active_alerts')}
                </h3>
                {alerts.length === 0 ? (
                  <div className="flex bg-green-50 text-green-800 p-4 rounded-xl border border-green-100 items-start">
                    <Info className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                    <p>{t('no_alerts')} <strong>{location}</strong>. {t('safe_farming')}</p>
                  </div>
                ) : (
                  <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
                    {alerts.map((a, i) => {
                      const c = riskColor(a.severity);
                      return (
                        <div key={i} className={`p-4 rounded-xl border ${c.bg} ${c.border} ${c.text}`}>
                          <div className="flex justify-between items-start mb-1">
                            <h4 className="font-bold flex items-center gap-2">
                              {a.type}
                              <span className={`text-xs text-white px-2 py-0.5 rounded-full ${c.badge}`}>{a.severity}</span>
                            </h4>
                            <span className="text-sm opacity-100">{a.date}</span>
                          </div>
                          <p className="text-sm font-medium mb-2">{a.message}</p>
                          <p className="text-xs bg-white/90 border border-black/5 p-2 rounded-lg"><strong>{t('action')}:</strong> {a.recommendation}</p>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>

            {/* ═══════════ SECTION 2: 7-DAY FORECAST ═══════════ */}
            <ForecastChart data={forecast} />

            {/* ═══════════ SECTION 3: HAZARD MONITOR ═══════════ */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Shield className="w-5 h-5 text-indigo-500" /> {t('hazard_monitor')} — {location}
              </h3>
              {hazards.length === 0 ? (
                <div className="flex bg-green-50 text-green-800 p-4 rounded-xl border border-green-100 items-start">
                  <Info className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
                  <p>{t('no_hazards')} <strong>{location}</strong>.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {hazards.map((h, i) => {
                    const c = riskColor(h.risk_level);
                    return (
                      <div key={i} className={`p-5 rounded-xl border-l-4 ${c.bg} ${c.border} ${c.text} shadow-sm`}>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-2xl">{h.icon}</span>
                          <div>
                            <h4 className="font-bold">{h.hazard}</h4>
                            <span className={`text-xs text-white px-2 py-0.5 rounded-full ${c.badge}`}>{h.risk_level} Risk</span>
                          </div>
                        </div>
                        <p className="text-sm mb-3">{h.description}</p>
                        <div className="text-xs bg-white/90 border border-black/5 p-2 rounded-lg">
                          <strong>{t('mitigation')}:</strong> {h.mitigation}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* ═══════════ SECTION 4: PEST + DISEASE + IRRIGATION ═══════════ */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

              {/* Pest Outbreak */}
              {pestRisk && (
                <div className={`rounded-2xl p-6 shadow-sm border ${riskColor(pestRisk.risk_level).bg} ${riskColor(pestRisk.risk_level).border}`}>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                      <Bug className="w-5 h-5 text-orange-500" /> {t('pest_risk')}
                    </h3>
                    <span className={`text-xs text-white px-2.5 py-1 rounded-full font-semibold ${riskColor(pestRisk.risk_level).badge}`}>
                      {pestRisk.risk_level}
                    </span>
                  </div>
                  <p className="text-sm text-gray-800 mb-1"><strong>Crop:</strong> {pestRisk.crop}</p>
                  <p className="text-sm text-gray-800 font-semibold mb-2">{pestRisk.identified_pest}</p>
                  <div className="text-xs bg-white/95 border border-black/5 p-3 rounded-lg text-gray-700">
                    <strong>Recommendation:</strong> {pestRisk.recommendation}
                  </div>
                </div>
              )}

              {/* Disease Risk */}
              {diseaseRisk && (
                <div className={`rounded-2xl p-6 shadow-sm border ${riskColor(diseaseRisk.risk_level).bg} ${riskColor(diseaseRisk.risk_level).border}`}>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                      <AlertTriangle className="w-5 h-5 text-purple-500" /> {t('disease_risk')}
                    </h3>
                    <span className={`text-xs text-white px-2.5 py-1 rounded-full font-semibold ${riskColor(diseaseRisk.risk_level).badge}`}>
                      {diseaseRisk.risk_level}
                    </span>
                  </div>
                  <p className="text-sm text-gray-800 mb-1"><strong>Crop:</strong> {diseaseRisk.crop}</p>
                  <p className="text-sm text-gray-800 font-semibold mb-2">{diseaseRisk.disease}</p>
                  <div className="text-xs bg-white/95 border border-black/5 p-3 rounded-lg text-gray-700">
                    <strong>Recommendation:</strong> {diseaseRisk.recommendation}
                  </div>
                </div>
              )}

              {/* Irrigation Advice */}
              {irrigation && (
                <div className={`rounded-2xl p-6 shadow-sm border ${riskColor(irrigation.urgency === 'High' ? 'High' : irrigation.urgency === 'Normal' ? 'Low' : 'Medium').bg} ${riskColor(irrigation.urgency === 'High' ? 'High' : irrigation.urgency === 'Normal' ? 'Low' : 'Medium').border}`}>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                      <Droplets className="w-5 h-5 text-blue-500" /> {t('irrigation_advice')}
                    </h3>
                    <span className={`text-xs text-white px-2.5 py-1 rounded-full font-semibold ${
                      irrigation.urgency === 'High' ? 'bg-red-600' : irrigation.urgency === 'Medium' ? 'bg-amber-500' : 'bg-green-500'
                    }`}>
                      {irrigation.urgency}
                    </span>
                  </div>
                  <p className="text-sm text-gray-800 mb-1"><strong>Crop:</strong> {irrigation.crop} ({irrigation.water_need_level} water need)</p>
                  <p className="text-sm text-gray-800 font-semibold mb-2">{irrigation.action}</p>
                  <div className="text-xs bg-white/95 border border-black/5 p-3 rounded-lg text-gray-700 space-y-1">
                    {irrigation.detailed_advice?.map((line, i) => (
                      <p key={i}>• {line}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>

          </div>
        )}
      </div>
    </div>
  );
};

export default WeatherIntelligence;
