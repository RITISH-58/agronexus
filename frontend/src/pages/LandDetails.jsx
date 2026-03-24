import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MapPin, ArrowLeft, Loader2, Save, Leaf, Droplets } from 'lucide-react';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';


const LandDetails = () => {
    const { token } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    const [formData, setFormData] = useState({
        land_size: '',
        soil_type: 'Loamy',
        water_availability: 'Borewell',
        primary_crop: '',
        district: '',
        village: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${API_BASE_URL}/api/profile/land`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                // Ensure number conversion
                body: JSON.stringify({
                    ...formData,
                    land_size: parseFloat(formData.land_size)
                }),
            });

            if (response.ok) {
                navigate('/profile');
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to add land details');
            }
        } catch (error) {
            setError('Network error connecting to API');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
            <Link to="/profile" className="inline-flex items-center text-sm font-medium text-green-600 hover:text-green-800 mb-6">
                <ArrowLeft className="mr-1 h-4 w-4" /> Back to Profile
            </Link>
            
            <div className="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-100 relative">
                <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-green-100 rounded-full blur-3xl opacity-90 pointer-events-none"></div>
                
                <div className="px-6 py-6 border-b border-gray-200 sm:px-10 bg-gradient-to-r from-green-50 to-white">
                    <div className="flex items-center">
                        <div className="flex-shrink-0 bg-green-100 rounded-xl p-3">
                            <MapPin className="h-8 w-8 text-green-600" />
                        </div>
                        <div className="ml-5">
                            <h2 className="text-2xl font-bold text-gray-900">Add New Farmland</h2>
                            <p className="mt-1 text-sm text-gray-700">Provide details about your plot to receive better personalized recommendations.</p>
                        </div>
                    </div>
                </div>

                <form className="px-6 py-8 sm:px-10 space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-md">
                            <p className="text-red-700 text-sm font-medium">{error}</p>
                        </div>
                    )}

                    <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                        
                        {/* Size */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Land Size (Acres)</label>
                            <div className="mt-1 relative rounded-md shadow-sm">
                                <input
                                    type="number"
                                    step="any"
                                    name="land_size"
                                    required
                                    min="0"
                                    className="block w-full pr-10 border-gray-300 rounded-xl focus:ring-green-500 focus:border-green-500 sm:text-sm py-3 px-4 border"
                                    placeholder="e.g. 5.5"
                                    value={formData.land_size}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        {/* Primary Crop */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Primary Crop Currently Grown</label>
                            <div className="mt-1 relative rounded-md shadow-sm">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Leaf className="h-5 w-5 text-gray-600" />
                                </div>
                                <input
                                    type="text"
                                    name="primary_crop"
                                    required
                                    className="block w-full pl-10 border-gray-300 rounded-xl focus:ring-green-500 focus:border-green-500 sm:text-sm py-3 px-4 border"
                                    placeholder="e.g. Wheat, Rice, Cotton"
                                    value={formData.primary_crop}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        {/* Soil Type */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Soil Type</label>
                            <div className="mt-1">
                                <select
                                    name="soil_type"
                                    className="block w-full border-gray-300 rounded-xl focus:ring-green-500 focus:border-green-500 sm:text-sm py-3 px-4 border"
                                    value={formData.soil_type}
                                    onChange={handleChange}
                                >
                                    <option value="Loamy">Loamy</option>
                                    <option value="Clay">Clay</option>
                                    <option value="Sandy">Sandy</option>
                                    <option value="Silty">Silty</option>
                                    <option value="Peaty">Peaty</option>
                                    <option value="Chalky">Chalky</option>
                                    <option value="Black Cotton">Black Cotton</option>
                                    <option value="Red Laterite">Red Laterite</option>
                                </select>
                            </div>
                        </div>

                        {/* Water Availability */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Water Source</label>
                            <div className="mt-1 relative rounded-md shadow-sm">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Droplets className="h-5 w-5 text-gray-600" />
                                </div>
                                <select
                                    name="water_availability"
                                    className="block w-full pl-10 border-gray-300 rounded-xl focus:ring-green-500 focus:border-green-500 sm:text-sm py-3 px-4 border"
                                    value={formData.water_availability}
                                    onChange={handleChange}
                                >
                                    <option value="Borewell">Borewell</option>
                                    <option value="Canal">Canal</option>
                                    <option value="Rainfed">Rainfed (Monsoon only)</option>
                                    <option value="River/Lake">River/Lake</option>
                                    <option value="Drip Irrigation">Drip Irrigation System</option>
                                </select>
                            </div>
                        </div>

                        {/* Location */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700">District / Region</label>
                            <div className="mt-1">
                                <input
                                    type="text"
                                    name="district"
                                    required
                                    className="block w-full border-gray-300 rounded-xl focus:ring-green-500 focus:border-green-500 sm:text-sm py-3 px-4 border"
                                    value={formData.district}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Village</label>
                            <div className="mt-1">
                                <input
                                    type="text"
                                    name="village"
                                    required
                                    className="block w-full border-gray-300 rounded-xl focus:ring-green-500 focus:border-green-500 sm:text-sm py-3 px-4 border"
                                    value={formData.village}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                    </div>

                    <div className="pt-5 border-t border-gray-100 flex justify-end">
                        <Link to="/profile" className="bg-white py-3 px-6 border border-gray-300 rounded-xl shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none mr-3 transition-colors">
                            Cancel
                        </Link>
                        <button
                            type="submit"
                            disabled={loading}
                            className="inline-flex justify-center items-center py-3 px-6 border border-transparent shadow-md text-sm font-bold rounded-xl text-white bg-green-600 hover:bg-green-700 focus:outline-none transition-all hover:scale-[1.02]"
                        >
                            {loading ? <Loader2 className="animate-spin h-5 w-5" /> : <Save className="mr-2 h-5 w-5" />}
                            Save Plot
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LandDetails;
