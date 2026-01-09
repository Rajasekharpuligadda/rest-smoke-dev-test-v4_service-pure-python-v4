from flask import Flask
from a2wsgi import WSGIMiddleware
from .routes import main as main_blueprint
from .health import health as health_blueprint
from app.settings import Settings
from app.logger import logger, configure_logging_and_tracing

def init_settings(app: Flask):
    if not hasattr(app, "extensions"):
        app.extensions = {}

    settings = Settings()
    app.config.from_object(settings)
    app.extensions["settings"] = settings

def create_app():
    """
    Flask application factory function.
    """

    app = Flask(__name__)
    init_settings(app)
    configure_logging_and_tracing(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(health_blueprint)

    logger.info("Flask service setup is completed.")
    return WSGIMiddleware(app)