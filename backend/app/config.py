import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    SONG_FEATURES_FOLDER = 'song_features'
    DATABASE_URI = 'sqlite:///database/songs.db'