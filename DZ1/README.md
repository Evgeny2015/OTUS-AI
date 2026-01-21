# Python FastAPI Server

A simple Python server built with FastAPI following clean architecture principles.

## Project Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── models/
│       ├── __init__.py
├── tests/
├── requirements.txt
├── venv/
├── .vscode/
│   └── launch.json
└── README.md
```

## Features
- FastAPI web framework
- Uvicorn ASGI server
- Automatic Swagger documentation
- Clean architecture
- Virtual environment support
- Debug configuration for VS Code

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

5. Access the API documentation at `http://localhost:8000/docs`

## Endpoints

- `GET /` - Root endpoint

## Debugging

The project includes a debug configuration for VS Code in `.vscode/launch.json`. You can start debugging by pressing F5 or going to Run and Debug section in VS Code.