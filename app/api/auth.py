"""
Authentication API endpoints with JWT
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import check_password_hash
from datetime import timedelta

from app.models import User, db

api = Namespace('auth', description='Authentication operations')

# API Models for request/response validation
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username or email'),
    'password': fields.String(required=True, description='Password')
})

token_response_model = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user': fields.Raw(description='User information')
})

# Blacklist for JWT tokens
blacklisted_tokens = set()

@api.route('/register')
class UserRegistration(Resource):
    @api.expect(user_model)
    @api.marshal_with(token_response_model)
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            api.abort(400, 'Username already exists')
        
        if User.query.filter_by(email=data['email']).first():
            api.abort(400, 'Email already exists')
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, 201

@api.route('/login')
class UserLogin(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_response_model)
    def post(self):
        """Login user and return JWT tokens"""
        data = request.get_json()
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == data['username']) | 
            (User.email == data['username'])
        ).first()
        
        if not user or not user.check_password(data['password']):
            api.abort(401, 'Invalid credentials')
        
        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }

@api.route('/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        current_user_id = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=24)
        )
        return {'access_token': new_token}

@api.route('/logout')
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """Logout user by blacklisting token"""
        jti = get_jwt()['jti']
        blacklisted_tokens.add(jti)
        return {'message': 'Successfully logged out'}

@api.route('/profile')
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Get current user profile"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            api.abort(404, 'User not found')
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }

# JWT token blacklist checker
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens
