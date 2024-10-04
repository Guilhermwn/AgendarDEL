import htpy as h
from .page import basepage

uk_icon = h.Element("uk-icon")

def FormInput(
        flip:bool=False, 
        icon:str=None,
        label:str="",
        _type:str="text",
        input_name:str=""
) -> h.Element:
    icon_flip = "uk-form-icon-flip" if flip else "None"
    input_id = f"id-{label}-input"
    return h.div(".uk-margin.uk-margin-small-top")[
        h.label(".uk-form-label", _for=input_id)[label],
        h.div(".uk-inline.uk-width-1-1")[
            (h.span(f".uk-form-icon {icon_flip}")[uk_icon(icon=icon)] if icon else None),
            h.input(
                f"#{input_id}.uk-input", 
                type=_type, 
                name=input_name, 
                aria_label="Not clickable icon", 
                required=""
            )
        ]
    ]

def Form(title:str, inputs:list[dict]):
    form_inputs = []
    for input in inputs:
        label = input.get("label", "")
        icon = input.get("icon", "")
        _type = input.get("type", "")
        name = input.get("name", "")
        form_inputs.append(FormInput(icon=icon, label=label, _type=_type, input_name=name))
            
    return h.form(
        f"#form-{title}-id.uk-form-stacked",
        hx_post="/API/V1/user/register",
        hx_headers='{"Content-Type": "application/json"}',
        hx_ext="json-enc",
        hx_trigger="submit", 
        hx_swap="outerHTML",
        hx_target=f"#response-{title.lower()}",
    )[
        form_inputs,
        h.button(".uk-button.uk-button-default.uk-width-1-1", type="submit")[title]
    ]


def AuthTabs():
    return h.ul(".uk-tab-alt.uk-margin-medium",uk_switcher="")[
        h.li(".uk-active")[h.a(".px-4.pb-3.pt-2", href="#")["Login"]],
        h.li[h.a(".px-4.pb-3.pt-2", href="#")["Signup"]],
    ]


def AuthSwitcher():
    return h.ul(".uk-switcher.mt-5")[
        h.li[
            Form(title="Login", inputs=[
                {"label":"Username", "icon":"User"},
                {"label":"Password", "icon":"key-round", "type":"password"}
            ])],
        h.li[
            Form(title="Signup", inputs=[
                {"label":"Username", "icon":"user","name":"username"},
                {"label":"Email", "icon":"mail", "type": "email", "name":"email"},
                {"label":"Password", "icon":"key-round", "type":"password", "name":"password"}
            ]),
            h.div("#response-signup")
            ],
    ]

def AuthPage() -> h.Element:
    return basepage(
        extra_head=[
            h.comment("Extra Head"),
            h.script(src="https://unpkg.com/htmx-ext-json-enc@2.0.1/json-enc.js"),
            h.script[
                """
                document.body.addEventListener('htmx:afterSwap', function(evt) {
                    const form = document.querySelector("#my-form");
                    form.reset();
                });
                """
            ]
        ],
        content=[
            h.div(".uk-flex.uk-flex-center.uk-flex-middle.uk-background-muted")[
                h.div(".uk-width-large")[
                    h.div(".uk-section.uk-height-viewport")[
                        h.div(".uk-container")[
                            h.div(".uk-card.uk-card-default")[
                                h.div(".uk-card-body")[
                                    AuthTabs(),
                                    h.comment("===== FORMULÁRIO ====="),
                                    AuthSwitcher(),
                                    h.comment("===== FIM FORMULÁRIO ====="),
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ])