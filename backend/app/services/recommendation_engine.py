"""
Recommendation Engine — filters, scores, and ranks agri-business suggestions.
Ensures minimum 5 results via progressive filter relaxation.
"""
from typing import List, Dict, Any, Optional


# Soil compatibility mapping
SOIL_COMPATIBLE = {
    "alluvial": ["Grain Processing", "Dairy", "Bakery", "Processing", "Beverages", "Cereal",
                 "Oil Extraction", "Ready Food", "Feed", "Snacks", "Preserved Food", "Sauce",
                 "Organic", "Export", "Service", "Processed Food", "Retail", "Fiber",
                 "Starch", "Frozen Food", "Agriculture", "Confectionery", "Pharma", "Herbal",
                 "Specialty", "Fuel", "Energy", "Textile", "Trading", "Medical", "Cosmetic",
                 "Superfood", "Cultivation"],
    "black soil": ["Grain Processing", "Spice Processing", "Oil Extraction", "Processing",
                   "Dairy", "Organic", "Export", "Preserved Food", "Sauce", "Snacks",
                   "Feed", "Textile", "Trading", "Processed Food", "Retail", "Service",
                   "Bakery", "Beverages", "Pharma", "Herbal", "Cosmetic", "Specialty"],
    "red soil": ["Spice Processing", "Oil Extraction", "Processing", "Dairy", "Organic",
                 "Export", "Preserved Food", "Snacks", "Beverages", "Pharma", "Herbal",
                 "Cosmetic", "Cultivation", "Superfood", "Service", "Retail", "Processed Food",
                 "Feed", "Fiber", "Textile", "Agriculture", "Confectionery"],
    "sandy": ["Oil Extraction", "Organic", "Processing", "Dairy", "Export", "Spice Processing",
              "Preserved Food", "Snacks", "Feed", "Service", "Retail", "Processed Food",
              "Herbal", "Cosmetic", "Agriculture"],
    "clay": ["Grain Processing", "Dairy", "Processing", "Bakery", "Preserved Food",
             "Organic", "Sauce", "Feed", "Beverages", "Export", "Service"],
    "loamy": ["Grain Processing", "Dairy", "Oil Extraction", "Processing", "Organic",
              "Export", "Spice Processing", "Preserved Food", "Sauce", "Snacks",
              "Bakery", "Beverages", "Pharma", "Herbal", "Cosmetic", "Cultivation",
              "Superfood", "Service", "Retail", "Processed Food", "Feed", "Fiber",
              "Textile", "Agriculture", "Confectionery", "Specialty", "Ready Food"],
}

# Season to compatible categories
SEASON_COMPATIBLE = {
    "kharif": ["Grain Processing", "Spice Processing", "Oil Extraction", "Processing", "Dairy",
               "Organic", "Snacks", "Preserved Food", "Feed", "Textile", "Export", "Sauce",
               "Bakery", "Beverages", "Pharma", "Herbal", "Cosmetic", "Service", "Retail",
               "Processed Food", "Ready Food", "Confectionery", "Cereal", "Starch",
               "Frozen Food", "Agriculture", "Specialty", "Fuel", "Energy", "Trading",
               "Medical", "Superfood", "Cultivation", "Fiber"],
    "rabi": ["Grain Processing", "Oil Extraction", "Processing", "Dairy", "Bakery",
             "Organic", "Snacks", "Preserved Food", "Feed", "Export", "Sauce",
             "Beverages", "Spice Processing", "Pharma", "Herbal", "Cosmetic", "Service",
             "Retail", "Processed Food", "Ready Food", "Confectionery", "Cereal",
             "Starch", "Agriculture", "Specialty", "Textile", "Trading", "Medical"],
    "summer": ["Dairy", "Processing", "Organic", "Export", "Beverages", "Snacks",
               "Preserved Food", "Service", "Retail", "Bakery", "Confectionery", "Pharma",
               "Herbal", "Cosmetic", "Cultivation", "Superfood", "Ready Food", "Feed",
               "Oil Extraction", "Processed Food", "Grain Processing", "Spice Processing",
               "Sauce", "Cereal", "Starch", "Frozen Food", "Agriculture", "Specialty",
               "Fiber", "Fuel", "Energy", "Textile", "Trading", "Medical"],
}

WATER_LEVELS = {"low": 1, "medium": 2, "high": 3}


def _parse_roi_avg(roi_str: str) -> float:
    """Parse ROI string like '30-42%' and return average as decimal."""
    try:
        parts = roi_str.replace("%", "").split("-")
        return (float(parts[0]) + float(parts[1])) / 2 / 100
    except Exception:
        return 0.25


def _parse_margin_avg(margin_str: str) -> float:
    try:
        parts = margin_str.replace("%", "").split("-")
        return (float(parts[0]) + float(parts[1])) / 2 / 100
    except Exception:
        return 0.20


