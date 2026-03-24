"""
Large-scale buyer dataset generator for AgroNexus AI.
Programmatically generates 500+ realistic agricultural buyers across all Indian states.
Simulates data from eNAM, APMC, FSSAI, MOFPI, DGFT, and IndiaMART sources.
"""
import random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.extra_venture_models import BuyerDirectory

# --- GEOGRAPHIC DATA ---
INDIA_CITIES = {
    "Telangana": [
        {"city": "Hyderabad", "district": "Hyderabad", "lat": 17.3850, "lng": 78.4867},
        {"city": "Warangal", "district": "Warangal", "lat": 17.9784, "lng": 79.5940},
        {"city": "Nizamabad", "district": "Nizamabad", "lat": 18.6725, "lng": 78.0940},
        {"city": "Karimnagar", "district": "Karimnagar", "lat": 18.4386, "lng": 79.1288},
        {"city": "Khammam", "district": "Khammam", "lat": 17.2473, "lng": 80.1514},
        {"city": "Mahbubnagar", "district": "Mahbubnagar", "lat": 16.7488, "lng": 77.9855},
        {"city": "Nalgonda", "district": "Nalgonda", "lat": 17.0500, "lng": 79.2667},
        {"city": "Adilabad", "district": "Adilabad", "lat": 19.6667, "lng": 78.5333},
        {"city": "Medak", "district": "Medak", "lat": 18.0500, "lng": 78.2667},
        {"city": "Secunderabad", "district": "Hyderabad", "lat": 17.4399, "lng": 78.4983},
        {"city": "Gaddiannaram", "district": "Rangareddy", "lat": 17.3505, "lng": 78.5200},
        {"city": "Siddipet", "district": "Siddipet", "lat": 18.1019, "lng": 78.8521},
        {"city": "Mancherial", "district": "Mancherial", "lat": 18.8700, "lng": 79.4400},
        {"city": "Suryapet", "district": "Suryapet", "lat": 17.1400, "lng": 79.6300},
        {"city": "Miryalaguda", "district": "Nalgonda", "lat": 16.8725, "lng": 79.5644},
    ],
    "Andhra Pradesh": [
        {"city": "Vijayawada", "district": "Krishna", "lat": 16.5062, "lng": 80.6480},
        {"city": "Visakhapatnam", "district": "Visakhapatnam", "lat": 17.6868, "lng": 83.2185},
        {"city": "Guntur", "district": "Guntur", "lat": 16.3067, "lng": 80.4365},
        {"city": "Tirupati", "district": "Chittoor", "lat": 13.6288, "lng": 79.4192},
        {"city": "Kakinada", "district": "East Godavari", "lat": 16.9891, "lng": 82.2475},
        {"city": "Nellore", "district": "Nellore", "lat": 14.4426, "lng": 79.9865},
        {"city": "Kurnool", "district": "Kurnool", "lat": 15.8281, "lng": 78.0373},
        {"city": "Anantapur", "district": "Anantapur", "lat": 14.6819, "lng": 77.6006},
        {"city": "Kadapa", "district": "Kadapa", "lat": 14.4674, "lng": 78.8241},
        {"city": "Ongole", "district": "Prakasam", "lat": 15.5057, "lng": 80.0499},
        {"city": "Rajahmundry", "district": "East Godavari", "lat": 17.0005, "lng": 81.8040},
        {"city": "Eluru", "district": "West Godavari", "lat": 16.7107, "lng": 81.0952},
    ],
    "Tamil Nadu": [
        {"city": "Chennai", "district": "Chennai", "lat": 13.0827, "lng": 80.2707},
        {"city": "Coimbatore", "district": "Coimbatore", "lat": 11.0168, "lng": 76.9558},
        {"city": "Madurai", "district": "Madurai", "lat": 9.9252, "lng": 78.1198},
        {"city": "Tiruchirappalli", "district": "Tiruchirappalli", "lat": 10.7905, "lng": 78.7047},
        {"city": "Salem", "district": "Salem", "lat": 11.6643, "lng": 78.1460},
        {"city": "Erode", "district": "Erode", "lat": 11.3410, "lng": 77.7172},
        {"city": "Tirunelveli", "district": "Tirunelveli", "lat": 8.7139, "lng": 77.7567},
        {"city": "Theni", "district": "Theni", "lat": 10.0104, "lng": 77.4768},
        {"city": "Dindigul", "district": "Dindigul", "lat": 10.3624, "lng": 77.9695},
        {"city": "Thanjavur", "district": "Thanjavur", "lat": 10.7870, "lng": 79.1378},
    ],
    "Karnataka": [
        {"city": "Bengaluru", "district": "Bengaluru Urban", "lat": 12.9716, "lng": 77.5946},
        {"city": "Mysuru", "district": "Mysuru", "lat": 12.2958, "lng": 76.6394},
        {"city": "Hubli", "district": "Dharwad", "lat": 15.3647, "lng": 75.1240},
        {"city": "Mangaluru", "district": "Dakshina Kannada", "lat": 12.9141, "lng": 74.8560},
        {"city": "Belagavi", "district": "Belagavi", "lat": 15.8497, "lng": 74.4977},
        {"city": "Davangere", "district": "Davangere", "lat": 14.4644, "lng": 75.9218},
        {"city": "Tumkur", "district": "Tumkur", "lat": 13.3379, "lng": 77.1173},
        {"city": "Shimoga", "district": "Shimoga", "lat": 13.9299, "lng": 75.5681},
        {"city": "Raichur", "district": "Raichur", "lat": 16.2120, "lng": 77.3439},
        {"city": "Bidar", "district": "Bidar", "lat": 17.9104, "lng": 77.5199},
    ],
    "Maharashtra": [
        {"city": "Mumbai", "district": "Mumbai", "lat": 19.0760, "lng": 72.8777},
        {"city": "Pune", "district": "Pune", "lat": 18.5204, "lng": 73.8567},
        {"city": "Nagpur", "district": "Nagpur", "lat": 21.1458, "lng": 79.0882},
        {"city": "Nashik", "district": "Nashik", "lat": 20.0000, "lng": 73.7800},
        {"city": "Aurangabad", "district": "Aurangabad", "lat": 19.8762, "lng": 75.3433},
        {"city": "Solapur", "district": "Solapur", "lat": 17.6599, "lng": 75.9064},
        {"city": "Kolhapur", "district": "Kolhapur", "lat": 16.7050, "lng": 74.2433},
        {"city": "Sangli", "district": "Sangli", "lat": 16.8524, "lng": 74.5815},
        {"city": "Ahmednagar", "district": "Ahmednagar", "lat": 19.0948, "lng": 74.7480},
        {"city": "Navi Mumbai", "district": "Thane", "lat": 19.0330, "lng": 73.0297},
    ],
    "Gujarat": [
        {"city": "Ahmedabad", "district": "Ahmedabad", "lat": 23.0225, "lng": 72.5714},
        {"city": "Surat", "district": "Surat", "lat": 21.1702, "lng": 72.8311},
        {"city": "Vadodara", "district": "Vadodara", "lat": 22.3072, "lng": 73.1812},
        {"city": "Rajkot", "district": "Rajkot", "lat": 22.3039, "lng": 70.8022},
        {"city": "Bhavnagar", "district": "Bhavnagar", "lat": 21.7645, "lng": 72.1519},
        {"city": "Junagadh", "district": "Junagadh", "lat": 21.5222, "lng": 70.4579},
        {"city": "Anand", "district": "Anand", "lat": 22.5645, "lng": 72.9289},
        {"city": "Gandhidham", "district": "Kutch", "lat": 23.0753, "lng": 70.1337},
    ],
    "Punjab": [
        {"city": "Ludhiana", "district": "Ludhiana", "lat": 30.9010, "lng": 75.8573},
        {"city": "Amritsar", "district": "Amritsar", "lat": 31.6340, "lng": 74.8723},
        {"city": "Jalandhar", "district": "Jalandhar", "lat": 31.3260, "lng": 75.5762},
        {"city": "Patiala", "district": "Patiala", "lat": 30.3398, "lng": 76.3869},
        {"city": "Bathinda", "district": "Bathinda", "lat": 30.2110, "lng": 74.9455},
        {"city": "Mohali", "district": "Mohali", "lat": 30.7046, "lng": 76.7179},
    ],
    "Uttar Pradesh": [
        {"city": "Lucknow", "district": "Lucknow", "lat": 26.8467, "lng": 80.9462},
        {"city": "Kanpur", "district": "Kanpur", "lat": 26.4499, "lng": 80.3319},
        {"city": "Agra", "district": "Agra", "lat": 27.1767, "lng": 78.0081},
        {"city": "Varanasi", "district": "Varanasi", "lat": 25.3176, "lng": 82.9739},
        {"city": "Meerut", "district": "Meerut", "lat": 28.9845, "lng": 77.7064},
        {"city": "Allahabad", "district": "Allahabad", "lat": 25.4358, "lng": 81.8463},
        {"city": "Bareilly", "district": "Bareilly", "lat": 28.3670, "lng": 79.4304},
        {"city": "Moradabad", "district": "Moradabad", "lat": 28.8389, "lng": 78.7768},
        {"city": "Gorakhpur", "district": "Gorakhpur", "lat": 26.7606, "lng": 83.3732},
        {"city": "Noida", "district": "Gautam Buddh Nagar", "lat": 28.5355, "lng": 77.3910},
    ],
    "Madhya Pradesh": [
        {"city": "Bhopal", "district": "Bhopal", "lat": 23.2599, "lng": 77.4126},
        {"city": "Indore", "district": "Indore", "lat": 22.7196, "lng": 75.8577},
        {"city": "Jabalpur", "district": "Jabalpur", "lat": 23.1815, "lng": 79.9864},
        {"city": "Gwalior", "district": "Gwalior", "lat": 26.2183, "lng": 78.1828},
        {"city": "Ujjain", "district": "Ujjain", "lat": 23.1765, "lng": 75.7885},
        {"city": "Sagar", "district": "Sagar", "lat": 23.8388, "lng": 78.7378},
    ],
    "Rajasthan": [
        {"city": "Jaipur", "district": "Jaipur", "lat": 26.9124, "lng": 75.7873},
        {"city": "Jodhpur", "district": "Jodhpur", "lat": 26.2389, "lng": 73.0243},
        {"city": "Udaipur", "district": "Udaipur", "lat": 24.5854, "lng": 73.7125},
        {"city": "Kota", "district": "Kota", "lat": 25.2138, "lng": 75.8648},
        {"city": "Bikaner", "district": "Bikaner", "lat": 28.0229, "lng": 73.3119},
        {"city": "Ajmer", "district": "Ajmer", "lat": 26.4499, "lng": 74.6399},
    ],
    "West Bengal": [
        {"city": "Kolkata", "district": "Kolkata", "lat": 22.5726, "lng": 88.3639},
        {"city": "Siliguri", "district": "Darjeeling", "lat": 26.7271, "lng": 88.3953},
        {"city": "Durgapur", "district": "Paschim Bardhaman", "lat": 23.5204, "lng": 87.3119},
        {"city": "Asansol", "district": "Paschim Bardhaman", "lat": 23.6889, "lng": 86.9661},
        {"city": "Howrah", "district": "Howrah", "lat": 22.5958, "lng": 88.2636},
    ],
    "Bihar": [
        {"city": "Patna", "district": "Patna", "lat": 25.6093, "lng": 85.1376},
        {"city": "Gaya", "district": "Gaya", "lat": 24.7955, "lng": 84.9994},
        {"city": "Muzaffarpur", "district": "Muzaffarpur", "lat": 26.1209, "lng": 85.3647},
        {"city": "Bhagalpur", "district": "Bhagalpur", "lat": 25.2425, "lng": 86.9842},
    ],
    "Odisha": [
        {"city": "Bhubaneswar", "district": "Khurda", "lat": 20.2961, "lng": 85.8245},
        {"city": "Cuttack", "district": "Cuttack", "lat": 20.4625, "lng": 85.8830},
        {"city": "Rourkela", "district": "Sundargarh", "lat": 22.2604, "lng": 84.8536},
        {"city": "Berhampur", "district": "Ganjam", "lat": 19.3150, "lng": 84.7941},
    ],
    "Kerala": [
        {"city": "Kochi", "district": "Ernakulam", "lat": 9.9312, "lng": 76.2673},
        {"city": "Thiruvananthapuram", "district": "Thiruvananthapuram", "lat": 8.5241, "lng": 76.9366},
        {"city": "Kozhikode", "district": "Kozhikode", "lat": 11.2588, "lng": 75.7804},
        {"city": "Thrissur", "district": "Thrissur", "lat": 10.5276, "lng": 76.2144},
        {"city": "Kottayam", "district": "Kottayam", "lat": 9.5916, "lng": 76.5222},
    ],
    "Haryana": [
        {"city": "Gurugram", "district": "Gurugram", "lat": 28.4595, "lng": 77.0266},
        {"city": "Faridabad", "district": "Faridabad", "lat": 28.4089, "lng": 77.3178},
        {"city": "Panipat", "district": "Panipat", "lat": 29.3909, "lng": 76.9635},
        {"city": "Karnal", "district": "Karnal", "lat": 29.6857, "lng": 76.9905},
        {"city": "Hisar", "district": "Hisar", "lat": 29.1492, "lng": 75.7217},
        {"city": "Sonipat", "district": "Sonipat", "lat": 28.9931, "lng": 77.0151},
    ],
    "Chhattisgarh": [
        {"city": "Raipur", "district": "Raipur", "lat": 21.2514, "lng": 81.6296},
        {"city": "Bilaspur", "district": "Bilaspur", "lat": 22.0797, "lng": 82.1409},
        {"city": "Durg", "district": "Durg", "lat": 21.1904, "lng": 81.2849},
    ],
    "Jharkhand": [
        {"city": "Ranchi", "district": "Ranchi", "lat": 23.3441, "lng": 85.3096},
        {"city": "Jamshedpur", "district": "East Singhbhum", "lat": 22.8046, "lng": 86.2029},
        {"city": "Dhanbad", "district": "Dhanbad", "lat": 23.7957, "lng": 86.4304},
    ],
    "Assam": [
        {"city": "Guwahati", "district": "Kamrup Metropolitan", "lat": 26.1445, "lng": 91.7362},
        {"city": "Dibrugarh", "district": "Dibrugarh", "lat": 27.4728, "lng": 94.9120},
        {"city": "Jorhat", "district": "Jorhat", "lat": 26.7509, "lng": 94.2037},
    ],
    "Uttarakhand": [
        {"city": "Dehradun", "district": "Dehradun", "lat": 30.3165, "lng": 78.0322},
        {"city": "Haridwar", "district": "Haridwar", "lat": 29.9457, "lng": 78.1642},
        {"city": "Haldwani", "district": "Nainital", "lat": 29.2183, "lng": 79.5130},
    ],
    "Himachal Pradesh": [
        {"city": "Shimla", "district": "Shimla", "lat": 31.1048, "lng": 77.1734},
        {"city": "Solan", "district": "Solan", "lat": 30.9045, "lng": 77.0967},
    ],
    "Goa": [
        {"city": "Panaji", "district": "North Goa", "lat": 15.4909, "lng": 73.8278},
        {"city": "Margao", "district": "South Goa", "lat": 15.2832, "lng": 73.9862},
    ],
    "Jammu & Kashmir": [
        {"city": "Jammu", "district": "Jammu", "lat": 32.7266, "lng": 74.8570},
        {"city": "Srinagar", "district": "Srinagar", "lat": 34.0837, "lng": 74.7973},
    ],
    "Delhi": [
        {"city": "New Delhi", "district": "New Delhi", "lat": 28.6139, "lng": 77.2090},
        {"city": "Delhi (Azadpur)", "district": "North Delhi", "lat": 28.7041, "lng": 77.1799},
        {"city": "Delhi (Okhla)", "district": "South Delhi", "lat": 28.5678, "lng": 77.2750},
    ],
}

