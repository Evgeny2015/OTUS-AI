# Python FastAPI Server with React Frontend

A simple Python server built with FastAPI following clean architecture principles, with a React frontend for survey interaction.

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
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
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
- React frontend for survey interaction
- Survey question display and answer submission
- Thank you message after submission

## Setup

### Backend Setup

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

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

4. Open your browser and navigate to `http://localhost:3000`

## Endpoints

### Backend API Endpoints
- `GET /` - Root endpoint
- `GET /api/v1/questions` - Get survey questions
- `POST /api/v1/answers` - Submit survey answers

### Frontend
- `http://localhost:3000` - Survey application

## Debugging

The project includes a debug configuration for VS Code in `.vscode/launch.json`. You can start debugging by pressing F5 or going to Run and Debug section in VS Code.