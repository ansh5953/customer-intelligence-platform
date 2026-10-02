# Customer Intelligence Platform

A full-stack customer churn prediction system built on the **IBM Telco Customer Churn** dataset. It combines a PostgreSQL data warehouse, a scikit-learn / XGBoost ML pipeline, and an interactive Streamlit dashboard for real-time analytics and single-customer churn prediction.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [End-to-End Pipeline](#end-to-end-pipeline)
4. [Machine Learning Models & Comparison](#machine-learning-models--comparison)
5. [Dashboard Pages](#dashboard-pages)
6. [Setup & Installation](#setup--installation)
7. [Running the Project](#running-the-project)
8. [Snapshots](#snapshots)
9. [Tech Stack](#tech-stack)

---

## Project Overview

Telecom companies lose significant revenue to customer churn. This platform helps analysts and product managers:

- **Understand** churn patterns across contract type, internet service, and tenure
- **Evaluate** ML model performance with an adjustable decision threshold
- **Predict** churn probability for any individual customer in real time
- **Act** on AI-generated retention suggestions for high-risk customers

---

## Folder Structure

```
customer-intelligence-platform/
│
├── data/
│   ├── telco_churn.csv               # Raw IBM Telco dataset (7043 rows, 21 columns)
│   └── processed/
│       └── telco_churn_cleaned.csv   # Cleaned & normalised CSV ready for DB ingestion
│
├── models/
│   ├── xgb_model.pkl                 # Trained XGBoost classifier (saved with joblib)
│   └── model_columns.pkl             # Feature column list for inference alignment
│
├── notebooks/
│   └── 01_data_inspection.ipynb      # Exploratory data analysis notebook
│
├── snapshots/                        # Dashboard screenshots (add your own here)
│
├── sql/
│   └── schema.sql                    # PostgreSQL CREATE TABLE statement
│
├── src/
│   ├── preprocessing/
│   │   └── clean_data.py             # Step 1 — raw CSV cleaning & normalisation
│   │
│   ├── ingestion/
│   │   └── load_data.py              # Step 2 — bulk load cleaned CSV into PostgreSQL
│   │
│   ├── database/
│   │   └── connection.py             # Reusable psycopg3 connection helper
│   │
│   ├── features/
│   │   └── preprocess.py             # Step 3 — feature engineering & encoding
│   │
│   ├── models/
│   │   └── train.py                  # Step 4 — model training & persistence
│   │
│   ├── analysis/
│   │   └── explore.py                # Scratch exploration & model comparison script
│   │
│   └── dashboard/
│       ├── app.py                    # Streamlit main page (overview analytics)
│       ├── utils.py                  # Cached data & model loaders
│       ├── styles.py                 # Shared CSS, HTML component renderers
│       └── pages/
│           ├── Model_Performance.py  # Page 2 — confusion matrix, threshold slider
│           └── Predict.py            # Page 3 — single-customer churn predictor
│
├── .env                              # DB credentials (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## End-to-End Pipeline

```
Raw CSV  →  Clean  →  PostgreSQL  →  Feature Engineering  →  Train XGBoost  →  Dashboard
```

### Step 1 — Data Cleaning (`src/preprocessing/clean_data.py`)

- Strips whitespace from `TotalCharges` and coerces it to `float` (11 rows had empty strings representing new customers with zero charges)
- Renames CamelCase columns to `snake_case` using a regex substitution
- Maps Yes/No binary columns (`partner`, `dependents`, `phone_service`, `paperless_billing`, `churn`) to Python booleans
- Strips whitespace from multi-category service columns (`multiple_lines`, `online_security`, etc.)
- Writes the cleaned dataset to `data/processed/telco_churn_cleaned.csv`

### Step 2 — Database Ingestion (`src/ingestion/load_data.py`)

- Reads the cleaned CSV and bulk-inserts all 7043 rows into the `customers` PostgreSQL table using parameterised `psycopg3` queries
- Schema defined in `sql/schema.sql` — run `psql -f sql/schema.sql` once before ingestion

### Step 3 — Feature Engineering (`src/features/preprocess.py`)

| Function | Purpose |
|---|---|
| `load_data()` | Pulls all rows from PostgreSQL via pandas `read_sql` |
| `clean_data(df)` | Drops non-predictive columns (`customer_id`, `created_at`) |
| `split_features_target(df)` | Separates feature matrix `X` and binary target `y` (churn) |
| `encode_features(X)` | One-hot encodes all categorical columns with `pd.get_dummies(drop_first=True)` |
| `prepare_data()` | Orchestrates all of the above in order |

### Step 4 — Model Training (`src/models/train.py`)

- Calls `prepare_data()` to get encoded features
- Splits 80/20 with stratification to preserve class imbalance ratio
- Trains `XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)`
- Persists model to `models/xgb_model.pkl` and feature columns to `models/model_columns.pkl`

---

## Machine Learning Models & Comparison

During exploration (`src/analysis/explore.py`) three models were evaluated on the same 80/20 stratified split:

| Model | Accuracy | Churn Recall | Churn Precision | Notes |
|---|---|---|---|---|
| **Logistic Regression** | ~80% | ~55% | ~64% | Baseline — fast, interpretable, poor recall on minority class |
| **Random Forest** | ~79% | ~48% | ~68% | Less recall than LR despite higher overall accuracy; overfits without tuning |
| **XGBoost** (chosen) | ~81% | **~79%** | ~60% | Best recall at threshold=0.35; gradient boosting handles class imbalance better |

### Why XGBoost Won

**Recall on the churn class is the business-critical metric** — a false negative (missing a churner) costs more than a false positive (flagging a loyal customer). XGBoost achieved the highest churn recall (~79%) when the decision threshold was lowered from the default 0.5 to **0.35**, at only a modest precision trade-off.

Key XGBoost advantages on this dataset:
- Handles the imbalanced class ratio (~73% non-churn / ~27% churn) via gradient weighting without requiring `scale_pos_weight`
- No need to manually scale features (unlike Logistic Regression with `StandardScaler`)
- Tree ensembles capture non-linear interactions (e.g. Fiber optic + Month-to-month → very high churn risk)

### Adjustable Decision Threshold

The Model Performance dashboard page exposes a **threshold slider (0.0 – 1.0)**. Lowering the threshold increases recall (catches more churners) at the cost of precision (more false alarms). The sweet spot found during exploration was **0.35**.

---

## Dashboard Pages

| Page | URL suffix | Description |
|---|---|---|
| Overview | `/` | KPI cards (total customers, churn rate, avg tenure), churn by contract type, internet service, and tenure bucket |
| Model Performance | `/Model_Performance` | Accuracy / Recall / Precision cards, interactive confusion matrix heatmap, predicted probability distribution with threshold line |
| Predict | `/Predict` | Input form → animated churn probability ring → risk card → AI retention suggestions |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 14+ running locally

### 1. Clone & create virtual environment

```bash
git clone <repo-url>
cd customer-intelligence-platform
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env` and fill in your credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=customer_intelligence
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Create the database schema

```bash
psql -U postgres -d customer_intelligence -f sql/schema.sql
```

### 5. Clean raw data

```bash
python src/preprocessing/clean_data.py
```

### 6. Load data into PostgreSQL

```bash
python src/ingestion/load_data.py
```

### 7. Train the model

```bash
python src/models/train.py
```

---

## Running the Project

```bash
streamlit run src/dashboard/app.py
```

The app opens at `http://localhost:8501`. Use the sidebar to navigate between pages.

---

## Snapshots

Screenshots are stored in the [`snapshots/`](snapshots/) folder. See [`snapshots/README.md`](snapshots/README.md) for naming conventions.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data store | PostgreSQL 14 + psycopg3 |
| Data processing | pandas |
| ML | scikit-learn, XGBoost |
| Model persistence | joblib |
| Dashboard | Streamlit + Plotly |
| Styling | Custom CSS (glassmorphism, CSS animations) |
| Config | python-dotenv |
