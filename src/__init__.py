from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()
cors = CORS()

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

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    db.init_app(app)
    cors.init_app(app)

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    # Register the blueprints in the app
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    @app.errorhandler(404)
    def page_not_found(error):
        return {"error": "Not found", "message": str(error)}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad request", "message": str(error)}, 400
