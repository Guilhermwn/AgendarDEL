import htpy as h
from .page import basepage

uk_icon = h.Element("uk-icon")

def DashboardPage():
    return basepage(
        page_title="Dashboard",
        content=[
            h.h1["DASHBOARD"],
        ]
    )