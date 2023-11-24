import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configura las credenciales de la API de Spotify
client_credentials_manager = SpotifyClientCredentials(client_id='tu_client_id', client_secret='tu_client_secret')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ID de la playlist que deseas extraer
playlist_id = 'tu_playlist_id'

# Número máximo de elementos por página (máximo 100 según la API de Spotify)
items_per_page = 100

# Realiza la primera solicitud para obtener la primera página de elementos
results = sp.playlist_tracks(playlist_id, limit=items_per_page) # objeto tipo dict

# Procesa los elementos de la primera página
for item in results['items']:
    # Realiza la operación que necesites con cada elemento
    print(item['track']['name'])

# Verifica si hay más páginas y realiza solicitudes adicionales si es necesario
while results['next']: # Mientras haya páginas adicionales
    results = sp.next(results) # Solicitud para obtener la página siguiente
    for item in results['items']:
        # Realiza la operación que necesites con cada elemento de las páginas adicionales
        print(item['track']['name'])