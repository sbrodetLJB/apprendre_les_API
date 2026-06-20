"""
API "Carnet d'adresses" - implementation FastAPI.

Cette API respecte le contrat decrit dans docs/03-api-rest-crud.md :

    GET    /contacts        -> liste des contacts (recherche et pagination en option)
    GET    /contacts/{id}   -> un contact
    POST   /contacts        -> creer un contact (cle API requise)
    PUT    /contacts/{id}   -> modifier un contact (cle API requise)
    DELETE /contacts/{id}   -> supprimer un contact (cle API requise)

Les contacts sont stockes dans le fichier contacts.json, a cote de ce fichier.
Pas de base de donnees : on lit le fichier, on modifie la liste en memoire,
on reecrit le fichier. C'est volontairement simple pour se concentrer sur l'API.

Ce fichier met aussi en oeuvre les pistes de docs/06-pour-aller-plus-loin.md :
validation, pagination, filtrage, et securisation par cle API. La demo
JWT + versionning (piste "authentification" avancee et "versionner une API")
est dans v2.py, montee plus bas.
"""

import os
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

from storage import load_contacts, next_id, save_contacts

app = FastAPI(title="Carnet d'adresses (FastAPI)")

# Le client web (client-web/) tourne sur une autre adresse/port que cette API :
# c'est ce qu'on appelle une requete "cross-origin". Par defaut, un navigateur
# bloque ces requetes (politique CORS) sauf si le serveur autorise explicitement
# l'origine appelante. Pour ce cours, on autorise tout le monde (a ne jamais
# faire ainsi dans une vraie application en production).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Securisation : cle API ------------------------------------------------
#
# Mecanisme le plus simple decrit dans la lecon 6 : un en-tete "x-api-key"
# obligatoire pour les operations d'ecriture. La lecture reste publique.
# La cle est lue dans une variable d'environnement pour ne jamais l'ecrire
# en dur dans le code d'une vraie application ; une valeur par defaut est
# fournie ici uniquement pour que ce cours fonctionne sans configuration.
API_KEY = os.environ.get("API_KEY", "demo-secret-key-123")


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Cle API invalide ou manquante (en-tete 'x-api-key')",
        )


# --- Validation : erreurs 400 claires --------------------------------------
#
# Par defaut, FastAPI renvoie 422 quand les donnees recues ne correspondent
# pas au schema. La lecon 6 parle de 400 Bad Request : on intercepte donc
# l'erreur de validation pour renvoyer un message simple, dans le meme style
# que l'API PHP (voir api-php/index.php : validateContactInput).
@app.exception_handler(RequestValidationError)
async def on_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    return JSONResponse(
        status_code=400,
        content={"detail": f"Le champ '{field}' est invalide : {first_error['msg']}"},
    )


# --- Schemas (la "forme" attendue des donnees) -----------------------------
#
# ContactIn decrit ce que le client envoie pour creer ou modifier un contact :
# pas d'id, car c'est le serveur qui l'attribue. EmailStr valide le format de
# l'email, Field(min_length=1) refuse les champs vides.
class ContactIn(BaseModel):
    firstName: str = Field(min_length=1)
    lastName: str = Field(min_length=1)
    email: EmailStr
    phone: Optional[str] = None


# Contact decrit ce que l'API renvoie : les memes champs, plus l'id.
class Contact(ContactIn):
    id: int


# --- Endpoints --------------------------------------------------------------

@app.get("/contacts", response_model=list[Contact])
def list_contacts(search: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None):
    contacts = load_contacts()

    # Filtrage : ne garder que les contacts dont prenom/nom/email contiennent
    # le terme recherche (lecon 6, "Filtrage et recherche").
    if search:
        term = search.lower()
        contacts = [
            c
            for c in contacts
            if term in c["firstName"].lower() or term in c["lastName"].lower() or term in c["email"].lower()
        ]

    # Pagination : sans page/limit, on renvoie tout (comportement inchange
    # pour le client web). Avec les deux, on renvoie une tranche de la liste
    # (lecon 6, "Pagination").
    if page is not None and limit is not None:
        start = (page - 1) * limit
        contacts = contacts[start : start + limit]

    return contacts


@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    contacts = load_contacts()
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact introuvable")


@app.post("/contacts", response_model=Contact, status_code=201, dependencies=[Depends(require_api_key)])
def create_contact(new_contact: ContactIn):
    contacts = load_contacts()
    contact = {"id": next_id(contacts), **new_contact.model_dump()}
    contacts.append(contact)
    save_contacts(contacts)
    return contact


@app.put("/contacts/{contact_id}", response_model=Contact, dependencies=[Depends(require_api_key)])
def update_contact(contact_id: int, updated: ContactIn):
    contacts = load_contacts()
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            contacts[index] = {"id": contact_id, **updated.model_dump()}
            save_contacts(contacts)
            return contacts[index]
    raise HTTPException(status_code=404, detail="Contact introuvable")


@app.delete("/contacts/{contact_id}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_contact(contact_id: int):
    contacts = load_contacts()
    remaining = [contact for contact in contacts if contact["id"] != contact_id]
    if len(remaining) == len(contacts):
        raise HTTPException(status_code=404, detail="Contact introuvable")
    save_contacts(remaining)
    return None


# --- v2 : demo JWT + versionning -------------------------------------------
#
# Importe en dernier pour que v2.py puisse reutiliser storage.py sans import
# circulaire. Voir v2.py pour le detail (login, jeton, /v2/contacts).
from v2 import router as v2_router  # noqa: E402

app.include_router(v2_router, tags=["v2 (demo JWT + versionning)"])
