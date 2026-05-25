from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    api_domain: str
    base_url: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    upload_dir: str

  
    model_config = SettingsConfigDict(env_file=".env")

        

settings = Settings()