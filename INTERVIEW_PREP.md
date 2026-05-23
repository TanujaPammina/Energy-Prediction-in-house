# 📘 Interview Preparation Document
## Energy Consumption Prediction — Complete Technical Deep Dive

---

## 1. PROJECT OVERVIEW

**What is this project?**
A full-stack Machine Learning web application that predicts the **heating load** and **cooling load** of a building before it is constructed, based on 8 physical parameters. It helps architects and engineers make energy-efficient design decisions early.

**Problem Statement:**
Buildings account for ~40% of global energy consumption. Most energy waste happens because designers don't know the energy impact of their design choices. This tool solves that by predicting energy needs from building parameters alone.

**Dataset:** UCI Energy Efficiency Dataset
- 768 samples
- 8 input features (building physical properties)
- 2 output targets (Heating Load, Cooling Load in kWh/m²)

---

## 2. MACHINE LEARNING MODEL

### ✅ Algorithm Used: Random Forest Regressor (via MultiOutputRegressor)

```python
model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42
    )
)
```

### Why Random Forest?

| Reason | Explanation |
|---|---|
| **Non-linear relationships** | Building energy has complex non-linear interactions between features (e.g., height × glazing area). RF handles this naturally. |
| **No assumptions** | Unlike Linear Regression, RF doesn't assume linearity, normality, or homoscedasticity. |
| **Feature importance** | RF gives built-in feature importance scores — useful for explaining which building parameters matter most. |
| **Robust to outliers** | Averaging over 200 trees reduces the effect of any single outlier. |
| **Small dataset** | With only 768 samples, deep learning would overfit. RF works well on small tabular data. |

### Why NOT other algorithms?

| Algorithm | Why Not Used |
|---|---|
| **Linear Regression** | Assumes linear relationship. Energy consumption is non-linear — would give poor R². |
| **Neural Network / Deep Learning** | Needs large data (10k+ samples). With 768 rows it would overfit badly. Also harder to explain. |
| **SVM Regressor** | Slow to train on multi-output problems. Doesn't scale well. |
| **Decision Tree (single)** | High variance, overfits easily. RF is an ensemble of trees — much more stable. |
| **XGBoost** | Would also work well, but RF was simpler to implement and already achieved R² ~0.99. No need to add complexity. |
| **KNN Regressor** | Slow at prediction time (scans all training data). Not suitable for a real-time web app. |

### Why MultiOutputRegressor?

Scikit-learn's `RandomForestRegressor` doesn't natively support multi-output regression with separate trees per target. `MultiOutputRegressor` wraps it to train **one model per target** (one for Heating Load, one for Cooling Load), giving better accuracy than a single shared model.

---

## 3. DATA PREPROCESSING

### StandardScaler

