# SpamShield AI

Machine-learning web app that classifies text as **Spam** or **Ham** using TF-IDF features and a Linear SVM, with a Streamlit interface.

---

## Features

- TF-IDF vectorization (unigrams + bigrams)
- Model comparison: Naive Bayes, Logistic Regression, Linear SVM
- Best model selected by spam F1-score (Linear SVM)
- Confidence scores in the UI
- Pre-trained pipeline (`spam_detector.pkl`)

---

## Tech stack

Streamlit · scikit-learn · joblib · pandas · Python

---

## Project structure

```
spam-detection/
├── app.py                 # Streamlit app
├── spam_detector.pkl      # Trained pipeline
├── model_results.csv      # Model comparison metrics
├── confusion_matrix.png
├── model_comparison.png
└── requirements.txt
```

---

## How to download and run

```bash
git clone https://github.com/HAMADA-LAB/spam-detection.git
cd spam-detection
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit shows (usually http://localhost:8501).

Trained primarily on SMS-style messages.
