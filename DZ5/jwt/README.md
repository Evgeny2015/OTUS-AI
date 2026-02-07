# JWT Authentication Service

A FastAPI-based HTTP service that provides JWT (JSON Web Token) authentication functionality.

## Features

- Generate JWT tokens with username/password authentication
- Validate JWT tokens
- Protected endpoints requiring authentication
- User information retrieval

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The service uses the following environment variables:
- `SECRET_KEY`: Secret key for JWT signing (default: "your-secret-key-change-in-production")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: 30)

## Running the Service

```bash
python main.py
```

The service will start on `http://localhost:8000`

## API Endpoints

### 1. Generate JWT Token
**POST** `/token`

Authenticate with username and password to receive a JWT token.

**Request Body:**
```json
{
    "username": "admin",
    "password": "secret123"
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
}
```

### 2. Get Current User
**GET** `/users/me`

Retrieve current user information from JWT token.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "username": "admin",
    "disabled": false
}
```

### 3. Protected Endpoint
**GET** `/protected`

A sample protected endpoint that requires authentication.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "message": "Hello, admin! This is a protected endpoint.",
    "user_info": {
        "username": "admin",
        "timestamp": "2023-12-07T10:30:00.000Z"
    }
}
```

### 4. Validate Token
**GET** `/validate`

Validate a JWT token and return user information.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "valid": true,
    "user": {
        "username": "admin",
        "authenticated_at": "2023-12-07T10:30:00.000Z"
    }
}
```

### 5. Health Check
**GET** `/`

Service health check endpoint.

**Response:**
```json
{
    "service": "JWT Authentication Service",
    "status": "running",
    "version": "1.0.0",
    "endpoints": {
        "token": "POST /token - Generate JWT token",
        "me": "GET /users/me - Get current user",
        "protected": "GET /protected - Protected endpoint",
        "validate": "GET /validate - Validate token"
    }
}
```

## Test Users

The service includes two test users:

1. **Admin User:**
   - Username: `admin`
   - Password: `secret123`

2. **Regular User:**
   - Username: `user`
   - Password: `password123`

## Usage Examples

### Using curl

1. Generate a token:
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"secret123"}'
```

2. Use the token to access protected endpoints:
```bash
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using Python requests

```python
import requests

# Generate token
response = requests.post("http://localhost:8000/token", json={
    "username": "admin",
    "password": "secret123"
})
token = response.json()["access_token"]

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/users/me", headers=headers)
print(response.json())
```

## Security Notes

⚠️ **Important**: This is a demonstration service with the following security considerations:

1. Passwords are stored in plain text (in production, use proper hashing like bcrypt)
2. The default SECRET_KEY should be changed for production use
3. Consider using HTTPS in production environments
4. Implement proper user registration and password reset functionality

## Development

The project uses:
- FastAPI for the web framework
- python-jose for JWT handling
- Pydantic for data validation

To run with auto-reload during development:
```bash
uvicorn main:app --reload --host localhost --port 8000
```

## OpenAPI Documentation

The service automatically generates OpenAPI documentation available at:
- `http://localhost:8000/docs` - Interactive API documentation (Swagger UI)
- `http://localhost:8000/redoc` - Alternative documentation (ReDoc)
