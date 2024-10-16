from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
import uuid
from agendardel.utils import HTPYResponse
import htpy as h


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: uuid.UUID

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
    events: list["Event"] = Relationship(back_populates="owner")

class UserLogin(SQLModel):
    username: str
    password: str


class EventBase(SQLModel):
    title: str
    description: str = Field(default=None)
    date: datetime = Field(nullable=False, index=True)
    duration: int = Field(ge=0, nullable=False)

class EventCreate(EventBase):
    owner_id: uuid.UUID = Field(foreign_key="user.id")

class Event(EventCreate, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner: User | None = Relationship(back_populates="events")



class LabelResponse:
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
    def success(self, text:str) -> HTPYResponse:
        return HTPYResponse(h.div[
                h.style[self.SUCCESS_CSS],
                h.span(".uk-label.uk-label-primary.bg-success.uk-padding-small.uk-width-1-1.uk-margin.uk-text-center")[text]
            ])
    
    @classmethod
    def error(self, text:str, status_code:int=422) -> HTPYResponse:
        return HTPYResponse(h.div[
                h.style[self.SUCCESS_CSS],
                h.span(".uk-label.uk-label-primary.bg-error.uk-padding-small.uk-width-1-1.uk-margin.uk-text-center")[text]
            ], status_code=status_code)