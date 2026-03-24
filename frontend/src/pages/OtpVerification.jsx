import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Loader2, ShieldCheck, Sprout } from 'lucide-react';
import { API_BASE_URL } from '../config/api';


const OtpVerification = () => {
    const [otp, setOtp] = useState(['', '', '', '', '', '']);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const phone = location.state?.phone || '';

    if (!phone) { navigate('/signup'); return null; }

    const handleChange = (element, index) => {
        if (isNaN(element.value)) return;
        setOtp([...otp.map((d, idx) => (idx === index ? element.value : d))]);
        if (element.nextSibling && element.value !== '') element.nextSibling.focus();
    };

    const handleKeyDown = (e, index) => {
        if (e.key === 'Backspace' && otp[index] === '' && e.target.previousSibling) e.target.previousSibling.focus();
    };

    const handleVerify = async (e) => {
        e.preventDefault();
        const otpString = otp.join('');
        if (otpString.length !== 6) { setError('Enter all 6 digits'); return; }
        setLoading(true); setError('');
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/verify-otp`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone, otp: otpString }),
            });
            if (response.ok) navigate('/login', { state: { message: 'Phone verified! You can now login.' } });
            else { const data = await response.json(); setError(data.detail || "Invalid OTP"); }
        } catch { setError("Network error."); }
        finally { setLoading(false); }
    };

    const resendOtp = async () => {
        try {
            await fetch(`${API_BASE_URL}/api/auth/send-otp`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone }),
            });
            alert('New OTP sent!');
        } catch { alert('Failed to resend'); }
    };

    return (
        <div className="min-h-screen relative flex items-center justify-center p-4 overflow-hidden">
            <div className="absolute inset-0 z-0">
                <img src="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=1200&q=80" alt="Wheat" className="w-full h-full object-cover blur-sm scale-105" />
                <div className="absolute inset-0 bg-black/50" />
            </div>

            <div className="relative z-10 w-full max-w-sm animate-fade-in-up">
                <div className="bg-white/10 backdrop-blur-2xl border border-white/20 rounded-4xl p-8 shadow-2xl text-center space-y-6">
                    <div className="w-16 h-16 bg-leaf-500/20 rounded-full flex items-center justify-center mx-auto">
                        <ShieldCheck className="text-leaf-400" size={32} />
                    </div>
                    <div>
                        <h2 className="text-2xl font-extrabold text-white">Verify Phone</h2>
                        <p className="text-white/90 text-sm mt-1">Code sent to <span className="text-white font-bold">{phone}</span></p>
                    </div>

                    <div className="bg-blue-500/20 border border-blue-400/30 p-3 rounded-2xl">
                        <p className="text-blue-200 text-xs">Test: use <strong>123456</strong></p>
                    </div>

                    <form onSubmit={handleVerify} className="space-y-5">
                        <div className="flex justify-center gap-2">
                            {otp.map((data, index) => (
                                <input key={index} className="w-11 h-13 text-center text-xl font-bold bg-white/10 border-2 border-white/20 rounded-xl text-white focus:border-leaf-400 focus:ring-2 focus:ring-leaf-400/20 transition-all outline-none"
                                    type="text" maxLength="1" value={data}
                                    onChange={e => handleChange(e.target, index)} onKeyDown={e => handleKeyDown(e, index)} />
                            ))}
                        </div>
                        {error && <p className="text-red-300 text-sm font-medium">{error}</p>}
                        <button type="submit" disabled={loading}
                            className="w-full py-3.5 bg-gradient-to-r from-leaf-500 to-olive-500 text-white font-bold rounded-2xl shadow-lg active:scale-[0.98] transition-all disabled:opacity-90">
                            {loading ? <Loader2 className="animate-spin mx-auto" size={22} /> : 'Verify Code'}
                        </button>
                    </form>
                    <p className="text-white/90 text-sm">
                        Didn't receive?{' '}
                        <button onClick={resendOtp} className="text-leaf-400 font-bold hover:underline">Resend</button>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default OtpVerification;
