import uuid
from fastapi import Request
import htpy as h

from agendardel.backend.models import Event, User
from .page import basepage

uk_icon = h.Element("uk-icon")


def navbar(host):
    return h.nav(".uk-navbar-container.uk-padding", uk_navbar="",uk_dropnav="mode: click", style="z-index: 8888;")[
        h.div(".uk-navbar-left")[h.h3(".uk-h3")["Dashboard"]],
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


def short_text(text:str, amount:int):
    return [text if len(text.split())<amount 
            else " ".join(text.split()[:amount])+"..."][0]

def delete_event_modal(event_id:uuid.UUID):
    return h.div(f"#delete-event-{event_id}-modal.uk-modal.uk-flex-top", uk_modal="", style="z-index: 9999;")[
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
            h.a(".uk-icon-button.uk-button-danger.uk-margin-small-right", uk_toggle=f"target: #delete-event-{event.id}-modal")[  # Botão "Excluir"
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
            h.a(".uk-icon-button.uk-button-primary", href=f"/dashboard/{event.id}/edit")[  # Botão "Editar"
                uk_icon(icon="pencil")
            ]
        ],
        h.div(".uk-flex.uk-flex-right.uk-width-1-1.uk-hidden@s.uk-margin-small-top")[  # Botões visíveis apenas em telas pequenas e alinhados abaixo do texto
            h.a(".uk-width-1-2.uk-icon-button.uk-button-danger.uk-margin-small-right", uk_toggle=f"target: #delete-event-{event.id}-modal")[  # Botão "Excluir"
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
            h.a(".uk-width-1-2.uk-icon-button.uk-button-primary", href=f"/dashboard/{event.id}/edit")[  # Botão "Editar"
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

def breadcrumb(itens: dict[str,str]):
    return h.div(".uk-container.uk-margin")[
        h.nav(aria_label="Breadcrumb")[
            h.ul(".uk-breadcrumb")[
                [ h.li[h.a(href=item[1])[item[0]]] for item in itens.items()],
            ]
        ]
    ],

def DashboardPage(
        user_data: User,
        user_events: list[Event],
        request: Request
) -> h.Element:
    return basepage(
        page_title="Dashboard",
        content=[
            navbar(request.base_url),
            breadcrumb({
                "Dashboard": ""
            }),
            h.div(".uk-container.uk-margin-bottom")[
                h.div(".uk-card.uk-card-default.uk-padding-small")[
                    h.div(".uk-card-header.uk-flex.uk-flex-between.uk-flex-stretch")[
                        h.h4(".uk-h4")[f"Eventos de {user_data.username}"],
                        h.a(".uk-button.uk-button-primary", href="/dashboard/new-event")[
                                uk_icon(icon="plus"),"NOVO"
                        ],
                    ],
                    h.div(".uk-card-body")[eventlist(user_events)],
                ]
            ],
        ]
    )