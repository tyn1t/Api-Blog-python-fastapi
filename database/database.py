import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_CONFIG = {
    "host": "db",
    "database": "blogdb",
    "user": "postgres",
    "password":"124578",
    "port": "5432",
}

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
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