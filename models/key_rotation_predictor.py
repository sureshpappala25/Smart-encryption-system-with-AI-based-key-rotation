import joblib
import config

model = joblib.load(config.MODEL_PATH)

def predict_rotation(login_attempts,data_access,threat_score):

    result = model.predict([[login_attempts,data_access,threat_score]])

    return result[0]