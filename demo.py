#!/usr/bin/env python3
"""
Demo script for Personal Finance Tracker
This script demonstrates the key features and provides setup guidance.
"""

import os
import sys

def print_banner():
    print("=" * 60)
    print("PERSONAL FINANCE TRACKER - DEMO SETUP")
    print("=" * 60)
    print()

def check_dependencies():
    print("Checking dependencies...")
    
    # List of (import_name, display_name) tuples
    required_packages = [
        ('flask', 'Flask'),
        ('pandas', 'Pandas'),
        ('plotly', 'Plotly'),
        ('reportlab', 'ReportLab'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_login', 'Flask-Login'),
        ('werkzeug', 'Werkzeug')
    ]
    
    missing = []
    for import_name, display_name in required_packages:
        try:
            __import__(import_name)
            print(f"   [OK] {display_name}")
        except ImportError:
            print(f"   [MISSING] {display_name}")
            missing.append(display_name)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("   All dependencies installed!")
    return True

def show_features():
    print("\nKEY FEATURES:")
    print("   • User Registration & Authentication")
    print("   • CSV File Upload & Processing")
    print("   • Interactive Dashboard with Plotly Charts")
    print("   • PDF Report Generation")
    print("   • Email Report Delivery")
    print("   • Transaction Categorization")
    print("   • Financial Analytics & Summaries")

def show_usage_guide():
    print("\nQUICK START GUIDE:")
    print("   1. Register a new account at /auth/register")
    print("   2. Login with your credentials")
    print("   3. Upload sample CSV data (sample_data.csv provided)")
    print("   4. Explore the interactive dashboard")
    print("   5. Generate and download PDF reports")
    print("   6. (Optional) Configure email for report delivery")

def show_email_setup():
    print("\nEMAIL SETUP (Optional):")
    print("   For Gmail users:")
    print("   1. Enable 2-factor authentication")
    print("   2. Generate App Password in Google Account settings")
    print("   3. Set environment variables:")
    print("      export MAIL_USERNAME='your_email@gmail.com'")
    print("      export MAIL_PASSWORD='your_app_password'")
    print()
    print("   Current status:")
    mail_user = os.environ.get('MAIL_USERNAME')
    mail_pass = os.environ.get('MAIL_PASSWORD')
    
    if mail_user and mail_pass:
        print(f"   [CONFIGURED] Email configured for: {mail_user}")
    else:
        print("   [NOT CONFIGURED] Email not configured (email features will be disabled)")

def show_sample_data():
    print("\nSAMPLE DATA:")
    print("   A sample CSV file (sample_data.csv) is included with:")
    print("   • Various transaction types (income, expenses)")
    print("   • Multiple categories (Food, Transport, Shopping, etc.)")
    print("   • Realistic transaction amounts")
    print("   • Date range for testing monthly trends")

def main():
    print_banner()
    
    # Check if running from correct directory
    if not os.path.exists('run.py'):
        print("ERROR: Please run this script from the project root directory")
        print("   (where run.py is located)")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies first.")
        sys.exit(1)
    
    show_features()
    show_usage_guide()
    show_email_setup()
    show_sample_data()
    
    print("\nREADY TO START:")
    print("   Run: python run.py")
    print("   Then visit: http://localhost:5001")
    print()
    print("Have fun tracking your finances!")
    print("=" * 60)

if __name__ == "__main__":
    main()
