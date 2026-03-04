#!/usr/bin/env python3
"""
Setup script for JWT Test Runner MCP Server
This script helps install and configure the JWT Test Runner MCP server for SourceCraft.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install the required dependencies for the MCP server."""
    print("Installing JWT Test Runner MCP server dependencies...")
    try:
        subprocess.check_call(["uv", "pip", "install", "-e", "../mcp"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def create_config_file():
    """Create the MCP server configuration file."""
    config = {
        "mcpServers": {
            "jwt-test-runner": {
                "command": "python",
                "args": ["-m", "jwt_test_runner"],
                "env": {
                    "PYTHONPATH": "."
                },
                "disabled": False,
                "alwaysAllow": [],
                "disabledTools": []
            }
        }
    }

    config_file = "mcp_server_config.json"
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Configuration file created: {config_file}")
        return True
    except Exception as e:
        print(f"Error creating configuration file: {e}")
        return False


def verify_setup():
    """Verify that the setup is correct."""
    print("Verifying setup...")

    # Check if the mcp module exists
    if not os.path.exists("../mcp/jwt_test_runner.py"):
        print("Error: JWT Test Runner module not found!")
        return False

    # Check if the jwt project exists
    if not os.path.exists("../jwt/main.py"):
        print("Warning: JWT project not found!")

    print("Setup verification completed.")
    return True


def main():
    """Main setup function."""
    print("JWT Test Runner MCP Server Setup")
    print("=" * 40)

    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Please check your Python environment.")
        return 1

    # Create configuration file
    if not create_config_file():
        print("Failed to create configuration file.")
        return 1

    # Verify setup
    if not verify_setup():
        print("Setup verification failed.")
        return 1

    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Add the configuration from mcp_server_config.json to your SourceCraft MCP settings")
    print("2. Restart SourceCraft to load the new server")
    print("3. You can now use the JWT Test Runner tools in SourceCraft")

    return 0


if __name__ == "__main__":
    sys.exit(main())