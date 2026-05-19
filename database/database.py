import time
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()



DATABASE_URL = os.getenv("DATABASE_URL")


for _ in range(10):
    try:
        engine = create_engine(DATABASE_URL)
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