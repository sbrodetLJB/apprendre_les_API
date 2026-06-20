# 4. Notre projet : le carnet d'adresses

## Objectif

Construire un petit carnet d'adresses (une liste de contacts), **deux fois**, avec deux technologies serveur très différentes :

- **`api-fastapi/`** : en Python, avec le framework [FastAPI](https://fastapi.tiangolo.com/).
- **`api-php/`** : en PHP, sans framework ("PHP natif"), pour voir ce qu'un framework automatise pour nous.

Les deux respectent **exactement le même contrat** (voir la leçon précédente), et stockent leurs données dans un simple fichier JSON sur le disque (pas besoin d'installer une base de données pour suivre ce cours).

Un seul client web (`client-web/`), en HTML/JavaScript, vient ensuite consommer l'une ou l'autre de ces API — vous changerez une seule ligne de configuration pour basculer de l'une à l'autre, et tout continuera de fonctionner.

```
client-web/  (HTML + JS, dans votre navigateur)
      |
      |  requêtes HTTP (fetch)
      v
api-fastapi/  (Python, port 8000)        <-- vous choisissez l'une des deux,
   OU                                          le client ne change pas
api-php/      (PHP, port 8001)
```

## Pourquoi un fichier JSON plutôt qu'une base de données ?

Pour se concentrer sur **les API elles-mêmes** sans avoir à installer et configurer un serveur de base de données. Chaque service lit un fichier `contacts.json`, le modifie en mémoire, puis le réécrit sur le disque. C'est volontairement simple — dans un vrai projet en production, on utiliserait une base de données (comme dans le projet `ASSO_claude`, qui utilise MySQL).

## Le modèle de données

Un contact a la forme suivante :

```json
{
  "id": 1,
  "firstName": "Marie",
  "lastName": "Curie",
  "email": "marie.curie@example.com",
  "phone": "0600000000"
}
```

- `id` : un nombre entier, attribué automatiquement par le serveur à la création (le client ne le fournit jamais).
- `firstName`, `lastName`, `email` : obligatoires.
- `phone` : optionnel.

## Comment suivre ce cours

1. Lisez d'abord `api-fastapi/README.md`, lancez ce service, et testez-le avec les commandes `curl` fournies.
2. Lisez ensuite `api-php/README.md`, lancez ce second service (sur un port différent), et testez-le avec les **mêmes** commandes `curl` — vous constaterez que les réponses ont la même forme.
3. Comparez le code des deux services : même contrat, deux façons très différentes de l'implémenter.
4. Lisez `client-web/README.md`, lancez le client, et utilisez-le avec l'une puis l'autre API.

**Suite : [5. Tester une API avec curl](05-tester-avec-curl.md)**
