import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { ArrowLeft, Building2, MapPin, Phone, Mail, Globe, Package, TrendingUp, User, FileText } from 'lucide-react';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { API_BASE_URL } from '../config/api';


delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const API = `${API_BASE_URL}/api/buyers`;

const BuyerProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [buyer, setBuyer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/${id}`)
      .then(res => setBuyer(res.data))
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

  if (!buyer) return null;

  return (
    <div className="max-w-5xl mx-auto pt-24 pb-16 px-4">
      {/* Back Button */}
      <button
        onClick={() => navigate('/entrepreneur')}
        className="flex items-center gap-2 text-gray-700 hover:text-green-600 transition-colors font-medium mb-8"
      >
        <ArrowLeft size={20} /> Back to Buyer Finder
      </button>

      {/* Header Card */}
      <div className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-gray-100 mb-8">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold uppercase tracking-wide">
            {buyer.business_type}
          </span>
          {buyer.annual_capacity && (
            <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-bold">
              Capacity: {buyer.annual_capacity}
            </span>
          )}
        </div>
        <h1 className="text-3xl md:text-4xl font-black text-gray-800 mb-2">{buyer.buyer_name}</h1>
        <p className="text-gray-700 font-medium text-lg flex items-center gap-2">
          <MapPin size={18} className="text-green-500" /> {buyer.city}, {buyer.district && `${buyer.district},`} {buyer.state}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-8">
          {/* Products Purchased */}
          <SectionCard title="Products Purchased" icon={<Package className="text-orange-500" />}>
            <div className="flex flex-wrap gap-2">
              {buyer.product_category.split(',').map((p, i) => (
                <span key={i} className="bg-orange-50 border border-orange-100 text-orange-700 px-4 py-2 rounded-xl text-sm font-bold">
                  {p.trim()}
                </span>
              ))}
            </div>
          </SectionCard>

          {/* Contact Information */}
          <SectionCard title="Contact Information" icon={<Phone className="text-green-600" />}>
            <div className="space-y-4">
              <ContactRow icon={<Phone size={18} className="text-green-500" />} label="Phone Number" value={buyer.phone_number} />
              <ContactRow icon={<Mail size={18} className="text-blue-500" />} label="Email" value={buyer.email} />
              {buyer.website && (
                <ContactRow
                  icon={<Globe size={18} className="text-purple-500" />}
                  label="Website"
                  value={
                    <a href={buyer.website} target="_blank" rel="noreferrer" className="text-purple-600 hover:underline font-bold">
                      {buyer.website}
                    </a>
                  }
                />
              )}
              <ContactRow icon={<MapPin size={18} className="text-red-500" />} label="Address" value={`${buyer.city}, ${buyer.district || ''}, ${buyer.state}`} />
            </div>
          </SectionCard>

          {/* About */}
          {buyer.buyer_description && (
            <SectionCard title="About" icon={<FileText className="text-gray-700" />}>
              <p className="text-gray-800 leading-relaxed font-medium">{buyer.buyer_description}</p>
            </SectionCard>
          )}
        </div>

        {/* Right Column */}
        <div className="space-y-8">
          {/* Map */}
          <SectionCard title="Buyer Location" icon={<MapPin className="text-red-500" />}>
            <div className="h-[350px] rounded-2xl overflow-hidden border border-gray-200">
              <MapContainer
                center={[buyer.latitude, buyer.longitude]}
                zoom={13}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[buyer.latitude, buyer.longitude]}>
                  <Popup>
                    <strong>{buyer.buyer_name}</strong><br />
                    {buyer.city}, {buyer.state}
                  </Popup>
                </Marker>
              </MapContainer>
            </div>
          </SectionCard>

          {/* Quick Stats */}
          <SectionCard title="Business Details" icon={<Building2 className="text-indigo-500" />}>
            <div className="space-y-4">
              <StatRow label="Business Type" value={buyer.business_type} />
              <StatRow label="City" value={buyer.city} />
              <StatRow label="District" value={buyer.district || "N/A"} />
              <StatRow label="State" value={buyer.state} />
              {buyer.annual_capacity && <StatRow label="Annual Capacity" value={buyer.annual_capacity} />}
            </div>
          </SectionCard>

          {/* Call to Action */}
          <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-3xl p-8 text-white text-center">
            <h3 className="text-2xl font-black mb-3">Connect with this Buyer</h3>
            <p className="text-green-100 text-sm mb-6">Reach out directly to discuss your produce</p>
            <div className="flex gap-4 justify-center">
              <a href={`tel:${buyer.phone_number}`} className="bg-white text-green-700 px-6 py-3 rounded-2xl font-bold flex items-center gap-2 hover:bg-green-50 transition-colors">
                <Phone size={18} /> Call Now
              </a>
              <a href={`mailto:${buyer.email}`} className="bg-white/10 border border-white/30 text-white px-6 py-3 rounded-2xl font-bold flex items-center gap-2 hover:bg-white/20 transition-colors">
                <Mail size={18} /> Email
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ContactRow = ({ icon, label, value }) => (
  <div className="flex items-start gap-3 bg-gray-50 p-3 rounded-xl">
    <div className="mt-0.5">{icon}</div>
    <div>
      <span className="text-xs font-bold text-gray-600 uppercase tracking-wider block">{label}</span>
      <span className="font-bold text-gray-800">{typeof value === 'string' ? value : value}</span>
    </div>
  </div>
);

const StatRow = ({ label, value }) => (
  <div className="flex justify-between items-center bg-indigo-50/50 p-3 rounded-xl border border-indigo-100/50">
    <span className="text-gray-800 font-medium">{label}</span>
    <span className="font-bold text-gray-800">{value}</span>
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

export default BuyerProfile;
