import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'tu_cliente_id'
CLIENT_SECRET = 'tu_cliente_secreto'
REDIRECT_URI = 'tu_uri_de_redireccion'

scope = 'playlist-modify-private playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Obtén la URL de autorización
auth_url = sp.auth_manager.get_authorize_url()

# Abre la URL en el navegador
webbrowser.open(auth_url)

# Pide al usuario introducir el código de autorización
code = input("Introduce el código de autorización de la URL de redirección: ")

# Obtén el token de acceso
token_info = sp.auth_manager.get_access_token(code)

# Usa el token de acceso para realizar acciones en la cuenta del usuario
sp = spotipy.Spotify(auth=token_info['access_token'])
# Realiza acciones en la cuenta del usuario aquí
