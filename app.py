
import streamlit as st
import joblib

st.set_page_config(page_title="SpamShield AI", page_icon="📩", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load("spam_detector.pkl")

model = load_model()

st.title("📩 SpamShield AI")
st.subheader("Spam Email and SMS Detection")
st.write("Paste a message below. The model predicts whether it is spam or a legitimate message.")

message = st.text_area(
    "Message to analyze",
    height=160,
    placeholder="Example: Congratulations! You have won a free prize. Claim it now!"
)

if st.button("Analyze Message", type="primary"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        prediction = model.predict([message])[0]

        if prediction == "spam":
            st.error("⚠️ Prediction: SPAM")
        else:
            st.success("✅ Prediction: HAM (Legitimate Message)")

        classifier = model.named_steps["model"]

        if hasattr(classifier, "predict_proba"):
            probabilities = model.predict_proba([message])[0]
            spam_index = list(model.classes_).index("spam")
            spam_probability = probabilities[spam_index] * 100
            st.metric("Spam Probability", f"{spam_probability:.1f}%")
        else:
            score = model.decision_function([message])[0]
            st.metric("Model Confidence Score", f"{score:.2f}")

st.divider()

st.markdown("""
### About this project
- **Task:** Binary text classification (Spam vs Ham)
- **Feature extraction:** TF-IDF with unigrams and bigrams
- **Models compared:** Naive Bayes, Logistic Regression, and Linear SVM
- **Selection rule:** Highest spam F1-score on unseen test data

### Important limitation
This model was trained on SMS-style messages. A production email filter would also use sender reputation, URLs, email headers, attachments, and newer data.
""")
