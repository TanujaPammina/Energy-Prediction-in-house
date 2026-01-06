import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1️⃣ Load dataset
df = pd.read_csv("data/Energy.csv")

# 🔥 REMOVE unwanted unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

print("Columns after cleanup:", df.shape[1])

# 2️⃣ Rename columns (ONLY AFTER cleanup)
df.columns = [
    "Relative_Compactness",
    "Surface_Area",
    "Wall_Area",
    "Roof_Area",
    "Overall_Height",
    "Orientation",
    "Glazing_Area",
    "Glazing_Area_Distribution",
    "Heating_Load",
    "Cooling_Load"
]

# 🔥 Remove NaN targets
df = df.dropna(subset=["Heating_Load", "Cooling_Load"])

# 3️⃣ Split features & targets
X = df.drop(columns=["Heating_Load", "Cooling_Load"])
y = df[["Heating_Load", "Cooling_Load"]]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4️⃣ Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 5️⃣ Train model
model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42
    )
)
model.fit(X_train, y_train)

# 6️⃣ Evaluate model
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
rmsle = np.sqrt(
    mean_squared_error(np.log1p(y_test), np.log1p(y_pred))
)

print("\n📊 Model Evaluation Metrics")
print("MAE  :", mae)
print("RMSE :", rmse)
print("RMSLE:", rmsle)
print("R2   :", r2)

# 7️⃣ Save model & scaler
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("\n✅ Model and scaler saved successfully")