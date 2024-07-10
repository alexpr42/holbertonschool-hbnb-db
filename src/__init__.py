# src/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(env=None) -> Flask:
    """
    Create a Flask app with the given environment configuration.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    if env:
        app.config.from_object(env)
    else:
        app.config.from_object(os.environ.get('APP_SETTINGS', 'src.config.DevelopmentConfig'))

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    from src.models.base import Base
    Base.metadata.create_all(bind=db.engine)  # Create tables based on models

    # Further extensions can be added here

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp
    from src.routes.auth import auth_bp

    # Register the blueprints in the app
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(auth_bp)

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    )
    )
    app.errorhandler(400)(
        lambda e: (
            {"error": "Bad request", "message": str(e)}, 400
        )
    )
