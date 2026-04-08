from encryption.key_manager import generate_key
from models.key_rotation_predictor import predict_rotation

def rotate_key(login_attempts,data_access,threat_score):

    result = predict_rotation(login_attempts,data_access,threat_score)

    if result == 1:
        new_key = generate_key()
        return "Key Rotated"

    else:
        return "No Rotation Needed"