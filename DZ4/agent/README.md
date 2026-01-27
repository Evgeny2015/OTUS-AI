# LangChain Agent for HTTP Server API

This directory contains a LangChain agent that can interact with the Flask HTTP server API to perform CRUD operations on users through natural language commands.

## Overview

The LangChain agent provides a conversational interface to manage users in the HTTP server API. It uses Ollama's local language models to understand natural language requests and execute the appropriate API calls.

## Features

- **Natural Language Interface**: Use plain English to perform API operations
- **Complete CRUD Support**: Create, Read, Update, and Delete users
- **Error Handling**: Comprehensive error handling and user feedback
- **Interactive Mode**: Real-time conversation with the agent
- **Automated Testing**: Built-in test suite for validation

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Ollama:
   - Install Ollama from https://ollama.com/download
   - Pull the required model:
     ```bash
     ollama pull llama3.2:3b
     ```

## Usage

### 1. Start the Flask Server

First, start the HTTP server in one terminal:
```bash
cd ../backend
python app.py
```

The server will start on `http://localhost:5000`

### 2. Run the LangChain Agent

In another terminal, run the agent:

#### Interactive Mode (Default)
```bash
cd ../agent
python langchain_agent.py
```

This will start an interactive session where you can type natural language commands like:
- "Get all users"
- "Create a user named Alice with email alice@example.com"
- "Update user 1's email to alice.updated@example.com"
- "Delete user 2"

#### Automated Testing
```bash
python langchain_agent.py test
```

This runs a predefined test suite to verify all functionality.

#### Demo Mode
```bash
python demo_agent.py
```

This demonstrates the agent functionality with predefined operations.

#### Usage Examples
```bash
python demo_agent.py examples
```

Shows usage examples for all available commands.

## Available Commands

The agent understands these natural language commands:

### User Management
- **Get all users**: `Get all users` or `List all users`
- **Get specific user**: `Get user 1` or `Show user with ID 1`
- **Create user**: `Create a user named John with email john@example.com`
- **Update user**: `Update user 1's email to new@example.com` or `Change user 1's username to Johnny`
- **Delete user**: `Delete user 5` or `Remove user with ID 5`

### System Commands
- **Exit**: `exit` or `quit`
- **Run tests**: `test`

## Example Session

```
🤖 LangChain Agent for HTTP Server API
Type 'exit' to quit, 'test' to run automated tests
============================================================

You: Get all users
Agent: ✅ Success: Retrieved 0 users

You: Create a user named Alice with email alice@example.com
Agent: ✅ Success: Successfully created user: Alice

You: Get all users
Agent: ✅ Success: Retrieved 1 users

You: Update user 1's email to alice.updated@example.com
Agent: ✅ Success: Successfully updated user 1

You: Delete user 1
Agent: ✅ Success: Successfully deleted user 1

You: exit
👋 Goodbye!
```

## Architecture

### Components

1. **Tools**: Individual functions that perform specific API operations
   - `GetAllUsersTool`: GET /api/users
   - `GetUserTool`: GET /api/users/{id}
   - `CreateUserTool`: POST /api/users
   - `UpdateUserTool`: PUT /api/users/{id}
   - `DeleteUserTool`: DELETE /api/users/{id}

2. **Agent**: LangChain agent that uses the tools based on user input
3. **LLM**: Ollama Llama3.2:3b for natural language understanding
4. **Executor**: Manages tool execution and response handling

### Flow

1. User provides natural language input
2. LLM processes the input and determines which tool to use
3. Agent executes the appropriate tool
4. Tool makes HTTP request to Flask API
5. Agent processes the response and generates a natural language reply

## Error Handling

The agent provides clear error messages for common issues:

- **Server not running**: "Failed to retrieve users - Connection refused"
- **Invalid user ID**: "Failed to retrieve user 999 - 404 Not Found"
- **Duplicate user**: "Failed to create user: john - 409 Conflict"
- **Invalid input**: "Please provide both username and email"

## Configuration

### Agent Settings

You can modify these settings in `langchain_agent.py`:

```python
llm = ChatOllama(
    model="llama3.2:3b",  # Change to any available model
    temperature=0.1,         # Adjust creativity (0.0-1.0)
    max_tokens=1000          # Limit response length
)
```

### Available Models

You can use any model available in Ollama. Popular choices include:
- `llama3.2:3b` - Fast, lightweight model
- `llama3.2:1b` - Even faster, smaller model
- `mistral` - Good balance of speed and quality
- `codellama` - Optimized for code generation

To change the model, update the `model` parameter in the `ChatOllama` initialization.

## Testing

### Unit Tests

The agent includes comprehensive tests in `test_langchain_agent.py`:

1. **Server Startup**: Verifies Flask server starts correctly
2. **Agent Functionality**: Tests all CRUD operations
3. **Error Scenarios**: Tests error handling
4. **Cleanup**: Ensures proper resource cleanup

### Manual Testing

Run individual test cases:
```bash
python langchain_agent.py test
```

## Troubleshooting

### Common Issues

1. **"Connection refused" errors**
   - Ensure Flask server is running on `http://localhost:5000`
   - Check that port 5000 is not in use

2. **"Module not found" errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Ensure Python version is compatible (3.8+)

3. **"Ollama not accessible" errors**
   - Ensure Ollama is running: `ollama serve`
   - Verify the model is available: `ollama list`
   - Check that the llama3.2:3b model is pulled: `ollama pull llama3.2:3b`

4. **Slow responses**
   - Response time depends on local model processing
   - Consider reducing `max_tokens` for faster responses
   - Try a smaller model like `llama3.2:1b` for faster performance

### Debug Mode

Enable verbose logging by setting:
```python
agent = create_tool_calling_agent(llm, tools, prompt, verbose=True)
```

## Security Considerations

- **Local Processing**: No external API keys required (runs locally with Ollama)
- **Input Validation**: The agent validates all inputs before making API calls
- **Error Information**: Error messages don't expose sensitive system information

## Performance

- **Response Time**: ~1-10 seconds per operation (depends on local model processing)
- **Memory Usage**: ~50-500MB additional memory (depends on model size)
- **Network**: No internet connection required (local processing)

## Extending the Agent

### Adding New Tools

1. Create a new tool class inheriting from `BaseTool`
2. Implement the `_run` method
3. Add the tool to the `tools` list in `create_agent()`
4. Update the system prompt to describe the new functionality

### Example: Adding a Search Tool

```python
class SearchUsersTool(BaseTool):
    name = "search_users"
    description = "Search for users by username or email"

    def _run(self, query: str):
        # Implementation here
        pass
```

## Dependencies

- **langchain**: Core LangChain framework
- **langchain-ollama**: Ollama integration
- **langchain-classic**: Classic LangChain agents
- **requests**: HTTP client for API calls
- **pydantic**: Data validation

## License

This project is open source and available under the MIT License.
