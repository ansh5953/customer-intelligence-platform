# models/

Serialised ML artefacts produced by `src/models/train.py` (or `src/analysis/explore.py`).

## Files

| File | Description |
|---|---|
| `xgb_model.pkl` | Trained `XGBClassifier` — 100 estimators, learning rate 0.1, random state 42 |
| `model_columns.pkl` | Python list of feature column names in the exact order the model was trained on |

## Why `model_columns.pkl` exists

After one-hot encoding (`pd.get_dummies`), the feature matrix has a fixed set of columns. At inference time (Predict page), the user only fills in 5 fields. `model_columns.pkl` lets us `reindex` the sparse input DataFrame to match the full training schema — filling missing columns with `0`.

## Regenerating Models

```bash
# from the project root
python src/models/train.py
```

Both `.pkl` files will be overwritten.

## Model Performance (at threshold = 0.35)

| Metric | Value |
|---|---|
| Accuracy | ~81% |
| Churn Recall | ~79% |
| Churn Precision | ~60% |
| No-Churn Recall | ~83% |

> Threshold 0.35 was chosen to maximise churn recall (catching churners matters more than false positives in retention campaigns).
