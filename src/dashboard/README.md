# src/dashboard/

Streamlit multi-page dashboard for the Customer Intelligence Platform.

## Structure

```
dashboard/
├── app.py              # Entry point — main Overview page
├── utils.py            # Cached loaders for DB data and ML model
├── styles.py           # All CSS, HTML component builders
└── pages/
    ├── Model_Performance.py   # Confusion matrix + probability distribution
    └── Predict.py             # Single-customer churn probability predictor
```

## Running

```bash
# from the project root
streamlit run src/dashboard/app.py
```

Streamlit auto-discovers `pages/` and adds them to the sidebar.

## Pages

### Overview (`app.py`)
- KPI metric cards: total customers, overall churn rate, average tenure
- Bar chart: churn rate by contract type
- Bar chart: churn rate by internet service
- Bar chart: churn rate by tenure bucket (0–6 mo, 6–12 mo, 1–2 yr, 2+ yr)

### Model Performance (`pages/Model_Performance.py`)
- Threshold slider (0.0 – 1.0, default 0.35) — dynamically recomputes all metrics
- KPI cards: accuracy, recall (churn class), precision (churn class)
- Confusion matrix heatmap (Plotly)
- Predicted probability distribution histogram with threshold line

### Predict (`pages/Predict.py`)
- Input form: contract type, internet service, payment method, tenure, monthly charges
- Outputs an animated SVG churn probability ring
- Colour-coded risk card (red > 50%, amber 30–50%, green < 30%)
- AI retention suggestions conditionally shown for high-risk predictions

## Shared Utilities

### `utils.py`
- `get_data()` — `@st.cache_data` wrapper around `load_data()` to avoid repeated DB queries
- `get_model()` — `@st.cache_resource` wrapper to load the XGBoost `.pkl` once per session

### `styles.py`
- `inject_global_styles()` — injects global CSS (glassmorphism cards, gradient header, animations)
- `render_header(title, subtitle)` — animated gradient header component
- `render_metric_card(icon, label, value, delay)` — glassmorphism KPI card HTML
- `render_section_divider()` — gradient horizontal rule
- `render_churn_ring(probability)` — SVG animated probability ring
- `render_result_card(probability)` — high/low risk result card
- `get_plotly_layout()` — consistent dark Plotly theme dict shared across all charts
