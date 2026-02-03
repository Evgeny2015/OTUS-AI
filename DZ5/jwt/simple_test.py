#!/usr/bin/env python3
"""
Simple test for JWT Authentication Service
This script tests the JWT service without external dependencies.
"""

import json
import urllib.request
import urllib.parse

BASE_URL = "http://localhost:8000"

def make_request(method, endpoint, data=None, headers=None):
    """Make HTTP request"""
    url = f"{BASE_URL}{endpoint}"

    if headers is None:
        headers = {}

    if data and method in ['POST']:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def print_response(status, data, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {status}")
    print(f"Response: {json.dumps(data, indent=2)}")

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    status, data = make_request("GET", "/")
    print_response(status, data, "Health Check")

def test_generate_token():
    """Test token generation"""
    print("\nTesting token generation...")

    # Test with admin user
    status, data = make_request("POST", "/token", {
        "username": "admin",
        "password": "secret123"
    })
    print_response(status, data, "Token Generation (Admin)")

    if status == 200:
        return data["access_token"]
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
    status, data = make_request("GET", "/users/me", headers=headers)
    print_response(status, data, "Get Current User")

    # Test protected endpoint
    status, data = make_request("GET", "/protected", headers=headers)
    print_response(status, data, "Protected Endpoint")

    # Test token validation
    status, data = make_request("GET", "/validate", headers=headers)
    print_response(status, data, "Token Validation")

def test_invalid_token():
    """Test with invalid token"""
    print("\nTesting with invalid token...")

    headers = {"Authorization": "Bearer invalid_token_here"}
    status, data = make_request("GET", "/users/me", headers=headers)
    print_response(status, data, "Invalid Token Test")

def test_wrong_credentials():
    """Test with wrong credentials"""
    print("\nTesting with wrong credentials...")

    status, data = make_request("POST", "/token", {
        "username": "admin",
        "password": "wrong_password"
    })
    print_response(status, data, "Wrong Credentials Test")

def main():
    """Main test function"""
    print("JWT Authentication Service Simple Test")
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

    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()
