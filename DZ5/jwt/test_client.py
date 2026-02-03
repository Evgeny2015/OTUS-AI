#!/usr/bin/env python3
"""
Test client for JWT Authentication Service
This script demonstrates how to use the JWT authentication service.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Health Check")

def test_generate_token():
    """Test token generation"""
    print("\nTesting token generation...")

    # Test with admin user
    response = requests.post(f"{BASE_URL}/token", json={
        "username": "admin",
        "password": "secret123"
    })
    print_response(response, "Token Generation (Admin)")

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Failed to generate token")
        return None

def test_protected_endpoints():
    """Test protected endpoints with the generated token"""
    # First generate a token
    token = test_generate_token()
    if not token:
        print("No token available, skipping protected endpoint tests")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Test get current user
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_response(response, "Get Current User")

    # Test protected endpoint
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print_response(response, "Protected Endpoint")

    # Test token validation
    response = requests.get(f"{BASE_URL}/validate", headers=headers)
    print_response(response, "Token Validation")

def test_invalid_token():
    """Test with invalid token"""
    print("\nTesting with invalid token...")

    headers = {"Authorization": "Bearer invalid_token_here"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_response(response, "Invalid Token Test")

def test_wrong_credentials():
    """Test with wrong credentials"""
    print("\nTesting with wrong credentials...")

    response = requests.post(f"{BASE_URL}/token", json={
        "username": "admin",
        "password": "wrong_password"
    })
    print_response(response, "Wrong Credentials Test")

def main():
    """Main test function"""
    print("JWT Authentication Service Test Client")
    print("=" * 50)

    try:
        # Test health check
        test_health_check()

        # Test wrong credentials
        test_wrong_credentials()

        # Test token generation
        token = test_generate_token()

        # Test protected endpoints
        test_protected_endpoints(token)

        # Test invalid token
        test_invalid_token()

        print(f"\n{'='*50}")
        print("Test completed successfully!")
        print(f"{'='*50}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Please make sure the JWT service is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
