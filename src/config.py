from abc import ABC

class Config(ABC):
    """Initial configuration settings."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration settings."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb_dev.db"

class TestingConfig(Config):
    """Testing configuration settings."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    """Production configuration settings."""
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/hbnb_prod"
