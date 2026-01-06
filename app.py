from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error, r2_score

app = Flask(__name__)
app.secret_key = "energy_dashboard_secret"

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ================= BASELINE METRICS =================
BASELINE_METRICS = {
    "mae": 0.722,
    "rmse": 1.290,
    "rmsle": 0.039,
    "r2": 0.982
}

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        mae=session.get("mae", BASELINE_METRICS["mae"]),
        rmse=session.get("rmse", BASELINE_METRICS["rmse"]),
        rmsle=session.get("rmsle", BASELINE_METRICS["rmsle"]),
        r2=session.get("r2", BASELINE_METRICS["r2"]),

        # ✅ DATASET VALUES
        heating=session.get("dataset_heating", []),
        cooling=session.get("dataset_cooling", []),
        total=session.get("dataset_total", []),

        # ✅ THIS WAS MISSING
        open_tab=session.get("open_tab")
    )


# ================= SINGLE BUILDING PREDICTION =================
@app.route("/predict", methods=["POST"])
def predict():
    features = [
        float(request.form["Relative_Compactness"]),
        float(request.form["Surface_Area"]),
        float(request.form["Wall_Area"]),
        float(request.form["Roof_Area"]),
        float(request.form["Overall_Height"]),
        float(request.form["Orientation"]),
        float(request.form["Glazing_Area"]),
        float(request.form["Glazing_Area_Distribution"])
    ]

    X_scaled = scaler.transform([features])
    pred = model.predict(X_scaled)[0]

    heating = round(pred[0], 2)
    cooling = round(pred[1], 2)
    total = round(heating + cooling, 2)

    return render_template(
        "result.html",
        heating=heating,
        cooling=cooling,
        total=total
    )

# ================= UPLOAD =================
@app.route("/upload")
def upload():
    return render_template("upload.html")

# ================= DATASET EVALUATION =================
@app.route("/evaluate", methods=["POST"])
def evaluate():
    file = request.files.get("dataset")

    if not file or file.filename == "":
        session["open_tab"] = "analysis"
        session["dataset_heating"] = []
        return redirect(url_for("dashboard"))

    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip().str.upper()

        required = ['X1','X2','X3','X4','X5','X6','X7','X8','Y1','Y2']
        if not all(col in df.columns for col in required):
            session["open_tab"] = "analysis"
            session["dataset_heating"] = []
            return redirect(url_for("dashboard"))

        df = df[required].apply(pd.to_numeric, errors="coerce").dropna()
        if df.empty:
            session["open_tab"] = "analysis"
            session["dataset_heating"] = []
            return redirect(url_for("dashboard"))

        # 🔥 SCALE FEATURES (THIS WAS MISSING EARLIER)
        X = df[['X1','X2','X3','X4','X5','X6','X7','X8']]
        X_scaled = scaler.transform(X)

        y_pred = model.predict(X_scaled)

        # ✅ STORE DATASET VALUES
        session["dataset_heating"] = y_pred[:,0].round(2).tolist()
        session["dataset_cooling"] = y_pred[:,1].round(2).tolist()
        session["dataset_total"]   = (y_pred[:,0] + y_pred[:,1]).round(2).tolist()

        # ✅ METRICS
        session["mae"] = round(mean_absolute_error(df[['Y1','Y2']], y_pred), 3)
        session["rmse"] = round(np.sqrt(mean_squared_error(df[['Y1','Y2']], y_pred)), 3)
        session["rmsle"] = round(
            np.sqrt(mean_squared_log_error(
                np.maximum(df[['Y1','Y2']],0),
                np.maximum(y_pred,0)
            )), 3
        )
        session["r2"] = round(r2_score(df[['Y1','Y2']], y_pred), 3)

        # 🔥 THIS IS KEY
        session["open_tab"] = "analysis"

        return redirect(url_for("dashboard"))

    except Exception as e:
        print("EVALUATE ERROR:", e)
        session["open_tab"] = "analysis"
        session["dataset_heating"] = []
        return redirect(url_for("dashboard"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
