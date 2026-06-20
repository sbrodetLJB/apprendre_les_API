// Client web du carnet d'adresses.
//
// Ce script ne dépend d'aucune bibliothèque ni d'aucun outil de build :
// du JavaScript "vanilla", chargé directement par le navigateur, pour
// rester concentré sur l'essentiel : comment un client web parle à une API.

// --- Éléments de la page --------------------------------------------------

const apiBaseUrlSelect = document.getElementById('api-base-url');
const form = document.getElementById('contact-form');
const formTitle = document.getElementById('form-title');
const contactIdInput = document.getElementById('contact-id');
const firstNameInput = document.getElementById('firstName');
const lastNameInput = document.getElementById('lastName');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const submitButton = document.getElementById('submit-button');
const cancelButton = document.getElementById('cancel-button');
const errorMessage = document.getElementById('error-message');
const contactsList = document.getElementById('contacts-list');

// L'URL de base de l'API change selon le menu déroulant : c'est la SEULE
// chose qui change quand on bascule de FastAPI à PHP natif.
function getApiBaseUrl() {
  return apiBaseUrlSelect.value;
}

// Clé API attendue par les deux implémentations (voir leçon 6, "Authentification")
// pour les opérations d'écriture. ATTENTION pédagogique : une clé codée en dur
// dans du JS exécuté côté navigateur est visible par n'importe qui (View Source,
// outils de développement) — cela ne protège que les endpoints de démonstration
// de ce cours, jamais une vraie application avec de vrais utilisateurs.
const DEMO_API_KEY = 'demo-secret-key-123';

// --- Affichage des erreurs ------------------------------------------------

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function clearError() {
  errorMessage.hidden = true;
  errorMessage.textContent = '';
}

// --- Appels à l'API --------------------------------------------------------
//
// `fetch` est la fonction native du navigateur pour faire des requêtes HTTP.
// Elle renvoie une "promesse" (Promise), qu'on peut lire avec `await` à
// l'intérieur d'une fonction déclarée `async`.

async function fetchContacts() {
  const response = await fetch(`${getApiBaseUrl()}/contacts`);
  if (!response.ok) {
    throw new Error(`Erreur ${response.status} en récupérant les contacts`);
  }
  return response.json();
}

async function createContact(contact) {
  const response = await fetch(`${getApiBaseUrl()}/contacts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': DEMO_API_KEY },
    body: JSON.stringify(contact),
  });
  if (!response.ok) {
    throw new Error(`Erreur ${response.status} en créant le contact`);
  }
  return response.json();
}

async function updateContact(id, contact) {
  const response = await fetch(`${getApiBaseUrl()}/contacts/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'x-api-key': DEMO_API_KEY },
    body: JSON.stringify(contact),
  });
  if (!response.ok) {
    throw new Error(`Erreur ${response.status} en modifiant le contact`);
  }
  return response.json();
}

async function deleteContact(id) {
  const response = await fetch(`${getApiBaseUrl()}/contacts/${id}`, {
    method: 'DELETE',
    headers: { 'x-api-key': DEMO_API_KEY },
  });
  if (!response.ok) {
    throw new Error(`Erreur ${response.status} en supprimant le contact`);
  }
}

// --- Affichage de la liste --------------------------------------------------

function renderContacts(contacts) {
  contactsList.innerHTML = '';

  if (contacts.length === 0) {
    contactsList.innerHTML = '<li>Aucun contact pour le moment.</li>';
    return;
  }

  for (const contact of contacts) {
    const item = document.createElement('li');

    const text = document.createElement('span');
    text.textContent = `${contact.firstName} ${contact.lastName} — ${contact.email}${contact.phone ? ` — ${contact.phone}` : ''}`;
    item.appendChild(text);

    const editButton = document.createElement('button');
    editButton.textContent = 'Modifier';
    editButton.addEventListener('click', () => startEditing(contact));
    item.appendChild(editButton);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Supprimer';
    deleteButton.addEventListener('click', () => handleDelete(contact.id));
    item.appendChild(deleteButton);

    contactsList.appendChild(item);
  }
}

async function refreshContacts() {
  try {
    clearError();
    const contacts = await fetchContacts();
    renderContacts(contacts);
  } catch (error) {
    showError(error.message);
  }
}

// --- Formulaire : créer ou modifier -----------------------------------------

function startEditing(contact) {
  contactIdInput.value = contact.id;
  firstNameInput.value = contact.firstName;
  lastNameInput.value = contact.lastName;
  emailInput.value = contact.email;
  phoneInput.value = contact.phone ?? '';

  formTitle.textContent = `Modifier le contact n°${contact.id}`;
  submitButton.textContent = 'Enregistrer';
  cancelButton.hidden = false;
}

function stopEditing() {
  contactIdInput.value = '';
  form.reset();

  formTitle.textContent = 'Ajouter un contact';
  submitButton.textContent = 'Ajouter';
  cancelButton.hidden = true;
}

async function handleSubmit(event) {
  event.preventDefault();
  clearError();

  const contact = {
    firstName: firstNameInput.value,
    lastName: lastNameInput.value,
    email: emailInput.value,
    phone: phoneInput.value || undefined,
  };

  try {
    if (contactIdInput.value) {
      await updateContact(contactIdInput.value, contact);
    } else {
      await createContact(contact);
    }
    stopEditing();
    await refreshContacts();
  } catch (error) {
    showError(error.message);
  }
}

async function handleDelete(id) {
  try {
    clearError();
    await deleteContact(id);
    await refreshContacts();
  } catch (error) {
    showError(error.message);
  }
}

// --- Initialisation -----------------------------------------------------

form.addEventListener('submit', handleSubmit);
cancelButton.addEventListener('click', stopEditing);
apiBaseUrlSelect.addEventListener('change', refreshContacts);

refreshContacts();
