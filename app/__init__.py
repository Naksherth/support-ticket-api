import os
from flask import Flask 
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app=Flask(__name__)

    config_name = os.getenv("FLASK_CONFIG") or "DevelopmentConfig"
    app.config.from_object(f"app.config.{config_name}")

    #Extensions


    #Register Blueprints

    @app.route("/")
    def index():
        return {"message":"Support Ticket API running Successfully!"}
      
    return app