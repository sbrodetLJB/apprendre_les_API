using System.Net.Http.Json;
using CarnetAdresses.Maui.Models;

namespace CarnetAdresses.Maui.Services;

// Erreur levee quand l'API repond par un code d'erreur (400, 401, 404...),
// avec un message lisible a afficher a l'utilisateur.
public class ApiClientException : Exception
{
    public ApiClientException(string message) : base(message) { }
}

// Client HTTP vers l'API "carnet d'adresses" (FastAPI ou PHP, au choix) :
// chaque methode correspond exactement a une ligne du contrat decrit dans
// docs/03-api-rest-crud.md, comme client-web/app.js le fait en JavaScript.
public class ContactsApiClient
{
    // Meme cle que client-web/app.js et la meme valeur par defaut que les deux
    // API (voir docs/06-pour-aller-plus-loin.md) : les ecritures sont protegees.
    private const string ApiKey = "demo-secret-key-123";

    private readonly HttpClient _http = new();

    public required string BaseUrl { get; set; }

    public async Task<List<AddressBookContact>> GetContactsAsync(string? search = null)
    {
        var url = $"{BaseUrl}/contacts";
        if (!string.IsNullOrWhiteSpace(search))
        {
            url += $"?search={Uri.EscapeDataString(search)}";
        }

        using var response = await _http.GetAsync(url);
        await EnsureSuccessAsync(response, "recuperation des contacts");
        return await response.Content.ReadFromJsonAsync<List<AddressBookContact>>() ?? [];
    }

    public async Task<AddressBookContact> CreateContactAsync(AddressBookContact contact)
    {
        using var request = NewWriteRequest(HttpMethod.Post, $"{BaseUrl}/contacts", contact);
        using var response = await _http.SendAsync(request);
        await EnsureSuccessAsync(response, "creation du contact");
        return await ReadContactAsync(response);
    }

    public async Task<AddressBookContact> UpdateContactAsync(int id, AddressBookContact contact)
    {
        using var request = NewWriteRequest(HttpMethod.Put, $"{BaseUrl}/contacts/{id}", contact);
        using var response = await _http.SendAsync(request);
        await EnsureSuccessAsync(response, "modification du contact");
        return await ReadContactAsync(response);
    }

    public async Task DeleteContactAsync(int id)
    {
        using var request = new HttpRequestMessage(HttpMethod.Delete, $"{BaseUrl}/contacts/{id}");
        request.Headers.Add("x-api-key", ApiKey);
        using var response = await _http.SendAsync(request);
        await EnsureSuccessAsync(response, "suppression du contact");
    }

    private static HttpRequestMessage NewWriteRequest(HttpMethod method, string url, AddressBookContact contact)
    {
        var request = new HttpRequestMessage(method, url) { Content = JsonContent.Create(contact) };
        request.Headers.Add("x-api-key", ApiKey);
        return request;
    }

    private static async Task<AddressBookContact> ReadContactAsync(HttpResponseMessage response) =>
        await response.Content.ReadFromJsonAsync<AddressBookContact>()
        ?? throw new ApiClientException("Reponse vide inattendue de l'API");

    private static async Task EnsureSuccessAsync(HttpResponseMessage response, string action)
    {
        if (response.IsSuccessStatusCode)
        {
            return;
        }

        var body = await response.Content.ReadAsStringAsync();
        throw new ApiClientException($"Erreur {(int)response.StatusCode} lors de la {action} : {body}");
    }
}
