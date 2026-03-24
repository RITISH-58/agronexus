"""
Business Recommender — ML/Logic layer for the Entrepreneur Mode.
Handles: crop lookup, trending aggregation, search/filter, and business plan generation.
"""
import json
import os
from typing import List, Dict, Any, Optional

class BusinessRecommender:

    def __init__(self):
        self.dataset_path = os.path.join(os.path.dirname(__file__), "../data/agro_business.json")
        self.data = self._load_data()

        # --- Build indexes for fast lookups ---
        # crop_name (lowercase) -> list of business dicts
        self.crop_index: Dict[str, List[Dict[str, Any]]] = {}
        # business_name (lowercase) -> business dict + crop
        self.business_index: Dict[str, Dict[str, Any]] = {}
        # flat list of ALL businesses (for trending & search)
        self.all_businesses: List[Dict[str, Any]] = []

        for entry in self.data:
            crop = entry["crop"].lower()
            businesses = entry.get("businesses", [])
            self.crop_index[crop] = businesses
            for biz in businesses:
                enriched = {**biz, "crop": entry["crop"]}
                self.all_businesses.append(enriched)
                self.business_index[biz["name"].lower()] = enriched

        # Government schemes with full details for business plans
        self.scheme_details = {
            "PMFME": {
                "name": "PM Formalisation of Micro Food Processing Enterprises (PMFME)",
                "benefit": "35% capital subsidy (up to ₹10 Lakhs) for micro food processing units, plus training and hand-holding support.",
                "official_link": "https://pmfme.mofpi.gov.in"
            },
            "Agriculture Infrastructure Fund": {
                "name": "Agriculture Infrastructure Fund (AIF)",
                "benefit": "3% interest subvention and credit guarantee up to ₹2 Crore for post-harvest and agro-processing infrastructure.",
                "official_link": "https://agriinfra.dac.gov.in"
            },
            "Startup India": {
                "name": "Startup India – Agriculture",
                "benefit": "Tax exemptions for 3 years, fast-track patents, ₹10,000 Cr Fund-of-Funds access, and mentorship.",
                "official_link": "https://www.startupindia.gov.in"
            },
            "Mudra Loan": {
                "name": "Mudra Loan (PMMY)",
                "benefit": "Collateral-free loans up to ₹10 Lakhs under Shishu (₹50K), Kishore (₹5L), Tarun (₹10L) categories.",
                "official_link": "https://www.mudra.org.in"
            },
            "NABARD Fund": {
                "name": "NABARD – Agri Processing Fund",
                "benefit": "Refinance support and term loans for food processing, cold storage, warehousing, and rural enterprises.",
                "official_link": "https://www.nabard.org"
            },
            "MIDH": {
                "name": "Mission for Integrated Development of Horticulture (MIDH)",
                "benefit": "40-50% subsidy for horticulture infrastructure including cold chains, greenhouse, and processing units.",
                "official_link": "https://midh.gov.in"
            },
            "APEDA Export": {
                "name": "APEDA Export Promotion Scheme",
                "benefit": "Financial assistance for export infrastructure, quality certification, and market development.",
                "official_link": "https://apeda.gov.in"
            },
            "APEDA Export Support": {
                "name": "APEDA Export Promotion Scheme",
                "benefit": "Financial assistance for export infrastructure, quality certification, and market development.",
                "official_link": "https://apeda.gov.in"
            },
            "PMEGP": {
                "name": "Prime Minister's Employment Generation Programme",
                "benefit": "15-35% subsidy for setting up micro enterprises in rural areas. Max project cost ₹25 Lakhs.",
                "official_link": "https://www.kviconline.gov.in/pmegp"
            },
            "e-NAM": {
                "name": "National Agriculture Market (e-NAM)",
                "benefit": "Online trading platform to sell produce at best prices across India. Transparent price discovery.",
                "official_link": "https://enam.gov.in"
            },
            "PM KUSUM": {
                "name": "PM KUSUM – Solar Pump Scheme",
                "benefit": "60% subsidy on solar water pumps for irrigation. Reduces electricity costs to zero.",
                "official_link": "https://pmkusum.mnre.gov.in"
            },
            "PM-KISAN": {
                "name": "PM-KISAN",
                "benefit": "₹6000/year direct income support to all landholding farmer families.",
                "official_link": "https://pmkisan.gov.in"
            },
            "PKVY": {
                "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
                "benefit": "₹50,000/ha support for organic farming clusters. Training, certification, and marketing support.",
                "official_link": "https://pgsindia-ncof.gov.in"
            },
            "RKVY": {
                "name": "Rashtriya Krishi Vikas Yojana (RKVY)",
                "benefit": "Flexible funding for agri-related startups and infrastructure. Up to ₹25 Lakhs for startups.",
                "official_link": "https://rkvy.nic.in"
            },
            "NHM": {
                "name": "National Horticulture Mission",
                "benefit": "Subsidies for cold storage construction, greenhouse setup, and horticulture mechanization.",
                "official_link": "https://nhb.gov.in"
            },
            "DEDS (Dairy Entrepreneurship)": {
                "name": "Dairy Entrepreneurship Development Scheme (DEDS)",
                "benefit": "25-33% subsidy for establishing dairy processing, milk parlors, and vermicompost units.",
                "official_link": "https://dahd.nic.in"
            },
            "MNRE Biomass Scheme": {
                "name": "MNRE Biomass Energy Scheme",
                "benefit": "Capital subsidy and CFA for biomass-based power and briquette manufacturing units.",
                "official_link": "https://mnre.gov.in"
            },
            "Ethanol Blending Programme": {
                "name": "Ethanol Blending Programme (EBP)",
                "benefit": "Government-guaranteed purchase of ethanol at fixed remunerative prices for fuel blending.",
                "official_link": "https://dfpd.gov.in"
            },
            "Coconut Development Board": {
                "name": "Coconut Development Board (CDB)",
                "benefit": "25% subsidy for coconut processing units. Technical training and quality certification support.",
                "official_link": "https://coconutboard.gov.in"
            },
            "Tea Board Subsidies": {
                "name": "Tea Board of India – Subsidy Schemes",
                "benefit": "Factory modernization, quality upgradation, and marketing subsidies for small tea growers.",
                "official_link": "https://teaboard.gov.in"
            },
            "Coffee Board Subsidies": {
                "name": "Coffee Board of India – Support Schemes",
                "benefit": "Subsidies for post-harvest equipment, quality labs, and marketing for small coffee growers.",
                "official_link": "https://indiacoffee.org"
            },
            "Coir Board Schemes": {
                "name": "Coir Board – Development Schemes",
                "benefit": "40% subsidy on coir processing machinery. Training and exhibition support.",
                "official_link": "https://coirboard.gov.in"
            },
            "FSSAI Registration": {
                "name": "FSSAI Food Safety License",
                "benefit": "Mandatory food business license. Easy online registration. Builds consumer trust and enables retail/export.",
                "official_link": "https://foscos.fssai.gov.in"
            },
            "State Solar Subsidies": {
                "name": "State Solar Energy Subsidies",
                "benefit": "Various state-level subsidies (30-70%) for solar installations on agricultural land.",
                "official_link": "https://mnre.gov.in"
            },
            "Waste to Wealth Mission": {
                "name": "Waste to Wealth Mission",
                "benefit": "Support for converting agricultural waste into valuable products. R&D grants and pilot project funding.",
                "official_link": "https://dst.gov.in"
            },
            "National Millet Mission": {
                "name": "National Millet Mission",
                "benefit": "Financial support for millet processing, value addition, and brand development.",
                "official_link": "https://millets.dacnet.nic.in"
            },
            "NABARD": {
                "name": "NABARD – Agri Processing Fund",
                "benefit": "Refinance support and term loans for food processing, cold storage, warehousing, and rural enterprises.",
                "official_link": "https://www.nabard.org"
            }
        }

    def _load_data(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.dataset_path):
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_opportunities(self, crop: str) -> List[Dict[str, Any]]:
        """Return business opportunities for a given crop."""
        return self.crop_index.get(crop.lower().strip(), [])

    def get_trending(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return top trending businesses sorted by demand and trending flag."""
        demand_order = {"Very High": 4, "High": 3, "Medium": 2, "Low": 1}
        trending = [b for b in self.all_businesses if b.get("trending", False)]
        # Sort by demand level descending
        trending.sort(key=lambda x: demand_order.get(x.get("market_demand", "Medium"), 2), reverse=True)
        return trending[:limit]

    def search(self, query: str, investment_filter: str = None, demand_filter: str = None) -> List[Dict[str, Any]]:
        """
        Search all businesses by keyword. Optionally filter by investment range and demand.
        investment_filter: 'low' (<5L), 'medium' (5-20L), 'high' (>20L)
        demand_filter: 'High', 'Very High', 'Medium'
        """
        query_lower = query.lower().strip()
        results = []

        for biz in self.all_businesses:
            # Keyword match across name, description, crop, machinery, govt schemes
            searchable = " ".join([
                biz.get("name", ""),
                biz.get("description", ""),
                biz.get("crop", ""),
                " ".join(biz.get("machinery", [])),
                " ".join(biz.get("government_schemes", [])),
                biz.get("production_process", ""),
                biz.get("export_potential", "")
            ]).lower()

            if query_lower in searchable:
                results.append(biz)

        # Apply investment filter
        if investment_filter:
            f = investment_filter.lower()
            if f == "low":
                results = [r for r in results if r.get("investment_numeric", 0) < 500000]
            elif f == "medium":
                results = [r for r in results if 500000 <= r.get("investment_numeric", 0) <= 2000000]
            elif f == "high":
                results = [r for r in results if r.get("investment_numeric", 0) > 2000000]

        # Apply demand filter
        if demand_filter:
            results = [r for r in results if r.get("market_demand", "").lower() == demand_filter.lower()]

        return results

    def generate_business_plan(self, business_name: str) -> Optional[Dict[str, Any]]:
        """Generate a comprehensive business plan from the dataset."""
        biz = self.business_index.get(business_name.lower().strip())
        if not biz:
            return None

        crop = biz.get("crop", "agriculture").title()

        # Resolve government schemes to full details
        scheme_keys = biz.get("government_schemes", [])
        resolved_schemes = []
        for key in scheme_keys:
            if key in self.scheme_details:
                resolved_schemes.append(self.scheme_details[key])
            else:
                resolved_schemes.append({
                    "name": key,
                    "benefit": "Government support available. Contact local agriculture department for details.",
                    "official_link": "https://agricoop.nic.in"
                })

        plan = {
            "business_name": biz["name"],
            "crop": crop,
            "introduction": f"{biz['name']} is a high-potential agribusiness opportunity in the {crop} value chain. {biz['description']} This venture is ideal for farmers and rural entrepreneurs looking to add value to their harvest and build a sustainable business.",
            "market_opportunity": biz.get("export_potential", "Strong domestic market demand with growing consumer awareness."),
            "required_machinery": biz.get("machinery", ["Contact local suppliers for equipment details"]),
            "raw_material_sources": biz.get("raw_materials", "Locally sourced agricultural produce from farmers and mandis."),
            "manufacturing_process": biz.get("production_process", "Standard food processing workflow. Contact industry experts for detailed SOP."),
            "investment_breakdown": f"Total Estimated Investment: {biz['investment']}. This covers machinery procurement, raw material for initial batches, FSSAI/GST/MSME licensing, packaging material, marketing setup, and 3 months working capital.",
            "operational_costs": f"Monthly operational costs include raw materials (40-50% of revenue), labor (15-20%), electricity & fuel (8-12%), packaging (5-8%), and logistics (5-10%). Keep overhead below 80% of revenue for healthy margins.",
            "expected_revenue": biz.get("monthly_revenue", "₹2-5 Lakhs/month depending on scale and market reach."),
            "profit_margin": biz.get("profit_margin", biz.get("roi", "20-35%")),
            "breakeven_period": biz.get("breakeven", "12-18 months"),
            "export_potential": biz.get("export_potential", "Domestic market focused. Export potential to be evaluated."),
            "government_schemes": resolved_schemes,
            "startup_roadmap": [
                "Month 1-2: Market research, business plan finalization, MSME/FSSAI registration",
                "Month 2-3: Secure funding (bank loan + subsidy application)",
                "Month 3-4: Procure machinery, set up production facility",
                "Month 4-5: Trial production, quality testing, packaging design",
                "Month 5-6: Soft launch, local market distribution, collect feedback",
                "Month 6-8: Scale up production, expand distribution network",
                "Month 8-12: Brand building, online presence, explore B2B partnerships",
                "Month 12+: Evaluate export potential, apply for government export schemes"
            ]
        }
        return plan
