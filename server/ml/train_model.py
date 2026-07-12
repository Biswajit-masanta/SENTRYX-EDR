import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# ==========================
# Load Dataset
# ==========================
data = pd.read_csv("dataset.csv")


# ==========================
# Features and Labels
# ==========================
X = data.drop("risk_label", axis=1)
y = data["risk_label"]


# ==========================
# Split Dataset
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================
# Create Model
# ==========================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# ==========================
# Train Model
# ==========================
model.fit(X_train, y_train)


# ==========================
# Test Model
# ==========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy * 100:.2f}%\n")

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ==========================
# Save Model
# ==========================
joblib.dump(model, "model.pkl")

# Save feature names
joblib.dump(list(X.columns), "features.pkl")

print("\nModel saved as model.pkl")
print("Feature list saved as features.pkl")