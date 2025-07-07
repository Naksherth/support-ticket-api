import os

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","super-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.getenv("DEV_DATABASE_URI","sqlite://dev.db")
    
class ProductionConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI=os.getenv("PROD_DATABASE_URI")

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI="sqlite://:memory:"     
