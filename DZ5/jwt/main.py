from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os

app = FastAPI(title="JWT Authentication Service", version="1.0.0")

# Security scheme
security = HTTPBearer()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Mock database
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrator",
        "email": "admin@example.com",
        "hashed_password": "secret123",  # In real app, this should be hashed
        "disabled": False,
    },
    "user": {
        "username": "user",
        "full_name": "Regular User",
        "email": "user@example.com",
        "hashed_password": "password123",  # In real app, this should be hashed
        "disabled": False,
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password (in real app, use proper hashing like bcrypt)"""
    return plain_password == hashed_password

def get_user(db, username: str) -> Optional[UserInDB]:
    """Get user from database"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user"""
    user = get_user(fake_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=TokenResponse, summary="Generate JWT Token")
async def login_for_access_token(form_data: TokenRequest):
    """
    Generate a JWT access token for authentication.

    Requires username and password.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/users/me", response_model=User, summary="Get Current User")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information from JWT token.

    Requires a valid JWT token in the Authorization header.
    """
    return current_user

@app.get("/protected", summary="Protected Endpoint")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    """
    A protected endpoint that requires authentication.

    Returns a welcome message with the current user's information.
    """
    return {
        "message": f"Hello, {current_user.username}! This is a protected endpoint.",
        "user_info": {
            "username": current_user.username,
            "timestamp": datetime.utcnow().isoformat()
        }
    }

@app.get("/validate", summary="Validate JWT Token")
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Validate a JWT token and return user information.

    This endpoint can be used to check if a token is valid.
    """
    return {
        "valid": True,
        "user": {
            "username": current_user.username,
            "authenticated_at": datetime.utcnow().isoformat()
        }
    }

@app.get("/", summary="Service Health Check")
async def root():
    """Health check endpoint"""
    return {
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
