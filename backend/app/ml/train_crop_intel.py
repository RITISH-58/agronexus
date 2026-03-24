import pandas as pd
import numpy as np
import random
import os
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

VALID_CROPS = ["rice", "cotton", "groundnut", "maize", "wheat", "sugarcane", "tomato", "potato"]

def generate_dataset(num_rows=10000):
    data = []
    
    for _ in range(num_rows):
        crop = random.choice(VALID_CROPS)
        previous_crop = random.choice(VALID_CROPS)
        
        # Base Soil Nutrients influenced by previous_crop
        # cotton -> reduces N, groundnut -> increases N
        if previous_crop == "cotton":
            n = random.randint(20, 40)
        elif previous_crop == "groundnut":
            n = random.randint(60, 90)
        else:
            n = random.randint(40, 70)
            
        p = random.randint(20, 60)
        k = random.randint(20, 60)
        ph = round(random.uniform(5.5, 7.5), 1)
        
        # Soil type derivation based on combinations (simplified logic for synthetic data)
        if crop == "rice" and random.random() < 0.7:
            soil_type = "high_nitrogen"
        elif crop in ["groundnut", "potato"] and random.random() < 0.7:
            soil_type = "low_nitrogen"
        else:
            soil_type = random.choice(["high_nitrogen", "low_nitrogen", "balanced"])
            
        temperature = round(random.uniform(20.0, 35.0), 1)
        humidity = random.randint(40, 90)
        
        # Yield Logic
        base_yields = {
            "rice": 5.0, "cotton": 4.0, "groundnut": 3.5,
            "maize": 6.0, "wheat": 4.5, "sugarcane": 30.0,
            "tomato": 15.0, "potato": 10.0
        }
        
        target_yield = base_yields[crop]
        # Soil modifier
        if soil_type == "balanced":
            target_yield += 0.5
        elif soil_type == "low_nitrogen" and crop == "rice":
            target_yield -= 0.5
        elif soil_type == "high_nitrogen" and crop == "groundnut":
            target_yield -= 0.5
            
        # Add slight random noise to yield
        target_yield += random.uniform(-0.3, 0.3)
        target_yield = max(0.1, round(target_yield, 2))
        
        # Market Price Logic
        base_prices = {
            "rice": 2200, "cotton": 6700, "groundnut": 5700,
            "maize": 1800, "wheat": 2400, "sugarcane": 300,
            "tomato": 1500, "potato": 1200
        }
        
        target_price = base_prices[crop] + random.randint(-400, 400)
        if target_price < 200: target_price = 200 # safeguard
        
        data.append([
            previous_crop, crop, soil_type, temperature, humidity, 
            target_yield, target_price, n, p, k, ph
        ])
        
    df = pd.DataFrame(data, columns=[
        "previous_crop", "crop", "soil_type", "temperature", "humidity",
        "yield", "market_price", "nitrogen", "phosphorus", "potassium", "ph"
    ])
    
    return df

def train_and_save():
    print("Generating 10000 rows of synthetic dataset...")
    df = generate_dataset(10000)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, 'crop_dataset.csv'), index=False)
    
    print("Encoding categorical features...")
    le_crop = LabelEncoder()
    le_prev = LabelEncoder()
    le_soil = LabelEncoder()
    
    # Fit on all possible crops exactly
    le_crop.fit(VALID_CROPS)
    le_prev.fit(VALID_CROPS)
    le_soil.fit(["high_nitrogen", "low_nitrogen", "balanced"])
    
    X = pd.DataFrame()
    X['crop_encoded'] = le_crop.transform(df['crop'])
    X['prev_crop_encoded'] = le_prev.transform(df['previous_crop'])
    
    y_yield = df['yield']
    y_price = df['market_price']
    y_soil = le_soil.transform(df['soil_type'])
    
    print("Training Yield Model (RandomForestRegressor)...")
    yield_model = RandomForestRegressor(n_estimators=50, random_state=42)
    yield_model.fit(X, y_yield)
    
    print("Training Price Model (RandomForestRegressor)...")
    price_model = RandomForestRegressor(n_estimators=50, random_state=42)
    price_model.fit(X, y_price)
    
    print("Training Soil Model (RandomForestClassifier)...")
    soil_model = RandomForestClassifier(n_estimators=50, random_state=42)
    soil_model.fit(X, y_soil)
    
    models_dir = os.path.join(base_dir, '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    print("Saving models...")
    joblib.dump(yield_model, os.path.join(models_dir, 'yield_model.pkl'))
    joblib.dump(price_model, os.path.join(models_dir, 'price_model.pkl'))
    joblib.dump(soil_model, os.path.join(models_dir, 'soil_model.pkl'))
    joblib.dump(le_crop, os.path.join(models_dir, 'le_crop.pkl'))
    joblib.dump(le_prev, os.path.join(models_dir, 'le_prev.pkl'))
    joblib.dump(le_soil, os.path.join(models_dir, 'le_soil.pkl'))
    
    print(f"Training Complete. Models saved to {models_dir}")

if __name__ == "__main__":
    train_and_save()
