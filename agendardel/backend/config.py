# agendardel/backend/config.py

"""
Backenf API Config 
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME:str = "agendardel"

    SQL_LOCAL_FILE:str = f"{DB_NAME}.db"
    DB_SERVICE: list[str] = [
        "sqlite",
        "sqlitecloud"
    ]
    
    DB_LOCAL:str = f"{DB_SERVICE[0]}:///{SQL_LOCAL_FILE}"

    DB_CLOUD_API_KEY:str = "wrp99LK1ndNslF1TvS2DDY67RhpjCq0mVdKxQyRlztk"
    DB_CLOUD:str = f"{DB_SERVICE[1]}://cgkgccrgnz.sqlite.cloud:8860/agendardel?apikey={DB_CLOUD_API_KEY}"
    
    API_V1:str = "/API/V1"

    API_Version: str = "0.0.1"
    FRONTEND_Version: str = "0.0.1"

settings = Settings()