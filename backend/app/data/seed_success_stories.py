"""
Large-scale Success Stories dataset generator for AgroNexus AI.
Generates 100+ realistic farmer success stories across 15 crops and 10 Indian states.
"""
import json
import random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.extra_venture_models import SuccessStory

# --- FARMER NAMES BY STATE ---
FARMER_NAMES = {
    "Telangana": ["Ramesh Reddy", "Srinivas Rao", "Lakshmi Devi", "Venkat Goud", "Anjali Sharma", "Mahesh Kumar", "Padma Reddy", "Krishna Murthy", "Sarita Kumari", "Ravi Teja"],
    "Andhra Pradesh": ["Narasimha Rao", "Suresh Babu", "Lakshmi Naidu", "Rajendra Prasad", "Durga Devi", "Venu Gopal", "Padmavathi", "Siva Kumar", "Anitha Reddy", "Chandra Mohan"],
    "Karnataka": ["Basavaraj Patil", "Shivanna Gowda", "Rekha Kumari", "Manjunath Hegde", "Radha Krishna", "Mallikarjun Swamy", "Kavitha Bai", "Ramanna Shetty", "Deepa Gowda", "Suresh Kumar"],
    "Tamil Nadu": ["Murugan Pillai", "Lakshmi Ammal", "Senthil Kumar", "Meenakshi Devi", "Rajkumar Nadar", "Tamilselvi", "Arun Prakash", "Gomathi Devi", "Karthik Vel", "Parvathy Sundaram"],
    "Maharashtra": ["Baburao Patil", "Sunita Jadhav", "Vitthal Shinde", "Mangala Deshmukh", "Rajesh Pawar", "Savitri Bai", "Nitin Kulkarni", "Anita More", "Kiran Gaikwad", "Prashant Wagh"],
    "Punjab": ["Harpal Singh", "Gurpreet Kaur", "Baljinder Singh", "Manpreet Kaur", "Amrik Singh", "Jaswant Kaur", "Daljit Singh", "Rajwinder Kaur", "Kuldeep Singh", "Simranjit Kaur"],
    "Uttar Pradesh": ["Ram Prasad Yadav", "Sunita Devi", "Shyam Lal Gupta", "Meera Sharma", "Rajendra Singh", "Kamla Devi", "Anil Kumar", "Savitri Devi", "Vipin Chandra", "Geeta Rani"],
    "Madhya Pradesh": ["Ratan Lal Patel", "Kamla Bai", "Shiv Kumar Sharma", "Durga Bai", "Mohan Lal Joshi", "Sunita Thakur", "Govind Sahu", "Rekha Devi", "Bhagwan Das", "Lakshmi Bai"],
    "Gujarat": ["Jayesh Patel", "Savitaben Shah", "Ramesh Desai", "Meenaben Patel", "Bharat Mehta", "Kokilaben Rana", "Haresh Modi", "Jayshriben Thakkar", "Kiran Vyas", "Damayanti Joshi"],
    "Rajasthan": ["Mohan Lal Sharma", "Sita Devi", "Babu Lal Meena", "Kamla Devi", "Hari Ram Jat", "Geeta Rathore", "Kishan Lal Gurjar", "Pushpa Devi", "Bhagchand Meena", "Santosh Kumari"],
}

