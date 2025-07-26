"""
Transactions API endpoints
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import pandas as pd

from app.models import Transaction, User, db

api = Namespace('transactions', description='Transaction operations')

# API Models
transaction_model = api.model('Transaction', {
    'date': fields.String(required=True, description='Transaction date (YYYY-MM-DD)'),
    'category': fields.String(required=True, description='Transaction category'),
    'amount': fields.Float(required=True, description='Amount in ₹ (negative for expenses)'),
    'description': fields.String(description='Transaction description')
})

transaction_response_model = api.model('TransactionResponse', {
    'id': fields.Integer(description='Transaction ID'),
    'date': fields.String(description='Transaction date'),
    'category': fields.String(description='Category'),
    'amount': fields.Float(description='Amount in ₹'),
    'description': fields.String(description='Description'),
    'created_at': fields.String(description='Created timestamp')
})

@api.route('/')
class TransactionList(Resource):
    @jwt_required()
    @api.marshal_list_with(transaction_response_model)
    def get(self):
        """Get all transactions for current user"""
        current_user_id = get_jwt_identity()
        
        # Query parameters for filtering
        parser = api.parser()
        parser.add_argument('category', type=str, help='Filter by category')
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')
        parser.add_argument('limit', type=int, default=100, help='Number of transactions to return')
        parser.add_argument('offset', type=int, default=0, help='Offset for pagination')
        
        args = parser.parse_args()
        
        query = Transaction.query.filter_by(user_id=current_user_id)
        
        # Apply filters
        if args['category']:
            query = query.filter(Transaction.category.ilike(f"%{args['category']}%"))
        
        if args['start_date']:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= start_date)
        
        if args['end_date']:
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= end_date)
        
        # Apply pagination and ordering
        transactions = query.order_by(Transaction.date.desc())\
                          .offset(args['offset'])\
                          .limit(args['limit'])\
                          .all()
        
        return [{
            'id': t.id,
            'date': t.date.strftime('%Y-%m-%d'),
            'category': t.category,
            'amount': t.amount,
            'description': t.description,
            'created_at': t.created_at.isoformat()
        } for t in transactions]
    
    @jwt_required()
    @api.expect(transaction_model)
    @api.marshal_with(transaction_response_model)
    def post(self):
        """Create a new transaction"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        try:
            transaction_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        
        transaction = Transaction(
            date=transaction_date,
            category=data['category'],
            amount=float(data['amount']),
            description=data.get('description', ''),
            user_id=current_user_id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return {
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category': transaction.category,
            'amount': transaction.amount,
            'description': transaction.description,
            'created_at': transaction.created_at.isoformat()
        }, 201

@api.route('/<int:transaction_id>')
class TransactionItem(Resource):
    @jwt_required()
    @api.marshal_with(transaction_response_model)
    def get(self, transaction_id):
        """Get a specific transaction"""
        current_user_id = get_jwt_identity()
        transaction = Transaction.query.filter_by(
            id=transaction_id, 
            user_id=current_user_id
        ).first()
        
        if not transaction:
            api.abort(404, 'Transaction not found')
        
        return {
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category': transaction.category,
            'amount': transaction.amount,
            'description': transaction.description,
            'created_at': transaction.created_at.isoformat()
        }
    
    @jwt_required()
    @api.expect(transaction_model)
    @api.marshal_with(transaction_response_model)
    def put(self, transaction_id):
        """Update a transaction"""
        current_user_id = get_jwt_identity()
        transaction = Transaction.query.filter_by(
            id=transaction_id, 
            user_id=current_user_id
        ).first()
        
        if not transaction:
            api.abort(404, 'Transaction not found')
        
        data = request.get_json()
        
        try:
            transaction.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            api.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        
        transaction.category = data['category']
        transaction.amount = float(data['amount'])
        transaction.description = data.get('description', '')
        
        db.session.commit()
        
        return {
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category': transaction.category,
            'amount': transaction.amount,
            'description': transaction.description,
            'created_at': transaction.created_at.isoformat()
        }
    
    @jwt_required()
    def delete(self, transaction_id):
        """Delete a transaction"""
        current_user_id = get_jwt_identity()
        transaction = Transaction.query.filter_by(
            id=transaction_id, 
            user_id=current_user_id
        ).first()
        
        if not transaction:
            api.abort(404, 'Transaction not found')
        
        db.session.delete(transaction)
        db.session.commit()
        
        return {'message': 'Transaction deleted successfully'}

@api.route('/upload')
class TransactionUpload(Resource):
    @jwt_required()
    def post(self):
        """Upload transactions from CSV"""
        current_user_id = get_jwt_identity()
        
        # Check if file is present
        if 'file' not in request.files:
            api.abort(400, 'No file provided')
        
        file = request.files['file']
        if file.filename == '':
            api.abort(400, 'No file selected')
        
        try:
            # Read CSV file
            df = pd.read_csv(file)
            
            # Validate required columns
            required_columns = ['date', 'category', 'amount']
            if not all(col in df.columns for col in required_columns):
                api.abort(400, f'CSV must contain columns: {", ".join(required_columns)}')
            
            transactions_created = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    transaction_date = pd.to_datetime(row['date']).date()
                    
                    transaction = Transaction(
                        date=transaction_date,
                        category=str(row['category']),
                        amount=float(row['amount']),
                        description=str(row.get('description', '')),
                        user_id=current_user_id
                    )
                    
                    db.session.add(transaction)
                    transactions_created += 1
                    
                except Exception as e:
                    errors.append(f'Row {index + 1}: {str(e)}')
            
            db.session.commit()
            
            return {
                'message': f'Successfully imported {transactions_created} transactions',
                'transactions_created': transactions_created,
                'errors': errors
            }, 201
            
        except Exception as e:
            api.abort(400, f'Error processing CSV: {str(e)}')

@api.route('/summary')
class TransactionSummary(Resource):
    @jwt_required()
    def get(self):
        """Get financial summary for current user"""
        current_user_id = get_jwt_identity()
        
        transactions = Transaction.query.filter_by(user_id=current_user_id).all()
        
        if not transactions:
            return {
                'total_income': 0,
                'total_expenses': 0,
                'net_balance': 0,
                'transaction_count': 0,
                'categories': []
            }
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
        net_balance = total_income - total_expenses
        
        # Category breakdown
        categories = {}
        for t in transactions:
            if t.category not in categories:
                categories[t.category] = {'total': 0, 'count': 0}
            categories[t.category]['total'] += t.amount
            categories[t.category]['count'] += 1
        
        category_list = [
            {
                'category': cat,
                'total': data['total'],
                'count': data['count']
            }
            for cat, data in categories.items()
        ]
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'transaction_count': len(transactions),
            'categories': category_list
        }
