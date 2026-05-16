from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from leads.models.leads import Lead
from leads.schemas.leads import LeadSchemas
from leads.utils.utils import verifica_numero, verifica_email

router = APIRouter(prefix="/leads", tags=["Leads"])


    

@router.post("/create")
async def create_lead(leads: LeadSchemas, db: Session = Depends(get_db)):
    phone = await verifica_numero(leads.phone)
    email = await verifica_email(leads.email)
    lead = Lead(
        name=leads.name,
        email=email,
        phone=phone,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
