import React, { useState } from 'react';
import { 
  ChevronLeft, Loader2, Landmark, CheckCircle2, Circle, 
  UploadCloud, AlertTriangle, FileText, CalendarClock, ShieldCheck, 
  TrendingDown, Languages
} from 'lucide-react';
import { Link } from 'react-router-dom';

// Simulated Scheme Database with enriched metadata
const schemeDatabase = [
  {
    id: "PMFBY",
    name: "Pradhan Mantri Fasal Bima Yojana (Crop Insurance)",
    benefit: "Financial support against crop loss from natural calamities.",
    target_risk: "high",
    target_msp: "normal",
    deadline: 15, // days left
    link: "https://pmfby.gov.in/",
    docs: [
      { id: 'd1', name: 'Aadhaar Card' },
      { id: 'd2', name: 'Land Ownership Passbook (Pattadar)' },
      { id: 'd3', name: 'Sowing Certificate' }
    ],
    steps: [
      "Gather your land documents.",
      "Upload documents to estimate premium.",
      "Pay your share (~2% for Kharif) to Common Service Centre."
    ]
  },
  {
    id: "PMAASHA",
    name: "PM-AASHA (Procurement Scheme)",
    benefit: "Ensures you get Minimum Support Price (MSP) if market crashes.",
    target_risk: "low",
    target_msp: "below",
    deadline: 7,
    link: "https://pmkisan.gov.in/", // Placeholder for PMAASHA or actual URL if known
    docs: [
      { id: 'd4', name: 'Bank Passbook Copy' },
      { id: 'd5', name: 'Farmer Registration ID' }
    ],
    steps: [
      "Register on state procurement portal.",
      "Upload active bank account details.",
      "Wait for procurement SMS mandate."
    ]
  },
  {
    id: "PMKISAN",
    name: "PM-KISAN Samman Nidhi",
    benefit: "₹6000/year minimum income support directly to bank.",
    target_risk: "all",
    target_msp: "all",
    deadline: 30,
    link: "https://pmkisan.gov.in/",
    docs: [
      { id: 'd6', name: 'Aadhaar Linked Bank Account' },
      { id: 'd7', name: 'Land Record Extract (1B/Khatauni)' }
    ],
    steps: [
      "Ensure Aadhaar is seeded with bank.",
      "Upload land extract.",
      "Complete eKYC on PM-Kisan portal."
    ]
  }
];

