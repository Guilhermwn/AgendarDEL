# agendardel/backend/main.py

from fastapi import (
    APIRouter, 
    HTTPException, 
    Request, 
    Depends,
    Response, 
    status,
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from dotenv import load_dotenv
from datetime import timedelta

from .database import engine

from .models import UserCreate, UserPublic, User
from .models import Event, EventBase, EventCreate
from .models import LabelResponse

from agendardel.security import (
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    verify_pwd,
    hash_pwd
)

load_dotenv()

router = APIRouter()


# === USER ENDPOINTS ===

@router.post("/user/login", tags=["Backend | User"])
def user_login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    statement = select(User).where(User.username == form_data.username)
    htmx = request.headers.get('HX-Request') == "true"
    with Session(engine) as session:
        user = session.exec(statement).first()
        if not user or not verify_pwd(form_data.password, user.password):
            if htmx:
                return LabelResponse.error("Username ou senha incorretos", status_code=401)
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
        response = JSONResponse(content={
            "access_token": access_token, 
            "token_type": "bearer"
        })
        response.set_cookie(
            key="access_token", 
            value=access_token, 
            httponly=True, 
            # secure=True,
            max_age=30 * 60,
            expires=30 * 60
        )
        print(request.url.scheme)
        response.headers["HX-Redirect"] = "/dashboard"
        return response


@router.get("/user/logout")
def user_logout(request: Request, response: Response):
    response = Response()
    response.delete_cookie(key="access_token")
    response.headers["HX-Redirect"] = "/"
    return response


@router.post("/user/register", response_model=UserPublic, tags=["Backend | User"])
def user_register(user: UserCreate, request: Request):

    if not user.username.isalnum():
        return LabelResponse.error("Username não pode conter espaços ou símbolos")
    if len(user.password) < 4:
        return LabelResponse.error("Senha precisa ser maior que 4 caracteres")
    statement = select(User).where(User.username == user.username)
    
    hash_password = hash_pwd(user.password)
    extra_data = {"password": hash_password}
    new_user = User.model_validate(user, update=extra_data)
    
    htmx = request.headers.get('HX-Request') == "true"
    
    with Session(engine) as session:
        result: User | None = session.exec(statement).first()    
        if result:
            if htmx:
                return LabelResponse.error("Nome de usuário já em uso, escolha outro.", status_code=409)
            else:
                raise HTTPException(409, "Username already registered")
        else:    
            session.add(new_user)
            session.commit() 
            session.refresh(new_user)
            if htmx:
                return LabelResponse.success("Usuário criado com sucesso.")
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
        users: list[User] = session.exec(statement).all()
        return users


# === USER ENDPOINTS ===


# === EVENT ENDPOINTS ===


@router.post("/events/add", response_model=EventBase, tags=["Backend | Event"])
def add_event(request: Request, event: EventCreate):
    new_event = Event.model_validate(event)
    htmx = request.headers.get('HX-Request') == "true"
    with Session(engine) as session:
        session.add(new_event)
        session.commit()
        session.refresh(new_event)
        return new_event

@router.get("/events/all", response_model=list[EventBase])
def get_events():
    with Session(engine) as session:
        statement = select(Event)
        events: list[Event] = session.exec(statement).all()
        return events
    
@router.get("/events/{username}")
def get_events_from_user(username:str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        db_user = session.exec(statement).first()
        if not db_user:
            raise HTTPException(404, detail="User not found")
        return db_user.events
        


