"""
Programmatic generator for 500+ agri ventures across crops, dairy, spices, oilseeds, etc.
"""
import json, random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.venture_model import AgriVentureDataset

CROPS = {
    "Rice": {"soil": "Alluvial,Loamy,Clay", "water": "High", "season": "Kharif,Rabi", "img": "rice+processing"},
    "Wheat": {"soil": "Alluvial,Loamy,Black Soil", "water": "Medium", "season": "Rabi", "img": "wheat+flour"},
    "Maize": {"soil": "Alluvial,Loamy,Sandy", "water": "Medium", "season": "Kharif,Rabi", "img": "corn+processing"},
    "Millets": {"soil": "Red Soil,Sandy,Loamy", "water": "Low", "season": "Kharif", "img": "millet+grain"},
    "Jowar": {"soil": "Black Soil,Red Soil", "water": "Low", "season": "Kharif,Rabi", "img": "sorghum+grain"},
    "Bajra": {"soil": "Sandy,Loamy", "water": "Low", "season": "Kharif", "img": "pearl+millet"},
    "Ragi": {"soil": "Red Soil,Loamy", "water": "Low", "season": "Kharif", "img": "finger+millet"},
    "Tomato": {"soil": "Loamy,Red Soil,Black Soil", "water": "Medium", "season": "Kharif,Rabi,Summer", "img": "tomato+processing"},
    "Potato": {"soil": "Alluvial,Loamy,Sandy", "water": "Medium", "season": "Rabi", "img": "potato+chips"},
    "Onion": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Kharif,Rabi", "img": "onion+dehydration"},
    "Chilli": {"soil": "Black Soil,Loamy,Red Soil", "water": "Medium", "season": "Kharif,Rabi", "img": "chilli+powder"},
    "Turmeric": {"soil": "Loamy,Alluvial,Clay", "water": "Medium", "season": "Kharif", "img": "turmeric+powder"},
    "Ginger": {"soil": "Loamy,Sandy", "water": "Medium", "season": "Kharif", "img": "ginger+processing"},
    "Garlic": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Rabi", "img": "garlic+processing"},
    "Coriander": {"soil": "Loamy,Black Soil", "water": "Low", "season": "Rabi", "img": "coriander+spice"},
    "Cumin": {"soil": "Sandy,Loamy", "water": "Low", "season": "Rabi", "img": "cumin+spice"},
    "Black Pepper": {"soil": "Loamy,Red Soil", "water": "High", "season": "Kharif", "img": "pepper+spice"},
    "Cardamom": {"soil": "Loamy,Red Soil", "water": "High", "season": "Kharif", "img": "cardamom+spice"},
    "Mustard": {"soil": "Loamy,Alluvial,Sandy", "water": "Low", "season": "Rabi", "img": "mustard+oil"},
    "Groundnut": {"soil": "Sandy,Loamy,Red Soil", "water": "Medium", "season": "Kharif", "img": "groundnut+oil"},
    "Soybean": {"soil": "Black Soil,Loamy", "water": "Medium", "season": "Kharif", "img": "soybean+processing"},
    "Sunflower": {"soil": "Loamy,Black Soil", "water": "Medium", "season": "Kharif,Rabi", "img": "sunflower+oil"},
    "Sesame": {"soil": "Sandy,Loamy", "water": "Low", "season": "Kharif", "img": "sesame+oil"},
    "Castor": {"soil": "Sandy,Loamy", "water": "Low", "season": "Kharif", "img": "castor+oil"},
    "Coconut": {"soil": "Sandy,Loamy,Red Soil", "water": "High", "season": "Kharif,Rabi,Summer", "img": "coconut+oil"},
    "Banana": {"soil": "Alluvial,Loamy,Clay", "water": "High", "season": "Kharif,Rabi,Summer", "img": "banana+chips"},
    "Mango": {"soil": "Alluvial,Loamy", "water": "Medium", "season": "Summer", "img": "mango+processing"},
    "Guava": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Kharif,Rabi", "img": "guava+jam"},
    "Papaya": {"soil": "Loamy,Sandy", "water": "Medium", "season": "Kharif,Rabi,Summer", "img": "papaya+processing"},
    "Grapes": {"soil": "Loamy,Sandy", "water": "Medium", "season": "Rabi", "img": "grape+wine"},
    "Orange": {"soil": "Loamy,Red Soil", "water": "Medium", "season": "Rabi", "img": "orange+juice"},
    "Lemon": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Kharif,Rabi,Summer", "img": "lemon+juice"},
    "Pomegranate": {"soil": "Loamy,Black Soil", "water": "Low", "season": "Rabi", "img": "pomegranate+juice"},
    "Apple": {"soil": "Loamy", "water": "Medium", "season": "Rabi", "img": "apple+processing"},
    "Sugarcane": {"soil": "Alluvial,Loamy,Black Soil", "water": "High", "season": "Kharif", "img": "sugarcane+jaggery"},
    "Cotton": {"soil": "Black Soil,Alluvial", "water": "Medium", "season": "Kharif", "img": "cotton+ginning"},
    "Jute": {"soil": "Alluvial,Clay", "water": "High", "season": "Kharif", "img": "jute+product"},
    "Tea": {"soil": "Loamy,Red Soil", "water": "High", "season": "Kharif,Rabi", "img": "tea+processing"},
    "Coffee": {"soil": "Red Soil,Loamy", "water": "High", "season": "Kharif", "img": "coffee+roasting"},
    "Rubber": {"soil": "Loamy,Red Soil", "water": "High", "season": "Kharif", "img": "rubber+sheet"},
    "Milk": {"soil": "Alluvial,Loamy,Black Soil,Red Soil,Sandy,Clay", "water": "Medium", "season": "Kharif,Rabi,Summer", "img": "milk+dairy"},
    "Honey": {"soil": "Alluvial,Loamy,Black Soil,Red Soil,Sandy,Clay", "water": "Low", "season": "Kharif,Rabi,Summer", "img": "honey+bee"},
    "Mushroom": {"soil": "Alluvial,Loamy,Black Soil,Red Soil,Sandy,Clay", "water": "Medium", "season": "Kharif,Rabi,Summer", "img": "mushroom+farm"},
    "Aloe Vera": {"soil": "Sandy,Loamy", "water": "Low", "season": "Kharif,Rabi,Summer", "img": "aloe+vera"},
    "Moringa": {"soil": "Loamy,Sandy,Red Soil", "water": "Low", "season": "Kharif,Rabi", "img": "moringa+powder"},
    "Neem": {"soil": "Sandy,Loamy,Red Soil", "water": "Low", "season": "Kharif,Rabi,Summer", "img": "neem+product"},
    "Amla": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Rabi", "img": "amla+processing"},
    "Tamarind": {"soil": "Red Soil,Loamy,Black Soil", "water": "Low", "season": "Kharif", "img": "tamarind+paste"},
    "Cashew": {"soil": "Sandy,Loamy,Red Soil", "water": "Low", "season": "Summer", "img": "cashew+processing"},
    "Arecanut": {"soil": "Red Soil,Loamy", "water": "High", "season": "Kharif", "img": "arecanut+processing"},
    "Peas": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Rabi", "img": "peas+frozen"},
    "Cabbage": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Rabi", "img": "cabbage+processing"},
    "Cauliflower": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Rabi", "img": "cauliflower+processing"},
    "Carrot": {"soil": "Loamy,Sandy", "water": "Medium", "season": "Rabi", "img": "carrot+juice"},
    "Beetroot": {"soil": "Loamy,Sandy", "water": "Medium", "season": "Rabi", "img": "beetroot+powder"},
    "Spinach": {"soil": "Loamy,Clay", "water": "Medium", "season": "Rabi", "img": "spinach+powder"},
    "Brinjal": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Kharif,Rabi", "img": "brinjal+pickle"},
    "Okra": {"soil": "Loamy,Black Soil", "water": "Medium", "season": "Kharif,Summer", "img": "okra+dehydrated"},
    "Drumstick": {"soil": "Loamy,Sandy,Red Soil", "water": "Low", "season": "Kharif,Rabi,Summer", "img": "moringa+drumstick"},
    "Watermelon": {"soil": "Sandy,Loamy", "water": "Medium", "season": "Summer", "img": "watermelon+juice"},
    "Pineapple": {"soil": "Loamy,Sandy,Red Soil", "water": "Medium", "season": "Kharif", "img": "pineapple+juice"},
    "Jackfruit": {"soil": "Loamy,Alluvial", "water": "Medium", "season": "Summer", "img": "jackfruit+chips"},
    "Litchi": {"soil": "Alluvial,Loamy", "water": "High", "season": "Summer", "img": "litchi+juice"},
    "Strawberry": {"soil": "Loamy,Sandy", "water": "Medium", "season": "Rabi", "img": "strawberry+jam"},
    "Fig": {"soil": "Loamy,Black Soil", "water": "Low", "season": "Kharif", "img": "fig+dried"},
    "Toor Dal": {"soil": "Black Soil,Red Soil,Loamy", "water": "Low", "season": "Kharif", "img": "toor+dal"},
    "Chana Dal": {"soil": "Loamy,Black Soil", "water": "Low", "season": "Rabi", "img": "chana+dal"},
    "Moong Dal": {"soil": "Loamy,Sandy", "water": "Low", "season": "Kharif,Summer", "img": "moong+dal"},
    "Urad Dal": {"soil": "Loamy,Black Soil", "water": "Low", "season": "Kharif", "img": "urad+dal"},
    "Masoor Dal": {"soil": "Loamy,Alluvial", "water": "Low", "season": "Rabi", "img": "masoor+dal"},
    "Silk": {"soil": "Loamy,Red Soil", "water": "Medium", "season": "Kharif,Rabi", "img": "silk+production"},
    "Wool": {"soil": "Sandy,Loamy", "water": "Low", "season": "Rabi", "img": "wool+processing"},
    "Fish": {"soil": "Alluvial,Clay", "water": "High", "season": "Kharif,Rabi,Summer", "img": "fish+farming"},
    "Poultry": {"soil": "Alluvial,Loamy,Black Soil,Red Soil,Sandy,Clay", "water": "Medium", "season": "Kharif,Rabi,Summer", "img": "poultry+farm"},
    "Goat": {"soil": "Alluvial,Loamy,Black Soil,Red Soil,Sandy,Clay", "water": "Low", "season": "Kharif,Rabi,Summer", "img": "goat+farming"},
    "Vermicompost": {"soil": "Alluvial,Loamy,Black Soil,Red Soil,Sandy,Clay", "water": "Low", "season": "Kharif,Rabi,Summer", "img": "vermicompost"},
    "Flowers": {"soil": "Loamy,Red Soil,Sandy", "water": "Medium", "season": "Kharif,Rabi", "img": "flower+farming"},
}

