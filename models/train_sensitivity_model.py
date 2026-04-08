import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
df = pd.read_csv("dataset/sensitivity_data.csv")

# Preprocessing
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Train Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save Model and Vectorizer
if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/sensitivity_model.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')

print("Sensitivity model and vectorizer trained and saved successfully.")
