import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Sample dataset
data = pd.DataFrame({
    'transport_km':[10,20,30,15,40,25],
    'transport_mode':['car','bus','train','car','bike','walk'],
    'electricity_kwh':[200,400,300,250,500,350],
    'renewable_energy':[0,1,0,0,1,0],
    'food_meat':[5,6,3,4,7,2],
    'food_dairy':[2,3,1,2,3,1],
    'food_plant':[5,6,7,5,6,7],
    'waste_kg':[5,7,6,8,10,9],
    'recycling_score':[50,70,60,40,90,80],
    'water_liters':[100,120,90,110,130,95],
    'shopping_spend':[1000,2000,1500,1800,2200,1200],
    'carbon_footprint':[2.5,4.0,3.5,3.0,5.0,4.2]
})

# One-hot encode transport_mode
X = pd.get_dummies(data.drop(columns=['carbon_footprint']), drop_first=True)
y = data['carbon_footprint']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train,y_train)

joblib.dump(model,'model/random_forest.joblib')
print("✅ Model saved")
