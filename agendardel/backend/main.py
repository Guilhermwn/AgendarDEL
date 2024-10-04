from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session, select

import htpy as h

from .database import engine
from .models import UserCreate, UserPublic, User
from agendardel.frontend.components.auth import Form
from agendardel.utils import HTPYResponse


router = APIRouter()


# === USER ENDPOINTS ===

def user_register_response():
    SUCCESS_CSS = """
    :root {
        --success: 134.6 61.2% 41.4%; /* Cor verde */
        --success-foreground: 134.6 100% 98%; /* Cor clara para o texto */
    }
    .bg-success {
        background-color: hsl(var(--success)); /* Usando a variável de fundo success */
    }
    """

    return HTPYResponse(h.div[
                h.style[SUCCESS_CSS],
                h.span(".uk-label.uk-label-primary.bg-success.uk-padding-small.uk-width-1-1.uk-margin")["✔ Usuário criado!"]
            ])

@router.post("/user/register", response_model=UserPublic, tags=["Backend | User"])
def user_register(user: UserCreate, request: Request):
    with Session(engine) as session: # Start a new session on the engine
        statement = select(User).where(User.username == user.username)
        result = session.exec(statement).first()
        
        if result:
            raise HTTPException(status_code=409, detail="Username already registered")
        
        new_user = User.model_validate(user) # create an instance model of the user
        session.add(new_user) # add the new user to the session
        session.commit() # commit the session to the database connected
        session.refresh(new_user) # update the information on the session

        if request.headers.get("hx-request") == "true":
            return user_register_response()
        else:
            return new_user # returns a json string representing with the new user info


@router.get("/user/users", response_model=list[UserPublic], tags=["Backend | User"])
def list_users():
    with Session(engine) as session: # Start a new session on the engine 
        statement = select(User) # Creates a statement to select the whole user database
        users = session.exec(statement).all() # Execute the SQL statement in the database and returns a list of users in the database
        return users # Returns a list of users in the database


# === USER ENDPOINTS ===