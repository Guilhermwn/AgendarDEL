# agendardel/frontend/main.py

from fastapi import APIRouter

from ..utils import HTPYResponse
from .components import auth

router = APIRouter()

@router.get("/", response_class=HTPYResponse, tags=["Frontend | Page"])
def authpage():
    return HTPYResponse(auth.AuthPage())