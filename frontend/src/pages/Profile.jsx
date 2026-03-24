import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { User, Phone, MapPin, Mail, Save, Loader2, Plus, Trash2, ChevronLeft, LogOut, Edit3, Settings } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';


const Profile = () => {
    const { user, token, logout } = useAuth();
    const navigate = useNavigate();
    const [isEditing, setIsEditing] = useState(false);
    const [loading, setLoading] = useState(false);
    const [lands, setLands] = useState([]);
    const [loadingLands, setLoadingLands] = useState(true);
    const [message, setMessage] = useState({ text: '', type: '' });
    const [formData, setFormData] = useState({ full_name: '', phone: '', state: '', district: '' });

    useEffect(() => {
        if (user) setFormData({ full_name: user.full_name || '', phone: user.phone || '', state: user.state || '', district: user.district || '' });
    }, [user]);

    useEffect(() => {
        const fetchLands = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/api/profile/land`, { headers: { 'Authorization': `Bearer ${token}` } });
                if (res.ok) setLands(await res.json());
            } catch (e) { console.error(e); }
            finally { setLoadingLands(false); }
        };
        if (token) fetchLands();
    }, [token]);

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleUpdateProfile = async (e) => {
        e.preventDefault(); setLoading(true); setMessage({ text: '', type: '' });
        try {
            const res = await fetch(`${API_BASE_URL}/api/profile/update`, {
                method: 'PUT', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify(formData),
            });
            if (res.ok) { setMessage({ text: 'Updated!', type: 'success' }); setIsEditing(false); }
            else { const d = await res.json(); setMessage({ text: d.detail || 'Failed', type: 'error' }); }
        } catch { setMessage({ text: 'Network error.', type: 'error' }); }
        finally { setLoading(false); }
    };

    const handleDeleteLand = async (landId) => {
        if (!window.confirm("Delete this land?")) return;
        try {
            const res = await fetch(`${API_BASE_URL}/api/profile/land/${landId}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
            if (res.ok) setLands(lands.filter(l => l.land_id !== landId));
        } catch { alert("Error deleting."); }
    };

    const handleLogout = () => { logout(); navigate('/login'); };

    if (!user) return <div className="flex items-center justify-center min-h-screen"><Loader2 className="animate-spin text-leaf-500" size={32} /></div>;

    return (
        <div className="min-h-screen px-4 pt-6 pb-4 max-w-lg mx-auto space-y-5 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <Link to="/" className="w-10 h-10 bg-white rounded-2xl shadow-card flex items-center justify-center active:scale-90 transition-transform">
                        <ChevronLeft size={20} className="text-dark" />
                    </Link>
                    <h1 className="text-xl font-extrabold text-dark tracking-tight">Profile</h1>
                </div>
                <button onClick={handleLogout} className="w-10 h-10 bg-red-50 rounded-2xl flex items-center justify-center active:scale-90 transition-transform">
                    <LogOut size={18} className="text-red-500" />
                </button>
            </div>

            {/* Profile Card */}
            <div className="bg-white rounded-3xl shadow-card p-5 space-y-4">
                <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-gradient-to-br from-leaf-400 to-olive-500 rounded-2xl flex items-center justify-center shadow-lg">
                        <span className="text-white font-bold text-2xl">{user.full_name?.charAt(0)?.toUpperCase()}</span>
                    </div>
                    <div className="flex-1">
                        <h2 className="text-lg font-extrabold text-dark">{user.full_name}</h2>
                        <p className="text-xs text-muted">{user.email}</p>
                        <span className="badge badge-green text-[9px] mt-1">{user.role?.replace('_', ' ')?.toUpperCase()}</span>
                    </div>
                    <button onClick={() => setIsEditing(!isEditing)} className="w-9 h-9 bg-cream-200 rounded-xl flex items-center justify-center">
                        <Edit3 size={16} className="text-muted" />
                    </button>
                </div>

                {message.text && (
                    <div className={`p-3 rounded-2xl text-sm font-medium ${message.type === 'success' ? 'bg-leaf-100 text-leaf-700' : 'bg-red-100 text-red-600'}`}>
                        {message.text}
                    </div>
                )}

                {!isEditing ? (
                    <div className="space-y-3 pt-3 border-t border-cream-300">
                        {[
                            { icon: Phone, label: 'Phone', value: user.phone, extra: user.phone_verified ? '✓' : '' },
                            { icon: MapPin, label: 'Location', value: `${user.district}, ${user.state}` },
                            { icon: Mail, label: 'Email', value: user.email },
                        ].map((item) => (
                            <div key={item.label} className="flex items-center gap-3">
                                <div className="w-9 h-9 bg-cream-200 rounded-xl flex items-center justify-center">
                                    <item.icon size={15} className="text-muted" />
                                </div>
                                <div>
                                    <p className="text-[10px] text-muted font-bold uppercase">{item.label}</p>
                                    <p className="text-sm text-dark font-medium">{item.value} {item.extra && <span className="text-leaf-500 text-xs">{item.extra}</span>}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <form onSubmit={handleUpdateProfile} className="space-y-3 pt-3 border-t border-cream-300 animate-fade-in">
                        <input name="full_name" value={formData.full_name} onChange={handleChange} className="input-mobile text-sm" placeholder="Full Name" />
                        <input name="phone" value={formData.phone} onChange={handleChange} className="input-mobile text-sm" placeholder="Phone" />
                        <div className="grid grid-cols-2 gap-3">
                            <input name="state" value={formData.state} onChange={handleChange} className="input-mobile text-sm" placeholder="State" />
                            <input name="district" value={formData.district} onChange={handleChange} className="input-mobile text-sm" placeholder="District" />
                        </div>
                        <div className="flex gap-2">
                            <button type="button" onClick={() => setIsEditing(false)} className="btn-secondary flex-1 py-2.5 text-sm">Cancel</button>
                            <button type="submit" disabled={loading} className="btn-primary flex-1 py-2.5 text-sm flex items-center justify-center gap-1">
                                {loading ? <Loader2 className="animate-spin" size={16} /> : <Save size={14} />} Save
                            </button>
                        </div>
                    </form>
                )}
            </div>

            {/* Land Management */}
            <div className="bg-white rounded-3xl shadow-card overflow-hidden">
                <div className="p-4 flex items-center justify-between border-b border-cream-300">
                    <div>
                        <h3 className="text-sm font-extrabold text-dark">My Farms</h3>
                        <p className="text-[10px] text-muted">Manage your land details</p>
                    </div>
                    <Link to="/profile/add-land" className="badge badge-green flex items-center gap-1 px-3 py-1.5">
                        <Plus size={12} /> Add
                    </Link>
                </div>

                <div className="p-4">
                    {loadingLands ? (
                        <div className="flex justify-center py-6"><Loader2 className="animate-spin text-leaf-500" size={24} /></div>
                    ) : lands.length === 0 ? (
                        <div className="text-center py-8 space-y-2">
                            <MapPin className="mx-auto text-cream-400" size={32} />
                            <p className="text-sm text-muted font-medium">No farms added yet</p>
                            <Link to="/profile/add-land" className="btn-primary text-xs inline-flex items-center gap-1 py-2 px-4">
                                <Plus size={14} /> Add Farm
                            </Link>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {lands.map((land) => (
                                <div key={land.land_id} className="bg-cream-100 rounded-2xl p-4 space-y-2">
                                    <div className="flex items-center justify-between">
                                        <h4 className="font-bold text-sm text-dark">{land.primary_crop || 'Mixed'} Plot</h4>
                                        <button onClick={() => handleDeleteLand(land.land_id)} className="text-muted hover:text-red-500 transition-colors">
                                            <Trash2 size={14} />
                                        </button>
                                    </div>
                                    <p className="text-xs text-muted">{land.village}, {land.district}</p>
                                    <div className="flex gap-3 text-[10px]">
                                        <span className="badge badge-green">{land.land_size} acres</span>
                                        <span className="badge badge-gold">{land.soil_type}</span>
                                        <span className="badge badge-blue">{land.water_availability}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile;
