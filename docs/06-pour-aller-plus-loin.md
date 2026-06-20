# 6. Pour aller plus loin

Les pistes ci-dessous ne sont plus seulement théoriques : elles sont implémentées dans `api-fastapi/` et `api-php/` (sauf mention contraire), avec les mêmes garanties qu'ailleurs dans ce cours : même contrat, même comportement sur les deux API.

## Authentification

Comment l'API sait-elle qui fait la requête, et si cette personne a le droit de faire telle ou telle action ? Ce cours met en œuvre deux mécanismes différents, à deux endroits différents, pour montrer leur différence concrète.

### Clé API (v1)

Les opérations d'écriture (`POST`, `PUT`, `DELETE` sur `/contacts`) exigent un en-tête `x-api-key`. La lecture (`GET`) reste publique. C'est le mécanisme le plus simple : un secret partagé entre le serveur et l'application appelante.

```bash
# Sans cle -> 401
curl -i -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Marie","lastName":"Curie","email":"marie.curie@example.com"}'

# Avec la cle de demonstration -> 201
curl -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" \
  -H "x-api-key: demo-secret-key-123" \
  -d '{"firstName":"Marie","lastName":"Curie","email":"marie.curie@example.com"}'
```

La clé (`demo-secret-key-123`) vient d'une variable d'environnement (`API_KEY` côté FastAPI, constante `API_KEY` côté PHP) avec une valeur par défaut pour que ce cours fonctionne sans configuration — **une vraie application ne mettrait jamais sa clé en dur dans le code**.

Le client web (`client-web/app.js`) envoie cette clé sur ses requêtes d'écriture. C'est l'occasion d'observer une limite importante : ouvrez les outils de développement du navigateur (onglet réseau, ou simplement le code source de `app.js`) et vous verrez la clé en clair. **Une clé API codée dans du JavaScript exécuté côté navigateur n'est pas un secret** — n'importe quel visiteur peut la lire. Ce mécanisme convient pour protéger un script serveur-à-serveur ou une démonstration, jamais une application avec de vrais utilisateurs.

### JWT (v2, démo FastAPI)

C'est exactement cette limite que JWT corrige : au lieu d'un secret partagé visible côté client, chaque utilisateur s'authentifie (`/v2/auth/login`) et reçoit un **jeton signé par le serveur**, valable un temps limité, qu'il transmet ensuite dans l'en-tête `Authorization: Bearer <jeton>`. Le serveur vérifie la signature à chaque requête, sans avoir besoin de se souvenir de qui est connecté (toujours le principe *stateless* de la leçon 3).

```bash
# Connexion (compte de demonstration : demo / demo123)
curl -X POST http://localhost:8000/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
# -> {"access_token":"eyJ...", "token_type":"bearer"}

# Utilisation du jeton
curl http://localhost:8000/v2/contacts \
  -H "Authorization: Bearer eyJ..."
```

Voir `api-fastapi/v2.py`. Cette démo est volontairement limitée à la lecture et à la création — ajouter `PUT`/`DELETE` en `/v2` est un bon exercice. Ce n'est pas implémenté en PHP natif (il faudrait une bibliothèque externe, ex. `firebase/php-jwt` via Composer) : un projet pour qui veut s'entraîner.

### OAuth2

OAuth2 va un cran plus loin que JWT : c'est un protocole standard pour déléguer l'authentification à un **tiers** ("se connecter avec Google/GitHub..."), plutôt que de gérer soi-même des mots de passe. Un fournisseur d'identité (Google, etc.) authentifie l'utilisateur et délivre un jeton (souvent un JWT) que votre API accepte. Ce cours ne l'implémente pas — la complexité (enregistrement de l'application auprès du fournisseur, flux de redirection, etc.) dépasse le cadre d'un projet pédagogique sans serveur public. Si ce sujet vous intéresse, regardez comment `ASSO_claude` (un autre dépôt) le met en œuvre en situation réelle.

## Validation et gestion des erreurs

Les deux API valident désormais les données reçues : les champs `firstName`/`lastName` ne peuvent pas être vides, et `email` doit être un email syntaxiquement valide (`pydantic[email]` côté FastAPI, `filter_var(..., FILTER_VALIDATE_EMAIL)` côté PHP). Une donnée invalide renvoie `400 Bad Request` avec un message explicite, sur le même modèle dans les deux implémentations :

```bash
curl -i -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" -H "x-api-key: demo-secret-key-123" \
  -d '{"firstName":"Bad","lastName":"Email","email":"pas-un-email"}'
# -> 400 {"detail":"Le champ 'email' est invalide : ..."}
```

Côté FastAPI, ceci passe par un `exception_handler` qui transforme le `422` par défaut de FastAPI en `400`, pour rester cohérent avec le contrat décrit ici et avec la réponse PHP (`{"error": "..."}`).

## Pagination

`GET /contacts` accepte deux paramètres optionnels, `page` et `limit` ; sans eux, le comportement est inchangé (toute la liste, pour ne pas casser le client web) :

```bash
curl "http://localhost:8000/contacts?page=1&limit=20"
curl "http://localhost:8001/contacts?page=2&limit=20"
```

## Filtrage et recherche

`GET /contacts` accepte aussi un paramètre `search`, qui filtre sur le prénom, le nom ou l'email (recherche insensible à la casse, sur une sous-chaîne) :

```bash
curl "http://localhost:8000/contacts?search=curie"
```

`search` et la pagination se combinent (le filtrage s'applique avant la pagination).

## Versionner une API

La démo `/v2/contacts` (FastAPI) sert aussi d'exemple de versionning : le champ `phone` y devient `phoneNumber`, un changement de contrat qui aurait cassé tous les clients existants s'il avait été fait directement sur `/contacts`. En introduisant une nouvelle version plutôt qu'en modifiant l'existante, `/contacts` (v1) continue de fonctionner sans aucun changement pour le client web — observez `client-web/app.js` : il n'a pas besoin d'être modifié pour que ce cours fonctionne encore.

## D'autres technologies pour la même API

Le principe de ce dépôt (la même API réimplémentée dans plusieurs technologies) peut continuer : Node.js/Express, Java/Spring, Go, Ruby on Rails... Le contrat ne change pas, seule l'implémentation change. Si vous voulez vous entraîner, essayez d'ajouter une troisième implémentation de notre carnet d'adresses dans la technologie de votre choix, en respectant le contrat de la leçon 3 — et, maintenant, la sécurisation par clé API décrite plus haut.

## API et bases de données réelles

Ce cours utilise un simple fichier JSON pour rester accessible sans installation. Une vraie application utiliserait une base de données (MySQL, PostgreSQL, MongoDB...). Si ce sujet vous intéresse, regardez comment `ASSO_claude` utilise MySQL avec un ORM (TypeORM).

**Suite : [7. Un client lourd et un client mobile, avec .NET MAUI](07-client-lourd-et-mobile-maui.md)**
