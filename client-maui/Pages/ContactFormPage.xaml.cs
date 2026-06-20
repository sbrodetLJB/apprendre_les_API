using CarnetAdresses.Maui.Models;
using CarnetAdresses.Maui.Services;

namespace CarnetAdresses.Maui.Pages;

// Une seule page pour creer ET modifier un contact, comme le formulaire
// unique de client-web/index.html : la difference est juste la presence
// (ou non) d'un contact existant passe au constructeur.
public partial class ContactFormPage : ContentPage
{
    private readonly ContactsApiClient _api;
    private readonly AddressBookContact? _editedContact;

    public ContactFormPage(ContactsApiClient api, AddressBookContact? contact)
    {
        InitializeComponent();
        _api = api;
        _editedContact = contact;

        Title = contact is null ? "Ajouter un contact" : $"Modifier {contact.DisplayName}";
        SaveButton.Text = contact is null ? "Ajouter" : "Enregistrer";

        if (contact is not null)
        {
            FirstNameEntry.Text = contact.FirstName;
            LastNameEntry.Text = contact.LastName;
            EmailEntry.Text = contact.Email;
            PhoneEntry.Text = contact.Phone;
        }
    }

    private async void OnSaveClicked(object? sender, EventArgs e)
    {
        HideError();

        var contact = new AddressBookContact
        {
            FirstName = FirstNameEntry.Text?.Trim() ?? string.Empty,
            LastName = LastNameEntry.Text?.Trim() ?? string.Empty,
            Email = EmailEntry.Text?.Trim() ?? string.Empty,
            Phone = string.IsNullOrWhiteSpace(PhoneEntry.Text) ? null : PhoneEntry.Text.Trim(),
        };

        try
        {
            if (_editedContact is null)
            {
                await _api.CreateContactAsync(contact);
            }
            else
            {
                await _api.UpdateContactAsync(_editedContact.Id, contact);
            }

            await Navigation.PopAsync();
        }
        catch (Exception ex) when (ex is ApiClientException or HttpRequestException)
        {
            ShowError(ex.Message);
        }
    }

    private void ShowError(string message)
    {
        ErrorLabel.Text = message;
        ErrorLabel.IsVisible = true;
    }

    private void HideError() => ErrorLabel.IsVisible = false;
}
