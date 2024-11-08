# agendardel/backend/main.py

from uuid import UUID
from fastapi import (
    APIRouter, 
    HTTPException, 
    Request, 
    Depends,
    Response, 
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from dotenv import load_dotenv
from datetime import datetime, timedelta

from .database import engine

from .models import Attendee, AttendeeBase, UserCreate, UserPublic, User
from .models import Event, EventBase, EventCreate, EventUpdate
from .models import LabelResponse

from agendardel.security import (
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    verify_pwd,
    hash_pwd
)

from agendardel.logger import logger

logger.info("API | Inicializada")

load_dotenv()

router = APIRouter()


# === USER ENDPOINTS ===

@router.post("/user/login", tags=["Backend | Auth"])
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
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
            expires=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        response.headers["HX-Redirect"] = "/dashboard"
        return response


@router.get("/user/logout", tags=["Backend | Auth"])
def user_logout(request: Request, response: Response):
    response = Response()
    response.delete_cookie(key="access_token")
    response.headers["HX-Redirect"] = "/"
    return response


@router.post("/user/register", response_model=UserPublic, tags=["Backend | Auth"])
def user_register(user: UserCreate, request: Request):
    htmx = request.headers.get('HX-Request') == "true"

    if not user.username.isalnum():
        if htmx:
            return LabelResponse.error("Username não pode conter espaços ou símbolos")
        raise HTTPException(status_code=422, detail="Username não pode conter espaços ou símbolos")
        
    if len(user.password) < 4:
        if htmx:
            return LabelResponse.error("Senha precisa ser maior que 4 caracteres")
        raise HTTPException(status_code=422, detail="Senha precisa ser maior que 4 caracteres")

    statement = select(User).where(User.username == user.username)
    
    hash_password = hash_pwd(user.password)
    extra_data = {"password": hash_password}
    new_user = User.model_validate(user, update=extra_data)
    
    
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

            logger.info(f"API | Novo usuário cadastrado [ {new_user.username} ]")

            if htmx:
                return LabelResponse.success("Usuário criado com sucesso.")
            else:
                return new_user


# @router.get("/user/users", response_model=list[UserPublic], tags=["Backend | User"])
# def list_users():
#     with Session(engine) as session:
#         statement = select(User)
#         users: list[User] = session.exec(statement).all()
#         return users


# === USER ENDPOINTS ===


# === EVENT ENDPOINTS ===


@router.post("/events/add", response_model=EventBase, tags=["Backend | Event"])
def add_event(event: EventCreate, request: Request):
    htmx = request.headers.get('HX-Request') == "true"

    # Verifique se a data do evento é anterior ao dia atual
    if event.date.date() < datetime.now().date():
        if htmx:
            return LabelResponse.error("A data do evento não pode ser anterior à data atual.", status_code=409)
        raise HTTPException(status_code=409, detail="A data do evento não pode ser anterior à data atual.")
    
    # Conecte ao banco de dados
    with Session(engine) as session:
        # Valide o evento
        new_event = Event.model_validate(event)

        # Adicione o evento ao banco de dados
        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        # Retorne diferentes respostas dependendo do tipo de requisição (HTMX ou não)
        if request.headers.get('HX-Request') == "true":
            return LabelResponse.success("Evento criado com sucesso.")
        else:
            return new_event

# @router.get("/events/all", response_model=list[EventBase], tags=["Backend | Event"])
# def get_events():
#     with Session(engine) as session:
#         statement = select(Event)
#         events: list[Event] = session.exec(statement).all()
#         return events
    
@router.get("/events/{username}", tags=["Backend | Event"])
def get_events_from_user(username:str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        db_user = session.exec(statement).first()
        if not db_user:
            raise HTTPException(404, detail="User not found")
        return db_user.events
    

@router.delete("/events/{event_id}", tags=["Backend | Event"])
def delete_event(event_id:str, request:Request):
    htmx = request.headers.get('HX-Request') == "true"
    
    with Session(engine) as session:
        
        try:
            event_id = UUID(event_id)
        except ValueError:
            raise HTTPException(404, detail="Invalid ID format")

        statement = select(Event).where(Event.id == event_id)
        event: Event | None = session.exec(statement).first()
        if not event:
            raise HTTPException(404, detail="Event not found")
    
        session.delete(event)
        session.commit()

        if htmx:
            response = Response()
            response.headers["HX-Refresh"] = "true"
            return response

        return  {"message": "Event deleted", "event_name": f"{event.title}", "event_id": f"{event.id}"}


@router.patch("/events/{event_id}", tags=["Backend | Event"])
def patch_event(event_id:str, event_update:EventUpdate, request:Request):
    htmx = request.headers.get("HX-Request") == "true"
    time_now = datetime.now()

    with Session(engine) as session:
        try:
            event_id = UUID(event_id)
        except ValueError:
            raise HTTPException(404, detail="Invalid ID format")
        
        statement = select(Event).where(Event.id == event_id)
        event: Event | None = session.exec(statement).first()

        if not event:
            raise HTTPException(404, detail="Event not found")
        
        event_items = event_update.model_dump(exclude_unset=True).items()


        for key, value in event_items:
            setattr(event, key, value)
        
        if event.date.date() < time_now.date():
            if htmx:
                return LabelResponse.error("A data do evento não pode ser anterior à data atual.", status_code=409)
            raise HTTPException(status_code=409, detail="A data do evento não pode ser anterior à data atual.")
        
        print(
            event.start_time,
            event.end_time
        )

        if event.end_time < event.start_time:
            if htmx:
                return LabelResponse.error("Horário de fim precisa ser após o horário de início.", status_code=409)
            raise HTTPException(status_code=409, detail="Horário de fim precisa ser após o horário de início.")

        session.add(event)
        session.commit()
        session.refresh(event)
        
        if htmx:
            response = Response()
            response.headers["HX-Refresh"] = "true"
            return response

        return {"message": "Event updated", "event": event}


# === EVENT ENDPOINTS ===


# === ATTENDEE ENDPOINTS ===

@router.post("/attendee/subscribe/{event_id}", tags=["Backend | Attendee"])
def subscribe_attendee(attendee:AttendeeBase, request:Request, event_id:str):
    htmx = request.headers.get("HX-Request") == "true"
    
    with Session(engine) as session:
        try:
            event_id = UUID(event_id)
        except ValueError:
            raise HTTPException(404, detail="Invalid ID format")
        
        extra_data = {"event_id": event_id}
        new_attendee = Attendee.model_validate(attendee, update=extra_data)
        
        event: Event | None = session.exec(
            select(Event).where(Event.id == event_id)
        ).first()

        event_attendees:list[Attendee] | None = event.attendees
        if event_attendees:
            for participante in event_attendees:
                if participante.email == new_attendee.email:
                    if htmx:
                        return LabelResponse.error("Email já cadastrado no evento", status_code=409)
                    raise HTTPException(409, detail="Email já cadastrado no evento")

        
        session.add(new_attendee)
        session.commit()
        session.refresh(new_attendee)

        if htmx:
            return LabelResponse.success("Inscrito no evento com sucesso!")
        else:
            return new_attendee
    
@router.get("/attendee/{event_id}", tags=["Backend | Attendee"])
def get_attendees_from_event(event_id:str):
     with Session(engine) as session:
        try:
            event_id = UUID(event_id)
        except ValueError:
            raise HTTPException(404, detail="Invalid ID format")
        
        statement = select(Event).where(Event.id == event_id)
        event = session.exec(statement).first()

        if not event:
            raise HTTPException(404, "Event not found")
        
        return event.attendees

@router.delete("/attendee/{attendee_id}", tags=["Backend | Event"])
def delete_attendee(attendee_id:str, request:Request):
    htmx = request.headers.get('HX-Request') == "true"
    
    with Session(engine) as session:
        
        try:
            attendee_id = UUID(attendee_id)
        except ValueError:
            raise HTTPException(404, detail="Invalid ID format")

        statement = select(Attendee).where(Attendee.id == attendee_id)
        attendee: Attendee | None = session.exec(statement).first()
        
        if not attendee:
            raise HTTPException(404, detail="Attendee not found")
    
        session.delete(attendee)
        session.commit()

        if htmx:
            response = Response()
            response.headers["HX-Refresh"] = "true"
            return response

        return  {"message": "Attendee deleted", "event_name": f"{attendee.name}", "attendee_id": f"{attendee.id}"}