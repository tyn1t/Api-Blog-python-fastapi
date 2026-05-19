from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    api_domain: str
    base_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    upload_dir: str
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

        

settings = Settings()