import pandas as pd
from pathlib import Path
import re

# Resolve paths relative to project root so the script works from any CWD
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
path = project_root / 'data' / 'telco_churn.csv'
path_cleaned = project_root / 'data' / 'processed' / 'telco_churn_cleaned.csv'

df = pd.read_csv(path)

# TotalCharges is stored as a string in the raw CSV; new customers (tenure=0)
# have empty strings instead of '0', which pd.to_numeric must handle.
df['TotalCharges'] = df['TotalCharges'].str.strip()
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(0)

# Convert CamelCase column names to snake_case (e.g. MonthlyCharges → Monthly_Charges)
# then lowercase the result so every name is fully lowercase snake_case.
df.columns = [
    re.sub(r'(?<=[a-z])(?=[A-Z])', '_', column)
    for column in df.columns
]
df.columns = [
    column.replace("customer_ID", "customer_id")
    for column in df.columns
]
df.columns = df.columns.str.lower()

# These columns store binary yes/no values — map them to Python booleans
# so PostgreSQL can store them as BOOLEAN without a cast at insert time.
bool_cols = ['partner', 'dependents', 'phone_service', 'paperless_billing', 'churn']
df[bool_cols] = df[bool_cols].replace({'Yes': True, 'No': False})

# Strip any residual whitespace from the multi-value service columns
# (e.g. "No phone service" vs "No phone service " would otherwise be two categories)
service_cols = [
    'multiple_lines', 'online_security', 'online_backup',
    'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies',
]
df[service_cols] = df[service_cols].apply(lambda col: col.str.strip())

df.to_csv(path_cleaned, index=False)
print(f"Cleaned data written to {path_cleaned}")
