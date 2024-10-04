from fastapi.responses import Response
import typing
import htpy as h
import bs4

def h_render(element:h.Node) -> str:
    """
    Recebe: Um elemento qualquer Node HTPY\n
    Retorna: Uma string HTML formatada e identada do elemento HTPY
    """
    s = h.render_node(element)
    formatter = bs4.formatter.HTMLFormatter(indent=2)
    string = bs4.BeautifulSoup(s, features="html.parser")
    return string.prettify(formatter=formatter)

# class HTPYResponse(Response):
#     media_type = "text/html"

#     def __init__(self, content: h.Node, status_code: int = 200):
#         html_content = h_render(content)
#         super().__init__(content=html_content, status_code=status_code)


class HTPYResponse(Response):
    media_type = "text/html"

    def render(self, content:h.Node) -> bytes:
        return h_render(content).encode('utf-8')

