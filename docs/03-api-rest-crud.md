# 3. Anatomie d'une API REST

## REST, c'est quoi ?

**REST** (REpresentational State Transfer) est un style d'architecture pour concevoir des API web. Ce n'est pas une technologie ni une norme stricte, mais un ensemble de conventions largement adoptées qui rendent une API prévisible et facile à utiliser. L'idée centrale : on manipule des **ressources** (des "choses" : un contact, une commande, un article...) via des **URL**, en utilisant les méthodes HTTP vues dans la leçon précédente.

## Les ressources et leurs URL

Une **ressource** est représentée par une URL. Pour notre carnet d'adresses, la ressource est "un contact" ou "la collection de contacts" :

| URL | Représente |
|---|---|
| `/contacts` | La collection de tous les contacts |
| `/contacts/1` | Le contact dont l'identifiant est `1` |

Convention importante : les noms de ressources sont au **pluriel** et ne décrivent pas une action (on ne fait pas `/getContacts` ou `/createContact` — l'action est portée par la méthode HTTP, pas par l'URL).

## CRUD : les quatre opérations de base

CRUD est un acronyme : **C**reate, **R**ead, **U**pdate, **D**elete (créer, lire, modifier, supprimer). C'est ce que l'on veut faire avec n'importe quelle donnée, et REST associe naturellement chaque opération à une méthode HTTP :

| Opération CRUD | Méthode + URL | Effet |
|---|---|---|
| Create | `POST /contacts` | Crée un nouveau contact |
| Read (liste) | `GET /contacts` | Renvoie tous les contacts |
| Read (un seul) | `GET /contacts/1` | Renvoie le contact n°1 |
| Update | `PUT /contacts/1` | Remplace le contact n°1 par les nouvelles données envoyées |
| Delete | `DELETE /contacts/1` | Supprime le contact n°1 |

C'est exactement le contrat que nos deux API (`api-fastapi/` et `api-php/`) vont implémenter à l'identique.

## Sans état (stateless)

Un principe important de REST : chaque requête doit contenir **toute l'information nécessaire** pour être traitée, indépendamment des requêtes précédentes. Le serveur ne "se souvient" pas que vous avez consulté la liste des contacts il y a deux minutes — si le client a besoin de cette information à nouveau, il doit la redemander.

Cela simplifie beaucoup les choses : on peut redémarrer le serveur, le dupliquer sur plusieurs machines, etc., sans casser le fonctionnement.

## Le contrat de notre carnet d'adresses

Voici le contrat exact que respectent les deux implémentations de ce projet — c'est ce qui permettra à notre client web de fonctionner avec l'une ou l'autre sans modification :

| Méthode | URL | Body envoyé | Réponse |
|---|---|---|---|
| `GET` | `/contacts` | — | `200` + tableau de contacts |
| `GET` | `/contacts/{id}` | — | `200` + un contact, ou `404` si inexistant |
| `POST` | `/contacts` | `{ firstName, lastName, email, phone? }` | `201` + le contact créé (avec son `id`) |
| `PUT` | `/contacts/{id}` | `{ firstName, lastName, email, phone? }` | `200` + le contact mis à jour, ou `404` |
| `DELETE` | `/contacts/{id}` | — | `204`, ou `404` si inexistant |

`phone` est optionnel (le `?` l'indique) ; les autres champs sont obligatoires.

**Suite : [4. Notre projet : le carnet d'adresses](04-notre-projet-carnet-adresses.md)**
