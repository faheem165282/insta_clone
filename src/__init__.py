import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # Register blueprints
    from src.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from src.creator import bp as creator_bp
    app.register_blueprint(creator_bp, url_prefix='/creator')
    
    from src.consumer import bp as consumer_bp
    app.register_blueprint(consumer_bp, url_prefix='/consumer')
    
    from src.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
