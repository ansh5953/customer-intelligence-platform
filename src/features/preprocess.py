from src.database.connection import create_connection
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def load_data():
    """Pull the full customers table from PostgreSQL into a DataFrame."""
    conn = create_connection()
    df = pd.read_sql('SELECT * FROM customers;', conn)
    conn.close()
    return df


def clean_data(df):
    """Drop non-predictive columns and extract the customer_id index."""
    customer_id = df['customer_id']
    # created_at is an audit timestamp, not a behavioural feature
    df = df.drop(columns=['customer_id', 'created_at'])
    return df, customer_id


def split_features_target(df):
    """Separate feature matrix X from binary churn label y."""
    y = df['churn']
    x = df.drop(columns='churn')
    return x, y


def encode_features(x):
    """One-hot encode all categorical columns.

    drop_first=True avoids the dummy variable trap (perfect multicollinearity)
    that would hurt Logistic Regression and inflate tree-model feature counts.
    """
    return pd.get_dummies(x, drop_first=True)


def prepare_data():
    """Full preprocessing pipeline — returns (x_encoded, y, customer_id)."""
    df = load_data()
    df, customer_id = clean_data(df)
    x, y = split_features_target(df)
    x_encoded = encode_features(x)
    return x_encoded, y, customer_id
