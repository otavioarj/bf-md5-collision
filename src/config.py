"""Application configuration management."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY: str = os.getenv('SECRET_KEY', os.urandom(24).hex())
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Challenge settings
    FLAG: str = os.getenv('FLAG', 'FLAG{example_flag_change_in_production}')
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', 1024 * 1024))  # 1MB
    
    # Security settings
    MAX_CONTENT_LENGTH: int = MAX_FILE_SIZE
    UPLOAD_TIMEOUT: int = int(os.getenv('UPLOAD_TIMEOUT', 30))
    
    # Brainfuck interpreter settings
    BF_MEMORY_SIZE: int = int(os.getenv('BF_MEMORY_SIZE', 30000))
    BF_TIMEOUT: int = int(os.getenv('BF_TIMEOUT', 5))
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT: str = os.getenv('RATE_LIMIT', '10 per minute')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    @classmethod
    def validate(cls):
        """Validate production configuration."""
        if cls.FLAG == 'FLAG{example_flag_change_in_production}':
            raise ValueError("Please set a production FLAG in environment variables")
        if len(cls.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")


def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        config = ProductionConfig()
        config.validate()
        return config
    
    return DevelopmentConfig()