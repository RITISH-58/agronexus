"""
Dynamic Agri-Business Generator Engine.
Maps products/crops to value-added businesses using CSV datasets and rule-based generation.
"""
import os, csv, random, hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent.parent.parent / "datasets"

# ── Product → Business Mapping (100+ products, 1000+ combinations) ──
PRODUCT_BUSINESS_MAP = {
    # DAIRY
    "milk": [
        {"name": "Paneer Production Unit", "category": "Dairy", "inv_min": 3, "inv_max": 8, "roi": "30-40%", "margin": "25-35%", "risk": "Low", "water": "Medium", "land_min": 0.5},
        {"name": "Ghee Processing Plant", "category": "Dairy", "inv_min": 5, "inv_max": 12, "roi": "25-35%", "margin": "20-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Flavoured Milk Bottling", "category": "Dairy", "inv_min": 8, "inv_max": 20, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Milk Powder Plant", "category": "Dairy", "inv_min": 15, "inv_max": 40, "roi": "20-30%", "margin": "18-25%", "risk": "Medium", "water": "Medium", "land_min": 2},
        {"name": "Organic Dairy Products", "category": "Dairy", "inv_min": 5, "inv_max": 15, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Medium", "land_min": 1},
        {"name": "Cheese Making Unit", "category": "Dairy", "inv_min": 8, "inv_max": 20, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Yogurt & Curd Production", "category": "Dairy", "inv_min": 5, "inv_max": 15, "roi": "28-38%", "margin": "22-32%", "risk": "Low", "water": "Medium", "land_min": 0.5},
        {"name": "Ice Cream Manufacturing", "category": "Dairy", "inv_min": 10, "inv_max": 30, "roi": "32-45%", "margin": "28-38%", "risk": "Medium", "water": "Medium", "land_min": 1.5},
        {"name": "Butter Production Unit", "category": "Dairy", "inv_min": 5, "inv_max": 12, "roi": "22-30%", "margin": "18-25%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
    # GRAINS
    "rice": [
        {"name": "Rice Flour Mill", "category": "Grain Processing", "inv_min": 3, "inv_max": 8, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Puffed Rice Manufacturing", "category": "Grain Processing", "inv_min": 2, "inv_max": 5, "roi": "30-45%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Rice Bran Oil Extraction", "category": "Oil Extraction", "inv_min": 10, "inv_max": 25, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Low", "land_min": 1.5},
        {"name": "Flattened Rice (Poha) Unit", "category": "Grain Processing", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Rice Vermicelli Unit", "category": "Grain Processing", "inv_min": 5, "inv_max": 12, "roi": "30-40%", "margin": "25-32%", "risk": "Low", "water": "Medium", "land_min": 1},
        {"name": "Idli Dosa Batter Unit", "category": "Ready Food", "inv_min": 2, "inv_max": 5, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Medium", "land_min": 0.5},
        {"name": "Organic Rice Brand", "category": "Organic", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-45%", "risk": "Low", "water": "Low", "land_min": 2},
    ],
    "wheat": [
        {"name": "Wheat Flour Mill (Atta Chakki)", "category": "Grain Processing", "inv_min": 5, "inv_max": 12, "roi": "22-30%", "margin": "18-25%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Bread & Bakery Unit", "category": "Bakery", "inv_min": 8, "inv_max": 20, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Biscuit Manufacturing", "category": "Bakery", "inv_min": 15, "inv_max": 40, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Medium", "land_min": 2},
        {"name": "Pasta & Noodles Unit", "category": "Grain Processing", "inv_min": 8, "inv_max": 20, "roi": "30-40%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Semolina (Suji/Rava) Plant", "category": "Grain Processing", "inv_min": 5, "inv_max": 12, "roi": "25-32%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Cookie & Snacks Bakery", "category": "Bakery", "inv_min": 5, "inv_max": 15, "roi": "32-45%", "margin": "28-38%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
    "maize": [
        {"name": "Maize Starch Unit", "category": "Grain Processing", "inv_min": 15, "inv_max": 35, "roi": "25-35%", "margin": "20-28%", "risk": "Medium", "water": "High", "land_min": 2},
        {"name": "Cornflakes Manufacturing", "category": "Cereal", "inv_min": 10, "inv_max": 25, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1.5},
        {"name": "Corn Oil Extraction", "category": "Oil Extraction", "inv_min": 10, "inv_max": 25, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Low", "land_min": 1.5},
        {"name": "Popcorn Processing", "category": "Snacks", "inv_min": 2, "inv_max": 5, "roi": "40-60%", "margin": "35-50%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Cattle Feed Production", "category": "Feed", "inv_min": 5, "inv_max": 12, "roi": "20-28%", "margin": "15-22%", "risk": "Low", "water": "Low", "land_min": 1},
    ],
    "potato": [
        {"name": "Potato Chips Manufacturing", "category": "Snacks", "inv_min": 5, "inv_max": 15, "roi": "35-50%", "margin": "28-40%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Dehydrated Potato Processing", "category": "Preserved Food", "inv_min": 5, "inv_max": 12, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Potato Starch Plant", "category": "Starch", "inv_min": 8, "inv_max": 20, "roi": "25-32%", "margin": "20-28%", "risk": "Medium", "water": "High", "land_min": 1.5},
        {"name": "Frozen French Fries Unit", "category": "Frozen Food", "inv_min": 15, "inv_max": 35, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 2},
        {"name": "Seed Potato Business", "category": "Agriculture", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Medium", "land_min": 2},
        {"name": "Potato Flakes Production", "category": "Preserved Food", "inv_min": 8, "inv_max": 18, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Low", "land_min": 1},
    ],
    "tomato": [
        {"name": "Tomato Ketchup Unit", "category": "Sauce", "inv_min": 5, "inv_max": 12, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Tomato Paste Production", "category": "Sauce", "inv_min": 8, "inv_max": 18, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Tomato Powder Unit", "category": "Preserved Food", "inv_min": 5, "inv_max": 12, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Sun-dried Tomato Export", "category": "Export", "inv_min": 3, "inv_max": 8, "roi": "40-55%", "margin": "35-45%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Tomato Sauce & Puree", "category": "Sauce", "inv_min": 5, "inv_max": 12, "roi": "28-38%", "margin": "22-32%", "risk": "Low", "water": "Medium", "land_min": 0.5},
    ],
    "onion": [
        {"name": "Onion Dehydration Unit", "category": "Preserved Food", "inv_min": 5, "inv_max": 12, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Onion Powder Production", "category": "Spice Processing", "inv_min": 5, "inv_max": 12, "roi": "35-48%", "margin": "28-38%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Onion Paste Unit", "category": "Processed Food", "inv_min": 3, "inv_max": 8, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Onion Storage & Export", "category": "Export", "inv_min": 10, "inv_max": 25, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Low", "land_min": 2},
        {"name": "Onion Flakes Processing", "category": "Preserved Food", "inv_min": 5, "inv_max": 12, "roi": "32-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
    "turmeric": [
        {"name": "Turmeric Powder Processing", "category": "Spice Processing", "inv_min": 3, "inv_max": 8, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Curcumin Extraction Unit", "category": "Pharma", "inv_min": 20, "inv_max": 50, "roi": "40-60%", "margin": "35-50%", "risk": "High", "water": "Medium", "land_min": 1.5},
        {"name": "Organic Turmeric Export", "category": "Export", "inv_min": 5, "inv_max": 12, "roi": "35-50%", "margin": "30-45%", "risk": "Medium", "water": "Low", "land_min": 2},
        {"name": "Turmeric Oil Extraction", "category": "Oil Extraction", "inv_min": 5, "inv_max": 15, "roi": "32-45%", "margin": "28-38%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Turmeric Capsule Manufacturing", "category": "Pharma", "inv_min": 10, "inv_max": 25, "roi": "40-55%", "margin": "35-45%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Medicinal Turmeric Products", "category": "Herbal", "inv_min": 5, "inv_max": 12, "roi": "35-48%", "margin": "28-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
    "chili": [
        {"name": "Chili Powder Unit", "category": "Spice Processing", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Chili Sauce Production", "category": "Sauce", "inv_min": 5, "inv_max": 12, "roi": "32-45%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 0.5},
        {"name": "Chili Flakes & Crushed Chili", "category": "Spice Processing", "inv_min": 3, "inv_max": 8, "roi": "30-40%", "margin": "25-32%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Chili Oil Extraction", "category": "Oil Extraction", "inv_min": 5, "inv_max": 12, "roi": "35-48%", "margin": "28-38%", "risk": "Medium", "water": "Low", "land_min": 0.5},
        {"name": "Dried Red Chili Export", "category": "Export", "inv_min": 5, "inv_max": 15, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Low", "land_min": 1},
    ],
    "sugarcane": [
        {"name": "Jaggery Production Unit", "category": "Processing", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Medium", "land_min": 1},
        {"name": "Sugarcane Juice Parlor", "category": "Beverages", "inv_min": 1, "inv_max": 3, "roi": "40-60%", "margin": "35-50%", "risk": "Low", "water": "Low", "land_min": 0.1},
        {"name": "Organic Jaggery Export", "category": "Export", "inv_min": 5, "inv_max": 12, "roi": "35-50%", "margin": "30-40%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Bagasse Briquettes Plant", "category": "Energy", "inv_min": 5, "inv_max": 15, "roi": "25-35%", "margin": "20-28%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Ethanol Production Unit", "category": "Fuel", "inv_min": 50, "inv_max": 200, "roi": "22-30%", "margin": "18-25%", "risk": "High", "water": "High", "land_min": 5},
    ],
    "cotton": [
        {"name": "Cotton Ginning Plant", "category": "Textile", "inv_min": 15, "inv_max": 40, "roi": "22-30%", "margin": "18-25%", "risk": "Medium", "water": "Low", "land_min": 2},
        {"name": "Cotton Yarn Spinning", "category": "Textile", "inv_min": 20, "inv_max": 50, "roi": "25-32%", "margin": "20-28%", "risk": "Medium", "water": "Low", "land_min": 3},
        {"name": "Surgical Cotton Unit", "category": "Medical", "inv_min": 10, "inv_max": 25, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Cotton Seed Oil Extraction", "category": "Oil Extraction", "inv_min": 8, "inv_max": 20, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Cotton Bale Trading", "category": "Trading", "inv_min": 5, "inv_max": 15, "roi": "20-28%", "margin": "15-22%", "risk": "Low", "water": "Low", "land_min": 2},
    ],
    "groundnut": [
        {"name": "Groundnut Oil Mill", "category": "Oil Extraction", "inv_min": 8, "inv_max": 20, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Peanut Butter Manufacturing", "category": "Processed Food", "inv_min": 5, "inv_max": 12, "roi": "35-48%", "margin": "28-38%", "risk": "Medium", "water": "Low", "land_min": 0.5},
        {"name": "Roasted Peanut Packaging", "category": "Snacks", "inv_min": 2, "inv_max": 5, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Groundnut Cake Feed", "category": "Feed", "inv_min": 3, "inv_max": 8, "roi": "20-28%", "margin": "15-22%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Groundnut Export Business", "category": "Export", "inv_min": 5, "inv_max": 15, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Low", "land_min": 1},
    ],
    "soybean": [
        {"name": "Soybean Oil Extraction", "category": "Oil Extraction", "inv_min": 10, "inv_max": 25, "roi": "22-30%", "margin": "18-25%", "risk": "Medium", "water": "Low", "land_min": 1.5},
        {"name": "Soy Milk Production", "category": "Beverages", "inv_min": 5, "inv_max": 15, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Tofu Manufacturing", "category": "Processed Food", "inv_min": 5, "inv_max": 12, "roi": "32-45%", "margin": "28-38%", "risk": "Medium", "water": "Medium", "land_min": 0.5},
        {"name": "Soy Chunks (TVP) Unit", "category": "Processed Food", "inv_min": 8, "inv_max": 20, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Soy Sauce Production", "category": "Sauce", "inv_min": 5, "inv_max": 15, "roi": "35-48%", "margin": "30-40%", "risk": "Medium", "water": "Medium", "land_min": 0.5},
    ],
    "coconut": [
        {"name": "Virgin Coconut Oil Unit", "category": "Oil Extraction", "inv_min": 5, "inv_max": 15, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Coconut Milk Processing", "category": "Beverages", "inv_min": 5, "inv_max": 12, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Medium", "land_min": 0.5},
        {"name": "Desiccated Coconut Unit", "category": "Preserved Food", "inv_min": 5, "inv_max": 12, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Coir Products Manufacturing", "category": "Fiber", "inv_min": 3, "inv_max": 8, "roi": "22-30%", "margin": "18-25%", "risk": "Low", "water": "Medium", "land_min": 1},
        {"name": "Coconut Shell Charcoal", "category": "Fuel", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Coconut Water Bottling", "category": "Beverages", "inv_min": 8, "inv_max": 20, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Low", "land_min": 1},
    ],
    "banana": [
        {"name": "Banana Chips Manufacturing", "category": "Snacks", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "28-38%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Banana Powder Production", "category": "Preserved Food", "inv_min": 5, "inv_max": 12, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Banana Fiber Extraction", "category": "Fiber", "inv_min": 5, "inv_max": 12, "roi": "32-45%", "margin": "28-38%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Banana Wine Production", "category": "Beverages", "inv_min": 8, "inv_max": 20, "roi": "35-50%", "margin": "30-40%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Banana Export Business", "category": "Export", "inv_min": 5, "inv_max": 15, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Low", "land_min": 2},
    ],
    "mango": [
        {"name": "Mango Pulp Processing", "category": "Processing", "inv_min": 8, "inv_max": 18, "roi": "28-38%", "margin": "22-30%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Mango Pickle Unit", "category": "Preserved Food", "inv_min": 2, "inv_max": 6, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Mango Juice & Nectar", "category": "Beverages", "inv_min": 8, "inv_max": 20, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Dried Mango Export", "category": "Export", "inv_min": 5, "inv_max": 12, "roi": "35-48%", "margin": "30-40%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Mango Jam & Jelly", "category": "Preserved Food", "inv_min": 3, "inv_max": 8, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
    "tea": [
        {"name": "Tea Processing Factory", "category": "Beverage Processing", "inv_min": 15, "inv_max": 40, "roi": "22-30%", "margin": "18-25%", "risk": "Medium", "water": "Medium", "land_min": 2},
        {"name": "Green Tea Brand", "category": "Beverage Processing", "inv_min": 5, "inv_max": 15, "roi": "35-50%", "margin": "30-40%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Herbal Tea Blending", "category": "Beverage Processing", "inv_min": 3, "inv_max": 10, "roi": "40-55%", "margin": "35-45%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Tea Export Business", "category": "Export", "inv_min": 10, "inv_max": 25, "roi": "25-35%", "margin": "20-28%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Specialty Tea Boutique", "category": "Retail", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 0.2},
    ],
    "coffee": [
        {"name": "Coffee Roasting Unit", "category": "Beverage Processing", "inv_min": 5, "inv_max": 15, "roi": "30-42%", "margin": "25-35%", "risk": "Medium", "water": "Low", "land_min": 0.5},
        {"name": "Instant Coffee Plant", "category": "Beverage Processing", "inv_min": 20, "inv_max": 50, "roi": "25-35%", "margin": "20-28%", "risk": "High", "water": "Medium", "land_min": 2},
        {"name": "Specialty Coffee Brand", "category": "Retail", "inv_min": 5, "inv_max": 15, "roi": "35-50%", "margin": "30-42%", "risk": "Medium", "water": "Low", "land_min": 0.5},
        {"name": "Coffee Export Business", "category": "Export", "inv_min": 10, "inv_max": 25, "roi": "25-35%", "margin": "20-28%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Cold Brew Coffee Unit", "category": "Beverages", "inv_min": 3, "inv_max": 8, "roi": "40-55%", "margin": "35-45%", "risk": "Low", "water": "Medium", "land_min": 0.5},
    ],
    "honey": [
        {"name": "Honey Processing & Packaging", "category": "Processing", "inv_min": 3, "inv_max": 8, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Organic Honey Brand", "category": "Organic", "inv_min": 5, "inv_max": 12, "roi": "38-55%", "margin": "32-45%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Flavoured Honey Products", "category": "Processed Food", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Bee Farming Training Center", "category": "Service", "inv_min": 2, "inv_max": 5, "roi": "40-60%", "margin": "35-50%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Honey Export Business", "category": "Export", "inv_min": 5, "inv_max": 15, "roi": "28-40%", "margin": "22-32%", "risk": "Medium", "water": "Low", "land_min": 0.5},
    ],
    "mushroom": [
        {"name": "Mushroom Cultivation Farm", "category": "Cultivation", "inv_min": 2, "inv_max": 5, "roi": "40-60%", "margin": "35-50%", "risk": "Medium", "water": "Medium", "land_min": 0.2},
        {"name": "Dried Mushroom Processing", "category": "Preserved Food", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Mushroom Pickle Unit", "category": "Preserved Food", "inv_min": 2, "inv_max": 5, "roi": "35-48%", "margin": "28-38%", "risk": "Low", "water": "Low", "land_min": 0.2},
        {"name": "Mushroom Powder Production", "category": "Superfood", "inv_min": 3, "inv_max": 8, "roi": "40-55%", "margin": "35-45%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Mushroom Spawn Lab", "category": "Agriculture", "inv_min": 5, "inv_max": 12, "roi": "35-50%", "margin": "30-40%", "risk": "Medium", "water": "Medium", "land_min": 0.5},
    ],
    "millets": [
        {"name": "Millet Flour Processing", "category": "Grain Processing", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Millet Health Cookies", "category": "Bakery", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-42%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Millet Ready-to-Eat Mixes", "category": "Ready Food", "inv_min": 5, "inv_max": 12, "roi": "35-50%", "margin": "30-42%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Millet Health Drinks", "category": "Beverages", "inv_min": 5, "inv_max": 15, "roi": "38-55%", "margin": "30-45%", "risk": "Medium", "water": "Medium", "land_min": 1},
        {"name": "Organic Millet Brand", "category": "Organic", "inv_min": 3, "inv_max": 8, "roi": "40-55%", "margin": "35-45%", "risk": "Low", "water": "Low", "land_min": 2},
    ],
    "pulses": [
        {"name": "Dal Mill (Pulse Processing)", "category": "Grain Processing", "inv_min": 5, "inv_max": 15, "roi": "22-30%", "margin": "18-25%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Besan (Gram Flour) Unit", "category": "Grain Processing", "inv_min": 5, "inv_max": 12, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Papad Manufacturing", "category": "Snacks", "inv_min": 2, "inv_max": 5, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Ready-to-Cook Dal Packs", "category": "Ready Food", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Pulse Export Business", "category": "Export", "inv_min": 5, "inv_max": 15, "roi": "25-35%", "margin": "20-28%", "risk": "Medium", "water": "Low", "land_min": 1},
    ],
    "ginger": [
        {"name": "Ginger Powder Processing", "category": "Spice Processing", "inv_min": 4, "inv_max": 10, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Ginger Oil Extraction", "category": "Oil Extraction", "inv_min": 5, "inv_max": 15, "roi": "35-48%", "margin": "30-40%", "risk": "Medium", "water": "Low", "land_min": 0.5},
        {"name": "Ginger Candy & Confectionery", "category": "Confectionery", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "28-40%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Dried Ginger Export", "category": "Export", "inv_min": 5, "inv_max": 12, "roi": "28-40%", "margin": "22-32%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Ginger Tea Premix", "category": "Beverages", "inv_min": 3, "inv_max": 8, "roi": "32-45%", "margin": "28-38%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
    "garlic": [
        {"name": "Garlic Powder Unit", "category": "Spice Processing", "inv_min": 3, "inv_max": 8, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Garlic Paste Production", "category": "Processed Food", "inv_min": 3, "inv_max": 8, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Garlic Oil Extraction", "category": "Oil Extraction", "inv_min": 5, "inv_max": 12, "roi": "35-48%", "margin": "28-38%", "risk": "Medium", "water": "Low", "land_min": 0.5},
        {"name": "Dehydrated Garlic Export", "category": "Export", "inv_min": 5, "inv_max": 12, "roi": "28-40%", "margin": "22-32%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Black Garlic Processing", "category": "Specialty", "inv_min": 3, "inv_max": 8, "roi": "40-55%", "margin": "35-45%", "risk": "Medium", "water": "Low", "land_min": 0.5},
    ],
    "mustard": [
        {"name": "Mustard Oil Mill", "category": "Oil Extraction", "inv_min": 5, "inv_max": 15, "roi": "22-30%", "margin": "18-25%", "risk": "Low", "water": "Low", "land_min": 1},
        {"name": "Mustard Sauce Production", "category": "Sauce", "inv_min": 3, "inv_max": 8, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Mustard Seed Export", "category": "Export", "inv_min": 5, "inv_max": 12, "roi": "22-30%", "margin": "18-25%", "risk": "Medium", "water": "Low", "land_min": 1},
        {"name": "Cold-Pressed Mustard Oil", "category": "Organic", "inv_min": 5, "inv_max": 12, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
        {"name": "Mustard Cake Feed", "category": "Feed", "inv_min": 2, "inv_max": 5, "roi": "18-25%", "margin": "15-20%", "risk": "Low", "water": "Low", "land_min": 0.5},
    ],
}

# Additional generic categories for any unlisted product
GENERIC_BUSINESSES = [
    {"name": "{product} Processing Unit", "category": "Processing", "inv_min": 3, "inv_max": 10, "roi": "25-35%", "margin": "20-28%", "risk": "Low", "water": "Low", "land_min": 0.5},
    {"name": "{product} Powder Production", "category": "Processing", "inv_min": 3, "inv_max": 8, "roi": "28-38%", "margin": "22-30%", "risk": "Low", "water": "Low", "land_min": 0.5},
    {"name": "{product} Organic Brand", "category": "Organic", "inv_min": 3, "inv_max": 8, "roi": "35-50%", "margin": "30-40%", "risk": "Low", "water": "Low", "land_min": 1},
    {"name": "{product} Export Business", "category": "Export", "inv_min": 5, "inv_max": 15, "roi": "25-38%", "margin": "20-30%", "risk": "Medium", "water": "Low", "land_min": 1},
    {"name": "{product} Pickle & Preservation", "category": "Preserved Food", "inv_min": 2, "inv_max": 5, "roi": "30-45%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
    {"name": "{product} Value Addition Unit", "category": "Processed Food", "inv_min": 5, "inv_max": 12, "roi": "28-40%", "margin": "22-32%", "risk": "Medium", "water": "Medium", "land_min": 0.5},
    {"name": "{product} Cold Storage", "category": "Service", "inv_min": 15, "inv_max": 50, "roi": "18-25%", "margin": "15-22%", "risk": "Low", "water": "Low", "land_min": 2},
    {"name": "{product} Packaging & Branding", "category": "Retail", "inv_min": 2, "inv_max": 5, "roi": "30-42%", "margin": "25-35%", "risk": "Low", "water": "Low", "land_min": 0.5},
    {"name": "Vermicompost from {product} Waste", "category": "Organic", "inv_min": 1, "inv_max": 3, "roi": "35-50%", "margin": "30-42%", "risk": "Low", "water": "Medium", "land_min": 0.5},
    {"name": "{product}-based Agritourism", "category": "Service", "inv_min": 10, "inv_max": 30, "roi": "28-42%", "margin": "22-35%", "risk": "Medium", "water": "Medium", "land_min": 3},
]

# Also map alternate names/aliases to canonical product keys
PRODUCT_ALIASES = {
    "chilli": "chili", "mirchi": "chili", "pepper": "chili",
    "doodh": "milk", "dudh": "milk",
    "chawal": "rice", "paddy": "rice", "dhan": "rice",
    "gehu": "wheat", "gehun": "wheat", "atta": "wheat",
    "makka": "maize", "corn": "maize", "makkai": "maize",
    "aloo": "potato", "aaloo": "potato",
    "tamatar": "potato",
    "pyaz": "onion", "pyaaz": "onion",
    "haldi": "turmeric",
    "ganna": "sugarcane",
    "kapas": "cotton", "kapasa": "cotton",
    "moongfali": "groundnut", "peanut": "groundnut",
    "nariyal": "coconut",
    "kela": "banana",
    "aam": "mango",
    "chai": "tea",
    "shahad": "honey", "madhu": "honey",
    "khumb": "mushroom",
    "bajra": "millets", "ragi": "millets", "jowar": "millets",
    "dal": "pulses", "chana": "pulses", "moong": "pulses", "urad": "pulses",
    "adrak": "ginger",
    "lahsun": "garlic",
    "sarson": "mustard", "rai": "mustard",
}


class BusinessGenerator:
    """Generates dynamic business ideas from product name using datasets + rule engine."""

    def __init__(self):
        self.crop_data = self._load_csv("crop_production.csv")
        self.product_data = self._load_csv("agri_products.csv")
        self.price_data = self._load_csv("agmarknet_prices.csv")
        self.processing_data = self._load_csv("food_processing_units.csv")
        self.export_data = self._load_csv("export_products.csv")

    def _load_csv(self, filename: str) -> List[Dict]:
        path = DATASETS_DIR / filename
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _normalize_product(self, product: str) -> str:
        p = product.strip().lower()
        return PRODUCT_ALIASES.get(p, p)

    def _get_image_url(self, business_name: str, product: str) -> str:
        query = f"{product}+{business_name.split()[0]}+agriculture".replace(" ", "+")
        seed = int(hashlib.md5(business_name.encode()).hexdigest()[:8], 16) % 1000
        return f"https://source.unsplash.com/featured/600x400/?{query}&sig={seed}"

    def _estimate_monthly_income(self, inv_min: float, inv_max: float, roi_str: str) -> str:
        try:
            roi_parts = roi_str.replace("%", "").split("-")
            roi_avg = (float(roi_parts[0]) + float(roi_parts[1])) / 2 / 100
            inv_avg = (inv_min + inv_max) / 2 * 100000
            monthly = inv_avg * roi_avg / 12
            if monthly >= 100000:
                return f"₹{monthly/100000:.1f} Lakhs"
            return f"₹{monthly/1000:.0f}K"
        except Exception:
            return "₹50K-1L"

    def _get_demand_from_data(self, product: str) -> str:
        for row in self.price_data:
            if row.get("crop", "").lower() == product:
                return row.get("demand_level", "High")
        return "High"

    def _get_export_potential(self, product: str) -> float:
        for row in self.export_data:
            raw = row.get("product_name", "").lower()
            if product in raw:
                try:
                    return float(row.get("growth_rate_percent", 10))
                except (ValueError, TypeError):
                    return 10.0
        return 8.0

    def _generate_blueprint_fields(self, name: str, category: str, product: str) -> Dict[str, Any]:
        """Generates extended implementation details for the Business Details page."""
        # Create a URL-safe ID
        biz_id = f"{product.lower().replace(' ', '-')}-{name.lower().replace(' ', '-').replace('&', 'and')}"
        biz_id = ''.join(c for c in biz_id if c.isalnum() or c == '-')

        return {
            "id": biz_id,
            "description": f"A profitable {category.lower()} venture focusing on converting raw {product.lower()} into high-demand {name.lower()}. This business offers excellent value addition and steady market demand.",
            "marketing_strategy": [
                "B2B partnerships with local distributors",
                "Direct-to-consumer online sales via e-commerce",
                "Tie-ups with regional supermarts and grocery chains",
                "Participation in local agricultural and food expos"
            ],
            "buyers": [
                "Wholesale food distributors",
                "Retail grocery stores and supermarkets",
                "Export agencies",
                "Local restaurants and hospitality businesses"
            ],
            "subsidies": [
                "PM Formalisation of Micro Food Processing Enterprises (PMFME)",
                "Agriculture Infrastructure Fund (AIF)",
                "State-specific Agri-Business Grants"
            ],
            "equipment": [
                f"{product.title()} Processing Machinery",
                "Industrial Packaging Unit",
                "Weighing and Grading Scales",
                "Quality Testing Kit",
                "Storage Bins & Racks"
            ],
            "setup_steps": [
                {"title": "Market Research & Planning", "desc": "Identify target buyers and finalize the product catalog."},
                {"title": "Licensing & Registration", "desc": "Obtain FSSAI, GST, and MSME/Udyam registrations."},
                {"title": "Facility Setup", "desc": "Secure land/shed and install necessary processing machinery."},
                {"title": "Raw Material Sourcing", "desc": f"Establish supply chain for high-quality {product.lower()}."},
                {"title": "Production & Packaging", "desc": "Begin trial runs, quality testing, and final packaging."},
                {"title": "Sales & Distribution", "desc": "Launch product into retail and wholesale channels."}
            ]
        }

    def generate_businesses(self, product: str) -> List[Dict[str, Any]]:
        """Generate all possible businesses for a given product."""
        normalized = self._normalize_product(product)
        businesses = []

        # Get mapped businesses
        mapped = PRODUCT_BUSINESS_MAP.get(normalized, [])
        for biz in mapped:
            demand = self._get_demand_from_data(normalized)
            export_growth = self._get_export_potential(normalized)
            
            biz_data = {
                "name": biz["name"],
                "product": product.title(),
                "category": biz["category"],
                "investment_range": f"₹{biz['inv_min']}-{biz['inv_max']} Lakhs",
                "inv_min_lakhs": biz["inv_min"],
                "inv_max_lakhs": biz["inv_max"],
                "roi": biz["roi"],
                "monthly_income": self._estimate_monthly_income(biz["inv_min"], biz["inv_max"], biz["roi"]),
                "profit_margin": biz["margin"],
                "risk": biz["risk"],
                "demand": demand,
                "water_requirement": biz["water"],
                "min_land_acres": biz["land_min"],
                "export_growth": export_growth,
                "image": self._get_image_url(biz["name"], normalized),
            }
            biz_data.update(self._generate_blueprint_fields(biz["name"], biz["category"], product.title()))
            businesses.append(biz_data)

        # If no mapped businesses, use generics
        if not businesses:
            product_title = product.strip().title()
            for tmpl in GENERIC_BUSINESSES:
                name = tmpl["name"].format(product=product_title)
                biz_data = {
                    "name": name,
                    "product": product_title,
                    "category": tmpl["category"],
                    "investment_range": f"₹{tmpl['inv_min']}-{tmpl['inv_max']} Lakhs",
                    "inv_min_lakhs": tmpl["inv_min"],
                    "inv_max_lakhs": tmpl["inv_max"],
                    "roi": tmpl["roi"],
                    "monthly_income": self._estimate_monthly_income(tmpl["inv_min"], tmpl["inv_max"], tmpl["roi"]),
                    "profit_margin": tmpl["margin"],
                    "risk": tmpl["risk"],
                    "demand": self._get_demand_from_data(normalized),
                    "water_requirement": tmpl["water"],
                    "min_land_acres": tmpl["land_min"],
                    "export_growth": self._get_export_potential(normalized),
                    "image": self._get_image_url(name, normalized),
                }
                biz_data.update(self._generate_blueprint_fields(name, tmpl["category"], product_title))
                businesses.append(biz_data)

        # Also enrich from product data (CSV value-added products)
        for row in self.product_data:
            if row.get("raw_material", "").lower() == normalized and len(businesses) < 20:
                pname = row.get("product_name", "")
                # Skip if already covered
                if any(pname.lower() in b["name"].lower() for b in businesses):
                    continue
                try:
                    mkt = float(row.get("market_size_crore", 500))
                    growth = float(row.get("growth_rate_percent", 10))
                except (ValueError, TypeError):
                    mkt, growth = 500, 10
                demand = "Very High" if mkt > 5000 else "High" if mkt > 1000 else "Medium"
                
                name = f"{pname} Manufacturing"
                category = row.get("processing_type", "Processing")
                biz_data = {
                    "name": name,
                    "product": product.strip().title(),
                    "category": category,
                    "investment_range": "₹3-10 Lakhs",
                    "inv_min_lakhs": 3,
                    "inv_max_lakhs": 10,
                    "roi": f"{int(growth+15)}-{int(growth+30)}%",
                    "monthly_income": self._estimate_monthly_income(3, 10, f"{int(growth+15)}-{int(growth+30)}%"),
                    "profit_margin": f"{int(growth+10)}-{int(growth+20)}%",
                    "risk": "Medium",
                    "demand": demand,
                    "water_requirement": row.get("water_requirement", "Low") if "water_requirement" in row else "Low",
                    "min_land_acres": 0.5,
                    "export_growth": growth,
                    "image": self._get_image_url(pname, normalized),
                }
                biz_data.update(self._generate_blueprint_fields(name, category, product.strip().title()))
                businesses.append(biz_data)

        return businesses


# Singleton instance
_generator = None

def get_generator() -> BusinessGenerator:
    global _generator
    if _generator is None:
        _generator = BusinessGenerator()
    return _generator
