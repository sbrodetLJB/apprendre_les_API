<?php
/**
 * API "Carnet d'adresses" - implementation PHP natif (sans framework).
 *
 * Cette API respecte le meme contrat que api-fastapi/main.py
 * (voir docs/03-api-rest-crud.md) :
 *
 *   GET    /contacts        -> liste des contacts
 *   GET    /contacts/{id}   -> un contact
 *   POST   /contacts        -> creer un contact
 *   PUT    /contacts/{id}   -> modifier un contact
 *   DELETE /contacts/{id}   -> supprimer un contact
 *
 * Contrairement a FastAPI, PHP natif ne fournit aucun routeur, aucune
 * validation automatique, aucune generation de documentation : tout est
 * ecrit explicitement ci-dessous. C'est plus verbeux, mais cela montre
 * ce qu'un framework fait "a notre place".
 */

declare(strict_types=1);

const DATA_FILE = __DIR__ . '/contacts.json';

// --- CORS -------------------------------------------------------------
// Comme pour l'API FastAPI, on autorise toutes les origines pour ce cours.
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Le navigateur envoie une requete OPTIONS ("preflight") avant un POST/PUT/DELETE
// avec un en-tete personnalise (Content-Type: application/json), pour verifier
// que le serveur autorise bien cette requete. On y repond simplement "ok, vide".
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

header('Content-Type: application/json');

// --- Stockage : lire/ecrire le fichier JSON ----------------------------

function loadContacts(): array
{
    if (!file_exists(DATA_FILE)) {
        return [];
    }
    $content = file_get_contents(DATA_FILE);
    return json_decode($content, true) ?? [];
}

function saveContacts(array $contacts): void
{
    file_put_contents(DATA_FILE, json_encode($contacts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

function nextId(array $contacts): int
{
    if (empty($contacts)) {
        return 1;
    }
    return max(array_column($contacts, 'id')) + 1;
}

function sendJson($data, int $status = 200): void
{
    http_response_code($status);
    if ($data !== null) {
        echo json_encode($data, JSON_UNESCAPED_UNICODE);
    }
    exit;
}

function readJsonBody(): array
{
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

/**
 * Verifie que les champs obligatoires sont presents.
 * Une vraie API ferait une validation plus complete (format de l'email, etc.) :
 * on simplifie pour ce cours.
 */
function validateContactInput(array $input): ?string
{
    foreach (['firstName', 'lastName', 'email'] as $field) {
        if (empty($input[$field])) {
            return "Le champ '$field' est obligatoire";
        }
    }
    return null;
}

// --- Routage : on regarde la methode HTTP et le chemin de l'URL --------

$method = $_SERVER['REQUEST_METHOD'];

// $_SERVER['REQUEST_URI'] peut contenir une query string (?...) qu'on retire.
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// On retire un eventuel prefixe de sous-dossier et les slashs en trop,
// pour ne garder que "/contacts" ou "/contacts/3".
$path = rtrim($path, '/');

$matches = [];

if ($path === '/contacts' && $method === 'GET') {
    sendJson(loadContacts());
}

if ($path === '/contacts' && $method === 'POST') {
    $input = readJsonBody();
    $error = validateContactInput($input);
    if ($error !== null) {
        sendJson(['error' => $error], 400);
    }

    $contacts = loadContacts();
    $contact = [
        'id' => nextId($contacts),
        'firstName' => $input['firstName'],
        'lastName' => $input['lastName'],
        'email' => $input['email'],
        'phone' => $input['phone'] ?? null,
    ];
    $contacts[] = $contact;
    saveContacts($contacts);
    sendJson($contact, 201);
}

if (preg_match('#^/contacts/(\d+)$#', $path, $matches)) {
    $id = (int) $matches[1];
    $contacts = loadContacts();
    $index = null;
    foreach ($contacts as $i => $contact) {
        if ($contact['id'] === $id) {
            $index = $i;
            break;
        }
    }

    if ($method === 'GET') {
        if ($index === null) {
            sendJson(['error' => 'Contact introuvable'], 404);
        }
        sendJson($contacts[$index]);
    }

    if ($method === 'PUT') {
        if ($index === null) {
            sendJson(['error' => 'Contact introuvable'], 404);
        }
        $input = readJsonBody();
        $error = validateContactInput($input);
        if ($error !== null) {
            sendJson(['error' => $error], 400);
        }
        $contacts[$index] = [
            'id' => $id,
            'firstName' => $input['firstName'],
            'lastName' => $input['lastName'],
            'email' => $input['email'],
            'phone' => $input['phone'] ?? null,
        ];
        saveContacts($contacts);
        sendJson($contacts[$index]);
    }

    if ($method === 'DELETE') {
        if ($index === null) {
            sendJson(['error' => 'Contact introuvable'], 404);
        }
        array_splice($contacts, $index, 1);
        saveContacts($contacts);
        sendJson(null, 204);
    }
}

// Aucune route ne correspond.
sendJson(['error' => 'Route inconnue'], 404);
