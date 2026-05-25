from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    api_domain: str
    base_url: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    upload_dir: str
  
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

        

settings = Settings()