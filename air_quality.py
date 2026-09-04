import requests


def get_air_quality(city):
    # -----------------------------
    # 1. Find city location
    # -----------------------------

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(geo_url, params=geo_params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    city_name = data["results"][0].get("name", city)

    # -----------------------------
    # 2. Get current air quality
    # -----------------------------

    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    air_params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone"
        ),

        # Hourly data will help with
        # pollutant prediction and best-time analysis
        "hourly": (
            "pm10,"
            "pm2_5,"
            "carbon_monoxide,"
            "nitrogen_dioxide,"
            "sulphur_dioxide,"
            "ozone"
        ),

        "forecast_days": 1,
        "timezone": "auto"
    }

    response = requests.get(
        air_url,
        params=air_params,
        timeout=10
    )

    response.raise_for_status()

    air_data = response.json()

    current = air_data.get("current", {})

    # -----------------------------
    # 3. Extract current pollutants
    # -----------------------------

    pm25 = current.get("pm2_5")
    pm10 = current.get("pm10")
    carbon_monoxide = current.get("carbon_monoxide")
    nitrogen_dioxide = current.get("nitrogen_dioxide")
    sulphur_dioxide = current.get("sulphur_dioxide")
    ozone = current.get("ozone")

    # -----------------------------
    # 4. Return air-quality data
    # -----------------------------

    return {
        "city": city_name,

        "latitude": latitude,
        "longitude": longitude,

        "pm10": pm10,
        "pm2_5": pm25,

        "carbon_monoxide": carbon_monoxide,
        "nitrogen_dioxide": nitrogen_dioxide,
        "sulphur_dioxide": sulphur_dioxide,
        "ozone": ozone,

        # Hourly prediction data
        "hourly": air_data.get("hourly", {}),

        "timezone": air_data.get("timezone")
    }