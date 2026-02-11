import os
from dotenv import load_dotenv

# Load the .env file once at the top
load_dotenv()

class Config:
    """Centralized configuration for the application."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG")
    TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER=os.getenv("TWILIO_PHONE_NUMBER")
    TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    DB_NAME = os.getenv('DB_NAME', 'agrisense_db')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv('DB_PORT', '3306')

secretKeys = Config()
