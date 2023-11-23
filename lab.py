import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistCreatorMetods import *

# Coloca aquí tus credenciales
client_id = 'cc2ece12ff0840e68932c542a3870c46'
client_secret = '85fe48dc89d2469aa8a39ca57838e7e6'
redirect_uri = 'http://localhost:8888/callback'

# Configuración de autenticación de usuario
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-private'))

# Nombre de usuario de Spotify
username = 'germanmallo44'
print(f'bienvenido a playlist creator, {username}')

# recibir playlist original
url_playlist = 'https://open.spotify.com/playlist/2T4BuGz7Sd6IwDOMxcQjic?si=c85e0012f8d74ec4'
id_playlist = get_id_playlist(url_playlist)
playlistOriginal = sp.playlist_tracks(id_playlist)
playlist_info = sp.playlist(id_playlist)
print(f'La playlist original es: {playlist_info["name"]}')

listaCanciones = extraerCanciones(playlistOriginal)
print(listaCanciones)

print("\n\n mi puta polla huele a queso\n\n")

new_playlist = sp.user_playlist_create(user=sp.me()['id'], name="esto es una prueba", public=False, description="esto es una descripción")
print(new_playlist)

print("\n\n mi puta polla huele a queso joder que alguien me pare\n\n")

añadirCanciones(listaCanciones, new_playlist, sp)
print(new_playlist['items']['track']['name'])