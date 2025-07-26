"""
API package initialization
"""
from flask_restx import Api
from flask_jwt_extended import JWTManager

# Initialize extensions
api = Api(
    title='Personal Finance Tracker API',
    version='1.0',
    description='REST API for Personal Finance Tracker with Indian Rupee support',
    doc='/api/docs/',
    prefix='/api/v1'
)

jwt = JWTManager()

def init_api(app):
    """Initialize API extensions with Flask app"""
    api.init_app(app)
    jwt.init_app(app)
    
    # Import namespaces after initialization to avoid circular imports
    from .auth import api as auth_ns
    from .transactions import api as transactions_ns
    from .reports import api as reports_ns
    
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(transactions_ns, path='/transactions')
    api.add_namespace(reports_ns, path='/reports')
