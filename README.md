# SpamShield AI

A machine-learning web app that classifies text as **Spam** or **Ham** using TF-IDF features and a Linear SVM, served through a polished Streamlit UI.

---

## Features

- TF-IDF vectorization with unigrams and bigrams
- Model comparison: Naive Bayes, Logistic Regression, Linear SVM
- Best model selected by spam F1-score (Linear SVM)
- Interactive Streamlit interface with confidence scores
- Pre-trained pipeline shipped as `spam_detector.pkl`

---

## Tech stack

| Layer | Tool |
|-------|------|
| UI | Streamlit |
| ML | scikit-learn, joblib |
| Data | pandas |

---

## Project structure

```
spam-detection/
├── app.py                 # Streamlit application
├── spam_detector.pkl      # Trained pipeline (TF-IDF + Linear SVM)
├── model_results.csv      # Accuracy / precision / F1 comparison
├── confusion_matrix.png   # Evaluation chart
├── model_comparison.png   # Model comparison chart
├── requirements.txt
└── .devcontainer/         # Optional Codespaces / Dev Container
```

---

## Getting started

### Prerequisites

- Python 3.10+

### Install & run

```bash
git clone https://github.com/HAMADA-LAB/spam-detection.git
cd spam-detection
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).

---

## How it works

1. Input text is vectorized with TF-IDF (unigrams + bigrams).
2. A Linear SVM (chosen for highest spam F1) predicts `spam` or `ham`.
3. Confidence is derived from `decision_function` / probability estimates and shown in the UI.

**Limitation:** Trained on SMS-style messages. Production filters typically also use sender reputation, URL analysis, and fresher data.

---

## License

See repository for license details.
