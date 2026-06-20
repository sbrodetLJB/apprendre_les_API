"""
API "Carnet d'adresses" - implementation FastAPI.

Cette API respecte le contrat decrit dans docs/03-api-rest-crud.md :

    GET    /contacts        -> liste des contacts
    GET    /contacts/{id}   -> un contact
    POST   /contacts        -> creer un contact
    PUT    /contacts/{id}   -> modifier un contact
    DELETE /contacts/{id}   -> supprimer un contact

Les contacts sont stockes dans le fichier contacts.json, a cote de ce fichier.
Pas de base de donnees : on lit le fichier, on modifie la liste en memoire,
on reecrit le fichier. C'est volontairement simple pour se concentrer sur l'API.
"""

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_FILE = Path(__file__).parent / "contacts.json"

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


# --- Schemas (la "forme" attendue des donnees) -----------------------------
#
# ContactIn decrit ce que le client envoie pour creer ou modifier un contact :
# pas d'id, car c'est le serveur qui l'attribue.
class ContactIn(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: Optional[str] = None


# Contact decrit ce que l'API renvoie : les memes champs, plus l'id.
class Contact(ContactIn):
    id: int


# --- Stockage : lire/ecrire le fichier JSON --------------------------------

def load_contacts() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_contacts(contacts: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)


def next_id(contacts: list[dict]) -> int:
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1


# --- Endpoints --------------------------------------------------------------

@app.get("/contacts", response_model=list[Contact])
def list_contacts():
    return load_contacts()


@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    contacts = load_contacts()
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact introuvable")


@app.post("/contacts", response_model=Contact, status_code=201)
def create_contact(new_contact: ContactIn):
    contacts = load_contacts()
    contact = {"id": next_id(contacts), **new_contact.model_dump()}
    contacts.append(contact)
    save_contacts(contacts)
    return contact


@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, updated: ContactIn):
    contacts = load_contacts()
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            contacts[index] = {"id": contact_id, **updated.model_dump()}
            save_contacts(contacts)
            return contacts[index]
    raise HTTPException(status_code=404, detail="Contact introuvable")


@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int):
    contacts = load_contacts()
    remaining = [contact for contact in contacts if contact["id"] != contact_id]
    if len(remaining) == len(contacts):
        raise HTTPException(status_code=404, detail="Contact introuvable")
    save_contacts(remaining)
    return None
