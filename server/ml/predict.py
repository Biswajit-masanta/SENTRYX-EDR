from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).parent

model = joblib.load(BASE_DIR / "model.pkl")
feature_names = joblib.load(BASE_DIR / "features.pkl")


def predict_risk(features):
    df = pd.DataFrame([features])
    df = df[feature_names]
    prediction = model.predict(df)[0]
    return prediction