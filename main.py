
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from config import Settings

from users.route import users
from gmail.router import envia
from post.route import post
from leads.route import leads
from post.route import post_teste
from routers import google_auth

from database.database import Base, engine

from pathlib import Path

from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

settings = Settings()

Base_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = Base_DIR / settings.UPLOAD_DIR

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def hello_test(): 
    return {"MENSSAGEM":"oLA MUNDO"}

@app.get("/info")
def set_domin():
    return {"domain": settings.api_domain, "url": settings.base_url, "path-img": UPLOAD_DIR}

app.include_router(users.router)
app.include_router(post.router)
app.include_router(leads.router)
app.include_router(envia.router)
app.include_router(google_auth.router)


# img 
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# teste post 
app.include_router(post_teste.router)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)