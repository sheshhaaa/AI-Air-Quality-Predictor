const BACKEND_URL = "http://localhost:8000";

let currentCity = "";


// ==========================================
// CHECK AQI
// ==========================================

async function checkAQI() {

    const city = document.getElementById("city").value.trim();

    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    currentCity = city;

    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const error = document.getElementById("error");

    loading.classList.remove("hidden");
    result.classList.add("hidden");
    error.classList.add("hidden");

    try {

        const response = await fetch(
            `${BACKEND_URL}/predict?city=${encodeURIComponent(city)}`
        );

        if (!response.ok) {
            throw new Error("Backend error: " + response.status);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }


        // ==================================
        // CITY
        // ==================================

        document.getElementById("cityName").textContent =
            data.city;


        // ==================================
        // AQI
        // ==================================

        document.getElementById("aqi").textContent =
            data.aqi;

        setAQIStatus(Number(data.aqi));


        // ==================================
        // POLLUTANTS
        // ==================================

        document.getElementById("pm25").textContent =
            formatValue(data.air_quality.pm2_5);

        document.getElementById("pm10").textContent =
            formatValue(data.air_quality.pm10);

        document.getElementById("co").textContent =
            formatValue(data.air_quality.carbon_monoxide);

        document.getElementById("no2").textContent =
            formatValue(data.air_quality.nitrogen_dioxide);

        document.getElementById("so2").textContent =
            formatValue(data.air_quality.sulphur_dioxide);

        document.getElementById("ozone").textContent =
            formatValue(data.air_quality.ozone);


        // ==================================
        // AI ADVICE
        // ==================================

        document.getElementById("explanation").textContent =
            data.explanation;


        // ==================================
        // SET CURRENT PM2.5
        // ==================================

        document.getElementById("pm25Input").value =
            data.air_quality.pm2_5;


        // ==================================
        // SHOW RESULTS
        // ==================================

        result.classList.remove("hidden");


        // ==================================
        // GET BEST TIME
        // ==================================

        getBestTime(city);

    }

    catch (err) {

        console.error("Connection error:", err);

        error.textContent =
            "Cannot connect to backend: " + err.message;

        error.classList.remove("hidden");

    }

    finally {

        loading.classList.add("hidden");

    }
}


// ==========================================
// FORMAT POLLUTANT VALUE
// ==========================================

function formatValue(value) {

    if (value === null || value === undefined) {
        return "--";
    }

    return Number(value).toFixed(2);
}


// ==========================================
// AQI STATUS
// ==========================================

function setAQIStatus(aqi) {

    const status =
        document.getElementById("aqiStatus");


    if (aqi <= 50) {

        status.textContent = "GOOD";
        status.style.color = "#00e676";

    }

    else if (aqi <= 100) {

        status.textContent = "MODERATE";
        status.style.color = "#ffeb3b";

    }

    else if (aqi <= 150) {

        status.textContent =
            "UNHEALTHY FOR SENSITIVE GROUPS";

        status.style.color = "#ff9800";

    }

    else if (aqi <= 200) {

        status.textContent = "UNHEALTHY";
        status.style.color = "#ff5252";

    }

    else if (aqi <= 300) {

        status.textContent = "VERY UNHEALTHY";
        status.style.color = "#ce93d8";

    }

    else {

        status.textContent = "HAZARDOUS";
        status.style.color = "#ff1744";

    }
}


// ==========================================
// BEST TIME TO GO OUTSIDE
// ==========================================

async function getBestTime(city) {

    const bestTime =
        document.getElementById("bestTime");

    bestTime.textContent =
        "Analyzing predicted air quality...";


    try {

        const response = await fetch(
            `${BACKEND_URL}/best-time?city=${encodeURIComponent(city)}`
        );

        if (!response.ok) {

            throw new Error(
                "Best-time service unavailable"
            );
        }

        const data = await response.json();

        if (data.error) {

            bestTime.textContent =
                data.error;

            return;
        }


        bestTime.innerHTML = `
            <strong>${data.best_time}</strong>
            <br>
            ${data.reason || "Lower predicted pollution during this period."}
        `;

    }

    catch (err) {

        console.error("Best-time error:", err);

        bestTime.textContent =
            "Best-time analysis is currently unavailable.";

    }
}


// ==========================================
// WHAT-IF SIMULATOR
// ==========================================

async function simulateAQI() {

    if (!currentCity) {

        alert("Please check a city first.");

        return;
    }


    const pm25Input =
        document.getElementById("pm25Input");

    const simulationResult =
        document.getElementById("simulationResult");


    const pm25 = pm25Input.value;


    if (pm25 === "") {

        alert("Please enter a PM2.5 value.");

        return;
    }


    simulationResult.classList.remove("hidden");

    simulationResult.textContent =
        "Running simulation...";


    try {

        const url =
            `${BACKEND_URL}/simulate` +
            `?city=${encodeURIComponent(currentCity)}` +
            `&pm2_5=${encodeURIComponent(pm25)}`;


        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                "Simulation error: " + response.status
            );
        }


        const data =
            await response.json();


        if (data.error) {

            throw new Error(data.error);
        }


        simulationResult.innerHTML = `
            <div>
                Current AQI:
                <strong>${data.current_aqi}</strong>
            </div>

            <div>
                Simulated AQI:
                <strong>${data.simulated_aqi}</strong>
            </div>
        `;

    }

    catch (err) {

        console.error("Simulation error:", err);

        simulationResult.textContent =
            "Simulation failed: " + err.message;

    }
}


// ==========================================
// CHECK AQI BUTTON
// ==========================================

document
    .getElementById("checkButton")
    .addEventListener(
        "click",
        checkAQI
    );


// ==========================================
// SIMULATOR BUTTON
// ==========================================

document
    .getElementById("simulateButton")
    .addEventListener(
        "click",
        simulateAQI
    );


// ==========================================
// ENTER KEY
// ==========================================

document
    .getElementById("city")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                checkAQI();

            }

        }
    );