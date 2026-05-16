from pydantic import BaseModel

class LeadSchemas(BaseModel):
    name: str
    email: str
    phone: str
