"""
explore.py — model comparison scratch script.

Trains Logistic Regression, Random Forest, and XGBoost on the same
80/20 stratified split and prints classification reports so their
recall / precision trade-offs can be compared directly.

Results summary (threshold=0.35 for XGBoost):
  - Logistic Regression : accuracy ~80%, churn recall ~55%
  - Random Forest        : accuracy ~79%, churn recall ~48%
  - XGBoost              : accuracy ~81%, churn recall ~79%  ← chosen for production

XGBoost was selected because churn recall — catching actual churners —
is the primary business metric.  Missing a churner (false negative) is
more costly than a false positive in a retention campaign context.
"""

from src.database.connection import create_connection
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

conn = create_connection()
df = pd.read_sql('SELECT * FROM customers;', conn)
conn.close()

customer_id = df['customer_id']
df = df.drop(columns=['customer_id', 'created_at'])

y = df['churn']
x = df.drop(columns='churn')

x_encoded = pd.get_dummies(x, drop_first=True)

x_train, x_test, y_train, y_test = train_test_split(
    x_encoded, y, test_size=0.2, stratify=y, random_state=42
)

# ── Logistic Regression (baseline) ────────────────────────────────────────────
# Requires scaling; class_weight='balanced' compensates for 73/27 imbalance.
# scaler = StandardScaler()
# x_train_scaled = scaler.fit_transform(x_train)
# x_test_scaled = scaler.transform(x_test)
# lr = LogisticRegression(max_iter=1000, class_weight='balanced')
# lr.fit(x_train_scaled, y_train)
# y_pred_lr = lr.predict(x_test_scaled)
# print("=== Logistic Regression ===")
# print(classification_report(y_test, y_pred_lr))

# ── Random Forest ─────────────────────────────────────────────────────────────
# balanced_subsample weights each tree's bootstrap sample independently.
# model_rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced_subsample')
# model_rf.fit(x_train, y_train)
# y_pred_rf = model_rf.predict(x_test)
# print("=== Random Forest ===")
# print(classification_report(y_test, y_pred_rf))

# ── XGBoost (production model) ────────────────────────────────────────────────
# Lowering the decision threshold from 0.5 → 0.35 trades precision for recall,
# which is the right trade-off for a churn-retention use case.
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42,
)
model.fit(x_train, y_train)

joblib.dump(model, 'models/xgb_model.pkl')
joblib.dump(x_encoded.columns.tolist(), 'models/model_columns.pkl')

probs = model.predict_proba(x_test)[:, 1]
threshold_pred = (probs >= 0.35)

print("=== XGBoost (threshold=0.35) ===")
print(confusion_matrix(y_test, threshold_pred))
print(classification_report(y_test, threshold_pred))
print("Accuracy:", accuracy_score(y_test, threshold_pred))

# Sanity-check: reloaded model should produce identical probabilities
loaded_model = joblib.load('models/xgb_model.pkl')
loaded_probs = loaded_model.predict_proba(x_test)[:, 1]
assert (loaded_probs == probs).all(), "Model round-trip mismatch!"
print("Model persistence verified.")