# Business templates per crop category
VENTURE_TEMPLATES = {
    "Rice": [
        {"name": "Puffed Rice Manufacturing", "cat": "Crop Processing", "inv": "₹1.5-3 Lakhs", "lo": 1.5, "hi": 3, "roi": "30-40%", "mi": "₹45,000-₹65,000", "pm": "35-45%", "demand": "Very High",
         "raw": {"Rice": "500 kg/day", "Salt": "5 kg/day", "Packaging": "200 bags/day"}, "machines": ["Puffing Machine", "Grading Sieve", "Packaging Machine", "Weighing Scale"], "prod": {"Daily": "400 kg puffed rice", "Monthly": "12 tons"}, "buyers": {"type": ["Wholesale distributors", "Kirana stores", "Supermarkets"], "cities": ["Local markets", "District towns"]}, "breakdown": {"Puffing Machine": "₹60,000", "Packaging Unit": "₹25,000", "Working Capital": "₹40,000", "Rent + Setup": "₹25,000"}, "steps": ["Register MSME and FSSAI", "Apply for PMFME subsidy", "Purchase puffing machine", "Source rice from local mandis", "Connect with wholesale distributors", "Start production and packaging"]},
        {"name": "Rice Flour Milling", "cat": "Crop Processing", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "25-35%", "mi": "₹60,000-₹85,000", "pm": "30-40%", "demand": "High",
         "raw": {"Rice": "1 ton/day", "Packaging Materials": "500 bags/day"}, "machines": ["Pulverizer", "Sifter", "Packaging Machine", "Weighing Scale", "Sealing Machine"], "prod": {"Daily": "800 kg rice flour", "Monthly": "24 tons"}, "buyers": {"type": ["Bakeries", "Hotels", "Supermarkets", "Export agents"], "cities": ["Metro cities", "District towns"]}, "breakdown": {"Pulverizer": "₹1,20,000", "Sifter": "₹40,000", "Packaging": "₹30,000", "Working Capital": "₹60,000", "Setup": "₹50,000"}, "steps": ["Get FSSAI license", "Setup flour mill in 1000 sq ft", "Purchase pulverizer and sifter", "Source paddy/rice from farmers", "Start milling and distribution", "Build bakery client network"]},
        {"name": "Rice Bran Oil Extraction", "cat": "Oil Extraction", "inv": "₹10-20 Lakhs", "lo": 10, "hi": 20, "roi": "20-30%", "mi": "₹1.5L-₹2.5L", "pm": "25-35%", "demand": "High",
         "raw": {"Rice Bran": "2 tons/day", "Hexane Solvent": "50 liters/day"}, "machines": ["Solvent Extraction Plant", "Refining Unit", "Bottling Line", "Storage Tanks"], "prod": {"Daily": "400 liters oil", "Monthly": "12,000 liters"}, "buyers": {"type": ["Oil distributors", "Hotels", "Health food stores"], "cities": ["Metro cities", "Export"]}, "breakdown": {"Extraction Plant": "₹8,00,000", "Refining Unit": "₹3,00,000", "Bottling": "₹1,00,000", "Working Capital": "₹3,00,000"}, "steps": ["Obtain manufacturing license", "Setup solvent extraction plant", "Source rice bran from mills", "Refine and bottle oil", "Build distribution network", "Apply for Agri Infrastructure Fund"]},
        {"name": "Idli/Dosa Batter Production", "cat": "Crop Processing", "inv": "₹1-3 Lakhs", "lo": 1, "hi": 3, "roi": "35-50%", "mi": "₹40,000-₹70,000", "pm": "40-50%", "demand": "Very High",
         "raw": {"Rice": "200 kg/day", "Urad Dal": "80 kg/day", "Salt": "5 kg/day"}, "machines": ["Wet Grinder (Commercial)", "Packaging Machine", "Refrigerator", "Delivery Vehicle"], "prod": {"Daily": "500 kg batter", "Monthly": "15 tons"}, "buyers": {"type": ["Hotels", "Tiffin centers", "Households", "Supermarkets"], "cities": ["City areas", "Residential colonies"]}, "breakdown": {"Wet Grinder": "₹45,000", "Packaging": "₹20,000", "Refrigerator": "₹30,000", "Working Capital": "₹50,000"}, "steps": ["Get FSSAI license", "Setup grinding unit", "Develop consistent recipe", "Start door-to-door delivery", "Partner with supermarkets", "Scale through fleet delivery"]},
        {"name": "Rice Snacks (Murukku/Chakli)", "cat": "Crop Processing", "inv": "₹1-3 Lakhs", "lo": 1, "hi": 3, "roi": "40-55%", "mi": "₹50,000-₹75,000", "pm": "40-50%", "demand": "High",
         "raw": {"Rice Flour": "100 kg/day", "Oil": "30 liters/day", "Spices": "5 kg/day"}, "machines": ["Murukku Extruder", "Deep Fryer", "Packaging Machine", "Sealing Machine"], "prod": {"Daily": "200 kg snacks", "Monthly": "6 tons"}, "buyers": {"type": ["Sweet shops", "Supermarkets", "Hotels", "Online stores"], "cities": ["Local", "State-wide"]}, "breakdown": {"Extruder": "₹35,000", "Fryer": "₹25,000", "Packaging": "₹20,000", "Working Capital": "₹40,000"}, "steps": ["Standardize recipes", "Get FSSAI license", "Purchase extruder and fryer", "Start small-batch production", "Build brand and packaging", "Expand to online sales"]},
    ],
    "Milk": [
        {"name": "Paneer Manufacturing Unit", "cat": "Dairy", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "30-40%", "mi": "₹70,000-₹1L", "pm": "35-45%", "demand": "Very High",
         "raw": {"Milk": "500 liters/day", "Citric Acid": "2 kg/day"}, "machines": ["Boiling Tank", "Paneer Press Machine", "Chilling Tank", "Packaging Unit"], "prod": {"Daily": "50 kg paneer", "Monthly": "1.5 tons"}, "buyers": {"type": ["Restaurants", "Hotels", "Supermarkets", "Sweet shops"], "cities": ["Local city", "Metro areas"]}, "breakdown": {"Boiling Tank": "₹40,000", "Press Machine": "₹50,000", "Chilling Tank": "₹80,000", "Packaging": "₹30,000", "Working Capital": "₹1,00,000"}, "steps": ["Register MSME", "Apply for PMFME subsidy", "Purchase boiling and pressing equipment", "Source milk from local dairy farmers", "Setup cold chain for distribution", "Connect with restaurants and retailers"]},
        {"name": "Ghee Production Unit", "cat": "Dairy", "inv": "₹1-3 Lakhs", "lo": 1, "hi": 3, "roi": "35-50%", "mi": "₹55,000-₹80,000", "pm": "40-50%", "demand": "Very High",
         "raw": {"Milk/Cream": "200 liters/day", "Packaging": "50 containers/day"}, "machines": ["Cream Separator", "Ghee Kettle", "Filling Machine", "Weighing Scale"], "prod": {"Daily": "20 kg ghee", "Monthly": "600 kg"}, "buyers": {"type": ["Households", "Sweet shops", "Restaurants", "Online"], "cities": ["Local", "Pan-India online"]}, "breakdown": {"Cream Separator": "₹25,000", "Ghee Kettle": "₹35,000", "Filling Machine": "₹20,000", "Working Capital": "₹50,000"}, "steps": ["Source cream from dairy farmers", "Setup ghee-making unit", "Get FSSAI license", "Build premium branding", "Sell online via Amazon/Flipkart", "Expand to corporate gifting"]},
        {"name": "Curd/Yogurt Processing", "cat": "Dairy", "inv": "₹1-3 Lakhs", "lo": 1, "hi": 3, "roi": "30-40%", "mi": "₹45,000-₹65,000", "pm": "35-45%", "demand": "High",
         "raw": {"Milk": "300 liters/day", "Culture": "100 gm/day"}, "machines": ["Pasteurizer", "Incubation Chamber", "Cup Filling Machine", "Cold Storage"], "prod": {"Daily": "300 kg curd", "Monthly": "9 tons"}, "buyers": {"type": ["Households", "Hotels", "Tiffin services", "Supermarkets"], "cities": ["Local city", "Nearby towns"]}, "breakdown": {"Pasteurizer": "₹45,000", "Incubation": "₹25,000", "Filling": "₹20,000", "Cold Storage": "₹40,000"}, "steps": ["Get FSSAI license", "Setup pasteurization unit", "Source quality milk", "Start local delivery", "Partner with supermarkets", "Add flavored yogurt variants"]},
        {"name": "Flavored Milk Production", "cat": "Dairy", "inv": "₹5-10 Lakhs", "lo": 5, "hi": 10, "roi": "25-35%", "mi": "₹1L-₹1.5L", "pm": "30-40%", "demand": "High",
         "raw": {"Milk": "1000 liters/day", "Flavoring": "10 kg/day", "Sugar": "50 kg/day"}, "machines": ["Homogenizer", "Pasteurizer", "Tetra-Pak Filler", "Cold Storage"], "prod": {"Daily": "1000 liters flavored milk", "Monthly": "30,000 liters"}, "buyers": {"type": ["Schools", "Gyms", "Supermarkets", "Vending machines"], "cities": ["Metro cities", "Tier-2 cities"]}, "breakdown": {"Homogenizer": "₹2,00,000", "Pasteurizer": "₹1,50,000", "Filler": "₹1,00,000", "Working Capital": "₹2,00,000"}, "steps": ["Develop chocolate, strawberry, mango flavors", "Get FSSAI and dairy license", "Setup UHT processing", "Partner with schools and gyms", "Launch in Tetra-Pak format", "Scale distribution state-wide"]},
        {"name": "Cheese Making Unit", "cat": "Dairy", "inv": "₹5-10 Lakhs", "lo": 5, "hi": 10, "roi": "25-35%", "mi": "₹1L-₹1.8L", "pm": "30-40%", "demand": "High",
         "raw": {"Milk": "500 liters/day", "Rennet": "Small qty", "Culture": "Small qty"}, "machines": ["Cheese Vat", "Press", "Aging Chamber", "Packaging"], "prod": {"Daily": "40 kg cheese", "Monthly": "1.2 tons"}, "buyers": {"type": ["Pizza chains", "Hotels", "Bakeries", "Retailers"], "cities": ["Metro cities"]}, "breakdown": {"Cheese Vat": "₹1,50,000", "Press": "₹60,000", "Aging Chamber": "₹1,00,000", "Working Capital": "₹2,00,000"}, "steps": ["Learn cheese-making techniques", "Setup cheese production room", "Source quality milk", "Develop mozzarella and cheddar", "Connect with pizza chains", "Build cold chain logistics"]},
    ],
    "Turmeric": [
        {"name": "Turmeric Powder Processing", "cat": "Spice Processing", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "30-40%", "mi": "₹70,000-₹1L", "pm": "35-45%", "demand": "Very High",
         "raw": {"Dried Turmeric": "500 kg/day"}, "machines": ["Pulverizer", "Sifter", "Packaging Machine", "Polishing Drum"], "prod": {"Daily": "400 kg powder", "Monthly": "12 tons"}, "buyers": {"type": ["FMCG distributors", "Supermarkets", "Kirana stores"], "cities": ["Pan-India"]}, "breakdown": {"Pulverizer": "₹1,20,000", "Sifter": "₹40,000", "Packaging": "₹40,000", "Working Capital": "₹1,00,000"}, "steps": ["Get FSSAI and Spices Board certification", "Setup processing unit", "Source dried turmeric from farmers", "Grind, sift and pack", "Build distribution network", "Register brand trademark"]},
        {"name": "Curcumin Extraction Unit", "cat": "Spice Processing", "inv": "₹10-20 Lakhs", "lo": 10, "hi": 20, "roi": "25-40%", "mi": "₹2L-₹4L", "pm": "35-50%", "demand": "Very High",
         "raw": {"Turmeric Rhizomes": "1 ton/day", "Solvents": "100 liters/day"}, "machines": ["Solvent Extraction Unit", "Evaporator", "Crystallizer", "Lab Equipment"], "prod": {"Daily": "5 kg curcumin (95%)", "Monthly": "150 kg"}, "buyers": {"type": ["Pharma companies", "Nutraceutical brands", "Export"], "cities": ["Pan-India", "International"]}, "breakdown": {"Extraction Unit": "₹6,00,000", "Evaporator": "₹2,00,000", "Lab": "₹1,00,000", "Working Capital": "₹5,00,000"}, "steps": ["Source Lakadong variety turmeric", "Setup extraction plant", "Extract and crystallize curcumin", "Get pharma grade certification", "Connect with pharma companies", "Start D2C supplement brand"]},
        {"name": "Turmeric Essential Oil", "cat": "Spice Processing", "inv": "₹5-10 Lakhs", "lo": 5, "hi": 10, "roi": "30-45%", "mi": "₹1.2L-₹2L", "pm": "40-55%", "demand": "High",
         "raw": {"Fresh Turmeric": "500 kg/day", "Water": "1000 liters/day"}, "machines": ["Steam Distillation Unit", "Condenser", "Separator", "Bottling Line"], "prod": {"Daily": "2 liters oil", "Monthly": "60 liters"}, "buyers": {"type": ["Cosmetic brands", "Aromatherapy companies", "Soap makers"], "cities": ["Metro cities", "Export"]}, "breakdown": {"Distillation Unit": "₹3,00,000", "Bottling": "₹50,000", "Working Capital": "₹2,00,000"}, "steps": ["Setup steam distillation plant", "Source fresh turmeric", "Distill and separate oil", "Bottle in dark glass vials", "Connect with cosmetic companies", "Launch own aromatherapy brand"]},
        {"name": "Organic Turmeric Export", "cat": "Organic Farming", "inv": "₹5-10 Lakhs", "lo": 5, "hi": 10, "roi": "25-40%", "mi": "₹1.5L-₹2.5L", "pm": "30-45%", "demand": "Very High",
         "raw": {"Organic Turmeric": "From contracted farmers"}, "machines": ["Polishing Drum", "Vacuum Packer", "Weighing Scale"], "prod": {"Monthly": "5-10 tons (seasonal)"}, "buyers": {"type": ["International buyers (UK, Germany, US)", "Organic brands"], "cities": ["Export markets"]}, "breakdown": {"Certification": "₹1,00,000", "Polishing": "₹80,000", "Packing": "₹50,000", "Working Capital": "₹3,00,000"}, "steps": ["Get NPOP organic certification", "Contract 50+ organic farmers", "Setup polishing and vacuum-packing", "Register on APEDA", "Get IEC export code", "Ship first container"]},
        {"name": "Turmeric Latte Mix", "cat": "Crop Processing", "inv": "₹1-3 Lakhs", "lo": 1, "hi": 3, "roi": "40-60%", "mi": "₹50,000-₹80,000", "pm": "45-60%", "demand": "High",
         "raw": {"Turmeric Powder": "50 kg/day", "Black Pepper": "5 kg/day", "Cinnamon": "3 kg/day"}, "machines": ["Blender", "Packaging Machine", "Sealing Machine"], "prod": {"Daily": "500 packets", "Monthly": "15,000 packets"}, "buyers": {"type": ["Cafes", "Health stores", "Online (Amazon)"], "cities": ["Metro cities", "Pan-India online"]}, "breakdown": {"Blender": "₹30,000", "Packaging": "₹25,000", "Working Capital": "₹50,000"}, "steps": ["Formulate turmeric+pepper+cinnamon blend", "Design premium packaging", "Get FSSAI license", "List on Amazon India", "Instagram and influencer marketing", "Scale to 5000 packets/month"]},
    ],
}