DISTRICTS = {
    "Telangana": ["Karimnagar", "Warangal", "Nizamabad", "Khammam", "Nalgonda", "Adilabad", "Medak", "Siddipet", "Mahbubnagar", "Suryapet"],
    "Andhra Pradesh": ["Guntur", "Krishna", "East Godavari", "Chittoor", "Prakasam", "Kurnool", "Anantapur", "Nellore", "West Godavari", "Kadapa"],
    "Karnataka": ["Belgaum", "Dharwad", "Mysore", "Tumkur", "Shimoga", "Davanagere", "Raichur", "Bidar", "Mandya", "Hassan"],
    "Tamil Nadu": ["Salem", "Coimbatore", "Thanjavur", "Madurai", "Dindigul", "Erode", "Tirunelveli", "Theni", "Tiruchirappalli", "Namakkal"],
    "Maharashtra": ["Nashik", "Pune", "Sangli", "Kolhapur", "Ahmednagar", "Solapur", "Aurangabad", "Nagpur", "Jalgaon", "Satara"],
    "Punjab": ["Ludhiana", "Amritsar", "Patiala", "Bathinda", "Jalandhar", "Moga", "Sangrur", "Ferozepur", "Gurdaspur", "Hoshiarpur"],
    "Uttar Pradesh": ["Lucknow", "Agra", "Varanasi", "Meerut", "Bareilly", "Moradabad", "Gorakhpur", "Allahabad", "Kanpur", "Mathura"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Sagar", "Ujjain", "Rewa", "Gwalior", "Dewas", "Chhindwara", "Hoshangabad"],
    "Gujarat": ["Ahmedabad", "Surat", "Rajkot", "Vadodara", "Junagadh", "Anand", "Bhavnagar", "Mehsana", "Sabarkantha", "Banaskantha"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer", "Alwar", "Bharatpur", "Sikar", "Nagaur"],
}

# --- CROP-BASED BUSINESS TEMPLATES ---
# Each crop has multiple business templates with realistic data
CROP_BUSINESSES = {
    "Rice": [
        {"business_type": "Puffed Rice Manufacturing", "investment": "₹1.8 Lakhs", "monthly_income": "₹55,000", "yearly_income": "₹6.6 Lakhs", "products_sold": ["Puffed Rice (Murmura)", "Flavored Murmura"], "buyers_connected": ["Wholesale snack distributors", "Kirana stores"], "scheme": "PMFME", "steps": ["Registered MSME", "Applied for PMFME subsidy", "Purchased puffing machine", "Connected with wholesale traders", "Started local brand packaging"]},
        {"business_type": "Rice Flour Milling", "investment": "₹3.5 Lakhs", "monthly_income": "₹70,000", "yearly_income": "₹8.4 Lakhs", "products_sold": ["Rice Flour", "Idli Batter Flour"], "buyers_connected": ["Bakeries", "Supermarkets", "Hotels"], "scheme": "PMFME", "steps": ["Setup flour mill", "Purchased pulverizer and sifter", "Got FSSAI license", "Started distributing to bakeries", "Added idli batter flour line"]},
        {"business_type": "Rice Bran Collection", "investment": "₹80,000", "monthly_income": "₹35,000", "yearly_income": "₹4.2 Lakhs", "products_sold": ["Rice Bran", "Cattle Feed"], "buyers_connected": ["Oil extraction units", "Dairy farms"], "scheme": "MUDRA Loan", "steps": ["Collected rice bran from local mills", "Setup storage shed", "Connected with oil extraction units", "Added cattle feed mixing"]},
        {"business_type": "Organic Rice Export", "investment": "₹8 Lakhs", "monthly_income": "₹1.5 Lakhs", "yearly_income": "₹18 Lakhs", "products_sold": ["Organic Basmati Rice", "Brown Rice", "Red Rice"], "buyers_connected": ["Export agents", "Organic stores (BigBasket, Amazon)"], "scheme": "APEDA Export Grant", "steps": ["Got organic certification (NPOP)", "Contracted 20 farmers for organic rice", "Registered on APEDA", "First export shipment to Dubai", "Built brand on Amazon"]},
        {"business_type": "Rice Snack (Murukku) Production", "investment": "₹2.5 Lakhs", "monthly_income": "₹60,000", "yearly_income": "₹7.2 Lakhs", "products_sold": ["Rice Murukku", "Ribbon Pakoda", "Rice Chips"], "buyers_connected": ["Sweet shops", "Supermarkets", "NRI exporters"], "scheme": "PMEGP", "steps": ["Standardized traditional recipe", "Purchased semi-auto extruder and fryer", "Got FSSAI license", "Started selling through sweet shops", "Added export-quality packaging"]},
    ],
    "Tomato": [
        {"business_type": "Tomato Sauce Manufacturing", "investment": "₹5 Lakhs", "monthly_income": "₹90,000", "yearly_income": "₹10.8 Lakhs", "products_sold": ["Tomato Ketchup", "Tomato Sauce", "Chili Sauce"], "buyers_connected": ["Restaurants", "Supermarkets", "Hotels"], "scheme": "PMFME", "steps": ["Setup small-scale processing unit", "Purchased kettle and bottle filler", "Got FSSAI certification", "Launched local brand", "Distributed to 50+ restaurants"]},
        {"business_type": "Tomato Puree Processing", "investment": "₹7 Lakhs", "monthly_income": "₹1.2 Lakhs", "yearly_income": "₹14.4 Lakhs", "products_sold": ["Tomato Puree 1kg", "Tomato Paste 5kg"], "buyers_connected": ["Cloud kitchens", "Caterers", "Food manufacturers"], "scheme": "State Agri Subsidy", "steps": ["Bought tomatoes during glut at ₹5/kg", "Setup pulper and pasteurizer", "Packaged in aseptic pouches", "Supplied to 30 cloud kitchens", "Reduced farmer tomato wastage by 40%"]},
        {"business_type": "Sun-Dried Tomato Production", "investment": "₹3 Lakhs", "monthly_income": "₹1 Lakh", "yearly_income": "₹12 Lakhs", "products_sold": ["Sun-Dried Tomatoes", "Tomato in Olive Oil"], "buyers_connected": ["Gourmet restaurants", "Export agents (Italy, US)"], "scheme": "APEDA", "steps": ["Built solar tunnel dryers", "Selected Roma variety tomatoes", "Dried, salted and packed in olive oil jars", "First export to Italy", "Premium pricing at ₹800/kg"]},
        {"business_type": "Tomato Powder Production", "investment": "₹12 Lakhs", "monthly_income": "₹1.8 Lakhs", "yearly_income": "₹21.6 Lakhs", "products_sold": ["Tomato Powder", "Soup Mix Powder"], "buyers_connected": ["Snack seasoning companies", "Instant food brands"], "scheme": "Agriculture Infrastructure Fund", "steps": ["Setup spray drying unit with subsidy", "Processed 2 tons tomatoes daily", "Created fine tomato powder", "Supplied to 5 seasoning companies", "Added soup mix powder line"]},
        {"business_type": "Tomato Pickle Manufacturing", "investment": "₹1.5 Lakhs", "monthly_income": "₹40,000", "yearly_income": "₹4.8 Lakhs", "products_sold": ["Tomato Pickle", "Tomato Chutney", "Green Tomato Pickle"], "buyers_connected": ["Kirana stores", "Weekly markets", "Online (Amazon)"], "scheme": "PMEGP", "steps": ["Used traditional family recipe", "Setup small kitchen unit", "Got FSSAI license", "Listed on Amazon Handmade", "Orders grew to 500 jars/month"]},
    ],
    "Turmeric": [
        {"business_type": "Turmeric Powder Processing", "investment": "₹4 Lakhs", "monthly_income": "₹80,000", "yearly_income": "₹9.6 Lakhs", "products_sold": ["Turmeric Powder 100g/250g", "Haldi (Polished Fingers)"], "buyers_connected": ["Supermarkets", "Kiranas", "FMCG distributors"], "scheme": "Spices Board Subsidy", "steps": ["Bought dried turmeric from farmers", "Setup micro-pulverizer and packing machine", "Got FSSAI and Spices Board certification", "Started distributing through FMCG network", "Monthly production reached 5 tons"]},
        {"business_type": "Organic Turmeric Export", "investment": "₹10 Lakhs", "monthly_income": "₹2 Lakhs", "yearly_income": "₹24 Lakhs", "products_sold": ["Organic Turmeric Fingers", "Organic Turmeric Powder"], "buyers_connected": ["International buyers (UK, Germany)", "Organic lifestyle brands"], "scheme": "APEDA Export Grant", "steps": ["Got NPOP organic certification", "Contracted 50 organic farmers", "Set up polishing and vacuum packing line", "Obtained IEC export code", "First container shipped to Germany"]},
        {"business_type": "Curcumin Extraction", "investment": "₹25 Lakhs", "monthly_income": "₹4 Lakhs", "yearly_income": "₹48 Lakhs", "products_sold": ["95% Curcumin Powder", "Curcumin Capsules"], "buyers_connected": ["Pharma companies", "Nutraceutical brands"], "scheme": "NHB (National Horticulture Board)", "steps": ["Setup solvent extraction plant", "Sourced Lakadong variety (High curcumin)", "Extracted and crystallized 95% curcumin", "Tied up with 3 pharma companies", "Launched own D2C capsule brand"]},
        {"business_type": "Turmeric Latte Mix", "investment": "₹2 Lakhs", "monthly_income": "₹50,000", "yearly_income": "₹6 Lakhs", "products_sold": ["Golden Milk Mix", "Turmeric Latte Powder", "Haldi Doodh Premix"], "buyers_connected": ["Cafes", "Health stores", "Online (Amazon, Flipkart)"], "scheme": "Startup India", "steps": ["Formulated turmeric + black pepper + cinnamon blend", "Designed premium packaging", "Listed on Amazon India", "Instagram marketing", "Monthly sales crossed 2000 packets"]},
        {"business_type": "Turmeric Essential Oil", "investment": "₹8 Lakhs", "monthly_income": "₹1.5 Lakhs", "yearly_income": "₹18 Lakhs", "products_sold": ["Turmeric Essential Oil 10ml/50ml"], "buyers_connected": ["Cosmetic brands", "Aromatherapy companies", "Soap makers"], "scheme": "CIMAP Guidance", "steps": ["Setup steam distillation plant", "Processed turmeric leaves and rhizomes", "Bottled in dark glass vials", "Supplied to 10 cosmetic companies", "Started own aromatherapy brand"]},
    ],
    "Potato": [
        {"business_type": "Potato Chips Unit", "investment": "₹6 Lakhs", "monthly_income": "₹1 Lakh", "yearly_income": "₹12 Lakhs", "products_sold": ["Salted Chips", "Masala Chips", "Tomato Chips"], "buyers_connected": ["Retailers", "School canteens", "Supermarkets"], "scheme": "PMFME", "steps": ["Purchased slicer and continuous fryer", "Setup in 1200 sq ft rented space", "Got FSSAI license", "Nitrogen packaging for freshness", "Distributed to 100+ shops locally"]},
        {"business_type": "Frozen French Fries", "investment": "₹15 Lakhs", "monthly_income": "₹2 Lakhs", "yearly_income": "₹24 Lakhs", "products_sold": ["Frozen French Fries", "Frozen Potato Wedges"], "buyers_connected": ["Fast food chains", "QSR restaurants", "Hotels"], "scheme": "PMKSY Cold Chain", "steps": ["Setup IQF (blast freezer) unit", "Purchased strip cutters and blancher", "Got HACCP certification", "Contracted with 5 QSR chains", "Monthly output reached 20 tons"]},
        {"business_type": "Potato Flour Production", "investment": "₹3 Lakhs", "monthly_income": "₹65,000", "yearly_income": "₹7.8 Lakhs", "products_sold": ["Potato Flour (Gluten-Free)"], "buyers_connected": ["Gluten-free bakeries", "Health food stores", "Online platforms"], "scheme": "PMEGP", "steps": ["Setup drying and milling unit", "Targeted gluten-free market", "Designed premium packaging", "Listed on health platforms", "Monthly orders 1.5 tons"]},
        {"business_type": "Aloo Bhujia Manufacturing", "investment": "₹4 Lakhs", "monthly_income": "₹75,000", "yearly_income": "₹9 Lakhs", "products_sold": ["Aloo Bhujia", "Namkeen Mix", "Sev"], "buyers_connected": ["Sweet shops", "Wholesale namkeen dealers"], "scheme": "MUDRA Loan", "steps": ["Setup namkeen production unit", "Purchased extruder and fryer", "Hired 4 workers", "Built local customer base", "Festival orders double production"]},
        {"business_type": "Dehydrated Potato Flakes", "investment": "₹10 Lakhs", "monthly_income": "₹1.8 Lakhs", "yearly_income": "₹21.6 Lakhs", "products_sold": ["Potato Flakes", "Instant Mashed Potato"], "buyers_connected": ["Ready-to-eat brands", "Army canteens", "Export agents"], "scheme": "PMFME", "steps": ["Setup drum drying facility", "Processed cull potatoes at low cost", "Supplied to ITC and MTR", "Got Army canteen supply order", "Started export to Middle East"]},
    ],
    "Groundnut": [
        {"business_type": "Groundnut Oil Mill", "investment": "₹8 Lakhs", "monthly_income": "₹1.2 Lakhs", "yearly_income": "₹14.4 Lakhs", "products_sold": ["Cold-Pressed Groundnut Oil", "Filtered Groundnut Oil"], "buyers_connected": ["Households", "Health stores", "Hotels"], "scheme": "Agriculture Infrastructure Fund", "steps": ["Purchased cold press oil expeller", "Setup filtering and bottling unit", "Built brand as 'Farm Fresh Oil'", "Sold via direct farm-to-home delivery", "Monthly production 2000 liters"]},
        {"business_type": "Peanut Butter Production", "investment": "₹5 Lakhs", "monthly_income": "₹90,000", "yearly_income": "₹10.8 Lakhs", "products_sold": ["Creamy Peanut Butter", "Crunchy Peanut Butter", "Chocolate Peanut Butter"], "buyers_connected": ["Gyms", "Health food stores", "Amazon"], "scheme": "Startup India", "steps": ["Roasted and ground peanuts", "Setup grinding and filling line", "Designed fitness-focused branding", "Listed on Amazon and gym networks", "Monthly sales 1500 jars"]},
        {"business_type": "Chikki (Peanut Brittle) Unit", "investment": "₹1.5 Lakhs", "monthly_income": "₹45,000", "yearly_income": "₹5.4 Lakhs", "products_sold": ["Groundnut Chikki", "Sesame Chikki", "Mixed Dry Fruit Chikki"], "buyers_connected": ["Sweet shops", "Railway vendors", "Gift shops"], "scheme": "PMEGP", "steps": ["Setup small heating and cutting unit", "Used local jaggery and groundnuts", "Packed in attractive gift boxes", "Sold at railway stations and shops", "Diwali season orders tripled production"]},
        {"business_type": "Groundnut Cake (Kachori) Stall", "investment": "₹50,000", "monthly_income": "₹30,000", "yearly_income": "₹3.6 Lakhs", "products_sold": ["Groundnut Kachori", "Mirchi Bajji", "Peanut Snacks"], "buyers_connected": ["Direct consumers", "Canteens", "Tiffin services"], "scheme": "MUDRA Shishu", "steps": ["Started roadside stall near market", "Used own farm groundnuts", "Expanded to 2 stalls within 6 months", "Added tiffin delivery service", "Employed 3 workers"]},
    ],
    "Chilli": [
        {"business_type": "Red Chilli Powder Processing", "investment": "₹6 Lakhs", "monthly_income": "₹1.1 Lakhs", "yearly_income": "₹13.2 Lakhs", "products_sold": ["Kashmiri Chilli Powder", "Guntur Chilli Powder", "Byadgi Chilli Powder"], "buyers_connected": ["FMCG distributors", "Hotels", "Supermarkets"], "scheme": "Spices Board", "steps": ["Purchased heavy-duty pulverizer", "Setup 2000 sq ft processing unit", "Got Spices Board and FSSAI license", "Launched 3 varieties of chilli powder", "Monthly production 8 tons"]},
        {"business_type": "Chilli Sauce Factory", "investment": "₹4 Lakhs", "monthly_income": "₹75,000", "yearly_income": "₹9 Lakhs", "products_sold": ["Hot Sauce", "Green Chilli Sauce", "Schezwan Sauce"], "buyers_connected": ["Restaurants", "Cloud kitchens", "Retailers"], "scheme": "PMFME", "steps": ["Developed 3 sauce recipes", "Setup bottling and labeling unit", "Got FSSAI license", "Supplied to 40 restaurants", "Launched Schezwan sauce variant"]},
        {"business_type": "Dried Chilli Export", "investment": "₹12 Lakhs", "monthly_income": "₹2.5 Lakhs", "yearly_income": "₹30 Lakhs", "products_sold": ["Dried Red Chillies (S17)", "Teja Chillies", "Byadgi Chillies"], "buyers_connected": ["Export firms", "International spice traders (Bangladesh, Sri Lanka)"], "scheme": "MPEDA/APEDA", "steps": ["Built solar drying yards", "Graded and sorted chillies by variety", "Obtained IEC code", "First export to Bangladesh", "Annual export volume reached 50 tons"]},
        {"business_type": "Chilli Flakes & Oleoresin", "investment": "₹15 Lakhs", "monthly_income": "₹3 Lakhs", "yearly_income": "₹36 Lakhs", "products_sold": ["Chilli Flakes", "Chilli Oleoresin"], "buyers_connected": ["Pizza chains", "Food processing industries", "Cosmetics (capsaicin)"], "scheme": "Agriculture Infrastructure Fund", "steps": ["Setup flaking and extraction unit", "Supplied flakes to pizza chains", "Extracted oleoresin for industrial use", "Built B2B relationships", "Reached 15 ton/month capacity"]},
    ],
    "Millets": [
        {"business_type": "Millet Flour Processing", "investment": "₹3 Lakhs", "monthly_income": "₹60,000", "yearly_income": "₹7.2 Lakhs", "products_sold": ["Ragi Flour", "Jowar Flour", "Bajra Flour", "Multi-Millet Flour"], "buyers_connected": ["Health food stores", "Supermarkets", "Online platforms"], "scheme": "National Millet Mission", "steps": ["Setup small flour mill", "Focused on health-conscious market", "Created multi-millet mix", "Listed on BigBasket and Amazon", "Monthly sales 3 tons"]},
        {"business_type": "Millet Cookies Bakery", "investment": "₹4 Lakhs", "monthly_income": "₹70,000", "yearly_income": "₹8.4 Lakhs", "products_sold": ["Ragi Cookies", "Jowar Biscuits", "Millet Energy Bars"], "buyers_connected": ["Schools", "Corporate offices", "Organic stores"], "scheme": "PMFME", "steps": ["Developed gluten-free cookie recipes", "Setup small bakery oven", "Packed in eco-friendly boxes", "Supplied to 20 schools as healthy snack", "Corporate order volume grew 3x"]},
        {"business_type": "Ready-to-Cook Millet Mix", "investment": "₹2 Lakhs", "monthly_income": "₹45,000", "yearly_income": "₹5.4 Lakhs", "products_sold": ["Millet Dosa Mix", "Millet Upma Mix", "Millet Khichdi Mix"], "buyers_connected": ["Supermarkets", "Online groceries"], "scheme": "Startup India", "steps": ["Developed instant millet mixes", "Designed attractive packaging", "Got FSSAI license", "Built presence on Instagram", "Monthly sales 1000 packets"]},
        {"business_type": "Millet Health Drink", "investment": "₹5 Lakhs", "monthly_income": "₹85,000", "yearly_income": "₹10.2 Lakhs", "products_sold": ["Ragi Malt", "Multi-Millet Health Mix", "Millet Porridge Powder"], "buyers_connected": ["Baby food stores", "Pharmacies", "Online"], "scheme": "National Millet Mission", "steps": ["Formulated ragi malt with vitamins", "Setup roasting and mixing unit", "Targeted mothers and children segment", "Sold through pharmacies and online", "Got NABL lab certification"]},
    ],
    "Cotton": [
        {"business_type": "Cotton Ginning Unit", "investment": "₹20 Lakhs", "monthly_income": "₹3.5 Lakhs", "yearly_income": "₹42 Lakhs", "products_sold": ["Ginned Cotton", "Cotton Bales", "Cottonseed"], "buyers_connected": ["Textile mills", "Oil mills (cottonseed)"], "scheme": "CGTMSE", "steps": ["Setup ginning press with subsidy", "Contracted 100 cotton farmers", "Supplied lint to spinning mills", "Sold cottonseed to oil mills", "Operating at 500 bales/month"]},
        {"business_type": "Cotton Wick Making", "investment": "₹1 Lakh", "monthly_income": "₹25,000", "yearly_income": "₹3 Lakhs", "products_sold": ["Cotton Wicks (Batti)", "Lamp Wicks"], "buyers_connected": ["Temple shops", "Pooja stores", "Wholesalers"], "scheme": "KVIC", "steps": ["Purchased wick-making machine", "Used short-staple cotton waste", "Supplied to temple shops", "Festival demand doubled", "Employed 5 village women"]},
        {"business_type": "Organic Cotton Bags", "investment": "₹3 Lakhs", "monthly_income": "₹55,000", "yearly_income": "₹6.6 Lakhs", "products_sold": ["Cloth Bags", "Tote Bags", "Produce Bags"], "buyers_connected": ["Supermarkets", "Corporate gifting", "Export"], "scheme": "PMEGP", "steps": ["Setup stitching unit with 5 machines", "Used organic cotton fabric", "Got eco-friendly certification", "Supplied to supermarkets as plastic alternative", "Corporate gifting orders surged after plastic ban"]},
    ],
    "Banana": [
        {"business_type": "Banana Chips Manufacturing", "investment": "₹4 Lakhs", "monthly_income": "₹80,000", "yearly_income": "₹9.6 Lakhs", "products_sold": ["Salted Banana Chips", "Sweet Banana Chips", "Spicy Banana Chips"], "buyers_connected": ["Retailers", "Supermarkets", "Online"], "scheme": "PMFME", "steps": ["Sourced raw Nendran bananas", "Setup slicer and fryer (coconut oil)", "Nitrogen packed for crispness", "Distributed to 80+ shops in Kerala and TN", "Added sweet jaggery variant"]},
        {"business_type": "Banana Flour Processing", "investment": "₹6 Lakhs", "monthly_income": "₹95,000", "yearly_income": "₹11.4 Lakhs", "products_sold": ["Green Banana Flour", "Resistant Starch Flour"], "buyers_connected": ["Gluten-free bakeries", "Baby food brands", "Export"], "scheme": "PMEGP", "steps": ["Peeled and sliced green bananas", "Solar dried below 10% moisture", "Milled into fine powder", "Marketed as gluten-free superfood", "Exported first batch to UAE"]},
        {"business_type": "Banana Fiber Extraction", "investment": "₹2 Lakhs", "monthly_income": "₹35,000", "yearly_income": "₹4.2 Lakhs", "products_sold": ["Banana Fiber", "Handmade Paper", "Fiber Yarn"], "buyers_connected": ["Textile artisans", "Paper companies", "Handicraft NGOs"], "scheme": "KVIC", "steps": ["Collected waste banana stems post-harvest", "Ran through extractor machine", "Sun-dried and sorted fibers", "Supplied to handloom weavers", "Started making banana paper as value addition"]},
        {"business_type": "Banana Puree B2B", "investment": "₹12 Lakhs", "monthly_income": "₹1.5 Lakhs", "yearly_income": "₹18 Lakhs", "products_sold": ["Banana Puree (Aseptic)", "Baby Food Grade Puree"], "buyers_connected": ["Ice cream companies", "Baby food manufacturers", "Juice brands"], "scheme": "Agriculture Infrastructure Fund", "steps": ["Setup pulper and pasteurizer", "Packed in aseptic drums", "Supplied to 3 ice cream brands", "Got baby food grade certification", "Monthly output 25 tons"]},
    ],
    "Coconut": [
        {"business_type": "Virgin Coconut Oil Unit", "investment": "₹5 Lakhs", "monthly_income": "₹85,000", "yearly_income": "₹10.2 Lakhs", "products_sold": ["Virgin Coconut Oil", "Cold-Pressed Coconut Oil"], "buyers_connected": ["Health stores", "Cosmetic brands", "Online"], "scheme": "Coconut Development Board", "steps": ["Setup cold-press extraction unit", "Used fresh coconut milk method", "Bottled in premium glass bottles", "Sold on Amazon and health stores", "Monthly production 1000 liters"]},
        {"business_type": "Coconut Water Packaging", "investment": "₹8 Lakhs", "monthly_income": "₹1.2 Lakhs", "yearly_income": "₹14.4 Lakhs", "products_sold": ["Packaged Tender Coconut Water", "Flavored Coconut Water"], "buyers_connected": ["Gyms", "Sports events", "Supermarkets"], "scheme": "Startup India", "steps": ["Setup Tetra-Pak filling unit", "Sourced from 200 coconut farms", "Targeted fitness and sports market", "Supplied to gym chains", "Added mango and lemon flavors"]},
        {"business_type": "Coir Products Manufacturing", "investment": "₹3 Lakhs", "monthly_income": "₹50,000", "yearly_income": "₹6 Lakhs", "products_sold": ["Coir Mats", "Coir Pots", "Coir Growing Medium"], "buyers_connected": ["Nurseries", "Export agents", "Landscaping companies"], "scheme": "Coir Board Subsidy", "steps": ["Collected coconut husks from oil mills", "Setup retting and spinning unit", "Made coir pots and growing blocks", "Exported to Netherlands for horticulture", "Employed 10 local women"]},
        {"business_type": "Desiccated Coconut Production", "investment": "₹7 Lakhs", "monthly_income": "₹1 Lakh", "yearly_income": "₹12 Lakhs", "products_sold": ["Desiccated Coconut", "Coconut Milk Powder"], "buyers_connected": ["Bakeries", "Confectioneries", "Export"], "scheme": "PMFME", "steps": ["Setup drying and shredding unit", "Processed 500 coconuts daily", "Supplied to bakeries and sweet shops", "Got export quality certification", "Monthly revenue crossed ₹1 Lakh"]},
    ],
    "Mango": [
        {"business_type": "Mango Pulp Processing", "investment": "₹10 Lakhs", "monthly_income": "₹2 Lakhs", "yearly_income": "₹24 Lakhs", "products_sold": ["Mango Pulp (Alphonso)", "Totapuri Pulp", "Kesar Pulp"], "buyers_connected": ["Juice brands", "Ice cream companies", "Export"], "scheme": "NHB", "steps": ["Setup pulping and pasteurization line", "Processed during peak season (Apr-Jun)", "Stored in aseptic drums", "Supplied to 5 juice brands year-round", "Exported Alphonso pulp to Middle East"]},
        {"business_type": "Mango Pickle Business", "investment": "₹1.5 Lakhs", "monthly_income": "₹40,000", "yearly_income": "₹4.8 Lakhs", "products_sold": ["Avakaya Pickle", "Sweet Mango Pickle", "Mango Thokku"], "buyers_connected": ["Kirana stores", "NRI customers online", "Restaurants"], "scheme": "PMEGP", "steps": ["Used grandmother's traditional recipe", "Setup small processing kitchen", "Listed on Amazon for NRI market", "Festival orders from 5 states", "Became viral on social media"]},
        {"business_type": "Dried Mango (Amchur) Production", "investment": "₹2 Lakhs", "monthly_income": "₹45,000", "yearly_income": "₹5.4 Lakhs", "products_sold": ["Mango Powder (Amchur)", "Dried Mango Slices"], "buyers_connected": ["Spice companies", "Snack retailers", "Health food stores"], "scheme": "Spices Board", "steps": ["Collected raw green mangoes", "Solar dried and powdered", "Supplied amchur to spice brands", "Dried slices sold as healthy snack", "Added packaging with nutritional info"]},
        {"business_type": "Mango Juice & Nectar", "investment": "₹8 Lakhs", "monthly_income": "₹1.5 Lakhs", "yearly_income": "₹18 Lakhs", "products_sold": ["Mango Juice", "Mango Nectar", "Mango Lassi"], "buyers_connected": ["Hotels", "Caterers", "Supermarkets", "Event companies"], "scheme": "PMFME", "steps": ["Setup juice extraction and bottling line", "Used Totapuri for juice, Alphonso for nectar", "Got FSSAI license", "Supplied to hotel chains", "Launched mango lassi in summer season"]},
    ],
    "Maize": [
        {"business_type": "Corn Flakes Production", "investment": "₹12 Lakhs", "monthly_income": "₹1.8 Lakhs", "yearly_income": "₹21.6 Lakhs", "products_sold": ["Corn Flakes", "Honey Corn Flakes", "Chocos"], "buyers_connected": ["Supermarkets", "Schools", "Retailers"], "scheme": "PMFME", "steps": ["Setup extrusion and flaking line", "Developed honey and chocolate variants", "Packaged in attractive boxes", "Supplied to schools for mid-day meals", "Retail distribution in 3 states"]},
        {"business_type": "Baby Corn Processing", "investment": "₹3 Lakhs", "monthly_income": "₹55,000", "yearly_income": "₹6.6 Lakhs", "products_sold": ["Pickled Baby Corn", "Frozen Baby Corn", "Fresh Baby Corn"], "buyers_connected": ["Chinese restaurants", "Hotels", "Supermarkets"], "scheme": "State Horticulture Mission", "steps": ["Grew baby corn variety (harvested at 55 days)", "Setup grading and packaging unit", "Supplied to Chinese restaurants", "Added pickle and frozen variants", "Employed 8 farm workers"]},
        {"business_type": "Popcorn Packaging Unit", "investment": "₹2 Lakhs", "monthly_income": "₹50,000", "yearly_income": "₹6 Lakhs", "products_sold": ["Ready-to-Pop Corn Kernels", "Flavored Popcorn (Cheese, Caramel)"], "buyers_connected": ["Movie theaters", "Retailers", "Event companies"], "scheme": "MUDRA Loan", "steps": ["Sourced popcorn maize variety", "Setup flavoring and packaging unit", "Supplied to movie theaters", "Added cheese and caramel flavors", "Monthly sales 5000 packets"]},
        {"business_type": "Corn Starch Unit", "investment": "₹18 Lakhs", "monthly_income": "₹2.5 Lakhs", "yearly_income": "₹30 Lakhs", "products_sold": ["Corn Starch", "Modified Starch"], "buyers_connected": ["Paper mills", "Textile units", "Food industries"], "scheme": "CGTMSE", "steps": ["Setup wet milling and drying unit", "Processed 10 tons maize daily", "Supplied to paper and textile industries", "Added food-grade modified starch", "Became major regional supplier"]},
    ],
    "Soybean": [
        {"business_type": "Soy Milk & Tofu Unit", "investment": "₹5 Lakhs", "monthly_income": "₹80,000", "yearly_income": "₹9.6 Lakhs", "products_sold": ["Soy Milk", "Fresh Tofu", "Flavored Soy Milk"], "buyers_connected": ["Health food stores", "Restaurants", "Gyms"], "scheme": "PMFME", "steps": ["Setup soaking, grinding, and boiling unit", "Produced soy milk and tofu daily", "Supplied to 15 vegetarian restaurants", "Added chocolate and vanilla soy milk", "Built loyal customer base in 6 months"]},
        {"business_type": "Soy Nuggets (Chunks) Production", "investment": "₹8 Lakhs", "monthly_income": "₹1.2 Lakhs", "yearly_income": "₹14.4 Lakhs", "products_sold": ["Soya Chunks", "Soya Granules", "Textured Soy Protein"], "buyers_connected": ["Wholesalers", "Supermarkets", "Hostels", "Army mess"], "scheme": "Agriculture Infrastructure Fund", "steps": ["Setup twin-screw extruder", "Produced soy nuggets at 500kg/day", "Distributed to wholesale markets", "Got Army mess supply contract", "Expanded to 3 packaging sizes"]},
        {"business_type": "Soybean Oil Extraction", "investment": "₹15 Lakhs", "monthly_income": "₹2 Lakhs", "yearly_income": "₹24 Lakhs", "products_sold": ["Refined Soybean Oil", "Soy Lecithin", "Soy Meal (Cattle Feed)"], "buyers_connected": ["Oil distributors", "Cattle feed companies", "Food industries"], "scheme": "SME Loan", "steps": ["Setup solvent extraction plant", "Processed 5 tons soybeans daily", "Sold refined oil through distributors", "Sold soy meal to cattle feed companies", "Added soy lecithin as value addition"]},
    ],
    "Wheat": [
        {"business_type": "Atta (Wheat Flour) Chakki", "investment": "₹5 Lakhs", "monthly_income": "₹75,000", "yearly_income": "₹9 Lakhs", "products_sold": ["Whole Wheat Atta", "Multigrain Atta", "Besan"], "buyers_connected": ["Households", "Retailers", "Hotels"], "scheme": "PMFME", "steps": ["Setup stone chakki and packaging", "Marketed as 'farm fresh' atta", "Home delivery service in town", "Added multigrain and besan varieties", "Monthly milling 10 tons"]},
        {"business_type": "Pasta & Noodles Unit", "investment": "₹10 Lakhs", "monthly_income": "₹1.5 Lakhs", "yearly_income": "₹18 Lakhs", "products_sold": ["Wheat Pasta (Penne, Fusilli)", "Vermicelli", "Semiya"], "buyers_connected": ["Supermarkets", "Restaurants", "Schools"], "scheme": "PMFME", "steps": ["Purchased extruder and dryer", "Made pasta from durum wheat semolina", "Supplied to school mid-day meals", "Added vermicelli and semiya lines", "Monthly production 8 tons"]},
        {"business_type": "Bread & Bakery Unit", "investment": "₹7 Lakhs", "monthly_income": "₹1 Lakh", "yearly_income": "₹12 Lakhs", "products_sold": ["Whole Wheat Bread", "Multigrain Bread", "Rusk", "Buns"], "buyers_connected": ["Tea stalls", "Hotels", "Retailers", "Hospitals"], "scheme": "Stand-Up India", "steps": ["Setup bakery with deck oven", "Used own farm wheat for atta", "Supplied bread to 50+ tea stalls", "Added rusk and bun production", "Hospital canteen contract secured"]},
        {"business_type": "Wheat Grass Juice Business", "investment": "₹1 Lakh", "monthly_income": "₹35,000", "yearly_income": "₹4.2 Lakhs", "products_sold": ["Wheatgrass Juice", "Wheatgrass Powder"], "buyers_connected": ["Juice bars", "Health clinics", "Online"], "scheme": "Startup India", "steps": ["Grew wheatgrass in trays hydroponically", "Cold-pressed into juice bottles", "Supplied to juice bars and naturopathy centers", "Added wheatgrass powder for online sales", "Growing at 20% month-on-month"]},
    ],
    "Sugarcane": [
        {"business_type": "Jaggery (Gur) Production", "investment": "₹6 Lakhs", "monthly_income": "₹90,000", "yearly_income": "₹10.8 Lakhs", "products_sold": ["Organic Jaggery Blocks", "Jaggery Powder", "Liquid Jaggery"], "buyers_connected": ["Sweet shops", "Organic stores", "Export"], "scheme": "NHB", "steps": ["Setup cane crushing and boiling unit", "Produced chemical-free jaggery", "Made powder and liquid variants", "Exported organic jaggery to Europe", "Farm-to-fork brand created"]},
        {"business_type": "Sugarcane Juice Parlor Chain", "investment": "₹2 Lakhs", "monthly_income": "₹50,000", "yearly_income": "₹6 Lakhs", "products_sold": ["Fresh Sugarcane Juice", "Sugarcane + Ginger Juice", "Sugarcane + Lemon Mint"], "buyers_connected": ["Direct consumers", "Roadside customers"], "scheme": "MUDRA Kishore", "steps": ["Started with 1 roadside parlor", "Used hygienic stainless steel crusher", "Added ginger and lemon variants", "Opened 3 more outlets in town", "Employed 6 workers from village"]},
        {"business_type": "Ethanol from Sugarcane", "investment": "₹50 Lakhs", "monthly_income": "₹8 Lakhs", "yearly_income": "₹96 Lakhs", "products_sold": ["Ethanol (for blending)", "Bagasse (Biomass Fuel)"], "buyers_connected": ["OMCs (IOCL, BPCL)", "Power plants"], "scheme": "Ethanol Blending Policy", "steps": ["Setup micro-distillery with govt license", "Processed B-heavy molasses", "Sold ethanol to Indian Oil Corporation", "Sold bagasse to biomass power plant", "Government guaranteed purchase under EBP"]},
        {"business_type": "Sugarcane Vinegar Production", "investment": "₹3 Lakhs", "monthly_income": "₹45,000", "yearly_income": "₹5.4 Lakhs", "products_sold": ["Sugarcane Vinegar", "Apple Cider Style Vinegar"], "buyers_connected": ["Health food stores", "Restaurants", "Pickle makers"], "scheme": "PMFME", "steps": ["Fermented sugarcane juice naturally", "Aged for 3 months in food-grade tanks", "Bottled as premium farm vinegar", "Marketed health benefits", "Growing demand from health-conscious consumers"]},
    ],
}

STORY_TEMPLATES = [
    "{farmer} from {district}, {state} started a {btype} business using locally grown {crop}. With an initial investment of {inv}, the unit now generates {mi} per month. {farmer} credits {scheme} for providing crucial financial support. The products are sold to {buyers_str} and the business continues to grow.",
    "After years of selling raw {crop}, {farmer} from {district}, {state} decided to add value by starting {btype}. The total setup cost was {inv} and within 8 months, monthly income reached {mi}. The {scheme} scheme helped with working capital. Today, {farmer} employs 5 people from the village.",
    "{farmer} of {district}, {state} transformed surplus {crop} into a profitable venture through {btype}. Initially investing {inv}, the business now earns {mi} monthly. Products reach {buyers_str}. {farmer} says, 'Processing our own crops has doubled our farm income.'",
    "Inspired by government push for food processing, {farmer} from {district}, {state} started {btype} with {inv} investment. Monthly earnings have reached {mi}. The {scheme} provided 35% subsidy on machinery. {farmer} now plans to expand capacity next year.",
    "What started as a small experiment by {farmer} in {district}, {state} has grown into a thriving {btype} business. From {crop} grown on the family farm, {farmer} invests {inv} and now earns {mi} per month. Products are supplied to {buyers_str} across the state.",
]

def generate_phone():
    prefixes = ["98", "97", "96", "95", "94", "93", "91", "90", "88", "87", "86", "85"]
    return f"+91 {random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generate_email(name):
    clean = name.lower().replace(" ", ".").replace("'", "")
    domain = random.choice(["gmail.com", "yahoo.com", "rediffmail.com"])
    return f"{clean}@{domain}"

def run_seed():
    db = SessionLocal()
    try:
        existing = db.query(SuccessStory).count()
        if existing >= 50:
            print(f"Success stories already has {existing} records, skipping seed.")
            return
        
        # Clear old data
        db.query(SuccessStory).delete()
        db.commit()
        
        print("Generating 100+ success stories...")
        stories = []
        states = list(FARMER_NAMES.keys())
        
        for crop, businesses in CROP_BUSINESSES.items():
            for biz in businesses:
                # Pick a random state and farmer
                state = random.choice(states)
                farmer = random.choice(FARMER_NAMES[state])
                district = random.choice(DISTRICTS[state])
                
                buyers_str = ", ".join(biz["buyers_connected"][:2])
                story_text = random.choice(STORY_TEMPLATES).format(
                    farmer=farmer, district=district, state=state,
                    btype=biz["business_type"], crop=crop.lower(),
                    inv=biz["investment"], mi=biz["monthly_income"],
                    scheme=biz["scheme"], buyers_str=buyers_str
                )
                
                story = SuccessStory(
                    farmer_name=farmer,
                    state=state,
                    district=district,
                    crop=crop,
                    business_type=biz["business_type"],
                    investment=biz["investment"],
                    monthly_income=biz["monthly_income"],
                    yearly_income=biz["yearly_income"],
                    products_sold=json.dumps(biz["products_sold"]),
                    buyers_connected=json.dumps(biz["buyers_connected"]),
                    government_scheme_used=biz["scheme"],
                    implementation_steps=json.dumps(biz["steps"]),
                    story=story_text,
                    contact_phone=generate_phone(),
                    contact_email=generate_email(farmer),
                )
                stories.append(story)
        
        db.add_all(stories)
        db.commit()
        print(f"Successfully seeded {len(stories)} success stories across {len(CROP_BUSINESSES)} crops.")
        
    except Exception as e:
        print(f"Error seeding success stories: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
