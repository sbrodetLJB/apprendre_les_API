# 6. Pour aller plus loin

Ce dépôt continuera de s'enrichir. Quelques pistes pour la suite, une fois les bases de ce cours maîtrisées :

## Authentification

Comment l'API sait-elle qui fait la requête, et si cette personne a le droit de faire telle ou telle action ? Plusieurs mécanismes existent :
- **Clé API** (`x-api-key` dans un en-tête) : simple, identifie l'application appelante.
- **JWT (JSON Web Token)** : un jeton signé contenant des informations sur l'utilisateur connecté, transmis dans l'en-tête `Authorization: Bearer <jeton>`.
- **OAuth2** : un protocole standard pour déléguer l'authentification à un tiers (ex: "se connecter avec Google").

Le projet `ASSO_claude` (un autre dépôt) met en œuvre ces deux premiers mécanismes en situation réelle, si vous voulez voir du code concret.

## Validation et gestion des erreurs

Que se passe-t-il si le client envoie un email mal formé, ou oublie un champ obligatoire ? Une bonne API valide les données reçues et renvoie une erreur claire (`400 Bad Request`) avec un message explicite, plutôt que de planter ou d'enregistrer une donnée invalide.

## Pagination

Quand une collection contient des milliers d'éléments, on ne renvoie jamais tout en une seule réponse : on **pagine** (ex: `GET /contacts?page=2&limit=20`).

## Filtrage et recherche

Permettre au client de ne demander qu'un sous-ensemble des données, via des paramètres dans l'URL (ex: `GET /contacts?search=curie`).

## Versionner une API

Quand on doit changer le contrat d'une API déjà utilisée par d'autres, on évite de casser ce qui existe : on introduit une nouvelle version (ex: `/v2/contacts`) en gardant l'ancienne disponible un temps.

## D'autres technologies pour la même API

Le principe de ce dépôt (la même API réimplémentée dans plusieurs technologies) peut continuer : Node.js/Express, Java/Spring, Go, Ruby on Rails... Le contrat ne change pas, seule l'implémentation change. Si vous voulez vous entraîner, essayez d'ajouter une troisième implémentation de notre carnet d'adresses dans la technologie de votre choix, en respectant le contrat de la leçon 3.

## API et bases de données réelles

Ce cours utilise un simple fichier JSON pour rester accessible sans installation. Une vraie application utiliserait une base de données (MySQL, PostgreSQL, MongoDB...). Si ce sujet vous intéresse, regardez comment `ASSO_claude` utilise MySQL avec un ORM (TypeORM).
