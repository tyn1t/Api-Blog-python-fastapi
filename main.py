from fastapi import FastAPI


from config import settings

from users.route import users 
from post.route import post
from leads.route import leads
from post.route import post_teste

from database.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/info")
def set_domin():
    return {"domain": settings.api_domain, "url": settings.base_url}

app.include_router(users.router)
app.include_router(post.router)
app.include_router(leads.router)


# teste post 
app.include_router(post_teste.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)