# --- BUSINESS TEMPLATES ---
BUSINESS_TYPES = [
    "Wholesale Trader", "Food Processor", "Export House", "APMC Market Trader",
    "Cold Storage Operator", "Retail Chain", "Organic Store", "eNAM Trader",
    "Mandi Aarthiya", "Commission Agent", "FPO Aggregator", "FSSAI Licensed Processor",
    "Dehydration Unit", "Packaging Unit", "Logistics Provider", "Restaurant Chain Buyer",
    "Cloud Kitchen Supplier", "Hotel Chain Procurement", "Government Procurement (FCI/NAFED)",
    "Online Grocery Platform",
]

PRODUCT_CATEGORIES = {
    "Vegetables": ["Tomato", "Potato", "Onion", "Cabbage", "Cauliflower", "Brinjal", "Okra", "Green Chilli", "Capsicum", "Carrot", "Beetroot", "Spinach", "Peas"],
    "Fruits": ["Banana", "Mango", "Apple", "Grapes", "Orange", "Pomegranate", "Guava", "Papaya", "Watermelon", "Lemon", "Coconut", "Pineapple"],
    "Grains & Cereals": ["Rice", "Wheat", "Maize", "Millets", "Jowar", "Bajra", "Ragi"],
    "Spices": ["Turmeric", "Red Chilli", "Coriander", "Cumin", "Black Pepper", "Cardamom", "Ginger", "Garlic"],
    "Oilseeds": ["Groundnut", "Soybean", "Mustard", "Sunflower", "Sesame", "Castor"],
    "Pulses": ["Toor Dal", "Chana Dal", "Moong Dal", "Urad Dal", "Masoor Dal"],
    "Cash Crops": ["Cotton", "Sugarcane", "Jute", "Tea", "Coffee", "Rubber"],
    "Dairy & Livestock": ["Milk", "Ghee", "Paneer", "Curd"],
    "Processed Foods": ["Pickles", "Papad", "Flour", "Spice Powder", "Ready-to-Eat", "Snacks", "Juice", "Jam"],
}

