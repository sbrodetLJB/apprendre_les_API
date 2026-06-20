# Carnet d'adresses — client lourd et mobile (.NET MAUI)

Une application [.NET MAUI](https://learn.microsoft.com/dotnet/maui/) qui consomme l'API carnet d'adresses — au choix, la version [FastAPI](../api-fastapi/) ou la version [PHP natif](../api-php/), via le menu déroulant en haut de l'écran — exactement comme [`client-web/`](../client-web/), mais cette fois en tant qu'application **installée** plutôt que dans un navigateur.

Ce projet ne cible que deux plateformes pour rester focalisé sur la leçon :
- **Windows** : le "client lourd".
- **Android** : le client mobile.

Voir [`docs/07-client-lourd-et-mobile-maui.md`](../docs/07-client-lourd-et-mobile-maui.md) pour les explications complètes.

## Prérequis

- Le SDK .NET 9.
- Les *workloads* MAUI installés : `dotnet workload install maui-windows android` (déjà fournis par Visual Studio si vous avez installé la charge de travail ".NET Multi-platform App UI development").
- Pour la cible Android : un émulateur configuré (via Android Studio / le gestionnaire d'appareils virtuels de Visual Studio), ou un appareil physique en mode développeur.

## Lancer

Démarrez au préalable au moins l'une des deux API (voir leurs README respectifs) :
- FastAPI sur `http://localhost:8000`
- PHP natif sur `http://localhost:8001`

### Client lourd (Windows)

```bash
cd client-maui
dotnet build -t:Run -f net9.0-windows10.0.19041.0
```

### Client mobile (Android)

```bash
cd client-maui
dotnet build -t:Run -f net9.0-android
```

Cette commande déploie sur l'émulateur ou l'appareil Android actuellement sélectionné. Si aucun n'est démarré, lancez d'abord un émulateur (Visual Studio : menu "Outils > Android > Gestionnaire de périphériques", ou Android Studio : "Device Manager").

**Important** : sur l'émulateur Android, `localhost` désigne l'émulateur lui-même, pas votre machine — l'application utilise automatiquement `10.0.2.2` à la place quand elle détecte qu'elle tourne sur Android (voir `Services/ApiEndpoints.cs`). Sur un appareil physique, il faudrait remplacer cette adresse par l'IP locale de votre machine sur le réseau Wi-Fi.

## Comment c'est fait

- `Models/AddressBookContact.cs` : la forme d'un contact, identique au contrat de [`docs/03-api-rest-crud.md`](../docs/03-api-rest-crud.md). Nommé `AddressBookContact` plutôt que `Contact` pour ne pas entrer en conflit avec le type `Contact` que MAUI fournit déjà (lecture du carnet d'adresses du téléphone — une fonctionnalité que ce cours n'utilise pas).
- `Services/ContactsApiClient.cs` : les appels HTTP vers l'API, avec `HttpClient` — l'équivalent C# de `client-web/app.js`.
- `Services/ApiEndpoints.cs` : construit les URL de base des deux API, en gérant la différence Windows/Android décrite plus haut.
- `MainPage.xaml(.cs)` : la liste des contacts, le sélecteur d'API, la recherche, les boutons Modifier/Supprimer.
- `Pages/ContactFormPage.xaml(.cs)` : le formulaire d'ajout/modification (une seule page pour les deux usages, comme `client-web/index.html`).

## Le point clé à observer

Changez la valeur du menu déroulant "API utilisée" : la liste se recharge depuis l'autre serveur, sans qu'aucune ligne de `Services/ContactsApiClient.cs` n'ait besoin de changer en dehors de l'URL de base — même démonstration que pour `client-web/`. Et en comparant ce dossier à `client-web/`, vous verrez que **la logique métier** (quelles requêtes envoyer, quand, avec quelles données) se traduit presque ligne à ligne d'un langage à l'autre ; ce qui change vraiment, c'est la construction de l'interface (HTML/CSS vs XAML).
