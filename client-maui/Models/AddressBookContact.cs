using System.Text.Json.Serialization;

namespace CarnetAdresses.Maui.Models;

// Memes champs que le contrat decrit dans docs/03-api-rest-crud.md. Les
// JsonPropertyName font correspondre les proprietes C# (PascalCase, convention
// .NET) aux noms JSON envoyes par les deux API (camelCase, convention JS/JSON).
//
// Nomme "AddressBookContact" plutot que "Contact" : MAUI definit deja un type
// Contact (Microsoft.Maui.ApplicationModel.Communication, pour lire le carnet
// d'adresses du telephone) importe globalement dans tout le projet.
public class AddressBookContact
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("firstName")]
    public string FirstName { get; set; } = string.Empty;

    [JsonPropertyName("lastName")]
    public string LastName { get; set; } = string.Empty;

    [JsonPropertyName("email")]
    public string Email { get; set; } = string.Empty;

    [JsonPropertyName("phone")]
    public string? Phone { get; set; }

    public string DisplayName => $"{FirstName} {LastName}";

    public string DisplaySubtitle => Phone is null ? Email : $"{Email} — {Phone}";
}
