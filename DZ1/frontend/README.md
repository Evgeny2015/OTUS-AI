# Survey Frontend Application

A React frontend application that interacts with the FastAPI backend to display survey questions and collect answers.

## Features

- Fetches survey questions from the backend API
- Displays questions in a user-friendly interface
- Supports different question types (text, single choice, multiple choice)
- Submits answers to the backend via POST request
- Shows a thank you message after successful submission

## Prerequisites

- Node.js (version 14 or higher)
- npm (usually comes with Node.js)

## Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

1. Make sure the backend server is running on `http://localhost:8000`
2. Start the React development server:
   ```
   npm start
   ```
3. Open your browser and navigate to `http://localhost:3000`

## API Endpoints

The frontend communicates with the following backend endpoints:

- `GET /api/v1/questions` - Fetch survey questions
- `POST /api/v1/answers` - Submit survey answers

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json
└── README.md
```

## Dependencies

- React
- Axios (for HTTP requests)