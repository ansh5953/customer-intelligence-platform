# notebooks/

Jupyter notebooks for exploratory data analysis.

## Files

| Notebook | Description |
|---|---|
| `01_data_inspection.ipynb` | Initial look at raw CSV — shapes, dtypes, missing values, value distributions |

## Running Notebooks

```bash
# from project root with venv active
pip install jupyter
jupyter notebook notebooks/
```

## What to Explore

- Class distribution: ~73% no-churn vs ~27% churn (imbalanced)
- `TotalCharges` has 11 empty-string rows (new customers)
- Strong churn signals: Month-to-month contract, Fiber optic internet, Electronic check payment, short tenure
- Weak/no signal: gender, phone service (when not combined with other features)
