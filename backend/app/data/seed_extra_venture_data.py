"""
Seed script for Buyers and Success Stories exactly mapping to the previous logic.
"""
import json
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.extra_venture_models import BuyerDirectory, SuccessStory

BUYERS = [
    {"buyer_name": "Godavari Spice Exports", "buyer_type": "Export Trader", "product_category": "Spices", "annual_capacity": "5000 MT", "location": "Kochi", "state": "Kerala", "latitude": 9.9312, "longitude": 76.2673, "phone_number": "+91-9876543210", "email": "contact@godavarisexport.in"},
    {"buyer_name": "ITC Agri Business", "buyer_type": "Wholesale Trader", "product_category": "Wheat", "annual_capacity": "10000 MT", "location": "Indore", "state": "Madhya Pradesh", "latitude": 22.7196, "longitude": 75.8577, "phone_number": "+91-9876543211", "email": "procurement@itc.in"},
    {"buyer_name": "Patanjali Ayurved Ltd", "buyer_type": "Food Processing Unit", "product_category": "Herbs", "annual_capacity": "2000 MT", "location": "Haridwar", "state": "Uttarakhand", "latitude": 29.9457, "longitude": 78.1642, "phone_number": "+91-9876543212", "email": "purchasing@patanjali.in"},
    {"buyer_name": "Reliance Fresh Procurement", "buyer_type": "Retail Distributor", "product_category": "Vegetables", "annual_capacity": "50000 MT", "location": "Mumbai", "state": "Maharashtra", "latitude": 19.0760, "longitude": 72.8777, "phone_number": "+91-9876543213", "email": "fresh@reliance.in"},
    {"buyer_name": "Adani Wilmar", "buyer_type": "Food Processing Unit", "product_category": "Oilseeds", "annual_capacity": "15000 MT", "location": "Mundra", "state": "Gujarat", "latitude": 22.8351, "longitude": 69.7348, "phone_number": "+91-9876543214", "email": "info@adaniwilmar.in"},
    {"buyer_name": "Sahyadri Farms", "buyer_type": "Wholesale Trader", "product_category": "Fruits", "annual_capacity": "25000 MT", "location": "Nashik", "state": "Maharashtra", "latitude": 20.0110, "longitude": 73.7903, "phone_number": "+91-9876543215", "email": "trade@sahyadrifarms.com"},
    {"buyer_name": "Everest Spices", "buyer_type": "Food Processing Unit", "product_category": "Spices", "annual_capacity": "8000 MT", "location": "Umbergaon", "state": "Gujarat", "latitude": 20.1917, "longitude": 72.7538, "phone_number": "+91-9876543216", "email": "spicebuy@everest.in"},
    {"buyer_name": "BigBasket Farm Direct", "buyer_type": "Retail Distributor", "product_category": "Vegetables", "annual_capacity": "40000 MT", "location": "Bengaluru", "state": "Karnataka", "latitude": 12.9716, "longitude": 77.5946, "phone_number": "+91-9876543217", "email": "farms@bigbasket.com"},
    {"buyer_name": "Mahindra Agri Solutions", "buyer_type": "Export Trader", "product_category": "Pulses", "annual_capacity": "12000 MT", "location": "Jaipur", "state": "Rajasthan", "latitude": 26.9124, "longitude": 75.7873, "phone_number": "+91-9876543218", "email": "agri@mahindra.com"},
    {"buyer_name": "Mother Dairy", "buyer_type": "Food Processing Unit", "product_category": "Dairy", "annual_capacity": "30000 MT", "location": "Delhi", "state": "Delhi", "latitude": 28.7041, "longitude": 77.1025, "phone_number": "+91-9876543219", "email": "procure@motherdairy.com"},
    {"buyer_name": "Telangana Food Park Traders", "buyer_type": "Food Processing Unit", "product_category": "Tomato", "annual_capacity": "4500 MT", "location": "Warangal", "state": "Telangana", "latitude": 17.9689, "longitude": 79.5941, "phone_number": "+91-8000000001", "email": "warangal@tfp.in"},
    {"buyer_name": "Deccan Wholesale Hub", "buyer_type": "Wholesale Trader", "product_category": "Tomato", "annual_capacity": "12000 MT", "location": "Hyderabad", "state": "Telangana", "latitude": 17.3850, "longitude": 78.4867, "phone_number": "+91-8000000002", "email": "hub@deccanwholesale.com"},
    {"buyer_name": "Karimnagar Retail Network", "buyer_type": "Retail Distributor", "product_category": "Tomato", "annual_capacity": "3200 MT", "location": "Karimnagar", "state": "Telangana", "latitude": 18.4386, "longitude": 79.1288, "phone_number": "+91-8000000003", "email": "retail@krn.in"}
]

