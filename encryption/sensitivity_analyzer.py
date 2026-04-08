import joblib
import os

# Load Model and Vectorizer
MODEL_PATH = 'models/sensitivity_model.pkl'
VECTORIZER_PATH = 'models/tfidf_vectorizer.pkl'

def analyze_sensitivity(text):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        # Fallback to a simple heuristic if model is missing
        sensitive_keywords = ['password', 'ssn', 'credit card', 'secret', 'confidential', 'private key']
        if any(kw in text.lower() for kw in sensitive_keywords):
            return 1.0
        return 0.0

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    
    X = vectorizer.transform([text])
    score = model.predict_proba(X)[0][1] # Probability of being sensitive (label 1)
    
    return float(score)