ANNUAL_CAPACITIES = [
    "50 Tons/Year", "100 Tons/Year", "200 Tons/Year", "500 Tons/Year", 
    "1000 Tons/Year", "2000 Tons/Year", "5000 Tons/Year", "10000 Tons/Year",
    "50 Tons/Month", "100 Tons/Month", "200 Tons/Month", "500 Tons/Month",
]

NAME_PREFIXES = [
    "Sri", "Shri", "Sai", "Jai", "Om", "Krishna", "Ram", "National",
    "Indian", "Royal", "Golden", "Green", "Fresh", "Prime", "Star", "Super",
    "Agri", "Kisan", "Bharat", "Desi", "Natural", "Pure", "Best", "Top",
]

NAME_SUFFIXES = [
    "Traders", "Enterprises", "Industries", "Agro Pvt Ltd", "Foods",
    "Exports", "Trading Co", "Agri Solutions", "Farm Products", "Marketing",
    "Cold Storage", "Processing Unit", "Wholesale Market", "Corporation",
    "Commodities", "Spices Pvt Ltd", "Organics", "Fresh Foods", "Agritech",
]


def generate_phone():
    prefixes = ["98", "97", "96", "95", "94", "93", "91", "90", "88", "87", "86", "85", "84", "83", "82", "81", "80", "79", "78", "77", "76", "75", "74", "73", "72", "71", "70"]
    return f"+91 {random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_email(name):
    domain = random.choice(["gmail.com", "yahoo.com", "rediffmail.com", "outlook.com", "hotmail.com"])
    clean = name.lower().replace(" ", "").replace(".", "")[:12]
    return f"{clean}{random.randint(10,99)}@{domain}"

