
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.metrics import mean_squared_log_error
from flask import jsonify, request
from dotenv import load_dotenv
from groq import Groq

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


from pymongo import MongoClient
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ================= APP SETUP =================
print("APP.PY IS RUNNING")

app = Flask(__name__)




# ================= MONGODB =================
client = MongoClient("mongodb://localhost:27017")


db = client["energy_dashboard"]

dataset_col = db["dataset_records"]
stats_col = db["dataset_stats"]
metrics_col = db["dataset_metrics"]

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return {"status": "BACKEND CONNECTED"}

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    metrics = metrics_col.find_one() or {}
    stats = stats_col.find_one() or {}

    return render_template(
        "dashboard.html",
        mae=float(metrics.get("mae", 0) or 0),
        rmse=float(metrics.get("rmse", 0) or 0),
        rmsle=float(metrics.get("rmsle", 0) or 0),
        r2=float(metrics.get("r2", 0) or 0),

        avg_heating=float(stats.get("avg_heating", 0) or 0),
        avg_cooling=float(stats.get("avg_cooling", 0) or 0),
        avg_total=float(stats.get("avg_total", 0) or 0),

        heating_series=stats.get("heating_series", []) or [],
        cooling_series=stats.get("cooling_series", []) or [],
        total_series=stats.get("total_series", []) or [],

        errors=stats.get("errors", []) or []
    )

load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()

    metrics = metrics_col.find_one() or {}
    stats = stats_col.find_one() or {}

    # --- Safe extraction ---
    mae = round(float(metrics.get("mae", 0) or 0), 4)
    rmse = round(float(metrics.get("rmse", 0) or 0), 4)
    rmsle = round(float(metrics.get("rmsle", 0) or 0), 4)
    r2 = round(float(metrics.get("r2", 0) or 0), 4)

    avg_heating = round(float(stats.get("avg_heating", 0) or 0), 2)
    avg_cooling = round(float(stats.get("avg_cooling", 0) or 0), 2)
    avg_total = round(float(stats.get("avg_total", 0) or 0), 2)

    heating_series = stats.get("heating_series", [])[:20]
    cooling_series = stats.get("cooling_series", [])[:20]
    total_series = stats.get("total_series", [])[:20]

    # --- Context for AI (dashboard aware) ---
    context = f"""
You are an AI Energy Analytics Assistant embedded inside a dashboard.

MODEL PERFORMANCE:
- MAE: {mae}
- RMSE: {rmse}
- RMSLE: {rmsle}
- R² Score: {r2}

ENERGY STATISTICS:
- Average Heating Energy: {avg_heating}
- Average Cooling Energy: {avg_cooling}
- Average Total Energy: {avg_total}

ENERGY TRENDS (recent samples):
- Heating: {heating_series}
- Cooling: {cooling_series}
- Total Energy: {total_series}

Your role:
• Explain metrics in simple terms
• Compare heating vs cooling
• Explain trends shown in graphs
• Give actionable insights
• Be concise and visual-friendly
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": "You are a smart, friendly Energy Dashboard Assistant."
            },
            {
                "role": "user",
                "content": context + "\n\nUser question: " + user_msg
            }
        ],
        temperature=0.4
    )

    return jsonify({
        "reply": completion.choices[0].message.content
    })


# ================= SINGLE PREDICTION =================
@app.route("/predict", methods=["POST"])
def predict():
    features = [float(request.form[k]) for k in request.form]
    X_scaled = scaler.transform([features])
    pred = model.predict(X_scaled)[0]

    return render_template(
        "result.html",
        heating=round(pred[0], 2),
        cooling=round(pred[1], 2),
        total=round(pred[0] + pred[1], 2)
    )

# ================= UPLOAD PAGE =================
@app.route("/upload")
def upload():
    return render_template("upload.html")

# ================= DATASET UPLOAD & AUTO UPDATE =================
@app.route("/evaluate", methods=["POST"])
def evaluate():
    file = request.files.get("dataset")
    if not file:
        return redirect(url_for("dashboard"))

    df = pd.read_csv(file)

    COLUMN_MAPPING = {
        "X1": "Relative_Compactness",
        "X2": "Surface_Area",
        "X3": "Wall_Area",
        "X4": "Roof_Area",
        "X5": "Overall_Height",
        "X6": "Orientation",
        "X7": "Glazing_Area",
        "X8": "Glazing_Area_Distribution",
        "Y1": "Heating_Load",
        "Y2": "Cooling_Load"
    }
    df.rename(columns=COLUMN_MAPPING, inplace=True)

    FEATURE_COLUMNS = [
        "Relative_Compactness",
        "Surface_Area",
        "Wall_Area",
        "Roof_Area",
        "Overall_Height",
        "Orientation",
        "Glazing_Area",
        "Glazing_Area_Distribution"
    ]

    TARGET_COLUMNS = ["Heating_Load", "Cooling_Load"]

    df = df[FEATURE_COLUMNS + TARGET_COLUMNS].dropna()
    if df.empty:
        return "Dataset has no valid rows", 400

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMNS]

    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    # ===== CREATE SERIES DATA FOR DASHBOARD =====
    series_limit = min(30, len(y_pred))

    heating_series = y_pred[:series_limit, 0].round(2).tolist()
    cooling_series = y_pred[:series_limit, 1].round(2).tolist()
    total_series = (y_pred[:series_limit, 0] + y_pred[:series_limit, 1]).round(2).tolist()

    # ---------- SERIES DATA (FOR DASHBOARD GRAPHS) ----------
    series_limit = min(30, len(y_pred))

    heating_series = y_pred[:series_limit, 0].round(2).tolist()
    cooling_series = y_pred[:series_limit, 1].round(2).tolist()
    total_series = (y_pred[:series_limit, 0] + y_pred[:series_limit, 1]).round(2).tolist()


    try:
        # Clear old DB data
        dataset_col.delete_many({})
        stats_col.delete_many({})
        metrics_col.delete_many({})

        # Save dataset
        dataset_col.insert_many(df.to_dict(orient="records"))

        # ---------- METRICS ----------
        y_true_safe = np.maximum(y.values, 0)
        y_pred_safe = np.maximum(y_pred, 0)

        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        rmsle = np.sqrt(mean_squared_log_error(y_true_safe, y_pred_safe))
        r2 = r2_score(y, y_pred)

        metrics = {
            "mae": round(float(mae), 3),
            "rmse": round(float(rmse), 3),
            "rmsle": round(float(rmsle),3),
            "r2": round(float(r2), 3)
        }
        metrics_col.insert_one(metrics)
        print("RAW RMSLE:", rmsle)

        # ---------- STATS ----------
        stats = {
    "rows": int(len(df)),
    "features": len(FEATURE_COLUMNS),

    "avg_heating": round(float(y_pred[:, 0].mean()), 2),
    "avg_cooling": round(float(y_pred[:, 1].mean()), 2),
    "avg_total": round(float((y_pred[:, 0] + y_pred[:, 1]).mean()), 2),

    # ✅ SERIES FOR CHARTS
    "heating_series": heating_series,
    "cooling_series": cooling_series,
    "total_series": total_series
}
        stats_col.delete_many({})
        stats_col.insert_one(stats)

    except Exception as e:
        print("⚠ MongoDB error while saving results:", e)

    return redirect(url_for("dashboard"))




# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
