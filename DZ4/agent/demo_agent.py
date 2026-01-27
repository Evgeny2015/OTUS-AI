#!/usr/bin/env python3
"""
Demonstration script for the LangChain Agent

This script demonstrates how to use the LangChain agent programmatically
to perform various operations on the HTTP server API.

Usage:
    python demo_agent.py
"""

import os
import sys
import time
from langchain_agent import create_agent


def demo_agent():
    """Demonstrate the LangChain agent functionality"""

    print("🚀 LangChain Agent Demonstration")
    print("=" * 50)

    # Check if Ollama is running
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
        else:
            print("⚠️  Warning: Ollama may not be properly configured")
    except requests.exceptions.ConnectionError:
        print("⚠️  Warning: Ollama is not running or not accessible")
        print("Please start Ollama and ensure the llama3.2:3b model is available")
        print("You can start Ollama with: ollama serve")
        print("\nContinuing with demo (may fail without Ollama)...")
        time.sleep(2)

    # Create the agent
    print("\n🤖 Creating LangChain agent...")
    try:
        agent = create_agent()
        print("✅ Agent created successfully!")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        print("Make sure Ollama is running and the llama3.2:3b model is available")
        return False

    # Demo operations
    demo_operations = [
        {
            "description": "Get all users (should be empty initially)",
            "command": "Get all users"
        },
        {
            "description": "Create a new user",
            "command": "Create a user named DemoUser with email demo@example.com"
        },
        {
            "description": "Get all users (should show 1 user)",
            "command": "Get all users"
        },
        {
            "description": "Get the specific user we just created",
            "command": "Get user 1"
        },
        {
            "description": "Update the user's email",
            "command": "Update user 1's email to demo.updated@example.com"
        },
        {
            "description": "Delete the user",
            "command": "Delete user 1"
        },
        {
            "description": "Verify user was deleted",
            "command": "Get all users"
        }
    ]

    print(f"\n📋 Running {len(demo_operations)} demo operations...")
    print("-" * 50)

    success_count = 0

    for i, operation in enumerate(demo_operations, 1):
        print(f"\n{i}. {operation['description']}")
        print(f"   Command: {operation['command']}")
        print("   → Executing...")

        try:
            result = agent.invoke({"input": operation["command"]})
            print(f"   ✅ Result: {result['output']}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    print("\n" + "=" * 50)
    print(f"🎉 Demo completed! {success_count}/{len(demo_operations)} operations successful")

    if success_count == len(demo_operations):
        print("✅ All operations completed successfully!")
    else:
        print("⚠️  Some operations failed. This might be due to:")
        print("   - Flask server not running on http://localhost:5000")
        print("   - Ollama not running or model not available")
        print("   - Network connectivity issues")

    return success_count == len(demo_operations)


def show_usage_examples():
    """Show usage examples for the agent"""

    print("\n📖 Usage Examples")
    print("=" * 50)

    examples = [
        {
            "command": "Get all users",
            "description": "Retrieve all users from the API"
        },
        {
            "command": "Create a user named John with email john@example.com",
            "description": "Create a new user with the specified details"
        },
        {
            "command": "Get user 5",
            "description": "Get specific user by ID"
        },
        {
            "command": "Update user 3's username to Johnny",
            "description": "Update an existing user's username"
        },
        {
            "command": "Update user 2's email to newemail@example.com",
            "description": "Update an existing user's email"
        },
        {
            "command": "Delete user 1",
            "description": "Delete a user by ID"
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['command']}")
        print(f"   → {example['description']}")
        print()


def main():
    """Main demonstration function"""

    if len(sys.argv) > 1 and sys.argv[1] == "examples":
        show_usage_examples()
    else:
        success = demo_agent()

        print("\n" + "=" * 50)
        print("📚 Next Steps:")
        print("1. Start the Flask server: python ../backend/app.py")
        print("2. Run interactive mode: python langchain_agent.py")
        print("3. Run tests: python langchain_agent.py test")
        print("4. Run integration test: python test_langchain_agent.py")
        print("5. See usage examples: python demo_agent.py examples")

        if not success:
            print("\n⚠️  If you encountered errors:")
            print("   - Make sure Flask server is running on http://localhost:5000")
            print("   - Ensure Ollama is running and model is available")
            print("   - Check your internet connection")


if __name__ == "__main__":
    main()