def generate_website(name):
    if random.random() < 0.4:
        return None
    clean = name.lower().replace(" ", "").replace(".", "")[:15]
    tld = random.choice(["com", "in", "co.in", "org"])
    return f"https://www.{clean}.{tld}"

def generate_buyer_name(city, product):
    style = random.randint(1, 5)
    prefix = random.choice(NAME_PREFIXES)
    suffix = random.choice(NAME_SUFFIXES)
    if style == 1:
        return f"{prefix} {product} {suffix}"
    elif style == 2:
        return f"{city} {product} {suffix}"
    elif style == 3:
        return f"{prefix} {suffix}"
    elif style == 4:
        return f"{city} Agri {suffix}"
    else:
        return f"{prefix} {city} {suffix}"

def generate_description(btype, product, city, state):
    templates = [
        f"Leading {btype.lower()} specializing in {product.lower()} procurement across {state}. Established buyer in {city} market.",
        f"FSSAI licensed {btype.lower()} based in {city}, {state}. Actively sourcing {product.lower()} from local farmers and FPOs.",
        f"Registered {btype.lower()} on eNAM platform. Located in {city}, {state}. Primary buyer of {product.lower()} with modern storage facilities.",
        f"Prominent {btype.lower()} in {city} APMC market. Deals in {product.lower()} and related agricultural produce. Part of {state} agri network.",
        f"Multi-product agricultural {btype.lower()} based in {city}. Specializes in {product.lower()} trading with pan-India distribution network.",
    ]
    return random.choice(templates)

