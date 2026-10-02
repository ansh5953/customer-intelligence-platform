# src/

Source code for the Customer Intelligence Platform, organised into five sub-packages:

| Package | Responsibility |
|---|---|
| `preprocessing/` | Step 1 — Clean the raw CSV before it touches the database |
| `ingestion/` | Step 2 — Bulk-load the cleaned CSV into PostgreSQL |
| `database/` | Shared DB connection helper used by all other packages |
| `features/` | Step 3 — Query DB, engineer features, encode categoricals |
| `models/` | Step 4 — Train XGBoost and save artefacts to `models/` |
| `analysis/` | Scratch exploration, model comparison experiments |
| `dashboard/` | Streamlit multi-page app (3 pages) |

## Execution Order

Run in this order the first time you set up the project:

```
clean_data.py  →  load_data.py  →  train.py  →  streamlit run dashboard/app.py
```
