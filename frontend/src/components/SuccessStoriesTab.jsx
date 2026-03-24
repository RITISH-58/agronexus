import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Sprout, BadgeIndianRupee, TrendingUp, MapPin, ChevronLeft, ChevronRight, BookOpen, ShieldCheck, User } from 'lucide-react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { API_BASE_URL } from '../config/api';


const API = `${API_BASE_URL}/api/success-stories`;

const CROP_FILTERS = [
  "All", "Rice", "Tomato", "Turmeric", "Potato", "Groundnut", "Chilli",
  "Millets", "Cotton", "Banana", "Coconut", "Mango", "Maize", "Soybean", "Wheat", "Sugarcane"
];

const SuccessStoriesTab = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeCrop, setActiveCrop] = useState('All');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const perPage = 12;

  const fetchStories = useCallback(async (crop, pg) => {
    setLoading(true);
    try {
      const params = { page: pg, per_page: perPage };
      if (crop && crop !== 'All') params.crop = crop;
      const { data } = await axios.get(API, { params });
      setStories(data.stories || []);
      setTotal(data.total || 0);
    } catch (err) {
      console.error(err);
      setStories([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStories(activeCrop, page);
  }, [activeCrop, page, fetchStories]);

  const handleCropFilter = (crop) => {
    setActiveCrop(crop);
    setPage(1);
  };

  const totalPages = Math.ceil(total / perPage);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Crop Filter Pills */}
      <div className="glass rounded-3xl p-5 border-0">
        <div className="flex items-center gap-2 mb-4">
          <Sprout size={20} className="text-green-500" />
          <span className="text-sm font-bold text-gray-700 uppercase tracking-wider">{t('filter_by_crop')}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {CROP_FILTERS.map(crop => (
            <button
              key={crop}
              onClick={() => handleCropFilter(crop)}
              className={`px-4 py-2 rounded-xl text-sm font-bold transition-all duration-300 ${
                activeCrop === crop
                  ? 'bg-gradient-to-r from-agri-primary to-agri-secondary text-white shadow-md shadow-agri-primary/20 scale-105'
                  : 'bg-white/90 border border-black/5 text-gray-800 hover:bg-white/90 hover:scale-105 hover:text-agri-primary shadow-sm'
              }`}
            >
              {crop}
            </button>
          ))}
        </div>
        {total > 0 && (
          <p className="mt-3 text-sm text-gray-700">
            {t('showing')} <span className="font-bold text-green-600">{total}</span> {t('success_stories')}
            {activeCrop !== 'All' && <> {t('for_text')} <span className="font-bold text-gray-700">{activeCrop}</span></>}
          </p>
        )}
      </div>

      {/* Loading */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="glass rounded-2xl p-6 border-0 animate-pulse">
              <div className="h-5 bg-gray-200 rounded w-3/4 mb-3"></div>
              <div className="h-4 bg-gray-100 rounded w-1/2 mb-4"></div>
              <div className="space-y-2">
                <div className="h-3 bg-gray-100 rounded"></div>
                <div className="h-3 bg-gray-100 rounded w-2/3"></div>
              </div>
            </div>
          ))}
        </div>
      ) : stories.length === 0 ? (
        <div className="glass rounded-3xl p-12 text-center border-0">
          <BookOpen size={48} className="mx-auto mb-4 text-gray-300" />
          <p className="text-xl font-medium text-gray-600">{t('no_stories_found')}</p>
          <p className="text-sm text-gray-600 mt-2">{t('try_different_crop')}</p>
        </div>
      ) : (
        <>
          {/* Story Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {stories.map(story => (
              <div
                key={story.id}
                onClick={() => navigate(`/success-story/${story.id}`)}
                className="glass card-hover rounded-2xl p-6 border-0 cursor-pointer group flex flex-col h-full"
              >
                {/* Top badges */}
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className="bg-green-100 text-green-700 text-xs font-bold px-2.5 py-1 rounded-full">{story.crop}</span>
                  {story.government_scheme_used && (
                    <span className="bg-amber-100 text-amber-700 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
                      <ShieldCheck size={12} /> {story.government_scheme_used}
                    </span>
                  )}
                </div>

                {/* Name & business */}
                <h3 className="text-lg font-bold text-gray-800 group-hover:text-green-700 transition-colors mb-1">{story.farmer_name}</h3>
                <p className="text-sm font-semibold text-green-600 mb-3">{story.business_type}</p>

                {/* Location */}
                <div className="flex items-center gap-1.5 text-xs text-gray-700 mb-4">
                  <MapPin size={14} className="text-red-400" />
                  <span className="font-medium">{story.district}, {story.state}</span>
                </div>

                {/* Key metrics */}
                <div className="grid grid-cols-2 gap-3 mb-5">
                  <MetricBadge label={t('investment')} value={story.investment} icon={<BadgeIndianRupee size={14} />} color="text-gray-800" />
                  <MetricBadge label={t('monthly_income')} value={story.monthly_income} icon={<TrendingUp size={14} />} color="text-green-600" />
                </div>

                {/* CTA */}
                <div className="mt-auto pt-4 border-t border-gray-100 flex justify-between items-center">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-gray-600">
                    <User size={14} /> {story.products_sold?.length || 0} {t('products_label')}
                  </div>
                  <span className="text-sm font-bold text-green-600 group-hover:translate-x-1 transition-transform">
                    {t('view_full_story')}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-between items-center glass rounded-2xl p-4 border-0">
              <button
                disabled={page <= 1}
                onClick={() => setPage(p => p - 1)}
                className="flex items-center gap-1 text-sm font-bold text-gray-800 hover:text-green-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft size={18} /> {t('previous')}
              </button>
              <span className="text-sm font-bold text-gray-700">
                {t('page')} <span className="text-green-600">{page}</span> {t('of')} {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(p => p + 1)}
                className="flex items-center gap-1 text-sm font-bold text-gray-800 hover:text-green-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                {t('next')} <ChevronRight size={18} />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

const MetricBadge = ({ label, value, icon, color }) => (
  <div className="bg-gray-50 p-3 rounded-xl">
    <span className="text-[10px] font-bold text-gray-600 uppercase tracking-wider block mb-1">{label}</span>
    <div className={`flex items-center gap-1 font-bold text-sm ${color}`}>
      {icon} {value}
    </div>
  </div>
);

export default SuccessStoriesTab;