```python
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

**Why StandardScaler?**
- Features have very different ranges: Relative Compactness (0.62–0.98) vs Surface Area (514–808)
- StandardScaler normalises each feature to mean=0, std=1
- Prevents features with large values from dominating distance-based calculations
- **Important:** `fit` only on training data, `transform` on both — prevents data leakage

**Why NOT MinMaxScaler?**
- MinMaxScaler is sensitive to outliers (clips to [0,1] based on min/max)
- StandardScaler is more robust for tree-based models and general use

### Train/Test Split: 80/20

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

- 80% training (614 samples), 20% testing (154 samples)
- `random_state=42` ensures reproducibility
- No cross-validation used (dataset is small but clean; single split was sufficient given R² ~0.99)

---

## 4. MODEL EVALUATION METRICS

### MAE — Mean Absolute Error
```
MAE = average of |actual - predicted|
```
- Measures average prediction error in the same unit as output (kWh/m²)
- Easy to interpret: "on average, predictions are off by X kWh/m²"
- **Not sensitive to outliers**

### RMSE — Root Mean Squared Error
```
RMSE = sqrt(average of (actual - predicted)²)
```
- Penalises large errors more than MAE
- Useful when large errors are especially bad
- Same unit as output

### RMSLE — Root Mean Squared Log Error
```
RMSLE = sqrt(average of (log(actual+1) - log(predicted+1))²)
```
- Measures relative error rather than absolute
- Useful when targets span a wide range
- Less sensitive to large absolute differences

### R² Score — Coefficient of Determination
```
R² = 1 - (SS_residual / SS_total)
```
- Measures what % of variance in the target is explained by the model
- R² = 1.0 → perfect prediction
- R² = 0.0 → model is no better than predicting the mean
- **Our model: R² ~0.99** → explains 99% of variance

### Why these 4 metrics?
Using multiple metrics gives a complete picture:
- MAE → average error magnitude
- RMSE → sensitivity to large errors
- RMSLE → relative error
- R² → overall model quality

---

## 5. BACKEND — FLASK

### Why Flask?

| Reason | Explanation |
|---|---|
| **Lightweight** | No ORM, no admin panel, no bloat. Perfect for an ML serving app. |
| **Python-native** | Seamlessly integrates with scikit-learn, pandas, numpy — no language boundary. |
| **Fast to build** | A prediction endpoint is 5 lines of code in Flask. |
| **Flexible routing** | Easy to define `/predict`, `/evaluate`, `/chat`, `/dashboard` routes. |

### Why NOT Django?
- Django is a full-featured framework with ORM, admin, auth — all unnecessary for this project
- Much heavier and slower to set up
- Overkill for a simple ML serving application

### Why NOT FastAPI?
- FastAPI is excellent for pure APIs but requires more setup for HTML template rendering
- Flask's Jinja2 templating is simpler for server-side rendered pages
- FastAPI would be the right choice if this were a pure REST API with a separate frontend

### API Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Render prediction form |
| `/predict` | POST | Accept form data, run model, return result |
| `/dashboard` | GET | Fetch metrics from MongoDB, render dashboard |
| `/upload` | GET | Render upload page |
| `/evaluate` | POST | Accept CSV, run model on it, save metrics to MongoDB |
| `/chat` | POST | Accept user message, call Groq API, return AI reply |
| `/ping` | GET | Health check endpoint |

---

## 6. DATABASE — MONGODB

### Why MongoDB?

| Reason | Explanation |
|---|---|
| **Schema-less** | Metrics and stats have varying structures. MongoDB stores them as flexible JSON documents. |
| **Fast reads** | Dashboard only needs `find_one()` — single document read, extremely fast. |
| **Python-friendly** | PyMongo returns Python dicts directly — no ORM mapping needed. |
| **Atlas free tier** | Free 512MB cloud cluster — perfect for a demo/production app. |

### Why NOT PostgreSQL / MySQL?
- Relational databases require fixed schemas and table definitions
- For storing ML metrics (which may change structure), a document store is more flexible
- No complex joins or transactions needed — MongoDB is simpler here

### Why NOT SQLite?
- SQLite is file-based and doesn't work well on cloud platforms like Render (ephemeral filesystem)
- Not suitable for production deployment

### Collections Used

| Collection | Stores |
|---|---|
| `dataset_records` | All rows from the uploaded CSV |
| `dataset_stats` | Avg heating/cooling/total, series data for charts |
| `dataset_metrics` | MAE, RMSE, RMSLE, R² from model evaluation |

---

## 7. AI CHATBOT — GROQ + LLAMA 3.1

### Why Groq?

| Reason | Explanation |
|---|---|
| **Speed** | Groq's LPU (Language Processing Unit) is the fastest LLM inference available — responses in <1 second |
| **Free tier** | Generous free API with no credit card required |
| **Llama 3.1 access** | Provides access to Meta's open-source Llama 3.1 model |

### Why Llama 3.1-8b-instant?

| Reason | Explanation |
|---|---|
| **8B parameters** | Small enough to be fast, large enough to give intelligent answers |
| **Instruction-tuned** | Fine-tuned to follow instructions and answer questions accurately |
| **Open source** | Meta's open model — no vendor lock-in |
| **"instant" variant** | Optimised for low-latency responses |

### Why NOT OpenAI GPT-4?
- Paid API — costs money per token
- Groq + Llama 3.1 is free and fast enough for this use case

### Why NOT a local LLM?
- Running a local LLM requires GPU/high RAM — not available on Render's free tier
- Groq API offloads inference to their hardware

### Context Injection Pattern
The chatbot receives live dashboard data (MAE, RMSE, R², energy averages, series) injected into the system prompt. This makes it **context-aware** — it can answer questions specifically about the current dataset, not just generic energy questions.

---

## 8. FRONTEND

### Why Vanilla HTML/CSS/JS + Jinja2?

| Reason | Explanation |
|---|---|
| **No build step** | No webpack, npm, node_modules. Deploy instantly. |
| **Server-side rendering** | Flask renders templates with data — no separate API calls needed for page load |
| **Lightweight** | Loads fast on free Render instances |
| **Jinja2 templating** | Python-native templating — pass variables directly from Flask to HTML |

### Why NOT React/Vue/Angular?
- Would require a separate frontend server or build pipeline
- Adds complexity (npm, bundling, CORS) for no real benefit in a small app
- Server-side rendering with Jinja2 is simpler and faster to develop

### Chart.js — Why?
- Lightweight (no D3.js complexity)
- Beautiful default styles
- Supports bar, line, doughnut, scatter, radar — all used in the dashboard
- CDN-loaded — no installation needed

---

## 9. DEPLOYMENT — RENDER

### Why Render?

| Reason | Explanation |
|---|---|
| **Free tier** | Free web service hosting for hobby projects |
| **GitHub integration** | Auto-deploys on every push to main |
| **Environment variables** | Secure storage for API keys and DB URIs |
| **Python support** | Native Python runtime with `gunicorn` |

### Why Gunicorn?
- Flask's built-in development server (`app.run()`) is **not production-safe** — single-threaded, no worker management
- Gunicorn is a production WSGI server that handles multiple concurrent requests
- Standard choice for Flask on any cloud platform

### Why NOT Heroku?
- Heroku removed its free tier in 2022
- Render offers equivalent features for free

### Why NOT AWS/GCP/Azure?
- Much more complex setup (IAM, VPCs, load balancers)
- Overkill and costly for a demo project

---

## 10. SYSTEM ARCHITECTURE

```
User Browser
     │
     │  HTTP Request
     ▼