const SchemeCard = ({ scheme }) => {
  const [uploadedDocs, setUploadedDocs] = useState({});
  const [showSteps, setShowSteps] = useState(false);

  const toggleDoc = (docId) => {
    setUploadedDocs(prev => ({ ...prev, [docId]: !prev[docId] }));
  };

  const progress = Math.round((Object.values(uploadedDocs).filter(Boolean).length / scheme.docs.length) * 100);

  return (
    <div className="bg-white rounded-3xl shadow-card p-5 space-y-4 relative overflow-hidden transition-all duration-300">
      {/* Deadline Badge */}
      <div className={`absolute top-0 right-0 px-3 py-1 text-[10px] font-black uppercase tracking-wider rounded-bl-2xl ${scheme.deadline <= 10 ? 'bg-red-100 text-red-600' : 'bg-amber-100 text-amber-600'}`}>
        {scheme.deadline} Days Left
      </div>

      <div className="flex items-start gap-4 pt-2">
        <div className="w-12 h-12 bg-indigo-50 rounded-2xl flex items-center justify-center flex-shrink-0">
          <Landmark size={24} className="text-indigo-600" />
        </div>
        <div>
          <h3 className="font-extrabold text-[15px] text-gray-800 leading-tight pr-10">{scheme.name}</h3>
          <p className="text-xs text-gray-600 mt-1 leading-relaxed font-medium">{scheme.benefit}</p>
        </div>
      </div>

      <div className="bg-green-50/50 p-3 rounded-2xl border border-green-100 flex items-center justify-between">
        <span className="text-xs font-bold text-green-700">Eligibility Status</span>
        <span className="text-[10px] bg-green-200 text-green-800 px-2 py-0.5 rounded-full font-black uppercase tracking-wider">Matched</span>
      </div>

      {/* Progress & Docs */}
      <div className="space-y-3 pt-2">
        <div className="flex justify-between items-center text-[10px] font-bold text-gray-500 uppercase tracking-widest">
          <span>Application Progress</span>
          <span className="text-indigo-600">{progress}%</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-2">
          <div className="bg-indigo-500 h-2 rounded-full transition-all duration-500" style={{ width: `${progress}%` }}></div>
        </div>

        <div className="space-y-2 mt-3">
          <p className="text-xs font-extrabold text-gray-800 flex items-center gap-1"><FileText size={14}/> Required Documents</p>
          {scheme.docs.map(doc => {
            const isDone = uploadedDocs[doc.id];
            return (
              <div 
                key={doc.id} 
                onClick={() => toggleDoc(doc.id)}
                className={`flex items-center justify-between p-2.5 rounded-xl border cursor-pointer active:scale-[0.98] transition-all
                  ${isDone ? 'bg-indigo-50/50 border-indigo-200' : 'bg-gray-50 border-gray-200 hover:border-indigo-300'}`}
              >
                <div className="flex items-center gap-2">
                  {isDone ? <CheckCircle2 size={16} className="text-indigo-600" /> : <Circle size={16} className="text-gray-400" />}
                  <span className={`text-xs font-semibold ${isDone ? 'text-indigo-900 line-through opacity-70' : 'text-gray-700'}`}>{doc.name}</span>
                </div>
                {!isDone && <UploadCloud size={14} className="text-gray-400" />}
              </div>
            );
          })}
        </div>
      </div>

      <button 
        onClick={() => setShowSteps(!showSteps)}
        className="w-full py-2.5 bg-gray-50 hover:bg-gray-100 text-gray-700 text-xs font-bold rounded-xl transition-colors"
      >
        {showSteps ? 'Hide Application Steps' : 'View Step-by-Step Guide'}
      </button>

      {showSteps && (
        <div className="bg-indigo-50 p-4 rounded-2xl space-y-3 animate-fade-in">
          {scheme.steps.map((step, idx) => (
            <div key={idx} className="flex gap-3">
              <div className="w-5 h-5 bg-indigo-200 text-indigo-800 rounded-full flex items-center justify-center flex-shrink-0 text-[10px] font-black">
                {idx + 1}
              </div>
              <p className="text-xs text-indigo-900 font-medium pt-0.5">{step}</p>
            </div>
          ))}
          {progress === 100 && (
            <a 
              href={scheme.link}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full mt-3 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl shadow-md active:scale-95 transition-all flex items-center justify-center"
            >
              Submit Application
            </a>
          )}
        </div>
      )}
    </div>
  );
};

