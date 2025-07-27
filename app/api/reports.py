"""
Reports API endpoints
"""
from flask import request, send_file
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from io import BytesIO
import json
import plotly
import plotly.graph_objs as go
from datetime import datetime, timedelta
from sqlalchemy import func

from app.models import Transaction, User, db

api = Namespace('reports', description='Report generation operations')

# API Models
report_request_model = api.model('ReportRequest', {
    'start_date': fields.String(description='Start date (YYYY-MM-DD)'),
    'end_date': fields.String(description='End date (YYYY-MM-DD)'),
    'categories': fields.List(fields.String, description='Filter by categories')
})

@api.route('/summary')
class ReportSummary(Resource):
    @jwt_required()
    def get(self):
        """Get detailed financial summary report"""
        current_user_id = get_jwt_identity()
        
        # Query parameters
        parser = api.parser()
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')
        args = parser.parse_args()
        
        query = Transaction.query.filter_by(user_id=current_user_id)
        
        # Apply date filters
        if args['start_date']:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= start_date)
        
        if args['end_date']:
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.all()
        
        if not transactions:
            return {
                'total_income': 0,
                'total_expenses': 0,
                'net_balance': 0,
                'transaction_count': 0,
                'monthly_breakdown': [],
                'category_breakdown': [],
                'top_expenses': [],
                'income_sources': []
            }
        
        # Basic calculations
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
        net_balance = total_income - total_expenses
        
        # Monthly breakdown
        monthly_data = {}
        for t in transactions:
            month_key = t.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {'income': 0, 'expenses': 0}
            
            if t.amount > 0:
                monthly_data[month_key]['income'] += t.amount
            else:
                monthly_data[month_key]['expenses'] += abs(t.amount)
        
        monthly_breakdown = [
            {
                'month': month,
                'income': data['income'],
                'expenses': data['expenses'],
                'net': data['income'] - data['expenses']
            }
            for month, data in sorted(monthly_data.items())
        ]
        
        # Category breakdown
        category_data = {}
        for t in transactions:
            if t.category not in category_data:
                category_data[t.category] = {'total': 0, 'count': 0}
            category_data[t.category]['total'] += t.amount
            category_data[t.category]['count'] += 1
        
        category_breakdown = [
            {
                'category': cat,
                'total': data['total'],
                'count': data['count'],
                'percentage': (abs(data['total']) / (total_income + total_expenses)) * 100 if (total_income + total_expenses) > 0 else 0
            }
            for cat, data in category_data.items()
        ]
        
        # Top expenses (largest expense transactions)
        top_expenses = [
            {
                'date': t.date.strftime('%Y-%m-%d'),
                'category': t.category,
                'amount': abs(t.amount),
                'description': t.description
            }
            for t in sorted([t for t in transactions if t.amount < 0], 
                          key=lambda x: abs(x.amount), reverse=True)[:10]
        ]
        
        # Income sources
        income_sources = [
            {
                'date': t.date.strftime('%Y-%m-%d'),
                'category': t.category,
                'amount': t.amount,
                'description': t.description
            }
            for t in sorted([t for t in transactions if t.amount > 0], 
                          key=lambda x: x.amount, reverse=True)[:10]
        ]
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'transaction_count': len(transactions),
            'monthly_breakdown': monthly_breakdown,
            'category_breakdown': category_breakdown,
            'top_expenses': top_expenses,
            'income_sources': income_sources
        }

