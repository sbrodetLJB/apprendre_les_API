# 7. Un client lourd et un client mobile, avec .NET MAUI

Jusqu'ici, un seul type de client a consommé nos API : un navigateur web (`client-web/`). Cette leçon ajoute deux autres types de clients, construits à partir du **même code** : un **client lourd** (une application installée sur le poste de travail, ici Windows) et un **client mobile** (une application Android). C'est le projet [`client-maui/`](../client-maui/).

## Client web, client lourd, client mobile : quelle différence ?

| Type de client | Exemple dans ce cours | Où s'exécute-t-il ? | Comment il consomme l'API |
|---|---|---|---|
| Client web | `client-web/` | Dans le navigateur, téléchargé à chaque visite | `fetch` en JavaScript |
| Client lourd | `client-maui/` (cible Windows) | Installé sur le poste, lancé comme n'importe quel logiciel | `HttpClient` en C# |
| Client mobile | `client-maui/` (cible Android) | Installé sur le téléphone/tablette | `HttpClient` en C# |

Dans les trois cas, **la leçon centrale ne change pas** : un client n'est qu'un programme qui envoie des requêtes HTTP vers une API et affiche les réponses. Ce qui change, c'est le langage, l'environnement d'exécution, et l'interface utilisateur — jamais le contrat de l'API (revoir la leçon 3 si besoin).

## Pourquoi .NET MAUI ?

[.NET MAUI](https://learn.microsoft.com/dotnet/maui/) (Multi-platform App UI) permet d'écrire une seule base de code (C# + XAML) et de la compiler pour plusieurs plateformes : Windows, macOS, Android, iOS. C'est l'occasion de montrer concrètement qu'un client lourd et un client mobile peuvent partager énormément de code — dans ce cours, **tout** le code est partagé : `client-maui/MainPage.xaml(.cs)`, `client-maui/Pages/ContactFormPage.xaml(.cs)` et `client-maui/Services/ContactsApiClient.cs` tournent à l'identique sur les deux plateformes.

## Le client API (`Services/ContactsApiClient.cs`)

Comparez ce fichier à `client-web/app.js` : les mêmes cinq opérations (`GetContacts`, `CreateContact`, `UpdateContact`, `DeleteContact`, et la lecture d'un seul contact), simplement écrites avec `HttpClient` au lieu de `fetch`. La clé API (`x-api-key`, voir la leçon 6) est envoyée de la même façon, sur les mêmes en-têtes.

## Une difficulté propre au mobile : `localhost`

Sur le client lourd (Windows) comme sur le client web (navigateur), `http://localhost:8000` désigne la machine qui exécute le client — la vôtre, là où tournent aussi `api-fastapi`/`api-php` pendant que vous suivez ce cours. **Un émulateur Android, lui, tourne dans sa propre machine virtuelle** : pour lui, `localhost` désignerait l'émulateur, pas votre machine. L'émulateur Android expose votre machine hôte à l'adresse spéciale `10.0.2.2` — c'est ce que `Services/ApiEndpoints.cs` utilise automatiquement selon la plateforme :

```csharp
private static string Host => DeviceInfo.Platform == DevicePlatform.Android ? "10.0.2.2" : "localhost";
```

Sur un vrai téléphone Android (pas un émulateur), il faudrait remplacer cette adresse par l'adresse IP locale de votre machine sur le réseau Wi-Fi (ex. `192.168.1.42`) — un bon exercice si vous voulez aller plus loin.

## Lancer le projet

Voir [`client-maui/README.md`](../client-maui/README.md) pour les instructions détaillées (prérequis, commandes). En résumé :

1. Démarrez une des deux API (`api-fastapi` ou `api-php`), comme dans les leçons précédentes.
2. `dotnet build -t:Run -f net9.0-windows10.0.19041.0` pour lancer le client lourd, **ou** déployez sur un émulateur/appareil Android avec `-f net9.0-android`.
3. Choisissez l'API dans le menu déroulant en haut de l'écran — comme dans `client-web/`.

## Ce qui est volontairement absent

Pas de stockage hors-ligne, pas de notification push, pas de tests automatisés : l'objectif est de montrer le strict nécessaire pour qu'un client lourd/mobile parle à une API REST, pas de couvrir tout ce qu'une vraie application mobile ferait. Ce sont de bons exercices pour qui veut approfondir.
