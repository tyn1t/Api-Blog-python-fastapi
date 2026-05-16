from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from auth.auth import HashPassword, create_access_token, create_refresh_token, security, blacklist, token_refresh
from database.database import get_db

from users.models.users import User
from users.schemas.users import CadastroSchemas, LoginResponse, LoginSchemas, RefreshTokenSchemas

router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.post("/register", status_code=201)
def register(credentials: CadastroSchemas, db: Session = Depends(get_db)):
    try:
        user_exixteng = db.query(User.email).filter(User.email == credentials.email).first()
        if user_exixteng:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        user = User(
            name = credentials.name, 
            email = credentials.email, 
            password = HashPassword().hash_password(credentials.password) 
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
        "message": "Usuário criado com sucesso",
        "status": status.HTTP_201_CREATED
    }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no cadastro {e}")

@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginSchemas,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.username).first()

    if not user or not HashPassword().verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id,
            "jti": str(uuid.uuid4())
        }
    )
    
    refreshtoken = create_refresh_token(
        data={
            "sub": user.email,
            "id": user.id,
            "jti": str(uuid.uuid4())
        }
    )
    
    return {
        "access_token": token,
        "refresh_token":refreshtoken,
        "token_type": "bearer"
    }
    
    

@router.post("/logout", name="Logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    blacklist.add(token)
    
    return {"message": "Logout bem-sucedido"}

@router.post("/refresh-token", name="Refresh Token", response_model=RefreshTokenSchemas)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    return token_refresh(token, db)