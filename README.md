# ⚡ Energy Prediction in House

This project predicts **heating and cooling energy consumption** before building a house, helping save energy efficiently. Using historical data and a trained Random Forest model, it estimates energy usage — enabling better planning and reducing waste.

## 🚀 Live Demo

👉 [Energy Consumption Prediction App](https://energy-consumption-prediction-2-3.onrender.com)

---

## ✨ Features

- 🔮 **Instant Predictions** — Enter 8 building parameters and get heating & cooling load predictions in milliseconds
- 📊 **Analytics Dashboard** — Upload a CSV dataset to visualise model performance, energy trends, and feature importance
- 🤖 **AI Energy Assistant** — Ask questions in plain English powered by Llama 3.1 (Groq)
- 🎤 **Voice Input** — Hands-free queries via Web Speech API
- 🗄️ **MongoDB Persistence** — All evaluation metrics stored and displayed on the dashboard
- 📂 **Drag & Drop Upload** — Evaluate the model on any compatible CSV dataset

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML Model | Scikit-learn (Random Forest, MultiOutputRegressor) |
| Database | MongoDB |
| AI Assistant | Groq API (Llama 3.1) |
| Frontend | HTML5, CSS3, JavaScript, Chart.js |

---

## 📋 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/TanujaPammina/Energy-Prediction-in-house.git
cd Energy-Prediction-in-house/Energy-Consumption-Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Start MongoDB (make sure it's running locally)

# 5. Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## 📐 Input Parameters

| Feature | Description | Range |
|---|---|---|
| Relative Compactness | Building shape ratio | 0.62 – 0.98 |
| Surface Area | Total surface area (m²) | 514 – 808 |
| Wall Area | Total wall area (m²) | 245 – 416 |
| Roof Area | Total roof area (m²) | 110 – 220 |
| Overall Height | Building height (m) | 3.5 or 7 |
| Orientation | Cardinal direction | 2 – 5 |
| Glazing Area | Window area fraction | 0 – 0.4 |
| Glazing Distribution | Window placement pattern | 0 – 5 |

**Outputs:** Heating Load (kWh/m²) · Cooling Load (kWh/m²)

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| R² Score | ~0.99 |
| MAE | ~0.3 |
| RMSE | ~0.5 |

---

## 👥 Team Members

| Name | Role |
|---|---|
| **Tanuja Pammina** | Project Lead & ML Engineer |
| **Peesa Lahari Sri** | Frontend Developer |
| **Ganta Nandini** | Frontend Developer & Chatbot Designer |
| **Tavva Roshini** | ML Engineer |

---

*Feel free to contribute or report issues!*
