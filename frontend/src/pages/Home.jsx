import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Sprout, Briefcase, Landmark, Users, ChevronRight, Wheat, TrendingUp, Star } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

/* Unsplash agriculture images */
const IMAGES = {
  wheat: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&q=80',
  rice: 'https://images.unsplash.com/photo-1536304993881-070f82905bae?w=600&q=80',
  vegetables: 'https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=600&q=80',
  dairy: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=600&q=80',
  aerial: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=600&q=80',
  farm: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&q=80',
  organic: 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=600&q=80',
  tractor: 'https://images.unsplash.com/photo-1530267981375-f0de937f5f13?w=600&q=80',
};

const featureCards = [
  {
    title: 'Crop Intelligence',
    desc: 'AI-powered predictions for yield, risk, and fertilizer plans',
    icon: Sprout,
    path: '/crop-plan',
    img: IMAGES.aerial,
    gradient: 'from-leaf-600/90 to-olive-600/80',
    badge: 'ML Powered',
  },
  {
    title: 'Entrepreneur',
    desc: 'Convert farm produce into profitable agri-ventures',
    icon: Briefcase,
    path: '/entrepreneur',
    img: IMAGES.organic,
    gradient: 'from-wheat-600/90 to-wheat-800/80',
    badge: 'Business PRO',
  },

  {
    title: 'Govt Schemes',
    desc: 'Find matching government subsidies & programs',
    icon: Landmark,
    path: '/schemes',
    img: IMAGES.farm,
    gradient: 'from-olive-600/90 to-leaf-800/80',
    badge: 'Updated',
  },
  {
    title: 'Find Buyers',
    desc: 'Connect with nearby buyers and sell your crops easily',
    icon: Users,
    path: '/buyers',
    img: IMAGES.vegetables,
    gradient: 'from-emerald-600/90 to-yellow-500/80',
    badge: '🆕 MARKET',
  },
];

const Home = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const today = new Date();
  const dateStr = today.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short' });

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-white to-green-50 px-5 pt-8 pb-6 max-w-lg mx-auto flex flex-col gap-8 animate-fade-in-up">
      
      {/* ── Header ── */}
      <div className="flex items-center justify-between z-10">
        <div>
          <p className="text-sm text-leaf-700/80 font-bold uppercase tracking-wider">{dateStr}</p>
          <h1 className="text-3xl font-black text-dark tracking-tight mt-1 drop-shadow-sm">
            Hello, {user?.full_name?.split(' ')[0] || 'Farmer'} 👋
          </h1>
        </div>
        <Link to="/profile" className="w-12 h-12 bg-gradient-to-br from-leaf-400 to-olive-500 rounded-2xl flex items-center justify-center shadow-lg hover:shadow-xl hover:scale-105 active:scale-95 transition-all">
          <span className="text-white font-black text-lg drop-shadow-sm">
            {user?.full_name?.charAt(0)?.toUpperCase() || 'F'}
          </span>
        </Link>
      </div>

      {/* ── Premium Hero Card ── */}
      <div className="relative z-10 w-full group animate-fade-in">
        <div className="relative overflow-hidden rounded-[24px] bg-gradient-to-br from-[#4CAF50] via-[#81C784] to-[#E8F5E9] p-6 shadow-[0_8px_30px_rgba(76,175,80,0.25)] border border-white/40">
          {/* Subtle farming background image overlay */}
          <div 
            className="absolute inset-0 opacity-10 mix-blend-overlay bg-cover bg-center pointer-events-none"
            style={{ backgroundImage: `url(${IMAGES.aerial})` }}
          />
          {/* Glassmorphism gradient blobs behind text */}
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/30 rounded-full blur-[40px] pointer-events-none" />
          <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-green-900/10 rounded-full blur-[30px] pointer-events-none" />

          <div className="relative z-10 flex flex-col justify-between h-full space-y-4">
            <div>
              <div className="inline-flex items-center justify-center p-2 bg-white/20 backdrop-blur-md rounded-xl mb-3 shadow-sm border border-white/20">
                <span className="text-xl">🌿</span>
              </div>
              <h2 className="text-2xl font-black text-white tracking-tight drop-shadow-sm leading-tight mb-2">
                Smart Farming <br/> Starts Here
              </h2>
              <p className="text-[13px] font-medium text-white/90 leading-relaxed drop-shadow-sm max-w-[90%]">
                AI-powered insights for better yield, smarter decisions, and higher profits.
              </p>
            </div>
            
            <button 
              onClick={() => navigate('/crop-plan')}
              className="mt-2 self-start bg-white text-green-700 font-bold text-sm px-6 py-3 rounded-full shadow-md hover:shadow-lg hover:bg-green-50 transform hover:-translate-y-0.5 transition-all active:scale-95 flex items-center gap-2"
            >
              Get Started <ChevronRight size={16} strokeWidth={3} />
            </button>
          </div>
        </div>
      </div>

      {/* ── Features Grid ── */}
      <div className="z-10 flex-1">
        <h2 className="text-xl font-black text-dark tracking-tight mb-4 flex items-center gap-2">
          Explore Features <ChevronRight className="text-leaf-500" size={20} strokeWidth={3} />
        </h2>
        <div className="grid grid-cols-2 gap-4">
          {featureCards.map((card, i) => (
            <div
              key={card.title}
              onClick={() => navigate(card.path)}
              className="img-card rounded-[28px] h-48 cursor-pointer active:scale-[0.96] transition-all animate-fade-in-up group"
              style={{ animationDelay: `${0.1 + i * 0.08}s`, animationFillMode: 'backwards' }}
            >
              <img src={card.img} alt={card.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" loading="lazy" />
              <div className={`absolute inset-0 bg-gradient-to-t ${card.gradient} z-[1] opacity-90`} />
              <div className="absolute inset-x-0 bottom-0 z-10 p-4 flex flex-col justify-end h-full mix-blend-normal">
                <div className="mb-auto self-start">
                  <span className="inline-block bg-white/20 backdrop-blur-md text-white text-[10px] font-black uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm border border-white/10">
                    {card.badge}
                  </span>
                </div>
                <p className="text-white font-black text-base leading-tight drop-shadow-md mb-1">{card.title}</p>
                <p className="text-white text-[10px] font-medium leading-snug drop-shadow-sm">{card.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Tip of the Day ── */}
      <div className="w-full z-10 transition-transform hover:scale-[1.01] active:scale-95 cursor-pointer">
        <div className="relative overflow-hidden bg-gradient-to-br from-olive-500 to-leaf-600 rounded-[28px] p-5 shadow-[0_8px_30px_rgba(107,142,35,0.3)]">
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10 mix-blend-overlay"></div>
          <div className="absolute -top-12 -right-12 w-32 h-32 bg-white/20 rounded-full blur-[30px]"></div>
          
          <div className="relative z-10 flex flex-col gap-2.5">
            <div className="flex items-center gap-2">
              <div className="bg-white/20 p-1.5 rounded-xl backdrop-blur-sm">
                <Wheat size={18} className="text-white" strokeWidth={2.5} />
              </div>
              <span className="text-[11px] font-black text-white/90 uppercase tracking-widest drop-shadow-sm">Daily Insight</span>
            </div>
            <p className="text-sm font-semibold text-white/95 leading-relaxed drop-shadow-sm">
              Intercropping legumes with cereals can boost soil nitrogen by 30%, noticeably reducing your fertilizer dependencies. 🌱
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
