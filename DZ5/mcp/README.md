# JWT Test Runner MCP Server

A Model Context Protocol server for automated testing and reporting of the JWT authentication service.

## Features

This MCP server provides comprehensive testing capabilities for Python projects, specifically designed for the JWT authentication service:

- **Test Execution**: Run pytest with customizable parameters
- **Coverage Analysis**: Generate detailed test coverage reports
- **Failure Analysis**: Analyze failed tests and provide suggestions
- **Test Discovery**: List available test files and functions
- **Metrics Tracking**: Get test execution statistics and trends

## Tools Provided

### `run_tests`
Execute pytest with flexible parameters:
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

```bash
pip install -e .
```

## Usage

The server can be run directly:

```bash
jwt-test-runner
```

Or integrated with MCP-compatible clients and IDEs.

## Dependencies

- pytest >= 8.0.0
- coverage >= 7.0.0
- requests >= 2.32.5
- mcp[cli] >= 1.21.0

## Configuration

The server expects the JWT project to be located at `../jwt` relative to the server directory.