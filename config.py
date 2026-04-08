import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "smart_encryption_secret"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

DATABASE = os.path.join(BASE_DIR, "database", "users.db")

MODEL_PATH = os.path.join(BASE_DIR, "models", "ai_key_rotation_model.pkl")