def score_business(biz: Dict[str, Any]) -> float:
    """
    ML-style scoring:
    score = 0.35 * demand_score + 0.25 * profit_margin + 0.20 * export_potential + 0.20 * risk_inverse
    """
    demand_map = {"Very High": 1.0, "High": 0.75, "Medium": 0.5, "Low": 0.25}
    risk_map = {"Low": 1.0, "Medium": 0.6, "High": 0.3}

    demand_score = demand_map.get(biz.get("demand", "Medium"), 0.5)
    profit_margin = _parse_margin_avg(biz.get("profit_margin", "20-30%"))
    export_growth = min(biz.get("export_growth", 10) / 50, 1.0)  # normalize to 0-1
    risk_inverse = risk_map.get(biz.get("risk", "Medium"), 0.5)

    score = (0.35 * demand_score +
             0.25 * (profit_margin / 0.5) +  # normalize margin (max ~50%)
             0.20 * export_growth +
             0.20 * risk_inverse)

    return round(min(score, 1.0) * 100, 1)


def filter_businesses(
    businesses: List[Dict],
    soil_type: Optional[str] = None,
    land_size: Optional[float] = None,
    season: Optional[str] = None,
    water: Optional[str] = None,
    budget: Optional[float] = None,
) -> tuple:
    """
    Filter businesses by farm inputs. Returns (filtered_list, filters_applied, filters_relaxed).
    If < 5 results, progressively relaxes filters.
    """
    filters_applied = []
    filters_relaxed = []

    budget_lakhs = budget / 100000 if budget and budget > 100 else budget  # handle raw rupees vs lakhs

    def apply_filters(skip_filters=None):
        skip = skip_filters or set()
        result = list(businesses)

        if soil_type and "soil" not in skip:
            soil_key = soil_type.strip().lower()
            compatible = SOIL_COMPATIBLE.get(soil_key)
            if compatible:
                result = [b for b in result if b.get("category") in compatible]
                if "soil" not in [f[0] for f in filters_applied]:
                    filters_applied.append(("soil", soil_type))

        if season and "season" not in skip:
            s_key = season.strip().lower()
            compatible = SEASON_COMPATIBLE.get(s_key, [])
            if compatible:
                result = [b for b in result if b.get("category") in compatible]
                if "season" not in [f[0] for f in filters_applied]:
                    filters_applied.append(("season", season))

        if water and "water" not in skip:
            w_level = WATER_LEVELS.get(water.strip().lower(), 2)
            water_map = {"Low": 1, "Medium": 2, "High": 3}
            result = [b for b in result if water_map.get(b.get("water_requirement", "Low"), 1) <= w_level]
            if "water" not in [f[0] for f in filters_applied]:
                filters_applied.append(("water", water))

        if land_size and "land" not in skip:
            result = [b for b in result if b.get("min_land_acres", 0) <= land_size]
            if "land" not in [f[0] for f in filters_applied]:
                filters_applied.append(("land", f"{land_size} acres"))

        if budget_lakhs and "budget" not in skip:
            result = [b for b in result if b.get("inv_min_lakhs", 0) <= budget_lakhs]
            if "budget" not in [f[0] for f in filters_applied]:
                filters_applied.append(("budget", f"₹{budget_lakhs} Lakhs"))

        return result

    # Try with all filters
    filtered = apply_filters()

    # Progressive relaxation if < 5 results
    relaxation_order = ["soil", "water", "budget", "season", "land"]
    skip = set()
    for filt in relaxation_order:
        if len(filtered) >= 5:
            break
        skip.add(filt)
        filters_relaxed.append(filt)
        filters_applied = []
        filtered = apply_filters(skip)

    return filtered, filters_applied, filters_relaxed


def recommend(
    businesses: List[Dict],
    soil_type: Optional[str] = None,
    land_size: Optional[float] = None,
    season: Optional[str] = None,
    water: Optional[str] = None,
    budget: Optional[float] = None,
    top_n: int = 10,
) -> Dict[str, Any]:
    """
    Full recommendation pipeline: filter → score → rank → return top N.
    Guarantees minimum 5 results.
    """
    filtered, filters_applied, filters_relaxed = filter_businesses(
        businesses, soil_type, land_size, season, water, budget
    )

    # Score each business
    for biz in filtered:
        biz["score"] = score_business(biz)

    # Sort by score descending
    filtered.sort(key=lambda x: x["score"], reverse=True)

    # Take top N
    top = filtered[:top_n]

    return {
        "recommendations": top,
        "total": len(top),
        "total_generated": len(businesses),
        "filters_applied": [{"type": f[0], "value": f[1]} for f in filters_applied],
        "filters_relaxed": filters_relaxed,
    }
