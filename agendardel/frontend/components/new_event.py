from datetime import datetime, timedelta
from fastapi import Request
import htpy as h

from agendardel.backend.models import Event, User
from .page import basepage

uk_icon = h.Element("uk-icon")


def navbar(host):
    return h.nav(".uk-navbar-container.uk-padding", uk_navbar="",uk_dropnav="mode: click", style="z-index: 8888;")[
        h.div(".uk-navbar-left")[h.h3(".uk-h3")["Novo Evento"]],
        h.div(".uk-navbar-right.")[
        h.ul(".uk-subnav")[
            h.li[
                h.a[h.img(".uk-border-pill", src=f"{host}static/no-user.webp", width="50", height="50")],
                h.div(".uk-drop.uk-dropdown")[
                    h.ul(".uk-dropdown-nav.uk-nav")[
                        h.li[h.a(href="#")["Perfil"]],
                        h.li[h.a(href="#", hx_get="/API/V1/user/logout")["Logout"]],
                    ]
                ]
            ],
        ]
    ]
]

def breadcrumb(itens: dict[str,str]):
    return h.div(".uk-container.uk-margin")[
        h.nav(aria_label="Breadcrumb")[
            h.ul(".uk-breadcrumb")[
                [ h.li[h.a(href=item[1])[item[0]]] for item in itens.items()],
            ]
        ]
    ],

def create_input_field(label_text, input_id, input_name, input_type="text", required=True, placeholder="", value="", margin=True):
    return h.div(".uk-margin" if margin else "")[
        h.label(".uk-form-label", for_=input_id)[label_text],
        h.div(".uk-form-controls")[
            h.input(f"#{input_id}.uk-input", name=input_name, type_=input_type, required=required, placeholder=placeholder, value=value)
        ],
    ]

def new_event_form(owner_id: str):
    current_date = datetime.now()
    later_time = current_date + timedelta(hours=5)

    return h.form(
        ".uk-form-stacked",
        hx_post="/API/V1/events/add",
        hx_headers='{"Content-Type": "application/json"}',
        hx_ext="json-enc",
        hx_trigger="submit",
        hx_swap="innerHTML",
        hx_target="#form-response",
        hx_target_error="#form-response"
    )[
        create_input_field("Título", "event-title", "title", placeholder="Meu evento..."),
        create_input_field("Descrição", "event-description", "description", placeholder="Um evento administrado pelo DEL.", required=False),
        create_input_field("Data", "event-date", "date", "date", value=current_date.date().strftime("%Y-%m-%d")),
        create_input_field("Duração", "event-duration", "duration", "number", placeholder="15 min"),
        h.div(".uk-grid-small.uk-child-width-1-2.uk-grid.uk-margin", uk_grid="")[
            create_input_field("Início", "event-start_time", "start_time", "time", value=current_date.time().strftime("%H:%M"), margin=False),
            create_input_field("Fim", "event-end_time", "end_time", "time", value=later_time.strftime("%H:%M"),margin=False),
        ],
        create_input_field("", "event-owner_id", "owner_id", "hidden", value=f"{owner_id}"),
        h.button(".uk-button.uk-button-primary.uk-width-1-1", type_="submit")["Criar"]
    ]

def NewEventPage(
        user_data: User,
        user_events: list[Event],
        request: Request
) -> h.Element:
    return basepage(
        page_title="Novo Evento",
        content=[
            navbar(request.base_url),
            breadcrumb({
                "Dashboard": "/dashboard",
                "Novo Evento": ""
            }),
            h.div(".uk-container.uk-margin-bottom")[
                h.div(".uk-card.uk-card-default")[
                    h.div(".uk-padding-medium", hx_ext="response-targets")[
                        new_event_form(user_data.id),
                        h.div("#form-response")
                    ]
                ]
            ]
        ]
    )