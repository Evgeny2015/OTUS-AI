#!/usr/bin/env python3
"""
Test script for ToolResponse __str__ and __repr__ methods
"""

from langchain_agent import ToolResponse


def test_tool_response_str_repr():
    """Test the __str__ and __repr__ methods of ToolResponse"""
    print("🧪 Testing ToolResponse __str__ and __repr__ methods")
    print("=" * 60)

    # Test successful response
    success_response = ToolResponse(
        status="success",
        action="get_all_users",
        data={"users": [{"id": 1, "username": "alice"}], "count": 1}
    )

    print("✅ Success Response:")
    print(f"str(): {str(success_response)}")
    print(f"repr(): {repr(success_response)}")
    print()

    # Test error response
    error_response = ToolResponse(
        status="error",
        action="create_user",
        errors={"message": "Failed to create user", "details": "Username already exists"}
    )

    print("❌ Error Response:")
    print(f"str(): {str(error_response)}")
    print(f"repr(): {repr(error_response)}")
    print()

    # Test minimal response
    minimal_response = ToolResponse(
        status="success",
        action="get_user"
    )

    print("📝 Minimal Response:")
    print(f"str(): {str(minimal_response)}")
    print(f"repr(): {repr(minimal_response)}")
    print()

    print("🎉 All tests completed successfully!")


if __name__ == "__main__":
    test_tool_response_str_repr()
