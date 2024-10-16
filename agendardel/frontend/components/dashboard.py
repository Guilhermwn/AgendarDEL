import htpy as h

from agendardel.backend.models import Event, User
from .page import basepage

uk_icon = h.Element("uk-icon")

def navbar():
    return h.nav(".uk-navbar-container.uk-padding", uk_navbar="")[

        # Navbar à esquerda
        h.div(".uk-navbar-left")[h.h3(".uk-h3")["Dashboard"]],
        
        # Navbar à direita
        h.div(".uk-navbar-right.")[

            # Imagem do avatar
            h.a[h.img(".uk-border-pill", src="https://franken-ui.dev/images/avatar.jpg", width="50", height="50")],
            
            # Dropdown 
            h.div(".uk-navbar-dropdown")[

                # Lista de opções dentro do dropdown
                h.ul(".uk-nav.uk-navbar-dropdown-nav")[
                    h.li[h.a(href="#")["Perfil"]],
                    h.li[h.a(href="/API/V1/user/logout")["Logout"]],
                ]
            ]
        ]
    ]


def eventlist_item(event: Event):
    # Cria um item de lista <li> que representará um evento
    
    return h.li[
        # Título do evento dentro de um cabeçalho <h2> com a classe .uk-h2
        h.h2(".uk-h2")[f"{event.title}"],

        # Descrição do evento dentro de um parágrafo <p> com a classe .uk-text-muted
        h.p(".uk-text-muted")[f"{event.description}"]
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
                h.div(".uk-container")[eventlist(user_events)]
            ]
        ]
    )