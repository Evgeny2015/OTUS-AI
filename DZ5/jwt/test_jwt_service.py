#!/usr/bin/env python3
"""
Pytest-compatible tests for JWT Authentication Service
"""
import json
import urllib.request
import urllib.parse
import requests
import pytest

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

def test_health_check():
    """Test the health check endpoint"""
    status, data = make_request("GET", "/")
    assert status == 200
    assert "service" in data
    assert data["service"] == "JWT Authentication Service"

def test_wrong_credentials():
    """Test with wrong credentials"""
    status, data = make_request("POST", "/token", {
        "username": "admin",
        "password": "wrong_password"
    })
    assert status == 401
    assert "detail" in data

def test_generate_token():
    """Test token generation"""
    status, data = make_request("POST", "/token", {
        "username": "admin",
        "password": "secret123"
    })
    assert status == 200
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

def test_invalid_token():
    """Test with invalid token"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    status, data = make_request("GET", "/users/me", headers=headers)
    assert status == 401
    assert "detail" in data

@pytest.fixture
def token():
    """Generate a valid token for testing"""
    status, data = make_request("POST", "/token", {
        "username": "admin",
        "password": "secret123"
    })
    assert status == 200
    assert "access_token" in data
    return data["access_token"]

def test_protected_endpoints_with_urllib(token):
    """Test protected endpoints with the generated token using urllib"""
    if not token:
        pytest.skip("No token available")

    headers = {"Authorization": f"Bearer {token}"}

    # Test get current user
    status, data = make_request("GET", "/users/me", headers=headers)
    assert status == 200
    assert "username" in data
    assert data["username"] == "admin"

    # Test protected endpoint
    status, data = make_request("GET", "/protected", headers=headers)
    assert status == 200
    assert "message" in data
    assert "user_info" in data

    # Test token validation
    status, data = make_request("GET", "/validate", headers=headers)
    assert status == 200
    assert "valid" in data
    assert data["valid"] == True
    assert "user" in data

def test_protected_endpoints_with_requests(token):
    """Test protected endpoints with the generated token using requests"""
    if not token:
        pytest.skip("No token available")

    headers = {"Authorization": f"Bearer {token}"}

    # Test get current user
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert data["username"] == "admin"

    # Test protected endpoint
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "user_info" in data

    # Test token validation
    response = requests.get(f"{BASE_URL}/validate", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "valid" in data
    assert data["valid"] == True
    assert "user" in data