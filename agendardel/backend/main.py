# agendardel/backend/main.py

from fastapi import APIRouter, HTTPException, Request
from sqlmodel import Session, select

import htpy as h

from agendardel.utils import HTPYResponse
from .database import engine
from .models import UserCreate, UserPublic, User

router = APIRouter()


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


@router.post("/user/register", response_model=UserPublic, tags=["Backend | User"])
def user_register(user: UserCreate, request: Request):
    statement = select(User).where(User.username == user.username)
    new_user = User.model_validate(user)
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