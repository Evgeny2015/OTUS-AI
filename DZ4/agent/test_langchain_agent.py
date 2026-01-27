#!/usr/bin/env python3
"""
Test script for the LangChain Agent

This script tests the LangChain agent functionality by:
1. Starting the Flask server in the background
2. Running the agent tests
3. Cleaning up the server process

Usage:
    python test_langchain_agent.py
"""

import subprocess
import time
import sys
import os
import signal
from threading import Thread


def start_flask_server():
    """Start the Flask server in a subprocess"""
    print("🚀 Starting Flask server...")
    try:
        # Start the Flask server
        server_process = subprocess.Popen(
            [sys.executable, "../backend/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Give the server time to start
        time.sleep(3)

        # Check if server started successfully
        if server_process.poll() is None:
            print("✅ Flask server started successfully")
            return server_process
        else:
            stdout, stderr = server_process.communicate()
            print(f"❌ Flask server failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None

    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")
        return None


def run_agent_tests():
    """Run the LangChain agent tests"""
    print("\n🧪 Testing LangChain Agent...")
    try:
        # Run the agent test
        result = subprocess.run(
            [sys.executable, "langchain_agent.py", "test"],
            capture_output=True,
            text=True,
            timeout=60
        )

        print("📋 Agent Test Output:")
        print("-" * 40)
        print(result.stdout)

        if result.stderr:
            print("⚠️  Agent Test Errors:")
            print(result.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("❌ Agent tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running agent tests: {e}")
        return False


def cleanup_server(server_process):
    """Clean up the Flask server process"""
    if server_process and server_process.poll() is None:
        print("\n🧹 Cleaning up Flask server...")
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
            print("✅ Flask server stopped successfully")
        except subprocess.TimeoutExpired:
            print("⚠️  Force killing Flask server...")
            server_process.kill()
            server_process.wait()
            print("✅ Flask server force killed")
        except Exception as e:
            print(f"❌ Error cleaning up server: {e}")


def main():
    """Main test function"""
    print("🧪 LangChain Agent Integration Test")
    print("=" * 50)

    server_process = None

    try:
        # Start Flask server
        server_process = start_flask_server()
        if not server_process:
            print("❌ Cannot proceed without Flask server")
            return False

        # Run agent tests
        test_success = run_agent_tests()

        # Report results
        print("\n" + "=" * 50)
        if test_success:
            print("🎉 All tests passed!")
        else:
            print("❌ Some tests failed")

        return test_success

    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    finally:
        # Always clean up the server
        cleanup_server(server_process)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
