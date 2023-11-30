import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistCreatorMetods import *
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# Coloca aquí tus credenciales
client_id = 'cc2ece12ff0840e68932c542a3870c46'
client_secret = '85fe48dc89d2469aa8a39ca57838e7e6'
redirect_uri = 'http://127.0.0.1:8888/callback'

# Configuración de autenticación de usuario
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-private'))

# Solicitar permisos de lectura y escritura

# Clase para manejar la solicitud HTTP de redirección
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Capturamos la URL de redirección
        url = self.path
        # Establecemos el token de acceso en el objeto sp
        sp.auth_manager.get_access_token(url)
        # Respondemos con un mensaje de éxito
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Authentication Complete</title></head><body><h1>Authentication Complete</h1><p>You can close this window now.</p></body></html>")

# Configuramos el servidor HTTP para manejar la redirección
server_address = ('', 8888)
httpd = HTTPServer(server_address, CallbackHandler)

# Abrimos automáticamente el navegador para la autenticación
webbrowser.open(sp.auth_manager.get_authorize_url())

# Manejamos las solicitudes hasta que el usuario cierre la ventana del navegador
httpd.handle_request()

# recibir playlist original
url_playlist = input('Ingresa la URL de la playlist original: ')
id_playlist = get_id_playlist(url_playlist)
playlistOriginal = sp.playlist_tracks(id_playlist, limit = 100) # playlist por paginas de 100 canciones
playlist_info = sp.playlist(id_playlist)
print(f'La playlist original es: {playlist_info["name"]}')

# elegir parámetros para la playlist
print('Cargando, no toques nada niño rata')
print('Ingresa los parámetros para la playlist nueva')
parameters = {}

# ARTISTAS
chosenArtists = artistParameter(playlistOriginal, playlist_info, sp)
parameters['artists'] = chosenArtists
artists_name = []
if chosenArtists != None and chosenArtists: # si se eligieron artistas
    for artist in chosenArtists:
        artist_info = sp.artist(artist)
        artist_name = artist_info['name']
        artists_name.append(artist_name)
    print(f'Artistas elegidos: {artists_name}')
else:
    chosenArtists = None
    print('No se eligieron artistas')

# ALBUM
chosenAlbums = albumParameter(playlistOriginal, playlist_info, sp)
parameters['albums'] = chosenAlbums
albums_name = []
if chosenAlbums != None and chosenAlbums:
    for album in chosenAlbums:
        album_info = sp.album(album)
        album_name = album_info['name']
        albums_name.append(album_name)
    print(f'Albumes elegidos: {albums_name}')
else:
    chosenAlbums = None
    print('No se eligieron albumes')

# AÑO
years = yearParameter()
parameters['years'] = years
print(f'Intervaflo de años elegido: {years}')

# POPULARIDAD
popularity = popularityParameter()
parameters['popularity'] = popularity
print(f'Popularidad mínima elegida: {popularity}')

# COVER
cover_url = coverPlaylist()
parameters['cover'] = cover_url
print(f'Cover elegido: {cover_url}')

# CREAR PLAYLIST

new_playlist = createPlaylist(parameters, sp, playlistOriginal)