const Schemes = () => {
  const [formData, setFormData] = useState({
    crop: 'Rice', land_size: 2.5, state: 'Telangana', income: 45000, 
    riskProfile: 'low', priceStatus: 'normal'
  });
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analyzed, setAnalyzed] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleAnalyze = (e) => {
    e.preventDefault();
    setLoading(true);
    
    setTimeout(() => {
      // Risk Engine Integration Fake Logic
      let results = [...schemeDatabase];
      
      // Filter out high risk if they are low risk, unless it's a general scheme
      if (formData.riskProfile !== 'high') {
         results = results.filter(s => s.target_risk !== 'high');
      }
      if (formData.priceStatus !== 'below') {
         results = results.filter(s => s.target_msp !== 'below');
      }
      
      setSchemes(results);
      setAnalyzed(true);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen px-4 pt-6 pb-20 max-w-lg mx-auto space-y-5 bg-gray-50/50">
      
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="w-10 h-10 bg-white rounded-2xl shadow-sm flex items-center justify-center active:scale-90 transition-transform border border-gray-100">
            <ChevronLeft size={20} className="text-gray-800" />
          </Link>
          <div>
            <h1 className="text-[17px] font-black text-gray-800 tracking-tight flex items-center gap-1.5 border-b-2 border-indigo-200 pb-0.5">
              Scheme Assistant <CheckCircle2 size={14} className="text-indigo-600"/>
            </h1>
          </div>
        </div>
        <div className="bg-indigo-50 p-2 rounded-xl border border-indigo-100">
          <Languages size={18} className="text-indigo-600" />
        </div>
      </div>

      {!analyzed ? (
        <div className="animate-fade-in-up space-y-4">
          <div className="bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-[24px] p-6 text-white shadow-lg relative overflow-hidden">
             <div className="absolute -top-10 -right-10 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
             <ShieldCheck size={28} className="text-indigo-200 mb-3" />
             <h2 className="text-xl font-black mb-1">AI Matchmaker</h2>
             <p className="text-[13px] text-indigo-100 font-medium leading-relaxed">
               We match your farm profile with active government schemes, tell you exactly what documents you need, and guide your application.
             </p>
          </div>

          <form onSubmit={handleAnalyze} className="bg-white rounded-3xl shadow-card p-5 space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 block">Primary Crop</label>
                <input type="text" name="crop" value={formData.crop} onChange={handleInputChange} className="input-mobile text-sm py-3 bg-gray-50" />
              </div>
              <div>
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 block">State</label>
                <select name="state" value={formData.state} onChange={handleInputChange} className="input-mobile text-sm py-3 bg-gray-50">
                  <option value="Telangana">Telangana</option>
                  <option value="Maharashtra">Maharashtra</option>
                  <option value="Punjab">Punjab</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 block">Land (Acres)</label>
                <input type="number" step="0.1" name="land_size" value={formData.land_size} onChange={handleInputChange} className="input-mobile text-sm py-3 bg-gray-50" />
              </div>
              <div>
                <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1.5 block">Annual Income (₹)</label>
                <input type="number" step="1000" name="income" value={formData.income} onChange={handleInputChange} className="input-mobile text-sm py-3 bg-gray-50" />
              </div>
            </div>

            <div className="pt-2">
              <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2 block flex items-center gap-1.5">
                <AlertTriangle size={12} className="text-amber-500" /> AI Risk Engine Triggers
              </label>
              
              <div className="grid grid-cols-2 gap-3">
                {/* Weather Risk Toggle */}
                <div 
                  onClick={() => handleInputChange({ target: { name: 'riskProfile', value: formData.riskProfile === 'high' ? 'low' : 'high' } })}
                  className={`border-2 p-3 rounded-2xl cursor-pointer transition-all ${formData.riskProfile === 'high' ? 'border-amber-400 bg-amber-50' : 'border-gray-100 bg-gray-50 hover:bg-gray-100'}`}
                >
                  <AlertTriangle size={16} className={formData.riskProfile === 'high' ? 'text-amber-500 mb-1' : 'text-gray-400 mb-1'} />
                  <p className="text-[11px] font-extrabold text-gray-800">High Weather Risk</p>
                  <p className="text-[9px] text-gray-500 mt-0.5">(Flood/Drought expected)</p>
                </div>

                {/* MSP Risk Toggle */}
                <div 
                  onClick={() => handleInputChange({ target: { name: 'priceStatus', value: formData.priceStatus === 'below' ? 'normal' : 'below' } })}
                  className={`border-2 p-3 rounded-2xl cursor-pointer transition-all ${formData.priceStatus === 'below' ? 'border-rose-400 bg-rose-50' : 'border-gray-100 bg-gray-50 hover:bg-gray-100'}`}
                >
                  <TrendingDown size={16} className={formData.priceStatus === 'below' ? 'text-rose-500 mb-1' : 'text-gray-400 mb-1'} />
                  <p className="text-[11px] font-extrabold text-gray-800">Price below MSP</p>
                  <p className="text-[9px] text-gray-500 mt-0.5">(Market crash warning)</p>
                </div>
              </div>
            </div>

            <button type="submit" disabled={loading} className="w-full bg-indigo-600 text-white font-bold text-[13px] py-4 rounded-2xl flex items-center justify-center gap-2 mt-4 shadow-lg shadow-indigo-200 active:scale-95 transition-all">
              {loading ? <><Loader2 className="animate-spin" size={18} /> Syncing with State Portal...</> : 'Check My Eligibility'}
            </button>
          </form>
        </div>
      ) : (
        <div className="space-y-4 animate-fade-in-up">
           <div className="flex justify-between items-center mb-1">
             <h2 className="text-[13px] font-black text-gray-800 uppercase tracking-wider flex items-center gap-1.5">
               <span className="w-2 h-2 rounded-full bg-green-500"></span> {schemes.length} Matches Found
             </h2>
             <button onClick={() => setAnalyzed(false)} className="text-[11px] font-bold text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-full">
               Edit Profile
             </button>
           </div>
           
           {schemes.map(scheme => <SchemeCard key={scheme.id} scheme={scheme} />)}
           
           {schemes.length === 0 && (
             <div className="bg-white rounded-3xl p-6 text-center border border-gray-100">
               <p className="text-sm font-bold text-gray-600">No active schemes match your current risk profile and state right now.</p>
               <button onClick={() => setAnalyzed(false)} className="mt-4 text-xs font-bold text-indigo-600">Go Back</button>
             </div>
           )}
        </div>
      )}
    </div>
  );
};

export default Schemes;
