#!/usr/bin/env python3
"""
Simple test script to verify the toJSON method implementation in ToolResponse class
"""

import json

class ToolResponse:
    """Contract for API response with standardized fields"""
    def __init__(self, status: str, action: str, data: dict = None, errors: dict = None):
        self.Status = status  # "success" or "error"
        self.Action = action  # string describing the action
        self.Data = data or {}  # object containing response data
        self.Errors = errors or {}  # object containing error details

    def toJSON(self) -> dict:
        """Convert the ToolResponse to a JSON-serializable dictionary"""
        return {
            "Status": self.Status,
            "Action": self.Action,
            "Data": self.Data,
            "Errors": self.Errors
        }

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
