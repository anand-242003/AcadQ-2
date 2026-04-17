import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from models.schemas import (
    RegisterRequest, LoginRequest, AuthResponse, UserResponse
)
from database.mongo import find_user_by_email, insert_user, user_exists

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", "7"))

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(days=EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    if user_exists(request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(request.password)
    user_doc = {
        "name": request.name,
        "email": request.email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow(),
    }
    insert_user(user_doc)

    token = create_access_token(request.email)
    return AuthResponse(token=token, name=request.name, email=request.email)


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    user = find_user_by_email(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(request.email)
    return AuthResponse(token=token, name=user["name"], email=user["email"])


@router.get("/me", response_model=UserResponse)
async def me(current_user: str = Depends(get_current_user)):
    user = find_user_by_email(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(name=user["name"], email=user["email"])
