#!/usr/bin/env python3
"""
Simple test script for ToolResponse __str__ and __repr__ methods without external dependencies
"""

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

    def __str__(self) -> str:
        """String representation of the ToolResponse"""
        if self.Status == "success":
            return f"ToolResponse(status='{self.Status}', action='{self.Action}', data={self.Data})"
        else:
            return f"ToolResponse(status='{self.Status}', action='{self.Action}', errors={self.Errors})"

    def __repr__(self) -> str:
        """Detailed representation of the ToolResponse"""
        return f"ToolResponse(status='{self.Status}', action='{self.Action}', data={self.Data}, errors={self.Errors})"


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
