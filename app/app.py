# app/__init__.py

import os
from flask import Flask, render_template
from . import db
from .game_logic import classify_game_state, get_empty_board

# Import your blueprints
from .main import main_bp
from .games import game_bp
from .logs import log_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Config
    app.config.from_mapping(
        SECRET_KEY='change-this-secret',
        DATABASE=os.path.join(app.instance_path, 'flask_app.sqlite'),
    )

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize DB
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)  
    app.register_blueprint(game_bp)  # Your /api routes for games
    app.register_blueprint(log_bp)   # For logs viewer

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    return app

# Optional: if you want to run "python -m app" directly:
if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
