from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import os
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models import db, Transaction
from sqlalchemy import func

main = Blueprint('main', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    """Homepage with welcome message"""
    return render_template('index.html')

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Handle file upload and CSV parsing"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        # Check if file is allowed and save it
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Parse CSV using pandas
                df = pd.read_csv(filepath)
                
                # Validate required columns
                required_columns = ['date', 'category', 'amount', 'description']
                if not all(col in df.columns for col in required_columns):
                    flash(f'CSV must contain columns: {", ".join(required_columns)}')
                    return redirect(request.url)
                
                # Save transactions to database
                saved_count = 0
                for _, row in df.iterrows():
                    try:
                        # Parse date
                        transaction_date = pd.to_datetime(row['date']).date()
                        
                        # Create new transaction
                        transaction = Transaction(
                            date=transaction_date,
                            category=str(row['category']),
                            amount=float(row['amount']),
                            description=str(row['description']) if pd.notna(row['description']) else '',
                            user_id=current_user.id
                        )
                        
                        db.session.add(transaction)
                        saved_count += 1
                    except Exception as e:
                        flash(f'Error processing row: {e}')
                        continue
                
                # Commit all transactions
                db.session.commit()
                
                # Convert DataFrame to HTML table
                table_html = df.to_html(classes='table table-striped table-bordered', 
                                      table_id='data-table', 
                                      escape=False)
                
                flash(f'File {filename} uploaded successfully! Saved {saved_count} transactions to database.')
                return render_template('upload.html', 
                                     table_data=table_html, 
                                     filename=filename,
                                     saved_count=saved_count)
                
            except Exception as e:
                flash(f'Error parsing CSV file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect(request.url)
    
    # GET request - show upload form
    return render_template('upload.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard to display all transactions and analytics"""
    import plotly
    import plotly.graph_objs as go
    import json
    
    # Get all transactions for current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    # Calculate category summaries for current user
    category_totals = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    ).filter_by(user_id=current_user.id).group_by(Transaction.category).all()
    
    # Calculate monthly summaries for current user
    monthly_totals = db.session.query(
        func.strftime('%Y-%m', Transaction.date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by(func.strftime('%Y-%m', Transaction.date)).all()
    
    # Calculate total income and expenses for current user
    total_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.amount > 0, Transaction.user_id == current_user.id
    ).scalar() or 0
    total_expenses = abs(db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.amount < 0, Transaction.user_id == current_user.id
    ).scalar() or 0)
    net_balance = total_income - total_expenses
    
    # Prepare data for Plotly charts
    charts_json = {}
    
    if category_totals:
        # Category Spending Pie Chart (only expenses)
        expense_categories = [(cat.category, abs(cat.total)) for cat in category_totals if cat.total < 0]
        if expense_categories:
            categories, amounts = zip(*expense_categories)
            
            pie_chart = go.Figure(data=[go.Pie(
                labels=categories,
                values=amounts,
                hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:.2f}<br>Percentage: %{percent}<extra></extra>',
                textinfo='label+percent',
                textposition='auto'
            )])
            pie_chart.update_layout(
                title='Spending by Category',
                font=dict(size=12),
                height=400
            )
            charts_json['category_pie'] = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    if monthly_totals:
        # Monthly Totals Bar Chart
        months, totals = zip(*[(mt.month, mt.total) for mt in monthly_totals])
        
        bar_chart = go.Figure(data=[go.Bar(
            x=months,
            y=totals,
            marker_color=['green' if total >= 0 else 'red' for total in totals],
            hovertemplate='<b>%{x}</b><br>Total: ₹%{y:.2f}<extra></extra>',
            text=[f'₹{total:.2f}' for total in totals],
            textposition='auto'
        )])
        bar_chart.update_layout(
            title='Monthly Financial Summary',
            xaxis_title='Month',
            yaxis_title='Amount (₹)',
            font=dict(size=12),
            height=400
        )
        charts_json['monthly_bar'] = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Income vs Expenses Comparison Chart
    if total_income > 0 or total_expenses > 0:
        comparison_chart = go.Figure(data=[go.Bar(
            x=['Income', 'Expenses', 'Net Balance'],
            y=[total_income, -total_expenses, net_balance],
            marker_color=['green', 'red', 'blue' if net_balance >= 0 else 'orange'],
            hovertemplate='<b>%{x}</b><br>Amount: ₹%{y:.2f}<extra></extra>',
            text=[f'₹{total_income:.2f}', f'₹{total_expenses:.2f}', f'₹{net_balance:.2f}'],
            textposition='auto'
        )])
        comparison_chart.update_layout(
            title='Financial Overview',
            yaxis_title='Amount (₹)',
            font=dict(size=12),
            height=400
        )
        charts_json['overview_bar'] = json.dumps(comparison_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('dashboard.html',
                         transactions=transactions,
                         category_totals=category_totals,
                         monthly_totals=monthly_totals,
                         total_income=total_income,
                         total_expenses=total_expenses,
                         net_balance=net_balance,
                         charts_json=charts_json)

@main.route('/report')
@login_required
def generate_report():
    """Generate and download PDF report of user's transactions"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    from io import BytesIO
    import datetime
    
    # Get user's transactions
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    if not transactions:
        flash('No transactions found to generate report.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Calculate summaries
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
    net_balance = total_income - total_expenses
    
    # Category summaries
    category_summary = {}
    for transaction in transactions:
        category = transaction.category
        if category not in category_summary:
            category_summary[category] = {'total': 0, 'count': 0}
        category_summary[category]['total'] += transaction.amount
        category_summary[category]['count'] += 1
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    title = Paragraph(f"Financial Report for {current_user.username}", title_style)
    elements.append(title)
    
    # Report date
    report_date = Paragraph(f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
    elements.append(report_date)
    elements.append(Spacer(1, 20))
    
    # Summary section
    summary_style = ParagraphStyle(
        'SummaryHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkgreen
    )
    
    summary_header = Paragraph("Financial Summary", summary_style)
    elements.append(summary_header)
    
    summary_data = [
        ['Metric', 'Amount'],
        ['Total Income', f'₹{total_income:,.2f}'],
        ['Total Expenses', f'₹{total_expenses:,.2f}'],
        ['Net Balance', f'₹{net_balance:,.2f}'],
        ['Total Transactions', str(len(transactions))]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Category breakdown
    if category_summary:
        category_header = Paragraph("Category Breakdown", summary_style)
        elements.append(category_header)
        
        category_data = [['Category', 'Total Amount', 'Transaction Count']]
        for category, data in sorted(category_summary.items()):
            category_data.append([
                category,
                f'₹{data["total"]:,.2f}',
                str(data['count'])
            ])
        
        category_table = Table(category_data, colWidths=[2*inch, 2*inch, 1.5*inch])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(category_table)
        elements.append(PageBreak())
    
    # Transaction details
    transaction_header = Paragraph("Transaction Details", summary_style)
    elements.append(transaction_header)
    
    # Transaction table header
    transaction_data = [['Date', 'Category', 'Amount', 'Description']]
    
    # Add transactions (limit to recent 50 for PDF size)
    recent_transactions = transactions[:50] if len(transactions) > 50 else transactions
    
    for transaction in recent_transactions:
        transaction_data.append([
            transaction.date.strftime('%Y-%m-%d'),
            transaction.category,
            f'₹{transaction.amount:,.2f}',
            transaction.description[:30] + '...' if len(transaction.description or '') > 30 else (transaction.description or '')
        ])
    
    if len(transactions) > 50:
        transaction_data.append(['...', f'({len(transactions) - 50} more transactions)', '', ''])
    
    transaction_table = Table(transaction_data, colWidths=[1.2*inch, 1.5*inch, 1.3*inch, 2.5*inch])
    transaction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),  # Right align amounts
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(transaction_table)
    
    # Build PDF
    doc.build(elements)
    
    # FileResponse
    buffer.seek(0)
    
    from flask import make_response
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=financial_report_{current_user.username}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response

@main.route('/email_report', methods=['GET', 'POST'])
@login_required
def email_report():
    """Send PDF report via email"""
    if request.method == 'POST':
        recipient_email = request.form.get('email')
        
        if not recipient_email:
            flash('Please provide an email address.', 'danger')
            return redirect(url_for('main.email_report'))
        
        try:
            # Generate PDF report in memory
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.units import inch
            from io import BytesIO
            import datetime
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            
            # Get user's transactions
            transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
            
            if not transactions:
                flash('No transactions found to generate report.', 'warning')
                return redirect(url_for('main.dashboard'))
            
            # Calculate summaries
            total_income = sum(t.amount for t in transactions if t.amount > 0)
            total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
            net_balance = total_income - total_expenses
            
            # Create PDF in memory (simplified version)
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(f"Financial Report for {current_user.username}", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Summary
            summary_data = [
                ['Total Income', f'₹{total_income:,.2f}'],
                ['Total Expenses', f'₹{total_expenses:,.2f}'],
                ['Net Balance', f'₹{net_balance:,.2f}'],
                ['Total Transactions', str(len(transactions))]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(summary_table)
            
            # Build PDF
            doc.build(elements)
            buffer.seek(0)
            
            # Email setup
            from flask import current_app
            
            # Check if email is configured
            mail_username = current_app.config.get('MAIL_USERNAME')
            if not mail_username or mail_username == 'demo@example.com':
                flash('Email service is not configured. For demo purposes, report will be generated instead.', 'info')
                # Instead of failing, let's redirect to the PDF download
                return redirect(url_for('main.generate_report'))
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = recipient_email
            msg['Subject'] = f"Financial Report - {current_user.username}"
            
            # Email body
            body = f"""
            Dear {current_user.username},
            
            Please find attached your financial report generated on {datetime.datetime.now().strftime('%B %d, %Y')}.
            
            Summary:
            - Total Income: ₹{total_income:,.2f}
            - Total Expenses: ₹{total_expenses:,.2f}
            - Net Balance: ₹{net_balance:,.2f}
            - Total Transactions: {len(transactions)}
            
            Best regards,
            Personal Finance Tracker Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDF
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(buffer.getvalue())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename=financial_report_{current_user.username}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
            )
            msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
            server.starttls()
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            text = msg.as_string()
            server.sendmail(current_app.config['MAIL_USERNAME'], recipient_email, text)
            server.quit()
            
            flash(f'Report successfully sent to {recipient_email}!', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'danger')
            return redirect(url_for('main.email_report'))
    
    # GET request - show email form
    return render_template('email_report.html')
