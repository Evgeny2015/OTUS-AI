# SourceCraft MCP Server Configuration Guide

This guide explains how to configure and use the JWT Test Runner MCP server in SourceCraft.

## Overview

The JWT Test Runner is a Model Context Protocol (MCP) server that provides comprehensive testing capabilities for Python projects, specifically designed for the JWT authentication service. It exposes several tools for running tests, analyzing coverage, and getting test metrics.

## Server Configuration

The MCP server configuration should be added to your SourceCraft MCP settings file. Here's the configuration:

```json
{
  "mcpServers": {
    "jwt-test-runner": {
      "command": "uv",
      "args": ["run", "jwt-test-runner"],
      "env": {
        "PYTHONPATH": "."
      },
      "disabled": false,
      "alwaysAllow": [],
      "disabledTools": []
    }
  }
}
```

### Configuration Options

- `command`: The command to execute the server (in this case, `python`)
- `args`: Arguments to pass to the command to run the server module
- `env`: Environment variables to set when running the server
- `disabled`: Whether the server should be disabled (set to `false` to enable)
- `alwaysAllow`: Array of tool names that don't require user confirmation
- `disabledTools`: Array of tool names that are not included in the system prompt

## Available Tools

The JWT Test Runner provides the following tools:

### `run_tests`
Execute pytest with customizable parameters:
- Run specific tests or test directories
- Filter tests by markers
- Parallel execution support
- Generate HTML, XML, and JSON reports

### `get_test_coverage`
Generate coverage reports:
- Line-by-line coverage analysis
- Configurable include/exclude patterns
- Detailed coverage statistics

### `analyze_test_failures`
Analyze failed tests and suggest fixes:
- Detailed failure information
- Common fix suggestions
- Error pattern recognition

### `list_test_files`
Discover and list available test files:
- List all test modules
- Show test functions
- Count test statistics

### `get_test_metrics`
Get test execution statistics and trends:
- Pass/fail statistics
- Execution time tracking
- Trend analysis

## Installation

To install and use the JWT Test Runner MCP server:

1. Ensure you have Python 3.10 or later installed
2. Install the required dependencies:
   ```bash
   pip install -e ./mcp
   ```
3. Add the server configuration to your SourceCraft MCP settings file
4. Restart SourceCraft to load the new server

## Usage

Once configured, the JWT Test Runner tools will be available in SourceCraft. You can use them to:

- Run tests on your JWT project
- Analyze test coverage
- Debug test failures
- Get test metrics and trends

Example usage:
```
Run tests on the JWT project with coverage analysis
```

## Project Structure

The JWT Test Runner expects the JWT project to be located at `../jwt` relative to the server directory. Make sure this structure is maintained for proper operation.

## Troubleshooting

If the server doesn't start:

1. Verify that all dependencies are installed
2. Check that the JWT project is in the expected location
3. Ensure Python can find the jwt_test_runner module
4. Check the server logs for error messages