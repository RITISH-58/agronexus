import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { MapPin, Search, Navigation, User, Phone, Mail, Crosshair, Globe, ChevronLeft, ChevronRight, Building2, PackageSearch, ExternalLink } from 'lucide-react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { API_BASE_URL } from '../config/api';


// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const API = `${API_BASE_URL}/api`;

// Component to update map view when center changes
const MapUpdater = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] && center[1]) {
      map.setView(center, zoom || 6);
    }
  }, [center, zoom, map]);
  return null;
};

const BuyerFinderTab = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [buyers, setBuyers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [product, setProduct] = useState('');
  const [locationStr, setLocationStr] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const perPage = 50;

  // Default map center (Central India)
  const [mapCenter, setMapCenter] = useState([20.5937, 78.9629]);
  const [mapZoom, setMapZoom] = useState(5);

  const searchBuyers = useCallback(async (pageNum = 1) => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/buyers/search`, {
        params: { product, location: locationStr, page: pageNum, per_page: perPage }
      });
      setBuyers(data.buyers || []);
      setTotal(data.total || 0);
      setPage(pageNum);

      if (data.buyers && data.buyers.length > 0) {
        const firstWithCoords = data.buyers.find(b => b.latitude && b.longitude);
        if (firstWithCoords) {
          setMapCenter([firstWithCoords.latitude, firstWithCoords.longitude]);
          setMapZoom(locationStr ? 8 : 5);
        }
      }
    } catch (err) {
      console.error(err);
      setBuyers([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [product, locationStr]);

  useEffect(() => {
    searchBuyers(1);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    searchBuyers(1);
  };

  const totalPages = Math.ceil(total / perPage);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Search Bar */}
      <div className="glass rounded-3xl p-6 border-0">
        <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-4">
          <div className="lg:col-span-4 relative">
            <PackageSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600" size={20} />
            <input
              type="text"
              placeholder={t('search_product_ph')}
              className="w-full pl-11 pr-4 py-3.5 bg-white/90 border border-black/5 border border-white/50 rounded-2xl input-glow transition-all duration-300 text-base"
              value={product}
              onChange={(e) => setProduct(e.target.value)}
            />
          </div>
          <div className="lg:col-span-5 relative">
            <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600" size={20} />
            <input
              type="text"
              placeholder={t('search_location_ph')}
              className="w-full pl-11 pr-4 py-3.5 bg-white/90 border border-black/5 border border-white/50 rounded-2xl input-glow transition-all duration-300 text-base"
              value={locationStr}
              onChange={(e) => setLocationStr(e.target.value)}
            />
          </div>
          <div className="lg:col-span-3">
            <button type="submit" className="w-full bg-gradient-to-r from-agri-primary to-agri-secondary hover:shadow-[0_8px_20px_rgba(46,125,50,0.3)] hover:scale-[1.02] text-white font-bold py-3.5 rounded-2xl transition-all duration-300 flex justify-center items-center gap-2 h-full text-base">
              <Crosshair size={20} /> {t('find_buyers')}
            </button>
          </div>
        </form>
        {total > 0 && (
          <div className="mt-4 text-sm text-gray-700 font-medium">
            {t('found')} <span className="text-green-600 font-bold">{total}</span> {t('buyers')}
            {product && <> {t('for_text')} "<span className="text-gray-700 font-bold">{product}</span>"</>}
            {locationStr && <> {t('in_text')} "<span className="text-gray-700 font-bold">{locationStr}</span>"</>}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[40%_60%] gap-5">
        {/* Map View */}
        <div className="lg:sticky lg:top-5 h-[400px] lg:h-[calc(100vh-140px)] glass rounded-3xl overflow-hidden border-0 z-0 order-1 lg:order-none">
          <MapContainer center={mapCenter} zoom={mapZoom} style={{ height: '100%', width: '100%' }}>
            <MapUpdater center={mapCenter} zoom={mapZoom} />
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {buyers.map((buyer) => (
              buyer.latitude && buyer.longitude ? (
                <Marker key={buyer.id} position={[buyer.latitude, buyer.longitude]}>
                  <Popup>
                    <div className="font-sans min-w-[200px]">
                      <h3 className="font-bold text-gray-800 text-sm mb-1">{buyer.buyer_name}</h3>
                      <p className="text-green-600 font-semibold text-xs mb-2">{buyer.business_type}</p>
                      <div className="text-xs text-gray-800 space-y-1">
                        <p>📍 {buyer.city}, {buyer.state}</p>
                        <p>📦 {buyer.product_category}</p>
                        <p>📞 {buyer.phone_number}</p>
                      </div>
                      <button
                        onClick={() => navigate(`/buyer/${buyer.id}`)}
                        className="mt-2 text-xs bg-green-600 text-white px-3 py-1 rounded font-bold hover:bg-green-700"
                      >
                        {t('view_profile')}
                      </button>
                    </div>
                  </Popup>
                </Marker>
              ) : null
            ))}
          </MapContainer>
        </div>

        {/* Buyer List */}
        <div className="flex flex-col gap-4 order-2 lg:order-none">
          <div className="grid grid-cols-1 gap-4">
            {loading ? (
              <>
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="glass border-0 rounded-2xl p-5 animate-pulse">
                    <div className="h-5 bg-gray-200 rounded w-3/4 mb-3"></div>
                    <div className="h-4 bg-gray-100 rounded w-1/2 mb-4"></div>
                    <div className="grid grid-cols-2 gap-3">
                      <div className="h-3 bg-gray-100 rounded"></div>
                      <div className="h-3 bg-gray-100 rounded"></div>
                    </div>
                  </div>
                ))}
              </>
            ) : buyers.length === 0 ? (
              <div className="glass rounded-3xl p-8 text-center border-0 flex-1 flex flex-col justify-center items-center text-gray-600">
                <User size={48} className="mb-4 opacity-30" />
                <p className="font-medium text-lg">{t('no_buyers_found')}</p>
                <p className="text-sm mt-1">{t('try_searching_buyer')}</p>
              </div>
            ) : (
              buyers.map((buyer) => (
                <div
                  key={buyer.id}
                  onClick={() => navigate(`/buyer/${buyer.id}`)}
                  className="glass card-hover border-0 rounded-2xl p-5 cursor-pointer group"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-gray-800 text-lg group-hover:text-green-700 transition-colors">{buyer.buyer_name}</h4>
                      <span className="inline-block bg-green-100 text-green-700 text-xs font-bold px-2.5 py-0.5 rounded-full mt-1">
                        {buyer.business_type}
                      </span>
                    </div>
                    <ExternalLink size={18} className="text-gray-300 group-hover:text-green-500 transition-colors mt-1" />
                  </div>

                  <div className="grid grid-cols-2 gap-y-3 gap-x-4 mt-4 text-sm">
                    <div>
                      <span className="text-gray-600 text-xs font-bold uppercase tracking-wider block">{t('products_label')}</span>
                      <span className="font-semibold text-gray-700">{buyer.product_category}</span>
                    </div>
                    <div>
                      <span className="text-gray-600 text-xs font-bold uppercase tracking-wider block">{t('location_label')}</span>
                      <span className="font-semibold text-gray-700">{buyer.city}, {buyer.state}</span>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-gray-50 flex gap-4">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-gray-700">
                      <Phone size={14} className="text-green-500" /> {buyer.phone_number}
                    </div>
                    {buyer.annual_capacity && (
                      <div className="flex items-center gap-1 text-xs font-bold text-gray-700">
                        <Building2 size={14} className="text-blue-500" /> {buyer.annual_capacity}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-between items-center glass rounded-2xl p-4 border-0 mt-2 mx-auto w-full max-w-sm sticky bottom-4 z-10">
              <button
                disabled={page <= 1}
                onClick={() => searchBuyers(page - 1)}
                className="flex items-center gap-1 text-sm font-bold text-gray-800 hover:text-green-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft size={18} /> {t('previous')}
              </button>
              <span className="text-sm font-bold text-gray-700">
                {t('page')} <span className="text-green-600">{page}</span> {t('of')} {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => searchBuyers(page + 1)}
                className="flex items-center gap-1 text-sm font-bold text-gray-800 hover:text-green-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                {t('next')} <ChevronRight size={18} />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BuyerFinderTab;
