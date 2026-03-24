import json
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.crop_business_model import CropBusinessDataset

# 25 Simulated Value-Added Businesses based on Agricultural Dataset
DATASET = [
    # --- POTATO ---
    {
        "crop_name": "Potato",
        "processed_product": "Potato Chips Manufacturing",
        "industry_type": "Snack Food Processing",
        "demand_level": "Very High",
        "industry_growth_rate": "15% Annual Growth",
        "investment_range": "₹8–12 Lakhs",
        "roi_range": "35–45%",
        "monthly_revenue": "₹3–5 Lakhs",
        "profit_margin": "25–30%",
        "break_even": "14 Months",
        "investment_breakdown": {
            "machinery": "₹6 Lakhs",
            "setup": "₹1.5 Lakhs",
            "packaging": "₹1 Lakhs",
            "working_capital": "₹1.5 Lakhs",
            "total": "₹10 Lakhs"
        },
        "raw_material_req": {
            "daily_crop_req": "1000 kg",
            "processing_yield": "300 kg chips (30% yield)"
        },
        "production_capacity": {
            "daily_output": "300 kg",
            "monthly_production": "7.5 Tons (25 days)"
        },
        "revenue_projection": {
            "selling_price": "₹150 per kg",
            "monthly_revenue": "₹11.25 Lakhs",
            "monthly_expenses": "₹8 Lakhs",
            "estimated_profit": "₹3.25 Lakhs"
        },
        "market_demand": {
            "demand_level": "Very High",
            "buyers": ["Supermarkets", "Kirana Stores", "Snack Distributors", "Bakeries"],
            "cities": ["Mumbai", "Delhi", "Hyderabad", "Pune"]
        },
        "machinery": ["Potato Washer", "Peeling Machine", "Slicing Machine", "Continuous Frying Machine", "Nitrogen Flush Packaging Machine"],
        "skills_required": ["Basic Food Processing", "Hygiene Management", "Packaging Operations"],
        "schemes": ["PMFME (35% Subsidy)", "MUDRA Loan", "Agriculture Infrastructure Fund"],
        "implementation_steps": ["Register MSME & FSSAI", "Apply for PMFME Subsidy", "Lease 1500 sq ft space", "Purchase and install machinery", "Source potatoes directly via eNAM", "Begin trial production"]
    },
    {
        "crop_name": "Potato",
        "processed_product": "Frozen French Fries Processing",
        "industry_type": "Frozen Food Processing",
        "demand_level": "High",
        "industry_growth_rate": "18% Annual Growth",
        "investment_range": "₹15–20 Lakhs",
        "roi_range": "30–40%",
        "monthly_revenue": "₹6–8 Lakhs",
        "profit_margin": "20–25%",
        "break_even": "18 Months",
        "investment_breakdown": {
            "machinery": "₹12 Lakhs",
            "setup": "₹2 Lakhs",
            "packaging": "₹1 Lakhs",
            "working_capital": "₹3 Lakhs",
            "total": "₹18 Lakhs"
        },
        "raw_material_req": {
            "daily_crop_req": "2000 kg",
            "processing_yield": "1000 kg fries (50% yield)"
        },
        "production_capacity": {
            "daily_output": "1000 kg",
            "monthly_production": "25 Tons"
        },
        "revenue_projection": {
            "selling_price": "₹90 per kg",
            "monthly_revenue": "₹22.5 Lakhs",
            "monthly_expenses": "₹18 Lakhs",
            "estimated_profit": "₹4.5 Lakhs"
        },
        "market_demand": {
            "demand_level": "High (B2B focused)",
            "buyers": ["Restaurants", "Fast Food Chains (QSR)", "Hotels", "Supermarkets"],
            "cities": ["Bengaluru", "Hyderabad", "Delhi NCR", "Chennai"]
        },
        "machinery": ["Washing Unit", "Steam Peeler", "Strip Cutter", "Blancher", "IQF (Individual Quick Freezing) Tunnel", "Cold Storage unit"],
        "skills_required": ["Cold Chain Management", "Temperature Control", "Food Safety (HACCP)"],
        "schemes": ["PMKSY (Cold Chain)", "State Food Processing Subsidy"],
        "implementation_steps": ["Secure Cold Storage Space", "Get FSSAI & HACCP certification", "Install IQF machinery", "Contract with local fast-food chains", "Set up refrigerated transport"]
    },
    {
        "crop_name": "Potato",
        "processed_product": "Potato Starch Production",
        "industry_type": "Industrial Agri-Processing",
        "demand_level": "Medium",
        "industry_growth_rate": "8% Annual Growth",
        "investment_range": "₹25–30 Lakhs",
        "roi_range": "25–35%",
        "monthly_revenue": "₹10–12 Lakhs",
        "profit_margin": "18–22%",
        "break_even": "24 Months",
        "investment_breakdown": {
            "machinery": "₹20 Lakhs",
            "setup": "₹4 Lakhs",
            "packaging": "₹1 Lakhs",
            "working_capital": "₹5 Lakhs",
            "total": "₹30 Lakhs"
        },
        "raw_material_req": {
            "daily_crop_req": "5000 kg (Can use lower grade/cull potatoes)",
            "processing_yield": "750 kg starch (15% yield)"
        },
        "production_capacity": {
            "daily_output": "750 kg",
            "monthly_production": "18 Tons"
        },
        "revenue_projection": {
            "selling_price": "₹60 per kg",
            "monthly_revenue": "₹10.8 Lakhs",
            "monthly_expenses": "₹8.5 Lakhs",
            "estimated_profit": "₹2.3 Lakhs"
        },
        "market_demand": {
            "demand_level": "Medium (Industrial)",
            "buyers": ["Textile Industries", "Paper Mills", "Pharmaceuticals", "Food Thickeners"],
            "cities": ["Ahmedabad", "Surat", "Ludhiana", "Mumbai"]
        },
        "machinery": ["Rasping Machine", "Centrifugal Extractor", "Hydrocyclone Wash", "Vacuum Filter", "Flash Dryer"],
        "skills_required": ["Chemical Processing", "Industrial Machine Operation", "Quality Testing"],
        "schemes": ["Agriculture Infrastructure Fund", "CGTMSE Loan"],
        "implementation_steps": ["Acquire 3000 sq ft industrial land", "Set up water treatment (effluent plant)", "Procure cull potatoes from farmers at low cost", "Establish tie-ups with paper/textile mills"]
    },
    {
        "crop_name": "Potato",
        "processed_product": "Dehydrated Potato Flakes",
        "industry_type": "Food Ingredients",
        "demand_level": "High",
        "industry_growth_rate": "20% Annual Growth",
        "investment_range": "₹12–18 Lakhs",
        "roi_range": "40–50%",
        "monthly_revenue": "₹5–7 Lakhs",
        "profit_margin": "30–35%",
        "break_even": "12 Months",
        "investment_breakdown": {
            "machinery": "₹9 Lakhs",
            "setup": "₹3 Lakhs",
            "packaging": "₹2 Lakhs",
            "working_capital": "₹2 Lakhs",
            "total": "₹16 Lakhs"
        },
        "raw_material_req": {
            "daily_crop_req": "2000 kg",
            "processing_yield": "300 kg flakes (15% yield)"
        },
        "production_capacity": {
            "daily_output": "300 kg",
            "monthly_production": "7.5 Tons"
        },
        "revenue_projection": {
            "selling_price": "₹180 per kg",
            "monthly_revenue": "₹13.5 Lakhs",
            "monthly_expenses": "₹9.5 Lakhs",
            "estimated_profit": "₹4 Lakhs"
        },
        "market_demand": {
            "demand_level": "High",
            "buyers": ["Ready-to-eat manufacturers", "Snack companies", "Export Markets", "Army canteens"],
            "cities": ["Delhi", "Chandigarh", "Bengaluru", "Kolkata"]
        },
        "machinery": ["Boiler", "Drum Dryer", "Flaker", "Hammer Mill", "Vacuum Sealer"],
        "skills_required": ["Dehydration Technology", "Moisture Control", "Export Logistics"],
        "schemes": ["PMFME", "APEDA Export Subsidy"],
        "implementation_steps": ["Procure high-solid potato varieties", "Install drum drying unit", "Obtain export license (IEC)", "Pitch to ready-to-eat brands (e.g., ITC, MTR)"]
    },
    {
        "crop_name": "Potato",
        "processed_product": "Potato Flour Processing",
        "industry_type": "Gluten-Free Foods",
        "demand_level": "Trending",
        "industry_growth_rate": "25% Annual Growth",
        "investment_range": "₹5–8 Lakhs",
        "roi_range": "45–55%",
        "monthly_revenue": "₹2–4 Lakhs",
        "profit_margin": "35–40%",
        "break_even": "10 Months",
        "investment_breakdown": {
            "machinery": "₹3.5 Lakhs",
            "setup": "₹1 Lakhs",
            "packaging": "₹1 Lakhs",
            "working_capital": "₹1 Lakhs",
            "total": "₹6.5 Lakhs"
        },
        "raw_material_req": {
            "daily_crop_req": "500 kg",
            "processing_yield": "100 kg flour (20% yield)"
        },
        "production_capacity": {
            "daily_output": "100 kg",
            "monthly_production": "2.5 Tons"
        },
        "revenue_projection": {
            "selling_price": "₹250 per kg",
            "monthly_revenue": "₹6.25 Lakhs",
            "monthly_expenses": "₹3.75 Lakhs",
            "estimated_profit": "₹2.5 Lakhs"
        },
        "market_demand": {
            "demand_level": "Trending (Health & Wellness)",
            "buyers": ["Gluten-free bakeries", "Health food stores", "Online (Amazon, BigBasket)", "Vegan restaurants"],
            "cities": ["Mumbai", "Bengaluru", "Hyderabad", "Gurugram"]
        },
        "machinery": ["Solar/Electric Tray Dryer", "Pulverizer/Mill", "Sieving Machine", "Pouch Packing Machine"],
        "skills_required": ["Milling", "Gluten-Free processing standards", "Digital Marketing"],
        "schemes": ["PMEGP (Prime Minister Employment Gen)", "Stand-Up India"],
        "implementation_steps": ["Register business", "Setup drying and milling unit", "Design premium packaging", "List on Amazon and health platforms", "Market as Gluten-Free alternative"]
    },

    # --- RICE ---
    {
        "crop_name": "Rice",
        "processed_product": "Rice Flour Processing",
        "industry_type": "Food Processing",
        "demand_level": "Very High",
        "industry_growth_rate": "10% Annual Growth",
        "investment_range": "₹4–7 Lakhs",
        "roi_range": "25–35%",
        "monthly_revenue": "₹2–3 Lakhs",
        "profit_margin": "20–25%",
        "break_even": "12 Months",
        "investment_breakdown": {"machinery": "₹3 Lakhs", "setup": "₹1 Lakhs", "packaging": "₹0.5 Lakhs", "working_capital": "₹1 Lakhs", "total": "₹5.5 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1000 kg", "processing_yield": "950 kg flour"},
        "production_capacity": {"daily_output": "950 kg", "monthly_production": "23.7 Tons"},
        "revenue_projection": {"selling_price": "₹45 per kg", "monthly_revenue": "₹10.6 Lakhs", "monthly_expenses": "₹8.5 Lakhs", "estimated_profit": "₹2.1 Lakhs"},
        "market_demand": {"demand_level": "Very High", "buyers": ["Bakeries", "Snack Brands", "Households"], "cities": ["Chennai", "Hyderabad", "Bengaluru", "Kochi"]},
        "machinery": ["Destoner", "Pulverizer", "Sifter", "Weighing Scale", "Sealer"],
        "skills_required": ["Basic Milling", "Packaging"],
        "schemes": ["PMFME"],
        "implementation_steps": ["Setup mill", "Source broken rice for low cost", "Package in 1kg/5kg bags", "Distribute to local Kirana stores"]
    },
    {
        "crop_name": "Rice",
        "processed_product": "Rice Bran Oil Extraction",
        "industry_type": "Edible Oil Processing",
        "demand_level": "High",
        "industry_growth_rate": "15% Annual Growth",
        "investment_range": "₹40–60 Lakhs",
        "roi_range": "20–30%",
        "monthly_revenue": "₹15–25 Lakhs",
        "profit_margin": "15–18%",
        "break_even": "36 Months",
        "investment_breakdown": {"machinery": "₹35 Lakhs", "setup": "₹10 Lakhs", "packaging": "₹5 Lakhs", "working_capital": "₹10 Lakhs", "total": "₹60 Lakhs"},
        "raw_material_req": {"daily_crop_req": "10 Tons (Rice Bran)", "processing_yield": "1.5 Tons Oil"},
        "production_capacity": {"daily_output": "1500 Liters", "monthly_production": "37,500 Liters"},
        "revenue_projection": {"selling_price": "₹140 per liter", "monthly_revenue": "₹52 Lakhs", "monthly_expenses": "₹44 Lakhs", "estimated_profit": "₹8 Lakhs"},
        "market_demand": {"demand_level": "High", "buyers": ["Supermarkets", "Health conscious consumers", "Restaurants"], "cities": ["Delhi", "Mumbai", "Kolkata"]},
        "machinery": ["Solvent Extraction Plant", "Refinery Unit", "Boiler", "Bottle Filling Machine"],
        "skills_required": ["Chemical Engineering", "Oil Refining", "Large Scale Plant Operation"],
        "schemes": ["Agri Tech Infrastructure Fund", "SME Loans"],
        "implementation_steps": ["Tie up with 5-10 rice mills for bran", "Setup solvent extraction plant", "Obtain strict FSSAI clearances", "Launch local brand"]
    },
    {
        "crop_name": "Rice",
        "processed_product": "Puffed Rice (Murmura) Manufacturing",
        "industry_type": "Snack Manufacturing",
        "demand_level": "High",
        "industry_growth_rate": "12% Annual Growth",
        "investment_range": "₹3–5 Lakhs",
        "roi_range": "50–60%",
        "monthly_revenue": "₹1.5–2.5 Lakhs",
        "profit_margin": "30–40%",
        "break_even": "8 Months",
        "investment_breakdown": {"machinery": "₹2 Lakhs", "setup": "₹0.5 Lakhs", "packaging": "₹0.5 Lakhs", "working_capital": "₹1 Lakhs", "total": "₹4 Lakhs"},
        "raw_material_req": {"daily_crop_req": "500 kg paddy", "processing_yield": "350 kg puffed rice"},
        "production_capacity": {"daily_output": "350 kg", "monthly_production": "8.7 Tons"},
        "revenue_projection": {"selling_price": "₹60 per kg", "monthly_revenue": "₹5.2 Lakhs", "monthly_expenses": "₹3.5 Lakhs", "estimated_profit": "₹1.7 Lakhs"},
        "market_demand": {"demand_level": "High (Regional)", "buyers": ["Street Vendors", "Snack Mix Brands", "Wholesalers"], "cities": ["Kolkata", "Patna", "Bhubaneswar", "Vijayawada"]},
        "machinery": ["Paddy Roaster", "Sand Separator", "Polisher", "Sealing Machine"],
        "skills_required": ["Roasting technique", "Heat management"],
        "schemes": ["MUDRA Shishu / Kishore"],
        "implementation_steps": ["Buy Roaster", "Hire 2 skilled roasters", "Source paddy locally", "Sell in bulk 10kg gunny bags to wholesalers"]
    },
    {
        "crop_name": "Rice",
        "processed_product": "Rice Noodles Production",
        "industry_type": "Convenience Foods",
        "demand_level": "Trending",
        "industry_growth_rate": "22% Annual Growth",
        "investment_range": "₹10–15 Lakhs",
        "roi_range": "40–45%",
        "monthly_revenue": "₹4–6 Lakhs",
        "profit_margin": "25–35%",
        "break_even": "15 Months",
        "investment_breakdown": {"machinery": "₹8 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹2 Lakhs", "total": "₹14 Lakhs"},
        "raw_material_req": {"daily_crop_req": "300 kg rice flour", "processing_yield": "280 kg noodles"},
        "production_capacity": {"daily_output": "280 kg", "monthly_production": "7 Tons"},
        "revenue_projection": {"selling_price": "₹120 per kg", "monthly_revenue": "₹8.4 Lakhs", "monthly_expenses": "₹5.6 Lakhs", "estimated_profit": "₹2.8 Lakhs"},
        "market_demand": {"demand_level": "Trending", "buyers": ["Pan-Asian Restaurants", "Supermarkets", "Online Groceries"], "cities": ["Bengaluru", "Mumbai", "Pune", "Delhi"]},
        "machinery": ["Dough Mixer", "Noodle Extruder", "Steamer", "Drying Cabinet", "Packaging Unit"],
        "skills_required": ["Extrusion Processing", "Quality Control"],
        "schemes": ["PMFME"],
        "implementation_steps": ["Setup clean room", "Install extruder and dryer", "Test noodle texture and boil time", "Package with tastemakers", "B2B sales to restaurants"]
    },
    {
        "crop_name": "Rice",
        "processed_product": "Rice Snack (Murukku/ पापड़) Processing",
        "industry_type": "Traditional Snacks",
        "demand_level": "Very High",
        "industry_growth_rate": "10% Annual Growth",
        "investment_range": "₹5–8 Lakhs",
        "roi_range": "35–50%",
        "monthly_revenue": "₹2.5–4 Lakhs",
        "profit_margin": "25–30%",
        "break_even": "10 Months",
        "investment_breakdown": {"machinery": "₹3 Lakhs", "setup": "₹1 Lakhs", "packaging": "₹1 Lakhs", "working_capital": "₹1.5 Lakhs", "total": "₹6.5 Lakhs"},
        "raw_material_req": {"daily_crop_req": "200 kg rice flour + spices", "processing_yield": "220 kg snacks"},
        "production_capacity": {"daily_output": "220 kg", "monthly_production": "5.5 Tons"},
        "revenue_projection": {"selling_price": "₹180 per kg", "monthly_revenue": "₹9.9 Lakhs", "monthly_expenses": "₹7 Lakhs", "estimated_profit": "₹2.9 Lakhs"},
        "market_demand": {"demand_level": "Very High", "buyers": ["Retailers", "Sweet Shops", "Export to NRIs"], "cities": ["Chennai", "Coimbatore", "Madurai", "Hyderabad"]},
        "machinery": ["Dough Kneader", "Murukku Extruder", "Continuous Fryer", "Oil Extractor", "Nitrogen Sealer"],
        "skills_required": ["Traditional Recipes", "Frying Management"],
        "schemes": ["PMEGP"],
        "implementation_steps": ["Standardize recipe", "Hire experienced snack makers", "Setup automated fryer", "Design attractive export-quality packaging"]
    },

    # --- TOMATO ---
    {
        "crop_name": "Tomato",
        "processed_product": "Tomato Sauce & Ketchup Processing",
        "industry_type": "Condiments",
        "demand_level": "Very High",
        "industry_growth_rate": "12% Annual Growth",
        "investment_range": "₹10–15 Lakhs",
        "roi_range": "30–40%",
        "monthly_revenue": "₹4–6 Lakhs",
        "profit_margin": "20–28%",
        "break_even": "18 Months",
        "investment_breakdown": {"machinery": "₹8 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹3 Lakhs", "total": "₹15 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1000 kg tomatoes", "processing_yield": "400 kg ketchup"},
        "production_capacity": {"daily_output": "400 kg", "monthly_production": "10 Tons"},
        "revenue_projection": {"selling_price": "₹120 per kg", "monthly_revenue": "₹12 Lakhs", "monthly_expenses": "₹9 Lakhs", "estimated_profit": "₹3 Lakhs"},
        "market_demand": {"demand_level": "Very High", "buyers": ["Fast Food Chains", "Supermarkets", "Households"], "cities": ["All major cities"]},
        "machinery": ["Washer", "Pulper", "Steam Jacketed Kettle", "Homogenizer", "Bottle Filling Machine"],
        "skills_required": ["Food formulation", "Preservation"],
        "schemes": ["PMFME"],
        "implementation_steps": ["Source ripe processing varieties", "Setup boiler and kettles", "Add preservatives & sugar", "Bottle and brand", "Distribute to retail"]
    },
    {
        "crop_name": "Tomato",
        "processed_product": "Tomato Puree Manufacturing",
        "industry_type": "Food Ingredients",
        "demand_level": "High",
        "industry_growth_rate": "18% Annual Growth",
        "investment_range": "₹8–12 Lakhs",
        "roi_range": "35–45%",
        "monthly_revenue": "₹3–5 Lakhs",
        "profit_margin": "25–30%",
        "break_even": "12 Months",
        "investment_breakdown": {"machinery": "₹6 Lakhs", "setup": "₹1.5 Lakhs", "packaging": "₹1.5 Lakhs", "working_capital": "₹2 Lakhs", "total": "₹11 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1500 kg", "processing_yield": "500 kg puree"},
        "production_capacity": {"daily_output": "500 kg", "monthly_production": "12.5 Tons"},
        "revenue_projection": {"selling_price": "₹80 per kg", "monthly_revenue": "₹10 Lakhs", "monthly_expenses": "₹7.2 Lakhs", "estimated_profit": "₹2.8 Lakhs"},
        "market_demand": {"demand_level": "High (B2B)", "buyers": ["Restaurants", "Cloud Kitchens", "Caterers"], "cities": ["Delhi NCR", "Mumbai", "Bengaluru"]},
        "machinery": ["Pulper", "Pasteurizer", "Vacuum Evaporator", "Aseptic Filler"],
        "skills_required": ["Pasteurization", "B2B Sales"],
        "schemes": ["State Agri Subsidy"],
        "implementation_steps": ["Buy tomatoes during glut season", "Pulp and concentrate", "Package in bulk 5kg/10kg food-grade pouches", "Supply to Cloud Kitchens"]
    },
    {
        "crop_name": "Tomato",
        "processed_product": "Sun-Dried Tomato Export",
        "industry_type": "Premium Foods / Export",
        "demand_level": "Trending",
        "industry_growth_rate": "25% Annual Growth",
        "investment_range": "₹6–10 Lakhs",
        "roi_range": "50–60%",
        "monthly_revenue": "₹4–7 Lakhs",
        "profit_margin": "40–50%",
        "break_even": "10 Months",
        "investment_breakdown": {"machinery": "₹4 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹1.5 Lakhs", "working_capital": "₹1.5 Lakhs", "total": "₹9 Lakhs"},
        "raw_material_req": {"daily_crop_req": "500 kg (Roma type)", "processing_yield": "50 kg dried"},
        "production_capacity": {"daily_output": "50 kg", "monthly_production": "1.25 Tons"},
        "revenue_projection": {"selling_price": "₹800 per kg", "monthly_revenue": "₹10 Lakhs", "monthly_expenses": "₹5.5 Lakhs", "estimated_profit": "₹4.5 Lakhs"},
        "market_demand": {"demand_level": "Trending (Export/Premium)", "buyers": ["Gourmet Restaurants", "Exporters (Italy, USA)"], "cities": ["Mumbai", "Export Hubs"]},
        "machinery": ["Solar Tunnel Dryers", "Slicer", "Vacuum Sealer", "Olive Oil Infusion Tanks"],
        "skills_required": ["Quality Drying", "Export Compliance"],
        "schemes": ["APEDA", "Nabard Solar Dryer Subsidy"],
        "implementation_steps": ["Build solar tunnel dryers", "Slice, salt, and dry tomatoes", "Preserve in olive oil jars", "Export or sell in premium supermarkets"]
    },
    {
        "crop_name": "Tomato",
        "processed_product": "Tomato Powder Production",
        "industry_type": "Food Ingredients",
        "demand_level": "High",
        "industry_growth_rate": "20% Annual Growth",
        "investment_range": "₹15–20 Lakhs",
        "roi_range": "40–50%",
        "monthly_revenue": "₹5–8 Lakhs",
        "profit_margin": "30–35%",
        "break_even": "16 Months",
        "investment_breakdown": {"machinery": "₹12 Lakhs", "setup": "₹3 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹3 Lakhs", "total": "₹20 Lakhs"},
        "raw_material_req": {"daily_crop_req": "2000 kg", "processing_yield": "100 kg powder"},
        "production_capacity": {"daily_output": "100 kg", "monthly_production": "2.5 Tons"},
        "revenue_projection": {"selling_price": "₹600 per kg", "monthly_revenue": "₹15 Lakhs", "monthly_expenses": "₹10 Lakhs", "estimated_profit": "₹5 Lakhs"},
        "market_demand": {"demand_level": "High", "buyers": ["Soup Makers", "Snack Seasoning Companies", "Instant Food Brands"], "cities": ["Pune", "Ahmedabad", "Delhi"]},
        "machinery": ["Spray Dryer / Vacuum Dryer", "Pulper", "Milling Machine"],
        "skills_required": ["Advanced Drying Tech", "Moisture Control"],
        "schemes": ["Agriculture Infrastructure Fund"],
        "implementation_steps": ["Setup Spray drying unit", "Process tomato slurry into powder", "Vacuum pack instantly to prevent caking", "B2B supply to seasoning companies"]
    },
    {
        "crop_name": "Tomato",
        "processed_product": "Tomato Seed Oil Extraction",
        "industry_type": "Cosmetics / Pharmaceuticals",
        "demand_level": "Niche",
        "industry_growth_rate": "30% Annual Growth",
        "investment_range": "₹10–15 Lakhs",
        "roi_range": "60–80%",
        "monthly_revenue": "₹3–6 Lakhs",
        "profit_margin": "50–60%",
        "break_even": "12 Months",
        "investment_breakdown": {"machinery": "₹8 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹1 Lakhs", "total": "₹13 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1000 kg tomato waste (seeds from puree plants)", "processing_yield": "5 Liters Oil"},
        "production_capacity": {"daily_output": "5 Liters", "monthly_production": "125 Liters"},
        "revenue_projection": {"selling_price": "₹8000 per Liter", "monthly_revenue": "₹10 Lakhs", "monthly_expenses": "₹4.5 Lakhs", "estimated_profit": "₹5.5 Lakhs"},
        "market_demand": {"demand_level": "Niche (High Value)", "buyers": ["Cosmetic Brands", "Skin Care Brands", "Export"], "cities": ["Mumbai", "Bengaluru"]},
        "machinery": ["Seed Separator", "Cold Press Oil Expeller", "Filter Press"],
        "skills_required": ["Cold Pressing", "Cosmetic Grade Filtration"],
        "schemes": ["Startup India"],
        "implementation_steps": ["Collect tomato pomace/waste from puree plants", "Separate and dry seeds", "Cold press for oil", "Bottle in dark glass bottles", "Sell B2B to cosmetic companies"]
    },

    # --- TURMERIC ---
    {
        "crop_name": "Turmeric",
        "processed_product": "Turmeric Powder Processing",
        "industry_type": "Spices",
        "demand_level": "Very High",
        "industry_growth_rate": "8% Annual Growth",
        "investment_range": "₹5–8 Lakhs",
        "roi_range": "35–45%",
        "monthly_revenue": "₹2.5–4 Lakhs",
        "profit_margin": "20–25%",
        "break_even": "10 Months",
        "investment_breakdown": {"machinery": "₹3.5 Lakhs", "setup": "₹1 Lakhs", "packaging": "₹1 Lakhs", "working_capital": "₹1.5 Lakhs", "total": "₹7 Lakhs"},
        "raw_material_req": {"daily_crop_req": "500 kg dry turmeric", "processing_yield": "480 kg powder"},
        "production_capacity": {"daily_output": "480 kg", "monthly_production": "12 Tons"},
        "revenue_projection": {"selling_price": "₹180 per kg", "monthly_revenue": "₹21.6 Lakhs", "monthly_expenses": "₹17 Lakhs", "estimated_profit": "₹4.6 Lakhs"},
        "market_demand": {"demand_level": "Very High", "buyers": ["Households", "Supermarkets", "Restaurants"], "cities": ["All India"]},
        "machinery": ["Pulverizer / Micro Pulverizer", "Sifter", "Blender", "Form Fill Seal Packaging Machine"],
        "skills_required": ["Grinding", "Quality Control (Curcumin levels)"],
        "schemes": ["PMFME", "Spices Board Subsidy"],
        "implementation_steps": ["Buy dried turmeric fingers", "Grind and sieve finely", "Pack in 100g/250g/500g pouches", "Distribute to FMCG network"]
    },
    {
        "crop_name": "Turmeric",
        "processed_product": "Curcumin Extraction",
        "industry_type": "Pharmaceuticals / Nutraceuticals",
        "demand_level": "Very High",
        "industry_growth_rate": "20% Annual Growth",
        "investment_range": "₹50–80 Lakhs",
        "roi_range": "40–60%",
        "monthly_revenue": "₹15–30 Lakhs",
        "profit_margin": "35–45%",
        "break_even": "24 Months",
        "investment_breakdown": {"machinery": "₹50 Lakhs", "setup": "₹10 Lakhs", "packaging": "₹5 Lakhs", "working_capital": "₹10 Lakhs", "total": "₹75 Lakhs"},
        "raw_material_req": {"daily_crop_req": "2000 kg high-curcumin turmeric", "processing_yield": "60 kg Curcumin (95%)"},
        "production_capacity": {"daily_output": "60 kg", "monthly_production": "1.5 Tons"},
        "revenue_projection": {"selling_price": "₹4000 per kg", "monthly_revenue": "₹60 Lakhs", "monthly_expenses": "₹35 Lakhs", "estimated_profit": "₹25 Lakhs"},
        "market_demand": {"demand_level": "Very High (Export & Pharma)", "buyers": ["Pharma Companies", "Vitamin Brands", "Exporters"], "cities": ["Hyderabad", "Mumbai", "US/Europe Export"]},
        "machinery": ["Solvent Extractor", "Evaporator", "Crystallizer", "Vacuum Dryer", "HPLC testing kit"],
        "skills_required": ["Chemical Engineering", "Pharma Grade QA/QC", "Export Regulation"],
        "schemes": ["NHB (National Horticulture Board)", "Agri Infrastructure Fund"],
        "implementation_steps": ["Setup solvent extraction plant", "Source Lakadong or Salem turmeric (High curcumin)", "Extract and crystallize to 95% purity", "Export to nutraceutical labs"]
    },
    {
        "crop_name": "Turmeric",
        "processed_product": "Organic Turmeric Export",
        "industry_type": "Premium Spices",
        "demand_level": "High",
        "industry_growth_rate": "15% Annual Growth",
        "investment_range": "₹8–12 Lakhs",
        "roi_range": "30–40%",
        "monthly_revenue": "₹5–8 Lakhs",
        "profit_margin": "30–35%",
        "break_even": "12 Months",
        "investment_breakdown": {"machinery": "₹4 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹3 Lakhs", "total": "₹11 Lakhs"},
        "raw_material_req": {"daily_crop_req": "500 kg (Certified Organic)", "processing_yield": "500 kg polished/packed"},
        "production_capacity": {"daily_output": "500 kg", "monthly_production": "12.5 Tons"},
        "revenue_projection": {"selling_price": "₹250 per kg", "monthly_revenue": "₹31 Lakhs", "monthly_expenses": "₹22 Lakhs", "estimated_profit": "₹9 Lakhs"},
        "market_demand": {"demand_level": "High", "buyers": ["International buyers", "Organic lifestyle brands"], "cities": ["Export (Dubai, UK, Germany)"]},
        "machinery": ["Polisher", "Color Sorter", "Metal Detector", "Vacuum Packer"],
        "skills_required": ["Organic Certification Management", "Export Logistics"],
        "schemes": ["APEDA", "Spices Board Export Grants"],
        "implementation_steps": ["Get NPOP Organic Certification", "Contract organic farmers", "Process and vacuum pack", "Acquire IEC code", "Export"]
    },
    {
        "crop_name": "Turmeric",
        "processed_product": "Turmeric Essential Oil Extraction",
        "industry_type": "Perfumery / Wellness",
        "demand_level": "Trending",
        "industry_growth_rate": "18% Annual Growth",
        "investment_range": "₹15–20 Lakhs",
        "roi_range": "40–50%",
        "monthly_revenue": "₹4–7 Lakhs",
        "profit_margin": "40–45%",
        "break_even": "18 Months",
        "investment_breakdown": {"machinery": "₹12 Lakhs", "setup": "₹3 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹2 Lakhs", "total": "₹19 Lakhs"},
        "raw_material_req": {"daily_crop_req": "500 kg turmeric leaves & rhizomes", "processing_yield": "5 Liters Oil"},
        "production_capacity": {"daily_output": "5 Liters", "monthly_production": "125 Liters"},
        "revenue_projection": {"selling_price": "₹6000 per Liter", "monthly_revenue": "₹7.5 Lakhs", "monthly_expenses": "₹4 Lakhs", "estimated_profit": "₹3.5 Lakhs"},
        "market_demand": {"demand_level": "Trending", "buyers": ["Aromatherapy brands", "Soap manufacturers", "Cosmetics"], "cities": ["Mumbai", "Bengaluru", "Kerala"]},
        "machinery": ["Steam Distillation Unit", "Condenser", "Oil Separator", "Bottling station"],
        "skills_required": ["Distillation Process", "Aromatherapy standards"],
        "schemes": ["CIMAP Guidance", "Startup India"],
        "implementation_steps": ["Setup steam distillation plant", "Boil turmeric leaves/rhizome", "Collect essential oil", "Bottle in dark 10ml/50ml vials", "Market to cosmetic brands"]
    },
    {
        "crop_name": "Turmeric",
        "processed_product": "Turmeric Capsule Manufacturing",
        "industry_type": "Nutraceuticals",
        "demand_level": "Trending",
        "industry_growth_rate": "25% Annual Growth",
        "investment_range": "₹10–15 Lakhs",
        "roi_range": "45–55%",
        "monthly_revenue": "₹5–9 Lakhs",
        "profit_margin": "45–50%",
        "break_even": "14 Months",
        "investment_breakdown": {"machinery": "₹8 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹2 Lakhs", "total": "₹14 Lakhs"},
        "raw_material_req": {"daily_crop_req": "20 kg 95% Curcumin + Piperine", "processing_yield": "40,000 Capsules"},
        "production_capacity": {"daily_output": "40,000 Capsules", "monthly_production": "10,00,000 Capsules"},
        "revenue_projection": {"selling_price": "₹2 per capsule", "monthly_revenue": "₹20 Lakhs", "monthly_expenses": "₹11 Lakhs", "estimated_profit": "₹9 Lakhs"},
        "market_demand": {"demand_level": "Trending", "buyers": ["Pharmacies", "E-commerce (Amazon, 1mg)", "Direct to Consumer"], "cities": ["Pan India", "Online"]},
        "machinery": ["Powder Mixer", "Semi-Auto Capsule Filling Machine", "Blister Packing Machine/Bottle Sealer"],
        "skills_required": ["Ayush / FSSAI licensing", "Nutraceutical formulation"],
        "schemes": ["Ministry of Ayush Subsidies"],
        "implementation_steps": ["Formulate Curcumin + Black Pepper (Piperine) mix", "Get Ayush/FSSAI license", "Run capsule filler", "Bottle into 60-cap bottles", "Sell via D2C e-commerce"]
    },

    # --- BANANA ---
    {
        "crop_name": "Banana",
        "processed_product": "Banana Chips Manufacturing",
        "industry_type": "Snack Food",
        "demand_level": "Very High",
        "industry_growth_rate": "12% Annual Growth",
        "investment_range": "₹5–8 Lakhs",
        "roi_range": "35–45%",
        "monthly_revenue": "₹2.5–4 Lakhs",
        "profit_margin": "25–30%",
        "break_even": "10 Months",
        "investment_breakdown": {"machinery": "₹4 Lakhs", "setup": "₹1 Lakhs", "packaging": "₹1 Lakhs", "working_capital": "₹1 Lakhs", "total": "₹7 Lakhs"},
        "raw_material_req": {"daily_crop_req": "500 kg raw green bananas", "processing_yield": "150 kg chips"},
        "production_capacity": {"daily_output": "150 kg", "monthly_production": "3.75 Tons"},
        "revenue_projection": {"selling_price": "₹250 per kg", "monthly_revenue": "₹9.3 Lakhs", "monthly_expenses": "₹6.5 Lakhs", "estimated_profit": "₹2.8 Lakhs"},
        "market_demand": {"demand_level": "Very High", "buyers": ["Retailers", "Supermarkets", "Online Groceries"], "cities": ["Kochi", "Chennai", "Mumbai", "Bengaluru"]},
        "machinery": ["Banana Slicer", "Continuous Fryer (Coconut Oil)", "Flavor Drum", "Nitrogen Pouch Packer"],
        "skills_required": ["Frying Temperature Control", "Flavoring"],
        "schemes": ["PMFME"],
        "implementation_steps": ["Source raw Nendran bananas", "Setup slicer directly over hot coconut oil", "Toss with salt/spices", "Nitrogen pack to retain crispness", "Distribute"]
    },
    {
        "crop_name": "Banana",
        "processed_product": "Banana Flour Processing",
        "industry_type": "Gluten-Free Foods",
        "demand_level": "Trending",
        "industry_growth_rate": "22% Annual Growth",
        "investment_range": "₹8–12 Lakhs",
        "roi_range": "40–50%",
        "monthly_revenue": "₹3–5 Lakhs",
        "profit_margin": "30–35%",
        "break_even": "14 Months",
        "investment_breakdown": {"machinery": "₹7 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹1.5 Lakhs", "working_capital": "₹1.5 Lakhs", "total": "₹12 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1000 kg green bananas", "processing_yield": "200 kg flour"},
        "production_capacity": {"daily_output": "200 kg", "monthly_production": "5 Tons"},
        "revenue_projection": {"selling_price": "₹180 per kg", "monthly_revenue": "₹9 Lakhs", "monthly_expenses": "₹5.5 Lakhs", "estimated_profit": "₹3.5 Lakhs"},
        "market_demand": {"demand_level": "Trending", "buyers": ["Gluten-free Bakeries", "Baby Food Brands", "Export"], "cities": ["Mumbai", "Delhi", "Export"]},
        "machinery": ["Peeler", "Chopper", "Cabinet Dryer / Solar Dryer", "Pulverizer", "Sifter"],
        "skills_required": ["Moisture management", "Hygienic milling"],
        "schemes": ["PMEGP"],
        "implementation_steps": ["Peel and slice green bananas", "Dry them below 10% moisture", "Mill into fine powder", "Package as premium Gluten-Rich/Resistant Starch flour"]
    },
    {
        "crop_name": "Banana",
        "processed_product": "Banana Fiber Extraction",
        "industry_type": "Textiles / Handicrafts",
        "demand_level": "High",
        "industry_growth_rate": "15% Annual Growth",
        "investment_range": "₹3–5 Lakhs",
        "roi_range": "30–40%",
        "monthly_revenue": "₹1.5–2.5 Lakhs",
        "profit_margin": "35–45%",
        "break_even": "12 Months",
        "investment_breakdown": {"machinery": "₹2 Lakhs", "setup": "₹1 Lakhs", "packaging": "₹0.5 Lakhs", "working_capital": "₹1 Lakhs", "total": "₹4.5 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1000 kg banana pseudo-stems (agri-waste)", "processing_yield": "15 kg premium fiber"},
        "production_capacity": {"daily_output": "15 kg", "monthly_production": "375 kg"},
        "revenue_projection": {"selling_price": "₹600 per kg", "monthly_revenue": "₹2.25 Lakhs", "monthly_expenses": "₹1 Lakhs", "estimated_profit": "₹1.25 Lakhs"},
        "market_demand": {"demand_level": "High (Eco-friendly)", "buyers": ["Textile Mills", "Handicraft NGOs", "Paper Mills"], "cities": ["Surat", "Coimbatore", "Delhi"]},
        "machinery": ["Banana Fiber Extractor Machine", "Washing tanks", "Sun drying racks", "Spinning Charkha (optional)"],
        "skills_required": ["Machine operation", "Fiber sorting"],
        "schemes": ["KVIC (Khadi and Village Industries)", "MSME Agri-Waste scheme"],
        "implementation_steps": ["Collect waste banana stems after harvest", "Run through extractor machine", "Wash and sun-dry the fibers", "Bundle and sell to eco-textile weavers"]
    },
    {
        "crop_name": "Banana",
        "processed_product": "Banana Puree Processing",
        "industry_type": "Food Ingredients",
        "demand_level": "High",
        "industry_growth_rate": "10% Annual Growth",
        "investment_range": "₹15–20 Lakhs",
        "roi_range": "25–35%",
        "monthly_revenue": "₹4–6 Lakhs",
        "profit_margin": "20–25%",
        "break_even": "18 Months",
        "investment_breakdown": {"machinery": "₹12 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹3 Lakhs", "working_capital": "₹3 Lakhs", "total": "₹20 Lakhs"},
        "raw_material_req": {"daily_crop_req": "2000 kg ripe bananas", "processing_yield": "1200 kg puree"},
        "production_capacity": {"daily_output": "1200 kg", "monthly_production": "30 Tons"},
        "revenue_projection": {"selling_price": "₹60 per kg", "monthly_revenue": "₹18 Lakhs", "monthly_expenses": "₹14.5 Lakhs", "estimated_profit": "₹3.5 Lakhs"},
        "market_demand": {"demand_level": "High", "buyers": ["Ice Cream Brands", "Baby Food Cos", "Juice Brands"], "cities": ["Mumbai", "Bengaluru", "Delhi"]},
        "machinery": ["Peeling table", "Pulper", "Pasteurizer", "Aseptic packaging unit"],
        "skills_required": ["Pasteurization", "Aseptic handling"],
        "schemes": ["Agriculture Infrastructure Fund"],
        "implementation_steps": ["Ripen bananas uniformly", "Pulp and pasteurize to kill bacteria", "Pack in aseptic drums (shelf-life of months without fridge)", "Sell to FMCG companies B2B"]
    },
    {
        "crop_name": "Banana",
        "processed_product": "Banana Powder Production",
        "industry_type": "Nutraceutical / Food",
        "demand_level": "Medium",
        "industry_growth_rate": "15% Annual Growth",
        "investment_range": "₹10–15 Lakhs",
        "roi_range": "35–45%",
        "monthly_revenue": "₹3–5 Lakhs",
        "profit_margin": "30–35%",
        "break_even": "14 Months",
        "investment_breakdown": {"machinery": "₹8 Lakhs", "setup": "₹2 Lakhs", "packaging": "₹2 Lakhs", "working_capital": "₹2 Lakhs", "total": "₹14 Lakhs"},
        "raw_material_req": {"daily_crop_req": "1000 kg ripe bananas", "processing_yield": "150 kg powder"},
        "production_capacity": {"daily_output": "150 kg", "monthly_production": "3.75 Tons"},
        "revenue_projection": {"selling_price": "₹350 per kg", "monthly_revenue": "₹13 Lakhs", "monthly_expenses": "₹8.5 Lakhs", "estimated_profit": "₹4.5 Lakhs"},
        "market_demand": {"demand_level": "Medium", "buyers": ["Baby Food Brands", "Health Drink Mixes", "Baking Industries"], "cities": ["Pune", "Chennai", "Delhi"]},
        "machinery": ["Spray Dryer / Freeze Dryer", "Pulper", "Homogenizer", "Vacuum Sealer"],
        "skills_required": ["Spray drying tech", "Powder handling"],
        "schemes": ["PMFME"],
        "implementation_steps": ["Pulp ripe bananas", "Pump slurry into spray dryer", "Collect fine banana powder", "Package instantly to prevent moisture clumping", "Supply to baby food manufacturers"]
    }
]

def run_seed():
    db = SessionLocal()
    try:
        # Check if empty
        if db.query(CropBusinessDataset).count() == 0:
            print("Seeding Crop Business Dataset (25 Items)...")
            for item in DATASET:
                # Need to convert all dict/list to json string to store in Text fields
                item_copy = item.copy()
                item_copy["investment_breakdown"] = json.dumps(item_copy["investment_breakdown"])
                item_copy["raw_material_req"] = json.dumps(item_copy["raw_material_req"])
                item_copy["production_capacity"] = json.dumps(item_copy["production_capacity"])
                item_copy["revenue_projection"] = json.dumps(item_copy["revenue_projection"])
                item_copy["market_demand"] = json.dumps(item_copy["market_demand"])
                item_copy["machinery"] = json.dumps(item_copy["machinery"])
                item_copy["skills_required"] = json.dumps(item_copy["skills_required"])
                item_copy["schemes"] = json.dumps(item_copy["schemes"])
                item_copy["implementation_steps"] = json.dumps(item_copy["implementation_steps"])
                
                db.add(CropBusinessDataset(**item_copy))
            db.commit()
            print("Successfully seeded Crop Business Dataset.")
    except Exception as e:
        print(f"Error seeding crop business dataset: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
