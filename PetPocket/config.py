
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from project root .env file
load_dotenv(os.path.join(BASE_DIR, '..', '.env'))

class Config:
    # --------------------------------------------------
    # FLASK CORE
    # --------------------------------------------------
    SECRET_KEY = os.environ.get('SECRET_KEY', 'petswale_super_secret_key_2025')

    DEBUG = False
    TESTING = False

    # --------------------------------------------------
    # DATABASE (LOCAL MYSQL ON SAME VPS)
    # --------------------------------------------------
    # Make sure this DB + user exists in MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        "mysql+pymysql://petswale_user:StrongPassword123!@localhost/petswale_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_timeout": 30,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
    }

    # --------------------------------------------------
    # SESSION / SECURITY
    # --------------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False   # set TRUE only after HTTPS

    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'petswale_password_salt')

    # --------------------------------------------------
    # CSRF
    # --------------------------------------------------
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = False     # enable after HTTPS

    # --------------------------------------------------
    # RAZORPAY
    # --------------------------------------------------
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_live_RGkEP4XjZZVrxv')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'LR0Iqe9U0XVEPzsxYo78MmOe')

    # --------------------------------------------------
    # GOOGLE OAUTH
    # --------------------------------------------------
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', "1047039162052-7e0fgrt2prvkcl2ta0ojao471ifs0c01.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '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')

    # --------------------------------------------------
    # FILE UPLOADS
    # --------------------------------------------------
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")


class DevelopmentConfig(Config):
    """Local development configuration"""
    DEBUG = True
    TESTING = False
    
    # Use existing petpocket.db database with preloaded data
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'petpocket.db')}"
    
    # Less strict security for local dev
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_SSL_STRICT = False
    
    # Local host
    HOST = "127.0.0.1"
    PORT = 5000


class ProductionConfig(Config):
    """Production configuration (Render)"""
    DEBUG = False
    TESTING = False
    
    # Production host settings
    HOST = "0.0.0.0"
    PORT = 5000  # Render expects port 5000
    
    # Production database (use environment variable)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 
        "postgresql://user:password@localhost:5432/database")


# Dictionary to easily access configs
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
