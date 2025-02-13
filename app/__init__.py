from flask import Flask
import os
from . import db
from .main import main_bp
from .games import game_bp
from .logs import log_bp
from .auth import auth_bp
from .account import account_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Ensure DATABASE is set
    app.config.from_mapping(
        SECRET_KEY='change-this-secret',
        DATABASE=os.path.join(app.instance_path, 'flask_app.sqlite'),  
        SESSION_TYPE='filesystem'
    )

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize DB before registering blueprints
    db.init_app(app)

    # Register Blueprints AFTER DB setup
    app.register_blueprint(main_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)

    return app
