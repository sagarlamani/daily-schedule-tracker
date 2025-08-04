#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints
"""

import requests
import json
from datetime import datetime, time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_root():
    """Test root endpoint."""
    print("🔍 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_register():
    """Test user registration."""
    print("🔍 Testing user registration...")
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login():
    """Test user login."""
    print("🔍 Testing user login...")
    credentials = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=credentials)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Token received: {token[:20]}...")
        return token
    else:
        print(f"Response: {response.json()}")
    print()
    return None

def test_templates():
    """Test templates endpoint."""
    print("🔍 Testing templates endpoint...")
    response = requests.get(f"{BASE_URL}/api/templates")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_protected_endpoints(token):
    """Test protected endpoints with token."""
    if not token:
        print("❌ No token available, skipping protected endpoints")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🔍 Testing protected endpoints...")
    
    # Test get tasks
    print("Testing GET /api/tasks...")
    response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test get streaks
    print("Testing GET /api/streaks...")
    response = requests.get(f"{BASE_URL}/api/streaks", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test analytics
    print("Testing GET /api/analytics/summary...")
    response = requests.get(f"{BASE_URL}/api/analytics/summary", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests."""
    print("🚀 Starting API tests...")
    print("=" * 50)
    
    try:
        test_health()
        test_root()
        test_register()
        token = test_login()
        test_templates()
        test_protected_endpoints(token)
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main() 