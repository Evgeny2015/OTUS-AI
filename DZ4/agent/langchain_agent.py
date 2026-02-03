#!/usr/bin/env python3
"""
LangChain Agent for HTTP Server API

This module creates a LangChain agent that can interact with the Flask HTTP server API
to perform CRUD operations on users. The agent uses tools to make HTTP requests and
process responses.

Usage:
    python langchain_agent.py

The agent can:
- Get all users
- Get a specific user by ID
- Create new users
- Update existing users
- Delete users
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_ollama import ChatOllama
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


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


class UserCreateRequest(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., description="The username for the new user")
    email: str = Field(..., description="The email address for the new user")


class UserUpdateRequest(BaseModel):
    """Schema for updating an existing user"""
    user_id: int = Field(..., description="The ID of the user to update")
    username: Optional[str] = Field(None, description="New username (optional)")
    email: Optional[str] = Field(None, description="New email (optional)")


class GetUserRequest(BaseModel):
    """Schema for getting a specific user"""
    user_id: int = Field(..., description="The ID of the user to retrieve")


class DeleteUserRequest(BaseModel):
    """Schema for deleting a user"""
    user_id: int = Field(..., description="The ID of the user to delete")


class GetAllUsersTool(BaseTool):
    """Tool to get all users from the API"""

    name: str = Field(default="get_all_users", description="Tool name for retrieving all users")
    description: str = Field(default="Retrieve all users from the HTTP server API", description="Tool description")

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> ToolResponse:
        """Execute the tool to get all users"""
        try:
            response = requests.get("http://localhost:5000/api/users")
            response.raise_for_status()
            response = ToolResponse(
                status="success",
                action="get_all_users",
                data={
                    "users": response.json(),
                    "count": len(response.json()),
                    "message": f"Retrieved {len(response.json())} users"
                }
            )
            return response

        except requests.exceptions.RequestException as e:
            return ToolResponse(
                status="error",
                action="get_all_users",
                errors={
                    "message": "Failed to retrieve users",
                    "details": str(e)
                }
            )


class GetUserTool(BaseTool):
    """Tool to get a specific user by ID"""

    name: str = Field(default="get_user", description="Tool name for retrieving a specific user")
    description: str = Field(default="Retrieve a specific user by their ID from the HTTP server API", description="Tool description")

    user_id: int = Field(default=1, description="The ID of the user to retrieve")

    def _run(
        self,
        user_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> ToolResponse:
        """Execute the tool to get a specific user"""
        try:
            response = requests.get(f"http://localhost:5000/api/users/{user_id}")
            response.raise_for_status()
            return ToolResponse(
                status="success",
                action="get_user",
                data={
                    "user": response.json(),
                    "message": f"Retrieved user {user_id}"
                }
            )
        except requests.exceptions.RequestException as e:
            return ToolResponse(
                status="error",
                action="get_user",
                errors={
                    "message": f"Failed to retrieve user {user_id}",
                    "details": str(e)
                }
            )


class CreateUserTool(BaseTool):
    """Tool to create a new user"""

    name: str = Field(default="create_user", description="Tool name for creating a new user")
    description: str = Field(default="Create a new user in the HTTP server API", description="Tool description")

    username: str = Field(default=None, description="The username for the new user")
    email: str = Field(default=None, description="The email address for the new user")

    def _run(
        self,
        username: str,
        email: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> ToolResponse:
        """Execute the tool to create a new user"""
        try:
            user_data = {
                "username": username,
                "email": email
            }
            response = requests.post(
                "http://localhost:5000/api/users",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return ToolResponse(
                status="success",
                action="create_user",
                data={
                    "user": response.json(),
                    "message": f"Successfully created user: {username}"
                }
            )
        except requests.exceptions.RequestException as e:
            return ToolResponse(
                status="error",
                action="create_user",
                errors={
                    "message": f"Failed to create user: {username}",
                    "details": str(e)
                }
            )


class UpdateUserTool(BaseTool):
    """Tool to update an existing user"""

    name: str = Field(default="update_user", description="Tool name for updating an existing user")
    description: str = Field(default="Update an existing user in the HTTP server API", description="Tool description")

    user_id: int = Field(None, description="The ID of the user to update")
    username: Optional[str] = Field(None, description="New username (optional)")
    email: Optional[str] = Field(None, description="New email (optional)")

    def _run(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> ToolResponse:
        """Execute the tool to update a user"""
        try:
            update_data = {}
            if username:
                update_data["username"] = username
            if email:
                update_data["email"] = email

            response = requests.put(
                f"http://localhost:5000/api/users/{user_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return ToolResponse(
                status="success",
                action="update_user",
                data={
                    "user": response.json(),
                    "message": f"Successfully updated user {user_id}"
                }
            )
        except requests.exceptions.RequestException as e:
            return ToolResponse(
                status="error",
                action="update_user",
                errors={
                    "message": f"Failed to update user {user_id}",
                    "details": str(e)
                }
            )


class DeleteUserTool(BaseTool):
    """Tool to delete a user"""

    name: str = Field(default="delete_user", description="Tool name for deleting a user")
    description: str = Field(default="Delete a user from the HTTP server API", description="Tool description")

    user_id: int = Field(None, description="The ID of the user to delete")

    def _run(
        self,
        user_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> ToolResponse:
        """Execute the tool to delete a user"""
        try:
            response = requests.delete(f"http://localhost:5000/api/users/{user_id}")
            response.raise_for_status()
            return ToolResponse(
                status="success",
                action="delete_user",
                data={
                    "user_id": user_id,
                    "message": f"Successfully deleted user {user_id}"
                }
            )
        except requests.exceptions.RequestException as e:
            return ToolResponse(
                status="error",
                action="delete_user",
                errors={
                    "message": f"Failed to delete user {user_id}",
                    "details": str(e)
                }
            )


def create_agent():
    """Create and configure the LangChain agent"""

    # Initialize the LLM (using Ollama)
    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.1,
        max_tokens=1000,
    )

    # Define the tools
    tools = [
        GetAllUsersTool(),
        GetUserTool(),
        CreateUserTool(),
        UpdateUserTool(),
        DeleteUserTool(),
    ]

    # Create a system prompt for the agent
    system_prompt = """You are a helpful assistant that manages users through an HTTP API.

    You have access to the following tools:
    - get_all_users: Get all users from the system
    - get_user: Get a specific user by ID
    - create_user: Create a new user with username and email
    - update_user: Update an existing user's username or email
    - delete_user: Delete a user by ID

    When users ask you to perform operations:
    1. Use the appropriate tool to interact with the HTTP API
    2. Parse the HTTP response containing fields:
        - status: "success" or "error"
        - action: string describing the action
        - data: object containing response data
        - errors: object containing error details if exists
    3. Return clear, concise responses about the operation results
    4. If an operation fails, explain what went wrong
    5. Always validate that required parameters are provided

    The API base URL is: http://localhost:5000/api

    Examples:
    - "Get all users" -> use get_all_users tool
    - "Create a user named John with email john@example.com" -> use create_user tool with username="John" and email="john@example.com"
    - "Update user 1's email to new@example.com" -> use update_user tool with user_id=1 and email="new@example.com"
    - "Delete user 5" -> use delete_user tool with user_id=5
    """

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor


def test_agent():
    """Test the agent with various operations"""
    print("🧪 Testing LangChain Agent for HTTP Server API")
    print("=" * 60)

    # Create the agent
    agent = create_agent()

    # Test cases
    test_cases = [
        {
            "name": "Get all users (should be empty initially)",
            "input": "Get all users"
        },
        {
            "name": "Create a new user",
            "input": "Create a user named Alice with email alice@example.com"
        },
        {
            "name": "Create another user",
            "input": "Create a user named Bob with email bob@example.com"
        },
        {
            "name": "Get all users (should show 2 users)",
            "input": "Get all users"
        },
        {
            "name": "Get specific user by ID",
            "input": "Get user 1"
        },
        {
            "name": "Update user's email",
            "input": "Update user 1's email to alice.updated@example.com"
        },
        {
            "name": "Delete a user",
            "input": "Delete user 2"
        },
        {
            "name": "Get all users (should show 1 user after deletion)",
            "input": "Get all users"
        }
    ]

    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 40)

        try:
            result = agent.invoke({"input": test_case["input"]})
            print(f"✅ Success: {result['output']}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    print("\n" + "=" * 60)
    print("🎉 Agent testing completed!")


def interactive_mode():
    """Run the agent in interactive mode"""
    print("🤖 LangChain Agent for HTTP Server API")
    print("Type 'exit' to quit, 'test' to run automated tests")
    print("=" * 60)

    agent = create_agent()

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'test':
                test_agent()
            elif user_input:
                result = agent.invoke({"input": user_input})
                print(f"Agent: {result['output']}")
            else:
                print("Please enter a valid command.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_agent()
    else:
        interactive_mode()