STORIES = [
    {
        "farmer_name": "Ramesh Reddy",
        "location": "Warangal",
        "state": "Telangana",
        "crop": "Tomato",
        "business_type": "Tomato Puree & Sauce Manufacturing",
        "investment": "₹7.5 Lakhs",
        "monthly_revenue": "₹3.2 Lakhs",
        "annual_profit": "₹9.6 Lakhs",
        "year_started": 2021,
        "story": "Facing post-harvest losses and price drops during peak season, I decided to stop selling raw tomatoes. With a small loan, I purchased a pulping machine and boiler. Now, I buy tomatoes from 10 neighboring farms and supply puree to 40 restaurants in Hyderabad.",
        "implementation_steps": ["Registered an MSME", "Applied for PMFME scheme subsidy (35%)", "Bought a 200kg/hr pulper", "Got FSSAI license", "Contracted with local restaurants"],
        "schemes_used": ["PMFME", "MUDRA Loan"],
        "contact_phone": "+91-9999888877"
    },
    {
        "farmer_name": "Suresh Patil",
        "location": "Nashik",
        "state": "Maharashtra",
        "crop": "Onion",
        "business_type": "Onion Flakes and Powder",
        "investment": "₹12 Lakhs",
        "monthly_revenue": "₹4 Lakhs",
        "annual_profit": "₹12 Lakhs",
        "year_started": 2020,
        "story": "Onion prices fluctuated wildly, sometimes dropping to ₹2/kg. I invested in a solar dehydration unit. Now we export dehydrated onion flakes to the Middle East.",
        "implementation_steps": ["Setup solar dryers", "Obtained export license (APEDA)", "Trained staff in hygiene", "Secured a Gulf buyer via trade fair"],
        "schemes_used": ["APEDA Export Assistance", "Agriculture Infrastructure Fund"],
        "contact_phone": "+91-9999888866"
    },
    {
        "farmer_name": "Anita Sharma",
        "location": "Kangra",
        "state": "Himachal",
        "crop": "Millets",
        "business_type": "Millet Health Bars & Cookies",
        "investment": "₹5 Lakhs",
        "monthly_revenue": "₹2 Lakhs",
        "annual_profit": "₹8 Lakhs",
        "year_started": 2022,
        "story": "Ragi and Bajra were largely ignored until the Millet boom. We started a women's cooperative making sugar-free millet bars. We now sell on Amazon.",
        "implementation_steps": ["Formed SHG (Self Help Group)", "Developed standardized recipes", "Got branding and packaging done", "Listed on E-commerce"],
        "schemes_used": ["NRLM (National Rural Livelihoods Mission)"],
        "contact_phone": "+91-9999888855"
    }
]

def run_seed():
    db = SessionLocal()
    try:
        if db.query(BuyerDirectory).count() == 0:
            print("Seeding Buyer Directory...")
            for b in BUYERS:
                db.add(BuyerDirectory(**b))
            db.commit()

        if db.query(SuccessStory).count() == 0:
            print("Seeding Success Stories...")
            for s in STORIES:
                s_copy = s.copy()
                s_copy["implementation_steps"] = json.dumps(s_copy["implementation_steps"])
                s_copy["schemes_used"] = json.dumps(s_copy["schemes_used"])
                db.add(SuccessStory(**s_copy))
            db.commit()
            
        print("Successfully seeded Extra Venture Data.")
    except Exception as e:
        print(f"Error seeding Extra Venture Data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
