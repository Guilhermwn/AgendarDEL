# agendardel/backend/config.py

"""
Backend API Config 
"""

from enum import Enum
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class DBServiceEnum(str, Enum):
    SQLITE = "sqlite"
    SQLITECLOUD = "sqlitecloud"

class DatabaseSettings(BaseSettings):
    """
    Configurações relacionadas ao banco de dados
    """

    DB_NAME:str = "agendardel"
    SQL_LOCAL_FILE:str = f"{DB_NAME}.db"
    

    @property
    def DB_LOCAL(self) -> str:
        """Retorna a URL do banco de dados local"""
        return f"{DBServiceEnum.SQLITE.value}:///{self.SQL_LOCAL_FILE}"

    @property
    def DB_CLOUD(self) -> str:
        """Retorna a URL do banco de dados hospedado em nuvem"""
        # DB_CLOUD_API_KEY:str = "wrp99LK1ndNslF1TvS2DDY67RhpjCq0mVdKxQyRlztk"
        DB_CLOUD_API_KEY = os.getenv("DB_CLOUD_API_KEY")
        return f"{DBServiceEnum.SQLITECLOUD.value}://cgkgccrgnz.sqlite.cloud:8860/{self.DB_NAME}?apikey={DB_CLOUD_API_KEY}"


class APISettings(BaseSettings):
    """
    Configurações relacionadas a API
    """
    API_V1:str = "/API/V1"
    API_Version: str = "0.0.1"
    FRONTEND_Version: str = "0.0.1"


class Settings(BaseSettings):
    """
    Configurações gerais da API
    """
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()


settings = Settings()