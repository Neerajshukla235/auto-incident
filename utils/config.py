"""Configuration management for LogAgent."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # LLM Configuration
    MODEL_NAME = "gemini-pro"
    TEMPERATURE = 0.7
    MAX_TOKENS = 2048
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")


# Initialize config
config = Config()
