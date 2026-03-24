"""
API routes for the Venture Intelligence Engine.
Includes: business ideas, profit simulation, market trends, buyer finder,
           loan calculator, export opportunities, success stories,
           + smart venture planner (recommend, search, detail).
NOTE: Specific path routes MUST be defined before /venture/{venture_id}
      to avoid FastAPI treating 'business-ideas' etc. as an int path param.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, List, Dict, Any
import json, math, random, hashlib, re
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.db.database import get_db
from app.models.venture_model import AgriVentureDataset
from app.models.agri_business_model import AgriBusiness
from app.models.extra_venture_models import BuyerDirectory, SuccessStory
from app.schemas.venture_schemas import (
    VentureRecommendRequest, VentureCardResponse,
    VentureListResponse, VentureDetailResponse
)

router = APIRouter(tags=["Smart Agri Venture Planner"])

# ─── HELPERS ──────────────────────────────────────────────────
def _parse_json(val):
    if not val:
        return {}
    try:
        return json.loads(val)
    except Exception:
        return {}

def _parse_json_list(val):
    if not val:
        return []
    try:
        return json.loads(val)
    except Exception:
        return []

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))

LOCATION_COORDS = {
    "warangal": (17.9784, 79.5941), "hyderabad": (17.3850, 78.4867),
    "karimnagar": (18.4386, 79.1288), "guntur": (16.3067, 80.4365),
    "nizamabad": (18.6725, 78.0940), "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946), "chennai": (13.0827, 80.2707),
    "mumbai": (19.0760, 72.8777), "pune": (18.5204, 73.8567),
    "nagpur": (21.1458, 79.0882), "vijayawada": (16.5062, 80.6480),
    "khammam": (17.2473, 80.1514), "secunderabad": (17.4399, 78.4983),
    "mangalore": (12.9141, 74.8560), "kurnool": (15.8281, 78.0373),
    "nashik": (19.9975, 73.7898), "coimbatore": (11.0168, 76.9558),
    "delhi": (28.7041, 77.1025), "indore": (22.7196, 75.8577),
    "agra": (27.1767, 78.0081), "kolkata": (22.5726, 88.3639),
    "rajkot": (22.3039, 70.8022), "junagadh": (21.5222, 70.4579),
    "madurai": (9.9252, 78.1198), "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462), "patna": (25.6093, 85.1376),
    "bhopal": (23.2599, 77.4126), "ahmedabad": (23.0225, 72.5714),
}

BUDGET_MAP = {
    "1-3": (1, 3), "3-5": (3, 5), "5-10": (5, 10), "10-20": (10, 20),
}

GOV_SCHEMES = [
    {"name": "PMFME", "benefit": "35% capital subsidy up to ₹10 Lakhs for micro food processing", "max_amount": "₹10 Lakhs", "link": "https://pmfme.mofpi.gov.in"},
    {"name": "MUDRA Loan (PMMY)", "benefit": "Collateral-free loans up to ₹10 Lakhs", "max_amount": "₹10 Lakhs", "link": "https://www.mudra.org.in"},
    {"name": "Agriculture Infrastructure Fund", "benefit": "3% interest subvention + credit guarantee up to ₹2 Cr", "max_amount": "₹2 Crore", "link": "https://agriinfra.dac.gov.in"},
    {"name": "PMEGP", "benefit": "15-35% subsidy for micro enterprises in rural areas", "max_amount": "₹25 Lakhs", "link": "https://www.kviconline.gov.in/pmegp"},
    {"name": "NABARD Agri Fund", "benefit": "Refinance for food processing, cold storage, warehousing", "max_amount": "₹50 Lakhs", "link": "https://www.nabard.org"},
    {"name": "Startup India", "benefit": "Tax exemptions + ₹10,000 Cr Fund-of-Funds access", "max_amount": "₹5 Crore", "link": "https://www.startupindia.gov.in"},
]

# Crop base prices per quintal (simulated)
CROP_BASE_PRICES = {
    "rice": 2200, "wheat": 2100, "maize": 1800, "tomato": 1500, "potato": 1200,
    "onion": 1600, "turmeric": 8500, "chili": 7000, "cotton": 5800,
    "sugarcane": 350, "groundnut": 5200, "soybean": 4000, "banana": 1400,
    "coconut": 2500, "mango": 3000, "millets": 2500, "tea": 18000,
    "coffee": 32000, "pulses": 5500, "chilli": 7000,
}

# Per-crop export data templates
EXPORT_DATA = {
    "rice": {"product_name": "Basmati & Non-Basmati Rice", "price_range": "₹30-120/kg", "demand": "Very High",
             "destinations": [
                 {"country": "Saudi Arabia", "volume_tons": 4200, "value_lakhs": 840, "demand_level": "Very High", "growth_percent": 12.5},
                 {"country": "Iran", "volume_tons": 3800, "value_lakhs": 760, "demand_level": "High", "growth_percent": 8.2},
                 {"country": "Iraq", "volume_tons": 2900, "value_lakhs": 580, "demand_level": "High", "growth_percent": 15.1},
                 {"country": "USA", "volume_tons": 1800, "value_lakhs": 540, "demand_level": "High", "growth_percent": 6.3},
                 {"country": "UK", "volume_tons": 1200, "value_lakhs": 360, "demand_level": "Medium", "growth_percent": 9.8},
             ], "certifications": ["APEDA Registration", "Phytosanitary Certificate", "Fumigation Certificate", "FSSAI License"]},
    "turmeric": {"product_name": "Turmeric Powder & Curcumin", "price_range": "₹150-4000/kg", "demand": "Very High",
                 "destinations": [
                     {"country": "USA", "volume_tons": 3500, "value_lakhs": 1050, "demand_level": "Very High", "growth_percent": 18.5},
                     {"country": "Germany", "volume_tons": 2100, "value_lakhs": 630, "demand_level": "High", "growth_percent": 14.2},
                     {"country": "Japan", "volume_tons": 1800, "value_lakhs": 540, "demand_level": "High", "growth_percent": 11.0},
                     {"country": "UAE", "volume_tons": 1500, "value_lakhs": 450, "demand_level": "High", "growth_percent": 20.3},
                     {"country": "UK", "volume_tons": 900, "value_lakhs": 270, "demand_level": "Medium", "growth_percent": 9.5},
                 ], "certifications": ["Spices Board Certificate", "Organic (NPOP)", "APEDA Registration", "ISO 22000"]},
    "wheat": {"product_name": "Wheat & Wheat Flour", "price_range": "₹20-60/kg", "demand": "High",
              "destinations": [
                  {"country": "Bangladesh", "volume_tons": 5000, "value_lakhs": 1000, "demand_level": "Very High", "growth_percent": 10.0},
                  {"country": "Sri Lanka", "volume_tons": 2000, "value_lakhs": 400, "demand_level": "High", "growth_percent": 8.0},
                  {"country": "Nepal", "volume_tons": 1500, "value_lakhs": 300, "demand_level": "High", "growth_percent": 12.0},
                  {"country": "UAE", "volume_tons": 1200, "value_lakhs": 240, "demand_level": "Medium", "growth_percent": 7.0},
              ], "certifications": ["Phytosanitary Certificate", "FSSAI License", "APEDA Registration"]},
    "mango": {"product_name": "Fresh Mango & Mango Pulp", "price_range": "₹40-300/kg", "demand": "Very High",
              "destinations": [
                  {"country": "UAE", "volume_tons": 3000, "value_lakhs": 900, "demand_level": "Very High", "growth_percent": 15.0},
                  {"country": "USA", "volume_tons": 2000, "value_lakhs": 800, "demand_level": "High", "growth_percent": 12.0},
                  {"country": "UK", "volume_tons": 1500, "value_lakhs": 600, "demand_level": "High", "growth_percent": 10.5},
                  {"country": "Saudi Arabia", "volume_tons": 1000, "value_lakhs": 350, "demand_level": "Medium", "growth_percent": 8.0},
              ], "certifications": ["APEDA Registration", "Phytosanitary Certificate", "VHT (Vapor Heat Treatment)", "GLOBALGAP"]},
    "cotton": {"product_name": "Raw Cotton & Cotton Yarn", "price_range": "₹50-200/kg", "demand": "High",
               "destinations": [
                   {"country": "China", "volume_tons": 8000, "value_lakhs": 2400, "demand_level": "Very High", "growth_percent": 6.0},
                   {"country": "Bangladesh", "volume_tons": 5000, "value_lakhs": 1500, "demand_level": "Very High", "growth_percent": 9.5},
                   {"country": "Vietnam", "volume_tons": 3000, "value_lakhs": 900, "demand_level": "High", "growth_percent": 11.0},
                   {"country": "Pakistan", "volume_tons": 2000, "value_lakhs": 600, "demand_level": "Medium", "growth_percent": 4.0},
               ], "certifications": ["Cotton Association Certificate", "DGFT License", "BIS Standards"]},
    "groundnut": {"product_name": "Groundnut & Groundnut Oil", "price_range": "₹80-250/kg", "demand": "High",
                  "destinations": [
                      {"country": "Indonesia", "volume_tons": 3200, "value_lakhs": 960, "demand_level": "Very High", "growth_percent": 13.0},
                      {"country": "Vietnam", "volume_tons": 2800, "value_lakhs": 840, "demand_level": "High", "growth_percent": 10.5},
                      {"country": "Philippines", "volume_tons": 1500, "value_lakhs": 450, "demand_level": "High", "growth_percent": 8.0},
                      {"country": "Malaysia", "volume_tons": 1200, "value_lakhs": 360, "demand_level": "Medium", "growth_percent": 7.5},
                  ], "certifications": ["APEDA Registration", "Aflatoxin Testing", "FSSAI License"]},
    "banana": {"product_name": "Fresh Banana & Banana Products", "price_range": "₹15-180/kg", "demand": "High",
               "destinations": [
                   {"country": "UAE", "volume_tons": 2500, "value_lakhs": 500, "demand_level": "Very High", "growth_percent": 14.0},
                   {"country": "Saudi Arabia", "volume_tons": 1800, "value_lakhs": 360, "demand_level": "High", "growth_percent": 11.0},
                   {"country": "Oman", "volume_tons": 1200, "value_lakhs": 240, "demand_level": "High", "growth_percent": 9.0},
                   {"country": "Iran", "volume_tons": 800, "value_lakhs": 160, "demand_level": "Medium", "growth_percent": 6.0},
               ], "certifications": ["Phytosanitary Certificate", "APEDA Registration", "FSSAI License"]},
    "sugarcane": {"product_name": "Sugar & Jaggery", "price_range": "₹30-150/kg", "demand": "High",
                  "destinations": [
                      {"country": "Bangladesh", "volume_tons": 6000, "value_lakhs": 1200, "demand_level": "Very High", "growth_percent": 8.0},
                      {"country": "Indonesia", "volume_tons": 4000, "value_lakhs": 800, "demand_level": "High", "growth_percent": 12.0},
                      {"country": "Afghanistan", "volume_tons": 2500, "value_lakhs": 500, "demand_level": "High", "growth_percent": 10.0},
                      {"country": "UAE", "volume_tons": 1500, "value_lakhs": 300, "demand_level": "Medium", "growth_percent": 6.0},
                  ], "certifications": ["BIS Standards", "FSSAI License", "APEDA Registration"]},
    "soybean": {"product_name": "Soybean Meal & Soy Oil", "price_range": "₹40-120/kg", "demand": "High",
                "destinations": [
                    {"country": "Japan", "volume_tons": 3000, "value_lakhs": 900, "demand_level": "Very High", "growth_percent": 9.0},
                    {"country": "South Korea", "volume_tons": 2200, "value_lakhs": 660, "demand_level": "High", "growth_percent": 7.5},
                    {"country": "Vietnam", "volume_tons": 1800, "value_lakhs": 540, "demand_level": "High", "growth_percent": 11.0},
                    {"country": "Thailand", "volume_tons": 1500, "value_lakhs": 450, "demand_level": "Medium", "growth_percent": 8.0},
                ], "certifications": ["Non-GMO Certificate", "FSSAI License", "APEDA Registration"]},
    "tea": {"product_name": "Orthodox & CTC Tea", "price_range": "₹200-2000/kg", "demand": "Very High",
            "destinations": [
                {"country": "Russia", "volume_tons": 4500, "value_lakhs": 2250, "demand_level": "Very High", "growth_percent": 5.0},
                {"country": "UAE", "volume_tons": 2500, "value_lakhs": 1250, "demand_level": "High", "growth_percent": 8.0},
                {"country": "UK", "volume_tons": 2200, "value_lakhs": 1100, "demand_level": "High", "growth_percent": 3.5},
                {"country": "USA", "volume_tons": 1800, "value_lakhs": 900, "demand_level": "High", "growth_percent": 12.0},
            ], "certifications": ["Tea Board License", "FSSAI License", "ISO 22000", "Rainforest Alliance"]},
    "coffee": {"product_name": "Arabica & Robusta Coffee", "price_range": "₹300-1500/kg", "demand": "Very High",
               "destinations": [
                   {"country": "Italy", "volume_tons": 3500, "value_lakhs": 3500, "demand_level": "Very High", "growth_percent": 7.0},
                   {"country": "Germany", "volume_tons": 2800, "value_lakhs": 2800, "demand_level": "Very High", "growth_percent": 6.5},
                   {"country": "Russia", "volume_tons": 2000, "value_lakhs": 2000, "demand_level": "High", "growth_percent": 10.0},
                   {"country": "Belgium", "volume_tons": 1500, "value_lakhs": 1500, "demand_level": "High", "growth_percent": 4.0},
               ], "certifications": ["Coffee Board Certificate", "Fair Trade", "ISO 22000", "Organic (NPOP)"]},
}


# ═══════════════════════════════════════════════════════════════
# INTELLIGENCE ENGINE TAB ENDPOINTS
# These MUST be defined BEFORE /venture/{venture_id}
# ═══════════════════════════════════════════════════════════════

# ─── 1. BUSINESS IDEAS ────────────────────────────────────────
@router.get("/venture/business-ideas")
def get_business_ideas(crop: str = "Rice", category: Optional[str] = None, db: Session = Depends(get_db)):
    """Return business ideas for a crop from AgriBusiness table."""
    query = db.query(AgriBusiness)
    if crop:
        query = query.filter(func.lower(AgriBusiness.crop_type) == crop.lower())
    if category:
        query = query.filter(func.lower(AgriBusiness.category) == category.lower())

    results = query.all()

    ideas = []
    for r in results:
        trending = r.market_demand_level in ("Very High",)
        ideas.append({
            "business_name": r.business_name,
            "crop_type": r.crop_type,
            "category": r.category,
            "market_demand": r.market_demand_level or "Medium",
            "investment": r.investment or "",
            "investment_display": r.investment or "",
            "roi": r.roi or "",
            "monthly_revenue": r.revenue_range or "",
            "profit_margin": r.profit_margin or "",
            "break_even": r.break_even or "",
            "breakeven_period": r.break_even or "",
            "description": f"High-potential {r.category or 'agri'} business based on {r.crop_type}. "
                           f"Estimated ROI of {r.roi or 'N/A'} with {r.market_demand_level or 'good'} market demand.",
            "trending": trending,
        })

    return {"ideas": ideas, "total": len(ideas)}


# ─── 2. PROFIT SIMULATION ────────────────────────────────────
class ProfitSimRequest(BaseModel):
    business_name: str = "General Business"
    crop_quantity_tons: float = 20
    processing_capacity_kg_per_day: float = 500
    labor_cost_monthly: float = 30000
    electricity_cost_monthly: float = 8000
    market_price_per_kg: float = 40
    rent_monthly: float = 10000

@router.post("/venture/profit-simulation")
def profit_simulation(req: ProfitSimRequest, db: Session = Depends(get_db)):
    """Calculate profit projection based on inputs."""
    days_per_month = 25
    output_kg_per_month = req.processing_capacity_kg_per_day * days_per_month

    raw_material_cost_per_kg = req.market_price_per_kg * 0.6
    raw_material_monthly = raw_material_cost_per_kg * output_kg_per_month
    packaging = output_kg_per_month * req.market_price_per_kg * 0.05
    transport = output_kg_per_month * req.market_price_per_kg * 0.08

    monthly_revenue = output_kg_per_month * req.market_price_per_kg

    monthly_costs = {
        "raw_material": round(raw_material_monthly),
        "labor": round(req.labor_cost_monthly),
        "electricity": round(req.electricity_cost_monthly),
        "rent": round(req.rent_monthly),
        "packaging": round(packaging),
        "transport": round(transport),
    }
    total_cost = sum(monthly_costs.values())
    net_profit = monthly_revenue - total_cost
    margin = round((net_profit / monthly_revenue * 100), 1) if monthly_revenue > 0 else 0

    # Estimate investment from DB or default
    biz = db.query(AgriBusiness).filter(
        func.lower(AgriBusiness.business_name) == req.business_name.lower()
    ).first()
    investment = 500000
    if biz and biz.investment:
        try:
            nums = re.findall(r'[\d.]+', biz.investment.replace(',', ''))
            if len(nums) >= 2:
                investment = (float(nums[0]) + float(nums[1])) / 2 * 100000
            elif len(nums) == 1:
                investment = float(nums[0]) * 100000
        except Exception:
            pass

    breakeven_months = round(investment / net_profit) if net_profit > 0 else 999

    monthly_breakdown = []
    for m in range(1, 13):
        ramp = min(1.0, 0.6 + (m - 1) * 0.13)
        rev = round(monthly_revenue * ramp)
        cost = round(total_cost * min(1.0, 0.8 + m * 0.02))
        monthly_breakdown.append({
            "month": f"M{m}",
            "revenue": rev,
            "cost": cost,
            "profit": rev - cost,
        })

    return {
        "business_name": req.business_name,
        "monthly_revenue": round(monthly_revenue),
        "total_monthly_cost": round(total_cost),
        "net_monthly_profit": round(net_profit),
        "profit_margin_percent": margin,
        "breakeven_months": min(breakeven_months, 60),
        "investment_estimated": round(investment),
        "monthly_costs": monthly_costs,
        "monthly_breakdown": monthly_breakdown,
    }


# ─── 3. MARKET TRENDS ────────────────────────────────────────
@router.get("/venture/market-trends")
def get_market_trends(crop: str = "Rice", market: Optional[str] = None):
    """Return simulated market trend data for a crop."""
    crop_lower = crop.lower().strip()
    base_price = CROP_BASE_PRICES.get(crop_lower, 2500)

    seed_val = int(hashlib.md5(crop_lower.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed_val)

    market_name = market or f"{crop.title()} Mandi (Simulated)"

    now = datetime.now()
    trend_data = []
    price = base_price
    for i in range(12):
        date = (now - timedelta(days=(11 - i) * 30)).strftime("%b %Y")
        change = rng.uniform(-0.06, 0.08)
        price = max(base_price * 0.7, min(base_price * 1.4, price * (1 + change)))
        min_p = price * rng.uniform(0.88, 0.95)
        max_p = price * rng.uniform(1.05, 1.15)
        trend_data.append({
            "date": date,
            "price": round(price),
            "min_price": round(min_p),
            "max_price": round(max_p),
        })

    current_price = trend_data[-1]["price"]
    old_price = trend_data[-7]["price"] if len(trend_data) > 6 else trend_data[0]["price"]
    price_change = round((current_price - old_price) / old_price * 100, 1) if old_price else 0

    avg_change = sum(
        (trend_data[i]["price"] - trend_data[i - 1]["price"]) / trend_data[i - 1]["price"]
        for i in range(1, len(trend_data))
    ) / (len(trend_data) - 1)
    predicted = round(current_price * (1 + avg_change))

    demand_forecast = "Rising" if price_change > 3 else "Stable" if price_change > -3 else "Declining"

    insight = (
        f"{crop.title()} prices have {'increased' if price_change > 0 else 'decreased'} by "
        f"{abs(price_change)}% over the last 6 months. "
        f"Current price: ₹{current_price}/qtl. "
        f"{'Strong demand expected next season.' if demand_forecast == 'Rising' else 'Market is stabilizing.'}"
    )

    return {
        "crop": crop,
        "market": market_name,
        "current_price": current_price,
        "price_change_percent": price_change,
        "predicted_next_month": predicted,
        "demand_forecast": demand_forecast,
        "trend_data": trend_data,
        "insight": insight,
    }


# ─── 4. BUYER FINDER ─────────────────────────────────────────
@router.get("/venture/buyers")
def find_buyers(
    product: str = "",
    location: str = "",
    radius: float = 100,
    db: Session = Depends(get_db)
):
    """Find buyers by product and location with distance calculation."""
    query = db.query(BuyerDirectory)

    if product and product.strip():
        search_term = f"%{product.strip().lower()}%"
        query = query.filter(or_(
            BuyerDirectory.product_category.ilike(search_term),
            BuyerDirectory.buyer_name.ilike(search_term),
            BuyerDirectory.business_type.ilike(search_term),
        ))

    user_coords = LOCATION_COORDS.get(location.lower().strip()) if location else None

    if not user_coords and location and location.strip():
        loc_term = f"%{location.strip().lower()}%"
        query = query.filter(or_(
            BuyerDirectory.city.ilike(loc_term),
            BuyerDirectory.state.ilike(loc_term),
            BuyerDirectory.district.ilike(loc_term),
        ))

    results = query.all()

    buyers = []
    for b in results:
        dist = 0
        if user_coords and b.latitude and b.longitude:
            dist = _haversine(user_coords[0], user_coords[1], b.latitude, b.longitude)
            if dist > radius:
                continue
        buyers.append({
            "buyer_name": b.buyer_name,
            "buyer_type": b.business_type or "",
            "product_types": b.product_category or "",
            "location": b.city or "",
            "state": b.state or "",
            "district": b.district or "",
            "annual_capacity": b.annual_capacity or "",
            "phone_number": b.phone_number or "",
            "email": b.email or "",
            "distance": round(dist, 1),
        })

    buyers.sort(key=lambda x: x["distance"])
    return {"buyers": buyers, "total": len(buyers)}


# ─── 5. LOAN CALCULATOR ──────────────────────────────────────
class LoanRequest(BaseModel):
    total_investment: float = 500000
    own_capital: float = 150000
    interest_rate: float = 9.0
    loan_duration_months: int = 60

@router.post("/venture/loan-calculator")
def loan_calculator(req: LoanRequest):
    """Calculate EMI, interest, and repayment schedule."""
    loan_required = req.total_investment - req.own_capital
    if loan_required <= 0:
        return {
            "loan_required": 0, "monthly_emi": 0, "total_interest": 0,
            "total_repayment": 0, "emi_schedule": [], "eligible_schemes": [],
        }

    monthly_rate = req.interest_rate / 100 / 12
    n = req.loan_duration_months

    if monthly_rate > 0:
        emi = loan_required * monthly_rate * (1 + monthly_rate) ** n / ((1 + monthly_rate) ** n - 1)
    else:
        emi = loan_required / n

    total_repayment = emi * n
    total_interest = total_repayment - loan_required

    balance = loan_required
    emi_schedule = []
    for m in range(1, min(13, n + 1)):
        interest_portion = balance * monthly_rate
        principal_portion = emi - interest_portion
        balance = max(0, balance - principal_portion)
        emi_schedule.append({
            "month": f"M{m}",
            "emi": round(emi),
            "principal": round(principal_portion),
            "interest": round(interest_portion),
            "balance": round(balance),
        })

    return {
        "loan_required": round(loan_required),
        "monthly_emi": round(emi),
        "total_interest": round(total_interest),
        "total_repayment": round(total_repayment),
        "emi_schedule": emi_schedule,
        "eligible_schemes": GOV_SCHEMES,
    }


# ─── 6. EXPORT OPPORTUNITIES ─────────────────────────────────
@router.get("/venture/export-opportunities")
def get_export_opportunities(crop: str = "Rice"):
    """Return export data for a crop."""
    crop_lower = crop.lower().strip()
    data = EXPORT_DATA.get(crop_lower)

    if not data:
        seed_val = int(hashlib.md5(crop_lower.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed_val)
        countries = ["UAE", "USA", "UK", "Germany", "Japan", "Saudi Arabia", "Singapore", "Malaysia"]
        rng.shuffle(countries)
        destinations = []
        for i, c in enumerate(countries[:4]):
            vol = rng.randint(500, 4000)
            val = round(vol * rng.uniform(0.2, 0.4))
            destinations.append({
                "country": c, "volume_tons": vol, "value_lakhs": val,
                "demand_level": ["Very High", "High", "High", "Medium"][i],
                "growth_percent": round(rng.uniform(5, 20), 1),
            })
        data = {
            "product_name": f"{crop.title()} (Processed)",
            "price_range": f"₹{rng.randint(30, 200)}-{rng.randint(300, 800)}/kg",
            "demand": "High",
            "destinations": destinations,
            "certifications": ["APEDA Registration", "FSSAI License", "Phytosanitary Certificate"],
        }

    total_value = sum(d["value_lakhs"] for d in data["destinations"])
    avg_growth = sum(d["growth_percent"] for d in data["destinations"]) / len(data["destinations"])
    top = data["destinations"][0]

    insight = (
        f"{data['product_name']} has strong export potential with {len(data['destinations'])} active markets. "
        f"Total export value: ₹{total_value:.0f} Lakhs. Average growth: {avg_growth:.1f}%. "
        f"Top market: {top['country']} (₹{top['value_lakhs']:.0f} Lakhs)."
    )

    return {
        "crop": crop,
        "product_name": data["product_name"],
        "overall_demand": data["demand"],
        "price_range_per_kg": data["price_range"],
        "top_destinations": data["destinations"],
        "certifications": data.get("certifications", []),
        "total_export_value_lakhs": total_value,
        "insight": insight,
    }


# ─── 7. SUCCESS STORIES ──────────────────────────────────────
@router.get("/venture/success-stories")
def get_success_stories(crop: Optional[str] = None, db: Session = Depends(get_db)):
    """Return success stories from the SuccessStory table."""
    query = db.query(SuccessStory)
    if crop and crop.strip():
        crop_term = f"%{crop.strip().lower()}%"
        query = query.filter(or_(
            SuccessStory.crop.ilike(crop_term),
            SuccessStory.business_type.ilike(crop_term),
        ))

    results = query.limit(20).all()

    stories = []
    for s in results:
        stories.append({
            "farmer_name": s.farmer_name or "",
            "location": f"{s.district or ''}, {s.state or ''}".strip(", "),
            "state": s.state or "",
            "crop": s.crop or "",
            "business_type": s.business_type or "",
            "investment": s.investment or "",
            "monthly_revenue": s.monthly_income or "",
            "annual_profit": s.yearly_income or "",
            "story": s.story or "",
            "implementation_steps": s.implementation_steps or "[]",
            "schemes_used": s.government_scheme_used or "[]",
            "contact_phone": s.contact_phone or "",
            "year_started": "",
        })

    return {"stories": stories, "total": len(stories)}


# ═══════════════════════════════════════════════════════════════
# DYNAMIC AGRI-BUSINESS RECOMMENDATION ENGINE
# ═══════════════════════════════════════════════════════════════

class EntrepreneurRecommendRequest(BaseModel):
    product: str = "milk"
    soil_type: Optional[str] = None
    land_size: Optional[float] = None      # acres
    season: Optional[str] = None
    water: Optional[str] = None            # Low / Medium / High
    budget: Optional[float] = None         # in rupees (e.g., 500000)

@router.post("/venture/entrepreneur/recommend")
def entrepreneur_recommend(req: EntrepreneurRecommendRequest):
    """Dynamic agri-business recommendation engine.
    Generates business ideas from product, filters by farm inputs, scores and ranks.
    Guarantees minimum 5 results."""
    from app.services.business_generator import get_generator
    from app.services.recommendation_engine import recommend

    generator = get_generator()
    businesses = generator.generate_businesses(req.product)

    result = recommend(
        businesses=businesses,
        soil_type=req.soil_type,
        land_size=req.land_size,
        season=req.season,
        water=req.water,
        budget=req.budget,
        top_n=10,
    )

    return result


# ═══════════════════════════════════════════════════════════════
# SMART VENTURE PLANNER ENDPOINTS (recommend, search, detail)
# The {venture_id} path endpoint MUST be LAST to avoid intercepting
# /venture/business-ideas, /venture/market-trends, etc.
# ═══════════════════════════════════════════════════════════════

@router.post("/venture/recommend", response_model=VentureListResponse)
def recommend_ventures(req: VentureRecommendRequest, db: Session = Depends(get_db)):
    query = db.query(AgriVentureDataset)

    if req.search_query and req.search_query.strip():
        term = f"%{req.search_query.strip().lower()}%"
        query = query.filter(or_(
            AgriVentureDataset.crop_name.ilike(term),
            AgriVentureDataset.venture_name.ilike(term),
            AgriVentureDataset.business_category.ilike(term),
        ))

    if req.soil_type and req.soil_type.strip():
        query = query.filter(AgriVentureDataset.soil_suitability.ilike(f"%{req.soil_type.strip()}%"))

    if req.water_availability and req.water_availability.strip():
        water = req.water_availability.strip()
        if water == "Low":
            query = query.filter(AgriVentureDataset.water_requirement.in_(["Low"]))
        elif water == "Medium":
            query = query.filter(AgriVentureDataset.water_requirement.in_(["Low", "Medium"]))

    if req.season and req.season.strip():
        query = query.filter(AgriVentureDataset.season_suitability.ilike(f"%{req.season.strip()}%"))

    if req.budget and req.budget.strip():
        budget_range = BUDGET_MAP.get(req.budget.strip())
        if budget_range:
            lo, hi = budget_range
            query = query.filter(AgriVentureDataset.investment_min <= hi, AgriVentureDataset.investment_max >= lo)

    if req.business_type and req.business_type.strip():
        query = query.filter(AgriVentureDataset.business_category.ilike(f"%{req.business_type.strip()}%"))

    results = query.all()
    ventures = [VentureCardResponse(
        id=v.id, crop_name=v.crop_name, venture_name=v.venture_name,
        business_category=v.business_category, demand_level=v.demand_level,
        investment_range=v.investment_range, roi_range=v.roi_range,
        monthly_income=v.monthly_income, profit_margin=v.profit_margin,
        image_url=v.image_url,
    ) for v in results]
    return VentureListResponse(ventures=ventures, total=len(ventures))


@router.get("/venture/search", response_model=VentureListResponse)
def search_ventures(q: str = "", db: Session = Depends(get_db)):
    if not q or len(q) < 2:
        results = db.query(AgriVentureDataset).limit(20).all()
    else:
        term = f"%{q.strip().lower()}%"
        results = db.query(AgriVentureDataset).filter(or_(
            AgriVentureDataset.crop_name.ilike(term),
            AgriVentureDataset.venture_name.ilike(term),
            AgriVentureDataset.business_category.ilike(term),
        )).all()

    ventures = [VentureCardResponse(
        id=v.id, crop_name=v.crop_name, venture_name=v.venture_name,
        business_category=v.business_category, demand_level=v.demand_level,
        investment_range=v.investment_range, roi_range=v.roi_range,
        monthly_income=v.monthly_income, profit_margin=v.profit_margin,
        image_url=v.image_url,
    ) for v in results]
    return VentureListResponse(ventures=ventures, total=len(ventures))


@router.get("/venture/business/{business_id}")
def get_dynamic_business_detail(business_id: str):
    """Fetch the full implementation blueprint for a dynamic Smart Recommendation generated business."""
    from app.services.business_generator import get_generator
    
    # 1. Extract product from the ID slug (e.g., "milk-paneer-production-unit" -> "milk")
    parts = business_id.split("-")
    if not parts:
        raise HTTPException(status_code=400, detail="Invalid business ID format.")
    product = parts[0]
    
    # 2. Re-generate businesses for that product
    generator = get_generator()
    businesses = generator.generate_businesses(product)
    
    # 3. Find the one matching the ID
    for biz in businesses:
        if biz.get("id") == business_id:
            return biz
            
    raise HTTPException(status_code=404, detail="Business blueprint not found.")


# ⚠️ This MUST be the LAST route — path param {venture_id} would
# otherwise match "business-ideas", "market-trends", etc.
@router.get("/venture/{venture_id}", response_model=VentureDetailResponse)
def get_venture_detail(venture_id: int, db: Session = Depends(get_db)):
    v = db.query(AgriVentureDataset).filter(AgriVentureDataset.id == venture_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Venture not found")
    return VentureDetailResponse(
        id=v.id, crop_name=v.crop_name, venture_name=v.venture_name,
        business_category=v.business_category, demand_level=v.demand_level,
        investment_range=v.investment_range, roi_range=v.roi_range,
        monthly_income=v.monthly_income, profit_margin=v.profit_margin,
        soil_suitability=v.soil_suitability or "", water_requirement=v.water_requirement or "",
        season_suitability=v.season_suitability or "", image_url=v.image_url,
        raw_material_required=_parse_json(v.raw_material_required),
        machinery_required=_parse_json_list(v.machinery_required),
        production_capacity=_parse_json(v.production_capacity),
        market_demand=_parse_json(v.market_demand),
        investment_breakdown=_parse_json(v.investment_breakdown),
        implementation_steps=_parse_json_list(v.implementation_steps),
    )
