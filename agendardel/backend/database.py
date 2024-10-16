from sqlmodel import SQLModel, create_engine
from agendardel.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(url=settings.database.DB_LOCAL, connect_args=connect_args)
# engine = create_engine(url=settings.database.DB_CLOUD)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)