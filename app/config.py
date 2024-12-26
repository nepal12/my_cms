import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Set it in .env file")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set for database connection. Set it in .env file")