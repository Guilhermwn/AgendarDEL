# agendardel/frontend/main.py

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from ..utils import HTPYResponse
from .components import auth, dashboard
from agendardel.backend.main import verify_token

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
    return HTPYResponse(dashboard.DashboardPage())