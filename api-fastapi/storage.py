"""
Stockage des contacts (fichier JSON), partage par l'API v1 (main.py) et la
demo v2 (v2.py) : les deux versions du contrat lisent/ecrivent les memes
donnees, seule leur "forme" change.
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "contacts.json"


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
