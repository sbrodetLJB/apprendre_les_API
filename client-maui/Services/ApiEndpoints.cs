namespace CarnetAdresses.Maui.Services;

// Construit les URL de base des deux API, en tenant compte d'une difference
// importante entre Windows et Android : sur Windows, "localhost" designe la
// machine qui execute l'app (le client lourd) -- exactement comme dans le
// navigateur pour client-web/. Mais un appareil Android tourne sur sa propre
// machine (physique ou virtuelle) : pour lui, "localhost" designerait
// l'appareil lui-meme, pas la machine hote ou tournent les API. L'emulateur
// Android expose la machine hote a l'adresse speciale 10.0.2.2 (voir la doc
// Microsoft) -- c'est ce qu'on utilise ici. Sur un appareil physique, il
// faudrait remplacer cette adresse par l'IP locale de la machine hote sur
// le reseau Wi-Fi (ex : 192.168.1.12).
public static class ApiEndpoints
{
    private static string Host = DeviceInfo.Platform == DevicePlatform.Android ? "10.0.2.2" : "localhost";

    public static IReadOnlyList<(string Label, string BaseUrl)> All { get; } = new[]
    {
        ("FastAPI", $"http://{Host}:8000"),
        ("PHP natif", $"http://{Host}:8001"),
    };
}