┌─────────────────────────────────┐
│         Render (Cloud)          │
│                                 │
│  ┌──────────────────────────┐   │
│  │      Flask App           │   │
│  │  (Gunicorn WSGI Server)  │   │
│  │                          │   │
│  │  Routes:                 │   │
│  │  / → index.html          │   │
│  │  /predict → ML Model     │   │
│  │  /evaluate → MongoDB     │   │
│  │  /dashboard → MongoDB    │   │
│  │  /chat → Groq API        │   │
│  └──────────┬───────────────┘   │
│             │                   │
└─────────────┼───────────────────┘
              │
    ┌─────────┴──────────┐
    │                    │
    ▼                    ▼
┌────────────┐    ┌─────────────┐
│  MongoDB   │    │  Groq API   │
│   Atlas    │    │ Llama 3.1   │
│  (Cloud)   │    │  (Cloud)    │
└────────────┘    └─────────────┘
```

### Data Flow for Prediction:
```
User fills form → POST /predict
→ Flask reads form fields
→ StandardScaler.transform()
→ RandomForest.predict()
→ Returns [heating, cooling]
→ Renders result.html
```

### Data Flow for Dashboard:
```
User uploads CSV → POST /evaluate
→ Flask reads CSV with pandas
→ Renames columns
→ Scaler transforms features
→ Model predicts on all rows
→ Computes MAE, RMSE, RMSLE, R²
→ Saves to MongoDB Atlas
→ Redirects to /dashboard
→ Flask fetches from MongoDB
→ Renders dashboard.html with data
→ Chart.js renders charts in browser
```

---

## 11. FEATURE IMPORTANCE (Why these 8 features?)

| Feature | Importance | Why it matters |
|---|---|---|
| **Relative Compactness** | 95% | More compact = less surface area = less heat loss |
| **Overall Height** | 90% | Taller buildings have more wall area and different thermal dynamics |
| **Glazing Area** | 82% | Windows are major sources of heat gain/loss |
| **Surface Area** | 75% | More surface = more exposure to outside temperature |
| **Wall Area** | 70% | Walls are the primary thermal barrier |
| **Roof Area** | 62% | Roof insulation significantly affects heating |
| **Glazing Distribution** | 35% | Where windows are placed affects solar gain direction |
| **Orientation** | 12% | South-facing gets more sun; minor effect compared to size |

These 8 features come from the **UCI Energy Efficiency Dataset** — a well-established benchmark dataset used in energy research.

---

## 12. COMMON INTERVIEW QUESTIONS & ANSWERS

**Q: Why did you choose Random Forest over XGBoost?**
A: Both would work well here. Random Forest was chosen because it already achieved R² ~0.99 on this dataset, making XGBoost's additional complexity unnecessary. If accuracy were lower, XGBoost would be the next step due to its gradient boosting approach.

**Q: How do you prevent data leakage?**
A: The StandardScaler is `fit` only on training data and `transform` applied to both train and test. This ensures test data statistics don't influence the scaling parameters.

**Q: Why 200 trees in Random Forest?**
A: More trees = lower variance (more stable predictions). 200 is a good balance — beyond ~300 trees, accuracy improvements become negligible while training time increases linearly.

**Q: What is MultiOutputRegressor doing?**
A: Scikit-learn's RandomForestRegressor can handle multi-output natively, but MultiOutputRegressor trains a completely separate model for each target (Heating Load and Cooling Load). This gives better accuracy because each target may have different feature relationships.

**Q: How does the AI chatbot know about the current data?**
A: Before calling the Groq API, we inject the current dashboard metrics (MAE, RMSE, R², average energy values, recent series data) into the system prompt. The LLM then answers questions in the context of the actual uploaded dataset.

**Q: Why MongoDB instead of a SQL database?**
A: The metrics and stats stored are JSON-like documents with flexible structure. MongoDB's document model fits naturally. Also, we only ever do `find_one()` and `insert_one()` — no complex queries that would benefit from SQL.

**Q: How does the app handle MongoDB being unavailable?**
A: The connection is wrapped in a try/except with a 5-second timeout. If MongoDB is unavailable, all collection variables are set to `None` and the app continues running — the dashboard just shows zeros. All MongoDB operations check `if collection is not None` before executing.

**Q: What is RMSLE and when is it better than RMSE?**
A: RMSLE measures the ratio between predicted and actual values (in log space). It's better when you care about relative errors rather than absolute ones, and when targets span a wide range. For energy loads (which can range from 6 to 43 kWh/m²), RMSLE penalises under-predictions more than over-predictions.

**Q: How would you improve this model?**
A: 
1. Collect more data (768 samples is small)
2. Try XGBoost or LightGBM for comparison
3. Add hyperparameter tuning with GridSearchCV
4. Add cross-validation (k-fold) for more reliable evaluation
5. Add more features (insulation type, climate zone, building age)

---

## 13. TECH STACK SUMMARY

| Component | Technology | Version | Why |
|---|---|---|---|
| Language | Python | 3.11 | ML ecosystem, Flask support |
| Web Framework | Flask | 3.0 | Lightweight, Jinja2, Python-native |
| ML Library | Scikit-learn | latest | Industry standard, MultiOutputRegressor |
| Data Processing | Pandas + NumPy | latest | Standard data science stack |
| Database | MongoDB Atlas | latest | Flexible schema, free cloud tier |
| AI/LLM | Groq + Llama 3.1 | 8b-instant | Free, fast, context-aware |
| Frontend Charts | Chart.js | 4.4.1 | Lightweight, beautiful, CDN |
| Production Server | Gunicorn | latest | WSGI, multi-worker, production-safe |
| Deployment | Render | - | Free tier, GitHub auto-deploy |
| Env Management | python-dotenv | latest | Secure API key handling |

---

*Prepared for interview use — covers ML, backend, database, AI integration, deployment, and design decisions.*
