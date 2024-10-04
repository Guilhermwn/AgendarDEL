from pydantic_settings import SettingsConfigDict
from sqlmodel import SQLModel, create_engine
from .config import settings
connect_args = {"check_same_thread": False}
# engine = create_engine(url=settings.DB_CLOUD, connect_args=connect_args)
engine = create_engine(url=settings.DB_CLOUD)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)