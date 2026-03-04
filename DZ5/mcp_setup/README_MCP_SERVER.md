# JWT Test Runner MCP Server for SourceCraft

This repository contains a Model Context Protocol (MCP) server for automated testing and reporting of the JWT authentication service. The server provides comprehensive testing capabilities that can be integrated with SourceCraft.

## Features

- **Test Execution**: Run pytest with customizable parameters
- **Coverage Analysis**: Generate detailed test coverage reports
- **Failure Analysis**: Analyze failed tests and provide suggestions
- **Test Discovery**: List available test files and functions
- **Metrics Tracking**: Get test execution statistics and trends

## Files in this Repository

- `mcp_server_config.json`: Configuration file for the MCP server
- `MCP_SERVER_CONFIGURATION.md`: Detailed documentation on configuring and using the server
- `setup_mcp_server.py`: Setup script to install dependencies and create configuration
- `mcp/`: Directory containing the JWT Test Runner MCP server implementation
- `jwt/`: Directory containing the JWT authentication service to be tested

## Quick Start

1. **Install Dependencies**:
   ```bash
   python setup_mcp_server.py
   ```

2. **Configure SourceCraft**:
   - Copy the configuration from `mcp_server_config.json` to your SourceCraft MCP settings
   - The configuration should be added to the `mcpServers` section of your settings

3. **Restart SourceCraft** to load the new server

## Manual Configuration

If you prefer to configure manually:

1. Install the server dependencies:
   ```bash
   pip install -e ./mcp
   ```

2. Add the following configuration to your SourceCraft MCP settings:
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

## Available Tools

Once configured, the following tools will be available in SourceCraft:

### `run_tests`
Execute pytest with flexible parameters:
- Run specific tests or test directories
- Filter tests by markers
- Parallel execution support
- Generate HTML, XML, and JSON reports

### `get_test_coverage`
Generate coverage reports with line-by-line analysis.

### `analyze_test_failures`
Analyze failed tests and provide suggestions for fixes.

### `list_test_files`
Discover and list available test files and functions.

### `get_test_metrics`
Get test execution statistics and trends.

## Usage Examples

After configuration, you can use natural language commands in SourceCraft:

- "Run tests on the JWT project"
- "Generate a coverage report for the JWT service"
- "Analyze test failures in the JWT project"
- "List all test files in the JWT project"
- "Get test metrics for the JWT service"

## Project Structure

The MCP server expects the JWT project to be located at `../jwt` relative to the server directory. This structure is already set up in this repository.

## Troubleshooting

If you encounter issues:

1. **Server not appearing in SourceCraft**:
   - Verify that the configuration was added correctly to your MCP settings
   - Check that SourceCraft was restarted after configuration
   - Ensure all dependencies are installed

2. **Tools not working**:
   - Verify that the JWT project is in the expected location
   - Check that the JWT service can run correctly
   - Review the server logs for error messages

3. **Dependency issues**:
   - Ensure you're using Python 3.10 or later
   - Verify that all required packages are installed
   - Check for conflicting package versions

## Security Notes

- The MCP server runs in a non-interactive environment
- All credentials and authentication tokens must be provided through environment variables
- The server cannot initiate OAuth flows or prompt for user input during runtime

## Contributing

To extend the MCP server with additional tools or functionality:

1. Modify `mcp/jwt_test_runner.py` to add new tools
2. Follow the existing pattern of using the `@mcp.tool()` decorator
3. Update the documentation to reflect new capabilities
4. Test the changes thoroughly

## License

This project is provided as part of the SourceCraft examples and follows the same licensing as the SourceCraft project.