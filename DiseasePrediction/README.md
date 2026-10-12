# Disease Prediction System (ML-powered symptom checker)

A real, working final-year project: predicts likely diseases from selected
symptoms using a model trained on a labeled medical dataset (132 symptoms →
41 diseases). Unlike the repo this was based on, every part here is fully
implemented — training script, saved model, and a working Flask web app.

## How it works
1. `train_model.py` trains 5 different ML models (Logistic Regression,
   Decision Tree, Random Forest, Naive Bayes, SVM) on `data/Training.csv`,
   evaluates each on `data/Testing.csv`, and saves the best one.
2. `app.py` loads that saved model and serves a web UI where you check off
   symptoms and get a predicted disease + confidence + top-3 alternatives.

## Real model comparison (from this dataset)

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 100% | 100% | 100% | 100% |
| Decision Tree | 100% | 100% | 100% | 100% |
| Random Forest | 100% | 100% | 100% | 100% |
| Naive Bayes | 100% | 100% | 100% | 100% |
| SVM (linear) | 100% | 100% | 100% | 100% |

All five hit 100% because this particular dataset's symptom patterns are
cleanly separable per disease (a known property of this Kaggle dataset —
each disease has a near-fixed symptom signature and the test set is small,
41 rows). **This is a real result from actually running the code**, not a
placeholder — but it's worth knowing *why* it's this high, because a
professor or interviewer will likely ask. Good talking points:
- The dataset is synthetic/curated, not real patient records — real-world
  clinical data would have noise, overlapping symptoms, and missing values.
- To make the project more defensible, you could add: k-fold cross
  validation, a confusion matrix, or a noisier/real dataset as a stretch
  goal.

Logistic Regression was saved as the "best" model (first among the tied
models) — you can force a different one by editing the `candidates` dict
order in `train_model.py`.

## Project structure
```
DiseasePrediction/
├── data/
│   ├── Training.csv          4920 rows, 132 symptoms, 41 diseases
│   └── Testing.csv             held-out evaluation set
├── train_model.py                trains + compares 5 models, saves the best
├── trained_model/                  created after training
│   ├── model.pkl
│   ├── label_encoder.pkl
│   ├── symptoms.json
│   └── model_comparison.json
├── app.py                              Flask app + /api/predict endpoint
├── templates/index.html
├── static/css/style.css
├── static/js/script.js                   search + AJAX prediction
├── requirements.txt
└── README.md
```

## How to run

```bash
cd DiseasePrediction
pip install -r requirements.txt

# Step 1: train the model (creates trained_model/ folder)
python train_model.py

# Step 2: start the web app
python app.py
```

Open **http://127.0.0.1:5002** in your browser. Search/select symptoms,
click "Analyze Symptoms", and you'll get the predicted disease with
confidence + top-3 alternatives.

## Notes for your final-year submission
- No database needed — model and symptom list load from files at startup.
- The disclaimer on the page ("educational / decision-support only") is
  intentional and worth keeping — it's standard practice for any medical
  ML demo and professors expect to see it.
- If you want this upgraded to match the original AI-Health360 idea
  (multi-disease dashboard, login, PDF reports, MySQL), that's a natural
  next step — just ask.
