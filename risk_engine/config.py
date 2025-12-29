import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration (SQLite for local development)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'risk_management.db')
    DB_USER = os.getenv('DB_USER', 'risk_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'risk_password')
    
    # API Configuration
    BALLERINE_API_URL = os.getenv('BALLERINE_API_URL', 'http://localhost:3000/api/v1')
    BALLERINE_API_KEY = os.getenv('BALLERINE_API_KEY', '')
    CISO_API_URL = os.getenv('CISO_API_URL', 'http://localhost:8000/api')
    CISO_API_TOKEN = os.getenv('CISO_API_TOKEN', '')
    
    # Risk Thresholds
    HIGH_RISK_THRESHOLD = float(os.getenv('HIGH_RISK_THRESHOLD', 0.8))
    MEDIUM_RISK_THRESHOLD = float(os.getenv('MEDIUM_RISK_THRESHOLD', 0.5))
    AMOUNT_THRESHOLD_HIGH = float(os.getenv('AMOUNT_THRESHOLD_HIGH', 10000000))
    AMOUNT_THRESHOLD_MEDIUM = float(os.getenv('AMOUNT_THRESHOLD_MEDIUM', 1000000))
    
    # Monitoring Settings
    POLLING_INTERVAL_SECONDS = int(os.getenv('POLLING_INTERVAL_SECONDS', 30))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
    
    @property
    def database_url(self):
        # Use SQLite for local development
        return f"sqlite:///{self.DB_NAME}"