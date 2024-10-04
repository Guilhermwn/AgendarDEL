import htpy as h
from markupsafe import Markup
uk_theme_switcher = h.Element("uk-theme-switcher")
uk_icon = h.Element("uk-icon")

STYLE_SETTINGS = [
    h.link(rel="stylesheet", href="https://unpkg.com/franken-ui@1.1.0/dist/css/core.min.css"),
    h.script(src="https://unpkg.com/franken-ui@1.1.0/dist/js/core.iife.js", type="module"),
    h.script(src="https://unpkg.com/franken-ui@1.1.0/dist/js/icon.iife.js", type="module"),
    h.script(src="https://unpkg.com/htmx.org@2.0.2"),
    h.style[
        Markup("""
        :root {
            font-family: Inter, sans-serif;
            font-feature-settings: "liga" 1, "calt" 1; /* fix for Chrome */
        }
        @supports (font-variation-settings: normal) {
            :root {
            font-family: InterVariable, sans-serif;
            }
        }
        """)
    ],
    h.script[
        Markup("""
        const htmlElement = document.documentElement;

        if (
            localStorage.getItem("mode") === "dark" ||
            (!("mode" in localStorage) &&
            window.matchMedia("(prefers-color-scheme: dark)").matches)
        ) {
            htmlElement.classList.add("dark");
        } else {
            htmlElement.classList.remove("dark");
        }

        htmlElement.classList.add(
            localStorage.getItem("theme") || "uk-theme-zinc"
        );
        """)
    ]
]

def basehead(page_title:str=None, extra_head:h.Node = None):
    return h.head[
        h.meta(charset="utf-8"),
        h.meta(name="viewport", content="width=device-width, initial-scale=1"),
        STYLE_SETTINGS,
        h.title[f"AgendarDEL - {page_title}" if page_title else "AgendarDEL"],
        extra_head if extra_head else None
    ]

def theme_settings():
    return h.div()[
        h.a(".uk-button.uk-button-default", href="#theme-switcher-modal", uk_toggle="")[
            uk_icon(icon="palette", uk_cloak="")
        ],
        h.div("#theme-switcher-modal.uk-modal", uk_modal="")[
            h.div(".uk-modal-dialog")[
                h.button(".uk-modal-close-default", _type="button", uk_close=""),
                h.div(".uk-modal-header")[
                    h.div(".uk-modal-title")["Customize"]
                ],h.div(".uk-modal-body")[uk_theme_switcher]
            ]
        ]
    ]

def basepage(page_title:str=None, extra_head:h.Node=None,content:h.Node=None) -> h.Element:
    return h.html(lang="pt-BR")[
        basehead(page_title, extra_head),
        h.body(".bg-background.text-foreground")[
            content,
        ]
    ]