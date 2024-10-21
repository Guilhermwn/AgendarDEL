import htpy as h
from typing import Optional

from markupsafe import Markup

from agendardel.backend.models import Event, User
from .page import basepage

uk_icon = h.Element("uk-icon")

def navbar():
    return h.nav(
        ".uk-navbar-container.uk-padding", 
        uk_navbar="",
        uk_dropnav="mode: click", 
        style="z-index: 8888;")[
            h.div(".uk-navbar-left")[h.h3(".uk-h3")["Subscribe"]],
    ]

def SubscribePage(
        event: Event
) -> h.Element:
    return basepage(
        page_title=f"Subscribe | {event.title}",
        content=[
            navbar(),
            h.p[f"EVENTO: {event.title}"]
        ]
    )