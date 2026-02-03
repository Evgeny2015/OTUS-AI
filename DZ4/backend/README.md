# Python HTTP Server with User Models

A simple Python HTTP server built with Flask that provides a REST API for user management.

## Features

- **User Management**: Create, read, update, and delete users
- **Database Integration**: Uses SQLAlchemy with SQLite for data persistence
- **RESTful API**: Follows REST conventions for all endpoints
- **Input Validation**: Validates required fields and prevents duplicate usernames/emails
- **Error Handling**: Proper HTTP status codes and error messages

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### Root Endpoint
- `GET /` - Returns API documentation and available endpoints

#### User Endpoints

- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get a specific user by ID
- `POST /api/users` - Create a new user
- `PUT /api/users/<id>` - Update a user
- `DELETE /api/users/<id>` - Delete a user

### User Model

Each user has the following fields:
- `id` (integer, auto-generated) - Unique identifier
- `username` (string, unique) - User's username
- `email` (string, unique) - User's email address
- `created_at` (datetime) - When the user was created
- `updated_at` (datetime) - When the user was last updated

### Example Usage

#### Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com"}'
```

#### Get All Users
```bash
curl http://localhost:5000/api/users
```

#### Get Specific User
```bash
curl http://localhost:5000/api/users/1
```

#### Update User
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

#### Delete User
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

## Testing

Run the test script to verify all functionality:

```bash
python test_server.py
```

This will start the server, run all tests, and clean up automatically.

## Dependencies

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.5
- python-dotenv 1.0.0

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── test_server.py      # Test script
└── README.md          # This file
```

## License

This project is open source and available under the MIT License.
