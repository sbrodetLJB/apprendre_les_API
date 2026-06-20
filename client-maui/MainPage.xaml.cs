using System.Collections.ObjectModel;
using CarnetAdresses.Maui.Models;
using CarnetAdresses.Maui.Services;
using CarnetAdresses.Maui.Pages;

namespace CarnetAdresses.Maui;

public partial class MainPage : ContentPage
{
    private readonly ContactsApiClient _api = new() { BaseUrl = ApiEndpoints.All[0].BaseUrl };
    private readonly ObservableCollection<AddressBookContact> _contacts = [];

    public MainPage()
    {
        InitializeComponent();
        ContactsList.ItemsSource = _contacts;

        ApiPicker.ItemsSource = ApiEndpoints.All.Select(endpoint => endpoint.Label).ToList();
        ApiPicker.SelectedIndex = 0;
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await RefreshContactsAsync();
    }

    private void OnApiChanged(object? sender, EventArgs e)
    {
        _api.BaseUrl = ApiEndpoints.All[ApiPicker.SelectedIndex].BaseUrl;
        _ = RefreshContactsAsync();
    }

    private void OnSearchPressed(object? sender, EventArgs e) => _ = RefreshContactsAsync();

    private void OnRefreshing(object? sender, EventArgs e) => _ = RefreshContactsAsync();

    private async Task RefreshContactsAsync()
    {
        HideError();
        try
        {
            var contacts = await _api.GetContactsAsync(SearchBarControl.Text);
            _contacts.Clear();
            foreach (var contact in contacts)
            {
                _contacts.Add(contact);
            }
        }
        catch (Exception ex) when (ex is ApiClientException or HttpRequestException)
        {
            ShowError(ex.Message);
        }
        finally
        {
            RefreshViewControl.IsRefreshing = false;
        }
    }

    private async void OnAddClicked(object? sender, EventArgs e) =>
        await Navigation.PushAsync(new ContactFormPage(_api, contact: null));

    private async void OnEditClicked(object? sender, EventArgs e)
    {
        if (sender is Button { CommandParameter: AddressBookContact contact })
        {
            await Navigation.PushAsync(new ContactFormPage(_api, contact));
        }
    }

    private async void OnDeleteClicked(object? sender, EventArgs e)
    {
        if (sender is not Button { CommandParameter: AddressBookContact contact })
        {
            return;
        }

        var confirmed = await DisplayAlert(
            "Confirmer la suppression",
            $"Supprimer {contact.DisplayName} ?",
            "Supprimer",
            "Annuler");
        if (!confirmed)
        {
            return;
        }

        try
        {
            await _api.DeleteContactAsync(contact.Id);
            await RefreshContactsAsync();
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
