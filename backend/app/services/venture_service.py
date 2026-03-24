"""
Service layer for the Venture Intelligence Engine.
Connects DB queries with the VentureAnalytics ML engine.
"""
import json
import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.venture_models import (
    BusinessIdea, BuyerDirectory, MarketPrice, ExportStatistic, SuccessStory
)
from app.ml.venture_analytics import VentureAnalytics


class VentureService:

    def __init__(self):
        self.analytics = VentureAnalytics()

    # ─── BUSINESS IDEAS ───────────────────────────────────────
    def get_business_ideas(self, db: Session, crop: Optional[str] = None,
                           category: Optional[str] = None) -> Dict[str, Any]:
        query = db.query(BusinessIdea)
        if crop:
            query = query.filter(func.lower(BusinessIdea.crop_type) == crop.lower())
        if category:
            query = query.filter(func.lower(BusinessIdea.category) == category.lower())
        ideas = query.order_by(BusinessIdea.trending.desc()).all()
        return {"ideas": ideas, "total": len(ideas)}

    # ─── BUYER FINDER ─────────────────────────────────────────
    def find_buyers(self, db: Session, product: str, location: str,
                    radius_km: float = 100) -> Dict[str, Any]:
        buyers = db.query(BuyerDirectory).all()
        # Filter by product type
        matched = []
        product_lower = product.lower().replace(" ", "_")
        for buyer in buyers:
            try:
                products = json.loads(buyer.product_types)
            except (json.JSONDecodeError, TypeError):
                products = []
            if product_lower in [p.lower() for p in products] or "all_products" in [p.lower() for p in products]:
                # Calculate approximate distance using Haversine-like approximation
                loc_coords = self._get_location_coords(location.lower())
                if loc_coords:
                    dist = self._haversine(loc_coords[0], loc_coords[1],
                                           buyer.latitude, buyer.longitude)
                    if dist <= radius_km:
                        buyer_dict = {
                            "id": buyer.id, "buyer_name": buyer.buyer_name,
                            "buyer_type": buyer.buyer_type,
                            "product_types": buyer.product_types,
                            "location": buyer.location, "state": buyer.state,
                            "district": buyer.district,
                            "latitude": buyer.latitude, "longitude": buyer.longitude,
                            "phone_number": buyer.phone_number, "email": buyer.email,
                            "annual_capacity": buyer.annual_capacity,
                            "distance": round(dist, 1),
                        }
                        matched.append(buyer_dict)
                else:
                    # No coords for location, include all matching product
                    buyer_dict = {
                        "id": buyer.id, "buyer_name": buyer.buyer_name,
                        "buyer_type": buyer.buyer_type,
                        "product_types": buyer.product_types,
                        "location": buyer.location, "state": buyer.state,
                        "district": buyer.district,
                        "latitude": buyer.latitude, "longitude": buyer.longitude,
                        "phone_number": buyer.phone_number, "email": buyer.email,
                        "annual_capacity": buyer.annual_capacity,
                        "distance": 0,
                    }
                    matched.append(buyer_dict)

        matched.sort(key=lambda x: x["distance"])
        return {
            "buyers": matched, "total": len(matched),
            "search_location": location, "search_product": product
        }

    # ─── PROFIT SIMULATION ────────────────────────────────────
    def simulate_profit(self, db: Session, params: Dict) -> Dict[str, Any]:
        # Get investment from DB if available
        biz = db.query(BusinessIdea).filter(
            func.lower(BusinessIdea.business_name) == params["business_name"].lower()
        ).first()
        investment = biz.investment_required if biz else 500000
        return self.analytics.simulate_profit(
            business_name=params["business_name"],
            crop_quantity_tons=params["crop_quantity_tons"],
            processing_capacity_kg_per_day=params["processing_capacity_kg_per_day"],
            labor_cost_monthly=params["labor_cost_monthly"],
            electricity_cost_monthly=params["electricity_cost_monthly"],
            market_price_per_kg=params["market_price_per_kg"],
            rent_monthly=params["rent_monthly"],
            investment_required=investment,
        )

    # ─── RISK SCORE ───────────────────────────────────────────
    def get_risk_score(self, db: Session, business_name: str) -> Dict[str, Any]:
        biz = db.query(BusinessIdea).filter(
            func.lower(BusinessIdea.business_name) == business_name.lower()
        ).first()
        if not biz:
            return self.analytics.calculate_risk_score(business_name)
        return self.analytics.calculate_risk_score(
            business_name=biz.business_name,
            market_demand=biz.market_demand,
            investment_required=biz.investment_required,
            crop=biz.crop_type,
            profit_margin=biz.profit_margin or "25-30%",
        )

    # ─── LOAN CALCULATOR ─────────────────────────────────────
    def calculate_loan(self, params: Dict) -> Dict[str, Any]:
        return self.analytics.calculate_loan(**params)

    # ─── MARKET TRENDS ────────────────────────────────────────
    def get_market_trends(self, db: Session, crop: str,
                          market: Optional[str] = None) -> Dict[str, Any]:
        query = db.query(MarketPrice).filter(func.lower(MarketPrice.crop) == crop.lower())
        if market:
            query = query.filter(MarketPrice.market_name.ilike(f"%{market}%"))
        prices = query.order_by(MarketPrice.date).all()

        if not prices:
            return self.analytics.forecast_trend([], crop, market or "All Markets")

        price_data = [
            {"date": p.date, "price_per_quintal": p.price_per_quintal,
             "min_price": p.min_price, "max_price": p.max_price}
            for p in prices
        ]
        market_name = prices[0].market_name if prices else (market or "All Markets")
        return self.analytics.forecast_trend(price_data, crop, market_name)

    # ─── EXPORT OPPORTUNITIES ─────────────────────────────────
    def get_export_opportunities(self, db: Session, crop: str) -> Dict[str, Any]:
        records = db.query(ExportStatistic).filter(
            func.lower(ExportStatistic.crop) == crop.lower()
        ).all()

        if not records:
            return {
                "crop": crop, "product_name": crop, "overall_demand": "Unknown",
                "price_range_per_kg": "N/A", "top_destinations": [],
                "certifications": [], "total_export_value_lakhs": 0,
                "insight": f"No export data available for {crop}."
            }

        product_name = records[0].product_name
        total_value = sum(r.export_value_lakhs for r in records)
        destinations = [
            {"country": r.destination_country, "volume_tons": r.export_volume_tons,
             "value_lakhs": r.export_value_lakhs, "demand_level": r.demand_level,
             "growth_percent": r.growth_percent}
            for r in records
        ]
        destinations.sort(key=lambda x: x["value_lakhs"], reverse=True)

        all_certs = set()
        for r in records:
            try:
                certs = json.loads(r.certifications_required)
                all_certs.update(certs)
            except (json.JSONDecodeError, TypeError):
                pass

        demand_counts = {}
        for r in records:
            demand_counts[r.demand_level] = demand_counts.get(r.demand_level, 0) + 1
        overall_demand = max(demand_counts, key=demand_counts.get) if demand_counts else "Unknown"

        price_range = records[0].price_range_per_kg if records else "N/A"
        avg_growth = sum(r.growth_percent for r in records) / len(records)

        insight = (
            f"{product_name} has strong export potential with {len(records)} active markets. "
            f"Total export value: ₹{total_value:.0f} Lakhs. "
            f"Average growth: {avg_growth:.1f}%. "
            f"Top market: {destinations[0]['country']} (₹{destinations[0]['value_lakhs']:.0f} Lakhs)."
        )

        return {
            "crop": crop, "product_name": product_name,
            "overall_demand": overall_demand, "price_range_per_kg": price_range,
            "top_destinations": destinations, "certifications": sorted(all_certs),
            "total_export_value_lakhs": total_value, "insight": insight,
        }

    # ─── SUCCESS STORIES ──────────────────────────────────────
    def get_success_stories(self, db: Session, crop: Optional[str] = None) -> Dict[str, Any]:
        query = db.query(SuccessStory)
        if crop:
            query = query.filter(func.lower(SuccessStory.crop) == crop.lower())
        stories = query.order_by(SuccessStory.year_started.desc()).all()
        return {"stories": stories, "total": len(stories)}

    # ─── HELPERS ──────────────────────────────────────────────
    def _get_location_coords(self, location: str):
        coords = {
            "warangal": (17.9784, 79.5941), "hyderabad": (17.3850, 78.4867),
            "karimnagar": (18.4386, 79.1288), "guntur": (16.3067, 80.4365),
            "nizamabad": (18.6725, 78.0940), "bangalore": (12.9716, 77.5946),
            "bengaluru": (12.9716, 77.5946), "chennai": (13.0827, 80.2707),
            "mumbai": (19.0760, 72.8777), "pune": (18.5204, 73.8567),
            "nagpur": (21.1458, 79.0882), "vijayawada": (16.5062, 80.6480),
            "khammam": (17.2473, 80.1514), "secunderabad": (17.4399, 78.4983),
            "mangalore": (12.9141, 74.8560), "kurnool": (15.8281, 78.0373),
            "nashik": (19.9975, 73.7898), "coimbatore": (11.0168, 76.9558),
            "madanapalle": (13.5502, 78.5025), "anantapur": (14.6819, 77.6006),
            "nalgonda": (17.0583, 79.2671), "coorg": (12.3375, 75.8069),
            "delhi": (28.7041, 77.1025), "indore": (22.7196, 75.8577),
            "agra": (27.1767, 78.0081), "kolkata": (22.5726, 88.3639),
            "rajkot": (22.3039, 70.8022), "junagadh": (21.5222, 70.4579),
        }
        return coords.get(location.lower().strip())

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        return R * 2 * math.asin(math.sqrt(a))
