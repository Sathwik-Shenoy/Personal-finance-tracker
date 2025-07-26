from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from typing import Optional

from app.models import db, User
from app.config import config

def create_app(config_name=None) -> Flask:
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Migrate for database migrations
    migrate = Migrate()
    migrate.init_app(app, db)
    
    # Initialize CORS for API access
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize Flask-Login for web interface
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        """Load user by ID for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Initialize JWT for API authentication
    jwt = JWTManager()
    jwt.init_app(app)
    
    # JWT token blacklist checker
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        from app.api.auth import blacklisted_tokens
        jti = jwt_payload['jti']
        return jti in blacklisted_tokens
    
    # Ensure upload folder exists
    upload_path: str = app.config['UPLOAD_FOLDER']  # type: ignore
    os.makedirs(upload_path, exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register web routes (existing functionality)
    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    
    # Register API routes (new functionality)
    from app.api import init_api
    init_api(app)
    
    return app