@api.route('/charts')
class ReportCharts(Resource):
    @jwt_required()
    def get(self):
        """Get chart data for dashboard visualization"""
        current_user_id = get_jwt_identity()
        
        transactions = Transaction.query.filter_by(user_id=current_user_id)\
                                      .order_by(Transaction.date.desc())\
                                      .all()
        
        if not transactions:
            return {'charts': {}}
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
        net_balance = total_income - total_expenses
        
        charts = {}
        
        # 1. Financial Overview Bar Chart
        overview_chart = go.Figure(data=[
            go.Bar(
                x=['Income', 'Expenses', 'Net Balance'],
                y=[total_income, -total_expenses, net_balance],
                marker_color=['green', 'red', 'blue' if net_balance >= 0 else 'orange'],
                hovertemplate='<b>%{x}</b><br>Amount: ₹%{y:.2f}<extra></extra>',
                text=[f'₹{total_income:.2f}', f'₹{total_expenses:.2f}', f'₹{net_balance:.2f}'],
                textposition='auto'
            )
        ])
        overview_chart.update_layout(
            title='Financial Overview',
            yaxis_title='Amount (₹)',
            font=dict(size=12),
            height=400
        )
        charts['overview'] = json.loads(json.dumps(overview_chart, cls=plotly.utils.PlotlyJSONEncoder))
        
        # 2. Category Pie Chart (expenses only)
        expense_categories = {}
        for t in transactions:
            if t.amount < 0:  # Expenses only
                category = t.category
                if category not in expense_categories:
                    expense_categories[category] = 0
                expense_categories[category] += abs(t.amount)
        
        if expense_categories:
            pie_chart = go.Figure(data=[
                go.Pie(
                    labels=list(expense_categories.keys()),
                    values=list(expense_categories.values()),
                    hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:.2f}<br>Percentage: %{percent}<extra></extra>',
                )
            ])
            pie_chart.update_layout(
                title='Expense Categories',
                font=dict(size=12),
                height=400
            )
            charts['categories'] = json.loads(json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder))
        
        # 3. Monthly Trend Chart
        monthly_data = {}
        for t in transactions:
            month_key = t.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = 0
            monthly_data[month_key] += t.amount
        
        if monthly_data:
            sorted_months = sorted(monthly_data.keys())
            totals = [monthly_data[month] for month in sorted_months]
            
            monthly_chart = go.Figure(data=[
                go.Bar(
                    x=sorted_months,
                    y=totals,
                    marker_color=['green' if total >= 0 else 'red' for total in totals],
                    hovertemplate='<b>%{x}</b><br>Total: ₹%{y:.2f}<extra></extra>',
                    text=[f'₹{total:.2f}' for total in totals],
                    textposition='auto'
                )
            ])
            monthly_chart.update_layout(
                title='Monthly Financial Summary',
                xaxis_title='Month',
                yaxis_title='Amount (₹)',
                font=dict(size=12),
                height=400
            )
            charts['monthly'] = json.loads(json.dumps(monthly_chart, cls=plotly.utils.PlotlyJSONEncoder))
        
        return {'charts': charts}

@api.route('/pdf')
class ReportPDF(Resource):
    @jwt_required()
    def post(self):
        """Generate and download PDF report"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        # Generate PDF using ReportLab
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.units import inch
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        elements.append(Paragraph("Personal Finance Report", title_style))
        elements.append(Paragraph(f"Generated for: {user.username}", styles['Normal']))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Get transactions
        transactions = Transaction.query.filter_by(user_id=current_user_id)\
                                      .order_by(Transaction.date.desc())\
                                      .all()
        
        if not transactions:
            elements.append(Paragraph("No transactions found.", styles['Normal']))
        else:
            # Summary
            total_income = sum(t.amount for t in transactions if t.amount > 0)
            total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
            net_balance = total_income - total_expenses
            
            summary_data = [
                ['Metric', 'Amount'],
                ['Total Income', f'₹{total_income:,.2f}'],
                ['Total Expenses', f'₹{total_expenses:,.2f}'],
                ['Net Balance', f'₹{net_balance:,.2f}'],
                ['Total Transactions', str(len(transactions))]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(Paragraph("Financial Summary", styles['Heading2']))
            elements.append(summary_table)
            elements.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'financial_report_{user.username}_{datetime.now().strftime("%Y%m%d")}.pdf',
            mimetype='application/pdf'
        )
