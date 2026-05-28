import json
import os
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import get_db
from models import Subscription, User

router = APIRouter(prefix='/auth', tags=['auth'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
ALGORITHM = 'HS256'

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    skills: list[str] = []
    industry: str = ''
    stage: str = 'idea'
    preferences: dict = {}

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    skills: list[str]
    industry: str
    stage: str
    preferences: dict
    plan: str = 'free'

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def serialize_user(user: User, plan: str = 'free') -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        skills=json.loads(user.skills or '[]'),
        industry=user.industry,
        stage=user.stage,
        preferences=json.loads(user.preferences or '{}'),
        plan=plan
    )

def create_access_token(user_id: int) -> str:
    expires = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({'sub': str(user_id), 'exp': expires}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> User:
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get('sub'))
    except (JWTError, TypeError, ValueError):
        raise credentials_error
    user = db.get(User, user_id)
    if not user:
        raise credentials_error
    return user

@router.post('/register', response_model=TokenResponse)
def register(payload: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=409, detail='Email already registered')
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        skills=json.dumps(payload.skills),
        industry=payload.industry,
        stage=payload.stage,
        preferences=json.dumps(payload.preferences)
    )
    db.add(user)
    db.flush()
    db.add(Subscription(user_id=user.id, plan='free'))
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(user.id), user=serialize_user(user))

@router.post('/login', response_model=TokenResponse)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    return TokenResponse(access_token=create_access_token(user.id), user=serialize_user(user, subscription.plan if subscription else 'free'))

@router.get('/me', response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    subscription = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    return serialize_user(current_user, subscription.plan if subscription else 'free')
