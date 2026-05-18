import time
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{ os.getenv("USER")}:{os.getenv("PASSWORD")}"
    f"@{os.getenv("HOST")}:{os.getenv("POST")}/{os.getenv("DATABASE")}"
)

for _ in range(10):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        conn = engine.connect()
        conn.close()
        break
    except Exception: 
        print("Aguardando banco de dado")
        time.sleep(3)

SessionLocal = sessionmaker(
    autocommit=False,
    bind=engine
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()