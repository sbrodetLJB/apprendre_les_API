# 2. Le protocole HTTP et le format JSON

## HTTP, le langage commun

HTTP (HyperText Transfer Protocol) est le protocole utilisé pour échanger des informations sur le web. Chaque échange est composé d'une **requête** envoyée par le client et d'une **réponse** renvoyée par le serveur.

### Les méthodes HTTP

Une requête HTTP indique une **méthode**, qui précise l'intention du client. Pour une API REST (voir leçon suivante), quatre méthodes couvrent presque tous les besoins :

| Méthode | Intention | Exemple chez nous |
|---|---|---|
| `GET` | Lire une donnée, sans rien modifier | Récupérer la liste des contacts |
| `POST` | Créer une nouvelle donnée | Ajouter un nouveau contact |
| `PUT` | Modifier une donnée existante (en entier) | Mettre à jour un contact |
| `DELETE` | Supprimer une donnée | Supprimer un contact |

### Les codes de statut

Chaque réponse HTTP contient un **code de statut** à 3 chiffres, qui dit si tout s'est bien passé et, sinon, pourquoi.

| Code | Signification | Exemple |
|---|---|---|
| `200 OK` | Tout s'est bien passé | La liste des contacts est renvoyée |
| `201 Created` | Une ressource a été créée | Le nouveau contact a été enregistré |
| `204 No Content` | Tout s'est bien passé, rien à renvoyer | Le contact a été supprimé |
| `400 Bad Request` | La requête du client est incorrecte | Un champ obligatoire manque |
| `404 Not Found` | La ressource demandée n'existe pas | Le contact avec cet identifiant n'existe pas |
| `500 Internal Server Error` | Le serveur a rencontré une erreur inattendue | Un bug côté serveur |

La règle d'or : **le premier chiffre donne la catégorie**. `2xx` = succès, `4xx` = erreur du côté du client, `5xx` = erreur du côté du serveur.

### Les en-têtes (headers)

En plus du contenu, une requête ou une réponse transporte des **en-têtes** : des informations complémentaires. Par exemple :
- `Content-Type: application/json` : "le contenu que j'envoie/renvoie est au format JSON".
- `Authorization: Bearer <jeton>` : "voici mon jeton d'authentification" (on verra cela dans une leçon ultérieure).

## JSON, le format d'échange

**JSON** (JavaScript Object Notation) est un format de texte simple pour représenter des données structurées. C'est devenu le format standard pour les API web, car il est à la fois lisible par un humain et facile à traiter par un programme.

Exemple de contact en JSON :

```json
{
  "id": 1,
  "firstName": "Marie",
  "lastName": "Curie",
  "email": "marie.curie@example.com",
  "phone": "0600000000"
}
```

Et une liste de contacts, c'est simplement un tableau d'objets JSON :

```json
[
  { "id": 1, "firstName": "Marie", "lastName": "Curie", "email": "marie.curie@example.com" },
  { "id": 2, "firstName": "Albert", "lastName": "Einstein", "email": "albert.einstein@example.com" }
]
```

Les types disponibles en JSON sont volontairement simples : texte (`"..."`), nombre (`42`, `3.14`), booléen (`true`/`false`), `null`, objet (`{ ... }`), et tableau (`[ ... ]`).

## Mettre tout ça ensemble

Quand notre client web voudra créer un contact, il enverra une requête comme ceci :

```
POST /contacts
Content-Type: application/json

{ "firstName": "Marie", "lastName": "Curie", "email": "marie.curie@example.com" }
```

Et l'API répondra par exemple :

```
201 Created
Content-Type: application/json

{ "id": 1, "firstName": "Marie", "lastName": "Curie", "email": "marie.curie@example.com" }
```

**Suite : [3. Anatomie d'une API REST](03-api-rest-crud.md)**
