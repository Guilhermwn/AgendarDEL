# agendardel/frontend/main.py

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
import uuid

from agendardel.backend.models import Event, User
from agendardel.backend.database import engine
from agendardel.utils import HTPYResponse
from agendardel.security import verify_token
from .components import auth, dashboard, subscribe

router = APIRouter()


@router.get("/", response_class=HTPYResponse, tags=["Frontend | Page"])
def authpage(request: Request):
    username = verify_token(request, raise_exception=False)
    if username:
        return RedirectResponse("/dashboard")
    return HTPYResponse(auth.AuthPage())


@router.get("/dashboard", response_class=HTPYResponse, tags=["Frontend | Page"])
def dashboardpage(request: Request):
    username = verify_token(request, raise_exception=False)
    if not username:
        return RedirectResponse("/")
    
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        logged_user: User | None = session.exec(statement).first()
        user_events = logged_user.events
    return HTPYResponse(dashboard.DashboardPage(logged_user, user_events))


@router.get("/subscribe/{event_id}", response_class=HTPYResponse, tags=["Frontend | Page"])
def subscribepage(event_id:str, request: Request):
    with Session(engine) as session:
        try:
            event_id = uuid.UUID(event_id)
        except ValueError:
            return RedirectResponse("/")

        statement = select(Event).where(Event.id == event_id)
        event: Event | None = session.exec(statement).first()

    return HTPYResponse(subscribe.SubscribePage(event))