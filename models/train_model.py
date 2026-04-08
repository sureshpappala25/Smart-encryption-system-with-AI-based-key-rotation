import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("C:/Users/Admin/Music/Smart encryption system with AI based key rotation/dataset/network_activity.csv")

X = data[["login_attempts","data_access","threat_score"]]
y = data["key_rotation_needed"]

model = RandomForestClassifier()
model.fit(X,y)

joblib.dump(model,"ai_key_rotation_model.pkl")

print("Model trained and saved")