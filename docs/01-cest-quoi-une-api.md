# 1. C'est quoi une API ?

## L'analogie du restaurant

Imaginez un restaurant. Vous (le client) ne rentrez pas en cuisine pour préparer votre plat vous-même. Vous donnez votre commande à un serveur, le serveur la transmet en cuisine, la cuisine prépare le plat, et le serveur vous le rapporte.

- **Vous** = l'application qui a besoin d'une information ou d'une action (par exemple, un site web, une application mobile).
- **La cuisine** = le programme qui sait faire le travail (chercher une donnée, l'enregistrer, faire un calcul...).
- **Le serveur (humain)** = l'**API**.

Une **API** (Application Programming Interface, "interface de programmation d'application") est cet intermédiaire : elle définit comment un programme peut demander quelque chose à un autre programme, sans avoir besoin de savoir comment ce dernier fonctionne en interne.

## Pourquoi est-ce utile ?

- **Séparer les responsabilités** : celui qui fabrique l'API gère ses données et sa logique comme il veut ; celui qui l'utilise n'a pas besoin de connaître ces détails.
- **Réutiliser** : la même API peut être utilisée par un site web, une application mobile, un autre programme automatique... sans rien dupliquer.
- **Faire évoluer indépendamment** : tant que le "contrat" (ce que l'API promet de faire) ne change pas, on peut changer ce qu'il y a derrière sans casser ceux qui l'utilisent.

C'est exactement ce qu'on va vérifier dans ce dépôt : nous allons construire **la même API** avec deux technologies totalement différentes (Python/FastAPI et PHP natif), et un seul client web qui pourra parler à l'une ou à l'autre **sans aucun changement de son côté**. C'est la preuve concrète qu'une API, c'est un contrat, pas une technologie.

## API web : client et serveur

Dans ce cours, on s'intéresse aux **API web** : des API qu'on utilise à travers le réseau, avec le protocole **HTTP** (celui que votre navigateur utilise déjà pour charger des pages web).

```
[ Client ]  --- requête HTTP --->  [ Serveur / API ]
[ Client ]  <--- réponse HTTP ---  [ Serveur / API ]
```

- Le **client** envoie une **requête** : "je voudrais la liste des contacts", "ajoute ce contact", etc.
- Le **serveur** (notre API) traite la demande et renvoie une **réponse** : les données demandées, une confirmation, ou une erreur.

Dans ce projet :
- Le **client**, c'est une petite page web en JavaScript (dossier `client-web/`).
- Le **serveur**, c'est l'une de nos deux API (`api-fastapi/` ou `api-php/`).

## Ce qu'il faut retenir

- Une API est un **intermédiaire** qui permet à deux programmes de communiquer selon des règles précises.
- Une API web fonctionne par **requêtes/réponses** via le protocole HTTP.
- Le client n'a pas besoin de savoir comment l'API est construite en interne — seulement comment lui parler.

**Suite : [2. Le protocole HTTP et le format JSON](02-http-json.md)**