# Generic templates for crops not in VENTURE_TEMPLATES
GENERIC_TEMPLATES = [
    {"suffix": "Powder Processing", "cat": "Crop Processing", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "25-35%", "mi": "₹60,000-₹85,000", "pm": "30-40%", "demand": "High", "machines": ["Pulverizer", "Sifter", "Packaging Machine", "Sealing Machine"], "steps": ["Get FSSAI license", "Setup processing unit", "Purchase machinery", "Source raw material", "Start production", "Build distribution network"]},
    {"suffix": "Pickle Manufacturing", "cat": "Crop Processing", "inv": "₹1-3 Lakhs", "lo": 1, "hi": 3, "roi": "35-50%", "mi": "₹40,000-₹65,000", "pm": "40-55%", "demand": "High", "machines": ["Mixing Tank", "Cutting Machine", "Jar Filling Machine", "Sealing Machine"], "steps": ["Develop traditional recipe", "Get FSSAI license", "Setup small kitchen", "Package in glass jars", "Sell at local markets", "List on Amazon"]},
    {"suffix": "Juice Production", "cat": "Fruit Processing", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "25-40%", "mi": "₹65,000-₹1L", "pm": "30-45%", "demand": "High", "machines": ["Juice Extractor", "Pasteurizer", "Bottle Filler", "Capping Machine"], "steps": ["Get FSSAI license", "Setup juice extraction line", "Source fresh produce", "Pasteurize and bottle", "Supply to retailers", "Add flavored variants"]},
    {"suffix": "Dehydration Unit", "cat": "Crop Processing", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "25-35%", "mi": "₹55,000-₹80,000", "pm": "30-40%", "demand": "Medium", "machines": ["Solar/Tray Dryer", "Cutting Machine", "Packaging Unit", "Weighing Scale"], "steps": ["Build solar dryers", "Source fresh produce", "Slice and dry", "Package in food-grade pouches", "Sell to food companies", "Explore export markets"]},
    {"suffix": "Organic Farming & Export", "cat": "Organic Farming", "inv": "₹5-10 Lakhs", "lo": 5, "hi": 10, "roi": "20-35%", "mi": "₹1L-₹1.8L", "pm": "25-40%", "demand": "Very High", "machines": ["Sorting Machine", "Vacuum Packer", "Weighing Scale"], "steps": ["Get organic certification", "Adopt organic practices", "Contract farmers", "Setup packaging unit", "Register on APEDA", "Find international buyers"]},
    {"suffix": "Chips/Snack Production", "cat": "Agro-based Manufacturing", "inv": "₹3-5 Lakhs", "lo": 3, "hi": 5, "roi": "30-45%", "mi": "₹60,000-₹90,000", "pm": "35-50%", "demand": "High", "machines": ["Slicer", "Fryer", "Seasoning Drum", "Packaging Machine"], "steps": ["Get FSSAI license", "Setup frying unit", "Develop flavoring recipes", "Nitrogen-pack for freshness", "Distribute to retailers", "Build regional brand"]},
    {"suffix": "Oil Extraction Unit", "cat": "Oil Extraction", "inv": "₹5-10 Lakhs", "lo": 5, "hi": 10, "roi": "25-35%", "mi": "₹80,000-₹1.5L", "pm": "30-40%", "demand": "High", "machines": ["Cold Press Expeller", "Filter Press", "Bottling Line", "Storage Tanks"], "steps": ["Purchase cold press machine", "Setup filtration system", "Source seeds/nuts from farmers", "Extract and filter oil", "Brand as cold-pressed/organic", "Sell online and locally"]},
]