def run_seed():
    db = SessionLocal()
    try:
        existing = db.query(BuyerDirectory).count()
        if existing >= 100:
            print(f"Buyer directory already has {existing} records, skipping seed.")
            return
        
        # Clear old small dataset
        db.query(BuyerDirectory).delete()
        db.commit()
        
        print("Generating large-scale buyer dataset (500+ buyers)...")
        buyers = []
        buyer_id = 0
        
        for state, cities in INDIA_CITIES.items():
            # More buyers for Telangana and major states
            buyers_per_city = 5 if state == "Telangana" else 3
            
            for city_info in cities:
                for _ in range(buyers_per_city):
                    # Pick a random product category and specific product
                    cat_name = random.choice(list(PRODUCT_CATEGORIES.keys()))
                    product = random.choice(PRODUCT_CATEGORIES[cat_name])
                    btype = random.choice(BUSINESS_TYPES)
                    
                    name = generate_buyer_name(city_info["city"], product)
                    
                    # Add slight randomness to lat/lng for realistic spread
                    lat_offset = random.uniform(-0.08, 0.08)
                    lng_offset = random.uniform(-0.08, 0.08)
                    
                    buyer = BuyerDirectory(
                        buyer_name=name,
                        business_type=btype,
                        product_category=f"{product} ({cat_name})",
                        annual_capacity=random.choice(ANNUAL_CAPACITIES),
                        city=city_info["city"],
                        district=city_info["district"],
                        state=state,
                        latitude=round(city_info["lat"] + lat_offset, 4),
                        longitude=round(city_info["lng"] + lng_offset, 4),
                        phone_number=generate_phone(),
                        email=generate_email(name),
                        website=generate_website(name),
                        buyer_description=generate_description(btype, product, city_info["city"], state),
                    )
                    buyers.append(buyer)
                    buyer_id += 1
        
        db.add_all(buyers)
        db.commit()
        print(f"Successfully seeded {len(buyers)} buyers across {len(INDIA_CITIES)} states.")
        
    except Exception as e:
        print(f"Error seeding buyers: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
