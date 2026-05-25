from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    api_domain: str
    base_url: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    


    DATABASE_URL: str

    SERVER_SMTP: str
    PORT_SMTP: int
    USER_SMTP: str
    PASSWORD_SMTP: str

    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    UPLOAD_DIR: str = "uploads"
    
    REDIRECT_URI: Optional[str] = None

  
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

        

