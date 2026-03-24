import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { User, Lock, Loader2, Eye, EyeOff, Sprout } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { API_BASE_URL } from '../config/api';


const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [showForm, setShowForm] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuth();
    const successMessage = location.state?.message;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                login(data.user, data.access_token);
                navigate('/');
            } else {
                const data = await response.json();
                setError(data.detail === "Incorrect email or password" ? "Invalid email or password." : data.detail || "Invalid email or password.");
            }
        } catch (error) {
            console.error("Login error:", error);
            setError("Unable to connect to server.");
        } finally {
            setLoading(false);
        }
    };

    // Onboarding hero screen
    if (!showForm) {
        return (
            <div className="min-h-screen relative flex flex-col items-center justify-end overflow-hidden">
                {/* Background Image */}
                <div className="absolute inset-0 z-0">
                    <img
                        src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80"
                        alt="Wheat field at sunrise"
                        className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
                </div>

                {/* Content */}
                <div className="relative z-10 w-full max-w-md mx-auto px-6 pb-16 text-center animate-fade-in-up space-y-6">
                    {/* Logo */}
                    <div className="flex items-center justify-center gap-2 mb-2">
                        <div className="w-12 h-12 bg-white/20 backdrop-blur-xl rounded-2xl flex items-center justify-center">
                            <Sprout className="text-leaf-400" size={28} />
                        </div>
                    </div>

                    <h1 className="text-4xl md:text-5xl font-black text-white leading-tight tracking-tight">
                        The New Era of
                        <span className="block text-leaf-400">Agriculture</span>
                    </h1>

                    <p className="text-white text-base max-w-sm mx-auto leading-relaxed">
                        AI-powered insights for smarter farming, better yields, and profitable agri-business ventures.
                    </p>

                    <button
                        onClick={() => setShowForm(true)}
                        className="w-full py-4 bg-gradient-to-r from-leaf-500 to-olive-500 text-white font-bold text-lg rounded-2xl shadow-xl hover:shadow-2xl active:scale-95 transition-all duration-300"
                    >
                        Get Started →
                    </button>

                    <p className="text-white/90 text-sm">
                        Already have an account?{' '}
                        <button onClick={() => setShowForm(true)} className="text-leaf-400 font-bold hover:underline">
                            Sign In
                        </button>
                    </p>
                </div>
            </div>
        );
    }

    // Login Form
    return (
        <div className="min-h-screen relative flex items-center justify-center p-4 overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 z-0">
                <img
                    src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&q=80"
                    alt="Wheat field"
                    className="w-full h-full object-cover blur-sm scale-105"
                />
                <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
            </div>

            <div className="relative z-10 w-full max-w-md animate-fade-in-up">
                {/* Back button */}
                <button
                    onClick={() => setShowForm(false)}
                    className="mb-4 text-white text-sm font-medium hover:text-white flex items-center gap-1 transition-colors"
                >
                    ← Back
                </button>

                {/* Card */}
                <div className="bg-white/10 backdrop-blur-2xl border border-white/20 rounded-4xl p-8 shadow-2xl space-y-6">
                    <div className="text-center space-y-2">
                        <div className="w-14 h-14 bg-leaf-500/20 backdrop-blur-xl rounded-2xl flex items-center justify-center mx-auto mb-3">
                            <Sprout className="text-leaf-400" size={28} />
                        </div>
                        <h2 className="text-2xl font-extrabold text-white">Welcome Back</h2>
                        <p className="text-white/90 text-sm">Sign in to AgroNexus AI</p>
                    </div>

                    {successMessage && (
                        <div className="bg-leaf-500/20 border border-leaf-400/30 p-3 rounded-2xl">
                            <p className="text-leaf-300 text-sm font-medium">{successMessage}</p>
                        </div>
                    )}

                    {error && (
                        <div className="bg-red-500/20 border border-red-400/30 p-3 rounded-2xl">
                            <p className="text-red-300 text-sm font-medium">{error}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="relative">
                            <User className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={18} />
                            <input
                                type="email"
                                required
                                className="w-full pl-12 pr-4 py-3.5 bg-white/10 border border-white/20 text-white placeholder-gray-200 rounded-2xl focus:outline-none focus:border-leaf-400 focus:ring-2 focus:ring-leaf-400/20 transition-all text-sm"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div className="relative">
                            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-white" size={18} />
                            <input
                                type={showPassword ? "text" : "password"}
                                required
                                className="w-full pl-12 pr-12 py-3.5 bg-white/10 border border-white/20 text-white placeholder-gray-200 rounded-2xl focus:outline-none focus:border-leaf-400 focus:ring-2 focus:ring-leaf-400/20 transition-all text-sm"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-4 top-1/2 -translate-y-1/2 text-white hover:text-white transition-colors">
                                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                            </button>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3.5 bg-gradient-to-r from-leaf-500 to-olive-500 text-white font-bold rounded-2xl shadow-lg hover:shadow-xl active:scale-[0.98] transition-all disabled:opacity-90"
                        >
                            {loading ? <Loader2 className="animate-spin mx-auto" size={22} /> : 'Sign In'}
                        </button>
                    </form>

                    <p className="text-center text-white/90 text-sm">
                        Don't have an account?{' '}
                        <Link to="/signup" className="text-leaf-400 font-bold hover:underline">Sign Up</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;
