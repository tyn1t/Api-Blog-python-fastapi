from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class SectionCreate(BaseModel):
    title: str
    img_url: Optional[str] = None
    content: str 
    order: int

    
class PostCreate(BaseModel):
    title: str
    img_url: Optional[str] = None 
    description: str
    sections: list[SectionCreate] 


class SectionResponse(BaseModel):
    id: int
    title: str
    img_url: Optional[str] = None
    slug: str
    sections: List[SectionCreate] 
    
    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    id: int 
    title: str 
    img_url: str | None
    description: str
    url: str
    slug: str
    model_config = ConfigDict(from_attributes=True)
    

class PostCreateResponse(BaseModel):
    message: str
    url: str