from src.features.preprocess import prepare_data
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib


def train_model():
    """Train XGBoost on the full customer dataset and persist the artefacts."""
    x_encoded, y, customer_id = prepare_data()

    # Stratify preserves the ~73/27 class ratio in both splits
    x_train, x_test, y_train, y_test = train_test_split(
        x_encoded, y, test_size=0.2, stratify=y, random_state=42
    )

    model = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(x_train, y_train)

    # Persist both model and its column schema — the Predict page needs the
    # column list to reindex sparse user input to the full feature space.
    joblib.dump(model, 'models/xgb_model.pkl')
    joblib.dump(x_encoded.columns.tolist(), 'models/model_columns.pkl')

    return model, x_test, y_test


if __name__ == "__main__":
    train_model()
    print('Model trained and saved to models/xgb_model.pkl')
