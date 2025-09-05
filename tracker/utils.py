import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__),"../model/random_forest.joblib")
model = joblib.load(MODEL_PATH)

def predict_footprint(entry):
    df = pd.DataFrame([{
        'transport_km': entry.transport_km,
        'electricity_kwh': entry.electricity_kwh,
        'renewable_energy': int(entry.renewable_energy),
        'food_meat': entry.food_meat,
        'food_dairy': entry.food_dairy,
        'food_plant': entry.food_plant,
        'waste_kg': entry.waste_kg,
        'recycling_score': entry.recycling_score,
        'water_liters': entry.water_liters,
        'shopping_spend': entry.shopping_spend,
        'transport_mode_bus': 1 if entry.transport_mode=='bus' else 0,
        'transport_mode_bike': 1 if entry.transport_mode=='bike' else 0,
        'transport_mode_car': 1 if entry.transport_mode=='car' else 0,
        'transport_mode_train': 1 if entry.transport_mode=='train' else 0,
    }])
    # Align columns
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    df = df[model.feature_names_in_]
    return model.predict(df)[0]

def get_suggestions(entry, prediction):
    tips = []

    # Transport
    if entry.transport_km > 20 or entry.transport_mode.lower() in ['car', 'diesel car', 'petrol car']:
        tips.append("Use public transport, bike or walk to reduce emissions.")
    if entry.transport_mode.lower() in ['diesel car', 'petrol car']:
        tips.append("Switch to a fuel-efficient or electric vehicle if possible.")
    
    # Electricity
    if entry.electricity_kwh > 300:
        tips.append("Consider energy-saving appliances & LED bulbs.")
    if entry.renewable_energy < 40:  
        tips.append("Switch to renewable energy providers if available in your area.")
    if entry.electricity_kwh > 500:
        tips.append("Unplug devices when not in use to cut standby power.")

    # Food
    if entry.food_meat > 5:
        tips.append("Reduce meat intake; try plant-based meals.")
    if entry.food_dairy > 7:
        tips.append("Swap dairy with plant-based alternatives like oat or soy milk.")
    if entry.food_plant < 5:
        tips.append("Increase vegetables, legumes, and grains in your diet.")

    # Waste
    if entry.waste_kg > 8 or entry.recycling_score < 50:
        tips.append("Recycle more & reduce waste.")
    if entry.waste_kg > 12:
        tips.append("Try composting organic waste to lower landfill impact.")
    
    # Water
    if entry.water_liters > 150:
        tips.append("Shorten showers and fix leaks to save water.")
    
    # Shopping
    if entry.shopping_spend > 2000:
        tips.append("Buy second-hand or sustainable products.")
    if entry.shopping_spend > 3000:
        tips.append("Avoid fast fashion; choose quality items that last longer.")

    # General lifestyle
    if prediction > 500:
        tips.append("Your footprint is above average; set monthly reduction goals.")
    if prediction < 200:
        tips.append("Great job! Keep up the sustainable lifestyle 🌱.")

    return tips

