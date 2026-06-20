"""
Demo "v2" du carnet d'adresses : illustre deux pistes de la lecon 6 en une fois.

- Versionning : le champ "phone" devient "phoneNumber". C'est exactement le
  genre de changement de contrat qui casserait les clients existants si on le
  faisait directement sur /contacts -> on l'introduit dans une nouvelle
  version, /v2/contacts, en laissant /contacts (v1) inchange.
- Authentification JWT : au lieu de la simple cle API de la v1 (un secret
  partage), on obtient un jeton nominatif via /v2/auth/login, signe par le
  serveur, valable un temps limite, et on le transmet dans l'en-tete
  "Authorization: Bearer <jeton>".

Compte de demonstration (en dur, jamais ainsi en production) :
  username = "demo", password = "demo123"

Volontairement incomplet (lecture + creation seulement) : modifier ce module
pour ajouter PUT/DELETE en v2 est un bon exercice, dans l'esprit de la lecon 6.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, EmailStr

from storage import load_contacts, next_id, save_contacts

# Comme pour API_KEY dans main.py, ce secret devrait venir d'une variable
# d'environnement et jamais etre commite en clair dans une vraie application.
JWT_SECRET = os.environ.get("JWT_SECRET", "demo-jwt-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo123"

router = APIRouter(prefix="/v2")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ContactInV2(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: Optional[str] = None


class ContactV2(ContactInV2):
    id: int


def to_v2(contact: dict) -> dict:
    """Traduit un contact stocke (v1, champ "phone") vers la forme v2."""
    return {
        "id": contact["id"],
        "firstName": contact["firstName"],
        "lastName": contact["lastName"],
        "email": contact["email"],
        "phoneNumber": contact.get("phone"),
    }


def to_v1(contact_v2: dict) -> dict:
    """Traduit en sens inverse, pour ecrire dans le meme stockage que la v1."""
    return {
        "firstName": contact_v2["firstName"],
        "lastName": contact_v2["lastName"],
        "email": contact_v2["email"],
        "phone": contact_v2.get("phoneNumber"),
    }


@router.post("/auth/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    if credentials.username != DEMO_USERNAME or credentials.password != DEMO_PASSWORD:
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MINUTES)
    token = jwt.encode({"sub": credentials.username, "exp": expire}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return TokenResponse(access_token=token)


def require_jwt(authorization: Optional[str] = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="En-tete 'Authorization: Bearer <jeton>' manquant (obtenez un jeton via /v2/auth/login)",
        )
    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Jeton invalide ou expire")
    return payload["sub"]


@router.get("/contacts", response_model=list[ContactV2])
def list_contacts_v2(user: str = Depends(require_jwt)):
    return [to_v2(c) for c in load_contacts()]


@router.post("/contacts", response_model=ContactV2, status_code=201)
def create_contact_v2(new_contact: ContactInV2, user: str = Depends(require_jwt)):
    contacts = load_contacts()
    contact = {"id": next_id(contacts), **to_v1(new_contact.model_dump())}
    contacts.append(contact)
    save_contacts(contacts)
    return to_v2(contact)
