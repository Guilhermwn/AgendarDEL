# agendardel/frontend/main.py

from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from datetime import time, timedelta, datetime
import uuid

from agendardel.backend.models import Attendee, Event, User
from agendardel.backend.database import engine
from agendardel.utils import HTPYResponse
from agendardel.security import verify_token
from .components import auth, dashboard, subscribe, new_event, edit


router = APIRouter()


@router.get("/", response_class=HTPYResponse, tags=["Frontend | Page"])
def authpage(request: Request):
    username = verify_token(request, raise_exception=False)
    if username:
        return RedirectResponse("/dashboard")
    return HTPYResponse(auth.AuthPage())


@router.get("/dashboard", response_class=HTPYResponse, tags=["Frontend | Page"])
def dashboardpage(request: Request, response: Response):
    username = verify_token(request, raise_exception=False)
    if not username:
        return RedirectResponse("/")
    
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        logged_user: User | None = session.exec(statement).first()
        print(logged_user)
        if logged_user:
            user_events = logged_user.events
        else:
            response.delete_cookie("access_token")
            return RedirectResponse("/")
    return HTPYResponse(dashboard.DashboardPage(logged_user, user_events, request))


@router.get("/dashboard/new-event", response_class=HTPYResponse, tags=["Frontend | Page"])
def neweventpage(request: Request):
    username = verify_token(request, raise_exception=False)
    if not username:
        return RedirectResponse("/")
    
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        logged_user: User | None = session.exec(statement).first()
        user_events = logged_user.events
    return HTPYResponse(new_event.NewEventPage(logged_user, user_events, request))


def schedule_list(start:time, end:time, duration:int):
    duration = timedelta(minutes=duration)

    start = datetime.combine(datetime.now(), start)
    end = datetime.combine(datetime.now(), end)

    current = start
    schedules = []

    while current < end:
        schedules.append(current)

        current += duration

    return schedules

@router.get("/subscribe/{event_id}", response_class=HTPYResponse, tags=["Frontend | Page"])
def subscribepage(event_id:str):
    with Session(engine) as session:
        try:
            event_id = uuid.UUID(event_id)
        except ValueError:
            return RedirectResponse("/")

        statement = select(Event).where(Event.id == event_id)
        event: Event | None = session.exec(statement).first()
        
        if not event:
            return RedirectResponse("/")
        
        current_attendees: list[Attendee] | None = event.attendees

        occupied_times = []
        for one in current_attendees:
            occupied_times.append(datetime.combine(datetime.now(), one.subscribed_time))

        schedule_times = schedule_list(event.start_time, event.end_time, event.duration)

        intersection = set(occupied_times) & set(schedule_times)
        
        schedule_times = [ item for item in schedule_times if item not in intersection ]

        statement = select(User).where(event.owner_id == User.id)
        creator: User| None = session.exec(statement).first()

    return HTPYResponse(subscribe.SubscribePage(creator, event, schedule_times))


@router.get("/dashboard/{event_id}/edit", response_class=HTPYResponse, tags=["Frontend | Page"])
def editpage(event_id:str, request: Request):
    username = verify_token(request, raise_exception=False)
    if not username:
        return RedirectResponse("/")
    
    with Session(engine) as session:
        try:
            event_id = uuid.UUID(event_id)
        except ValueError:
            return RedirectResponse("/")

        statement = select(Event).where(Event.id == event_id)
        event: Event | None = session.exec(statement).first()

        if not event:
            return RedirectResponse("/")
        
        attendees: list[Attendee] = event.attendees

    return HTPYResponse(edit.EditPage(event, attendees,request))