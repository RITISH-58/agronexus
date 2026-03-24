import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import Home from './pages/Home';
import Entrepreneur from './pages/Entrepreneur';
import BusinessDetails from './pages/BusinessDetails';
import BuyerProfile from './pages/BuyerProfile';
import SuccessStoryDetail from './pages/SuccessStoryDetail';
import Schemes from './pages/Schemes';
import Login from './pages/Login';
import Signup from './pages/Signup';
import OtpVerification from './pages/OtpVerification';
import Profile from './pages/Profile';
import LandDetails from './pages/LandDetails';
import CropPlanForm from './components/CropPlanForm';
import CropDashboard from './pages/CropDashboard';
import AgriVoice from './pages/AgriVoice';
import WhatsAppDashboard from './pages/WhatsAppDashboard';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import BottomNav from './components/BottomNav';

const pageVariants = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35, ease: 'easeOut' } },
  exit: { opacity: 0, y: -10, transition: { duration: 0.2 } },
};

function AnimatedRoutes() {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const isAuthPage = ['/login', '/signup', '/verify-otp'].includes(location.pathname);

  return (
    <>
      {/* Global Premium Background Layers */}
      <div className="fixed inset-0 -z-50 pointer-events-none overflow-hidden">
        {/* Radial Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[500px] bg-white/90 border border-black/5 rounded-full blur-[100px]" />
        
        {/* Blurred Agriculture Image Overlay */}
        <div 
          className="absolute top-0 left-0 w-full h-[50vh] opacity-[0.10] bg-[url('https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800&q=80')] bg-cover bg-center" 
          style={{ filter: 'blur(24px)' }} 
        />
        
        {/* Top Fade overlay so the image naturally blends into the gradient */}
        <div className="absolute top-0 left-0 w-full h-[50vh] bg-gradient-to-b from-transparent to-[#E8F5E9] opacity-80" />
        
        {/* Vignette Edges */}
        <div className="absolute inset-0 shadow-[inset_0_0_120px_rgba(0,0,0,0.03)]" />
        
        {/* Subtle Noise Texture */}
        <div className="absolute inset-0 bg-noise opacity-[0.015] mix-blend-overlay" />
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={location.pathname}
          variants={pageVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          className={`min-h-screen ${!isAuthPage ? 'pb-safe' : ''}`}
        >
          <Routes location={location} key={location.pathname}>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/verify-otp" element={<OtpVerification />} />

            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<Home />} />
              <Route path="/entrepreneur" element={<Entrepreneur />} />
              <Route path="/business-details/:id" element={<BusinessDetails />} />
              <Route path="/buyer/:id" element={<BuyerProfile />} />
              <Route path="/success-story/:id" element={<SuccessStoryDetail />} />
              <Route path="/schemes" element={<Schemes />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/profile/add-land" element={<LandDetails />} />
              <Route path="/crop-plan" element={<CropPlanForm />} />
              <Route path="/crop-dashboard/:planId" element={<CropDashboard />} />
              <Route path="/agrivoice" element={<AgriVoice />} />
              <Route path="/whatsapp" element={<WhatsAppDashboard />} />
            </Route>
          </Routes>
        </motion.div>
      </AnimatePresence>

      {/* Bottom Nav */}
      {isAuthenticated && !isAuthPage && <BottomNav />}
    </>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AnimatedRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
