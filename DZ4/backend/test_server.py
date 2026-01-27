#!/usr/bin/env python3
"""
Simple test script to verify the Python HTTP server functionality.
This script tests all the user endpoints without requiring external dependencies.
"""

import requests
import json
import time
import subprocess
import sys
import os

# Server configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_server():
    """Test the server endpoints"""
    print("Testing Python HTTP Server with User Models")
    print("=" * 50)

    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✓ Root endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ Root endpoint failed with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Server not running. Please start the server first.")
        return False

    # Test 2: Create a user
    print("\n2. Testing user creation...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    try:
        response = requests.post(f"{API_BASE}/users", json=user_data)
        if response.status_code == 201:
            created_user = response.json()
            print("✓ User created successfully")
            print(f"Created user: {created_user}")
            user_id = created_user['id']
        else:
            print(f"✗ User creation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        return False

    # Test 3: Get all users
    print("\n3. Testing get all users...")
    try:
        response = requests.get(f"{API_BASE}/users")
        if response.status_code == 200:
            users = response.json()
            print(f"✓ Got {len(users)} users")
            print(f"Users: {users}")
        else:
            print(f"✗ Get users failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error getting users: {e}")

    # Test 4: Get specific user
    print("\n4. Testing get specific user...")
    try:
        response = requests.get(f"{API_BASE}/users/{user_id}")
        if response.status_code == 200:
            user = response.json()
            print("✓ User retrieved successfully")
            print(f"User: {user}")
        else:
            print(f"✗ Get user failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error getting user: {e}")

    # Test 5: Update user
    print("\n5. Testing user update...")
    update_data = {
        "email": "updated@example.com"
    }

    try:
        response = requests.put(f"{API_BASE}/users/{user_id}", json=update_data)
        if response.status_code == 200:
            updated_user = response.json()
            print("✓ User updated successfully")
            print(f"Updated user: {updated_user}")
        else:
            print(f"✗ User update failed with status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"✗ Error updating user: {e}")

    # Test 6: Delete user
    print("\n6. Testing user deletion...")
    try:
        response = requests.delete(f"{API_BASE}/users/{user_id}")
        if response.status_code == 200:
            print("✓ User deleted successfully")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ User deletion failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error deleting user: {e}")

    # Test 7: Try to get deleted user (should return 404)
    print("\n7. Testing get deleted user (should return 404)...")
    try:
        response = requests.get(f"{API_BASE}/users/{user_id}")
        if response.status_code == 404:
            print("✓ Correctly returned 404 for deleted user")
        else:
            print(f"✗ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing deleted user: {e}")

    print("\n" + "=" * 50)
    print("Test completed!")
    return True

def start_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    try:
        # Start the server in a subprocess
        server_process = subprocess.Popen([sys.executable, "app.py"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        time.sleep(2)  # Give the server time to start
        return server_process
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def main():
    """Main function"""
    # Check if server is already running
    try:
        response = requests.get(BASE_URL, timeout=2)
        if response.status_code == 200:
            print("Server is already running!")
            test_server()
            return
    except:
        pass

    # Start server
    server_process = start_server()
    if server_process is None:
        return

    try:
        # Run tests
        test_server()
    finally:
        # Clean up
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    main()