def make_image_url(keyword):
    return f"https://images.unsplash.com/photo-placeholder?w=600&q=80&fit=crop&auto=format&search={keyword}"

def gen_raw(crop, template):
    return template.get("raw", {crop: "As required", "Packaging": "As needed"})

def gen_prod(template):
    return template.get("prod", {"Daily": "Variable", "Monthly": "Variable"})

def gen_buyers(template):
    return template.get("buyers", {"type": ["Local traders", "Wholesalers", "Retailers"], "cities": ["Local markets"]})

def gen_breakdown(template):
    return template.get("breakdown", {"Machinery": "50%", "Working Capital": "30%", "Setup": "20%"})

def run_seed():
    db = SessionLocal()
    try:
        existing = db.query(AgriVentureDataset).count()
        if existing >= 100:
            print(f"Agri ventures already has {existing} records, skipping.")
            return

        db.query(AgriVentureDataset).delete()
        db.commit()

        ventures = []

        # 1) Add specific templates
        for crop, templates in VENTURE_TEMPLATES.items():
            crop_info = CROPS.get(crop, {"soil": "Loamy", "water": "Medium", "season": "Kharif,Rabi", "img": crop.lower()})
            for t in templates:
                v = AgriVentureDataset(
                    crop_name=crop,
                    venture_name=t["name"],
                    business_category=t["cat"],
                    soil_suitability=crop_info["soil"],
                    water_requirement=crop_info["water"],
                    season_suitability=crop_info["season"],
                    investment_range=t["inv"],
                    investment_min=t["lo"],
                    investment_max=t["hi"],
                    roi_range=t["roi"],
                    monthly_income=t["mi"],
                    profit_margin=t["pm"],
                    demand_level=t["demand"],
                    raw_material_required=json.dumps(gen_raw(crop, t)),
                    machinery_required=json.dumps(t["machines"]),
                    production_capacity=json.dumps(gen_prod(t)),
                    market_demand=json.dumps(gen_buyers(t)),
                    investment_breakdown=json.dumps(gen_breakdown(t)),
                    implementation_steps=json.dumps(t["steps"]),
                    image_url=make_image_url(crop_info["img"]),
                )
                ventures.append(v)

        # 2) Generate generic ventures for ALL crops
        for crop, info in CROPS.items():
            if crop in VENTURE_TEMPLATES:
                # Add only generic templates not already covered
                existing_names = [t["name"] for t in VENTURE_TEMPLATES[crop]]
                for gt in GENERIC_TEMPLATES:
                    name = f"{crop} {gt['suffix']}"
                    if name not in existing_names:
                        v = AgriVentureDataset(
                            crop_name=crop,
                            venture_name=name,
                            business_category=gt["cat"],
                            soil_suitability=info["soil"],
                            water_requirement=info["water"],
                            season_suitability=info["season"],
                            investment_range=gt["inv"],
                            investment_min=gt["lo"],
                            investment_max=gt["hi"],
                            roi_range=gt["roi"],
                            monthly_income=gt["mi"],
                            profit_margin=gt["pm"],
                            demand_level=gt["demand"],
                            raw_material_required=json.dumps({crop: "As per capacity", "Packaging": "As needed"}),
                            machinery_required=json.dumps(gt["machines"]),
                            production_capacity=json.dumps({"Daily": "Variable", "Monthly": "Variable"}),
                            market_demand=json.dumps({"type": ["Local traders", "Wholesalers", "Retailers", "Online"], "cities": ["Local", "State-wide"]}),
                            investment_breakdown=json.dumps({"Machinery": "40-50%", "Working Capital": "30%", "Setup & License": "20%"}),
                            implementation_steps=json.dumps(gt["steps"]),
                            image_url=make_image_url(info["img"]),
                        )
                        ventures.append(v)
            else:
                for gt in GENERIC_TEMPLATES:
                    v = AgriVentureDataset(
                        crop_name=crop,
                        venture_name=f"{crop} {gt['suffix']}",
                        business_category=gt["cat"],
                        soil_suitability=info["soil"],
                        water_requirement=info["water"],
                        season_suitability=info["season"],
                        investment_range=gt["inv"],
                        investment_min=gt["lo"],
                        investment_max=gt["hi"],
                        roi_range=gt["roi"],
                        monthly_income=gt["mi"],
                        profit_margin=gt["pm"],
                        demand_level=gt["demand"],
                        raw_material_required=json.dumps({crop: "As per capacity", "Packaging": "As needed"}),
                        machinery_required=json.dumps(gt["machines"]),
                        production_capacity=json.dumps({"Daily": "Variable", "Monthly": "Variable"}),
                        market_demand=json.dumps({"type": ["Local traders", "Wholesalers", "Retailers", "Online"], "cities": ["Local", "State-wide"]}),
                        investment_breakdown=json.dumps({"Machinery": "40-50%", "Working Capital": "30%", "Setup & License": "20%"}),
                        implementation_steps=json.dumps(gt["steps"]),
                        image_url=make_image_url(info["img"]),
                    )
                    ventures.append(v)

        db.add_all(ventures)
        db.commit()
        print(f"Seeded {len(ventures)} agri ventures across {len(CROPS)} crops.")
    except Exception as e:
        print(f"Error seeding ventures: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
