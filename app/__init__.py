import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate, jwt  
from app.config import DevelopmentConfig
from app.routes.auth_routes import auth_bp
from app.models import User, Ticket, Comment, AuditLog
from app.routes.ticket import ticket_bp
from app.routes.admin_routes import admin_bp
from .extensions import ma




load_dotenv()

def create_app():
    app = Flask(__name__)


    config_name = os.getenv("FLASK_CONFIG") or "DevelopmentConfig"
    app.config.from_object(f"app.config.{config_name}")

    ma.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

  
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ticket_bp)
    app.register_blueprint(admin_bp)

    from app.models import User, Ticket, Comment, AuditLog

    @app.route("/")
    def index():
        return {"message": "Support Ticket API running Successfully!"}

    return app
