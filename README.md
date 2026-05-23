# ⚡ Energy Prediction in House

> Predict building heating & cooling energy consumption instantly using Machine Learning — before you even break ground.

<div align="center">

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-energy--prediction--in--house.onrender.com-6366f1?style=for-the-badge)](https://energy-prediction-in-house.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com/atlas)

</div>

---

## 🌐 Live Demo

👉 **[https://energy-prediction-in-house.onrender.com/](https://energy-prediction-in-house.onrender.com/)**

Explore real-time predictions based on building parameters — no setup required!

---

## 📸 Pages

| Page | Description |
|---|---|
| 🏠 **Home** | Enter 8 building parameters and predict energy loads instantly |
| 📊 **Dashboard** | Upload a CSV to visualise model metrics, trends & feature importance |
| 🔮 **Result** | Animated heating/cooling breakdown with charts |
| 📂 **Upload** | Drag & drop CSV evaluation with schema guide |

---

## ✨ Features

- 🔮 **Instant ML Predictions** — Heating & cooling load in milliseconds
- 📊 **Live Analytics Dashboard** — 3-tab dashboard with bar, line, doughnut, scatter & radar charts
- 🤖 **AI Energy Assistant** — Ask questions in plain English, powered by **Llama 3.1** via Groq
- 🎤 **Voice Input** — Hands-free queries via Web Speech API
- 📂 **Drag & Drop Upload** — Evaluate the model on any compatible CSV
- 🗄️ **MongoDB Atlas** — Persistent metrics and dataset statistics
- 📱 **Fully Responsive** — Works on desktop, tablet and mobile

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask |
| **ML Model** | Scikit-learn — Random Forest, MultiOutputRegressor |
| **Database** | MongoDB Atlas |
| **AI Assistant** | Groq API (Llama 3.1-8b-instant) |
| **Frontend** | HTML5, CSS3, Vanilla JS, Chart.js 4 |
| **Deployment** | Render (Web Service) |

---

## 📐 Input Parameters

| # | Feature | Description | Range |
|---|---|---|---|
| X1 | Relative Compactness | Building shape ratio | 0.62 – 0.98 |
| X2 | Surface Area | Total surface area (m²) | 514 – 808 |
| X3 | Wall Area | Total wall area (m²) | 245 – 416 |
| X4 | Roof Area | Total roof area (m²) | 110 – 220 |
| X5 | Overall Height | Building height (m) | 3.5 or 7 |
| X6 | Orientation | Cardinal direction | 2 – 5 |
| X7 | Glazing Area | Window area fraction | 0 – 0.4 |
| X8 | Glazing Distribution | Window placement pattern | 0 – 5 |

**Outputs:** `Heating Load (kWh/m²)` · `Cooling Load (kWh/m²)` · `Total Energy (kWh/m²)`

---

## 📊 Model Performance

| Metric | Value | Meaning |
|---|---|---|
| **R² Score** | ~0.99 | 99% variance explained |
| **MAE** | ~0.3 | Average prediction error |
| **RMSE** | ~0.5 | Penalised error metric |
| **RMSLE** | ~0.02 | Log-scale error |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/TanujaPammina/Energy-Prediction-in-house.git
cd Energy-Prediction-in-house/Energy-Consumption-Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "GROQ_API_KEY=your_groq_key_here" > .env
echo "MONGO_URI=mongodb://localhost:27017" >> .env

# 4. Run the app
python app.py
```

Open `http://localhost:5000` in your browser.

---

## 🌍 Deploy on Render

1. Fork this repo
2. Create a new **Web Service** on [render.com](https://render.com)
3. Set **Root Directory** → `Energy-Consumption-Prediction`
4. Set **Start Command** → `gunicorn app:app`
5. Add environment variables:
   - `GROQ_API_KEY` — from [console.groq.com](https://console.groq.com)
   - `MONGO_URI` — from [MongoDB Atlas](https://mongodb.com/atlas)

---

## 👥 Team

| Name | Role |
|---|---|
| **Tanuja Pammina** | Project Lead & ML Engineer |
| **Peesa Lahari Sri** | Frontend Developer |
| **Ganta Nandini** | Frontend Developer & Chatbot Designer |
| **Tavva Roshini** | ML Engineer |

---

<div align="center">

Made with ❤️ · [Live App](https://energy-prediction-in-house.onrender.com/) · [Report Issue](https://github.com/TanujaPammina/Energy-Prediction-in-house/issues)

</div>
