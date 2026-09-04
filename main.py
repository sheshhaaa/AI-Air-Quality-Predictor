from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from air_quality import get_air_quality
from aqi_model import predict_aqi, simulate_aqi
from ai_explanation import get_ai_explanation


app = FastAPI(title="AI Air Quality Predictor")


# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# -----------------------------------
# HOME
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Air Quality Predictor is running"
    }


# -----------------------------------
# AQI PREDICTION
# -----------------------------------

@app.get("/predict")
def predict(city: str):

    data = get_air_quality(city)

    if data is None:
        return {
            "error": "City not found"
        }

    # Predict AQI
    aqi = predict_aqi(data)

    # Generate AI explanation
    explanation = get_ai_explanation(
        city,
        aqi,
        data
    )

    return {
        "city": data["city"],
        "aqi": aqi,

        "air_quality": {
            "pm10": data["pm10"],
            "pm2_5": data["pm2_5"],
            "carbon_monoxide": data["carbon_monoxide"],
            "nitrogen_dioxide": data["nitrogen_dioxide"],
            "sulphur_dioxide": data["sulphur_dioxide"],
            "ozone": data["ozone"]
        },

        "explanation": explanation
    }


# -----------------------------------
# WHAT-IF SIMULATOR
# -----------------------------------

@app.get("/simulate")
def simulate(
    city: str,
    pm10: float = None,
    pm2_5: float = None,
    carbon_monoxide: float = None,
    nitrogen_dioxide: float = None,
    sulphur_dioxide: float = None,
    ozone: float = None
):

    data = get_air_quality(city)

    if data is None:
        return {
            "error": "City not found"
        }

    # Create changes dictionary
    changes = {}

    if pm10 is not None:
        changes["pm10"] = pm10

    if pm2_5 is not None:
        changes["pm2_5"] = pm2_5

    if carbon_monoxide is not None:
        changes["carbon_monoxide"] = carbon_monoxide

    if nitrogen_dioxide is not None:
        changes["nitrogen_dioxide"] = nitrogen_dioxide

    if sulphur_dioxide is not None:
        changes["sulphur_dioxide"] = sulphur_dioxide

    if ozone is not None:
        changes["ozone"] = ozone

    # Current AQI
    current_aqi = predict_aqi(data)

    # Simulated AQI
    simulated_aqi = simulate_aqi(
        data,
        changes
    )

    return {
        "city": data["city"],
        "current_aqi": current_aqi,
        "simulated_aqi": simulated_aqi,
        "changes": changes
    }