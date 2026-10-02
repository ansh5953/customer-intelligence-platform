# data/

Raw and processed datasets for the Customer Intelligence Platform.

## Files

| File | Description |
|---|---|
| `telco_churn.csv` | Raw IBM Telco Customer Churn dataset — 7043 rows, 21 columns |
| `processed/telco_churn_cleaned.csv` | Cleaned output produced by `src/preprocessing/clean_data.py` |

## Dataset Schema (Raw)

| Column | Type | Notes |
|---|---|---|
| customerID | string | Unique customer identifier |
| gender | string | Male / Female |
| SeniorCitizen | int | 0 or 1 |
| Partner | string | Yes / No |
| Dependents | string | Yes / No |
| tenure | int | Months as a customer |
| PhoneService | string | Yes / No |
| MultipleLines | string | Yes / No / No phone service |
| InternetService | string | DSL / Fiber optic / No |
| OnlineSecurity | string | Yes / No / No internet service |
| OnlineBackup | string | Yes / No / No internet service |
| DeviceProtection | string | Yes / No / No internet service |
| TechSupport | string | Yes / No / No internet service |
| StreamingTV | string | Yes / No / No internet service |
| StreamingMovies | string | Yes / No / No internet service |
| Contract | string | Month-to-month / One year / Two year |
| PaperlessBilling | string | Yes / No |
| PaymentMethod | string | Electronic check / Mailed check / Bank transfer / Credit card |
| MonthlyCharges | float | Monthly bill amount in USD |
| TotalCharges | string* | Cumulative charges — contains empty strings for new customers |
| Churn | string | Yes / No — prediction target |

*`TotalCharges` is stored as a string in the raw file and must be coerced to float during cleaning (11 rows have empty strings).

## Cleaning Changes (raw → processed)

- `TotalCharges` stripped and cast to `float`; empty strings replaced with `0`
- Column names converted from CamelCase to `snake_case`
- `customerID` renamed to `customer_id`
- Yes/No columns converted to Python booleans
- Whitespace stripped from all service columns
