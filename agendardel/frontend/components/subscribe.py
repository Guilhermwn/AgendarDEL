from uuid import UUID
import htpy as h

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

def breadcrumb(itens: dict[str,str]):
    return h.div(".uk-container.uk-margin")[
        h.nav(aria_label="Breadcrumb")[
            h.ul(".uk-breadcrumb")[
                [ h.li[h.a(href=item[1])[item[0]]] for item in itens.items()],
            ]
        ]
    ],

def event_information(creator: User, event: Event):
    return h.div(".uk-card")[
        # Header do card de evento
        h.div(".uk-card-header")[
            h.h3(".uk-card-title")[event.title],
            h.p(".uk-margin-xsmall-top uk-text-small text-muted-foreground")[event.description]
        ],
        # Corpo do card de evento
        h.div(".uk-card-body")[
            h.ul(".uk-list uk-list-divider uk-padding uk-card")[
                h.li[f"Criador: {creator.username}"],
                h.li[f"Data: {event.date.date().strftime('%d/%m/%Y')}"],
                h.li[f"Início: {event.start_time.strftime('%H:%M')}h"],
                h.li[f"Fim: {event.end_time.strftime('%H:%M')}h"],
                h.li[f"Duração: {event.duration} min"]
            ]
        ]
    ]

# def schedules_list(start:time, end:time, duration:int):
#     duration = timedelta(minutes=duration)

#     start = datetime.combine(datetime.now(), start)
#     end = datetime.combine(datetime.now(), end)

#     current = start
#     schedules = []

#     while current < end:
#         schedules.append(current)

#         current += duration

#     return schedules

def event_subscription_form(event_id:UUID, schedule_list: list):
    # schedule_times = schedules_list(start, end, duration)
    schedule_times = schedule_list

    schedule_options = [ h.option(value=f"{schedule.time()}")[f"{schedule.time()}"] for schedule in schedule_times]

    return h.div(".uk-card")[
        h.div(".uk-card-header")[ h.h3(".uk-card-title")["Inscrever no evento"] ],
        h.div(".uk-padding-medium", hx_ext="response-targets")[
            h.form(
                ".uk-form-stacked", 
                hx_post=f"/API/V1/attendee/subscribe/{event_id}", 
                hx_target="#response",
                hx_target_error="#response",
                hx_ext="json-enc",
                hx_trigger="submit",
                hx_swap="innerHTML",
            )[
                h.div(".uk-margin")[
                    h.label(".uk-form-label", for_="name")["Nome"],
                    h.div(".uk-form-controls")[
                        h.input("#name.uk-input", name="name", type="text", placeholder="Seu nome", required="")
                    ]
                ],
                h.div(".uk-margin")[
                    h.label(".uk-form-label", for_="email")["Email"],
                    h.div(".uk-form-controls")[
                        h.input("#email.uk-input", name="email", type="email", placeholder="user@example.com", required="")
                    ]
                ],
                h.div(".uk-margin")[
                    h.label(".uk-form-label", for_="subscribed_time")["Selecionar horário"],
                    h.div(".uk-form-controls")[
                        h.select("#subscribed_time.uk-select", name="subscribed_time", required="")[
                            schedule_options
                        ]
                    ]
                ],
                h.button(".uk-button uk-button-primary", type="submit")["INSCREVER-SE"],
                h.div("#response")
            ]
        ]
    ]

def SubscribePage(
        creator: User,
        event: Event,
        schedule: list
) -> h.Element:
    return basepage(
        page_title=f"Subscribe | {event.title}",
        content=[
            navbar(),
            breadcrumb({
                "Subscribe": ""
            }),
            h.div(".uk-container uk-flex uk-flex-around uk-flex-wrap uk-flex-wrap-around uk-margin-medium uk-margin-bottom")[
                h.div(".uk-width-1-4@m uk-width-1-1@s uk-padding-small")[
                    event_information(creator, event)
                ],
                h.div(".uk-width-2-3@m uk-width-1-1@s uk-padding-small")[
                    event_subscription_form(event.id, schedule)
                ]
            ]
        ]
    )