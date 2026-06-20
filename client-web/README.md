# Carnet d'adresses — client web

Une page HTML/JavaScript "vanilla" (sans framework ni outil de build) qui consomme l'API carnet d'adresses — au choix, la version [FastAPI](../api-fastapi/) ou la version [PHP natif](../api-php/), via le menu déroulant en haut de la page.

## Lancer

Ce client doit être servi par un petit serveur HTTP (ouvrir `index.html` directement avec `file://` fonctionne dans certains navigateurs mais pas tous, à cause des règles de sécurité du navigateur). Le plus simple, avec Python déjà installé pour `api-fastapi` :

```bash
cd client-web
python -m http.server 5500
```

Puis ouvrez **http://localhost:5500** dans votre navigateur.

Démarrez au préalable au moins l'une des deux API (voir leurs README respectifs) :
- FastAPI sur `http://localhost:8000`
- PHP natif sur `http://localhost:8001`

## Comment c'est fait

- `index.html` : la structure de la page (formulaire d'ajout/modification, liste des contacts, sélecteur d'API).
- `app.js` : toute la logique — appels à l'API avec `fetch`, mise à jour de la page. Chaque fonction d'appel (`fetchContacts`, `createContact`, `updateContact`, `deleteContact`) correspond exactement à une ligne du tableau de contrat dans [`docs/03-api-rest-crud.md`](../docs/03-api-rest-crud.md).
- `style.css` : mise en forme minimale.

## Le point clé à observer

Changez la valeur du menu déroulant "API utilisée" : la liste se recharge depuis l'autre serveur, sans qu'aucune ligne de `app.js` n'ait besoin de changer en dehors de l'URL de base. C'est la démonstration concrète qu'un client web ne dépend que du **contrat** de l'API (les URL, les méthodes, la forme du JSON), jamais de sa technologie d'implémentation.
