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

- `main.py` contient l'API v1 : les modèles de données (`ContactIn`, `Contact`), et les 5 endpoints (`GET`, `GET /:id`, `POST`, `PUT`, `DELETE`).
- `storage.py` contient la lecture/écriture de `contacts.json`, partagée par `main.py` et `v2.py`.
- `v2.py` contient une démo de versionning + authentification JWT, montée sous `/v2` (voir [`docs/06-pour-aller-plus-loin.md`](../docs/06-pour-aller-plus-loin.md)).
- FastAPI utilise les **annotations de type** Python (`contact_id: int`, `new_contact: ContactIn`) pour valider automatiquement les données reçues et générer la documentation interactive — c'est l'un des principaux atouts de ce framework par rapport à du PHP natif (comparez avec `../api-php/`).
- Les données sont stockées dans `contacts.json`, réinitialisé à `[]` par défaut.

## Sécurité et fonctionnalités avancées

- `POST`/`PUT`/`DELETE` sur `/contacts` exigent l'en-tête `x-api-key: demo-secret-key-123` (variable d'environnement `API_KEY`).
- `GET /contacts` accepte `?search=...` (filtrage) et `?page=...&limit=...` (pagination).
- `/v2/contacts` exige un jeton JWT obtenu via `POST /v2/auth/login` (compte de démo `demo`/`demo123`), et renomme `phone` en `phoneNumber`.

Détails et exemples `curl` : [`docs/06-pour-aller-plus-loin.md`](../docs/06-pour-aller-plus-loin.md).
