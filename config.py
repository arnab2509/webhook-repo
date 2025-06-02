import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'github_webhooks')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key')
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')