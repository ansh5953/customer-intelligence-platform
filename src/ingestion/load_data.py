from src.database.connection import create_connection
import pandas as pd
from pathlib import Path

conn = create_connection()
cursor = conn.cursor()

current_path = Path(__file__).resolve()
project_root = current_path.parent.parent.parent
csv_path = project_root / 'data' / 'processed' / 'telco_churn_cleaned.csv'

df = pd.read_csv(csv_path)

# Convert the entire DataFrame into a list of tuples for batch insertion
records = [tuple(row) for row in df.to_numpy()]

# Parameterised INSERT — psycopg3 handles type casting for BOOLEAN and NUMERIC columns.
sql = '''
INSERT INTO customers(
    customer_id, gender, senior_citizen, partner, dependents,
    tenure, phone_service, multiple_lines, internet_service,
    online_security, online_backup, device_protection, tech_support,
    streaming_tv, streaming_movies, contract, paperless_billing,
    payment_method, monthly_charges, total_charges, churn
)
VALUES(
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
'''

# Upload all 7,043 rows in a single network request instead of a loop
print(f"Uploading {len(records)} rows in a single batch...")
cursor.executemany(sql, records)

conn.commit()
conn.close()
print("All rows loaded into PostgreSQL successfully.")