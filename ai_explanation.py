def get_ai_explanation(city, aqi, data=None):
    """
    Generate AI-style air quality advice based on AQI
    and available pollutant information.
    """

    # -----------------------------
    # AQI HEALTH CATEGORY
    # -----------------------------

    if aqi <= 50:
        quality = "GOOD"
        impact = "Air quality is good and poses little or no health risk."

        precautions = [
            "Normal outdoor activities are safe.",
            "Continue normal exercise and daily activities.",
            "Avoid unnecessary exposure to smoke.",
        ]

        activity = "Outdoor activities are generally safe."

    elif aqi <= 100:
        quality = "MODERATE"
        impact = (
            "Air quality is generally acceptable, but sensitive people "
            "may experience minor health problems."
        )

        precautions = [
            "Outdoor activities are generally acceptable.",
            "Sensitive people should reduce prolonged outdoor activity.",
            "Check AQI before long outdoor activities.",
            "Avoid heavily congested roads when possible.",
            "Avoid smoking and indoor burning.",
        ]

        activity = (
            "Outdoor activity is generally acceptable. "
            "Sensitive people should take breaks if needed."
        )

    elif aqi <= 150:
        quality = "UNHEALTHY FOR SENSITIVE GROUPS"
        impact = (
            "Sensitive groups may experience health effects, "
            "while the general population is less likely to be affected."
        )

        precautions = [
            "Reduce prolonged or intense outdoor exercise.",
            "Children and older adults should limit prolonged outdoor exposure.",
            "Avoid busy roads and heavily polluted areas.",
            "Keep indoor pollution sources low.",
        ]

        activity = (
            "Limit prolonged outdoor activity, especially for sensitive groups."
        )

    elif aqi <= 200:
        quality = "UNHEALTHY"
        impact = (
            "Some people may experience health effects. "
            "Sensitive groups may experience more serious effects."
        )

        precautions = [
            "Avoid prolonged outdoor activity.",
            "Reduce strenuous outdoor exercise.",
            "Sensitive people should stay indoors as much as practical.",
            "Avoid busy roads and visible smoke.",
            "Keep windows closed when outdoor pollution is high.",
        ]

        activity = "Avoid strenuous outdoor activities."

    elif aqi <= 300:
        quality = "VERY UNHEALTHY"
        impact = "Health risks are increased for everyone."

        precautions = [
            "Avoid outdoor activities whenever possible.",
            "Stay indoors during peak pollution periods.",
            "Avoid strenuous exercise outdoors.",
            "Keep windows and doors closed when pollution is high.",
            "Follow local air-quality advisories.",
        ]

        activity = "Avoid outdoor activity until air quality improves."

    else:
        quality = "HAZARDOUS"
        impact = "Health risks are very high for everyone."

        precautions = [
            "Avoid outdoor activity.",
            "Stay indoors as much as possible.",
            "Keep windows and doors closed.",
            "Avoid strenuous physical activity.",
            "Follow official health instructions.",
        ]

        activity = "Avoid outdoor activity until air quality improves."

    # -----------------------------
    # POLLUTANT INFORMATION
    # -----------------------------

    pollutant_text = ""

    if data:

        pm25 = data.get("pm2_5")
        pm10 = data.get("pm10")
        co = data.get("carbon_monoxide")
        no2 = data.get("nitrogen_dioxide")

        pollutant_text = f"""
POLLUTANT LEVELS:

PM2.5: {pm25 if pm25 is not None else "N/A"} µg/m³
PM10: {pm10 if pm10 is not None else "N/A"} µg/m³
CO: {co if co is not None else "N/A"} µg/m³
NO₂: {no2 if no2 is not None else "N/A"}
"""

    # -----------------------------
    # BEST TIME TO GO OUTSIDE
    # -----------------------------

    if aqi <= 50:
        best_time = "Any time of the day is generally suitable for outdoor activities."

    elif aqi <= 100:
        best_time = (
            "Morning or periods with lower traffic are generally better "
            "for outdoor activities."
        )

    elif aqi <= 150:
        best_time = (
            "Choose shorter outdoor periods when pollution is lower, "
            "and avoid busy traffic hours."
        )

    elif aqi <= 200:
        best_time = (
            "Avoid outdoor activities during peak pollution and traffic hours. "
            "If necessary, choose the shortest possible outdoor period."
        )

    else:
        best_time = (
            "Outdoor activity should be avoided until air quality improves."
        )

    # -----------------------------
    # WHAT-IF SIMULATION
    # -----------------------------

    what_if = f"""
WHAT-IF SIMULATION:

Current AQI: {aqi}

If pollution increases:
- AQI may move into a higher health-risk category.
- Outdoor activity should be reduced.
- Sensitive groups may need to remain indoors.

If pollution decreases:
- Air quality may move into a safer category.
- More outdoor activities may become suitable.
- Health risks are expected to decrease.
"""

    # -----------------------------
    # FINAL AI EXPLANATION
    # -----------------------------

    precaution_text = "\n".join(
        f"* {item}" for item in precautions
    )

    return f"""🤖 AI AIR QUALITY ANALYSIS

AIR QUALITY: {quality}

City: {city}
AQI: {aqi}

HEALTH IMPACT:
{impact}

{pollutant_text}

PRECAUTIONS:

{precaution_text}

OUTDOOR ACTIVITY:
{activity}

BEST TIME TO GO OUTSIDE:
{best_time}

{what_if}
"""