# agendardel/backend/main.py

import logging
from typing import Optional

logging.getLogger('passlib').setLevel(logging.ERROR)

from fastapi import (
    APIRouter, 
    HTTPException, 
    Request, 
    Depends, 
    status,
)
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import UTC, datetime, timedelta
from passlib.context import CryptContext

import htpy as h

from agendardel.config import settings
from agendardel.utils import HTPYResponse
from .database import engine
from .models import UserCreate, UserPublic, User


load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api.API_V1+"/user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password:str, hash_password:str):
    return pwd_context.verify(plain_password, hash_password)

def create_access_token(data: dict, expires_delta:timedelta|None=None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def verify_token(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token=token, key=SECRET_KEY,algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         print(f"AUTH -> {username}")

#         if username is None:
#             raise credentials_exception
        
#         return username
#     except JWTError:
#         raise credentials_exception



# def verify_token(request: Request):
#     token = request.cookies.get("access_token")
#     if not token:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
    
#     try:
#         # Decodificando o token JWT
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
        
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
        
#         return username
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# def verify_token(request: Request, raise_exception: bool = True) -> Optional[str]:
#     token = request.cookies.get("access_token")
#     if not token:
#         if raise_exception:
#             raise HTTPException(
#                 status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"}
#             )
#         return None  # Se não levantar exceção, retorna None para indicar ausência de autenticação

#     try:
#         # Decodifica o token JWT
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
        
#         if username is None:
#             if raise_exception:
#                 raise HTTPException(status_code=401, detail="Invalid token")
#             return None
        
#         return username
#     except JWTError:
#         if raise_exception:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return None


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


class RegisterResponse:
    SUCCESS_CSS = """
    :root {
        --success: 134.6 61.2% 41.4%; /* Cor verde */
        --success-foreground: 134.6 100% 98%; /* Cor clara para o texto */
        --error: 0 61.2% 41.4%; /* Cor vermelha para erros */
        --error-foreground: 0 100% 98%; /* Cor clara para o texto de erro */
    }
    .bg-success {
        background-color: hsl(var(--success)); /* Usando a variável de fundo success */
        color: hsl(var(--success-foreground)); /* Cor de texto clara */
    }
    .bg-error {
        background-color: hsl(var(--error)); /* Usando a variável de fundo error */
        color: hsl(var(--error-foreground)); /* Cor de texto clara */
    }
    """

    @classmethod
    def success(self) -> HTPYResponse:
        """
        Message: ✔ Usuário criado!\n
        Status code: 200 OK
        """
        return HTPYResponse(h.div[
                h.style[self.SUCCESS_CSS],
                h.span(".uk-label.uk-label-primary.bg-success.uk-padding-small.uk-width-1-1.uk-margin.uk-text-center")["Usuário criado com sucesso."]
            ])
    
    @classmethod
    def error(self) -> HTPYResponse:
        """
        Message: Usuário já cadastrado!\n
        Status code: 409 Conflict
        """
        return HTPYResponse(h.div[
                h.style[self.SUCCESS_CSS],
                h.span(".uk-label.uk-label-primary.bg-error.uk-padding-small.uk-width-1-1.uk-margin.uk-text-center")["Nome de usuário já em uso, escolha outro."]
            ], status_code=409)



# === USER ENDPOINTS ===

@router.post("/user/login", tags=["Backend | User"])
def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    statement = select(User).where(User.username == form_data.username)
    with Session(engine) as session:
        user = session.exec(statement).first()
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, 
            expires_delta=access_token_expires
        )
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        response.set_cookie(
            key="access_token", 
            value=access_token, 
            httponly=True, 
            secure=True,
            max_age=access_token_expires.total_seconds(),
            expires=access_token_expires.total_seconds()
        )
        response.headers["HX-Redirect"] = "/dashboard"

        return response


@router.post("/user/register", response_model=UserPublic, tags=["Backend | User"])
def user_register(user: UserCreate, request: Request):
    statement = select(User).where(User.username == user.username)
    
    hash_password = pwd_context.hash(user.password)
    extra_data = {"password": hash_password}
    new_user = User.model_validate(user, update=extra_data)
    
    htmx = request.headers.get('HX-Request') == "true"
    
    with Session(engine) as session:
        result: User | None = session.exec(statement).first()    
        if result:
            if htmx:
                return RegisterResponse.error()
            else:
                raise HTTPException(409, "Username already registered")
        else:    
            session.add(new_user)
            session.commit() 
            session.refresh(new_user)
            if htmx:
                return RegisterResponse.success()
            else:
                return new_user


@router.get("/user/users", response_model=list[UserPublic], tags=["Backend | User"])
def list_users():
    """
    Enpoint que retorna uma lista, contendo informações
    com schema UserPublic, dos usuários cadastrados no
    banco de dados
    """
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()
        return users


# === USER ENDPOINTS ===