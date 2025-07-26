#!/usr/bin/env python3
"""
API Testing Script for Personal Finance Tracker
Test all API endpoints with sample data
"""
import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:5000/api/v1"
headers = {"Content-Type": "application/json"}

def test_api():
    """Test all API endpoints"""
    print("🚀 Testing Personal Finance Tracker API")
    print("=" * 50)
    
    # Test data
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    test_transactions = [
        {
            "date": "2024-01-15",
            "category": "Salary",
            "amount": 50000.00,
            "description": "Monthly salary"
        },
        {
            "date": "2024-01-16",
            "category": "Food",
            "amount": -500.50,
            "description": "Lunch at restaurant"
        },
        {
            "date": "2024-01-17",
            "category": "Transport",
            "amount": -250.30,
            "description": "Auto rickshaw"
        }
    ]
    
    access_token = None
    
    try:
        # 1. Test user registration
        print("1️⃣ Testing user registration...")
        response = requests.post(f"{BASE_URL}/auth/register", 
                               json=test_user, headers=headers)
        if response.status_code == 201:
            data = response.json()
            access_token = data.get('access_token')
            print(f"✅ Registration successful! User ID: {data['user']['id']}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
        
        # Set authorization header
        auth_headers = {**headers, "Authorization": f"Bearer {access_token}"}
        
        # 2. Test user login
        print("\n2️⃣ Testing user login...")
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", 
                               json=login_data, headers=headers)
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print(f"❌ Login failed: {response.text}")
        
        # 3. Test user profile
        print("\n3️⃣ Testing user profile...")
        response = requests.get(f"{BASE_URL}/auth/profile", headers=auth_headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profile retrieved: {profile['username']} ({profile['email']})")
        else:
            print(f"❌ Profile retrieval failed: {response.text}")
        
        # 4. Test transaction creation
        print("\n4️⃣ Testing transaction creation...")
        created_transactions = []
        for transaction in test_transactions:
            response = requests.post(f"{BASE_URL}/transactions/", 
                                   json=transaction, headers=auth_headers)
            if response.status_code == 201:
                created = response.json()
                created_transactions.append(created)
                print(f"✅ Transaction created: ₹{created['amount']} - {created['category']}")
            else:
                print(f"❌ Transaction creation failed: {response.text}")
        
        # 5. Test transaction retrieval
        print("\n5️⃣ Testing transaction retrieval...")
        response = requests.get(f"{BASE_URL}/transactions/", headers=auth_headers)
        if response.status_code == 200:
            transactions = response.json()
            print(f"✅ Retrieved {len(transactions)} transactions")
        else:
            print(f"❌ Transaction retrieval failed: {response.text}")
        
        # 6. Test transaction summary
        print("\n6️⃣ Testing transaction summary...")
        response = requests.get(f"{BASE_URL}/transactions/summary", headers=auth_headers)
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Summary: Income=₹{summary['total_income']}, "
                  f"Expenses=₹{summary['total_expenses']}, "
                  f"Balance=₹{summary['net_balance']}")
        else:
            print(f"❌ Summary retrieval failed: {response.text}")
        
        # 7. Test reports
        print("\n7️⃣ Testing reports...")
        response = requests.get(f"{BASE_URL}/reports/summary", headers=auth_headers)
        if response.status_code == 200:
            report = response.json()
            print(f"✅ Report generated with {report['transaction_count']} transactions")
        else:
            print(f"❌ Report generation failed: {response.text}")
        
        # 8. Test charts
        print("\n8️⃣ Testing chart data...")
        response = requests.get(f"{BASE_URL}/reports/charts", headers=auth_headers)
        if response.status_code == 200:
            charts = response.json()
            print(f"✅ Chart data generated with {len(charts['charts'])} charts")
        else:
            print(f"❌ Chart data retrieval failed: {response.text}")
        
        # 9. Test transaction update
        if created_transactions:
            print("\n9️⃣ Testing transaction update...")
            transaction_id = created_transactions[0]['id']
            update_data = {
                "date": "2024-01-15",
                "category": "Salary Updated",
                "amount": 55000.00,
                "description": "Updated monthly salary"
            }
            response = requests.put(f"{BASE_URL}/transactions/{transaction_id}", 
                                  json=update_data, headers=auth_headers)
            if response.status_code == 200:
                updated = response.json()
                print(f"✅ Transaction updated: ₹{updated['amount']} - {updated['category']}")
            else:
                print(f"❌ Transaction update failed: {response.text}")
        
        # 10. Test logout
        print("\n🔟 Testing logout...")
        response = requests.post(f"{BASE_URL}/auth/logout", headers=auth_headers)
        if response.status_code == 200:
            print("✅ Logout successful!")
        else:
            print(f"❌ Logout failed: {response.text}")
        
        print("\n🎉 API testing completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_api()
