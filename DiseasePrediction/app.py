"""
app.py — Disease Prediction web app.
Loads the model trained by train_model.py and serves a symptom-checker UI.
"""

import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MODEL_DIR = "trained_model"

# --- Load trained artifacts (created by train_model.py) ---
model = joblib.load(f"{MODEL_DIR}/model.pkl")
label_encoder = joblib.load(f"{MODEL_DIR}/label_encoder.pkl")

with open(f"{MODEL_DIR}/symptoms.json") as f:
    SYMPTOMS = json.load(f)

with open(f"{MODEL_DIR}/model_comparison.json") as f:
    MODEL_INFO = json.load(f)


def prettify(symptom: str) -> str:
    """Turn 'skin_rash' into 'Skin Rash' for display."""
    return symptom.replace("_", " ").strip().title()


@app.route("/")
def index():
    # group symptoms alphabetically for a scannable checkbox grid
    display_symptoms = sorted(
        [{"key": s, "label": prettify(s)} for s in SYMPTOMS],
        key=lambda x: x["label"],
    )
    return render_template(
        "index.html",
        symptoms=display_symptoms,
        best_model=MODEL_INFO["best_model"],
    )


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    selected = set(data.get("symptoms", []))

    if not selected:
        return jsonify({"error": "Select at least one symptom."}), 400

    # build the feature vector in the exact column order the model expects
    # (a DataFrame with matching column names avoids sklearn's feature-name warning)
    vector = pd.DataFrame(
        [[1 if s in selected else 0 for s in SYMPTOMS]], columns=SYMPTOMS
    )

    probs = model.predict_proba(vector)[0]
    top_idx = np.argsort(probs)[::-1][:3]

    top3 = [
        {
            "disease": label_encoder.inverse_transform([i])[0],
            "confidence": round(float(probs[i]) * 100, 1),
        }
        for i in top_idx
    ]

    return jsonify({
        "prediction": top3[0]["disease"],
        "confidence": top3[0]["confidence"],
        "top3": top3,
        "symptoms_used": sorted(prettify(s) for s in selected),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5002)
