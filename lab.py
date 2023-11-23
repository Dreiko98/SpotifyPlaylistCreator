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

song1 = listaCanciones[3]
print(f'\nsong1: {song1}\n')
song_info = sp.track(song1).keys()
print(f'song_info: {song_info} \n')
songAlbum = sp.track(song1)['album']
print(f'type(songAlbum){type(songAlbum)}\n') #lista

for artist in songAlbum:
    print(artist['name'])
    print(artist['id'])

"""for song in listaCanciones:
    nameSong = sp.track(song)['name']
    #obtener artista de la cancion teniendo la id de la cancion
    artist = sp.track(song).keys()
    print(nameSong)
    for artist in artist:
        artist = artist['name']
    print(artist)"""