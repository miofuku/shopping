# Initialize Flask application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import importlib.util


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def load_config(config_path):
    spec = importlib.util.spec_from_file_location("config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    return config_module.Config


def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')

    # Dynamically load the configuration
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'default.py')
    config = load_config(config_path)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        print("Creating database...")
        from app.models import Item  # Import here to avoid circular imports
        db.create_all()

        print("Loading csv data...")
        from app.services import csv_loader
        csv_loader.load_csv_data()

    from app.routes import main
    app.register_blueprint(main)

    return app
