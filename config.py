import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "focus_center_secret_key_2024"
    SQLALCHEMY_DATABASE_URI = "sqlite:///focus_center.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size