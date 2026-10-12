"""
train_model.py — Trains multiple ML models on the symptom-disease dataset,
compares them on the held-out Testing.csv, and saves the best one.

Run this once before starting the Flask app:
    python train_model.py
"""

import json
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

DATA_DIR = "data"
MODEL_DIR = "trained_model"

print("Loading data...")
train_df = pd.read_csv(f"{DATA_DIR}/Training.csv")
test_df = pd.read_csv(f"{DATA_DIR}/Testing.csv")

# The training CSV has a trailing unnamed column in some versions — drop if present
train_df = train_df.loc[:, ~train_df.columns.str.contains("^Unnamed")]
test_df = test_df.loc[:, ~test_df.columns.str.contains("^Unnamed")]

symptom_columns = [c for c in train_df.columns if c != "prognosis"]

X_train = train_df[symptom_columns]
y_train_raw = train_df["prognosis"]
X_test = test_df[symptom_columns]
y_test_raw = test_df["prognosis"]

# Encode disease names -> integers
label_encoder = LabelEncoder()
label_encoder.fit(pd.concat([y_train_raw, y_test_raw]))
y_train = label_encoder.transform(y_train_raw)
y_test = label_encoder.transform(y_test_raw)

print(f"{len(symptom_columns)} symptoms, {len(label_encoder.classes_)} diseases")
print(f"Train rows: {len(X_train)}, Test rows: {len(X_test)}\n")

# --- Train + compare multiple models ---
candidates = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Naive Bayes": GaussianNB(),
    "SVM (linear)": SVC(kernel="linear", probability=True, random_state=42),
}

results = []
trained_models = {}

for name, model in candidates.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average="weighted", zero_division=0)
    rec = recall_score(y_test, preds, average="weighted", zero_division=0)
    f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

    results.append({"model": name, "accuracy": acc, "precision": prec, "recall": rec, "f1": f1})
    trained_models[name] = model
    print(f"{name:22s} | acc={acc:.4f}  precision={prec:.4f}  recall={rec:.4f}  f1={f1:.4f}")

# --- Pick the best model by accuracy ---
best = max(results, key=lambda r: r["accuracy"])
best_model_name = best["model"]
best_model = trained_models[best_model_name]

print(f"\nBest model: {best_model_name} (accuracy={best['accuracy']:.4f})")

# --- Save everything the Flask app needs ---
import os
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(best_model, f"{MODEL_DIR}/model.pkl")
joblib.dump(label_encoder, f"{MODEL_DIR}/label_encoder.pkl")

with open(f"{MODEL_DIR}/symptoms.json", "w") as f:
    json.dump(symptom_columns, f, indent=2)

with open(f"{MODEL_DIR}/model_comparison.json", "w") as f:
    json.dump({"results": results, "best_model": best_model_name}, f, indent=2)

print(f"\nSaved model + encoder + symptom list to {MODEL_DIR}/")
print("Now run: python app.py")
