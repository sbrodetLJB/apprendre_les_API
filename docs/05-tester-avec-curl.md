# 5. Tester une API avec curl

Avant d'écrire le moindre client web, il est essentiel de savoir tester une API "à la main", sans interface graphique. L'outil le plus simple pour ça est `curl`, disponible en ligne de commande sur la plupart des systèmes (y compris dans Git Bash sur Windows).

Cette leçon utilise l'API FastAPI (port `8000`) comme exemple — remplacez `8000` par `8001` pour tester l'API PHP, les commandes sont identiques.

## Lire la liste des contacts (`GET`)

```bash
curl http://localhost:8000/contacts
```

Par défaut, `curl` fait une requête `GET`. La réponse est le tableau JSON de tous les contacts.

## Lire un seul contact (`GET` avec un identifiant)

```bash
curl http://localhost:8000/contacts/1
```

Si l'identifiant n'existe pas, vous recevrez une réponse avec le code `404`. Ajoutez `-i` à la commande pour voir les en-têtes et le code de statut de la réponse :

```bash
curl -i http://localhost:8000/contacts/999
```

## Créer un contact (`POST`)

```bash
curl -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" \
  -H "x-api-key: demo-secret-key-123" \
  -d '{"firstName":"Marie","lastName":"Curie","email":"marie.curie@example.com"}'
```

- `-X POST` : utilise la méthode `POST` au lieu de `GET`.
- `-H "Content-Type: application/json"` : précise que le corps de la requête est du JSON.
- `-H "x-api-key: ..."` : les écritures sont protégées par une clé API (voir [6. Pour aller plus loin](06-pour-aller-plus-loin.md)) ; sans elle, vous recevrez un `401`.
- `-d '...'` : le corps de la requête (les données envoyées).

La réponse contient le contact créé, avec son `id` généré par le serveur.

## Modifier un contact (`PUT`)

```bash
curl -X PUT http://localhost:8000/contacts/1 \
  -H "Content-Type: application/json" \
  -H "x-api-key: demo-secret-key-123" \
  -d '{"firstName":"Marie","lastName":"Curie","email":"marie.curie@example.com","phone":"0600000000"}'
```

## Supprimer un contact (`DELETE`)

```bash
curl -X DELETE http://localhost:8000/contacts/1 -H "x-api-key: demo-secret-key-123"
```

Cette commande ne renvoie pas de contenu (code `204`).

## Exercice

1. Démarrez l'API FastAPI (voir `api-fastapi/README.md`).
2. Listez les contacts (la liste devrait être vide au départ).
3. Créez deux ou trois contacts avec `curl`.
4. Listez à nouveau les contacts pour vérifier qu'ils ont bien été enregistrés.
5. Modifiez l'un d'entre eux, puis supprimez-en un autre.
6. Refaites les mêmes étapes sur l'API PHP (port `8001`) : vous devriez obtenir des réponses de la même forme.

**Suite : [6. Pour aller plus loin](06-pour-aller-plus-loin.md)**
