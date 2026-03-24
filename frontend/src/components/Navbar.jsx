import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Menu, X, Leaf, Sprout, Briefcase, Landmark, LogIn, UserPlus, LogOut, User, CloudSun, Microscope, Globe, Phone } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, logout, user } = useAuth();
  const { t, i18n } = useTranslation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleLanguageChange = (e) => {
    i18n.changeLanguage(e.target.value);
  };

  const navLinks = [
    { name: t('dashboard'), path: '/', icon: <Leaf className="w-4 h-4 mr-2" /> },
    { name: t('crop_intel'), path: '/crop-plan', icon: <Microscope className="w-4 h-4 mr-2" /> },
    { name: t('entrepreneur'), path: '/entrepreneur', icon: <Briefcase className="w-4 h-4 mr-2" /> },
    { name: t('schemes'), path: '/schemes', icon: <Landmark className="w-4 h-4 mr-2" /> },
    { name: 'AgriVoice', path: '/agrivoice', icon: <Phone className="w-4 h-4 mr-2" /> },
  ];

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-white/80 backdrop-blur-xl border-b border-white/40 shadow-sm transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
            <div className="flex-shrink-0 flex items-center space-x-2 cursor-pointer transition-transform hover:scale-105" onClick={() => navigate('/')}>
              <Sprout className="h-8 w-8 text-green-600" />
              <span className="font-extrabold text-2xl tracking-tight text-gray-900">
                AgroNexus <span className="text-green-500">AI</span>
              </span>
            </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-2">
            {navLinks.map((link) => (
                <Link
                key={link.name}
                to={link.path}
                className={`flex items-center px-4 py-2 rounded-xl text-sm transition-all duration-300 overflow-hidden relative group ${
                    isActive(link.path)
                    ? 'text-agri-primary font-bold bg-agri-primary/5'
                    : 'text-gray-800 font-medium hover:text-agri-primary hover:bg-agri-bgGradientStart/50'
                }`}
                >
                {isActive(link.path) && (
                   <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-agri-primary rounded-t-md animate-slide-up"></span>
                )}
                {/* Optional icon inclusion: {link.icon} */}
                {link.name}
                </Link>
            ))}
          </div>

          {/* Auth Buttons & Language */}
          <div className="hidden md:flex items-center space-x-3">
            <div className="flex items-center bg-gray-50 border border-gray-200 rounded-full px-3 py-1 mr-2">
              <Globe className="w-4 h-4 text-gray-700 mr-2" />
              <select 
                value={i18n.language} 
                onChange={handleLanguageChange}
                className="bg-transparent text-sm font-medium text-gray-700 outline-none cursor-pointer"
              >
                <option value="en">English</option>
                <option value="hi">हिंदी (Hindi)</option>
                <option value="te">తెలుగు (Telugu)</option>
                <option value="ta">தமிழ் (Tamil)</option>
              </select>
            </div>
            {isAuthenticated ? (
              <>
                <Link
                  to="/profile"
                  className="flex items-center px-4 py-2 rounded-full text-sm font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                  <User className="w-4 h-4 mr-2" />
                  {user?.full_name?.split(' ')[0] || t('profile')}
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center px-4 py-2 rounded-full text-sm font-semibold text-white bg-red-500 hover:bg-red-600 shadow-sm transition-colors"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  {t('logout')}
                </button>
              </>
            ) : (
              <>
                <Link 
                  to="/login"
                  className="flex items-center px-4 py-2 rounded-full text-sm font-semibold text-green-700 bg-white border border-green-600 hover:bg-green-50 transition-colors shadow-sm"
                >
                  <LogIn className="w-4 h-4 mr-2" />
                  Login
                </Link>
                <Link 
                  to="/signup"
                  className="flex items-center px-4 py-2 rounded-full text-sm font-semibold text-white bg-green-600 hover:bg-green-700 shadow-sm transition-colors"
                >
                  <UserPlus className="w-4 h-4 mr-2" />
                  Signup
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-green-600 focus:outline-none p-2"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden bg-white/95 backdrop-blur-xl border-b border-white/40 shadow-sm absolute w-full left-0 mt-0">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                className={`flex items-center px-3 py-3 rounded-xl text-base transition-colors ${
                  isActive(link.path)
                    ? 'bg-agri-primary/10 text-agri-primary font-bold border-l-4 border-agri-primary'
                    : 'text-gray-800 font-medium hover:bg-agri-bgGradientStart hover:text-agri-primary'
                }`}
                onClick={() => setIsOpen(false)}
              >
                {link.icon}
                {link.name}
              </Link>
            ))}
            
            <div className="border-t border-gray-200 mt-4 pt-4 pb-2 space-y-2">
              <div className="flex w-full items-center px-3 py-2 rounded-md text-base font-medium text-gray-700">
                <Globe className="w-5 h-5 mr-3 text-gray-600" />
                <select 
                  value={i18n.language} 
                  onChange={handleLanguageChange}
                  className="bg-transparent w-full text-base font-medium text-gray-700 outline-none cursor-pointer"
                >
                  <option value="en">English</option>
                  <option value="hi">हिंदी</option>
                  <option value="te">తెలుగు</option>
                  <option value="ta">தமிழ்</option>
                </select>
              </div>
              {isAuthenticated ? (
                <>
                  <Link
                    to="/profile"
                    className="flex w-full items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 bg-gray-50 hover:bg-gray-100"
                    onClick={() => setIsOpen(false)}
                  >
                    <User className="w-5 h-5 mr-3 text-gray-600" />
                    {t('profile')}
                  </Link>
                  <button
                    onClick={() => { handleLogout(); setIsOpen(false); }}
                    className="flex w-full text-left items-center px-3 py-2 rounded-md text-base font-medium text-red-600 bg-red-50 hover:bg-red-100"
                  >
                    <LogOut className="w-5 h-5 mr-3" />
                    {t('logout')}
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="flex w-full items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-green-600"
                    onClick={() => setIsOpen(false)}
                  >
                    <LogIn className="w-5 h-5 mr-3 text-gray-600" />
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="flex w-full items-center px-3 py-2 rounded-md text-base font-medium text-green-700 bg-green-50 hover:bg-green-100"
                    onClick={() => setIsOpen(false)}
                  >
                    <UserPlus className="w-5 h-5 mr-3" />
                    Create Account
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
