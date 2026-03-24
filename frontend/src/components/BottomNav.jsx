import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Sprout, Briefcase, Phone, User } from 'lucide-react';

const tabs = [
  { path: '/', icon: Home, label: 'Home' },
  { path: '/crop-plan', icon: Sprout, label: 'Crops' },
  { path: '/entrepreneur', icon: Briefcase, label: 'Business' },
  { path: '/agrivoice', icon: Phone, label: 'Voice' },
  { path: '/profile', icon: User, label: 'Profile' },
];

const BottomNav = () => {
  const location = useLocation();

  const isActive = (path) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-2xl border-t border-cream-400/30 shadow-bottom-nav"
         style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}>
      <div className="max-w-lg mx-auto flex items-center justify-around h-16">
        {tabs.map((tab) => {
          const active = isActive(tab.path);
          return (
            <Link
              key={tab.path}
              to={tab.path}
              className={`flex flex-col items-center justify-center gap-0.5 w-16 py-1 rounded-2xl transition-all duration-300 ${
                active
                  ? 'text-leaf-600 scale-105'
                  : 'text-muted hover:text-olive-500'
              }`}
            >
              {active && (
                <span className="absolute -top-0.5 w-8 h-1 bg-gradient-to-r from-leaf-500 to-olive-500 rounded-full" />
              )}
              <tab.icon size={active ? 24 : 22} strokeWidth={active ? 2.5 : 1.8} />
              <span className={`text-[10px] font-semibold ${active ? 'font-bold' : ''}`}>
                {tab.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNav;
