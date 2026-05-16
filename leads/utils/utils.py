import re
from fastapi import HTTPException


async def verifica_numero(numero: str):
    padrao = r"^\(?\d{2}\)?\s?9\d{4}-?\d{4}$"

    if not re.fullmatch(padrao, numero):
        raise HTTPException(
            status_code=400,
            detail="Número inválido"
        )

    return numero


async def verifica_email(email: str):
    padrao_email = r"^[\w\.-]+@gmail\.com$"

    if not re.fullmatch(padrao_email, email):
        raise HTTPException(
            status_code=400,
            detail="Email inválido"
        )

    return email

