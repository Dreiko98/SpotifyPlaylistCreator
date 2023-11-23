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

# elegir parámetros para la playlist
print('Ingresa los parámetros para la playlist nueva')
parameters = {}

# ARTISTAS
artists = artistParameter(playlistOriginal, playlist_info, sp)
parameters['artists'] = artists
artists_name = []
if artists != None and artists:
    for artist in artists:
        artist_info = sp.artist(artist)
        artist_name = artist_info['name']
        artists_name.append(artist_name)
    print(f'Artistas elegidos: {artists_name}')
else:
    artists = None
    print('No se eligieron artistas')

# ALBUM
albums = albumParameter(playlistOriginal, playlist_info, sp)
parameters['albums'] = albums
albums_name = []
if albums != None and albums:
    for album in albums:
        album_info = sp.album(album)
        album_name = album_info['name']
        albums_name.append(album_name)
    print(f'Albumes elegidos: {albums_name}')
else:
    albums = None
    print('No se eligieron albumes')

# AÑO
years = yearParameter()
parameters['years'] = years
print(f'Años elegidos: {years}')

# POPULARIDAD
popularity = popularityParameter()
parameters['popularity'] = popularity
print(f'Popularidad mínima elegida: {popularity}')

# UNIVERSALES
universals = universalParameters()
parameters['universalParameters'] = universals
print(f'Parámetros universales elegidos: {universals}')

# COVER
cover_url = coverPlaylist()
parameters['cover'] = cover_url
print(f'Cover elegido: {cover_url}')

# CREAR PLAYLIST

new_playlist = createPlaylist(parameters, sp, playlistOriginal)