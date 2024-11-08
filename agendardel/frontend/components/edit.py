from uuid import UUID
import uuid
from fastapi import Request
import htpy as h

from agendardel.backend.models import Attendee, Event
from .page import basepage

uk_icon = h.Element("uk-icon")

def navbar(host):
    return h.nav(".uk-navbar-container.uk-padding", uk_navbar="",uk_dropnav="mode: click", style="z-index: 8888;")[
        h.div(".uk-navbar-left")[h.h3(".uk-h3")["Editar"]],
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


def event_form(
        event_id: UUID,
        label_text,
        input_id,
        input_name,
        input_type="text",
        required=True,
        placeholder="",
        value="",
        margin=True
    ):
    return h.form(
        ".uk-form-stacked",
        hx_patch=f"/API/V1/events/{event_id}",
        hx_headers='{"Content-Type": "application/json"}',
        hx_ext="json-enc",
        hx_trigger="submit",
        hx_swap="innerHTML",
        hx_target="#form-response",
        hx_target_error="#form-response"
    )[
        h.div(".uk-margin" if margin else "")[
            h.label(".uk-form-label", for_=input_id, aria_label=label_text)[label_text],
            h.div(".uk-flex.uk-flex-middle")[
                h.input(
                    f"#{input_id}.uk-input.uk-flex-1",
                    name=input_name,
                    type_=input_type,
                    required=required,
                    placeholder=placeholder,
                    value=value,
                    aria_describedby=f"{input_id}-help"
                ),
                h.button(".uk-button.uk-button-primary.uk-margin-small-left", type_="submit")["EDITAR"]
            ]
        ],
    ]

def delete_attendee_modal(attendee_id:uuid.UUID):
    return h.div(f"#delete-attendee-{attendee_id}-modal.uk-modal.uk-flex-top", uk_modal="", style="z-index: 9999;")[
        h.div(".uk-modal-body.uk-modal-dialog.uk-margin-auto-vertical")[
            h.div(".uk-modal-header")[h.h2(".uk-modal-title")["Deletar participante ?"]],
            h.div(".uk-modal-footer.uk-text-right")[
                h.button(".uk-modal-close.uk-button.uk-button-default", type_="button")["Cancelar"],
                h.button(".uk-button.uk-button-danger", type_="button",hx_delete=f"/API/V1/attendee/{attendee_id}")["Deletar"],
            ]
        ]
    ]

def attendee_table_row(attendee: Attendee):
    return [
        h.td[attendee.name],
        h.td[attendee.email],
        h.td[f"{attendee.subscribed_time.strftime('%H:%M') if attendee.subscribed_time else None}"],
        h.td[
            h.button(".uk-icon-button uk-icon-button-outline", uk_toggle=f"target: #delete-attendee-{attendee.id}-modal")[
                uk_icon(icon="trash")
            ],
            delete_attendee_modal(attendee.id)
    ]]

def attendee_table(attendees: list[Attendee]):
    return h.table(".uk-table uk-table-divider uk-table-hover")[
        h.thead[
            h.tr[
                h.th["Nome"],
                h.th["Email"],
                h.th["Horário"],
                h.th["Deletar"],
            ],
        ],
        h.tbody[
            [ h.tr[attendee_table_row(attendee)] for attendee in attendees ]
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

def short_text(text:str, amount:int):
    return [text if len(text.split())<amount 
            else " ".join(text.split()[:amount])+"..."][0]

def event_card(event: Event):
    return h.div(".uk-card uk-card-default uk-padding-small uk-margin-medium")[
                h.div(".uk-panel.uk-flex.uk-flex-middle.uk-width-expand")[  # Flex container para alinhar o ícone e o texto à esquerda
                    h.div(".uk-margin-right uk-margin-left")[  # Div que contém o ícone com margem à direita
                        uk_icon(icon="calendar-days", width="30", height="30")  # Ícone do evento
                    ],
                    h.div[
                        h.div(".uk-flex")[
                            h.p(".uk-text-muted", style="margin-right:5px;")["Título:"],
                            h.p[event.title],
                        ],
                        h.div(".uk-flex")[
                            h.p(".uk-text-muted", style="margin-right:5px;")["Descrição:"],
                            h.p[event.description]
                        ],
                        h.div(".uk-flex")[
                            h.p(".uk-text-muted", style="margin-right:5px;")["Data:"],
                            h.p[event.date.strftime("%d/%m/%Y")],
                        ],
                        h.div(".uk-flex")[
                            h.p(".uk-text-muted", style="margin-right:5px;")["Duração:"],
                            h.p[event.duration, "min"]
                        ],
                        h.div(".uk-flex")[
                            h.p(".uk-text-muted", style="margin-right:5px;")["Horário de Início:"],
                            h.p[event.start_time.strftime("%H:%M"), "h"]
                        ],
                        h.div(".uk-flex")[
                            h.p(".uk-text-muted", style="margin-right:5px;")["Horário de Fim:"],
                            h.p[event.end_time.strftime("%H:%M"), "h"]
                        ],
                    ]
                ],
            ],

def EditPage(
        event: Event,
        event_attendees: list[Attendee],
        request: Request
) -> h.Element:
    return basepage(
        page_title=f"Editar | {event.title}",
        content=[
            navbar(request.base_url),
            breadcrumb({
                "Dashboard": "/dashboard",
                "Editar": ""
            }),
            h.div(".uk-container")[
                h.div[h.h2(".uk-h2 uk-margin")["Editar Evento"]],
                event_card(event),
            ],
            h.div(".uk-container uk-flex uk-flex-wrap uk-flex-wrap-around uk-margin-medium uk-margin-bottom")[
                h.comment("EVENT DATA FORM DIV"),
                h.div(".uk-width-1-2@m uk-width-1-1@s uk-padding-small")[
                    h.div[
                        h.h1(".uk-heading-line uk-heading-small uk-margin uk-text-center")[
                            h.span["Novos dados"]
                        ]
                    ],
                    h.comment("EVENT DATA EDIT FORM"),
                    h.div(hx_ext="response-targets")[
                        event_form(event.id, "Título", "event-title", "title", placeholder="Novo título"),
                        event_form(event.id, "Descrição", "event-description", "description", placeholder="Nova descrição"),
                        event_form(event.id, "Data", "event-date", "date", "date"),
                        event_form(event.id, "Duração", "event-duration", "duration", input_type="number", placeholder="Nova duração"),
                        event_form(event.id, "Horário de Início", "event-start_time", "start_time", "time",),
                        event_form(event.id, "Horário de Fim", "event-end_time", "end_time", "time"),
                        h.div("#form-response")
                    ]
                ],
                h.comment("EVENT ATTENDEES LIST"),
                h.div(".uk-width-1-2@m uk-width-1-1@s uk-padding-small")[
                    h.h1(".uk-heading-line uk-heading-small uk-margin uk-text-center")[
                        h.span["Participantes"],
                    ],
                    h.div(".uk-overflow-auto")[
                        h.comment("ATTENDEE TABLE"),
                        attendee_table(event_attendees)
                    ]
                ],
            ]
        ]
    )