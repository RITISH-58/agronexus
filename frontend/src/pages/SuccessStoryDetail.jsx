import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, MapPin, BadgeIndianRupee, TrendingUp, Package, Users, ShieldCheck, CheckCircle2, Phone, Mail, BookOpen, Sprout } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';

const SuccessStoryDetail = () => {
  const { id } = useParams();
  const API = `${API_BASE_URL}/api/success-stories`;
  const navigate = useNavigate();
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/${id}`)
      .then(res => setStory(res.data))
      .catch(err => {
        console.error(err);
        navigate('/entrepreneur');
      })
      .finally(() => setLoading(false));
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-32">
        <div className="animate-spin h-12 w-12 border-4 border-green-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!story) return null;

  return (
    <div className="max-w-5xl mx-auto pt-24 pb-16 px-4">
      {/* Back Button */}
      <button
        onClick={() => navigate('/entrepreneur')}
        className="flex items-center gap-2 text-gray-700 hover:text-green-600 transition-colors font-medium mb-8"
      >
        <ArrowLeft size={20} /> Back to Success Stories
      </button>

      {/* Hero Header */}
      <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-gray-100 mb-8">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold uppercase tracking-wide">
            {story.crop}
          </span>
          {story.government_scheme_used && (
            <span className="bg-amber-100 text-amber-700 px-3 py-1 rounded-full text-sm font-bold flex items-center gap-1">
              <ShieldCheck size={14} /> {story.government_scheme_used}
            </span>
          )}
        </div>
        <h1 className="text-3xl md:text-4xl font-black text-gray-800 mb-2">{story.farmer_name}</h1>
        <p className="text-xl font-bold text-green-600 mb-3">{story.business_type}</p>
        <div className="flex items-center gap-2 text-gray-700 font-medium">
          <MapPin size={18} className="text-red-400" /> {story.district}, {story.state}
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-8 pt-8 border-t border-gray-100">
          <Metric title="Investment" value={story.investment} icon={<BadgeIndianRupee className="text-amber-500" size={22} />} />
          <Metric title="Monthly Income" value={story.monthly_income} icon={<TrendingUp className="text-green-500" size={22} />} />
          <Metric title="Yearly Income" value={story.yearly_income} icon={<BadgeIndianRupee className="text-blue-500" size={22} />} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-8">

          {/* Story */}
          {story.story && (
            <SectionCard title="Farmer's Story" icon={<BookOpen className="text-blue-500" />}>
              <p className="text-gray-800 leading-relaxed font-medium">{story.story}</p>
            </SectionCard>
          )}

          {/* Products Sold */}
          <SectionCard title="Products Sold" icon={<Package className="text-orange-500" />}>
            <div className="flex flex-wrap gap-2">
              {story.products_sold && story.products_sold.map((p, i) => (
                <span key={i} className="bg-orange-50 border border-orange-100 text-orange-700 px-4 py-2 rounded-xl text-sm font-bold">
                  {p}
                </span>
              ))}
            </div>
          </SectionCard>

          {/* Buyers Connected */}
          <SectionCard title="Buyers Connected" icon={<Users className="text-purple-500" />}>
            <div className="space-y-3">
              {story.buyers_connected && story.buyers_connected.map((b, i) => (
                <div key={i} className="flex items-center gap-3 bg-purple-50/50 p-3 rounded-xl border border-purple-100/50">
                  <Users size={16} className="text-purple-500 shrink-0" />
                  <span className="font-bold text-gray-800">{b}</span>
                </div>
              ))}
            </div>
          </SectionCard>

          {/* Government Scheme */}
          {story.government_scheme_used && (
            <SectionCard title="Government Scheme Used" icon={<ShieldCheck className="text-emerald-600" />}>
              <div className="bg-emerald-50 border border-emerald-100 p-5 rounded-2xl flex items-center gap-4">
                <ShieldCheck className="text-emerald-500 shrink-0" size={28} />
                <div>
                  <span className="font-black text-gray-800 text-xl">{story.government_scheme_used}</span>
                  <p className="text-sm text-emerald-700 font-medium mt-1">Government subsidy/support scheme</p>
                </div>
              </div>
            </SectionCard>
          )}
        </div>

        {/* Right Column */}
        <div className="space-y-8">

          {/* Implementation Steps */}
          <SectionCard title="Step-by-Step Implementation" icon={<CheckCircle2 className="text-orange-500" />}>
            <div className="space-y-4">
              {story.implementation_steps && story.implementation_steps.map((step, i) => (
                <div key={i} className="flex gap-4 items-start">
                  <div className="flex items-center justify-center w-9 h-9 rounded-full bg-orange-100 text-orange-600 font-black text-sm shrink-0 shadow-sm">
                    {i + 1}
                  </div>
                  <div className="bg-white p-4 rounded-2xl shadow-sm border border-orange-100 text-gray-700 font-medium flex-1">
                    {step}
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>

          {/* Contact Details */}
          <SectionCard title="Contact Details" icon={<Phone className="text-green-600" />}>
            <div className="space-y-4">
              {story.contact_phone && (
                <div className="flex items-center gap-3 bg-gray-50 p-4 rounded-xl">
                  <Phone size={20} className="text-green-500" />
                  <div>
                    <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block">Phone</span>
                    <span className="font-bold text-gray-800">{story.contact_phone}</span>
                  </div>
                </div>
              )}
              {story.contact_email && (
                <div className="flex items-center gap-3 bg-gray-50 p-4 rounded-xl">
                  <Mail size={20} className="text-blue-500" />
                  <div>
                    <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block">Email</span>
                    <a href={`mailto:${story.contact_email}`} className="font-bold text-blue-600 hover:underline">{story.contact_email}</a>
                  </div>
                </div>
              )}
            </div>
          </SectionCard>

          {/* CTA */}
          <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-3xl p-8 text-white text-center">
            <Sprout size={36} className="mx-auto mb-3 opacity-80" />
            <h3 className="text-2xl font-black mb-2">Inspired by this Story?</h3>
            <p className="text-green-100 text-sm mb-5">Explore business blueprints for {story.crop}</p>
            <button
              onClick={() => navigate('/entrepreneur')}
              className="bg-white text-green-700 px-8 py-3 rounded-2xl font-bold hover:bg-green-50 transition-colors"
            >
              Explore Business Plans →
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};

const Metric = ({ title, value, icon }) => (
  <div>
    <div className="flex items-center gap-2 mb-2">
      {icon}
      <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">{title}</span>
    </div>
    <div className="text-xl md:text-2xl font-black text-gray-800">{value}</div>
  </div>
);

const SectionCard = ({ title, icon, children }) => (
  <div className="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-gray-100">
    <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-100">
      <div className="p-2 bg-gray-50 rounded-xl">{icon}</div>
      <h2 className="text-xl font-bold text-gray-800">{title}</h2>
    </div>
    {children}
  </div>
);

export default SuccessStoryDetail;
