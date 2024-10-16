import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from jose import JWTError, jwt
from datetime import UTC, datetime, timedelta
import bcrypt
from agendardel.config import settings
from typing import Optional


SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api.API_V1+"/user/login")


def to_bits(*args):
    return tuple(s.encode('utf-8') for s in args)

def to_str(*args):
    return tuple(b.decode('utf-8') for b in args)

def hash_pwd(pwd: str) -> str:
    salt = bcrypt.gensalt()
    return to_str(bcrypt.hashpw(*to_bits(pwd), salt))[0]

def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    return bcrypt.checkpw(*to_bits(plain_pwd, hashed_pwd))


def create_access_token(data: dict, expires_delta:timedelta|None=None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(request: Request, raise_exception: bool = True) -> Optional[str]:
    token = request.cookies.get("access_token")
    if not token:
        if raise_exception:
            return None  # Apenas retorna None quando o token não está presente
        return None

    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            return None
        
        return username
    except JWTError:
        return None