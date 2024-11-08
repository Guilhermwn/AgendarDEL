# agendardel/main.py

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from agendardel.backend.database import create_db_and_tables
from agendardel.config import settings
from agendardel import backend
from agendardel import frontend
from agendardel.logger import logger


async def lifespan(app: FastAPI):
    logger.info("Inicializando a aplicação e criando banco de dados")
    create_db_and_tables()
    yield
    # log de finalização
    logger.info("Finalizando a aplicação")

app = FastAPI(
    title="AgendarDEL",
    description="Aplicação Full Stack AgendarDEL | Frontend + Backend",
    version=settings.api.API_Version,
    contact={
        "name": "Guilhermwn",
        "email": "guilhermwn.franco@gmail.com",
        "url": "https://guilhermwn.vercel.app"
    },
    lifespan=lifespan,
    redoc_url=None,
    # docs_url=None
)

assets = Path(__file__).parent/"assets"

app.mount("/static", StaticFiles(directory=assets), name="static")
logger.info("Static files adicionados")

app.include_router(frontend.main.router)
app.include_router(backend.main.router, prefix=settings.api.API_V1)
