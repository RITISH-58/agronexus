import json
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models import agri_business_model as models

def run_seed():
    db = SessionLocal()
    try:
        count = db.query(models.AgriBusiness).count()
        if count > 0:
            print("AgriBusiness data already seeded.")
            return

        print("Seeding new AgriBusiness Blueprint data...")

        blueprints = [
            {
                "business_name": "Tomato Sauce Processing Unit",
                "crop_type": "Tomato",
                "category": "Food Processing",
                "investment": "₹6–10 Lakhs",
                "roi": "30–40%",
                "revenue_range": "₹2.5–4 Lakhs",
                "profit_margin": "22–28%",
                "break_even": "12–16 Months",
                "market_demand_level": "Very High",
                "investment_breakdown": {
                    "Machinery Cost": "₹3.5 Lakhs",
                    "Processing Equipment": "₹1.2 Lakhs",
                    "Packaging Setup": "₹80,000",
                    "Working Capital": "₹2 Lakhs",
                    "Total Investment": "₹7.5 Lakhs"
                },
                "production_capacity": {
                    "Raw Tomato Required": "1200 kg per day",
                    "Finished Sauce Output": "850 bottles per day",
                    "Monthly Production": "25,000 bottles"
                },
                "revenue_projection": {
                    "Selling Price per Bottle": "₹120",
                    "Monthly Revenue": "₹3.2 Lakhs",
                    "Monthly Expenses": "₹2.4 Lakhs",
                    "Estimated Monthly Profit": "₹80,000"
                },
                "market_demand": {
                    "Level": "Very High",
                    "Growth": "18% annually",
                    "Buyers": ["Restaurants", "Supermarkets", "Food Distributors", "Online Grocery Platforms"],
                    "Cities": ["Hyderabad", "Warangal", "Karimnagar"]
                },
                "machinery": [
                    "Tomato Washer", "Pulper Machine", "Steam Jacketed Kettle", "Bottle Filling Machine", "Sealing Machine"
                ],
                "skills_required": [
                    "Basic food processing knowledge", "Packaging and branding", "Quality control"
                ],
                "schemes": [
                    {
                        "name": "PMFME Scheme",
                        "benefit": "35% capital subsidy",
                        "link": "https://mofpi.gov.in/pmfme"
                    },
                    {
                        "name": "Agriculture Infrastructure Fund",
                        "benefit": "Up to ₹2 Crore loan support",
                        "link": "https://agriinfra.dac.gov.in"
                    }
                ],
                "implementation_steps": [
                    "Register MSME",
                    "Apply for PMFME subsidy",
                    "Purchase machinery",
                    "Setup processing unit",
                    "Connect with local retailers",
                    "Launch packaged tomato sauce brand"
                ]
            },
            {
                "business_name": "Turmeric Powder Processing Facility",
                "crop_type": "Turmeric",
                "category": "Spice Processing",
                "investment": "₹5–8 Lakhs",
                "roi": "35–45%",
                "revenue_range": "₹3–5 Lakhs",
                "profit_margin": "25–35%",
                "break_even": "10–14 Months",
                "market_demand_level": "Trending",
                "investment_breakdown": {
                    "Grinding & Polishing Setup": "₹3 Lakhs",
                    "Boiling/Drying Equipment": "₹1.5 Lakhs",
                    "Packaging Unit": "₹70,000",
                    "Working Capital": "₹1.5 Lakhs",
                    "Total Investment": "₹6.7 Lakhs"
                },
                "production_capacity": {
                    "Raw Turmeric Needed": "500 kg per day",
                    "Powder Output": "400 kg per day",
                    "Monthly Capacity": "10,000 kg"
                },
                "revenue_projection": {
                    "Wholesale Price per Kg": "₹280",
                    "Monthly Revenue": "₹4.2 Lakhs",
                    "Monthly Expenses": "₹2.8 Lakhs",
                    "Estimated Monthly Profit": "₹1.4 Lakhs"
                },
                "market_demand": {
                    "Level": "Trending",
                    "Growth": "22% annually (export boom)",
                    "Buyers": ["Spice wholesalers", "Export houses", "Direct to consumer brands", "Ayurvedic companies"],
                    "Cities": ["Nizamabad", "Mumbai", "Chennai", "Kochi"]
                },
                "machinery": [
                    "Turmeric Boiler", "Polishing Drum", "Pulverizer / Grinding Machine", "Sieving Machine", "Weighing & Sealing"
                ],
                "skills_required": [
                    "Drying and curing expertise", "Quality testing (Curcumin content)", "B2B sales"
                ],
                "schemes": [
                    {
                        "name": "Spices Board Export Subsidy",
                        "benefit": "Financial assistance for value addition",
                        "link": "http://www.indianspices.com/"
                    },
                    {
                        "name": "MUDRA Loan",
                        "benefit": "Up to ₹10 Lakhs uncollateralized loan",
                        "link": "https://www.mudra.org.in/"
                    }
                ],
                "implementation_steps": [
                    "Source high-curcumin turmeric locally",
                    "Establish drying and boiling facility",
                    "Install pulverizer and sieving units",
                    "Clear FSSAI food safety licenses",
                    "Design attractive export-ready packaging",
                    "Contact B2B spice boards and aggregators"
                ]
            },
            {
                "business_name": "Cold Pressed Groundnut Oil Extraction",
                "crop_type": "Groundnut",
                "category": "Oil Extraction",
                "investment": "₹8–15 Lakhs",
                "roi": "28–38%",
                "revenue_range": "₹4–7 Lakhs",
                "profit_margin": "20–25%",
                "break_even": "14–18 Months",
                "market_demand_level": "High",
                "investment_breakdown": {
                    "Wooden Ghani Machine (x2)": "₹4 Lakhs",
                    "Filter Press Model": "₹1.5 Lakhs",
                    "Storage Tanks & Bottles": "₹1 Lakhs",
                    "Working Capital & Rent": "₹3 Lakhs",
                    "Total Investment": "₹9.5 Lakhs"
                },
                "production_capacity": {
                    "Groundnut Seeds Required": "1000 kg per day",
                    "Oil Yield (40%)": "400 Liters per day",
                    "Monthly Output": "10,000 Liters"
                },
                "revenue_projection": {
                    "Selling Price per Liter": "₹250",
                    "Monthly Revenue": "₹5.5 Lakhs",
                    "Monthly Expenses": "₹4.2 Lakhs",
                    "Estimated Monthly Profit": "₹1.3 Lakhs"
                },
                "market_demand": {
                    "Level": "High",
                    "Growth": "15% annually (health conscious trend)",
                    "Buyers": ["Health food stores", "Premium supermarkets", "Direct D2C Subscriptions", "Organic markets"],
                    "Cities": ["Bengaluru", "Delhi NCR", "Pune", "Hyderabad"]
                },
                "machinery": [
                    "Wood-pressed Oil Extraction Machine (Ghani)", "Oil Filter Press Machine", "Stainless Steel Storage Tanks", "Bottle Filling Unit"
                ],
                "skills_required": [
                    "Machinery operation", "Seed quality inspection", "Digital marketing for D2C"
                ],
                "schemes": [
                    {
                        "name": "PMFME Scheme",
                        "benefit": "Up to 35% subsidy on machinery",
                        "link": "https://mofpi.gov.in/pmfme"
                    },
                    {
                        "name": "KVIC Margin Money Scheme",
                        "benefit": "25-35% subsidy for rural enterprises",
                        "link": "https://www.kviconline.gov.in/"
                    }
                ],
                "implementation_steps": [
                    "Secure a clean, FSSAI-compliant space",
                    "Purchase wood-press machines",
                    "Secure high quality, aflatoxin-free groundnuts",
                    "Establish a D2C brand and website",
                    "Implement a bottle return subscription model",
                    "Expand supply to local organic grocers"
                ]
            },
            {
                "business_name": "Premium Rice Bran Oil Mill",
                "crop_type": "Rice",
                "category": "Oil Extraction",
                "investment": "₹20–40 Lakhs",
                "roi": "25–35%",
                "revenue_range": "₹10–20 Lakhs",
                "profit_margin": "15–20%",
                "break_even": "24–30 Months",
                "market_demand_level": "High",
                "investment_breakdown": {
                    "Solvent Extraction Plant": "₹18 Lakhs",
                    "Refining Equipment": "₹8 Lakhs",
                    "Factory Setup & Utilities": "₹5 Lakhs",
                    "Working Capital": "₹5 Lakhs",
                    "Total Investment": "₹36 Lakhs"
                },
                "production_capacity": {
                    "Raw Bran Required": "5000 kg per day",
                    "Oil Yield (16%)": "800 Liters per day",
                    "Monthly Output": "20,000 Liters"
                },
                "revenue_projection": {
                    "Wholesale Price per Liter": "₹140",
                    "Monthly Revenue": "₹15 Lakhs",
                    "Monthly Expenses": "₹12 Lakhs",
                    "Estimated Monthly Profit": "₹3 Lakhs"
                },
                "market_demand": {
                    "Level": "High",
                    "Growth": "12% annually",
                    "Buyers": ["FMCG Brands", "Restaurant Chains", "Wholesalers"],
                    "Cities": ["Pan India Wholesale"]
                },
                "machinery": [
                    "Bran Stabilizer", "Solvent Extraction Unit", "Desolventizer", "Oil Refiner", "Packaging Plant"
                ],
                "skills_required": [
                    "Chemical engineering basics", "Large scale operations", "B2B supply chain management"
                ],
                "schemes": [
                    {
                        "name": "SAMPADA Scheme",
                        "benefit": "Mega food park grants",
                        "link": "https://mofpi.gov.in/"
                    }
                ],
                "implementation_steps": [
                    "Partner with local rice mills for steady bran supply",
                    "Set up heavy machinery and safety compliance",
                    "Obtain industrial pollution clearances",
                    "Establish B2B contracts for oil and de-oiled cake",
                    "Commence trial production"
                ]
            },
            {
                "business_name": "Millet Energy Bar Manufacturing",
                "crop_type": "Millets",
                "category": "Food Processing",
                "investment": "₹4–7 Lakhs",
                "roi": "40–50%",
                "revenue_range": "₹2–4 Lakhs",
                "profit_margin": "30–40%",
                "break_even": "8–12 Months",
                "market_demand_level": "Trending",
                "investment_breakdown": {
                    "Roasting & Mixing DB": "₹1.5 Lakhs",
                    "Forming & Cutting Machine": "₹2 Lakhs",
                    "Flow Wrapper": "₹1 Lakhs",
                    "Working Capital": "₹1 Lakhs",
                    "Total Investment": "₹5.5 Lakhs"
                },
                "production_capacity": {
                    "Raw Materials": "100 kg per day",
                    "Bar Output": "2500 bars per day",
                    "Monthly Production": "60,000 bars"
                },
                "revenue_projection": {
                    "Selling Price per Bar": "₹30",
                    "Monthly Revenue": "₹3 Lakhs",
                    "Monthly Expenses": "₹1.8 Lakhs",
                    "Estimated Monthly Profit": "₹1.2 Lakhs"
                },
                "market_demand": {
                    "Level": "Trending",
                    "Growth": "35% annually",
                    "Buyers": ["Gyms", "Corporate Offices", "Supermarkets", "Online marketplaces"],
                    "Cities": ["Mumbai", "Bengaluru", "Delhi", "Chennai"]
                },
                "machinery": [
                    "Industrial Roaster", "Sigma Mixer", "Slab Former", "Guillotine Cutter", "Pillow Pouch Packaging"
                ],
                "skills_required": [
                    "Recipe formulation", "FMCG Branding", "Dietary compliance"
                ],
                "schemes": [
                    {
                        "name": "National Millet Mission",
                        "benefit": "Special incentives for millet products",
                        "link": "https://www.nutricereals.dac.gov.in/"
                    }
                ],
                "implementation_steps": [
                    "Develop standard recipe (No sugar added)",
                    "Secure nutritional lab testing reports",
                    "Design modern FMCG packaging",
                    "Set up small scale production line",
                    "Launch via Instagram and Amazon",
                    "Distribute to local gyms and cafes"
                ]
            }
        ]

        for b_data in blueprints:
            biz = models.AgriBusiness(
                business_name=b_data["business_name"],
                crop_type=b_data["crop_type"],
                category=b_data["category"],
                investment=b_data["investment"],
                roi=b_data["roi"],
                revenue_range=b_data["revenue_range"],
                profit_margin=b_data["profit_margin"],
                break_even=b_data["break_even"],
                market_demand_level=b_data["market_demand_level"],
                investment_breakdown=json.dumps(b_data["investment_breakdown"]),
                production_capacity=json.dumps(b_data["production_capacity"]),
                revenue_projection=json.dumps(b_data["revenue_projection"]),
                market_demand=json.dumps(b_data["market_demand"]),
                machinery=json.dumps(b_data["machinery"]),
                skills_required=json.dumps(b_data["skills_required"]),
                schemes=json.dumps(b_data["schemes"]),
                implementation_steps=json.dumps(b_data["implementation_steps"])
            )
            db.add(biz)
        
        db.commit()
        print(f"Successfully seeded {len(blueprints)} high-quality Business Blueprints.")
    except Exception as e:
        print(f"Error seeding DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
