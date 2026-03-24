import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Leaf, User, Mail, Phone, MapPin, Map, Lock, ArrowRight, Home, Sprout, Loader2, Briefcase } from 'lucide-react';
import { API_BASE_URL } from '../config/api';

const Signup = () => {
    const [formData, setFormData] = useState({
        name: '', email: '', phone: '', password: '', confirmPassword: '',
        state: '', district: '', role: 'farmer'
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        if (formData.password !== formData.confirmPassword) { setError("Passwords do not match!"); return; }
        if (formData.password.length < 8) { setError("Password must be at least 8 characters."); return; }
        setLoading(true);
        try {
            // Step 1: Create user via API
            const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: formData.email, password: formData.password, name: formData.name,
                    phone: formData.phone, state: formData.state, district: formData.district, role: formData.role
                }),
            });
            if (response.ok) {
                navigate('/login', { state: { message: 'Account created! Please sign in.' } });
            } else {
                const data = await response.json();
                setError(data.detail || "Registration failed");
            }
        } catch (error) {
            setError("Network error. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const inputClass = "w-full pl-12 pr-4 py-3.5 bg-white/10 border border-white/20 text-white placeholder-gray-200 rounded-2xl focus:outline-none focus:border-leaf-400 focus:ring-2 focus:ring-leaf-400/20 transition-all text-sm";

    return (
        <div className="min-h-screen relative flex items-center justify-center p-4 overflow-hidden">
            <div className="absolute inset-0 z-0">
                <img src="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=1200&q=80" alt="Farm aerial" className="w-full h-full object-cover blur-sm scale-105" />
                <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
            </div>

            <div className="relative z-10 w-full max-w-lg animate-fade-in-up">
                <Link to="/login" className="mb-4 text-white text-sm font-medium hover:text-white flex items-center gap-1 transition-colors">← Back to Login</Link>

                <div className="bg-white/10 backdrop-blur-2xl border border-white/20 rounded-4xl p-7 shadow-2xl space-y-5">
                    <div className="text-center space-y-2">
                        <div className="w-12 h-12 bg-leaf-500/20 rounded-2xl flex items-center justify-center mx-auto">
                            <Sprout className="text-leaf-400" size={24} />
                        </div>
                        <h2 className="text-2xl font-extrabold text-white">Create Account</h2>
                        <p className="text-white/90 text-sm">Join the AgroNexus AI community</p>
                    </div>

                    {error && (
                        <div className="bg-red-500/20 border border-red-400/30 p-3 rounded-2xl">
                            <p className="text-red-300 text-sm font-medium">{error}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-3">
                        <div className="relative">
                            <User className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                            <input name="name" type="text" required className={inputClass} placeholder="Full Name" value={formData.name} onChange={handleChange} />
                        </div>
                        <div className="relative">
                            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                            <input name="email" type="email" required className={inputClass} placeholder="Email" value={formData.email} onChange={handleChange} />
                        </div>
                        <div className="relative">
                            <Phone className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                            <input name="phone" type="tel" required pattern="[0-9]{10}" className={inputClass} placeholder="Phone (10 digits)" value={formData.phone} onChange={handleChange} />
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            <div className="relative">
                                <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                                <input name="state" type="text" required className={inputClass} placeholder="State" value={formData.state} onChange={handleChange} />
                            </div>
                            <input name="district" type="text" required className="w-full px-4 py-3.5 bg-white/10 border border-white/20 text-white placeholder-gray-200 rounded-2xl focus:outline-none focus:border-leaf-400 text-sm" placeholder="District" value={formData.district} onChange={handleChange} />
                        </div>
                        <div className="relative">
                            <Briefcase className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                            <select name="role" required className={inputClass + " appearance-none"} value={formData.role} onChange={handleChange}>
                                <option value="farmer" className="text-dark">Farmer</option>
                                <option value="agri_business" className="text-dark">Agri-Business Owner</option>
                                <option value="expert" className="text-dark">Agricultural Expert</option>
                            </select>
                        </div>
                        <div className="relative">
                            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                            <input name="password" type="password" required minLength={8} className={inputClass} placeholder="Password (min 8 chars)" value={formData.password} onChange={handleChange} />
                        </div>
                        <div className="relative">
                            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={16} />
                            <input name="confirmPassword" type="password" required className={inputClass} placeholder="Confirm Password" value={formData.confirmPassword} onChange={handleChange} />
                        </div>

                        <button type="submit" disabled={loading}
                            className="w-full py-3.5 bg-gradient-to-r from-leaf-500 to-olive-500 text-white font-bold rounded-2xl shadow-lg hover:shadow-xl active:scale-[0.98] transition-all disabled:opacity-90 mt-2">
                            {loading ? <Loader2 className="animate-spin mx-auto" size={22} /> : 'Create Account'}
                        </button>
                    </form>

                    <p className="text-center text-white/90 text-sm">
                        Already have an account?{' '}
                        <Link to="/login" className="text-leaf-400 font-bold hover:underline">Sign In</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Signup;
