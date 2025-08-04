"""
Authentication service for user management
"""

import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from database.connection import SessionLocal
from models.user import User, UserCreate, UserLogin
from typing import Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def create_token(self, user: User) -> str:
        """Create JWT token for user."""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {"sub": str(user.id), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[User]:
        """Verify JWT token and return user."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = int(payload.get("sub"))
            if user_id is None:
                return None
        except jwt.PyJWTError:
            return None
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user
        finally:
            db.close()
    
    def register_user(self, user_data: dict) -> User:
        """Register a new user."""
        db = SessionLocal()
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                raise Exception("User already exists")
            
            # Create new user
            hashed_password = self.get_password_hash(user_data["password"]) if user_data.get("password") else None
            user = User(
                email=user_data["email"],
                name=user_data["name"],
                provider=user_data.get("provider", "email"),
                hashed_password=hashed_password,
                avatar_url=user_data.get("avatar_url")
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()
    
    def login_user(self, credentials: dict) -> str:
        """Login user and return token."""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == credentials["email"]).first()
            if not user:
                raise Exception("Invalid credentials")
            
            if user.provider == "email" and user.hashed_password:
                if not self.verify_password(credentials["password"], user.hashed_password):
                    raise Exception("Invalid credentials")
            
            return self.create_token(user)
        finally:
            db.close()
    
    def verify_google_token(self, token: str) -> User:
        """Verify Google token and return user (simplified for testing)."""
        # For testing, we'll create a mock user
        # In production, you'd verify the Google token properly
        db = SessionLocal()
        try:
            # Check if user exists
            user = db.query(User).filter(User.email == "test@example.com").first()
            if not user:
                # Create test user
                user = User(
                    email="test@example.com",
                    name="Test User",
                    provider="google",
                    avatar_url="https://via.placeholder.com/150"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            return user
        finally:
            db.close() 