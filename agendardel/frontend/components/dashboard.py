import uuid
import htpy as h
from typing import Optional

from markupsafe import Markup

from agendardel.backend.models import Event, User
from .page import basepage

uk_icon = h.Element("uk-icon")


def navbar():
    return h.nav(".uk-navbar-container.uk-padding", uk_navbar="",uk_dropnav="mode: click", style="z-index: 8888;")[
        h.div(".uk-navbar-left")[h.h3(".uk-h3")["Dashboard"]],
        h.div(".uk-navbar-right.")[
        h.ul(".uk-subnav")[
            h.li[
                h.a[h.img(".uk-border-pill", src="https://franken-ui.dev/images/avatar.jpg", width="50", height="50")],
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


def short_text(text:str, amount:int):
    return [text if len(text.split())<amount 
            else " ".join(text.split()[:amount])+"..."][0]

def delete_event_modal(event_id:uuid.UUID):
    return h.div("#delete-event-modal.uk-modal.uk-flex-top", uk_modal="", style="z-index: 9999;")[
        h.div(".uk-modal-body.uk-modal-dialog.uk-margin-auto-vertical")[
            h.div(".uk-modal-header")[h.h2(".uk-modal-title")["Deletar evento ?"]],
            h.div(".uk-modal-footer.uk-text-right")[
                h.button(".uk-modal-close.uk-button.uk-button-default", type_="button")["Cancelar"],
                h.button(".uk-button.uk-button-danger", type_="button",hx_delete=f"/API/V1/events/{event_id}")["Deletar"],
            ]
        ]
    ]

def no_event():
    return h.li(".uk-flex.uk-flex-wrap.uk-flex-between.uk-flex-middle.uk-padding-small")[
            h.div(".uk-panel.uk-flex.uk-flex-middle.uk-width-expand")[
                h.p["Sem eventos cadastrados..."]
            ]
        ]

def eventlist_item(event: Event):
    # Cria um item de lista <li> que representará um evento
    
    return h.li(".uk-flex.uk-flex-wrap.uk-flex-between.uk-flex-middle.uk-padding-small")[  # Alinha itens no centro e permite quebra de linha
        h.div(".uk-panel.uk-flex.uk-flex-middle.uk-width-expand")[  # Flex container para alinhar o ícone e o texto à esquerda
            h.div(".uk-margin-right")[  # Div que contém o ícone com margem à direita
                uk_icon(icon="calendar-days", width="30", height="30")  # Ícone do evento
            ],
            h.div[  # Div que contém o título e a descrição
                h.h3(".uk-text-lead.uk-text-truncate.uk-margin-remove")[
                    short_text(event.title, 4)  # Título do evento
                ],
                h.p(".uk-text-meta.uk-text-truncate.uk-margin-remove")[
                    short_text(event.description, 6)
                ],
                h.p(".uk-text-meta.uk-text-truncate.uk-margin-remove")[
                    f'{event.date.strftime("%d/%m/%Y")} | {event.duration} min'
                ],
            ]
        ],
        h.div(".uk-flex.uk-flex-right.uk-width-auto.uk-visible@s")[  # Botões visíveis apenas em telas grandes
            h.a(".uk-icon-button.uk-button-danger.uk-margin-small-right", uk_toggle="target: #delete-event-modal")[  # Botão "Excluir"
                uk_icon(icon="trash-2")
            ],
            h.a(
                ".uk-icon-button.uk-button-primary.uk-margin-small-right",
                href=f"/subscribe/{event.id}",  # Link dinâmico com o ID do evento
                target="_blank",  # Abre em uma nova aba
                rel="noopener noreferrer" # Segurança adicional ao abrir em nova aba  
                )[ # Botão "Abrir"
                uk_icon(icon="external-link")
            ],
            h.a(".uk-icon-button.uk-button-primary")[  # Botão "Editar"
                uk_icon(icon="pencil")
            ]
        ],
        h.div(".uk-flex.uk-flex-right.uk-width-1-1.uk-hidden@s.uk-margin-small-top")[  # Botões visíveis apenas em telas pequenas e alinhados abaixo do texto
            h.a(".uk-width-1-2.uk-icon-button.uk-button-danger.uk-margin-small-right", uk_toggle="target: #delete-event-modal")[  # Botão "Excluir"
                uk_icon(icon="trash-2")
            ],
            h.a(
                ".uk-width-1-2.uk-icon-button.uk-button-primary.uk-margin-small-right",
                href=f"/subscribe/{event.id}",  # Link dinâmico com o ID do evento
                target="_blank",  # Abre em uma nova aba
                rel="noopener noreferrer" # Segurança adicional ao abrir em nova aba
            )[  # Botão "Abrir"
                uk_icon(icon="external-link")
            ],
            h.a(".uk-width-1-2.uk-icon-button.uk-button-primary")[  # Botão "Editar"
                uk_icon(icon="pencil")
            ]
        ],
        delete_event_modal(event.id)
    ]


def eventlist(user_events: list[Event]):
    # Cria uma lista desordenada <ul> com classes que dividem os itens da lista
    if not user_events:
        return no_event()

    return h.ul(".uk-list.uk-list-divider")[
        # Itera sobre a lista de eventos do usuário (user_events)
        # Para cada evento, chama a função eventlist_item que cria o item da lista <li> correspondente
        [eventlist_item(event) for event in user_events]
    ]


def new_event_form_input(
        name: str,
        input_type: str,
        label: Optional[str] = None,
        placeholder: Optional[str] = None,
        required: bool = False,
        value: Optional[str] = None
):
    input_attrs = {
        "type": input_type,
        "name": name,
        "id": f"event-{name}",
        "class": "uk-input",
        "aria-label": f"{label}" if label else "Form input",
        "required": required
    }
    
    if placeholder:
        input_attrs["placeholder"] = placeholder
    if value:
        input_attrs["value"] = value

    # Se um label for fornecido, cria um campo com label
    if label:
        return h.div(".uk-margin")[
            h.label(".uk-form-label", for_=f"event-{name}")[label],
            h.div(".uk-form-controls")[
                h.input(**input_attrs)
            ]
        ]
    # Caso contrário, apenas cria o input sem label (para hidden, por exemplo)
    else:
        return h.input(**input_attrs)

def new_event_form(owner_id: str):
    return h.form(
        ".uk-form-stacked",
        hx_post="/API/V1/events/add",
        hx_ext="json-enc",
        hx_trigger="submit"
    )[
        new_event_form_input(label="Título", name="title", input_type="text", placeholder="Meu evento...", required=True),
        new_event_form_input(label="Descrição", name="description", input_type="text", placeholder="Um evento administrado pelo DEL.", required=False),
        new_event_form_input(label="Data", name="date", input_type="date", placeholder="17/10/2024", required=True),
        new_event_form_input(label="Duração", name="duration", input_type="number", placeholder="15 min...", required=True),
        new_event_form_input(name="owner_id", input_type="hidden", value=f"{owner_id}"),
        h.button(".uk-button.uk-button-primary.uk-width-1-1", type_="submit")["Criar"]
    ]


def new_event_modal(owner_id:str):
    return h.div("#new-event-modal.uk-modal.uk-flex-top", uk_modal="", style="z-index: 9999;")[
        h.div(".uk-modal-body.uk-modal-dialog.uk-margin-auto-vertical")[
            h.div(".uk-modal-header")[h.h2(".uk-modal-title")["Title"]],
            h.div(".uk-modal-body")[
                new_event_form(owner_id)
            ],
            h.div(".uk-modal-footer.uk-text-right")[
                h.button(".uk-modal-close.uk-button.uk-button-default", type_="button")["Cancelar"],
            ]
        ]
    ]

def DashboardPage(
        user_data: User,
        user_events: list[Event]
) -> h.Element:
    return basepage(
        page_title="Dashboard",
        content=[
            navbar(),
            h.div(".uk-section")[
                h.div(".uk-container")[
                    h.div(".uk-card.uk-card-default.uk-padding-small")[
                        h.div(".uk-card-header.uk-flex.uk-flex-between.uk-flex-stretch")[
                            h.h4(".uk-h4")[f"Eventos de {user_data.username}"],
                            h.button(".uk-button.uk-button-primary", 
                                    type_="button", 
                                    uk_toggle="target: #new-event-modal")[
                                    uk_icon(icon="plus"),"NOVO"
                            ],
                            new_event_modal(user_data.id)
                        ],
                        h.div(".uk-card-body")[eventlist(user_events)]
                    ]
                ],
            ]
        ]
    )