# Carnet d'adresses — API FastAPI

Implémentation Python de l'API décrite dans [`docs/03-api-rest-crud.md`](../docs/03-api-rest-crud.md), avec le framework [FastAPI](https://fastapi.tiangolo.com/).

## Installer

```bash
cd api-fastapi
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash) ; sous macOS/Linux : source venv/bin/activate
pip install -r requirements.txt
```

## Lancer

```bash
uvicorn main:app --reload --port 8000
```

Le service écoute sur `http://localhost:8000`.

FastAPI génère automatiquement une documentation interactive de l'API : ouvrez **http://localhost:8000/docs** dans votre navigateur pour tester chaque endpoint directement, sans `curl`.

## Tester

Voir [`docs/05-tester-avec-curl.md`](../docs/05-tester-avec-curl.md) pour des exemples de commandes `curl` (utilisez le port `8000`).

## Comment c'est fait

- `main.py` contient toute l'API : les modèles de données (`ContactIn`, `Contact`), les fonctions de lecture/écriture du fichier `contacts.json`, et les 5 endpoints (`GET`, `GET /:id`, `POST`, `PUT`, `DELETE`).
- FastAPI utilise les **annotations de type** Python (`contact_id: int`, `new_contact: ContactIn`) pour valider automatiquement les données reçues et générer la documentation interactive — c'est l'un des principaux atouts de ce framework par rapport à du PHP natif (comparez avec `../api-php/`).
- Les données sont stockées dans `contacts.json`, réinitialisé à `[]` par défaut.
