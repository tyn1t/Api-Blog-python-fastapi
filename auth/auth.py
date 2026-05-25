import os
import uuid
from dotenv import load_dotenv
from passlib.context import CryptContext

from datetime import datetime, timedelta, UTC, timezone
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from users.models.users import RefreshToken, User
from database.database import get_db

security = HTTPBearer()

blacklist = set()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

class HashPassword:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @classmethod
    def hash_password(cls, password: str):
        return cls.pwd_context.hash(password)
    
    @classmethod
    def verify_password(cls, password: str, hashed: str):
        return cls.pwd_context.verify(password, hashed)


def create_access_token(data: dict, expires_delta: timedelta = None, auth_method="password"):
    to_encode = data.copy()
     
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({
        "exp": expire,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "auth_method": auth_method
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(days=7)

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4())
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
def credentials_exception():
    return HTTPException(
        status_code=401,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"}
    )

def token_refresh(token: str, db: Session):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("sub") is None or payload.get("id") is None:
            raise credentials_exception()

        existing = db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()

        if not existing:
            refresh = RefreshToken(
                user_id=payload.get("id"),
                token=token
            )

            db.add(refresh)
            db.commit()

        new_access_token = create_access_token(
            data={
                "sub": payload.get("sub"),
                "id": payload.get("id")
            }
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise credentials_exception()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        user_id = payload.get("id")
        jti = payload.get("jti")
        token_type = payload.get("type")

        if not email or not user_id:
            raise credentials_exception()

        if token_type != "access":
            raise credentials_exception()

        if jti in blacklist:
            raise credentials_exception()

    except JWTError:
        raise credentials_exception()

    user = db.query(User).filter(
        User.id == user_id,
        User.email == email
    ).first()

    if not user:
        raise credentials_exception()

    return user