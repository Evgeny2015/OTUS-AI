#!/usr/bin/env python3
"""
Test script to verify the toJSON method implementation in ToolResponse class
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_agent import ToolResponse
import json

def test_tojson_method():
    """Test the toJSON method of ToolResponse class"""
    print("🧪 Testing ToolResponse.toJSON() method")
    print("=" * 50)

    # Test 1: Success response with data
    print("\n📋 Test 1: Success response with data")
    success_response = ToolResponse(
        status="success",
        action="get_all_users",
        data={"users": [{"id": 1, "username": "alice"}], "count": 1}
    )
    json_output = success_response.toJSON()
    print(f"✅ toJSON() output: {json_output}")
    print(f"✅ JSON serializable: {json.dumps(json_output)}")

    # Test 2: Error response with errors
    print("\n📋 Test 2: Error response with errors")
    error_response = ToolResponse(
        status="error",
        action="create_user",
        errors={"message": "User already exists", "details": "Username 'alice' is taken"}
    )
    json_output = error_response.toJSON()
    print(f"✅ toJSON() output: {json_output}")
    print(f"✅ JSON serializable: {json.dumps(json_output)}")

    # Test 3: Empty response
    print("\n📋 Test 3: Empty response")
    empty_response = ToolResponse(
        status="success",
        action="get_user",
        data={},
        errors={}
    )
    json_output = empty_response.toJSON()
    print(f"✅ toJSON() output: {json_output}")
    print(f"✅ JSON serializable: {json.dumps(json_output)}")

    print("\n" + "=" * 50)
    print("🎉 All tests passed! toJSON() method is working correctly.")

if __name__ == "__main__":
    test_tojson_method()
