# sql/

PostgreSQL DDL scripts for the Customer Intelligence Platform.

## Files

| File | Purpose |
|---|---|
| `schema.sql` | Creates the `customers` table |

## Running the Schema

```bash
# Create the database first (one time)
createdb -U postgres customer_intelligence

# Then apply the schema
psql -U postgres -d customer_intelligence -f sql/schema.sql
```

## Table: `customers`

| Column | Type | Constraint | Notes |
|---|---|---|---|
| customer_id | VARCHAR(50) | PRIMARY KEY | Unique customer identifier |
| gender | VARCHAR(20) | | Male / Female |
| senior_citizen | SMALLINT | | 0 or 1 |
| partner | BOOLEAN | | Has a partner |
| dependents | BOOLEAN | | Has dependents |
| tenure | INTEGER | CHECK >= 0 | Months as customer |
| phone_service | BOOLEAN | | Has phone service |
| multiple_lines | VARCHAR(30) | | Phone line type |
| internet_service | VARCHAR(30) | | DSL / Fiber optic / No |
| online_security | VARCHAR(30) | | Add-on status |
| online_backup | VARCHAR(30) | | Add-on status |
| device_protection | VARCHAR(30) | | Add-on status |
| tech_support | VARCHAR(30) | | Add-on status |
| streaming_tv | VARCHAR(30) | | Add-on status |
| streaming_movies | VARCHAR(30) | | Add-on status |
| contract | VARCHAR(50) | | Contract term |
| paperless_billing | BOOLEAN | | Paperless billing opted in |
| payment_method | VARCHAR(100) | | Payment channel |
| monthly_charges | NUMERIC(10,2) | | USD |
| total_charges | NUMERIC(12,2) | | USD; 0 for brand-new customers |
| churn | BOOLEAN | | Prediction target |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Auto-set at insert time |
