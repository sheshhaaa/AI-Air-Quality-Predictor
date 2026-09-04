import numpy as np
from sklearn.ensemble import RandomForestRegressor


# -----------------------------------
# SAMPLE TRAINING DATA
# -----------------------------------

X = np.array([
    [20, 10, 200, 10, 5, 40],
    [40, 20, 300, 20, 10, 50],
    [60, 30, 400, 30, 15, 60],
    [80, 40, 500, 40, 20, 70],
    [100, 50, 600, 50, 25, 80],
    [120, 60, 700, 60, 30, 90],
    [150, 80, 800, 70, 40, 100],
    [180, 100, 900, 80, 50, 110]
])


# -----------------------------------
# TARGET AQI VALUES
# -----------------------------------

y = np.array([
    35,
    55,
    75,
    95,
    120,
    145,
    175,
    210
])


# -----------------------------------
# RANDOM FOREST MODEL
# -----------------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# -----------------------------------
# AQI PREDICTION
# -----------------------------------

def predict_aqi(data):

    features = np.array([[
        data["pm10"],
        data["pm2_5"],
        data["carbon_monoxide"],
        data["nitrogen_dioxide"],
        data["sulphur_dioxide"],
        data["ozone"]
    ]])

    prediction = model.predict(features)

    # AQI should not be negative
    prediction = max(0, prediction[0])

    return round(float(prediction), 2)


# -----------------------------------
# WHAT-IF AQI SIMULATOR
# -----------------------------------

def simulate_aqi(data, changes=None):

    simulated_data = data.copy()

    if changes:

        if "pm10" in changes:
            simulated_data["pm10"] = changes["pm10"]

        if "pm2_5" in changes:
            simulated_data["pm2_5"] = changes["pm2_5"]

        if "carbon_monoxide" in changes:
            simulated_data["carbon_monoxide"] = changes["carbon_monoxide"]

        if "nitrogen_dioxide" in changes:
            simulated_data["nitrogen_dioxide"] = changes["nitrogen_dioxide"]

        if "sulphur_dioxide" in changes:
            simulated_data["sulphur_dioxide"] = changes["sulphur_dioxide"]

        if "ozone" in changes:
            simulated_data["ozone"] = changes["ozone"]

    return predict_aqi(simulated_data)