from pydantic import BaseModel, EmailStr, ConfigDict, Field


class CadastroSchemas(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    
  
        
class LoginSchemas(BaseModel):
    username: EmailStr
    password: str
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class RefreshTokenSchemas(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class UserResponseSchemas(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class CadastroMessageResponses(BaseModel):
    message: str
    status: int


