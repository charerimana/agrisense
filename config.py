import os
from dotenv import load_dotenv

# Load the .env file once at the top
load_dotenv()

class Config:
    """Centralized configuration for the application."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG")
    TWILIO_API_KEY = os.getenv("TWILIO_API_KEY")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Instantiate it so you can import the object directly
secretKeys = Config()
