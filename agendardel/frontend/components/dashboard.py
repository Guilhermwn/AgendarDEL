import htpy as h

from agendardel.backend.models import Event, User
from .page import basepage

uk_icon = h.Element("uk-icon")


def navbar():
    return h.nav(".uk-navbar-container.uk-padding", uk_navbar="",uk_dropnav="mode: click", style="z-index: 9999; position: relative")[
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
            else " ".join(text.split()[:amount])+"..."]


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
                    short_text(event.description, 6)  # Descrição do evento
                ]
            ]
        ],
        h.div(".uk-flex.uk-flex-right.uk-width-auto.uk-visible@s")[  # Botões visíveis apenas em telas grandes
            h.button(".uk-icon-button.uk-button-danger.uk-margin-small-right")[  # Botão "Excluir"
                uk_icon(icon="trash-2")
            ],
            h.button(".uk-icon-button.uk-button-primary")[  # Botão "Editar"
                uk_icon(icon="pencil")
            ]
        ],
        h.div(".uk-flex.uk-flex-right.uk-width-1-1.uk-hidden@s.uk-margin-small-top")[  # Botões visíveis apenas em telas pequenas e alinhados abaixo do texto
            h.button(".uk-width-1-2.uk-icon-button.uk-button-danger.uk-margin-small-right")[  # Botão "Excluir"
                uk_icon(icon="trash-2")
            ],
            h.button(".uk-width-1-2.uk-icon-button.uk-button-primary")[  # Botão "Editar"
                uk_icon(icon="pencil")
            ]
        ]
    ]


def eventlist(user_events: list[Event]):
    # Cria uma lista desordenada <ul> com classes que dividem os itens da lista
    
    return h.ul(".uk-list.uk-list-divider")[
        # Itera sobre a lista de eventos do usuário (user_events)
        # Para cada evento, chama a função eventlist_item que cria o item da lista <li> correspondente
        [eventlist_item(event) for event in user_events]
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
                        h.div(".uk-card-header")[
                            h.p[f"Eventos de {user_data.username}"]],
                        h.div(".uk-card-body")[eventlist(user_events)]
                    ]
                ],
            ]
        ]
    )