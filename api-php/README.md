# Carnet d'adresses — API PHP natif

Implémentation PHP de la même API que [`../api-fastapi/`](../api-fastapi/), **sans aucun framework**, pour voir ce qu'un framework comme FastAPI automatise habituellement (routage, validation, documentation).

## Prérequis

PHP installé (vérifiez avec `php --version` — PHP 8+ recommandé). Aucune dépendance à installer : ce projet n'utilise que le langage PHP de base.

## Lancer

PHP fournit un serveur de développement intégré, pratique pour ce genre d'exercice :

```bash
cd api-php
php -S localhost:8001
```

Le service écoute sur `http://localhost:8001`. Toutes les requêtes sont dirigées vers `index.php`, qui fait office de routeur.

## Tester

Voir [`docs/05-tester-avec-curl.md`](../docs/05-tester-avec-curl.md) pour des exemples de commandes `curl` (utilisez le port `8001` au lieu de `8000`).

## Comment c'est fait

- `index.php` contient tout : gestion CORS, lecture du corps de la requête, routage manuel (`if ($path === '/contacts' && $method === 'GET')`), validation manuelle des champs obligatoires, lecture/écriture de `contacts.json`.
- Pas de routeur automatique : on inspecte nous-mêmes `$_SERVER['REQUEST_METHOD']` et `$_SERVER['REQUEST_URI']`, et on compare avec une expression régulière pour extraire l'identifiant dans `/contacts/3`.
- Pas de validation de type automatique : on vérifie nous-mêmes que les champs obligatoires sont présents (`validateContactInput`).
- Pas de documentation générée : si vous en voulez une, il faudrait l'écrire à la main, ou utiliser un outil comme Swagger/OpenAPI séparément.

C'est exactement le même contrat que la version FastAPI, avec beaucoup plus de code écrit à la main — c'est ce que vous "payez" en choisissant de ne pas utiliser de framework, et ce qu'un framework vous "offre" en échange d'apprendre ses conventions.
